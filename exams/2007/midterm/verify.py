"""Independent switch graphs, weighted probability and analog-model checks."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import csv,json,math

B=Path(__file__).resolve().parent
def save(name,keys,rows):
    with (B/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(keys);w.writerows(rows)
def reach(edges,start):
    seen={start}
    while True:
        old=len(seen)
        for a,b in edges:
            if a in seen or b in seen:seen.update((a,b))
        if len(seen)==old:return seen
def req(edges,left,right):
    nodes=reach([(a,b) for a,b,r in edges],left)
    if right not in nodes:return None
    free=sorted(nodes-{left,right});n=len(free);idx={x:i for i,x in enumerate(free)}
    m=[[F(0) for _ in range(n+1)] for i in range(n)]
    for u,v,r in edges:
        if u not in nodes:continue
        g=1/r
        for a,b in [(u,v),(v,u)]:
            if a in idx:
                i=idx[a];m[i][i]+=g
                if b in idx:m[i][idx[b]]-=g
                elif b==left:m[i][-1]+=g
    for i in range(n):
        k=next(k for k in range(i,n) if m[k][i]);m[i],m[k]=m[k],m[i]
        d=m[i][i];m[i]=[a/d for a in m[i]]
        for k in range(n):
            if k!=i:
                d=m[k][i];m[k]=[a-d*b for a,b in zip(m[k],m[i])]
    volts={left:F(1),right:F(0),**{x:m[i][-1] for x,i in idx.items()}}
    current=sum((volts[left]-volts[v if u==left else u])/r for u,v,r in edges if left in (u,v))
    return 1/current

q1=[]
for a,b,c in product((0,1),repeat=3):
    ns=[(u,v) for g,on,u,v in [('a',a,'F','t'),('b',b,'t','GND'),('c',c,'t','GND')] if on]
    ps=[(u,v) for g,on,u,v in [('a',not a,'VDD','F'),('b',not b,'VDD','p'),('c',not c,'p','F')] if on]
    pu='VDD' in reach(ps,'F');pd='GND' in reach(ns,'F')
    assert pu!=pd and pu==bool(not(a and (b or c)))
    q1.append([a,b,c,int(pu),int(pd),int(pu)])
save('q1_aoi21_truth.csv',['a','b','c','pullup','pulldown','F'],q1)

# Build the 14 physical NMOS binary tree. Gate complements are full-rail inputs.
mux=[]
for i in range(4):
    mux.extend([(f'M{i*2}','D'+str(i*2),'m'+str(i),'S0bar'),(f'M{i*2+1}','D'+str(i*2+1),'m'+str(i),'S0')])
for i in range(2):
    mux.extend([(f'M{8+i*2}','m'+str(i*2),'n'+str(i),'S1bar'),(f'M{9+i*2}','m'+str(i*2+1),'n'+str(i),'S1')])
mux.extend([('M12','n0','Y','S2bar'),('M13','n1','Y','S2')])
save('q2_mux_netlist.csv',['device','left_channel','right_channel','gate'],mux)
cases=[]
for word in range(256):
    for s2,s1,s0 in product((0,1),repeat=3):
        gates={'S0':s0,'S1':s1,'S2':s2,'S0bar':1-s0,'S1bar':1-s1,'S2bar':1-s2}
        nodes=reach([(u,v) for dev,u,v,g in mux if gates[g]],'Y')
        selected=4*s2+2*s1+s0;data=[i for i in range(8) if 'D'+str(i) in nodes]
        assert data==[selected]
        out=(word>>selected)&1
        cases.append([word,s2,s1,s0,selected,out])
save('q2_mux_cases.csv',['data_word','S2','S1','S0','selected','Y'],cases)
xor=[]
for a,b in product((0,1),repeat=2):
    selected=b if a==0 else 1-b;assert selected==a^b;xor.append([a,b,selected])
save('q2_TG_xor.csv',['A','B','Y'],xor)

probs=[F(0)]*3
for u,v,w,t in product((0,1),repeat=4):
    pr=math.prod(F(1,5) if bit else F(4,5) for bit in (u,v,w,t))
    A=u or v;Bv=A and w;Cv=Bv and t
    for j,bit in enumerate((A,Bv,Cv)):
        if bit:probs[j]+=pr
assert probs==[F(9,25),F(9,125),F(9,625)]
probrows=[[name,str(p),str(p*(1-p)),float(p),float(p*(1-p))] for name,p in zip('ABC',probs)]
save('q3_independent_sample_probability.csv',['node','p1_exact','activity_exact','p1','activity'],probrows)

coupling=5e-14*(1e-4*100e-4)/1e-4;noise=1.8*coupling/(coupling+1e-15)
assert math.isclose(coupling,.5e-15) and math.isclose(noise,.6)
save('q4_crosstalk.csv',['Cc_fF','victim_Cground_fF','aggressor_step_V','victim_noise_V'],[[coupling*1e15,1,1.8,noise]])
trans=[]
for chain,p,n in [('a',[1,2,4,6],[1,2,4,6]),('b',[1,1,4,6],[1,2,2,6])]:
    for i in range(4):
        cl=(p[i+1]+n[i+1]) if i<3 else 16
        tr=F(2*cl,p[i]);tf=F(cl,n[i]);bn=n[i];bp=p[i]/2
        be=bn*bp/(math.sqrt(bn)+math.sqrt(bp))**2
        trans.append([chain,i+1,p[i],n[i],cl,str(tr),str(tf),float(tr),float(tf),be])
save('q5_literal_width_transition_times.csv',['chain','stage','p_width','n_width','Cout_over_Cg','tr_exact','tf_exact','tr','tf','beta_effective_over_beta0'],trans)
q=3-2*math.sqrt(2);sa=126*q;sb=9.5+72*q
assert sb>sa and math.isclose(sb-sa,9.5-54*q)
save('q5_declared_overlap_comparison.csv',['chain','downstream_S_over_beta0RCg'],[['a',sa],['b',sb]])

positions=[]
for x in range(101):positions.append([x,.13/50**2*(x*x+(100-x)**2)+.2])
assert min(positions,key=lambda v:v[1])[0]==50 and math.isclose(positions[50][1],.46)
save('q6_repeater_position_sweep.csv',['position_um','total_delay_ps'],positions)

pn=[('PA','A','VDD','pA',F(1,3)),('PB','B','pA','F',F(2,3)),('PC','C','pA','pC',F(1,3)),('PD','D','pC','F',F(1,3))]
nn=[('NA','A','F','GND',F(1)),('NB','B','F','nB',F(1,2)),('NC','C','nB','GND',F(1,2)),('ND','D','nB','GND',F(1,2))]
save('q7_sized_MOS_netlist.csv',['device','type','gate','left','right','width_lambda','length_lambda','R_over_reference'],[[dev,'p',g,u,v,10/r,2,str(r)] for dev,g,u,v,r in pn]+[[dev,'n',g,u,v,4/r,2,str(r)] for dev,g,u,v,r in nn])
q7=[]
for bits in product((0,1),repeat=4):
    sig=dict(zip('ABCD',bits));pedge=[(u,v,r) for dev,g,u,v,r in pn if not sig[g]];nedge=[(u,v,r) for dev,g,u,v,r in nn if sig[g]]
    rp=req(pedge,'VDD','F');rn=req(nedge,'F','GND');out=int(not(bits[0] or (bits[1] and (bits[2] or bits[3]))))
    assert (rp is not None)==bool(out) and (rn is not None)==bool(not out)
    assert (rp if out else rn)<=1
    q7.append([*bits,out,str(rp) if rp is not None else 'OFF',str(rn) if rn is not None else 'OFF'])
assert max(F(row[-2]) for row in q7 if row[-2]!='OFF')==1 and max(F(row[-1]) for row in q7 if row[-1]!='OFF')==1
save('q7_full_switch_graph.csv',['A','B','C','D','F','Req_p_over_Rp0','Req_n_over_Rn0'],q7)
report={'status':'PASS','q1_inputs':8,'q2_mux_data_select_cases':len(cases),'q2_xor_inputs':4,'q3_occupancy_independent_inputs':probs==[F(9,25),F(9,125),F(9,625)],'q3_activity_requires_extra_temporal_assumption':True,'q4_noise_V':noise,'q5_model':'Literal widths, inverse-width RC slews, square-law overlap current approximation; finite-load physical power not asserted','q5_downstream_S_a':sa,'q5_downstream_S_b':sb,'q5_b_minus_a':sb-sa,'q6_wire_ps':.52,'q6_buffered_min_ps':positions[50][1],'q7_full_graph_cases':len(q7),'q7_fixed_channel_length_lambda':2,'q7_worst_p_and_n_relative_resistance':1,'printed_total_percent':110}
(B/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
