"""2008 final Q2/Q3/Q7: original-derived ideal MOS conduction checks."""
from pathlib import Path
from itertools import product
import csv,json
OUT=Path(__file__).resolve().parent
def save(name,rows):
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
FIELDS=['device','type','left_channel','right_channel','gate']
def net(name,ds):save(name,[dict(zip(FIELDS,d)) for d in ds])
def connected(ds,val,a,b):
 graph={}
 for _,kind,x,y,g in ds:
  if val[g]==(0 if kind=='p' else 1):graph.setdefault(x,set()).add(y);graph.setdefault(y,set()).add(x)
 seen=set();todo=[a]
 while todo:
  n=todo.pop()
  if n==b:return True
  if n not in seen:seen.add(n);todo.extend(graph.get(n,set())-seen)
 return False
def rails(ds,val,node):return connected(ds,val,node,'VDD'),connected(ds,val,node,'VSS')

H=[('NA','n','F','bc','A'),('NB','n','bc','VSS','B'),('NC','n','bc','VSS','C'),('ND','n','F','de','D'),('NE','n','de','VSS','E')]
G=[('NAbar','n','Fbar','g1','Abar'),('NBbar','n','Fbar','g2','Bbar'),('NCbar','n','g2','g1','Cbar'),('NDbar','n','g1','VSS','Dbar'),('NEbar','n','g1','VSS','Ebar')]
P=[('PA','p','VDD','p1','A'),('PB','p','VDD','p2','B'),('PC','p','p2','p1','C'),('PD','p','p1','F','D'),('PE','p','p1','F','E')]
static=H+P
diff=H+G+[('PF','p','VDD','F','Fbar'),('PFbar','p','VDD','Fbar','F')]
comp=[(p+'_INV_'+g+'bar',p.lower(),'VDD' if p=='P' else g+'bar',g+'bar' if p=='P' else 'VSS',g) for g in 'ABCDE' for p in ('P','N')]
dom=[]
for name,k,a,b,g in G:dom.append((name,k,{'Fbar':'Z','VSS':'foot'}.get(a,a),{'Fbar':'Z','VSS':'foot'}.get(b,b),g))
dom+=[('Ppre','p','VDD','Z','phi'),('Nfoot','n','foot','VSS','phi'),('Pout','p','VDD','F','Z'),('Nout','n','F','VSS','Z')]
assert len(dom)==9 and len(diff)==12 and len(static)==10
assert len({d[0] for d in dom+comp})==19 and len({d[0] for d in diff+comp})==22
net('q2_domino_complete_netlist.csv',dom+comp);net('q2_differential_complete_netlist.csv',diff+comp);net('q2_static_netlist.csv',static)
truth=[];phases=[];candidates=[]
for bits in product((0,1),repeat=5):
 val=dict(zip('ABCDE',bits));val.update({g+'bar':1-v for g,v in zip('ABCDE',bits)});val.update(VDD=1,VSS=0)
 a,b,c,d,e=bits;h=int(a and(b or c)or(d and e));f=1-h
 assert int((not a or(not b and not c))and(not d or not e))==f
 assert rails(static,val,'F')==((True,False)if f else(False,True))
 stable=[]
 for candidatef,candidateg in product((0,1),repeat=2):
  v=dict(val,F=candidatef,Fbar=candidateg);rf=rails(diff,v,'F');rg=rails(diff,v,'Fbar')
  ok=rf==((True,False)if candidatef else(False,True)) and rg==((True,False)if candidateg else(False,True))
  if ok:stable.append((candidatef,candidateg))
  candidates.append({'ABCDE':''.join(map(str,bits)),'candidate_F':candidatef,'candidate_Fbar':candidateg,'rail_consistent':ok})
 assert stable==[(f,h)]
 for phi in(0,1):
  v=dict(val,phi=phi,Z=1 if phi==0 else h)
  assert rails(dom,v,'F')==((False,True)if phi==0 or f==0 else(True,False))
  assert connected(dom,v,'Z','VSS')==bool(phi and f)
  phases.append({'ABCDE':''.join(map(str,bits)),'phi':phi,'Z':v['Z'],'F':0 if not phi else f})
 truth.append({'ABCDE':''.join(map(str,bits)),'h_A_times_BplusC_or_DE':h,'required_f':f,'static_f':f,'differential_F':f,'differential_Fbar':h,'domino_evaluated_F':f})
save('q2_truth.csv',truth);save('q2_domino_phases.csv',phases);save('q2_differential_candidates.csv',candidates)

q3=[('P1','p','VDD','t1','I'),('Pclock1','p','t1','A','phi'),('N1','n','A','VSS','I'),('P2','p','VDD','t2','A'),('Pclock2','p','t2','B','phi'),('N2','n','B','VSS','A'),('P3','p','VDD','C','B'),('Nclock3','n','C','t3','phi'),('N3','n','t3','VSS','B'),('P4','p','VDD','O','C'),('Nclock4','n','O','t4','phi'),('N4','n','t4','VSS','C')]
net('q3_dynamic_register_netlist.csv',q3);rows=[]
for old,current,after in product((0,1),repeat=3):
 a=1-current;b=current;c=1 if not b else 1-old;o=1 if not c else old
 assert o==old
 low={'I':current,'A':a,'B':b,'C':c,'phi':0}
 assert rails(q3,low,'A')==((True,False)if a else(False,True))
 assert rails(q3,low,'B')==((True,False)if b else(False,True))
 high_a=0 if after else a;high_b=0 if high_a else b;assert high_b==current
 high_c=1-high_b;high_o=1-high_c
 high={'I':after,'A':high_a,'B':high_b,'C':high_c,'phi':1}
 assert rails(q3,high,'C')==((True,False)if high_c else(False,True))
 assert rails(q3,high,'O')==((True,False)if high_o else(False,True))
 rows.append({'old_sample':old,'I_before_rising':current,'I_after_rising':after,'low_A':a,'low_B':b,'low_C':c,'low_O_held':o,'high_A':high_a,'high_B_held':high_b,'high_C':high_c,'high_O_sampled':high_o})
save('q3_phase_histories.csv',rows)

q7a=[('P1','p','Y','u','Cbar'),('N1','n','Y','u','C'),('P2','p','u','v','C'),('N2','n','u','v','Cbar'),('P3','p','v','VDD','X'),('N3','n','v','VSS','X'),('P4','p','VDD','X','u'),('N4','n','VSS','X','u')]
net('q7a_literal_netlist.csv',q7a);rows=[]
for y,c in product((0,1),repeat=2):
 valid=[]
 for u,v,x in product((0,1),repeat=3):
  val={'Y':y,'C':c,'Cbar':1-c,'u':u,'v':v,'X':x}
  # Include the ideal external input's supply connection while TG1 is ON.
  driven=q7a+[('externalY','n','Y','VDD' if y else 'VSS','one')];val['one']=1
  ok=all(rails(driven,val,n)==((True,False)if value else(False,True))for n,value in [('u',u),('v',v),('X',x)])
  if ok:valid.append((u,v,x))
  rows.append({'Y':y,'C':c,'candidate_u':u,'candidate_v':v,'candidate_X':x,'rail_consistent':ok})
 assert valid==([(y,y,1-y)]if c else[(0,0,1),(1,1,0)])
save('q7a_latch_candidates.csv',rows)
q7b=[('P1','p','p0','p1','VDD'),('N1','n','n0','n1','VSS'),('P2','p','p1','VDD','VDD'),('N2','n','n1','VSS','VSS'),('P3','p','VDD','Z','a'),('N3','n','VSS','n3','a'),('P4','p','Z','VDD','b'),('N4','n','n3','n4','b'),('P5','p','VDD','Z','c'),('N5','n','n4','Z','c'),('P6','p','Z','p6','VDD'),('N6','n','Z','n6','VSS')]
net('q7b_literal_netlist.csv',q7b);rows=[]
for a,b,c in product((0,1),repeat=3):
 val={'a':a,'b':b,'c':c,'VDD':1,'VSS':0};z=int(not(a and b and c));assert rails(q7b,val,'Z')==((True,False)if z else(False,True))
 rows.append({'abc':f'{a}{b}{c}','Z_NAND3':z,'PUN_conducts':bool(z),'PDN_conducts':not bool(z),'physical_MOS':12,'OFF_devices':6})
save('q7b_switch_truth.csv',rows)
report={'all_checks_passed':True,'Q2':{'function':'NOT(A*(B+C)+D*E)','domino_core_MOS':9,'domino_complete_MOS':19,'differential_core_MOS':12,'differential_complete_MOS':22,'static_MOS':10,'truth_states':32,'differential_candidates':128,'domino_phases':64},'Q3':{'register':'positive-edge noninverting dynamic','physical_MOS':12,'phase_histories':8},'Q7a':{'physical_MOS':8,'topology':'2 TG+2 INV; first TG pCbar/nC, secondTG pC/nCbar; INVX->v,INVu->X','positive_level_inverting_latch':True,'candidates':32,'source_gap_evidence':'190 native white pixels separate dataY metal from independent clockC strip; see q7a-gap-evidence.json'},'Q7b':{'physical_MOS':12,'functional_MOS':6,'OFF_MOS':6,'function':'Z=NOT(a*b*c)','truth_states':8},'scope':'source-derived ideal Boolean/MOS switch checks, no process simulation or DRC'}
(OUT/'logic-layout-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'all_checks_passed':True,'Q2_truth':32,'Q3_histories':8,'Q7a_candidates':32,'Q7b_truth':8}))
