"""Independent ideal logic, switch connectivity, and labeled resistance checks."""
from pathlib import Path
import csv,json,itertools,math

BASE=Path(__file__).resolve().parent

def write_csv(name,rows):
 with (BASE/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def rail_reach(devices,values,start):
 graph={}
 for p,g,a,b in devices:
  if values[g]!=(0 if p else 1):continue
  graph.setdefault(a,set()).add(b);graph.setdefault(b,set()).add(a)
 seen={start};todo=[start]
 while todo:
  a=todo.pop()
  for b in graph.get(a,[]):
   if b not in seen:seen.add(b);todo.append(b)
 return int('VDD' in seen),int('0' in seen)

q3=[(0,'A','G','n1'),(0,'C','n1','0'),(0,'D','G','n2'),(0,'A','n2','0'),(0,'B','n2','0'),(0,'C','n2','0'),(1,'A','VDD','p1'),(1,'C','VDD','p1'),(1,'D','p1','G'),(1,'A','p1','p2'),(1,'B','p2','p3'),(1,'C','p3','G'),(1,'G','VDD','F'),(0,'G','F','0')]
q6a=[(0,'X','G','n'),(0,'Y','n','0'),(0,'Z','n','0'),(0,'W','n','0'),(1,'X','VDD','G'),(1,'Y','VDD','p1'),(1,'Z','p1','p2'),(1,'W','p2','G'),(1,'G','VDD','F'),(0,'G','F','0')]
q6b=[(0,'X','F','n'),(0,'Y','n','0'),(0,'Z','n','0'),(1,'X','VDD','F'),(1,'Y','VDD','p'),(1,'Z','p','F')]

def check_cmos(devices,keys,expected,printed=None):
 rows=[]
 for idx,bits in enumerate(itertools.product([0,1],repeat=len(keys))):
  values=dict(zip(keys,bits));f=int(expected(**values));values['G']=1-f
  fhigh,flow=rail_reach(devices,values,'F')
  assert (fhigh,flow)==(f,1-f),(values,fhigh,flow)
  if any('G' in d[2:] for d in devices):
   gh,gl=rail_reach(devices,values,'G');assert(gh,gl)==(1-f,f)
  if printed is not None:assert f==printed[idx]
  rows.append({**dict(zip(keys,bits)),'expected_F':f,'F_high_rail':fhigh,'F_low_rail':flow,'pass':True})
 return rows

def main():
 q3rows=check_cmos(q3,'ABCD',lambda A,B,C,D:(A and C)or(D and(A or B or C)),[0,0,0,1,0,1,0,1,0,1,1,1,0,1,1,1])
 write_csv('q3_cmos_checks.csv',q3rows)
 q6arows=check_cmos(q6a,'XYZW',lambda X,Y,Z,W:X and(Y or Z or W));write_csv('q6a_cmos_checks.csv',q6arows)
 q6brows=check_cmos(q6b,'XYZ',lambda X,Y,Z:not(X and(Y or Z)));write_csv('q6b_cmos_checks.csv',q6brows)
 transitions=[]
 for z in [1,0,1]:
  vals={'X':1,'Y':0,'Z':z};f=int(not z)
  h,l=rail_reach(q6b,vals,'F');assert(h,l)==(f,1-f)
  transitions.append({'X':1,'Y':0,'Z':z,'F':f,'conducting_drive_path':'P_Y + P_Z' if z==0 else 'N_X + N_Z','series_devices':2,'equivalent_width_over_W':.5,'pass':True})
 write_csv('q6b_transition_checks.csv',transitions)
 mux=[]
 for packed in range(256):
  data=[(packed>>i)&1 for i in range(8)]
  for s2,s1,s0 in itertools.product([0,1],repeat=3):
   first=[data[2*i+s0] for i in range(4)]
   second=[first[2*i+s1] for i in range(2)]
   y=second[s2];idx=4*s2+2*s1+s0
   assert y==data[idx]
   mux.append({'data_vector_integer':packed,'S2':s2,'S1':s1,'S0':s0,'selected_index':idx,'Y':y,'pass':True})
 write_csv('q2_mux_checks.csv',mux)
 nand=[]
 for a,b,c in itertools.product([0,1],repeat=3):
  i=4*a+2*b+c;f=int(i!=7);assert f==int(not(a and b and c))
  nand.append({'A':a,'B':b,'C':c,'selected_D':i,'F':f,'pass':True})
 write_csv('q2_nand_checks.csv',nand)
 xor=[]
 for a,b in itertools.product([0,1],repeat=2):
  # Stable complementary A: input-powered inverter only active for A=1;
  # TG uses NMOS gate ~A and PMOS gate A, and is active for A=0.
  tg_on=(a==0);pm_on=(a==1 and b==0);nm_on=(a==1 and b==1)
  y=b if tg_on else int(pm_on)
  assert y==(a^b) and not(pm_on and nm_on)
  xor.append({'A':a,'B':b,'TG_enabled':tg_on,'inverter_P_drive':pm_on,'inverter_N_drive':nm_on,'Y':y,'pass':True})
 write_csv('q5_xor_checks.csv',xor)
 u=1.2/(1+2);trip=u+.4
 assert math.isclose(u,.4) and math.isclose(trip,.8)
 regions=[]
 for vin in [.45,.5,.6,.7,.75]:
  vout=1.2
  for name,vgs,vgd in [('N1',vin,vin-u),('N2',vout-u,vout-1.2),('N3',vin-u,vin-vout)]:
   region='cutoff' if vgs<.4 else ('triode' if vgd>.4 else 'saturation')
   assert region==({'N1':'saturation','N2':'saturation','N3':'cutoff'}[name])
   regions.append({'model':'course_frozen_u_pre_discharge','Vin_V':vin,'u_V':u,'Vout_V':vout,'device':name,'VGS_V':vgs,'VGD_V':vgd,'Vtn_V':.4,'region':region,'pass':True})
 write_csv('q4_region_checks.csv',regions)
 discharge=[]
 for vin,un,vout in [(.7,.25,1.0),(.75,.3,.9),(.8,.3,.8)]:
  assert vout>=vin and vin-un>.4
  for name,vgs,vgd in [('N1',vin,vin-un),('N2',vout-un,vout-1.2),('N3',vin-un,vin-vout)]:
   region='cutoff' if vgs<.4 else ('triode' if vgd>.4 else 'saturation')
   assert region==({'N1':'triode','N2':'saturation','N3':'saturation'}[name])
   discharge.append({'model':'conducting_before_input_output_crossing_conditions','Vin_V':vin,'u_V':un,'Vout_V':vout,'device':name,'VGS_V':vgs,'VGD_V':vgd,'Vtn_V':.4,'region':region,'pass':True})
 write_csv('q4_discharge_region_checks.csv',discharge)
 report={'status':'PASS','checks':{'q2_mux_cases':len(mux),'q2_nand_cases':len(nand),'q3_printed_truth_and_cmos_cases':len(q3rows),'q5_xor_cases':len(xor),'q6a_cmos_cases':len(q6arows),'q6b_cmos_cases':len(q6brows),'q6b_transition_states':len(transitions),'q4_pre_discharge_device_samples':len(regions),'q4_conducting_discharge_device_samples':len(discharge)},'q4_course_resistance_model':{'u_V':u,'trip_V':trip,'exact_transient_claimed':False},'q6b_equivalent_W_over_W':{'p':.5,'n':.5},'limitations':['Ideal switch/Boolean checks do not establish transistor analog performance.','Q4 constant-R divider and frozen-u region samples are labeled approximations; exact waveform requires missing current laws, capacitances, slew and pull-up network.','Conducting discharge samples test voltage inequalities, not a solved dynamic trajectory.','No HSPICE result is claimed.'],'device_counts':{'Q2_core':28,'Q2_select_inverters':6,'Q3':14,'Q6a':10,'Q6b':6}}
 (BASE/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report['checks']));print('PASS')

if __name__=='__main__':main()
