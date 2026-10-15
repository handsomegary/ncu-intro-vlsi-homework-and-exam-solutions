"""Source-derived analytical checks: 2012 final Q3/Q4/Q6. No SPICE claim."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import csv
import json

OUT = Path(__file__).resolve().parent

def save_csv(name, rows):
    with (OUT / name).open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# Q3: gate widths, strengths, node loads, and preceding-driver output slews.
q3=[]
for i, scale in enumerate((1,2,4,8)):
    input_slew = F(2) if i == 0 else F(6)
    load = 6*scale if i < 3 else 'CL/Cg'
    q3.append({'stage':i+1,'Wn_over_W':scale,'Wp_over_W':2*scale,
               'beta_over_beta0':scale,'input_gate_cap_over_Cg':3*scale,
               'output_load_over_Cg':load,'input_slew_over_tau0':float(input_slew),
               'SC_coefficient':float(scale*input_slew)})
assert sum(r['SC_coefficient'] for r in q3)==86
assert sum(r['output_load_over_Cg'] for r in q3[:3])==42
save_csv('q3_stage_table.csv',q3)

# Q4: linear ON resistance normalized to fixed P1 resistance.
# Rn(W_um)/Rp1 = 2/W_um; fixed P1 is 4 um and mu_n=2 mu_p.
PDN=[('X1','Y','F'),('X2','Y','M'),('X4','Y','T'),('X5','T','M'),
     ('X3','M','F'),('X6','M','F'),('N1','F','GND')]
PATHS=[('X1','N1'),('X2','X3','N1'),('X2','X6','N1'),
       ('X4','X5','X3','N1'),('X4','X5','X6','N1')]
schemes={
    'correct_equal_single_path':{'X1':F(8,3),'X2':F(4),'X3':F(8),'X4':F(8),'X5':F(8),'X6':F(8),'N1':F(8)},
    'correct_uniform_8':{n:F(8) for n,_,_ in PDN},
    'student_A_a':{'X1':F(4),'X2':F(6),'X3':F(6),'X4':F(8),'X5':F(8),'X6':F(8),'N1':F(8)},
    'student_B_a':{'X1':F(4),'X2':F(6),'X3':F(8),'X4':F(8),'X5':F(8),'X6':F(8),'N1':F(8)},
    'student_A_b_readable_widths':{'X1':F(4),'X2':F(6),'X3':F(6),'X4':F(9),'X5':F(9),'X6':F(9),'N1':F(6)},
    'student_B_b_footer_8':{n:F(8) for n,_,_ in PDN},
}

def effective_resistance(widths, bits):
    values={f'X{i+1}':b for i,b in enumerate(bits)}; values['N1']=1
    active=[(a,b,F(2)/widths[n]) for n,a,b in PDN if values[n]]
    graph={}
    for a,b,r in active:
        graph.setdefault(a,set()).add(b); graph.setdefault(b,set()).add(a)
    seen=set(); todo=['Y']
    while todo:
        node=todo.pop()
        if node not in seen:
            seen.add(node); todo.extend(graph.get(node,set())-seen)
    if 'GND' not in seen: return None
    nodes=sorted(seen-{'GND'}); index={n:i for i,n in enumerate(nodes)}; size=len(nodes)
    matrix=[[F(0) for _ in range(size+1)] for _ in range(size)]
    matrix[index['Y']][-1]=F(1)
    for a,b,r in active:
        if a not in seen: continue
        g=1/r
        if a!='GND': matrix[index[a]][index[a]]+=g
        if b!='GND': matrix[index[b]][index[b]]+=g
        if a!='GND' and b!='GND':
            matrix[index[a]][index[b]]-=g; matrix[index[b]][index[a]]-=g
    for col in range(size):
        pivot=next(i for i in range(col,size) if matrix[i][col])
        matrix[col],matrix[pivot]=matrix[pivot],matrix[col]
        denominator=matrix[col][col]; matrix[col]=[v/denominator for v in matrix[col]]
        for i in range(size):
            if i!=col:
                coefficient=matrix[i][col]
                matrix[i]=[a-coefficient*b for a,b in zip(matrix[i],matrix[col])]
    return matrix[index['Y']][-1]

path_rows=[]; state_rows=[]; q4_report={}
for scheme,widths in schemes.items():
    ratios=[]
    for path in PATHS:
        ratio=sum((F(2)/widths[n] for n in path),F(0)); ratios.append(ratio)
        path_rows.append({'scheme':scheme,'path':' -> '.join(path),'R_over_Rp1':float(ratio),'exact':str(ratio)})
    all_re=[]
    for bits in product((0,1),repeat=6):
        r=effective_resistance(widths,bits)
        x1,x2,x3,x4,x5,x6=bits
        function=bool(x1 or (x2 or (x4 and x5)) and (x3 or x6))
        assert (r is not None)==function
        if r is not None: all_re.append(r)
        state_rows.append({'scheme':scheme,'inputs_X1_to_X6':''.join(map(str,bits)),
                           'conducting':function,'Req_over_Rp1':'' if r is None else float(r)})
    assert max(all_re)==max(ratios)
    coefficient=1+widths['N1']/4
    q4_report[scheme]={'worst_R_over_Rp1':float(max(all_re)), 'exact_worst':str(max(all_re)),
                       'clock_power_over_fCVDD2':float(coefficient),'power_limit_pass':coefficient<F(5,4),
                       'single_paths':[str(x) for x in ratios]}
assert q4_report['correct_equal_single_path']['single_paths']==['1']*5
assert q4_report['student_A_a']['exact_worst']=='13/12'
assert q4_report['student_B_a']['exact_worst']=='1'
save_csv('q4_single_paths.csv',path_rows); save_csv('q4_switch_network.csv',state_rows)
bound_rows=[]
for wf in (F(1,10),F(1,4),F(1,2),F(3,4),F(99,100),F(1),F(3,2),F(2),F(201,100),F(4),F(6),F(8),F(100)):
    power=1+wf/4; footer_r=2/wf
    clock_pass=power<F(5,4); balance_possible=footer_r<1
    assert not(clock_pass and balance_possible)
    bound_rows.append({'footer_W_um':float(wf),'clock_coefficient':float(power),'footer_R_over_Rp1':float(footer_r),
                       'clock_under_1p25':clock_pass,'necessary_balance_condition_pass':balance_possible})
save_csv('q4_footer_bound.csv',bound_rows)

# Q6: stop at each register; never concatenate across R3/R4/R5 boundaries.
DELAYS={'INV':F(3,10),'NOR':F(7,10),'XNOR_lower':F(7,10),
        'XOR_middle':F(7,10),'XNOR_final':F(7,10)}
EDGES={'R1':['INV','XNOR_final'],'INV':['R3'],'R2':['NOR'],'R3':['NOR','R4'],
       'NOR':['R5','XNOR_lower'],'R4':['XNOR_lower'],'XNOR_lower':['XOR_middle'],
       'R5':['XOR_middle'],'XOR_middle':['XNOR_final'],'XNOR_final':['R6']}

def paths(start,node=None,route=None):
    node=start if node is None else node; route=[start] if route is None else route
    if len(route)>1 and node.startswith('R'): return [route]
    return [p for nxt in EDGES.get(node,[]) for p in paths(start,nxt,route+[nxt])]

routes=[p for r in ('R1','R2','R3','R4','R5') for p in paths(r)]
assert len(routes)==9
q6_rows=[]; q6_report={}
for case in ('ab_unspecified_wire','c_wire_0p05','c_repaired','skew_safe'):
    data=[]
    for route in routes:
        d=sum((DELAYS.get(n,F(0)) for n in route),F(0))
        if route==['R3','R4']:
            if case!='ab_unspecified_wire': d+=F(1,20)
            if case in ('c_repaired','skew_safe'): d+=F(3,5)
        if case=='skew_safe' and route==['R1','INV','R3']: d+=F(3,5)
        data.append(d); q6_rows.append({'case':case,'path':' -> '.join(route),'data_delay_ns':float(d)})
    assert max(data)==F(14,5)
    for s in (F(-1,2),F(0),F(1,2)):
        period=F(2,5)+max(data)+F(3,10)-s
        bad=[' -> '.join(p) for p,d in zip(routes,data) if F(1,10)+d<F(1,5)+s]
        q6_report[f'{case},s={float(s):+.1f}ns']={'setup_period_ns':float(period),
                    'setup_frequency_MHz':float(F(1000)/period),'hold_violations':bad,
                    'pairwise_envelope_checks_pass':not bad}
assert len(q6_report['c_wire_0p05,s=+0.0ns']['hold_violations'])==1
assert q6_report['c_repaired,s=+0.0ns']['pairwise_envelope_checks_pass']
assert len(q6_report['c_repaired,s=+0.5ns']['hold_violations'])==1
assert all(q6_report[f'skew_safe,s={s}ns']['pairwise_envelope_checks_pass'] for s in ('-0.5','+0.0','+0.5'))
save_csv('q6_paths.csv',q6_rows)

report={'Q3':{'switching_gate_load_coefficient':42,'short_circuit_coefficient':86,
               'input_slews_in_tau0':[2,6,6,6],'uses_exam_VDD_minus_Vt_not_2Vt':True},
        'Q4':q4_report,'Q4b_proof':{'clock_limit_requires_footer_W_um':'<1',
                  'finite_equal_timing_requires_footer_W_um':'>2',
                  'finite_clock_power_lower_bound_coefficient':'>1.5','feasible':False},
        'Q6':q6_report,'Q6_skew_scope':'Signs are pairwise bounds, not a uniform physical clock distribution; setup ceilings require reported hold repairs.','model_scope':'Analytical fixed gate delays and linear ON resistances. No transistor simulation.'}
(OUT/'numerical-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'all_checks_passed':True,'Q3_stages':len(q3),'Q4_single_path_checks':len(path_rows),
                  'Q4_switch_states':len(state_rows),'Q6_paths':len(routes)}))
