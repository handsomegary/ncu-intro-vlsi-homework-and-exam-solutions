"""Independent source-derived Boolean/ratioed-latch checks. No SPICE model."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import csv,json
OUT=Path(__file__).resolve().parent
def save(name,rows):
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
FIELDS=['device','type','gate','left','right']
def net(name,devices):save(name,[dict(zip(FIELDS,d)) for d in devices])
def connect(devices,values,start,end):
 graph={}
 for name,kind,gate,a,b in devices:
  if values[gate]==(0 if kind=='p' else 1):
   graph.setdefault(a,set()).add(b);graph.setdefault(b,set()).add(a)
 seen=set();todo=[start]
 while todo:
  n=todo.pop()
  if n==end:return True
  if n not in seen:seen.add(n);todo.extend(graph.get(n,set())-seen)
 return False

q1=[('PC','p','CLK','VDD','CLKB'),('NC','n','CLK','CLKB','GND'),
 ('P1','p','D','VDD','dbar'),('N1','n','D','dbar','GND'),
 ('PT','p','CLKB','dbar','s'),('NT','n','CLK','dbar','s'),
 ('PF','p','s','VDD','Q'),('NF','n','s','Q','GND'),
 ('P2','p','Q','VDD','s'),('N2','n','Q','s','GND')]
net('q1_latch_netlist.csv',q1)
rows=[]
for rp1,rn1,rtg,rp2,rn2 in product([F(1),F(2)],[F(1),F(2)],[F(1,2),F(1)],[F(2),F(4),F(8)],[F(2),F(4),F(8)]):
 vlo=(rn1+rtg)/(rp2+rn1+rtg);vhi=rn2/(rp1+rtg+rn2)
 assert (vlo<F(1,2))==(rp2>rn1+rtg)
 assert (vhi>F(1,2))==(rn2>rp1+rtg)
 rows.append({'normalized_RP1':str(rp1),'normalized_RN1':str(rn1),'normalized_RTG':str(rtg),'normalized_RP2':str(rp2),'normalized_RN2':str(rn2),'write1_s_over_VDD':str(vlo),'write0_s_over_VDD':str(vhi),'writes1':vlo<F(1,2),'writes0':vhi>F(1,2)})
save('q1_divider_cases.csv',rows)

q2=[('P1','p','I','VDD','A'),('Nclock1','n','phi','A','u1'),('N1','n','I','u1','GND'),
 ('P2','p','A','VDD','B'),('Nclock2','n','phi','B','u2'),('N2','n','A','u2','GND'),
 ('P3','p','B','VDD','u3'),('Pclock3','p','phi','u3','C'),('N3','n','B','C','GND'),
 ('P4','p','C','VDD','u4'),('Pclock4','p','phi','u4','O'),('N4','n','C','O','GND')]
net('q2_dynamic_register_netlist.csv',q2)
rows=[]
for oldsample,current,low_input in product((0,1),repeat=3):
 # Completed low phase: O=oldsample, C=complement. High evaluates A/B.
 a=1-current;b=current;c=0 if b else 1-oldsample;o=0 if c else oldsample
 assert o==oldsample
 high_values={'phi':1,'I':current,'A':a,'B':b,'C':c,'VDD':1,'GND':0}
 assert connect(q2,high_values,'A','VDD')==bool(a)
 assert connect(q2,high_values,'A','GND')==bool(1-a)
 assert connect(q2,high_values,'B','VDD')==bool(b)
 assert connect(q2,high_values,'B','GND')==bool(1-b)
 # Falling edge lets C/O invert twice; A can only rise during low.
 edge_o=current;edge_c=1-current;low_a=1 if not low_input else a
 low_b=1 if not low_a else b
 assert low_b==current
 low_c=1-low_b;low_o=1-low_c
 assert low_o==current
 low_values={'phi':0,'I':low_input,'A':low_a,'B':low_b,'C':low_c,'VDD':1,'GND':0}
 assert connect(q2,low_values,'C','VDD')==bool(low_c)
 assert connect(q2,low_values,'C','GND')==bool(1-low_c)
 assert connect(q2,low_values,'O','VDD')==bool(low_o)
 assert connect(q2,low_values,'O','GND')==bool(1-low_o)
 rows.append({'previous_sample':oldsample,'input_before_falling_edge':current,'input_after_edge_during_low':low_input,'high_A':a,'high_B':b,'high_C':c,'high_O_held':o,'after_falling_O':edge_o,'low_A':low_a,'low_B_held':low_b,'low_C':low_c,'low_O_held':low_o})
save('q2_phase_histories.csv',rows)

# Complete static replacement uses the source Figure-1 cell twice.
stat=[]
for prefix,mapping in [('M',{'CLK':'phi','CLKB':'phib','D':'I','Q':'M'}),('S',{'CLK':'phib','CLKB':'phi_slave','D':'M','Q':'O'})]:
 def mapped(n):
  if n in ('VDD','GND'):return n
  return mapping.get(n,prefix+'_'+n)
 for name,kind,g,a,b in q1:stat.append((prefix+name,kind,mapped(g),mapped(a),mapped(b)))
assert len(stat)==20
net('q2_static_replacement_netlist.csv',stat)

q4=[('Ppre','p','phi','VDD','z'),('NA1','n','A','z','x'),('NB1','n','B','x','nf'),('NC','n','C','z','y'),('NA2','n','A','y','nf'),('NB2','n','B','y','nf'),('Nfooter','n','phi','nf','GND'),
 ('PX','p','z','VDD','X'),('NX','n','z','X','GND'),
 ('Pheader','p','phib','VDD','pu'),('PA1','p','A','pu','pv'),('PB1','p','B','pu','pv'),('PC1','p','C','pu','pv'),('Pz','p','z','pv','w'),('PA2','p','A','pv','r1'),('PB2','p','B','r1','r2'),('PC2','p','C','r2','w'),('Nreset','n','phib','w','GND'),('PY','p','w','VDD','Y'),('NY','n','w','Y','GND')]
net('q4_np_netlist.csv',q4)
rows=[]
for a,b,c in product((0,1),repeat=3):
 m=int(a*b+a*c+b*c>0);s=a^b^c;z=1-m;w=1-s
 values={'A':a,'B':b,'C':c,'z':z,'w':w,'phi':1,'phib':0,'VDD':1,'GND':0}
 assert connect(q4,values,'z','GND')==bool(m)
 assert connect(q4,values,'w','VDD')==bool(w)
 assert connect(q4,values,'X','VDD')==bool(m)
 assert connect(q4,values,'Y','VDD')==bool(s)
 sd=(not a and not b and c) or (not a and b and not c) or (a and not b and not c) or (a and b and c)
 assert bool(s)==sd
 pre={'A':a,'B':b,'C':c,'z':1,'w':0,'phi':0,'phib':1,'VDD':1,'GND':0}
 assert connect(q4,pre,'z','VDD') and not connect(q4,pre,'z','GND')
 assert connect(q4,pre,'w','GND') and not connect(q4,pre,'w','VDD')
 assert connect(q4,pre,'X','GND') and connect(q4,pre,'Y','VDD')
 rows.append({'ABC':f'{a}{b}{c}','pre_z':1,'pre_X':0,'pre_w':0,'pre_Y':1,'eval_z':z,'eval_X_carry':m,'eval_w':w,'eval_Y_sum':s,'domino_carry_after_eval':m,'domino_sum_after_eval':s})
save('q4_phase_truth.csv',rows)

def domino(terms,output,prefix):
 dyn=prefix+'z';foot=prefix+'foot';ds=[(prefix+'Ppre','p','phi','VDD',dyn),(prefix+'Nfoot','n','phi',foot,'GND'),(prefix+'Pout','p',dyn,'VDD',output),(prefix+'Nout','n',dyn,output,'GND')]
 for i,term in enumerate(terms):
  ends=[dyn]+[f'{prefix}b{i}n{j}' for j in range(len(term)-1)]+[foot]
  for j,g in enumerate(term):ds.append((f'{prefix}N{i}{j}','n',g,ends[j],ends[j+1]))
 return ds,dyn
mc,zm=domino([['A','B'],['A','C'],['B','C']],'X','M')
sc,zs=domino([['Abar','Bbar','C'],['Abar','B','Cbar'],['A','Bbar','Cbar'],['A','B','C']],'Y','S')
comp=[(p+g+'bar',p.lower(),g,'VDD' if p=='P' else g+'bar',g+'bar' if p=='P' else 'GND') for g in 'ABC' for p in ('P','N')]
assert len(mc)==10 and len(sc)==16 and len(comp)==6
net('q4_domino_complete_netlist.csv',mc+sc+comp)
for a,b,c in product((0,1),repeat=3):
 values={'A':a,'B':b,'C':c,'Abar':1-a,'Bbar':1-b,'Cbar':1-c,'phi':1,zm:int(not(a*b+a*c+b*c)),zs:1-(a^b^c)}
 assert connect(mc,values,zm,'GND')==bool(a*b+a*c+b*c)
 assert connect(sc,values,zs,'GND')==bool(a^b^c)
 pre=dict(values,phi=0);pre[zm]=1;pre[zs]=1
 assert connect(mc,pre,zm,'VDD') and not connect(mc,pre,zm,'GND')
 assert connect(sc,pre,zs,'VDD') and not connect(sc,pre,zs,'GND')
 assert connect(mc,pre,'X','GND') and connect(sc,pre,'Y','GND')

q6=[('PA','p','A','VDD','v'),('PB','p','B','v','w'),('PC','p','C','w','F'),('PD','p','D','w','v'),('NA','n','A','GND','F'),('NB','n','B','F','u'),('NC','n','C','F','GND'),('ND','n','D','GND','u')]
net('q6_literal_netlist.csv',q6)
rows=[]
for a,b,c,d in product((0,1),repeat=4):
 values=dict(zip('ABCD',(a,b,c,d)));values.update(VDD=1,GND=0)
 up=connect(q6,values,'F','VDD');down=connect(q6,values,'F','GND');expected=not(a or c or(b and d))
 assert up==expected and down==(not expected)
 rows.append({'ABCD':f'{a}{b}{c}{d}','PUN_to_VDD':up,'PDN_to_GND':down,'F':int(expected),'no_DC_contention':not(up and down)})
save('q6_switch_truth.csv',rows)
report={'all_checks_passed':True,'Q1':{'physical_MOS':10,'latch':'positive-level noninverting','write1':'RP2 > RN1+RTG','write0':'RN2 > RP1+RTG','divider_checks':len(list(product([1,2],[1,2],[.5,1],[2,4,8],[2,4,8]))),'scope':'normalized algebra samples, no process resistance assigned'},'Q2':{'physical_MOS':12,'register':'negative-edge noninverting dynamic','phase_histories':8,'static_replacement':'positive-level master +negative-level slave, complete Q1 latch cells'},'Q4':{'physical_MOS':20,'X':'AB+AC+BC carry','Y':'A XOR B XOR C sum','phase_truth_rows':8,'source_outputs':'static output inverters','domino_design':'carry SOP6 data nMOS +pre/footer+CMOS INV=10; sum SOP12 data nMOS +pre/footer+CMOS INV=16;3 complement INV=6, total32'},'Q6':{'physical_MOS':8,'function':'NOT(A+C+B*D)','literal_PUN':'A-series-(B parallel D)-series-C','literal_PDN':'A parallel C parallel (B-series-D)','truth_rows':16},'scope':'ideal switch graphs, phase histories and linear ON-resistor divider; no transistor simulation'}
(OUT/'register-layout-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'all_checks_passed':True,'Q2_phase_histories':8,'Q4_truth':8,'Q6_truth':16}))
