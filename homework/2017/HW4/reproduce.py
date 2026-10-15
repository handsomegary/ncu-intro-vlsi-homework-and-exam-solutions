"""Verify and calibrate the mirror and dual-rail domino full adders.
Mirror: every 56 directed transition, both outputs checked.
Domino: 8 independent evaluate/precharge cycles, both outputs checked.
Balanced tr=tf means max 10-90% rise/fall per output at stated conditions.
"""
from pathlib import Path
import argparse,csv,json,os,subprocess,bisect
H=Path(__file__).resolve().parent

def header(model):return f"* 2017 full-adder verification\n.protect\n.lib '{model.as_posix()}' tt\n.unprotect\nvvdd vdd 0 1.8\nvvss vss 0 0\n.temp 25\n.option ingold=2 lis_new=1 numdgt=8 delmax=2p\n"
def pwl(node,points):
 s=f'v{node} {node} 0 pwl(\n'
 for i in range(0,len(points),5):s+='+ '+' '.join(f'{t:g}n {v*1.8:g}' for t,v in points[i:i+5])+'\n'
 return s+'+)\n'
def read_trace(p):
 lines=p.read_text(errors='replace').splitlines();rows={};names=[];armed=False
 for i,l in enumerate(lines):
  if l.strip().lower().startswith('time '):names=lines[i+1].lower().split();armed=True;continue
  if not armed:continue
  try:n=[float(q.replace('D','e')) for q in l.split()]
  except ValueError:continue
  if len(n)==len(names)+1:rows.setdefault(n[0],{}).update(dict(zip(names,n[1:])))
 ts=[];sv=[];cv=[]
 for t,d in sorted(rows.items()):
  if 's' in d and 'co' in d:ts.append(t*1e9);sv.append(d['s']);cv.append(d['co'])
 return ts,{'S':sv,'Cout':cv}
def last_cross(ts,vs,start,stop,level,rising):
 lo=bisect.bisect_left(ts,start);hi=bisect.bisect_right(ts,stop);out=[]
 for i in range(max(1,lo),hi):
  a,b=vs[i-1],vs[i]
  if (a<level<=b) if rising else (a>level>=b):out.append(ts[i-1]+(level-a)/(b-a)*(ts[i]-ts[i-1]))
 if not out:raise AssertionError(f'Missing {level} crossing {start}..{stop}')
 return out[-1]
def sample(ts,vs,t):
 k=bisect.bisect_left(ts,t)
 if not 0<k<len(ts):return vs[max(0,min(k,len(vs)-1))]
 return vs[k-1]+(vs[k]-vs[k-1])*(t-ts[k-1])/(ts[k]-ts[k-1])
def truth(v):return {'S':v.bit_count()%2,'Cout':int(v.bit_count()>=2)}
def deck(kind,model,pars):
 s=header(model)+f".include '{kind}_full_adder.sp'\n"
 for k,v in pars.items():s+=f'.param {k}={v:g}u\n'
 if kind=='mirror':
  cases=[(a,b) for a in range(8) for b in range(8) if a!=b]
  for bit,node in [(2,'a'),(1,'b'),(0,'c')]:
   points=[(0,cases[0][0]>>bit&1)]
   for k,(old,new) in enumerate(cases):
    if k:points.extend([(10*k-.1,cases[k-1][1]>>bit&1),(10*k,old>>bit&1)])
    points.extend([(10*k+4.9,old>>bit&1),(10*k+5,new>>bit&1)])
   s+=pwl(node,points)
  s+='XF a b c s co vdd vss mirror_fa\n'
  stop=562
 else:
  cases=list(range(8))
  for bit,node in [(2,'a'),(1,'b'),(0,'c')]:
   points=[(0,0)]
   for k,v in enumerate(cases):points.extend([(10*k+1,v>>bit&1 if k==0 else (cases[k-1]>>bit&1)),(10*k+1.1,v>>bit&1)])
   s+=pwl(node,points)
  s+='vclk clk 0 pulse(0 1.8 5n .1n .1n 4n 10n)\nXF a b c clk s co vdd vss domino_fa\n';stop=82
 s+='CLS s 0 1f\nCLC co 0 1f\n'+f'.tran 2p {stop}n\n.print tran v(a) v(b) v(c) v(s) v(co)\n.end\n'
 return s,cases
def run(kind,pars,a,label):
 folder=Path(a.work).resolve()/kind/label;folder.mkdir(parents=True,exist_ok=True)
 (folder/f'{kind}_full_adder.sp').write_text((H/f'{kind}_full_adder.sp').read_text(),encoding='ascii')
 s,cases=deck(kind,Path(a.model).resolve(),pars);(folder/'testbench.sp').write_text(s,encoding='ascii')
 p=subprocess.run([a.hspice,'-i','testbench.sp','-o','run'],cwd=folder,capture_output=True,text=True,errors='replace',timeout=240)
 (folder/'console.log').write_text(p.stdout+p.stderr,encoding='utf-8');lis=(folder/'run.lis').read_text(errors='replace') if(folder/'run.lis').exists() else ''
 if p.returncode or 'job concluded' not in lis.lower() or '**error**' in lis.lower():raise RuntimeError('HSPICE failed: '+str(folder))
 ts,vs=read_trace(folder/'run.printtr0');metrics=[];checks=[]
 for k,case in enumerate(cases):
  new=case[1] if kind=='mirror' else case;old=case[0] if kind=='mirror' else 0
  out=truth(new);prior=truth(old);edge=10*k+4.9 if kind=='mirror' else 10*k+5
  end=10*k+8.5
  for node in ['S','Cout']:
   voltage=sample(ts,vs[node],end);passed=(voltage>=1.6 if out[node] else voltage<=.2)
   checks.append(dict(old=f'{old:03b}',new=f'{new:03b}',node=node,expected=out[node],voltage_V=voltage,passed=passed))
   if not passed:raise AssertionError(f'{kind} incorrect {new:03b} {node} {voltage}')
   if kind=='mirror' and prior[node]==out[node]:continue
   if kind=='domino' and not out[node]:continue
   rising=bool(out[node]);t50=last_cross(ts,vs[node],edge-.05,end,.9,rising)
   t10=last_cross(ts,vs[node],edge-.05,end,.18 if rising else 1.62,rising)
   t90=last_cross(ts,vs[node],edge-.05,end,1.62 if rising else .18,rising)
   metrics.append(dict(old=f'{old:03b}',new=f'{new:03b}',node=node,direction='rise' if rising else 'fall',phase='evaluate' if kind=='domino' else 'data',delay_ps=(t50-(edge+.05))*1e3,slew_ps=(t90-t10)*1e3))
   if kind=='domino':
    reset=10*k+9.1;limit=10*k+9.85
    r50=last_cross(ts,vs[node],reset-.05,limit,.9,False);r10=last_cross(ts,vs[node],reset-.05,limit,1.62,False);r90=last_cross(ts,vs[node],reset-.05,limit,.18,False)
    metrics.append(dict(old=f'{new:03b}',new='precharge',node=node,direction='fall',phase='precharge',delay_ps=(r50-(reset+.05))*1e3,slew_ps=(r90-r10)*1e3))
  if kind=='domino':
   for node in ['S','Cout']:
    v=sample(ts,vs[node],10*k+4)
    checks.append(dict(old='precharge',new=f'{new:03b}',node=node,expected=0,voltage_V=v,passed=v<=.2))
    if v>.2:raise AssertionError('Domino did not precharge/reset')
 stats={}
 for node in ['S','Cout']:
  q=[m for m in metrics if m['node']==node];tr=max(m['slew_ps'] for m in q if m['direction']=='rise');tf=max(m['slew_ps'] for m in q if m['direction']=='fall')
  stats[node]=dict(tr_ps=tr,tf_ps=tf,imbalance_percent=100*abs(tr-tf)/max(tr,tf),worst_delay_ps=max(m['delay_ps'] for m in q if m['phase']!='precharge'))
 return stats,metrics,checks,s

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--hspice',default=os.environ.get('HSPICE','C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com'));ap.add_argument('--model',default=os.environ.get('CIC018_MODEL','D:/cic018.l'));ap.add_argument('--work',default=str(H.parents[2]/'scratch'/'2017HW4'));ap.add_argument('--no-calibrate',action='store_true')
 a=ap.parse_args();results=H/'results';results.mkdir(exist_ok=True);summary={};allcal=[]
 for kind in ['mirror','domino']:
  defaults={'WOSS':1.8,'WOSC':1.8} if kind=='mirror' else {'WPSS':1.8,'WPSC':1.8}
  cfg=H/f'{kind}_sizes.json';pars=json.loads(cfg.read_text()) if cfg.exists() else defaults
  limit=1 if a.no_calibrate else 8
  for iteration in range(limit):
   pars={key:float(f'{value:.6g}') for key,value in pars.items()}
   stats,met,checks,s=run(kind,pars,a,f'iter{iteration}');allcal.append(dict(kind=kind,iteration=iteration,parameters=dict(pars),statistics=stats));print(json.dumps(allcal[-1]),flush=True)
   if a.no_calibrate or max(v['imbalance_percent'] for v in stats.values())<1 or iteration==limit-1:break
   for node,key in [('S','WOSS' if kind=='mirror' else 'WPSS'),('Cout','WOSC' if kind=='mirror' else 'WPSC')]:
    ratio=stats[node]['tr_ps']/stats[node]['tf_ps']
    # Mirror: increase output pMOS strength if rising is too slow.
    # Domino: reduce precharge pMOS strength if evaluation rise is too slow.
    factor=ratio if kind=='mirror' else 1/ratio
    pars[key]=max(.12,min(12,pars[key]*factor))
  cfg.write_text(json.dumps(pars,indent=2));(H/f'{kind}_testbench.sp').write_text(s,encoding='ascii')
  import re
  net=H/f'{kind}_full_adder.sp';nt=net.read_text()
  for key,value in pars.items():nt=re.sub(r'(?i)'+key+r'=[0-9.]+u',f'{key}={value:.9f}u',nt)
  net.write_text(nt,encoding='ascii')
  for fn,rows in [(f'{kind}_metrics.csv',met),(f'{kind}_logic.csv',checks)]:
   with(results/fn).open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
  summary[kind]=dict(parameters=pars,statistics=stats,all_logic_pass=True,checked_samples=len(checks),measured_edges=len(met),balance_target_percent=1,balanced=max(v['imbalance_percent'] for v in stats.values())<1)
 (results/'calibration.json').write_text(json.dumps(allcal,indent=2));(results/'summary.json').write_text(json.dumps(dict(simulator='HSPICE S-2021.09',model='CIC018 TT local',VDD_V=1.8,temperature_C=25,output_load_fF=1,input_and_clock_slew_ps=100,DELMAX_ps=2,mirror_directed_transitions=56,domino_input_states=8,designs=summary),indent=2))
 if not all(v['balanced'] for v in summary.values()):raise AssertionError('Balance target not achieved; inspect calibration data')
if __name__=='__main__':main()
