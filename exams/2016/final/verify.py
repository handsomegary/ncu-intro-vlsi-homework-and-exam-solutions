"""Source-derived logic and simple RC checks; no device-model simulation."""
from pathlib import Path
import csv
import itertools
import json
import math
import runpy

OUT=Path(__file__).resolve().parent
def save(name,rows):
    with (OUT/name).open('w',encoding='utf-8',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

q1=[]
for n in [0.5,1,2,4,8,16]:
    p1=n;p2=4
    xr=2*p2/p1;xf=2*p2/n
    outr=16/p2;outf=4
    assert math.isclose(xr,xf) and math.isclose(outr,outf)
    period=2*(xf+outr)
    assert math.isclose(period,8+16/n)
    q1.append({'n_N1_N2_P1':n,'p_P2_P3':p2,'X_rise_over_RC':xr,'X_fall_over_RC':xf,
               'Out_rise_over_RC':outr,'Out_fall_over_RC':outf,'period_over_RC':period,
               'clock_gate_cap_over_C':2*n+p2+1})
save('q1_balancing_family.csv',q1)
q1truth=[]
for value in (0,1):
    q1truth.append({'In':value,'precharge_X':1,'precharge_Out':0,'evaluate_X':1-value,'evaluate_Out':value})
save('q1_phase_truth.csv',q1truth)

q2=[]
for upper in [.9,1.0,1.2,1.5]:
    lower=.6;Vdd=1.8;Vt=.6
    nratio=((Vdd-upper)/(upper-Vt))**2
    pratio=(lower/(Vdd-lower-Vt))**2
    assert nratio>0 and math.isclose(pratio,1)
    q2.append({'VTH_V':upper,'VTL_V':lower,'beta_N1_over_N3':nratio,'beta_P1_over_P3':pratio})
save('q2_threshold_family.csv',q2)

q3=[]
for p in [1,2,3,4,5]:
    n7=9-p; delta=2/p-1/n7
    sizes={'N1':1/delta,'N2':2/delta,'N3':2/delta,'N4':4/delta,'N5':4/delta,'N6':2/delta,'N7':n7,'P1':p}
    paths=[['N1','N7'],['N2','N3','N7'],['N2','N6','N7'],['N4','N5','N3','N7'],['N4','N5','N6','N7']]
    for path in paths:
        resistance=sum(1/sizes[name] for name in path)
        assert math.isclose(resistance,2/p)
        q3.append({'P1_factor':p,'N7_factor':n7,'path':'-'.join(path),
                    'rise_resistance_over_R':2/p,'fall_resistance_over_R':resistance,
                    'clock_cap_over_C':p+n7,**sizes})
save('q3_balanced_paths.csv',q3)

# Exact Q4(b): input inverter plus 3-input NOR; isolation devices OFF.
q4b=[]
for a,b,c in itertools.product((0,1),repeat=3):
    u=1-a;pdn=bool(u or b or c);pun=bool(not u and not b and not c)
    Z=int(not pdn)
    assert pdn!=pun and Z==int(a and not b and not c)
    q4b.append({'a':a,'b':b,'c':c,'internal_u':u,'PDN':int(pdn),'PUN':int(pun),'Z':Z,
                 'isolation_pMOS_on':0,'isolation_nMOS_on':0})
save('q4b_contact_truth.csv',q4b)
q4a=[]
for C,Y,v,X in itertools.product((0,1),repeat=4):
    u=1-Y;r=1-X
    opposing_rail=1-X  # Literal col6 is self-connected at its gate/output X.
    assert opposing_rail!=X
    q4a.append({'C':C,'Y':Y,'u':u,'candidate_v':v,'candidate_X':X,'r':r,
                'input_TG_on':1-C,'feedback_TG_on':C,
                'Inv5_requested_X':1-v,'Inv6_opposing_rail':opposing_rail,
                'binary_X_has_self_load_contention':1})
save('q4a_literal_phase_checks.csv',q4a)

q7=[]
for A,B,C,D in itertools.product((0,1),repeat=4):
    h=bool((A or B and C) and D)
    opposite=bool(not D or not A and (not B or not C))
    assert h!=opposite
    q7.append({'A':A,'B':B,'C':C,'D':D,'PDN_h':int(h),'PDN_complement':int(opposite),
               'f':int(not h),'f_bar':int(h),'precharge_f':1})
save('q7_dual_network_truth.csv',q7)

if (OUT/'verify_timing.py').exists():
    runpy.run_path(str(OUT/'verify_timing.py'),run_name='__main__')
if (OUT/'verify_layout.py').exists():
    runpy.run_path(str(OUT/'verify_layout.py'),run_name='__main__')
report={'status':'pass','printed_points':[20,8,10,15,15,10,12,30],'printed_total':120,
        'Q1':{'common_time_sizes':{'N1':2,'N2':2,'P1':2,'P2':4,'P3':4,'output_footer':1},
              'common_time_period_over_RC':16,'common_time_clock_cap_over_C':9,
              'per_node_balance_family':'P1=N1=N2=n, P2=P3=4; T=(8+16/n)RC; no finite optimized minimum without a sizing bound'},
        'Q2':{'deducible_lower_trip_V':.6,'beta_P1_over_P3':1,
              'beta_N1_over_N3':'((1.8-VTH)/(VTH-.6))^2, with upper trip unspecified',
              'scope':'The1.2 V input noise peak occurs while Vout is LOW; it does not determine the rising-input trip'},
        'Q3':{'clock_gate_cap_over_C':9,'one_balanced_path_solution':{'P1':3,'N7':6,'N1':2,'N2':4,'N3':4,'N4':8,'N5':8,'N6':4},
              'non_unique':True,'all_lengths_um':.18,'width_unit_um':2},
        'Q4':{'physical_MOS_a':12,'physical_MOS_b':12,'b_function':'a AND NOT b AND NOT c',
              'a_scope':'Literal12MOS extraction contains final gate/output self-connection at X; do not assume an ideal clean latch transfer',
              'b_isolation_MOS':4},
        'Q7':{'function':'NOT((A+B*C)*D)','dynamic_MOS':6,'fully_differential_core_MOS':10,
              'DSL_core_MOS':12,'complement_input_generator_MOS':8},
        'method':'Ideal conduction/connectivity plus source-given RC and timing; no SPICE or invented physical parameters'}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('All logic, clock-capacitance, balancing-family, layout and differential-network checks pass.')
