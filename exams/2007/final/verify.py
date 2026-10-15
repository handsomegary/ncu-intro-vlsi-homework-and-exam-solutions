"""Independent MOS graph, NP full-adder, retention and dynamic-register checks."""
from pathlib import Path
from fractions import Fraction as F
import csv,itertools,json
HERE=Path(__file__).resolve().parent
net=json.loads((HERE/'device-netlists.json').read_text(encoding='utf-8'))
def save(name,rows):
 with (HERE/name).open('w',newline='',encoding='utf-8')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def reach(edges,start,target):
 seen={start};todo=[start]
 while todo:
  x=todo.pop()
  for a,b in edges:
   y=b if a==x else a if b==x else None
   if y is not None and y not in seen:seen.add(y);todo.append(y)
 return target in seen
def gate(g,v):
 if g=='0':return 0
 if g==r'\phi':return v['phi']
 if g==r'\bar\phi':return 1-v['phi']
 if g.startswith(r'\bar '):return 1-v[g[5:]]
 return v[g]
def edges(dev,v):return [(a,b)for n,p,g,a,b in dev if gate(g,v)==(0 if p else 1)]
def railcheck(dev,v,node,want):
 e=edges(dev,v);high=reach(e,node,'V_{DD}');low=reach(e,node,'0')
 assert high!=low and high==bool(want)
 return high,low

q2=[]
for A,B in itertools.product([0,1],repeat=2):
 a=1-A;b=1-B;v=dict(A=A,B=B,a=a,b=b)
 en=edges([d for d in net['Q2']if d[1]==0],v);pulldown=reach(en,'O','0');assert pulldown==bool(A^B)
 q2.append(dict(A=A,B=B,a=a,b=b,out_under_ratioed_level_assumption=1-int(pulldown),NMOS_output_ground_path=pulldown))
save('q2-xnor-switch-paths.csv',q2)

carryN=[d for d in net['Q4']if d[0]in ['NA1','NB1','NC1','NA2','NB2','Nfoot']]
sumP=[d for d in net['Q4']if d[0]in ['Phead','PA1','PB1','PC1','Pcb','PA2','PB2','PC2']]
q4=[]
for A,B,C in itertools.product([0,1],repeat=3):
 v=dict(A=A,B=B,C=C,phi=1);cout=int((A+B+C)>=2)
 cb=1-int(reach(edges(carryN,v),'cb','0'));assert cb==1-cout
 v['cb']=cb;sb=int(reach(edges(sumP,v),'sb','V_{DD}'));ss=1-sb
 assert ss==(A^B^C)
 v.update(cout=cout,sb=sb,sum=ss)
 railcheck([d for d in net['Q4']if d[0]in ['Pcarry','Ncarry']],v,'cout',cout)
 railcheck([d for d in net['Q4']if d[0]in ['Psum','Nsum']],v,'sum',ss)
 q4.append(dict(A=A,B=B,C=C,carrybar=cb,carry=cout,sumbar=sb,sum=ss,arithmetic_sum=A+B+C,encoded_sum=2*cout+ss))
save('q4-full-adder-truth.csv',q4)
ret=[]
for node in ['cb','sb']:
 drains=[d[0]for d in net['Q4']if node in d[3:5]]
 gates=[d[0]for d in net['Q4']if d[2]==node]
 cap=F(len(drains),5)+len(gates);limit=cap*F(9,10)
 ret.append(dict(node=node,channel_end_devices=' '.join(drains),gate_load_devices=' '.join(gates),drain_count=len(drains),gate_count=len(gates),C_fF=str(cap),allowed_deltaV='9/10',leakage_nA=1,retention_us=str(limit)))
assert ret[0]['C_fF']=='18/5'and ret[1]['C_fF']=='13/5'
assert min(F(r['retention_us'])for r in ret)==F(117,50)
save('q4-node-capacitance-retention.csv',ret)
save('q4-duty-dependent-frequency.csv',[dict(evaluation_fraction=str(duty),max_evaluation_us='117/50',minimum_frequency_kHz=str(duty*1000/F(117,50)))for duty in [F(1,4),F(1,2),F(3,4),F(1)]])

q5=[]
for A,B,C,D,E in itertools.product([0,1],repeat=5):
 g=int((A and(B or C))or(D and E));f=1-g;v=dict(A=A,B=B,C=C,D=D,E=E,phi=1,z=f,fb=g,g=g,f=f)
 railcheck(net['Q5_static'],v,'z',f)
 epdn=edges([d for d in net['Q5_fully_differential']if not d[1]],v)
 pz=reach(epdn,'z','0');pfb=reach(epdn,'fb','0');assert pz!=pfb and pz==bool(g)
 railcheck(net['Q5_fully_differential'],v,'z',f);railcheck(net['Q5_fully_differential'],v,'fb',g)
 dom=net['Q5_domino_with_output_inversion'];ed=edges([d for d in dom if d[0]not in ['Pi1','Ni1','Pi2','Ni2']],v)
 z=1-int(reach(ed,'z','0'));assert z==f
 railcheck([d for d in dom if d[0]in ['Pi1','Ni1']],v,'g',g)
 railcheck([d for d in dom if d[0]in ['Pi2','Ni2']],v,'f',f)
 v0={**v,'phi':0,'z':1,'g':0,'f':1};railcheck(dom,v0,'z',1);railcheck(dom,v0,'f',1)
 q5.append(dict(A=A,B=B,C=C,D=D,E=E,g=g,f=f,static=f,FD_f=f,FD_fbar=g,domino_raw_z=z,domino_one_buffer=g,domino_plus_second_inverter=f))
save('q5-three-style-truth.csv',q5)

# Independent phase update uses rail reachability of each literal3MOS stage.
stage_names=[['P1','N1c','N1d'],['P2','N2c','N2d'],['P3d','P3c','N3'],['P4d','P4c','N4']]
stages=[[d for d in net['Q6']if d[0]in names]for names in stage_names];outputs=['A','B','C','O']
assert len(net['Q6'])==12 and all(len(d)==3 for d in stages)
def settle(state,I,phi):
 state=state.copy();state.update(I=I,phi=phi)
 for t in range(8):
  new=state.copy()
  for node,dev in zip(outputs,stages):
   e=edges(dev,state);hi=reach(e,node,'V_{DD}');lo=reach(e,node,'0');assert not(hi and lo)
   if hi:new[node]=1
   elif lo:new[node]=0
  if all(new[k]==state[k]for k in outputs):return new
  state=new
 raise AssertionError('no stable phase state')
events=[]
for old,new in itertools.product([0,1],repeat=2):
 s=dict(A=1-old,B=old,C=1-old,O=old)
 for label,I,phi,want in [('old low phase',old,0,old),('input changes while low',new,0,old),('rising edge/master opens',new,1,old),('input changes while high',1-new,1,old),('falling edge/sample',1-new,0,1-new),('input changes after falling edge',new,0,1-new)]:
  s=settle(s,I,phi);assert s['O']==want
  if phi==1:assert s['A']==1-I and s['B']==I
  events.append(dict(initial_sample=old,next_input=new,event=label,I=I,phi=phi,A=s['A'],B=s['B'],C=s['C'],O=s['O'],expected_O=want))
save('q6-dynamic-phase-events.csv',events)
assert 2+15+3==20 and F(1000,20)==50
save('q7-timing.csv',[dict(model='printed setup bound',tpcq_ns=2,tpd_ns=15,tsetup_ns=3,Tmin_ns=20,fmax_MHz=50,hold_margin_ns='not established from propagation-only data'),dict(model='fixed max=min delay interpretation',tpcq_ns=2,tpd_ns=15,tsetup_ns=3,Tmin_ns=20,fmax_MHz=50,hold_margin_ns=16)])

# Root supplies the independent physical-contact audit; require it for final success.
q3file=HERE/'q3-literal-netlist.csv'
q3_report={'status':'pending independently audited extraction'}
if q3file.exists():
 with q3file.open(encoding='utf-8')as f:q3rows=list(csv.DictReader(f))
 def normalized(n):return {'VDD':'V_{DD}','VSS':'0','GND':'0','Dbar':'dbar','DB':'dbar','clk':'CLK','clkbar':'CLKB'}.get(n,n)
 q3dev=[(r['device'],1 if r['type'].upper()in ['P','PMOS']else 0,normalized(r['gate']),normalized(r['terminal_1']),normalized(r['terminal_2']))for r in q3rows]
 assert len(q3dev)==10 and sum(d[1]for d in q3dev)==5
 # Trace-derived reference ignores the arbitrary device names and terminal ordering.
 reference=[(1,'D','V_{DD}','dbar'),(0,'D','dbar','0'),(1,'CLKB','dbar','u'),(0,'CLK','dbar','u'),(1,'CLK','V_{DD}','CLKB'),(0,'CLK','CLKB','0'),(1,'u','V_{DD}','O'),(0,'u','O','0'),(1,'O','V_{DD}','u'),(0,'O','u','0')]
 signature=lambda p,g,a,b:(p,g,tuple(sorted([a,b])))
 assert {signature(*d[1:])for d in q3dev}=={signature(*d)for d in reference}
 q3states=[]
 for D,CLK,oldO in itertools.product([0,1],repeat=3):
  v=dict(D=D,CLK=CLK,CLKB=1-CLK,dbar=1-D,u=1-oldO,O=oldO)
  ee=edges(q3dev,v);hi=reach(ee,'u','V_{DD}');lo=reach(ee,'u','0');conflict=bool(CLK and D!=oldO)
  assert (hi and lo)==conflict
  if not conflict:
   assert hi==bool(1-oldO) and lo==bool(oldO)
   railcheck(q3dev,v,'O',oldO)
  q3states.append(dict(D=D,CLK=CLK,old_O=oldO,u_before_write=1-oldO,input_driver_dbar=1-D,feedback_driver_not_O=1-oldO,transmission_gate_on=CLK,VDD_path_to_u=hi,VSS_path_to_u=lo,write_contention=conflict,interpretation='input must overcome fixed feedback'if conflict else 'binary-consistent state'))
 # If the external write path wins and the loop settles, both new data states are consistent.
 for D in [0,1]:
  v=dict(D=D,CLK=1,CLKB=0,dbar=1-D,u=1-D,O=D)
  railcheck(q3dev,v,'u',1-D);railcheck(q3dev,v,'O',D)
 save('q3-independent-switch-states.csv',q3states)
 assert sum(r['write_contention']for r in q3states)==2
 q3_report={'status':'contact graph and conditional switch states passed','physical_MOS':len(q3dev),'inverters':4,'transmission_gates':1,'stable_loop_cases_tested':8,'opposite_data_write_contention_cases':2,'write_strength_unspecified':True,'conditional_transparency':'CLK=1: O=D if input path overrides feedback','opaque_phase':'CLK=0: stored O retained'}
assert sum([26,10,14,20,15,10,10])==105
report = {'all_checks_passed': q3file.exists(), 'all_independent_checks_passed': q3file.exists(), 'all_nonlayout_checks_passed': True, 'check_scope': 'Independent mathematical and circuit checks.', 'q2_cases': 4, 'q3': q3_report, 'q4_truth_states': 8, 'q4_governing_evaluation_us': '117/50', 'q4_minimum_frequency_depends_on_duty': True, 'q5_binary_cases': 32, 'q6_physical_MOS': 12, 'q6_phase_events': len(events), 'q6_active_capture_edge': 'falling', 'q7_setup_period_ns': 20, 'q7_minimum_hold_data_absent': True, 'printed_percentage_total': 105}
(HERE/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
