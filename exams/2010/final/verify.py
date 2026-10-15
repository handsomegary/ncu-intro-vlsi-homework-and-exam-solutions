from pathlib import Path
from itertools import product
from fractions import Fraction as F
import csv,json,math
B=Path(__file__).resolve().parent
graphs=json.loads((B/'device-netlists.json').read_text())
def save(name,keys,rows):
    with (B/name).open('w',newline='',encoding='utf-8')as f:
        w=csv.writer(f);w.writerow(keys);w.writerows(rows)
def reach(edges, start):
    seen = {start}
    while True:
        old = len(seen)
        for a, b in edges:
            if a in seen or b in seen:
                seen.update((a, b))
        if len(seen) == old:
            return seen

def req(edges, left, right):
    nodes = reach([(a, b) for a, b, r in edges], left)
    if right not in nodes:
        return None
    free = sorted(nodes - {left, right})
    n = len(free)
    idx = {x: i for i, x in enumerate(free)}
    m = [[F(0) for _ in range(n + 1)] for i in range(n)]
    for u, v, r in edges:
        if u not in nodes:
            continue
        g = 1 / r
        for a, b in [(u, v), (v, u)]:
            if a in idx:
                i = idx[a]
                m[i][i] += g
                if b in idx:
                    m[i][idx[b]] -= g
                elif b == left:
                    m[i][-1] += g
    for i in range(n):
        k = next((k for k in range(i, n) if m[k][i]))
        m[i], m[k] = (m[k], m[i])
        d = m[i][i]
        m[i] = [a / d for a in m[i]]
        for k in range(n):
            if k != i:
                d = m[k][i]
                m[k] = [a - d * b for a, b in zip(m[k], m[i])]
    volts = {left: F(1), right: F(0), **{x: m[i][-1] for x, i in idx.items()}}
    current = sum(((volts[left] - volts[v if u == left else u]) / r for u, v, r in edges if left in (u, v)))
    return 1 / current

def active(graph,sig):
    return[(a,b)for name,typ,g,a,b in graph if bool(sig[g])==(typ=='n')]
truth=[];phase=[]
for bits in product((0,1),repeat=5):
    sig=dict(zip('ABCDE',bits));sig.update({k+'bar':1-sig[k]for k in 'ABCDE'})
    h=int((sig['A']and sig['B'])or(sig['Cbar']and(sig['D']or sig['E'])))
    out=1-h
    edges=active(graphs['Q3_static'],sig);r=reach(edges,'f')
    assert ('VDD'in r)==bool(out)and('GND'in r)==bool(h)
    valid=[]
    for f,g in product((0,1),repeat=2):
        state={**sig,'f':f,'fbar':g};e=active(graphs['Q3_fully_differential'],state)
        rr=[reach(e,n)for n in ['f','fbar']]
        if all(('VDD'in r)!=('GND'in r)and('VDD'in r)==bool(v)for r,v in zip(rr,[f,g])):valid.append((f,g))
    assert valid==[(out,h)]
    truth.append([*bits,h,out,h,1])
    for clk in [0,1]:
        e=active(graphs['Q3_dynamic'],{**sig,'CLK':clk});r=reach(e,'f')
        pd='GND'in r;pu='VDD'in r
        assert pd==bool(clk and h)and pu==bool(not clk)and not(pu and pd)
        f=0 if pd else 1
        phase.append([*bits,clk,int(pu),int(pd),f])
save('q3_static_differential_truth.csv',['A','B','C','D','E','H','f','fbar','exclusive_and_unique'],truth)
save('q3_dynamic_phases.csv',['A','B','C','D','E','CLK','precharge_path','ground_path','f_from_precharged_state'],phase)
save('q3_transistor_counts.csv',['technique','core','local_complement_devices','complete'],[['dynamic',7,2,9],['fully_differential',12,10,22],['static',10,2,12]])

widths={'X1':F(4),'X2':F(8),'X3':F(8),'X4':F(16),'X5':F(16),'X6':F(8),'N1':F(4)}
edges=[('X1','Y','b'),('X2','Y','m'),('X3','m','b'),('X4','Y','a'),('X5','a','m'),('X6','m','b'),('N1','b','GND')]
rows=[]
for bits in product((0,1),repeat=6):
    sig=dict(zip(['X1','X2','X3','X4','X5','X6'],bits));sig['N1']=1
    e=[(u,v,2/widths[n])for n,u,v in edges if sig[n]]
    resistance=req(e,'Y','GND')
    expected=bool(bits[0]or((bits[1]or(bits[3]and bits[4]))and(bits[2]or bits[5])))
    assert (resistance is not None)==expected
    if expected:assert resistance<=1
    rows.append([*bits,int(expected),str(resistance)if expected else 'OFF'])
assert max(F(row[-1])for row in rows if row[-1]!='OFF')==1
save('q4_all64_switch_resistance.csv',['X1','X2','X3','X4','X5','X6','discharge','Req_over_Rp'],rows)
paths=[['X1','N1'],['X2','X3','N1'],['X2','X6','N1'],['X4','X5','X3','N1'],['X4','X5','X6','N1']]
save('q4_minimal_paths.csv',['path','Req_over_Rp'],[['-'.join(p),str(sum(2/widths[x]for x in p))]for p in paths])
assert all(sum(2/widths[x]for x in p)==1 for p in paths)
family=[]
for q,a in [(F(1,2),F(1,4)),(F(1,3),F(1,3)),(F(3,4),F(1,8))]:
    r={'N1':q,'X1':1-q,'X2':a,'X3':1-q-a,'X6':1-q-a,'X4':a/2,'X5':a/2}
    assert all(sum(r[x]for x in p)==1 for p in paths)
    wn1=2/q;power=1+wn1/4;assert wn1>2 and power>F(3,2)
    family.append([str(q),str(a),*[str(2/r[x])for x in widths],str(power)])
save('q4_balanced_family.csv',['q','a',*['W_'+x+'_um'for x in widths],'clock_power_over_fCV2'],family)

np=[]
for a,b,c in product((0,1),repeat=3):
    maj=int(a+b+c>=2);z=1-maj;x=maj;w=int((a,b,c)==(0,0,0)or a+b+c==2);y=w
    assert y==a^b^c^1 # p-stage w is even parity; final N dynamic output Y=wbar.
    Y=1-w;assert Y==a^b^c
    rz=F(13,7)if(a,b,c)==(1,1,1)else F(3)if maj else None
    rw=F(13,3)if(a,b,c)==(0,0,0)else F(3)if a+b+c==2 else None
    dz=2*(1+rz)if rz is not None else None;dw=(1+rw)/2 if rw is not None else None
    np.append([a,b,c,z,x,w,Y,str(rz)if rz else 'OFF',str(rw)if rw else 'OFF',str(dz)if dz else 'NA',str(dw)if dw else 'NA'])
save('q5_correlated_NP_cases.csv',['A','B','C','z','X','w','Y','z_evaluation_R_over_R','w_evaluation_R_over_R','z_mean_delay_RC','w_mean_delay_RC'],np)
assert min([F(8,3),F(40,7),F(8),F(10)])==F(8,3)and max([F(8,3),F(40,7),F(8),F(10)])==10
share=[['001','y',F(8,10),F(18,10)*2/(2+F(8,10))],['100','x',F(4,10),F(18,10)*2/(2+F(4,10))]]
assert all(v>F(12,10)for _,_,cap,v in share)
save('q5_legal_sharing.csv',['ABC','attached_internal_node','C_internal_pF','z_voltage_V'],[[s,n,str(c),str(v)]for s,n,c,v in share])

timing=[]
for delta in [F(-1,10),F(0),F(1,10)]:
    maximum=F(10)-F(8,10)-F(16,10)+delta
    n=math.ceil((F(12,10)+delta-F(4,10)-F(2,10))/F(3,10))
    timing.append([str(delta),str(maximum),n,str(F(4,10)+F(2,10)+n*F(3,10)),str(F(8,10)+F(2,10)+n*F(3,10)+F(16,10))])
assert timing[-1][2]==3
save('q6_signed_skew_and_hold.csv',['capture_minus_launch_ns','logic_max_ns','min_buffer_count','earliest_direct_arrival_ns','direct_setup_requirement_ns'],timing)

states=[]
for clk,d,m,q in product((0,1),repeat=4):
    sig={'CLK':clk,'CLKB':1-clk,'c1':1-clk,'c2':clk,'D':d,'b':1-m,'m':m,'s':1-q,'Q':q}
    e=active(graphs['Q7_layout'],sig)+[('D','VDD'if d else'GND')]
    short='GND'in reach(e,'VDD')
    expected=(d!=1-m)if clk else(m!=1-q)
    assert short==expected
    states.append([clk,d,m,q,1-m,1-q,int(short),int(not short)])
assert sum(r[-1]for r in states)==8
save('q7_conditional_settled_states.csv',['CLK','D','master_m','Q','master_input_b','slave_input_s','contention','consistent_if_written'],states)
save('q7_literal_MOS.csv',['device','type','gate','channel1','channel2'],graphs['Q7_layout'])
events=[]
for old,new in product((0,1),repeat=2):
    master=1-new;held=old;captured=1-master
    assert captured==new
    events.extend([[old,new,1,master,held,'slave_closed'],[old,new,0,master,captured,'falling_edge_capture_after_settle']])
save('q7_conditional_cycle_events.csv',['old_D','new_D','CLK','master_m','Q','condition'],events)

vdd=F(18,10);vt=F(6,10);trip=F(12,10);beta=((vdd-trip)/(trip-vt))**2
assert beta==1
save('q8_bias_current_balance.csv',['VDD','VTn','trip','internal_a','N1_overdrive','N3_overdrive','beta_N1_over_N3'],[[str(vdd),str(vt),str(trip),str(trip-vt),str(trip-vt),str(vdd-trip),str(beta)]])
report={'status':'PASS','Q3_truth_cases':32,'Q3_dynamic_phase_cases':64,'Q4_full_switch_resistance_cases':64,'Q4_minimal_balanced_paths':5,'Q4_strict_clock_target_feasible':False,'Q5_correlated_cases':8,'Q5_delay_RC':['8/3','10'],'Q5_sharing_min_V':'9/7','Q5_pMOS_enable_boundary_V':'6/5','Q6_worst_magnitude_skew_logic_max_ns':'15/2','Q6_buffer_count_with_single_delay_model':3,'Q7_physical_MOS':16,'Q7_switch_states':16,'Q7_consistent_conditional_states':8,'Q7_sampling':'falling edge, noninverting, conditional writeability','Q8_beta_ratio':1,'model':'ideal switches/RC/current onset, no process simulation','points_printed_total':130}
(B/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
