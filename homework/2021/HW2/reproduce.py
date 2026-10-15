"""Actual HSPICE checks of 40T rotator and pseudo-NMOS NOR.
No dual-Vt PDK is provided; Q1 is verified logically, not as leakage data.
"""
from pathlib import Path
import argparse,csv,json,os,subprocess
H=Path(__file__).resolve().parent

def run(folder,deck,a):
 folder.mkdir(parents=True,exist_ok=True)
 for name in ['rotator.sp','pseudo_nor.sp']:(folder/name).write_text((H/name).read_text(),encoding='ascii')
 (folder/'testbench.sp').write_text(deck,encoding='ascii')
 p=subprocess.run([a.hspice,'-i','testbench.sp','-o','run'],cwd=folder,capture_output=True,text=True,errors='replace',timeout=180)
 (folder/'console.log').write_text(p.stdout+p.stderr,encoding='utf-8')
 lis=(folder/'run.lis').read_text(errors='replace') if (folder/'run.lis').exists() else ''
 if p.returncode or 'job concluded' not in lis.lower() or '**error**' in lis.lower():raise RuntimeError('HSPICE failed: '+str(folder))
 lines=(folder/'run.mt0.csv').read_text(errors='replace').splitlines()
 row=list(csv.DictReader(l for l in lines if l.strip() and not l.startswith(('$','.'))))[0]
 return {k:float(v) for k,v in row.items() if k not in ['temper','alter#']}
def header(model):return f"* 2021 HW2 functional simulation\n.protect\n.lib '{model.as_posix()}' tt\n.unprotect\nvvdd vdd 0 1.8\nvvss vss 0 0\n.temp 25\n.option measform=3 measdgt=9\n"
def pwl(node,vals,step=10):
 points=[f'0n {vals[0]*1.8:g}']
 for k in range(1,len(vals)):
  if vals[k]!=vals[k-1]:points.extend([f'{step*k-.1:g}n {vals[k-1]*1.8:g}',f'{step*k:g}n {vals[k]*1.8:g}'])
 s=f'v{node} {node} 0 pwl(\n'
 for j in range(0,len(points),5):s+='+ '+' '.join(points[j:j+5])+'\n'
 return s+'+)\n'
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--hspice',default=os.environ.get('HSPICE','C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com'));ap.add_argument('--model',default=os.environ.get('CIC018_MODEL','D:/cic018.l'));ap.add_argument('--work',default=str(H.parents[2]/'scratch'/'2021_HW2'))
 a=ap.parse_args();model=Path(a.model).resolve();raw=Path(a.work).resolve();results=H/'results';results.mkdir(exist_ok=True)
 if not model.is_file():raise FileNotFoundError('Local model required: '+str(model))
 cases=[(data,r) for r in range(4) for data in range(16)]
 s=header(model)+".include 'rotator.sp'\n"
 for j in range(4):s+=pwl(f'a{j}',[data>>j&1 for data,r in cases])
 for j in range(4):s+=pwl(f'c{j}',[int(j!=3-r) for data,r in cases])
 s+='XR a0 a1 a2 a3 c0 c1 c2 c3 z0 z1 z2 z3 vdd vss rotate4\n'
 for j in range(4):s+=f'CL{j} z{j} 0 1f\n'
 s+='.tran 10p 640n 0 50p\n'
 for k,(data,r) in enumerate(cases):
  for j in range(4):s+=f'.measure tran q{k}b{j} find v(z{j}) at={10*k+8}n\n'
 s+='.end\n';(H/'rotator_testbench.sp').write_text(s,encoding='ascii');m=run(raw/'rotator',s,a)
 rows=[]
 for k,(data,r) in enumerate(cases):
  exp=((data<<r)|(data>>(4-r if r else 4)))&15
  volts=[m[f'q{k}b{j}'] for j in range(4)];got=sum(int(v>.9)<<j for j,v in enumerate(volts))
  passed=got==exp and all((v>1.6 if exp>>j&1 else v<.2) for j,v in enumerate(volts))
  rows.append(dict(data=data,rotation=r,expected=exp,observed=got,Z0_V=volts[0],Z1_V=volts[1],Z2_V=volts[2],Z3_V=volts[3],passed=passed))
  if not passed:raise AssertionError('Electrical rotator case failed')
 s=header(model)+".include 'pseudo_nor.sp'\n"+pwl('a',[0,0,1,1])+pwl('b',[0,1,0,1])+'XN a b z vdd vss pseudo_nor\nCL z 0 1f\n.tran 10p 40n 0 10p\n'
 for k in range(4):s+=f'.measure tran v{k} find v(z) at={10*k+8}n\n'
 s+='.end\n';(H/'pseudo_nor_testbench.sp').write_text(s,encoding='ascii');m=run(raw/'pseudo_nor',s,a)
 nr=[]
 for k in range(4):
  v=m[f'v{k}'];passed=v>1.6 if k==0 else v<=.18
  nr.append(dict(A=k>>1,B=k&1,Vout_V=v,passed=passed))
  if not passed:raise AssertionError('Pseudo-NMOS voltage check failed')
 for fn,rs in [('rotator_electrical.csv',rows),('pseudo_nor_electrical.csv',nr)]:
  with (results/fn).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
 # Q1 topology can be run with explicit educational square-law models.
 # These are not CIC018 models and cannot quantify process leakage.
 t="* Q1 illustrative topology verification only\n.include 'dual_vt_logic.sp'\n"
 t+=".model N_LVT NMOS LEVEL=1 VTO=.4 KP=100u\n.model P_LVT PMOS LEVEL=1 VTO=-.4 KP=50u\n.model N_HVT NMOS LEVEL=1 VTO=.6 KP=100u\n.model P_HVT PMOS LEVEL=1 VTO=-.6 KP=50u\n"
 t+='vvdd vdd 0 1.8\nvvss vss 0 0\n.temp 25\n.option measform=3 measdgt=9\n'
 for j,node in enumerate(['a','b','c']):t+=pwl(node,[(k>>(2-j))&1 for k in range(8)])
 t+='XL a b c d e vdd vss dual_vt_logic\nCD d 0 1f\nCE e 0 1f\n.tran 10p 80n 0 10p\n'
 for k in range(8):
  for node in ['d','e']:t+=f'.measure tran {node}{k} find v({node}) at={10*k+8}n\n'
 t+='.end\n';(H/'dual_vt_boolean_testbench.sp').write_text(t,encoding='ascii')
 folder=raw/'dual_vt_boolean';folder.mkdir(parents=True,exist_ok=True)
 (folder/'dual_vt_logic.sp').write_text((H/'dual_vt_logic.sp').read_text(),encoding='ascii')
 m=run(folder,t,a);vr=[]
 for k in range(8):
  aa,bb,cc=k>>2,(k>>1)&1,k&1;expd=int(aa==bb);expe=int(not(bb and cc));vd=m[f'd{k}'];ve=m[f'e{k}']
  passed=(vd>1.6 if expd else vd<.2) and (ve>1.6 if expe else ve<.2)
  vr.append(dict(A=aa,B=bb,C=cc,D_V=vd,E_V=ve,expected_D=expd,expected_E=expe,passed=passed,provenance='illustrative_LEVEL1_not_CIC018'))
  if not passed:raise AssertionError('Q1 illustrative topology failed')
 with (results/'dual_vt_illustrative.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(vr[0]));w.writeheader();w.writerows(vr)
 summary=dict(simulator='PrimeSim HSPICE S-2021.09 win64',model='CIC018 TT BSIM3 (local)',VDD_V=1.8,temperature_C=25,rotator_cases=64,all_rotator_pass=True,pseudo_nor=nr,dual_Vt_illustrative_cases=8,all_dual_Vt_illustrative_logic_pass=True,dual_Vt_physical_measurement='not available: no dual-Vt PDK provided')
 (results/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
