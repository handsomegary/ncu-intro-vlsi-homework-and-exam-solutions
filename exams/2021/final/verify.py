"""Independent ideal logic, clock-phase and algebra checks for readable questions."""
from pathlib import Path
import itertools,csv,json,math,heapq
BASE=Path(__file__).resolve().parent

def write(name,rows):
 with (BASE/name).open('w',encoding='utf-8',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def connected(dev,values,start,target):
 g={}
 for gate,a,b in dev:
  if values[gate]:g.setdefault(a,set()).add(b);g.setdefault(b,set()).add(a)
 seen={start};todo=[start]
 while todo:
  for b in g.get(todo.pop(),[]):
   if b not in seen:seen.add(b);todo.append(b)
 return target in seen

def trace(initial,changes,inv1=1.,inv2=1.,nand=.1):
 # Simultaneous events are applied as one batch, avoiding order-dependent races.
 s={'x':initial[0],'y':initial[1]};s.update(u=1-s['x'],v=s['x']);s['w']=1-(s['u']and s['y']);s['o']=1-(s['v']and s['w'])
 gate={'u':(lambda q:1-q['x'],inv1),'v':(lambda q:1-q['u'],inv2),'w':(lambda q:1-(q['u']and q['y']),nand),'o':(lambda q:1-(q['v']and q['w']),nand)}
 queue=[];seq=0;tokens={k:0 for k in gate};desired={k:s[k]for k in gate};rows=[]
 for t,k,v in changes:heapq.heappush(queue,(float(t),seq,k,v,None));seq+=1
 while queue:
  t=queue[0][0];batch=[]
  while queue and math.isclose(queue[0][0],t,rel_tol=0,abs_tol=1e-9):batch.append(heapq.heappop(queue))
  for _,_,k,v,token in batch:
   if token is not None and token!=tokens[k]:continue
   if s[k]!=v:rows.append({'time':round(t,6),'node':k,'old':s[k],'new':v});s[k]=v
  for k,(fn,delay) in gate.items():
   v=int(fn(s))
   if v!=desired[k]:
    desired[k]=v;tokens[k]+=1
    if v!=s[k]:heapq.heappush(queue,(t+delay,seq,k,v,tokens[k]));seq+=1
 return rows,s

def main():
 rows=[]
 pa=[('A','za','a1'),('B','a1','a2'),('phi','a2','0')]
 po=[('U','zo','e'),('C','zo','e'),('phi','e','0')]
 q3=[('A','f','n1'),('B','n1','n2'),('C','n2','n3'),('D','n2','n3'),('phi','n3','0')]
 q3c=[('a','q','0'),('b','q','0'),('c','q','n'),('d','n','0')]
 for A,B,C in itertools.product([0,1],repeat=3):
  v={'A':A,'B':B,'C':C,'phi':1};u=int(connected(pa,v,'za','0'));v['U']=u;y=int(connected(po,v,'zo','0'))
  assert u==(A&B) and y==((A&B)|C)
  v['phi']=0;assert not connected(pa,v,'za','0')and not connected(po,v,'zo','0')
  rows.append({'A':A,'B':B,'C':C,'evaluate_U':u,'evaluate_Y':y,'precharge_U':0,'precharge_Y':0,'pass':True})
 write('q1_domino_checks.csv',rows)
 logic=[]
 for A,B,C,D in itertools.product([0,1],repeat=4):
  v={'A':A,'B':B,'C':C,'D':D,'a':1-A,'b':1-B,'c':1-C,'d':1-D,'phi':1};h=int(A and B and(C or D));f=1-h
  low_p=connected(q3,v,'f','0');low_q=connected(q3c,v,'q','0')
  assert(low_p,low_q)==(bool(h),bool(f))
  v['phi']=0;assert not connected(q3,v,'f','0')
  # DSL reference devices are analog clamps: validate complementary PDNs only.
  logic.append({'A':A,'B':B,'C':C,'D':D,'h':h,'f':f,'dynamic_evaluate_f':int(not low_p),'DSL_p_ground_path':low_p,'DSL_q_ground_path':low_q,'pass':True})
 write('q3_dynamic_dsl_checks.csv',logic)
 capA=2*.1+2*1;capO=3*.1+2*1;I=7;teval=5.5
 leak=[]
 for name,cap in [('AND',capA),('OR',capO)]:
  drop=I*teval/cap*.001;hold=cap*.5/I*1000
  assert 1.8-drop>1.3
  leak.append({'gate':name,'dynamic_cap_fF':cap,'conservative_I_nA':I,'evaluation_ns':teval,'droop_bound_V':drop,'retained_high_lower_V':1.8-drop,'logic_high_threshold_V':1.3,'leakage_only_retention_ns':hold,'pass':True})
 write('q1_retention_checks.csv',leak)
 widths={'N1':100,'N2':100,'N3':100,'P1':200,'P2':200,'P3':200};r={k:(100 if k.startswith('N') else 200)/w for k,w in widths.items()}
 vplus=2*r['N1']/(r['N1']+r['N3'])+.4;vminus=2*r['P3']/(r['P1']+r['P3'])-.4
 assert math.isclose(vplus,1.4) and math.isclose(vminus,.6) and r['N1']+r['N2']==2 and r['P1']+r['P2']==2
 write('q2_balanced_size_checks.csv',[{'device':k,'width_nm':w,'length_nm':40,'R_over_R':r[k],'pass':True}for k,w in widths.items()])
 control=[]
 for rn4 in [3,2,1,.5,.25]:control.append({'R_N4_over_R':rn4,'u_N_V':2/(2+rn4),'V_T_plus_V':.4+2/(2+rn4),'pass':True})
 assert all(control[i+1]['V_T_plus_V']>control[i]['V_T_plus_V']for i in range(len(control)-1));write('q2_series_control_checks.csv',control)
 H=2980.;ratio=H**(1/8);opt=[{'N':n,'delay_over_tau':n*H**(1/n),'same_polarity':n%2==0}for n in range(2,15)]
 assert min(opt,key=lambda z:z['delay_over_tau'])['N']==8;write('q5_stage_count_checks.csv',opt)
 sizing=[{'stage':i+1,'Cin_over_Cg':ratio**i,'W_N_over_Wmin':ratio**i,'W_P_over_Wmin':ratio**i,'L_over_Lmin':1,'Cout_over_Cg':ratio**(i+1),'stage_effort':ratio,'pass':True}for i in range(8)];write('q5_buffer_sizes.csv',sizing)
 states=[]
 for x,y in [(0,0),(0,1),(1,0),(1,1)]:
  u=1-x;v=x;w=int(not(u and y));o=int(not(v and w));assert o==1-x
  states.append({'x':x,'y':y,'u':u,'v':v,'w':w,'o':o})
 write('q5_settled_truth.csv',states)
 activities=[]
 for k in ['u','v','w','o']:
  all_trans=sum(states[i][k]!=states[(i+1)%4][k] for i in range(4));charging=sum(states[i][k]==0 and states[(i+1)%4][k]==1 for i in range(4))
  assert all_trans==2 and charging==1
  activities.append({'node':k,'cycle_steps':4,'total_transitions':all_trans,'charging_transitions':charging,'alpha_all':all_trans/4,'alpha_01':charging/4,'pass':True})
 write('q5_activity_checks.csv',activities)
 traces=[]
 # Check specified ideal simultaneous steps across varying positive inverter/NAND delays.
 cases=0
 for di1,di2,dn in itertools.product([.1,1,3],repeat=3):
  for i,state in enumerate(states):
   nxt=states[(i+1)%4];changes=[(0.,k,nxt[k])for k in ['x','y']if state[k]!=nxt[k]]
   tr,end=trace((state['x'],state['y']),changes,di1,di2,dn)
   for k in ['u','v','w','o']:assert sum(e['node']==k for e in tr)==int(state[k]!=nxt[k])
   assert all(end[k]==nxt[k]for k in nxt)
   cases+=1
   for e in tr:traces.append({'case':cases,'from_xy':f"{state['x']}{state['y']}",'to_xy':f"{nxt['x']}{nxt['y']}",'inv1_delay':di1,'inv2_delay':di2,'equal_nand_delay':dn,**e,'pass':True})
 write('q5_ideal_event_checks.csv',traces)
 skew,end=trace((1,1),[(0,'x',0),(1.5,'y',0)],1,1,.1)
 assert sum(e['node']=='o' for e in skew)==3 and end['o']==1
 write('q5_skew_glitch_example.csv',[{**e,'pass':True}for e in skew])
 report={'status':'PASS','checks':{'q1_input_cases':len(rows),'q3_dynamic_and_complement_PDN_cases':len(logic),'q1_retention_bounds':len(leak),'q2_device_widths':len(widths),'q2_control_sweep_cases':len(control),'q5_candidate_stage_counts':len(opt),'q5_ideal_transition_timing_cases':cases,'q5_skew_example_output_edges':3},'q1_Tmin_ns':11,'q2_thresholds_V':{'plus':vplus,'minus':vminus},'q5_ratio':ratio,'q5_min_delay_over_tau':8*ratio,'q5_sum_output_cap_over_Cg':sum(ratio**i for i in range(1,9)),'q5_power_coefficient_per_step_f_V2_Cg':.25*sum(ratio**i for i in range(1,9)),'q6_answer':'missing original timing premises; numerical/reg insertion answers skipped','limits':['No HSPICE result.','DSL test verifies complementary pull-down conditions, not analog reference/load ratios.','Q1 current bound intentionally overcounts leakage magnitudes.','Q5 ideal no-glitch claim assumes simultaneous steps and complete settling; skew example demonstrates equal NAND delays alone are insufficient.']}
 (BASE/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
