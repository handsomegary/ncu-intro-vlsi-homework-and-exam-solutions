from pathlib import Path
from fractions import Fraction as F
from itertools import product
import csv
import json

OUT=Path(__file__).resolve().parent

def save_csv(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

NDEV=[('A','z','x'),('B','x','foot'),('C','z','y'),
      ('A','y','foot'),('B','y','foot'),('phi','foot','GND')]

def component(bits):
    a,b,c=bits; values={'A':a,'B':b,'C':c,'phi':1}; edges=[]; graph={}
    for gate,left,right in NDEV:
        if values[gate]:
            edges.append((left,right)); graph.setdefault(left,set()).add(right); graph.setdefault(right,set()).add(left)
    seen=set(); todo=['z']
    while todo:
        n=todo.pop()
        if n not in seen:
            seen.add(n); todo.extend(graph.get(n,set())-seen)
    return seen,edges

def n_resistance(bits):
    seen,edges=component(bits)
    if 'GND' not in seen: return None
    nodes=sorted(seen-{'GND'}); index={n:i for i,n in enumerate(nodes)}; size=len(nodes)
    m=[[F(0) for _ in range(size+1)] for _ in range(size)]; m[index['z']][-1]=1
    for left,right in edges:
        if left not in seen: continue
        if left!='GND': m[index[left]][index[left]]+=1
        if right!='GND': m[index[right]][index[right]]+=1
        if left!='GND' and right!='GND':
            m[index[left]][index[right]]-=1; m[index[right]][index[left]]-=1
    for col in range(size):
        pivot=next(i for i in range(col,size) if m[i][col]); m[col],m[pivot]=m[pivot],m[col]
        denom=m[col][col]; m[col]=[x/denom for x in m[col]]
        for i in range(size):
            if i!=col:
                coeff=m[i][col]; m[i]=[a-coeff*b for a,b in zip(m[i],m[col])]
    return m[index['z']][-1]

def p_resistance(bits,z):
    low_count=3-sum(bits)
    if low_count==0: return None
    conductance=F(int(z==0)) + (F(1,3) if sum(bits)==0 else F(0))
    if not conductance: return None
    return F(1)+F(1,low_count)+1/conductance

nrows=[]; prows=[]; complete=[]; sharing=[]
all_x=[]; all_y=[]
for bits in product((0,1),repeat=3):
    bitstring=''.join(map(str,bits)); majority=int(sum(bits)>=2); z=1-majority
    rn=n_resistance(bits)
    assert (rn is not None)==bool(majority)
    td_z=None if rn is None else (4+4*rn)/2
    if td_z is not None: all_x.append(td_z)
    nrows.append({'ABC':bitstring,'majority':majority,'stable_z':z,
                  'evaluation_Rz_over_R':'' if rn is None else str(rn),
                  'precharge_tr_over_RC':4,'evaluation_tf_over_RC':'' if rn is None else str(4*rn),
                  'average_td_over_RC':'' if td_z is None else str(td_z)})
    for candidate_z in (0,1):
        rp=p_resistance(bits,candidate_z)
        td_w=None if rp is None else (rp+1)/2
        prows.append({'ABC':bitstring,'candidate_z':candidate_z,'stable_z_consistent':candidate_z==z,
                      'w_pullup_R_over_R':'' if rp is None else str(rp),
                      'w_reset_tf_over_RC':1,'w_average_td_over_RC':'' if td_w is None else str(td_w)})
    rw=p_resistance(bits,z); w=int(rw is not None); y=1-w
    assert y==(sum(bits)%2)
    td_y=None
    if w:
        td_w=(rw+1)/2
        td_y=td_w+(td_z if majority else F(0))
        all_y.append(td_y)
    complete.append({'ABC':bitstring,'stable_z':z,'X':majority,'w':w,'Y':y,
                     'X_mean_delay_over_RC':'' if td_z is None else str(td_z),
                     'Y_mean_delay_over_RC':'' if td_y is None else str(td_y),
                     'Y_route':'no evaluation output transition' if not w else 'z -> w -> Y' if majority else 'primary ABC bypass -> w -> Y'})
    seen,edges=component(bits)
    if 'GND' in seen:
        sharing.append({'ABC':bitstring,'floating_connected_nodes':'not floating: connected to GND',
                        'initial_high_charge_pF_V':'','pooled_cap_pF':'','shared_z_V':'','false_p_trigger':''})
    else:
        cap=sum({'z':F(8,5),'x':F(2,5),'y':F(4,5)}.get(n,F(0)) for n in seen)
        voltage=F(8,5)*F(9,5)/cap
        sharing.append({'ABC':bitstring,'floating_connected_nodes':','.join(sorted(seen)),
                        'initial_high_charge_pF_V':str(F(72,25)),'pooled_cap_pF':str(cap),
                        'shared_z_V':float(voltage),'false_p_trigger':voltage<F(13,10)})
assert min(all_x)==F(40,7) and max(all_x)==8
assert min(all_y)==F(8,3) and max(all_y)==10
assert next(r for r in sharing if r['ABC']=='001')['shared_z_V']==1.2
assert next(r for r in sharing if r['ABC']=='100')['shared_z_V']==1.44
assert all(not('x' in r['floating_connected_nodes'] and 'y' in r['floating_connected_nodes']) for r in sharing)
save_csv('q5_n_stage.csv',nrows); save_csv('q5_p_stage_independent_z.csv',prows)
save_csv('q5_reachable_paths.csv',complete); save_csv('q5_sharing_cases.csv',sharing)
all_p_t=[F(r['w_average_td_over_RC']) for r in prows if r['w_average_td_over_RC']!='']
report={'stable_functions':{'z':'NOT majority(A,B,C)','X':'majority(A,B,C)','w':'NOT XOR3(A,B,C)','Y':'XOR3(A,B,C)'},
        'loads':{'z_in_C':4,'w_in_C':1,'X_output_in_C':0,'Y_output_in_C':0},
        'source_average_convention':{'X_tcd_over_RC':str(min(all_x)),'X_tpd_over_RC':str(max(all_x)),
                                    'Y_tcd_over_RC':str(min(all_y)),'Y_tpd_over_RC':str(max(all_y)),
                                    'whole_tcd_over_RC':str(min(all_x+all_y)),
                                    'whole_tpd_over_RC':str(max(all_x+all_y))},
        'independent_stage_envelope':{'w_tcd_over_RC':str(min(all_p_t)),'w_tpd_over_RC':str(max(all_p_t)),
                                      'sum_min_not_jointly_reachable':str(min(all_x)+min(all_p_t)),
                                      'sum_max_not_jointly_reachable':str(max(all_x)+max(all_p_t))},
        'charge_sharing_counterexample':{'ABC':'001','initial_y_V':0,'initial_z_V':1.8,
                                         'connected_caps_pF':[1.6,0.8],'shared_z_V':1.2,'p_turnon_threshold_V':1.3},
        'scope':'Exact linear ON-resistance / source average-delay convention. No external X/Y load is drawn and drain caps are neglected. Initial internal node voltages must be stated for sharing.'}
(OUT/'q5-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
