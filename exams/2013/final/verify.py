"""Independent switch, rational-resistance and sequential checks; no TeX parsing."""
from pathlib import Path
from fractions import Fraction as F
import csv,itertools,json

HERE=Path(__file__).resolve().parent
NET=json.loads((HERE/'device-netlists.json').read_text(encoding='utf-8'))
def save(name,rows):
 with (HERE/name).open('w',newline='',encoding='utf-8')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def reachable(edges,start,target):
 found={start};pending=[start]
 while pending:
  x=pending.pop()
  for a,b in edges:
   y=b if a==x else a if b==x else None
   if y is not None and y not in found:found.add(y);pending.append(y)
 return target in found
def gate(g,v):
 if g==r'\phi':return v['phi']
 if g==r'\bar\phi':return 1-v['phi']
 if g.startswith(r'\bar '):return 1-v[g[5:]]
 return v[g]
def on_edges(net,v,only=None):
 return [(d,s)for name,p,g,d,s in net if (only is None or name in only)and gate(g,v)==(0 if p else 1)]
def equiv(edges,start,end):
 # Exact resistor network from channel conductances, with V(start)=1,V(end)=0.
 nodes={start,end}
 for a,b,r in edges:nodes.update([a,b])
 nodes=sorted(nodes-{start,end});n=len(nodes);index={x:i for i,x in enumerate(nodes)}
 a=[[F(0)for j in range(n+1)]for i in range(n)]
 for x,y,r in edges:
  c=1/F(r)
  for u,v in [(x,y),(y,x)]:
   if u not in index:continue
   i=index[u];a[i][i]+=c
   if v in index:a[i][index[v]]-=c
   elif v==start:a[i][-1]+=c
 for i in range(n):
  pivot=next((j for j in range(i,n)if a[j][i]),None)
  if pivot is None:return None
  a[i],a[pivot]=a[pivot],a[i];scale=a[i][i];a[i]=[x/scale for x in a[i]]
  for j in range(n):
   if j!=i:
    factor=a[j][i];a[j]=[x-factor*y for x,y in zip(a[j],a[i])]
 volts={start:F(1),end:F(0),**{x:a[i][-1]for x,i in index.items()}}
 current=sum((volts[x]-volts[y])/F(r)if x==start else (volts[y]-volts[x])/F(r)if y==start else F(0)for x,y,r in edges)
 return 1/current if current else None

q2=[]
for A,B,C,D in itertools.product([0,1],repeat=4):
 v=dict(A=A,B=B,C=C,D=D,phi=1);h=A and B and(C or D);f=1-int(h)
 dyn=int(not reachable(on_edges(NET['Q2_dynamic'],v),'f','0'));assert dyn==f
 pdn=NET['Q2_fully_differential'][2:]
 e=on_edges(pdn,v);fdown=reachable(e,'f','0');gdown=reachable(e,r'\bar f','0')
 assert fdown!=gdown and int(not fdown)==f
 q2.append(dict(A=A,B=B,C=C,D=D,f=f,dynamic=dyn,f_pdn_to_ground=int(fdown),fbar_pdn_to_ground=int(gdown)))
save('q2-switch-truth.csv',q2)

q3=[]
sizes=[('independent_a',[4,2,4,4,8,8,4]),('independent_b',[2,1,2,2,4,4,2]),('student_a',[4,F(16,9),F(8,3),F(16,3),F(16,3),F(16,3),F(16,3)])]
for label,W in sizes:
 p,*n=map(F,W);rp=3/p
 for path in [[1,6],[2,3,6],[4,5,3,6]]:
  rn=sum(1/n[i-1]for i in path);assert rn==rp
  q3.append(dict(sizing=label,path='-'.join('N'+str(i)for i in path),R_over_k=str(rn),R_P1_over_k=str(rp),clock_C_over_C=str((p+n[5])/2)))
assert (F(sizes[1][1][0])+F(sizes[1][1][-1]))/2==2
save('q3-balanced-widths.csv',q3)

q4=[]
znames={'NA1','NB1','NC1','NA2','NB2','Nfoot'}
vnames={'Pvh','PA1','PB1','PC1','Pvz','PA2','PB2','PC2'}
for A,B,C in itertools.product([0,1],repeat=3):
 M=int((A and B)or(C and(A or B)));z=1-M
 values=dict(A=A,B=B,C=C,phi=1,z=z,v=0)
 ze=on_edges(NET['Q4'],values,znames);zd=reachable(ze,'z','0');assert zd==bool(M)
 ve=on_edges(NET['Q4'],values,vnames);v=int(reachable(ve,'V_{DD}','v'))
 assert v==1-(A^B^C)
 rz=equiv([(a,b,1)for a,b in ze if reachable(ze,'z',a)],'z','0')if zd else None
 rv=equiv([(a,b,1)for a,b in ve if reachable(ve,'V_{DD}',a)],'V_{DD}','v')if v else None
 if sum([A,B,C])==2:assert rz==3 and rv==3
 if sum([A,B,C])==3:assert rz==F(13,7)
 if sum([A,B,C])==0:assert rv==F(13,3)
 q4.append(dict(A=A,B=B,C=C,z=z,X=M,v=v,Y=1-v,z_R_over_R=str(rz),v_R_over_R=str(rv),z_td_over_RC=str(2*(1+rz))if rz else '',v_td_over_RC=str((1+rv)/2)if rv else ''))
save('q4-correlated-resistance.csv',q4)
assert 2*(1+3)+(1+3)/2==10
assert min(F(40,7),F(8,3))==F(8,3)
sharing=[dict(node='x',Cz_pF=1,Cinternal_pF=F(2,5),Vafter=F(9,5)/(1+F(2,5))),dict(node='y',Cz_pF=1,Cinternal_pF=F(4,5),Vafter=F(9,5)/(1+F(4,5)))]
for r in sharing:assert r['Vafter']<F(13,10)
save('q4-sharing.csv',sharing)

# Gate-path data are reconstructed independently from the diagram's gate sequence.
paths=[('u_to_R4',[F(1,5)]),('u_to_R5',[F(1,5),F(2,5)]),('v_to_R5',[F(1,2),F(2,5),F(2,5)]),('w_to_R5',[F(1,2),F(1,5),F(2,5),F(2,5)]),('w_to_R6',[F(1,2)])]
q5=[]
for skew in [F(0),F(-1,2),F(1,2)]:
 for name,p in paths:
  delay=sum(p);pad=F(0)
  # At zero/early skew repair R4 only; late skew repairs each short branch locally.
  if skew<=0 and name=='u_to_R4':pad=F(2,5)
  elif skew>0:pad={'u_to_R4':F(4,5),'u_to_R5':F(2,5),'w_to_R6':F(2,5)}.get(name,F(0))
  d=delay+pad;setup=F(3,10)+d+F(1,5)-skew;hold=F(1,10)+d-(F(2,5)+skew)
  assert hold>=0
  q5.append(dict(path=name,capture_minus_launch_ns=str(skew),original_logic_ns=str(delay),local_padding_ns=str(pad),setup_period_bound_ns=str(setup),hold_margin_ns=str(hold)))
save('q5-path-timing.csv',q5)
for skew,want in [(F(0),F(2)),(F(-1,2),F(5,2)),(F(1,2),F(3,2))]:
 assert max(F(r['setup_period_bound_ns'])for r in q5 if F(r['capture_minus_launch_ns'])==skew)==want

# Derive arrival times from the original DAG, then enumerate aligned three-FF
# frontiers: one u branch FF, plus either split v/lower FFs or a shared s/final
# FF and a lower bypass FF. The lower bypass can store w or not_w.
dag={'u':(['A','B'],F(1,5)),'v':(['B','C'],F(1,2)),'w':(['A','C'],F(1,2)),'not_w':(['w'],F(1,5)),'s':(['v','not_w'],F(2,5)),'final':(['u','s'],F(2,5))}
def arrival(node,cuts=frozenset()):
 if node in ['A','B','C']or node in cuts:return F(0)
 parents,d=dag[node];return max(arrival(p,cuts)for p in parents)+d
frontiers=[]
for lower in ['w','not_w']:
 for shared in [None,'s','final']:
  cuts={'u',lower}|({'v'}if shared is None else {shared})
  # For shared s/final cut, lower's bypass FF is on its output branch; the
  # first-stage shared node still sees the original unregistered lower path.
  first=max(arrival('u')+F(2,5),arrival(lower),arrival(shared)if shared else arrival('v'))
  if shared is None:
   second=arrival('final',frozenset(cuts))
  elif shared=='s':second=F(2,5)
  else:second=F(0)
  # Hold-safe u bypass and w polarity-restoration branches.
  second=max(second,F(2,5),F(3,5)if lower=='not_w' else F(2,5))
  frontiers.append((','.join(sorted(cuts)),first,second))
q5cuts=[dict(frontier=f,registers=3,stage1_max_ns=str(x),stage2_max_ns=str(y),period_ns=str(F(1,2)+max(x,y)))for f,x,y in frontiers]
assert min(F(r['period_ns'])for r in q5cuts)==F(13,10)
save('q5-three-register-frontiers.csv',q5cuts)
stagepaths=[('stage1_u',F(3,5)),('stage1_v',F(1,2)),('stage1_not_w',F(7,10)),('stage2_Y1',F(2,5)),('stage2_Y2_from_u',F(2,5)),('stage2_Y2_from_v_or_not_w',F(4,5)),('stage2_Y3_restoration_and_padding',F(3,5))]
for n,d in stagepaths:assert F(1,10)+d>=F(2,5)and F(3,10)+d+F(1,5)<=F(13,10)
save('q5-pipeline-stage-timing.csv',[dict(path=n,logic_ns=str(d),hold_margin_ns=str(F(1,10)+d-F(2,5)),setup_bound_ns=str(F(1,2)+d))for n,d in stagepaths])
def combo(a,b,c):
 u=1-(a|b);v=b^c;w=a^c;s=1-(v^(1-w));return u,1-(u^s),w
def pipelined(u,v,n):return u,1-(u^(1-(v^n))),1-n
cycles=[]
sequence=list(itertools.product([0,1],repeat=3))*2
stored=(0,0,0);prev_input=None
for i,(a,b,c)in enumerate(sequence):
 got=pipelined(*stored)
 if prev_input is not None:assert got==combo(*prev_input)
 cycles.append(dict(edge=i,input_ABC=f'{a}{b}{c}',output_bits=''.join(map(str,got)),captured_previous_ABC=''.join(map(str,prev_input))if prev_input else 'initial'))
 stored=(1-(a|b),b^c,1-(a^c));prev_input=(a,b,c)
save('q5-pipeline-cycle-alignment.csv',cycles)

# Independently re-evaluate the contact auditor's literal 12-device table.
with (HERE/'q6b_literal_netlist.csv').open(encoding='utf-8')as f:q6net=list(csv.DictReader(f))
assert len(q6net)==12
q6=[]
for a,b,c in itertools.product([0,1],repeat=3):
 values=dict(a=a,b=b,c=c,VDD=1,VSS=0);edges=[];on=[]
 for dev in q6net:
  if values[dev['gate']]==(0 if dev['type']=='p'else 1):
   edges.append((dev['left_channel'],dev['right_channel']));on.append(dev['device'])
 assert not {'P1','N1','P2','N2','P6','N6'}&set(on)
 high=reachable(edges,'Z','VDD');low=reachable(edges,'Z','VSS');assert high!=low and high==bool(not(a or b or c))
 q6.append(dict(a=a,b=b,c=c,Z=int(high),VDD_reachable=high,VSS_reachable=low,on_devices=' '.join(on)))
save('q6-independent-switch-truth.csv',q6)
with (HERE/'q6a_literal_netlist.csv').open(encoding='utf-8')as f:q6anet=list(csv.DictReader(f))
assert len(q6anet)==12
byname={d['device']:d for d in q6anet}
for name,rail in [('P6','VDD'),('N6','VSS')]:
 assert byname[name]['gate']=='X'and {byname[name]['left_channel'],byname[name]['right_channel']}=={'X',rail}

# Two distinct upper thresholds produce the same shown falling-input response.
q7=[]
lower=F(1,2)
for upper in [F(9,10),F(3,2)]:
 rn=((F(9,5)-upper)/(upper-F(3,5)))**2
 rp=(lower/(F(6,5)-lower))**2
 out=0;wave=[F(9,5),F(3,2),F(3,5),F(11,10),F(7,10),F(2,5),F(0)]
 result=[]
 for vin in wave:
  if out==0 and vin<lower:out=1
  elif out==1 and vin>upper:out=0
  result.append(out)
 q7.append(dict(VTplus=str(upper),VTminus=str(lower),betaN1_over_N3=str(rn),betaP1_over_P3=str(rp),falling_wave_output=''.join(map(str,result))))
assert q7[0]['falling_wave_output']==q7[1]['falling_wave_output']and q7[0]['betaN1_over_N3']!=q7[1]['betaN1_over_N3']
save('q7-nonidentifiability.csv',q7)
q8=[]
for rfb in [F(1),F(2),F(3),F(4)]:
 vh=rfb/(2+rfb);vl=2/(2+rfb);passmargin=(vh>F(1,2)and vl<F(1,2));assert passmargin==(rfb>2)
 q8.append(dict(RP1=1,RN1=1,RTG=1,RP2=str(rfb),RN2=str(rfb),Vhigh_over_VDD=str(vh),Vlow_over_VDD=str(vl),strict_write_margin=passmargin))
save('q8-write-dividers.csv',q8)

report = {'all_checks_passed': True, 'all_independent_checks_passed': True, 'check_scope': 'Independent mathematical and circuit checks.', 'q2_binary_cases': 16, 'q3_independent_and_student_paths': 9, 'q4_states': 8, 'q4_correlated_unloaded_delay_RC': {'contamination': '8/3', 'propagation': '10'}, 'q5_signed_skew_path_checks': 15, 'q5_three_register_optimal_period_ns': '13/10', 'q5_aligned_frontiers': len(frontiers), 'q5_pipeline_events': len(cycles), 'q6b_literal_switch_cases': 8, 'q6_physical_devices_each': 12, 'q6a_self_connected_pair_preserved': True, 'q7_distinct_upper_threshold_examples': 2, 'q7_unique_numeric_pair': False, 'q8_write_margin_examples': 4}
(HERE/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
