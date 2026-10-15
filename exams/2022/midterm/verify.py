#!/usr/bin/env python3
"""Analytical checks for complete 2022 midterm; no process simulation."""
import csv,itertools,json,math
from pathlib import Path
OUT=Path(__file__).resolve().parent
def save(name,rows):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def mux(s,i0,i1):return i1 if s else i0
def connected(edges,start):
    nodes={start}
    while True:
        nxt=nodes|{b for a,b in edges if a in nodes}|{a for a,b in edges if b in nodes}
        if nxt==nodes:return nodes
        nodes=nxt
def core(v):
    n=[];p=[]
    if v['X']:n.append(('U','n'))
    for t in ['Y','Z','W']:
        if v[t]:n.append(('n','GND'))
    if not v['X']:p.append(('U','VDD'))
    chain=['U','p1','p2','VDD']
    for i,t in enumerate(['Y','Z','W']):
        if not v[t]:p.append((chain[i],chain[i+1]))
    lo='GND' in connected(n,'U');hi='VDD' in connected(p,'U');assert lo != hi
    return int(hi),lo,hi
def main():
    tree=[]
    for s0,s1,s2 in itertools.product([0,1],repeat=3):
        first=[mux(s2,[f'x{i}' for i in range(8)][2*k],[f'x{i}' for i in range(8)][2*k+1]) for k in range(4)]
        second=[mux(s1,first[2*k],first[2*k+1]) for k in range(2)]
        selected=mux(s0,*second);index=4*s0+2*s1+s2;assert selected==f'x{index}'
        tree.append({'s0':s0,'s1':s1,'s2':s2,'selected_index':index,'selected_signal':selected,'enabled_TGs_on_path':3})
    save('q2_mux8_selection.csv',tree)
    shannon=[]
    for a,b,c,d in itertools.product([0,1],repeat=4):
        upper=mux(d,c,1);lower=mux(d,a,1);actual=mux(b,upper,lower)
        target=int((a and b)or((not b)and c)or d);assert actual==target
        shannon.append({'A':a,'B':b,'C':c,'D':d,'upper_C_plus_D':upper,'lower_A_plus_D':lower,'F':actual,'target':target})
    save('q2_shannon_truth.csv',shannon)
    ladder=[{'selection_bits_N':n,'TG_R_Cint_Elmore_coefficient':n*(n+1)/2,'TG_R_CL_coefficient':n} for n in range(1,11)]
    save('q2_unbuffered_rc_scaling.csv',ladder)
    h=2980.0;n=8;f=h**(1/n)
    stage_choices=[]
    for k in range(2,22,2):
        ratio=h**(1/k);delay=1.5*k*ratio
        stage_choices.append({'inverters':k,'noninverting':True,'stage_ratio':ratio,'unmodified_worst_delay_over_R_Cg':delay})
    assert min(stage_choices,key=lambda r:r['unmodified_worst_delay_over_R_Cg'])['inverters']==8
    save('q3_stage_count.csv',stage_choices)
    stages=[]
    tr0=tf0=tr1=tf1=0.0
    for i in range(n):
        s=f**i;old_next=f**(i+1) if i<n-1 else h
        new_next=1.5*f**(i+1) if i<n-1 else h
        old_r_input_rise=(1 if i%2==0 else 2)/s
        old_r_input_fall=(2 if i%2==0 else 1)/s
        balanced_r=1/s
        tr0+=old_r_input_rise*old_next;tf0+=old_r_input_fall*old_next
        tr1+=balanced_r*new_next;tf1+=balanced_r*new_next
        stages.append({'stage_index_zero_based':i,'NMOS_width_over_Wmin':s,
                       'PMOS_width_before_over_Wmin':s,'PMOS_width_after_over_Wmin':2*s,
                       'input_cap_before_over_Cg':s,'input_cap_after_over_Cg':1.5*s,
                       'load_before_over_Cg':old_next,'load_after_over_Cg':new_next,
                       'balanced_stage_delay_over_R_Cg':balanced_r*new_next})
    assert math.isclose(tr0,1.5*n*f) and math.isclose(tf0,tr0)
    assert math.isclose(tr1,(1.5*(n-1)+1)*f) and math.isclose(tf1,tr1)
    assert stages[0]['input_cap_after_over_Cg']==1.5
    save('q3_fixed_NMOS_balancing.csv',stages)
    q4=[]
    for vin in [.45,.5,.6,.7,.75]:
        vx=.4;vout=1.2;vt=.4
        cases=[('N1',vin,vx),('N2',vout-vx,1.2-vx),('N3',vin-vx,vout-vx)]
        for name,vgs,vds in cases:
            reg='cutoff' if vgs<=vt else('saturation' if vds>=vgs-vt else'triode')
            assert reg==('cutoff' if name=='N3' else'saturation')
            q4.append({'Vin_V':vin,'device':name,'VGS_V':vgs,'VDS_V':vds,'region':reg})
    assert math.isclose(1.2*1/(1+2)+.4,.8)
    save('q4_regions.csv',q4)
    xor=[]
    for a,b in itertools.product([0,1],repeat=2):
        # TG passes B iff A=0. Rail-fed p/n branch controlled by B.
        drivers=[]
        if a==0:drivers.append(('TG_B',b))
        drivers.append(('pMOS_from_A',a) if b==0 else('nMOS_from_Abar',1-a))
        assert all(v==int(bool(a)^bool(b)) for _,v in drivers)
        xor.append({'A':a,'B':b,'TG_enabled_A0':a==0,'right_device_on':'pMOS' if b==0 else'nMOS',
                    'right_connected_input':'A' if b==0 else'Abar','y':drivers[0][1],
                    'XOR_reference':int(bool(a)^bool(b)), 'restoring_fixed_VDD_GND_stage':False})
    save('q5_xor_routes.csv',xor)
    truth=[]
    for bits in itertools.product([0,1],repeat=4):
        v=dict(zip(['X','Y','Z','W'],bits));u,lo,hi=core(v);actual=1-u
        expected=int(v['X']and(v['Y']or v['Z']))or int(v['X']and v['W']);assert actual==expected
        truth.append({**v,'core_U':u,'PDN_conducts':lo,'PUN_conducts':hi,'F':actual,'expected':expected})
    save('q6a_cmos_truth.csv',truth)
    seq=[]
    for bits in [(1,0,1),(1,0,0),(1,0,1)]:
        x,y,z=bits;out=int(not(x and(y or z)))
        seq.append({'XYZ':''.join(map(str,bits)),'F':out,'active_path':'pMOS Y+Z in series' if out else'nMOS X+Z in series',
                    'path_resistance_over_own_type_R':2,'equivalent_width_over_W':.5})
    assert [r['F'] for r in seq]==[0,1,0]
    save('q6b_equivalent_inverter.csv',seq)
    report={'question_points':[35,20,10,15,10,10],'point_total':100,
        'Q2':{'mux_tree_TGs':14,'transistors_in_TGs':28,'select_complement_inverters':3,
              'total_including_select_generators':34,'index_convention':'4s0+2s1+s2',
              'unbuffered_Elmore':'R_TG*Cint*N(N+1)/2 + N*R_TG*CL',
              'Shannon_function':'F=not(B)*(C+D)+B*(A+D)'},
        'Q3':{'source_Cg_fF':1,'source_CL_pF':2.98,'H':h,'inverters':n,'index_range':'0 through7',
              'optimal_equal_ratio_exact':f,'source_rounded_e':2.7,
              'unmodified_even_chain_both_direction_delays_over_R_Cg':tr0,
              'balanced_modified_both_direction_delays_over_R_Cg':tr1,
              'modified_formula':'[(3N-1)/2]*f R Cg','modified_rounded_e_estimate_over_R_Cg':11.5*2.7,
              'modified_first_input_cap_over_Cg':1.5,
              'constraint_note':'Doubling PMOS while NMOS fixed necessarily raises A output load from Cg to1.5Cg; part(b) cannot also retain the old input load without violating fixed NMOS'},
        'Q4':{'source_Vtn_V':.4,'source_R_N1_N2_N3':[1,2,1],'RC_divider_VX_V':.4,'Vin_switch_onset_V':.8,
              'open_t1_t2_regions':{'N1':'saturation','N2':'saturation','N3':'cutoff'},'model':'Stated ON-resistance approximation, not exact device transient'},
        'Q5':{'function':'A XOR B','weakness':'Finite pass/input-rail drive depends on input drivers; no independent fixed-rail restoring stage',
              'not_claimed':'No driving ability whatsoever; all ideal static input states have correct full-rail paths'},
        'Q6':{'a_count_including_output_inverter':10,'b_equivalent_n_width':'W/2','b_equivalent_p_width':'W/2',
              'b_rise_delay':'2Rp*Co','b_fall_delay':'2Rn*Co','source_mobility_ratio_for_Q6':'unspecified; Rp/Rn kept symbolic'},
        'method':'Source-derived graph/truth and analytical RC checks; no SPICE simulation'}
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'Checks pass: mux8, Shannon16, Q3 N8 f{f:.9f}, modifiedT{tr1:.9f}RCg, Q4 regions, XOR4, CMOS16, equivalent transition sequence.')
if __name__=='__main__':main()
