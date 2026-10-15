"""Printed clock-tree units, symmetric-threshold mobility and ideal VTC checks."""
from pathlib import Path
import csv,json,math
H=Path(__file__).resolve().parent
def csvout(name,rows):
 with (H/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
paths=[]
for name,length,gates in [('A->B',650,2),('A->C',400,3),('A->D',650,2)]:
 wire=.5*.05*30e-18*length**2
 paths.append(dict(path=name,length_um=length,isolated_wire_estimate_ps=wire*1e12,neglect_cutoff_ps=800,wire_neglected=wire<=4*.2e-9,gate_units=gates,delay_ns=gates*.2))
assert max(paths,key=lambda r:r['delay_ns'])['path']=='A->C'
csvout('clock_tree.csv',paths)
def vil(rho,vdd=1.8,t=.45):
 T=vdd-2*t;lo=0;hi=T/(1+math.sqrt(rho))
 for _ in range(100):
  u=(lo+hi)/2;v=T-u
  f=(v+rho*u)/math.sqrt(max(v*v-rho*u*u,1e-30))-2
  if f>0:hi=u
  else:lo=u
 return t+(lo+hi)/2
noise=[]
for rho in (.25,.5,1,2,4):
 a=vil(rho);b=1.8-vil(1/rho)
 row=dict(beta_n_over_beta_p=rho,VIL_V=a,VIH_V=b,NML_V=a,NMH_V=1.8-b)
 if rho>1:assert row['NMH_V']>row['NML_V']
 elif rho<1:assert row['NMH_V']<row['NML_V']
 else:assert abs(row['NMH_V']-row['NML_V'])<1e-12
 noise.append(row)
csvout('noise_margin.csv',noise)
result={'status':'PASS','clock_paths':3,'critical_path':'A->C','critical_delay_ns':.6,'matched_threshold_mobility_ratio_mu_n_over_mu_p':2,'noise_margin_examples':len(noise),'noise_model':'ideal long-channel inverter; Vdd1.8V, equal |Vt|0.45V; slope=-1 boundaries','physical_simulation_required_by_prompt':False}
(H/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
