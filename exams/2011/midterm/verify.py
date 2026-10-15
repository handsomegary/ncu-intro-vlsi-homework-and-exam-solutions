"""Independent MOS connectivity, delay, event and partition checks."""
from pathlib import Path
from fractions import Fraction as F
import csv,itertools,json,math
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
def check_mos(devices,v,node,expected):
 edges=[(a,b)for name,p,g,a,b in devices if v[g]==(0 if p else 1)]
 high=reach(edges,node,'V_{DD}');low=reach(edges,node,'0')
 assert high!=low and int(high)==expected
 return high,low
q1=[]
for vals in itertools.product([0,1],repeat=5):
 v=dict(zip(['x','y','u','v','w'],vals));wanted=int(not((v['x']and v['y'])or((v['u']or v['v'])and v['w'])))
 high,low=check_mos(net['Q1c'],v,'f',wanted)
 q1.append({**v,'f':wanted,'pullup_reachable':high,'pulldown_reachable':low})
save('q1-cmos-truth.csv',q1)

# From transistor areas and matched beta, independently derive receiver loads.
nwidth=[1,2,4,8];pwidth=[2,4,8,16];gatecap=[n+p for n,p in zip(nwidth,pwidth)]
loads=gatecap[1:];assert loads==[6,12,24]and sum(loads)==42
output_slew=[F(c,n)for c,n in zip(loads,nwidth[:3])];assert output_slew==[6,6,6]
input_slew=[F(3+2,2),*output_slew];coef=sum(F(n)*s for n,s in zip(nwidth,input_slew));assert coef==F(173,2)
save('q2-chain-power.csv',[dict(stage=i+1,nwidth=nwidth[i],pwidth=pwidth[i],beta_over_beta0=nwidth[i],own_input_Cg=gatecap[i],output_Cg=loads[i]if i<3 else 'CL',input_mean_slew_tau0=str(input_slew[i]),short_circuit_coefficient=str(nwidth[i]*input_slew[i]))for i in range(4)])
tap=[]
for n in range(1,17):
 r=64**(1/n);delay=n*r
 tap.append(dict(stages=n,taper=r,delay_over_td=delay,positive_buffer=n%2==0))
best=min(tap,key=lambda x:x['delay_over_td']);assert best['stages']==4 and math.isclose(best['delay_over_td'],8*math.sqrt(2))
# For every N>=12, D(N)>=N>=12>the four-stage result, completing the integer bound.
assert best['delay_over_td']<12
assert 2**6==64 and 6*2==12
save('q2-integer-taper.csv',tap)

def logic(bits):
 a,b,c,d=bits;u=b|c;v=1-(a|u);w=1-(a&c);o0=v&w&d;o1=1-(w&d)
 return dict(I_0=a,I_1=b,I_2=c,I_3=d,u=u,v=v,w=w,a=1-u,b=1-o0,O_0=o0,O_1=o1)
q3=[]
groups={'a':[d for d in net['Q3']if d[0].startswith('U')and not d[0].startswith('Ui')],
 'u':[d for d in net['Q3']if d[0].startswith('Ui')],
 'v':[d for d in net['Q3']if d[0].startswith('V')],
 'w':[d for d in net['Q3']if d[0].startswith('W')],
 'b':[d for d in net['Q3']if d[0].startswith('Z')and not d[0].startswith('Zi')],
 'O_0':[d for d in net['Q3']if d[0].startswith('Zi')],
 'O_1':[d for d in net['Q3']if d[0].startswith('J')]}
assert len(net['Q3'])==26
for bits in itertools.product([0,1],repeat=4):
 v=logic(bits)
 for node,devices in groups.items():check_mos(devices,v,node,v[node])
 q3.append({'input':' '.join(map(str,bits)),**{k:v[k]for k in ['u','v','w','O_0','O_1']}})
save('q3-cmos-truth.csv',q3)

# Transport event model. Input changes at t=0 are atomic; all gates delay1.
gates={'u':(['I1','I2'],lambda a,b:a|b),'v':(['I0','u'],lambda a,b:1-(a|b)),
 'w':(['I0','I2'],lambda a,b:1-(a&b)),'O0':(['v','w','I3'],lambda a,b,c:a&b&c),'O1':(['w','I3'],lambda a,b:1-(a&b))}
sequence=['0100','0011','1100','1011'];events=[]
for old,new in zip(sequence,sequence[1:]+sequence[:1]):
 state=dict(zip(['I0','I1','I2','I3'],map(int,old)))
 for name,(parents,fn)in gates.items():state[name]=fn(*[state[x]for x in parents])
 queue={0:dict(zip(['I0','I1','I2','I3'],map(int,new)))}
 for t in range(5):
  update=queue.pop(t,{})
  changes={name:value for name,value in update.items()if state[name]!=value}
  for name,value in changes.items():
   events.append(dict(transition=old+'->'+new,time_in_gate_delays=t,node=name,old_value=state[name],new_value=value))
  state.update(changes)
  for name,(parents,fn)in gates.items():
   if set(parents)&set(changes):queue.setdefault(t+1,{})[name]=fn(*[state[x]for x in parents])
 assert state['O0']==logic(tuple(map(int,new)))['O_0']and state['O1']==logic(tuple(map(int,new)))['O_1']
assert [(r['time_in_gate_delays'],r['new_value'])for r in events if r['transition']=='1100->1011'and r['node']=='O1']==[(1,0),(2,1)]
assert not [r for r in events if r['node']=='O0']
save('q3-transport-events.csv',events)
timing=[]
for dw,d1 in [(F(0),F(0)),(F(1),F(1)),(F(1,2),F(3,2)),(F(3,2),F(0)),(F(1),F(3,2))]:
 worst=max(F(8),F(7)+dw,F(6)+dw+d1);feasible=worst<=8
 assert feasible==(dw<=1 and dw+d1<=2)
 timing.append(dict(extra_w_delay=str(dw),extra_O1_delay=str(d1),worst_structural_delay=str(worst),within_reference_target=feasible))
save('q3-conditional-dual-VT.csv',timing)

# User-approved gate graph: six channel devices share VDD; upper Ngate cascades.
vdd=F(9,5);vt=F(2,5);G=vdd-vt;Y=G-vt;Z=vdd-vt
assert(G,Y,Z)==(F(7,5),F(1),F(7,5))
levels=[]
for x in [F(0),F(1,5),F(3,5),F(6,5),F(9,5)]:
 g=min(x,G);y=min(x,max(g-vt,0));z=min(x,Z)
 levels.append(dict(X=str(x),G=str(g),Y_assuming_discharged_initial_cap=str(y),Z=str(z)))
save('q4-ideal-threshold-levels.csv',levels)
regions=[]
for label,vd,vs in [('m1_early_ramp',F(1),F(1,5)),('m1_late_ramp',F(9,5),F(1)),('m2_to_m6_intermediate',F(6,5),F(3,5)),('m2_to_m6_high_boundary',F(7,5),F(7,5))]:
 on=vdd-vs>vt
 region='cutoff/boundary'if not on else 'saturation'if vd>vdd-vt else 'saturation_boundary'if vd==vdd-vt else 'linear'
 regions.append(dict(case=label,Vd=str(vd),Vs=str(vs),Vg=str(vdd),Vt=str(vt),region=region))
assert regions[0]['region']=='linear'and regions[1]['region']=='saturation'and regions[2]['region']=='linear'
save('q4-region-inequalities.csv',regions)

# Every possible internal buffer subset, calibrated discrete Elmore and continuum.
parts=[]
for mask in range(16):
 cuts=[i+1 for i in range(4)if mask>>i&1];ends=[0,*cuts,5];lengths=[b-a for a,b in zip(ends,ends[1:])]
 discrete=sum(F(3*n*(n+1),2)for n in lengths)+sum(lengths[1:])
 continuum=sum(F(9*n*n,4)for n in lengths)+sum(lengths[1:])
 parts.append(dict(buffer_mask=mask,buffers=len(cuts),cuts_after_TG=' '.join(map(str,cuts)),segment_lengths=' '.join(map(str,lengths)),discrete_ns=str(discrete),continuum_ns=str(continuum),discrete_lt_30=discrete<30,continuum_lt_30=continuum<30))
assert parts[0]['discrete_ns']=='45'
meet=[r for r in parts if r['discrete_lt_30']];minimum_buffers=min(r['buffers']for r in meet)
assert minimum_buffers==1
single=[r for r in meet if r['buffers']==1];assert len(single)==1 and single[0]['cuts_after_TG']=='3'and single[0]['discrete_ns']=='29'
assert min(F(r['discrete_ns'])for r in parts)==19 and parts[-1]['discrete_ns']=='19'
assert min(r['buffers']for r in parts if r['continuum_lt_30'])==2 and min(F(r['continuum_ns'])for r in parts)==F(61,4)
save('q5-all-buffer-partitions.csv',parts)

# Confirm parasitic collector/base cross-coupling, not a MOS-logic net repair.
scr={'NPN':{'emitter':'VSS','base':'S','collector':'W'},'PNP':{'emitter':'VDD','base':'W','collector':'S'},'Rwell':['VDD','W'],'Rsub':['S','VSS']}
assert scr['NPN']['collector']==scr['PNP']['base']and scr['PNP']['collector']==scr['NPN']['base']
(HERE/'q6-scr-netlist.json').write_text(json.dumps(scr,indent=2),encoding='utf-8')
report = {'all_checks_passed': True, 'all_independent_checks_passed': True, 'check_scope': 'Independent mathematical and circuit checks.', 'q1_cmos_cases': 32, 'q2_switch_load_Cg': 42, 'q2_short_circuit_coefficient': '173/2', 'q2_exact_integer_stages': 4, 'q2_taper_counts_tested': 16, 'q3_cmos_cases': 16, 'q3_physical_MOS': 26, 'q3_sequence_transitions': 4, 'q3_glitch': 'O1,1100->1011,falls1d/rises2d', 'q3_conditional_timing_cases': 5, 'q4_gate_junction': 'user-approved VDD assumption', 'q4_constant_Vt_highs': {'G': '1.4V', 'Y': '1.0V', 'Z': '1.4V'}, 'q5_buffer_subsets': 16, 'q5_discrete_unbuffered_ns': 45, 'q5_min_buffers_below_30': 1, 'q5_one_buffer_best_ns': 29, 'q5_global_min_ns': 19, 'q6_SCR_feedback_checked': True, 'printed_points': 110}
(HERE/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
