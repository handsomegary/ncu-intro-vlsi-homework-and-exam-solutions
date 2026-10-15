"""2008 final Q4/Q5/Q6/Q8 independent verification, standard library only.
Fixed lumped capacitance, linear ON-resistance overwrite, symbolic normalized
square-law families, and ideal mux-latch states; no SPICE or unprinted Vt.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import csv
import json

OUT = Path(__file__).resolve().parent
FIELDS = ('device','type','left_channel','right_channel','gate')

def save(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        fields=list(dict.fromkeys(key for row in rows for key in row))
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def graph(devices,values):
    g,on={},[]
    for name,kind,left,right,gate in devices:
        if values[gate] == (0 if kind=='p' else 1):
            g.setdefault(left,set()).add(right); g.setdefault(right,set()).add(left); on.append(name)
    return g,on

def component(g,start):
    seen,todo=set(),[start]
    while todo:
        n=todo.pop()
        if n not in seen:
            seen.add(n); todo.extend(g.get(n,set())-seen)
    return seen

def reach(g,start,end):
    return end in component(g,start)

def rails(g,node):
    return reach(g,node,'VDD'),reach(g,node,'VSS')

def consistent(g,node,value):
    return rails(g,node)==((True,False) if value else (False,True))

def netrows(devices):
    return [dict(zip(FIELDS,d)) for d in devices]

# Q4 native full adder: both final triangles are static inverters.
ADDER=[
 ('P_pre','p','VDD','z','phi'),
 ('N_A_top','n','z','x','A'),('N_B_left','n','x','foot','B'),
 ('N_C_top','n','z','y','C'),('N_A_right','n','y','foot','A'),
 ('N_B_right','n','y','foot','B'),('N_footer','n','foot','VSS','phi'),
 ('P_carry_inv','p','VDD','Carry','z'),('N_carry_inv','n','Carry','VSS','z'),
 ('P_header','p','VDD','h','phibar'),
 ('P_A_parallel','p','h','t','A'),('P_B_parallel','p','h','t','B'),
 ('P_C_parallel','p','h','t','C'),('P_z','p','t','w','z'),
 ('P_A_series','p','t','s1','A'),('P_B_series','p','s1','s2','B'),
 ('P_C_series','p','s2','w','C'),('N_reset','n','w','VSS','phibar'),
 ('P_sum_inv','p','VDD','Sum','w'),('N_sum_inv','n','Sum','VSS','w'),
]
assert len(ADDER)==20
save('q4_full_adder_literal_netlist.csv',netrows(ADDER))
CD,CG,VDD,VM,ILEAK=F(1,5),F(1),F(9,5),F(1),F(1) # fF, fF, V, V, nA
caps=[]; capvalues={}
for node in ('z','w'):
    terminals=[d[0] for d in ADDER for endpoint in d[2:4] if endpoint==node]
    gates=[d[0] for d in ADDER if d[4]==node]
    value=len(terminals)*CD+len(gates)*CG
    capvalues[node]=value
    caps.append({'node':node,'diffusion_count':len(terminals),'gate_count':len(gates),
                 'diffusion_devices':' '.join(terminals),'gate_devices':' '.join(gates),
                 'capacitance_fF':float(value)})
assert capvalues=={'z':F(18,5),'w':F(13,5)}
save('q4_dynamic_capacitances.csv',caps)
truth=[]
for a,b,c in product((0,1),repeat=3):
    carry=int(a+b+c>=2); total=(a+b+c)%2; z,w=1-carry,1-total
    values={'VDD':1,'VSS':0,'A':a,'B':b,'C':c,'phi':1,'phibar':0,'z':z,'w':w}
    g,on=graph(ADDER,values)
    assert consistent(g,'Carry',carry) and consistent(g,'Sum',total)
    assert rails(g,'z')==((False,True) if carry else (False,False))
    assert rails(g,'w')==((True,False) if w else (False,False))
    truth.append({'A':a,'B':b,'C':c,'z_carrybar':z,'Carry':carry,'w_sumbar':w,'Sum':total})
save('q4_full_adder_truth.csv',truth)
# fF*V/nA numerically gives microseconds.
HOLD_Z_US=capvalues['z']*(VDD-VM)/ILEAK
HOLD_W_US=capvalues['w']*VM/ILEAK
LIMIT_US=min(HOLD_Z_US,HOLD_W_US)
assert HOLD_Z_US==F(72,25) and HOLD_W_US==F(13,5)
hold=[
 {'node':'z','initial_V':float(VDD),'error_threshold_V':float(VM),
  'adverse_leak_direction':'discharge high','allowed_delta_V':float(VDD-VM),'critical_hold_us':float(HOLD_Z_US)},
 {'node':'w','initial_V':0,'error_threshold_V':float(VM),
  'adverse_leak_direction':'charge low','allowed_delta_V':float(VM),'critical_hold_us':float(HOLD_W_US)}
]
save('q4_retention_bounds.csv',hold)
dutyrows=[]
for duty in (F(1,4),F(1,2),F(3,4),F(1)):
    boundary_khz=1000*duty/LIMIT_US
    dutyrows.append({'assumed_evaluation_fraction_D':str(duty),'critical_frequency_kHz':float(boundary_khz),
                     'safe_condition':'f greater than this boundary; equality has zero threshold margin'})
save('q4_duty_parameter.csv',dutyrows)

# Q5: tccq is NOT supplied. Only propagation tpcq=1 ns is printed.
PERIOD_NS=F(10); TPCQ=F(1); SETUP=F(3,2); HOLD=F(1)
MAX_PD=PERIOD_NS-TPCQ-SETUP
assert MAX_PD==F(15,2)
setuprows=[]
for delay in (F(749,100),F(15,2),F(751,100)):
    slack=PERIOD_NS-TPCQ-delay-SETUP
    assert (slack>=0)==(delay<=MAX_PD)
    setuprows.append({'candidate_tpd_ns':float(delay),'setup_slack_ns':float(slack),'setup_pass':slack>=0})
save('q5_setup_bound.csv',setuprows)
holdrows=[]
for hypothetical_tccq in (F(0),F(1,4),F(1,2),F(1)):
    required=max(F(0),HOLD-hypothetical_tccq)
    holdrows.append({'hypothetical_NOT_source_given_tccq_ns':float(hypothetical_tccq),
                     'required_tcd_ns':float(required),'condition':'tccq+tcd>=1 ns'})
save('q5_conditional_hold.csv',holdrows)

# Q6: symbolic normalized threshold eta is a parameter, not a source value.
SCHMITT=[
 ('P1','p','VDD','up','Vin'),('P2','p','up','Vout','Vin'),
 ('P3','p','up','VSS','Vout'),('N2','n','Vout','down','Vin'),
 ('N1','n','down','VSS','Vin'),('N3','n','VDD','down','Vout')]
save('q6_schmitt_literal_netlist.csv',netrows(SCHMITT))
VP,VMIN=F(7,10),F(3,10)
family=[]
for eta in (F(0),F(1,10),F(2,10),F(3,10),F(4,10),F(5,10),F(6,10)):
    ov=VP-eta
    ratio=(ov/VMIN)**2
    assert ov>0
    i_main=ov**2/2
    i_feedback=ratio*VMIN**2/2
    assert i_main==i_feedback
    for polarity,base in (('n',F(4)),('p',F(6))):
        family.append({'polarity':polarity,'hypothetical_eta_Vt_over_VDD':str(eta),
                        'feedback_beta_over_main_beta':str(ratio),
                        'feedback_W_over_L':str(base*ratio),
                        'main_current_over_beta_main_VDD2':str(i_main),
                        'feedback_current_over_beta_main_VDD2':str(i_feedback),
                        'source_numeric_threshold':'NOT GIVEN'})
save('q6_symbolic_family_checks.csv',family)
save('q6_trip_regions_symbolic.csv',[
 {'branch':'rising n','device':'N1','VGS_over_VDD':'0.7','VDS_over_VDD':'0.7-eta_n','overdrive_over_VDD':'0.7-eta_n','region':'saturation boundary'},
 {'branch':'rising n','device':'N3','VGS_over_VDD':'0.3+eta_n','VDS_over_VDD':'0.3+eta_n','overdrive_over_VDD':'0.3','region':'saturation'},
 {'branch':'falling p','device':'P1','VSG_over_VDD':'0.7','VSD_over_VDD':'0.7-eta_p','overdrive_over_VDD':'0.7-eta_p','region':'saturation boundary'},
 {'branch':'falling p','device':'P3','VSG_over_VDD':'0.3+eta_p','VSD_over_VDD':'0.3+eta_p','overdrive_over_VDD':'0.3','region':'saturation'}
])

# Q8a native upstream gate: OAI21, U=NOT(C(A+B)), six MOS.
FEEDER=[
 ('PA','p','VDD','p_ab','A'),('PB','p','p_ab','U','B'),
 ('PC','p','VDD','U','C'),('NC','n','U','n_ab','C'),
 ('NA','n','n_ab','VSS','A'),('NB','n','n_ab','VSS','B')]
save('q8a_upstream_literal_netlist.csv',[
 {**row,'source_W_over_L':2 if row['type']=='p' else 1} for row in netrows(FEEDER)])
# With mu_n=2mu_p, p width2 and n width1 each have ON resistance R.
def equivalent(g,on,start,end):
    vertices=component(g,start)
    assert end in vertices
    edges=[(l,r) for name,kind,l,r,gate in FEEDER if name in on and l in vertices]
    nodes=sorted(vertices-{end}); ix={n:i for i,n in enumerate(nodes)}; sz=len(nodes)
    m=[[F(0) for _ in range(sz+1)] for _ in range(sz)]; m[ix[start]][-1]=1
    for l,r in edges:
        if l!=end: m[ix[l]][ix[l]]+=1
        if r!=end: m[ix[r]][ix[r]]+=1
        if l!=end and r!=end:
            m[ix[l]][ix[r]]-=1; m[ix[r]][ix[l]]-=1
    for col in range(sz):
        pivot=next(i for i in range(col,sz) if m[i][col])
        m[col],m[pivot]=m[pivot],m[col]
        denom=m[col][col]; m[col]=[v/denom for v in m[col]]
        for i in range(sz):
            if i!=col:
                factor=m[i][col]; m[i]=[a-factor*b for a,b in zip(m[i],m[col])]
    return m[ix[start]][-1]
drivers=[]; rup=[]; rdown=[]
for a,b,c in product((0,1),repeat=3):
    value=int(not(c and (a or b)))
    g,on=graph(FEEDER,{'A':a,'B':b,'C':c})
    assert consistent(g,'U',value)
    re=equivalent(g,on,'U','VDD' if value else 'VSS')
    (rup if value else rdown).append(re)
    drivers.append({'A':a,'B':b,'C':c,'U':value,'driver_R_over_R':str(re),
                     'selected_rail':'VDD' if value else 'VSS'})
assert max(rup)==max(rdown)==2
save('q8a_upstream_truth_resistance.csv',drivers)
keeperrows=[]
for wp,wn in product((F(1,2),F(999,1000),F(1),F(1001,1000),F(3,2)),
                      (F(1,4),F(499,1000),F(1,2),F(501,1000),F(3,4))):
    rp=2/wp; rn=1/wn
    allpass=True
    for driver in drivers:
        rd=F(driver['driver_R_over_R'])
        vs=rn/(rd+rn) if driver['U'] else rd/(rd+rp)
        passed=vs>F(1,2) if driver['U'] else vs<F(1,2)
        allpass=allpass and passed
        keeperrows.append({'hypothetical_keeper_P_W_over_L':str(wp),
                            'hypothetical_keeper_N_W_over_L':str(wn),
                            'ABC':str(driver['A'])+str(driver['B'])+str(driver['C']),
                            'write_U':driver['U'],'contended_S_over_VDD':str(vs),
                            'write_crosses_Inv1_half_threshold':passed})
    assert allpass==(wp<1 and wn<F(1,2))
save('q8a_keeper_write_checks.csv',keeperrows)

# Q8b exact mux labels: upper D=0 -> low latch; lower D=1 -> high latch.
save('q8b_source_mux_phases.csv',[
 {'source_latch':'upper, data port0','CLK':0,'transparent':True,'selected':'D','triangle':'noninverting buffer'},
 {'source_latch':'upper, data port0','CLK':1,'transparent':False,'selected':'feedback Q','triangle':'noninverting buffer'},
 {'source_latch':'lower, data port1','CLK':0,'transparent':False,'selected':'feedback Q','triangle':'noninverting buffer'},
 {'source_latch':'lower, data port1','CLK':1,'transparent':True,'selected':'D','triangle':'noninverting buffer'}])
trace=[]; sequence_checks=0
for initial_m,bits in product((0,1),product((0,1),repeat=4)):
    m=q=initial_m; clk=0
    for cycle in range(2):
        dlow,dhigh=bits[2*cycle:2*cycle+2]
        # Low phase: high-level master holds; low-level slave follows stored M.
        old=q; q=m; assert q==old
        # Rising edge: low-level slave closes; high-level master may track D.
        clk=1; m=dlow; assert q==old
        # D changes in high phase: master follows; slave holds old Q.
        m=dhigh; assert q==old
        # Falling edge: master closes on D; slave opens to this stored M.
        clk=0; q=m; assert q==dhigh
    sequence_checks+=1
assert sequence_checks==32
m=q=0
for step,(clk,d,event) in enumerate([(0,0,'initial low'),(0,1,'D changes while low'),
                                   (1,1,'rising edge'),(1,0,'D changes while high'),
                                   (0,0,'falling edge captures0'),(0,1,'D changes while low'),
                                   (1,1,'rising edge'),(1,1,'stable high'),
                                   (0,1,'falling edge captures1')]):
    if clk: m=d
    else: q=m
    trace.append({'step':step,'CLK':clk,'D':d,'master_M':m,'output_Q':q,'event':event})
save('q8b_negative_edge_trace.csv',trace)
report={
 'all_checks_passed':True,
 'source':{'paper':'2008 final','printed_footer':'Fall 2008','pages':3,
           'method':'Original full pages first, student full pages afterward; 2008 is the printed footer despite handwritten year notes.'},
 'Q4':{'style':'NP-domino with two static output inverters','MOS_count':20,
       'z_cap_fF':float(capvalues['z']),'w_cap_fF':float(capvalues['w']),
       'z_hold_boundary_us':float(HOLD_Z_US),'w_hold_boundary_us':float(HOLD_W_US),
       'maximum_evaluation_hold_boundary_us':float(LIMIT_US),
       'safe_condition':'D/f < 2.60 us; f > D/(2.60 us), where D is evaluation duty fraction.',
       'D_source_value':'NOT GIVEN','frequency_boundary_50percent_kHz':float(1000*F(1,2)/LIMIT_US),
       'conservative_full_period_boundary_kHz':float(1000/LIMIT_US),
       'model':'1 nA total per specified dynamic node; worst adverse direction; linear constant leakage; Cgate1fF and Cdrain0.2fF per device.'},
 'Q5':{'frequency_MHz':100,'period_ns':10,'maximum_tpd_ns':float(MAX_PD),
       'tccq_source_value':'NOT GIVEN','hold_condition':'tcd+tccq>=1 ns',
       'conservative_nonnegative_tccq_design_tcd_ns':1},
 'Q6':{'reference_N1_W_um':2,'reference_N1_L_um':0.5,'reference_P1_W_um':3,'reference_P1_L_um':0.5,
       'VTplus':'0.7VDD','VTminus':'0.3VDD','Vtn_source_value':'NOT GIVEN','absVtp_source_value':'NOT GIVEN',
       'N3_W_over_L':'4*((0.7VDD-Vtn)/(0.3VDD))^2',
       'P3_W_over_L':'6*((0.7VDD-absVtp)/(0.3VDD))^2',
       'scope':'Fixed-threshold long-channel square-law onset, Vout~VDD on rising and~0 on falling; N2/P2 at threshold. Feedback lengths are unprovided; no numerical threshold is selected. Normalized eta samples are algebraic checks, not source values.',
       'parameter_checks':len(family)},
 'Q8a':{'upstream_function':'U=NOT(C(A+B))','standard_name':'OAI21',
         'source_p_W_over_L':2,'source_n_W_over_L':1,'mu_n_over_mu_p':2,
         'worst_upstream_pullup_R_over_R':2,'worst_upstream_pulldown_R_over_R':2,
         'strict_keeper_bounds':{'P_W_over_L':'0<P<1','N_W_over_L':'0<N<0.5'},
         'TG_resistance':0,'decision_voltage':'VDD/2',
         'scope':'Linear ON-resistance overwrite approximation; no unprovided Vt is chosen or inferred from inverter trip point. Equal-beta optional pair P=2N does not by itself establish an analog inverter threshold without threshold assumptions.'},
 'Q8b':{'actual_panel':'Figure6(b), right upper and lower mux latches; text reference(c) is a typo.',
         'upper':'low-level, D on port0, noninverting buffer',
         'lower':'high-level, D on port1, noninverting buffer',
         'negative_edge_order':'D -> lower high-level master -> upper low-level slave -> Q',
         'ideal_exhaustive_sequences_checked':sequence_checks,
         'scope':'Ideal latch state phases; no numerical latch delay, overlap or metastability model supplied.'},
 'student_comparison':{'answer.pdf_and_final-answer.pdf':'SHA256 identical; one student answer set, not two independent references.',
                       'duplicate_sha256':'71EE6167FCFDC5205889B851F54130C9190523226D75A556D6EA54EB40746437',
                       'Q4':'Node cap counts agree after handwritten correction; uses high-side margin but does not complete low-node/duty-specific frequency analysis.',
                       'Q5':'Correct setup/hold inequalities, unfinished numerical setup bound; tccq unprovided.',
                       'Q6':'Begins with internal-node relation but switches to constant-R network and drops threshold; no justified unique N3/P3 dimensions.',
                       'Q8':'No complete numerical keeper sizing or correctly identified mux-latch edge timing answer is supplied on the two photographed answer pages.'},
 'limits':'Analytical graph/capacitance/ON-resistance/square-law checks only; no process simulation or layout DRC.'
}
(OUT/'numerical-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'all_checks_passed':True,'Q4_MOS':20,'Q4_truth':len(truth),'Q6_parameter_checks':len(family),
                  'Q8_driver_states':len(drivers),'Q8_keeper_cases':len(keeperrows),'Q8_sequences':sequence_checks}))

