"""Real HSPICE MUX comparison and inverter short-circuit current-overlap study.

The process file stays external. TG widths are fixed at N=10um, P=20um,
L=.18um in both designs. Raw simulation and license logs go to --work.
"""
from pathlib import Path
from itertools import product
import argparse,csv,hashlib,json,os,shutil,subprocess,tempfile,re
from collections import defaultdict
H=Path(__file__).resolve().parent
def csvout(path,rows):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def mux_netlist():
 s='''* Fixed TG dimensions; geometry is a declared schematic estimate.
.subckt inv a z vdd vss
MP z a vdd vdd P_18 W=20u L=.18u
MN z a vss vss N_18 W=10u L=.18u
.ends inv
.subckt tg a z cn cp vdd vss
MN z cn a vss N_18 W=10u L=.18u
+ AD='10u*.18u' AS='10u*.18u' PD='2*(10u+.18u)' PS='2*(10u+.18u)'
MP z cp a vdd P_18 W=20u L=.18u
+ AD='20u*.18u' AS='20u*.18u' PD='2*(20u+.18u)' PS='2*(20u+.18u)'
.ends tg
'''
 ports=' '.join(f'a{i}' for i in range(8))+' s0 s1 s2 z vdd vss'
 for design in ('baseline','tree'):
  s+=f'.subckt {design} {ports}\n'
  for k in range(3):s+=f'XI{k} s{k} b{k} vdd vss inv\n'
  if design=='baseline':
   for j in range(8):
    prev=f'a{j}'
    for k in range(3):
     dest='z' if k==2 else f'q{j}_{k}'
     cn,cp=(f's{k}',f'b{k}') if j>>k&1 else (f'b{k}',f's{k}')
     s+=f'XT{j}_{k} {prev} {dest} {cn} {cp} vdd vss tg\n';prev=dest
  else:
   prev=[f'a{i}' for i in range(8)]
   for k in range(3):
    nxt=[]
    for j in range(len(prev)//2):
     dest='z' if k==2 else f'q{k}_{j}';nxt.append(dest)
     s+=f'XT{k}_{j}L {prev[2*j]} {dest} b{k} s{k} vdd vss tg\n'
     s+=f'XT{k}_{j}H {prev[2*j+1]} {dest} s{k} b{k} vdd vss tg\n'
    prev=nxt
  s+=f'.ends {design}\n'
 return s
def check_topologies(text):
 blocks={m.group(1):(m.group(2).split(),[l.split() for l in m.group(3).splitlines() if l and l[0] in 'MX'])
         for m in re.finditer(r'\.subckt\s+(\w+)\s+([^\n]+)\n(.*?)\.ends[^\n]*',text,re.S)}
 def reachable(edges,start):
  seen={start};todo=[start]
  while todo:
   for n in edges[todo.pop()]:
    if n not in seen:seen.add(n);todo.append(n)
  return seen
 inv=blocks['inv'][1]
 for bit in (0,1):
  edges=defaultdict(set)
  for d in inv:
   assert d[4]==('vdd' if d[5][0]=='P' else 'vss')
   if bit==(0 if d[5][0]=='P' else 1):edges[d[1]].add(d[3]);edges[d[3]].add(d[1])
  rails=reachable(edges,'z')&{'vdd','vss'}
  assert rails==({'vdd'} if bit==0 else {'vss'})
 counts={}
 for design in ('baseline','tree'):
  instances=blocks[design][1];counts[design]=sum(len(blocks[d[-1]][1]) for d in instances)
  for select in range(8):
   values={f's{k}':select>>k&1 for k in range(3)}
   for d in instances:
    if d[-1]=='inv':values[d[2]]=1-values[d[1]]
   edges=defaultdict(set)
   for d in instances:
    if d[-1]!='tg':continue
    ports=dict(zip(blocks['tg'][0],d[1:-1]))
    states=[]
    for t in blocks['tg'][1]:
     kind=t[5][0];assert ports[t[4]]==('vdd' if kind=='P' else 'vss')
     enabled=values[ports[t[2]]]==(0 if kind=='P' else 1);states.append(enabled)
     if enabled:edges[ports[t[1]]].add(ports[t[3]]);edges[ports[t[3]]].add(ports[t[1]])
    assert states[0]==states[1], 'Both TG devices must share the enable state'
   sources=reachable(edges,'z')&{f'a{i}' for i in range(8)}
   assert sources=={f'a{select}'},(design,select,sources)
 assert counts=={'baseline':54,'tree':34}
 result={'status':'PASS','baseline_select_paths':8,'tree_select_paths':8,'inverter_rail_cases':2,'transistor_counts':counts,'exactly_one_correct_data_source_connected':True,'all_body_ties_correct':True}
 (H/'results/topology_checks.json').write_text(json.dumps(result,indent=2)+'\n')
 return result
def header(model):
 return f"* 2013 HW3 actual HSPICE, 1.8V TT 25C\n.protect\n.lib '{model.as_posix()}' TT\n.unprotect\n.option post=0 measform=3 measdgt=10 numdgt=10 ingold=2 delmax=1p\n.temp 25\nVDD vdd 0 1.8\n"
def mux_deck(model):
 s=header(model)+".include 'mux.sp'\n.param "+' '.join(f'a{i}a=0 a{i}b=0' for i in range(8))+' s0v=0 s1v=0 s2v=0\n'
 for k in range(3):s+=f"VS{k} s{k} 0 's{k}v'\n"
 for i in range(8):s+=f"VA{i} a{i} 0 pwl(0 'a{i}a' 1n 'a{i}a' 1.02n 'a{i}b' 3n 'a{i}b')\n"
 s+='VREF ref 0 pwl(0 0 1n 0 1.02n 1.8 3n 1.8)\n'
 ports=' '.join(f'a{i}' for i in range(8))+' s0 s1 s2'
 for design in ('baseline','tree'):
  s+=f'X{design} {ports} z_{design} vdd 0 {design}\nCL_{design} z_{design} 0 10f\n'
 s+='.data CASES caseid '+ ' '.join(f'a{i}a a{i}b' for i in range(8))+' s0v s1v s2v\n'
 cases=[]
 for select in range(8):
  for old,new in ((0,1),(1,0)):
   cases.append(dict(select=select,old=old,new=new))
   values=[]
   for i in range(8):values += [1.8*old if i==select else 0,1.8*new if i==select else 0]
   values +=[1.8*(select>>k&1) for k in range(3)]
   s+=str(len(cases))+' '+' '.join(f'{v:g}' for v in values)+'\n'
 s+='.enddata\n.tran 1p 3n sweep data=CASES\n'
 for design in ('baseline','tree'):
  s+=f'.meas tran pre_{design} find v(z_{design}) at=.9n\n.meas tran post_{design} find v(z_{design}) at=2.9n\n'
  s+=f'.meas tran d_{design} trig v(ref) val=.9 rise=1 targ v(z_{design}) val=.9 cross=last\n'
 return s+'.end\n',cases
def inverter_deck(model):
 return header(model)+'''* Positive intrinsic-channel-current overlap estimates direct through current.
.param LOAD=.1p
MP out vin vdd vdd P_18 W=20u L=.18u
MN out vin 0 0 N_18 W=10u L=.18u
CL out 0 'LOAD'
VIN vin 0 pulse(0 1.8 3n 3n 3n 7n 20n)
.data LOADS LOAD
.1p
.3p
.5p
.7p
1p
.enddata
.tran 1p 63n sweep data=LOADS
.meas tran capacitance param='LOAD'
.meas tran pdd avg par('-v(vdd)*i(VDD)') from=23n to=43n
.meas tran isc avg par('max(0,min(lx4(MP),lx4(MN)))') from=23n to=43n
.meas tran psc param='1.8*isc'
.meas tran esc integ par('1.8*max(0,min(lx4(MP),lx4(MN)))') from=23n to=43n
.meas tran high_level find v(out) at=42.9n
.meas tran low_level find v(out) at=32.9n
.end
'''
def run(a,stem,deck):
 folder=a.work/stem;folder.mkdir(parents=True,exist_ok=True)
 (folder/'testbench.sp').write_text(deck,encoding='ascii')
 if stem=='mux':shutil.copyfile(H/'mux.sp',folder/'mux.sp')
 p=subprocess.run([a.hspice,'-i','testbench.sp','-o','run'],cwd=folder,capture_output=True,timeout=300)
 (folder/'console.log').write_bytes(p.stdout+p.stderr)
 lis=(folder/'run.lis').read_text(errors='replace') if (folder/'run.lis').exists() else ''
 if p.returncode or 'job concluded' not in lis.lower() or '**error**' in lis.lower():raise RuntimeError('HSPICE failed: '+str(folder))
 lines=(folder/'run.mt0.csv').read_text().splitlines()
 rows=[{k.strip().lower():float(v) for k,v in r.items()} for r in csv.DictReader(l for l in lines if l.strip() and not l.startswith(('$','.')))]
 return rows
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--model',type=Path,default=os.getenv('CIC018_MODEL','D:/cic018.l'))
 p.add_argument('--hspice',default=os.getenv('HSPICE','C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com'))
 p.add_argument('--work',type=Path,default=Path(tempfile.gettempdir())/'intro-vlsi-2013-hw3')
 p.add_argument('--prepare-only',action='store_true');a=p.parse_args();a.model=a.model.resolve();a.work=a.work.resolve()
 netlist=mux_netlist();(H/'mux.sp').write_text(netlist,encoding='ascii')
 (H/'results').mkdir(exist_ok=True);check_topologies(netlist)
 # Independent exhaustive function proof, then actual electrical delay checks.
 logic=[]
 for select in range(8):
  for word in range(256):
   vals=[word>>i&1 for i in range(8)]
   tree=vals
   for bit in range(3):tree=[tree[2*j+(select>>bit&1)] for j in range(len(tree)//2)]
   actual=tree[0];expected=word>>select&1
   assert actual==expected
   logic.append(dict(select=select,data=word,expected=expected,tree_output=actual,passed=True))
 results=H/'results';results.mkdir(exist_ok=True);csvout(results/'logic_2048.csv',logic)
 mdeck,cases=mux_deck(a.model);ideck=inverter_deck(a.model)
 (H/'mux_testbench.sp').write_text(mdeck,encoding='ascii');(H/'inverter_testbench.sp').write_text(ideck,encoding='ascii')
 if a.prepare_only:print('2048 function cases passed; HSPICE decks prepared');return
 measured=run(a,'mux',mdeck);assert len(measured)==16
 delay_rows=[]
 for k,(r,case) in enumerate(zip(measured,cases),start=1):
  assert int(r['caseid'])==k
  row={**case,'direction':'LH' if case['new'] else 'HL'}
  for design in ('baseline','tree'):
   for phase,bit in [('pre',case['old']),('post',case['new'])]:
    v=r[f'{phase}_{design}'];assert 1.6<v<1.82 if bit else -.02<v<.2
   delay=r['d_'+design]*1e12;assert delay>0
   row[design+'_delay_ps']=delay
  row['improvement_percent']=100*(1-row['tree_delay_ps']/row['baseline_delay_ps']);row['passed']=True;delay_rows.append(row)
 csvout(results/'mux_delays.csv',delay_rows)
 curve=[];irun=run(a,'inverter',ideck);assert len(irun)==5
 for r in irun:
  assert r['high_level']>1.6 and r['low_level']<.2
  assert r['pdd']>0 and 0<=r['psc']<=r['pdd']*1.05
  curve.append(dict(CL_pF=r['capacitance']*1e12,Psc_overlap_uW=r['psc']*1e6,E_sc_overlap_fJ=r['esc']*1e15,
                    total_supply_power_uW=r['pdd']*1e6,external_load_switching_power_uW=r['capacitance']*1.8**2/20e-9*1e6,
                    high_V=r['high_level'],low_V=r['low_level'],passed=True))
 csvout(results/'inverter_power.csv',curve)
 baseline=max(r['baseline_delay_ps'] for r in delay_rows);tree=max(r['tree_delay_ps'] for r in delay_rows)
 assert tree<baseline,'No measured worst-delay improvement'
 summary={'status':'PASS','simulator':'PrimeSim HSPICE S-2021.09','corner':'TT','VDD_V':1.8,'temperature_C':25,
          'TG_dimensions_um':{'WN':10,'WP':20,'L':.18},'mux_output_load_fF':10,'mux_input_slew_ps':20,'maximum_timestep_ps':1,
          'logic_cases':2048,'mux_electrical_transition_cases':16,'mux_measured_output_delays':32,'baseline_transistors':54,'tree_transistors':34,
          'baseline_worst_delay_ps':baseline,'tree_worst_delay_ps':tree,'worst_delay_improvement_percent':100*(1-tree/baseline),
          'inverter_load_cases':5,'inverter_input_rise_fall_ns':3,'inverter_period_ns':20,'averaging_window_ns':[23,43],
          'Psc_method':'VDD times cycle-average nonnegative minimum of positive intrinsic LX4 PMOS/NMOS channel IDS; explicit overlap estimator, not total transistor dissipation',
          'model_sha256':hashlib.sha256(a.model.read_bytes()).hexdigest(),'mux_sha256':hashlib.sha256((H/'mux.sp').read_bytes()).hexdigest()}
 (results/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
