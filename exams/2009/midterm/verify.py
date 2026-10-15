"""Reproduce original-first switch, energy and nodal RC evidence using Python stdlib."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json,csv,math,hashlib
P=Path(__file__).resolve().parent
graphs=json.loads((P/'device-netlists.json').read_text())
def reach(edges,node):
    seen={node}
    while True:
        more={b for a,b in edges if a in seen}|{a for a,b in edges if b in seen}
        if more<=seen:return seen
        seen|=more
def active(graph,sig):
    return [(a,b) for name,typ,g,a,b in graph if bool(sig[g])==(typ=='n')]
def save(name,keys,rows):
    with (P/name).open('w',newline='',encoding='utf-8')as f:
        w=csv.writer(f);w.writerow(keys);w.writerows(rows)
def rail_check(graph,sig,out,value):
    component=reach(active(graph,sig),out)
    assert ('VDD'in component)==bool(value)and('GND'in component)==bool(1-value)
q1=[]
for bits in product((0,1),repeat=4):
    s=dict(zip(['x1','x2','x3','x4'],bits));v=int(not(bits[0]or bits[1]and bits[2]or bits[3]))
    rail_check(graphs['Q1'],s,'f',v);q1.append([*bits,v])
save('q1_full_CMOS_truth.csv',['x1','x2','x3','x4','f'],q1)
q4=[]
def signals(bits):
    s=dict(zip(['I0','I1','I2','I3','I4'],bits));s['a']=int(s['I1']or s['I2']);s['ar']=1-s['a']
    s['b']=int(not(s['I0']or s['a']));s['d']=int(not(s['a']and s['I3']))
    s['O0']=int(s['b']or s['d']or s['I4']);s['r0']=1-s['O0'];s['O1']=s['d']and s['I4'];s['r1']=1-s['O1'];return s
for bits in product((0,1),repeat=5):
    s=signals(bits)
    for o in ['ar','a','b','d','r0','O0','r1','O1']:rail_check(graphs['Q4'],s,o,s[o])
    assert s['O0']==int(not(s['I1']or s['I2'])or not s['I3']or s['I4'])
    q4.append([*bits,*[s[k]for k in ['a','b','d','O0','O1']]])
save('q4_full_CMOS_truth.csv',['I0','I1','I2','I3','I4','a','b','d','O0','O1'],q4)
seq=[signals(tuple(map(int,s)))for s in ['01001','11011','11100','01101']]
loads={'a':2,'b':1,'d':2,'O0':2,'O1':2,'ar':1,'r0':1,'r1':1}
events=[]
for i,s in enumerate(seq):
    t=seq[(i+1)%4];charges={k:c for k,c in loads.items()if s[k]==0 and t[k]==1}
    e=sum(charges.values());visible=sum(c for k,c in charges.items()if k in ['a','b','d','O0','O1'])
    events.append([i,''.join(str(s['I'+str(j)])for j in range(5)),','.join(charges),visible,e])
assert [r[-1]for r in events]==[1,2,2,0]
assert sum(r[-1]for r in events)==5 and max(r[-1]for r in events)==2
save('q4_settled_charging_events.csv',['interval','from_word','nodes_charged','visible_Ci','with_internal_Ci'],events)
gates=[['a','NOR2+INV',2,1,F(7,2)],['b','NOR2',1,0,F(3,2)],['d','NAND2',2,0,F(3)],['O0','NOR3+INV',2,1,F(4)],['O1','NAND2+INV',2,1,F(7,2)]]
save('q4_actual_load_delays.csv',['gate','implementation','external_Ci','internal_Ci','mean_units'],gates)
paths=[['a-d-O0',F(21,2)],['a-b-O0',F(9)],['a-d-O1',F(10)],['I0-b-O0',F(11,2)],['I3-d-O0',F(7)],['I3-d-O1',F(13,2)]]
assert max(x[1]for x in paths)==F(21,2)
save('q4_physical_path_delays.csv',['path','delay_units'],paths)
slack=[]
for db,do1 in [(F(0),F(0)),(F(3,2),F(1,2)),(F(2),F(0))]:
    maximum=max(F(21,2),F(9)+db,F(10)+do1)
    slack.append([str(db),str(do1),str(maximum),int(maximum<=F(21,2))])
assert [x[-1]for x in slack]==[1,1,0]
save('q4_conditional_VT_examples.csv',['b_penalty','O1_penalty','new_max','meets_original'],slack)
q=3-2*math.sqrt(2);sa=126*q;sb=9.5+72*q
assert sb>sa and math.isclose(sb-sa,9.5-54*q)
save('q3_declared_overlap_comparison.csv',['chain','downstream_strength_slew_over_beta0RCg'],[['a',sa],['b',sb],['b-a',sb-sa]])
chainrows=[]
for name,ps,ns in [('a',[1,2,4,6],[1,2,4,6]),('b',[1,1,4,6],[1,2,2,6])]:
    for i,(wp,wn)in enumerate(zip(ps,ns)):
        cap=ps[i+1]+ns[i+1]if i<3 else 16
        chainrows.append([name,i+1,wp,wn,cap,str(F(2*cap,wp)),str(F(cap,wn))])
save('q3_literal_slews.csv',['chain','stage','wp','wn','Cout_Cg','rise_RCg','fall_RCg'],chainrows)

def solve(a,b):
    a=[list(row)+[rhs]for row,rhs in zip(a,b)];n=len(b)
    for i in range(n):
        j=next(j for j in range(i,n)if a[j][i]);a[i],a[j]=a[j],a[i]
        pivot=a[i][i];a[i]=[x/pivot for x in a[i]]
        for j in range(n):
            if j!=i:
                k=a[j][i];a[j]=[x-k*y for x,y in zip(a[j],a[i])]
    return [r[-1]for r in a]
def moment(graph,sig,res,caps,root,out):
    edges=[(a,b,res[name])for name,typ,g,a,b in graph if bool(sig[g])==(typ=='n')]
    component=reach([(a,b)for a,b,r in edges],out);assert root in component
    nodes=sorted(component-{root});idx={x:i for i,x in enumerate(nodes)};n=len(nodes)
    mat=[[F(0)for _ in nodes]for _ in nodes]
    for a,b,r in edges:
        if a not in component or b not in component:continue
        g=1/r
        for u,v in [(a,b),(b,a)]:
            if u==root:continue
            mat[idx[u]][idx[u]]+=g
            if v!=root:mat[idx[u]][idx[v]]-=g
    return solve(mat,[caps.get(x,F(0))for x in nodes])[idx[out]]
truth=[];rc=[]
for bits in product((0,1),repeat=3):
    s=dict(zip('ABC',bits));v=int(sum(bits)<2);rail_check(graphs['Q6'],s,'Y',v);truth.append([*bits,v])
save('q6_literal_majority_truth.csv',['A','B','C','Y'],truth)
# Vary every named R/C independently to verify symbolic path/shared-load formulas.
for sample in range(24):
    res={name:F(1+(j*7+sample*3)%19,1+(j+sample)%5)for j,(name,*_)in enumerate(graphs['Q6'])}
    caps={node:F(1+(j*5+sample*11)%23,1+(sample+j)%4)for j,node in enumerate(['1','2','3','4','Y'])}
    p={i:res['P'+str(i)]for i in range(1,6)};n={i:res['N'+str(i)]for i in range(1,6)}
    c1,c2,c3,c4,c=[caps[x]for x in ['1','2','3','4','Y']];u=1/(1/p[1]+1/p[2])
    expected={'001':u*(c1+c2+c+c3)+p[4]*(c2+c+c3)+p[5]*(c+c3),
      '010':p[1]*(c1+c2+c+c4)+p[3]*(c+c4),'100':p[2]*(c1+c2+c)+p[3]*(c2+c),
      '011':(n[1]+n[3])*(c+c4)+n[3]*c3,'101':(n[1]+n[2])*(c+c2)+n[2]*c3,
      '110':(n[4]+n[5])*(c+c1)+n[5]*c4}
    ss=p[3]+p[4]+p[5]
    expected['000']=u*c1+(u+p[3]*p[4]/ss)*c2+(u+p[3]*(p[4]+p[5])/ss)*c
    rb=1/(1/n[2]+1/n[3]);re=1/(1/(n[1]+rb)+1/(n[4]+n[5]))
    expected['111']=re*c+re*rb/(n[1]+rb)*c3+re*n[5]/(n[4]+n[5])*c4
    assert expected['000']<=expected['001'] and expected['111']<=expected['011']
    for bits in product((0,1),repeat=3):
        s=dict(zip('ABC',bits));word=''.join(map(str,bits));root='VDD'if sum(bits)<2 else'GND'
        value=moment(graphs['Q6'],s,res,caps,root,'Y');assert value==expected[word],(sample,word,value,expected[word])
        rc.append([sample,word,root,str(value),str(expected[word]),1])
save('q6_full_nodal_moment_checks.csv',['independent_parameter_sample','ABC','active_rail','nodal_first_moment','symbolic_formula','exact_match'],rc)
save('q6_literal_MOS.csv',['device','type','gate','channel1','channel2'],graphs['Q6'])
save('q4_literal_MOS.csv',['device','type','gate','channel1','channel2'],graphs['Q4'])
report={'status':'PASS','printed_points':105,'Q1_truth_cases':16,'Q4_truth_cases':32,'Q4_physical_MOS':28,'Q4_max_settled_interval_Ci':2,'Q4_cycle_with_internal_Ci':5,'Q4_conservative_max_delay_units':'21/2','Q3_overlap_b_minus_a':sb-sa,'Q6_truth_cases':8,'Q6_nodal_moment_checks':len(rc),'Q6_model':'Elmore first moment of each final ON network, connected caps fully unsettled; no measured transient bound','limits':['Actual instantaneous/glitch power requires current/transition data','High-VT minimum leakage requires delay and leakage characterization','RC initial voltages not given']}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))
