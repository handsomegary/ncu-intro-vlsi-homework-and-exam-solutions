"""Independent analytical verification for 2009 final Q3, Q5 and Q7.

Python standard library only. The source is the native three-page final.pdf,
printed Fall 2009. Gate names A/B/C in Q3a are introduced audit names for the
three unlabelled data controls. No unprinted threshold or absolute device
parameter is assigned. Boolean MOS graphs use ideal channel switches; the
charge-sharing calculation uses source lumped Cg, Cd=Cs and initially low
internal diffusion nodes. This is not SPICE, DRC or transistor timing.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import csv
import json

OUT = Path(__file__).resolve().parent
FIELDS = ('device', 'type', 'left_channel', 'right_channel', 'gate')


def save(name, rows):
    with (OUT/name).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def net_rows(devices):
    return [dict(zip(FIELDS, device)) for device in devices]


def graph(devices, values):
    g, on = {}, []
    for name, kind, left, right, gate in devices:
        assert kind in ('p', 'n')
        assert gate in values, (name, gate)
        if values[gate] == (0 if kind == 'p' else 1):
            g.setdefault(left,set()).add(right); g.setdefault(right,set()).add(left)
            on.append(name)
    return g, on


def component(g, start):
    seen, todo = set(), [start]
    while todo:
        n = todo.pop()
        if n not in seen:
            seen.add(n); todo.extend(g.get(n,set())-seen)
    return seen


def reach(g, start, end):
    return end in component(g,start)


def rails(g, node):
    return reach(g,node,'VDD'), reach(g,node,'VSS')


def consistent(g,node,value):
    return rails(g,node)==((True,False) if value else (False,True))


def count(devices):
    c=Counter(d[1] for d in devices)
    return {'pMOS':c['p'],'nMOS':c['n'],'total':len(devices)}


Q3A = [
    ('P_pre','p','VDD','VF','Vin'),
    ('N_A','n','VF','u1','A'), ('N_B','n','u1','u2','B'),
    ('N_C','n','u2','u3','C'), ('N_footer','n','u3','VSS','Vin'),
    ('P_inv','p','VDD','out','VF'), ('N_inv','n','out','VSS','VF'),
]
save('q3a_literal_netlist.csv',net_rows(Q3A))
# Count every diffusion terminal and gate at each relevant node directly from
# the full graph, including both input gates of the output inverter at VF.
caps=[]; cap_map={}
for node in ('VF','u1','u2','u3'):
    cd_devices=[d[0] for d in Q3A for endpoint in d[2:4] if endpoint==node]
    cg_devices=[d[0] for d in Q3A if d[4]==node]
    cap_map[node]=(len(cd_devices),len(cg_devices))
    caps.append({'node':node,'Cd_or_Cs_terms':len(cd_devices),'Cg_terms':len(cg_devices),
                  'diffusion_devices':' '.join(cd_devices),'gate_devices':' '.join(cg_devices),
                  'capacitance_over_Cd':f'{len(cd_devices)}+{len(cg_devices)}*alpha'})
assert cap_map=={'VF':(2,2),'u1':(2,0),'u2':(2,0),'u3':(2,0)}
save('q3a_node_capacitances.csv',caps)
sharing_rows=[]; component_rows=[]; max_internal=0
gate_only=Q3A[:5]
for vin,a,b,c in product((0,1),repeat=4):
    values={'Vin':vin,'A':a,'B':b,'C':c}
    g,on=graph(gate_only,values); seen=component(g,'VF')
    high,low=rails(g,'VF')
    if vin==0:
        assert high and not low
        mode='precharge clamped to VDD; not isolated sharing'
    elif low:
        assert a and b and c
        mode='legitimate AND discharge to VSS; not isolated sharing'
    else:
        assert not high
        mode='isolated charge-sharing component'
        internal=seen & {'u1','u2','u3'}
        assert 'u3' not in internal
        internal_cd=sum(cap_map[n][0] for n in internal)
        max_internal=max(max_internal,internal_cd)
        for alpha in (F(0),F(1,2),F(1),F(1001,1000),F(2),F(4)):
            vf_cap=F(2)+2*alpha
            ratio=vf_cap/(vf_cap+internal_cd)
            relation='above threshold' if ratio>F(1,2) else 'at threshold' if ratio==F(1,2) else 'below threshold'
            sharing_rows.append({'A':a,'B':b,'C':c,'connected_internal_nodes':' '.join(sorted(internal)),
                                 'C_internal_over_Cd':internal_cd,'alpha_test':str(alpha),
                                 'VF_over_VDD':str(ratio),'relation_to_VDD_over_2':relation,
                                 'strict_high_valid':ratio>F(1,2)})
    component_rows.append({'Vin':vin,'A':a,'B':b,'C':c,
                           'VF_component':' '.join(sorted(seen)),'VF_to_VDD':high,'VF_to_VSS':low,'mode':mode})
assert max_internal==4
assert (F(2)+2*F(1))/(F(2)+2*F(1)+4)==F(1,2)
save('q3a_switch_components.csv',component_rows)
save('q3a_sharing_parameter_checks.csv',sharing_rows)

# Q3b: preserve the p pass transistor and add an n pass transistor controlled
# by a physically generated Cbar. This completes a TG without assuming Vtp.
Q3B = [
    ('P_existing','p','X','Y','C'), ('N_added','n','X','Y','Cbar'),
    ('P_Cbar','p','VDD','Cbar','C'), ('N_Cbar','n','Cbar','VSS','C'),
]
save('q3b_completed_TG_netlist.csv',net_rows(Q3B))
assert count(Q3B)=={'pMOS':2,'nMOS':2,'total':4}
restore=[]
for x,c in product((0,1),repeat=2):
    values={'X':x,'C':c,'Cbar':1-c,'VDD':1,'VSS':0}
    g,on=graph(Q3B,values)
    assert consistent(g,'Cbar',1-c)
    # X is driven externally at its valid rail, not by an invented transistor.
    rail='VDD' if x else 'VSS'
    g.setdefault('X',set()).add(rail); g.setdefault(rail,set()).add('X')
    if c==0:
        assert {'P_existing','N_added'}.issubset(on)
        assert reach(g,'Y','X') and consistent(g,'Y',x)
        result=str(x)
    else:
        assert not({'P_existing','N_added'} & set(on))
        assert not reach(g,'Y','X') and rails(g,'Y')==(False,False)
        result='isolated; previous capacitive state unspecified'
    restore.append({'X':x,'C':c,'Cbar':1-c,'p_pass_on':'P_existing' in on,
                    'n_pass_on':'N_added' in on,'Y_after_phase':result,
                    'full_low_path_via_nMOS':c==0 and x==0,
                    'full_high_path_via_pMOS':c==0 and x==1})
save('q3b_TG_truth.csv',restore)

# Q5: source has the same clock net at both registers, no stated skew.
FREQUENCY_MHZ=F(200); PERIOD_NS=1000/FREQUENCY_MHZ
TPCQ,TCCQ,TSETUP,THOLD=F(1,2),F(1,5),F(3,2),F(1)
MAX_DELAY=PERIOD_NS-TPCQ-TSETUP
MIN_DELAY=THOLD-TCCQ
assert PERIOD_NS==5 and MAX_DELAY==3 and MIN_DELAY==F(4,5)
timing=[]
for minimum,maximum in ((F(79,100),F(3)),(F(4,5),F(3)),(F(81,100),F(3)),
                        (F(4,5),F(301,100)),(F(4,5),F(299,100))):
    setup_slack=PERIOD_NS-(TPCQ+maximum+TSETUP)
    hold_slack=TCCQ+minimum-THOLD
    assert (setup_slack>=0)==(maximum<=MAX_DELAY)
    assert (hold_slack>=0)==(minimum>=MIN_DELAY)
    timing.append({'candidate_tcd_ns':float(minimum),'candidate_tpd_ns':float(maximum),
                   'setup_slack_ns':float(setup_slack),'hold_slack_ns':float(hold_slack),
                   'valid':minimum<=maximum and setup_slack>=0 and hold_slack>=0})
save('q5_timing_bounds.csv',timing)

# Q7: verified in native vectors: the overbar spans the WHOLE AB+C+DE.
COMPLEMENTS=[device for s in ('A','B','C','D','E') for device in (
    (f'P_{s}bar','p','VDD',s+'bar',s),(f'N_{s}bar','n',s+'bar','VSS',s))]
G_LEFT=[('NA','n','F','ab','A'),('NB','n','ab','VSS','B'),
        ('NC','n','F','VSS','C'),('ND','n','F','de','D'),('NE','n','de','VSS','E')]
F_RIGHT=[('NAbar','n','Fbar','f1','Abar'),('NBbar','n','Fbar','f1','Bbar'),
         ('NCbar','n','f1','f2','Cbar'),('NDbar','n','f2','VSS','Dbar'),('NEbar','n','f2','VSS','Ebar')]
STATIC_P=[('PA','p','VDD','p1','A'),('PB','p','VDD','p1','B'),
          ('PC','p','p1','p2','C'),('PD','p','p2','F','D'),('PE','p','p2','F','E')]
STATIC=G_LEFT+STATIC_P
DIFF_CORE=G_LEFT+F_RIGHT+[('P_F','p','VDD','F','Fbar'),('P_Fbar','p','VDD','Fbar','F')]
DOMINO_PDN=[('NAbar','n','Z','d1','Abar'),('NBbar','n','Z','d1','Bbar'),
            ('NCbar','n','d1','d2','Cbar'),('NDbar','n','d2','foot','Dbar'),('NEbar','n','d2','foot','Ebar')]
DOMINO_CORE=DOMINO_PDN+[('Ppre','p','VDD','Z','phi'),('Nfoot','n','foot','VSS','phi'),
                         ('Pout','p','VDD','F','Z'),('Nout','n','F','VSS','Z')]
assert count(STATIC)=={'pMOS':5,'nMOS':5,'total':10}
assert count(DIFF_CORE)=={'pMOS':2,'nMOS':10,'total':12}
assert count(DIFF_CORE+COMPLEMENTS)=={'pMOS':7,'nMOS':15,'total':22}
assert count(DOMINO_CORE)=={'pMOS':2,'nMOS':7,'total':9}
assert count(DOMINO_CORE+COMPLEMENTS)=={'pMOS':7,'nMOS':12,'total':19}
save('q7_static_CMOS_netlist.csv',net_rows(STATIC))
save('q7_fully_differential_complete_netlist.csv',net_rows(DIFF_CORE+COMPLEMENTS))
save('q7_domino_complete_netlist.csv',net_rows(DOMINO_CORE+COMPLEMENTS))
truth=[]; domino_phase=[]; diff_candidate=[]
for bits in product((0,1),repeat=5):
    a,b,c,d,e=bits
    g_value=int(a and b or c or d and e)
    expected_f=1-g_value
    complement_formula=int(((not a) or (not b)) and (not c) and ((not d) or (not e)))
    assert complement_formula==expected_f
    values={'VDD':1,'VSS':0,**dict(zip(('A','B','C','D','E'),bits))}
    values.update({s+'bar':1-values[s] for s in ('A','B','C','D','E')})
    static_g,_=graph(STATIC,values)
    assert rails(static_g,'F') in ((True,False),(False,True))
    assert consistent(static_g,'F',expected_f)
    comp_g,_=graph(COMPLEMENTS,values)
    assert all(consistent(comp_g,s+'bar',values[s+'bar']) for s in ('A','B','C','D','E'))
    for phi in (0,1):
        z=1 if phi==0 else 1-expected_f
        f=1-z
        gd,_=graph(DOMINO_CORE+COMPLEMENTS,{**values,'phi':phi,'Z':z})
        if phi==0:
            assert consistent(gd,'Z',1)
        elif expected_f:
            assert consistent(gd,'Z',0)
        else:
            assert rails(gd,'Z')==(False,False)
        assert consistent(gd,'F',f)
        if phi: assert f==expected_f
        domino_phase.append({'A':a,'B':b,'C':c,'D':d,'E':e,'phi':phi,
                             'Z':z,'domino_output_F':f,'expected_evaluation_F':expected_f,
                             'Z_retains_precharge':phi==1 and expected_f==0})
    stable=[]
    for candidate_f,candidate_fb in product((0,1),repeat=2):
        df,_=graph(DIFF_CORE+COMPLEMENTS,{**values,'F':candidate_f,'Fbar':candidate_fb})
        valid=consistent(df,'F',candidate_f) and consistent(df,'Fbar',candidate_fb)
        if valid:
            stable.append((candidate_f,candidate_fb))
            assert all(consistent(df,s+'bar',values[s+'bar']) for s in ('A','B','C','D','E'))
        diff_candidate.append({'A':a,'B':b,'C':c,'D':d,'E':e,
                               'candidate_F':candidate_f,'candidate_Fbar':candidate_fb,'stable':valid})
    assert stable==[(expected_f,g_value)]
    truth.append({'A':a,'B':b,'C':c,'D':d,'E':e,'AB_plus_C_plus_DE':g_value,
                  'printed_F':expected_f,'complement_input_expression':complement_formula,
                  'static_F':int(rails(static_g,'F')[0]),'domino_evaluation_F':expected_f,
                  'differential_F':stable[0][0],'differential_Fbar':stable[0][1]})
save('q7_truth.csv',truth); save('q7_domino_phases.csv',domino_phase)
save('q7_differential_candidates.csv',diff_candidate)
save('q7_transistor_counts.csv',[
    {'implementation':'static CMOS',**count(STATIC)},
    {'implementation':'domino core, complements supplied',**count(DOMINO_CORE)},
    {'implementation':'domino complete from A/B/C/D/E',**count(DOMINO_CORE+COMPLEMENTS)},
    {'implementation':'fully differential core, complements supplied',**count(DIFF_CORE)},
    {'implementation':'fully differential complete from A/B/C/D/E',**count(DIFF_CORE+COMPLEMENTS)},
])
report={
    'all_checks_passed':True,
    'source':{'paper':'2009 final','printed_footer':'Fall 2009','pages':3,
              'Q3_text_page':'1-1','Q3_figure_page':'1-2','Q5_Q7_page':'1-3',
              'read_method':'Native vector original and full rendered pages. Q7 overbar verified visually.'},
    'Q3a':{'full_capacitance_map':{n:{'Cd_Cs_terms':v[0],'Cg_terms':v[1]} for n,v in cap_map.items()},
           'switch_cases':len(component_rows),'maximum_floating_internal_C_over_Cd':max_internal,
           'worst_case_data_controls':'A=B=1,C=0,Vin=1',
           'worst_VF_over_VDD':'(2+2alpha)/(6+2alpha)',
           'critical_alpha_boundary':1,'strict_safe_requirement':'alpha>1',
           'alpha_equals_1':'VF=VDD/2, precisely the inverter switching point; no high-state margin.',
           'scope':'Initially VF=VDD and connected internal nodes=0. Equal device sizes, source Cd=Cs. Three internal nodes are counted but the third is grounded in evaluation; all-data-ON is a real discharge, not isolated sharing.'},
    'Q3b':{'completion':'Add parallel nMOS controlled by explicit Cbar inverter; retain existing pMOS.',
           'original_pass_MOS':1,'added_MOS':3,'complete_MOS':count(Q3B),'truth_cases':len(restore),
           'requested_X0_C0_result':'Y=0 via strong nMOS low path',
           'scope':'No pass threshold or restore-inverter threshold is invented. Disabled TG leaves Y isolated; prior state unspecified.'},
    'Q5':{'frequency_MHz':float(FREQUENCY_MHZ),'period_ns':float(PERIOD_NS),
          'tpcq_ns':float(TPCQ),'tccq_ns':float(TCCQ),'tsetup_ns':float(TSETUP),'thold_ns':float(THOLD),
          'maximum_allowed_propagation_delay_ns':float(MAX_DELAY),
          'minimum_required_contamination_delay_ns':float(MIN_DELAY),
          'conditions':'0.8 ns <= tcd <= tpd <= 3.0 ns under the source common-clock/no-skew model.'},
    'Q7':{'printed_function':'F=NOT(AB+C+DE)', 'overbar_entire_expression_confirmed':True,
          'positive_complement_input_form':'(Abar+Bbar)*Cbar*(Dbar+Ebar)',
          'truth_cases':len(truth),'domino_phase_cases':len(domino_phase),
          'fully_differential_candidate_cases':len(diff_candidate),
          'counts':{'static':count(STATIC),'domino_core':count(DOMINO_CORE),
                    'domino_complete':count(DOMINO_CORE+COMPLEMENTS),
                    'fully_differential_core':count(DIFF_CORE),
                    'fully_differential_complete':count(DIFF_CORE+COMPLEMENTS)},
          'domino_scope':'Input complement inverters are explicit. Complemented controls must be valid/stable before evaluation, or obey nondecreasing domino input transitions during evaluation. A PDN for bare AB+C+DE followed by a domino inverter would output the wrong polarity.',
          'differential_scope':'Exactly one complementary rail pair is stable for every input in the ideal graph.'},
    'model_limits':'Analytical lumped-capacitance and ideal MOS-switch checks only; no process model, threshold body-effect model, waveform simulation, or parasitic extraction.',
}
(OUT/'numerical-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'all_checks_passed':True,'Q3a_switch_cases':len(component_rows),
                  'Q3b_cases':len(restore),'Q7_truth_cases':len(truth),'Q7_domino_phases':len(domino_phase),
                  'Q7_differential_candidates':len(diff_candidate),'alpha_safe':'alpha>1',
                  'tcd_min_ns':float(MIN_DELAY),'tpd_max_ns':float(MAX_DELAY)}))
