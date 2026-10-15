"""Fall 2018 final: exhaustive MOS/logic, analytical RC and timing checks.

Python standard library only; run from any directory. This is not process
simulation. Ratioed DSL/latches are explicitly separated from rail-exclusive
static logic: their analogue write/noise margins need device data.
"""
from pathlib import Path
from fractions import Fraction as F
import csv
import itertools
import json

HERE=Path(__file__).resolve().parent


def mos(name,kind,drain,gate,source,role="logic",weak=False,column=None):
    return dict(name=name,kind=kind,drain=drain,gate=gate,source=source,
                body="VDD" if kind=="P" else "VSS",role=role,weak=weak,column=column)


def inv(prefix,out,gate,role="inverter",column=None):
    return [mos(prefix+"P","P",out,gate,"VDD",role,column=column),
            mos(prefix+"N","N",out,gate,"VSS",role,column=column)]


def adjacency(graph,values,extra=()):
    edges={}
    for m in graph:
        assert m['body']==('VDD' if m['kind']=='P' else 'VSS')
        active=not values[m['gate']] if m['kind']=='P' else values[m['gate']]
        if active:
            a,b=m['drain'],m['source']
            edges.setdefault(a,[]).append((b,m['name']))
            edges.setdefault(b,[]).append((a,m['name']))
    for a,b,name in extra:
        edges.setdefault(a,[]).append((b,name));edges.setdefault(b,[]).append((a,name))
    return edges


def path_to(graph,values,start,end,extra=()):
    edges=adjacency(graph,values,extra)
    queue,seen=[(start,[])],{start}
    for node,path in queue:
        if node==end:return path
        for other,name in edges.get(node,[]):
            if other not in seen:
                seen.add(other);queue.append((other,path+[name]))
    return None


def rail(graph,values,node,extra=()):
    hi,lo=path_to(graph,values,node,'VDD',extra),path_to(graph,values,node,'VSS',extra)
    assert not(hi is not None and lo is not None),(node,values,hi,lo)
    return (1 if hi is not None else 0 if lo is not None else None),hi,lo


def csv_file(name,rows):
    with (HERE/name).open('w',encoding='utf-8',newline='')as out:
        writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def domino_graph():
    graph=[]
    for i,inputs,out in (('1',('A','B'),'u'),('2',('u','C'),'Y')):
        graph+=[mos('PRE'+i,'P','d'+i,'phi','VDD'),
                mos('N'+i+'a','N','d'+i,inputs[0],'s'+i),
                mos('N'+i+'b','N','s'+i,inputs[1],'e'+i),
                mos('FOOT'+i,'N','e'+i,'phi','VSS')]+inv('OUT'+i,out,'d'+i)
    return graph


def q2():
    graph=domino_graph();rows=[];phases=[]
    pdn=[m for m in graph if m['kind']=='N' and m['role']!='inverter']
    for a,b,c in itertools.product((0,1),repeat=3):
        vv=dict(VDD=1,VSS=0,A=a,B=b,C=c,u=0,phi=1)
        d1=int(path_to(pdn,vv,'d1','VSS')is None);u=1-d1;vv['u']=u
        d2=int(path_to(pdn,vv,'d2','VSS')is None);y=1-d2
        assert u==(a&b)and y==(a&b&c)
        rows.append(dict(A=a,B=b,C=c,u=u,Y=y,passed=True))
        for phi in (0,1):
            vv.update(phi=phi,d1=d1 if phi else 1,d2=d2 if phi else 1,u=u if phi else 0,Y=y if phi else 0)
            for node in ('d1','d2','u','Y'):
                value,hi,lo=rail(graph,vv,node);assert value in (None,vv[node])
                if not phi:assert value==vv[node]
                phases.append(dict(A=a,B=b,C=c,phi=phi,node=node,value=vv[node],
                                   high_path=';'.join(hi or []),low_path=';'.join(lo or []),charge_storage=(value is None),passed=True))
    csv_file('q2_domino_truth.csv',rows);csv_file('q2_phase_checks.csv',phases)
    cap=F(22,10);current_nA=F(1);margin=F(1,2)
    retention_ns=cap*margin/current_nA*1000
    assert retention_ns==1100
    droop=F(2,1000)*current_nA/cap
    shared=F(18,10)*cap/(cap+F(2,10))
    assert shared==F(165,100)and shared-droop>F(13,10)
    leakage=[dict(model='raw_node_no_sharing',cap_fF=float(cap),initial_V=1.8,net_leak_nA=1,
                  threshold_V=1.3,retention_ns=1100,evaluate_ns=2,droop_V=float(droop),passed=True),
             dict(model='all_junction_internal_share',cap_fF=2.4,initial_V=float(shared),net_leak_nA=1,
                  threshold_V=1.3,retention_ns=840,evaluate_ns=2,droop_V=float(F(2,1000)/F(24,10)),passed=True)]
    csv_file('q2_retention.csv',leakage)
    return dict(cases=8,phase_node_cases=64,graph=graph,MOS=12,explicit_duty_percent=50,
                evaluate_ns=2,concurrent_precharge_ns=2,min_period_ns=4,max_MHz=250,
                no_sharing_retention_ns=1100,leakage_net_nA=1,
                edge_meaning='positive AND output rises during evaluation; resets low during precharge',
                no_process_measurement=True)


def q3():
    widths={'N1':100,'N2':100,'N3':100,'P1':200,'P2':200,'P3':200}
    csv_file('q3_classroom_sizing.csv',[dict(device=k,width_nm=v,length_nm=40,model='effective_external_C;choose_a1',passed=True)for k,v in widths.items()])
    trip_hi=F(4,10)+F(2)*F(1,2);trip_lo=F(2)*F(1,2)-F(4,10)
    assert(trip_hi,trip_lo)==(F(14,10),F(6,10))
    # Literal feedback gate loading: eta is NOT given in this paper.
    eta=F(1,10);a=F(1);k=1+eta*(1+2/a)
    rn2=2/k-1;rp2=2/k-a
    assert rn2>0 and rp2>0 and(1+rn2)*k==2 and(a+rp2)*k==2
    assert F(2)*eta/(1-eta)<a<(2-2*eta)/(1+eta)
    # Part b's NEW trip values imply feedback/main resistance ratio2.
    assert F(6,10)+F(18,10)/3==F(12,10)
    assert F(18,10)*2/3-F(6,10)==F(6,10)
    # For the declared constant-R overlap illustration, one active feedback
    # branch of 2R is parallel to the other three main devices (3R), then
    # series with the remaining main device R. 3R is only a branch path.
    overlap_stc=1+F(3)*2/(3+2)
    assert overlap_stc==F(11,5) and 1/overlap_stc>F(1,4)
    csv_file('q3_overlap_model.csv',[
        dict(circuit='STC_one_active_feedback_full_network',normalized_equivalent_R=float(overlap_stc),normalized_supply_current=float(1/overlap_stc),
             model='R+(3R parallel 2R);matched main R;constant resistor overlap illustration'),
        dict(circuit='feedback_removed_four_device_inverter',normalized_equivalent_R=4,normalized_supply_current=1/4,
             model='same main R;constant resistor overlap illustration')])
    return dict(widths_nm=widths,length_nm=40,trip_points_V=[.6,1.4],
                p_family='a=RP1/R,0<a<2;WP1=WP3=200/a,WP2=200/(2-a)nm',
                beta_interpretation='stated factor2 interpreted as equal-geometry n/p process strength for RC width scaling; matches graded sizing',
                literal_C='C is drawn external/effective load; no given equality C=CgateN1',
                literal_gate_loading='eta=CgateN1/C;K=1+eta(1+2/a);RN2/R=2/K-1,RP2/R=2/K-a',
                literal_feasible_condition='0<=eta<1/3, 2eta/(1-eta)<a<2(1-eta)/(1+eta); no eta value supplied',
                part_b_classroom_answer='feedback-removed inverter has smaller overlap current under declared matched-resistance model',
                part_b_new_thresholds='1.2/.6V atVDD1.8VT.6 imply RN3=2RN1 and RP3=2RP1, not part_a ratio1',
                power_limit='No numerical or universally ordered cycle-average Psc without input slew/waveform and voltage-dependent device currents; resistor illustration is not HSPICE')


def h_network(out,prefix='H'):
    return [mos(prefix+'A','N',out,'A',prefix+'u'),mos(prefix+'B','N',prefix+'u','B',prefix+'v'),
            mos(prefix+'C','N',prefix+'v','C','VSS'),mos(prefix+'D','N',prefix+'u','D','VSS')]


def complement_network(out,prefix='G'):
    return [mos(prefix+'A','N',out,'Ab','VSS'),mos(prefix+'D','N',out,'Db',prefix+'w'),
            mos(prefix+'B','N',prefix+'w','Bb','VSS'),mos(prefix+'C','N',prefix+'w','Cb','VSS')]


def dynamic_complex_graph():
    net=h_network('f')
    for m in net:
        if m['source']=='VSS':m['source']='eval'
    return[mos('Ppre','P','f','phi','VDD')]+net+[mos('Nfoot','N','eval','phi','VSS')]


def differential_graph(dsl=False):
    if dsl:
        return h_network('vf')+complement_network('vg')+[
            mos('NFsplit','N','f','Vref','vf','reference_clamp'),mos('NGsplit','N','g','Vref','vg','reference_clamp'),
            mos('PFload','P','f','vg','VDD','ratioed_load',True),mos('PGload','P','g','vf','VDD','ratioed_load',True)]
    return h_network('f')+complement_network('g')+[
        mos('PFload','P','f','g','VDD','cross_coupled_load'),mos('PGload','P','g','f','VDD','cross_coupled_load')]


def q4():
    dynamic=dynamic_complex_graph();dcvs=differential_graph();dsl=differential_graph(True)
    rows=[];phases=[]
    for a,b,c,d in itertools.product((0,1),repeat=4):
        vv=dict(VDD=1,VSS=0,A=a,B=b,C=c,D=d,Ab=1-a,Bb=1-b,Cb=1-c,Db=1-d,phi=1)
        f=int(path_to(h_network('f'),vv,'f','VSS')is None)
        g=int(path_to(complement_network('g'),vv,'g','VSS')is None)
        expected=int(not(a and((b and c)or d)))
        assert(f,g)==(expected,1-expected)
        vv.update(f=f,g=g)
        assert rail(dcvs,vv,'f')[0]==f and rail(dcvs,vv,'g')[0]==g
        dsl_f_ground=path_to(dsl[:8],vv,'vf','VSS')is not None
        dsl_g_ground=path_to(dsl[:8],vv,'vg','VSS')is not None
        assert dsl_f_ground!=dsl_g_ground and dsl_f_ground==bool(1-f)
        rows.append(dict(A=a,B=b,C=c,D=d,f=f,g=g,DSL_vf_PDN_on=dsl_f_ground,DSL_vg_PDN_on=dsl_g_ground,
                         DSL_check_scope='lower PDN complement only; no analogue rail/noise-margin claim',passed=True))
        for phi in (0,1):
            vv['phi']=phi;actual,hi,lo=rail(dynamic,vv,'f')
            expected_phase=f if phi else 1
            assert actual in(None,expected_phase)
            phases.append(dict(A=a,B=b,C=c,D=d,phi=phi,f=expected_phase,charge_storage=(actual is None),passed=True))
    csv_file('q4_logic_checks.csv',rows);csv_file('q4_dynamic_phase_checks.csv',phases)
    csv_file('q4_DSL_netlist.csv',dsl)
    return dict(cases=16,dynamic_phase_cases=32,dynamic_graph=dynamic,DCVSL_graph=dcvs,DSL_graph=dsl,
                dynamic_MOS=6,DCVSL_MOS=10,DSL_MOS=12,complement_inputs='Ab,Bb,Cb,Db externally available;4inverters add8MOS',
                function='f=NOT[A(BC+D)]',complement_PDN='Ab+Db(Bb+Cb)',
                DSL_bias='external Vref; clamp gates use Vref, pMOS loads use opposite LOWER nodes',
                DSL_limit='ratioed analogue/DC behavior requires Vref and strengths; verifier checks complementary functional PDNs only')


def np_graph():
    return[mos('P1','P','X','CLK','VDD','precharge'),
           mos('N1','N','X','A','n1'),mos('N2','N','n1','B','n2'),mos('N3','N','n2','C','n3'),
           mos('N4','N','n3','CLK','VSS','evaluation'),
           mos('P2','P','phead','CLKB','VDD','evaluation'),
           mos('P3','P','pxd','X','phead'),mos('P4','P','Y','D','pxd'),
           mos('P5','P','Y','E','phead'),mos('P6','P','pgf','G','phead'),mos('P7','P','Y','F','pgf'),
           mos('N5','N','Y','CLKB','VSS','precharge')]


def q5():
    graph=np_graph();rows=[];phases=[]
    for bits in itertools.product((0,1),repeat=7):
        vals=dict(zip('ABCDEFG',bits));vv=dict(VDD=1,VSS=0,CLK=1,CLKB=0,X=1,**vals)
        x=int(path_to(graph[:5],vv,'X','VSS')is None);vv['X']=x
        y=int(path_to(graph[5:],vv,'Y','VDD')is not None)
        a,b,c,d,e,f,g=bits;expected=int((a and b and c and not d)or not e or(not f and not g))
        assert y==expected and x==int(not(a and b and c))
        rows.append(dict(**vals,X=x,Y=y,expected_Y=expected,passed=True))
        for clk in(0,1):
            vv.update(CLK=clk,CLKB=1-clk,X=x if clk else 1,Y=y if clk else 0)
            for node in('X','Y'):
                value,hi,lo=rail(graph,vv,node);assert value in(None,vv[node])
                if not clk:assert value==vv[node]
                phases.append(dict(**vals,CLK=clk,node=node,value=vv[node],high_path=';'.join(hi or []),
                                   low_path=';'.join(lo or []),charge_storage=(value is None),passed=True))
    csv_file('q5_NP_truth.csv',rows);csv_file('q5_NP_phase_checks.csv',phases)
    widths={'P1':80,'N1':160,'N2':160,'N3':160,'N4':160,'P2':120,'P3':120,'P4':120,'P5':60,'P6':120,'P7':120,'N5':20}
    res={k:F(40 if k.startswith('P')else 20,v)for k,v in widths.items()}
    assert sum(res[k]for k in('N1','N2','N3','N4'))==res['P1']==F(1,2)
    assert res['P2']+res['P3']+res['P4']==res['P2']+res['P5']==res['P2']+res['P6']+res['P7']==res['N5']==1
    csv_file('q5_balanced_sizing.csv',[dict(device=k,width_nm=v,length_nm=20,R_over_RN5=float(res[k]),passed=True)for k,v in widths.items()])
    clock_load=[dict(device=k,clock='CLK' if k in('P1','N4')else 'CLKB',gate_cap_over_C=widths[k]/20)for k in('P1','N4','P2','N5')]
    assert sum(r['gate_cap_over_C']for r in clock_load)==19
    csv_file('q5_clock_loading.csv',clock_load)
    return dict(input_cases=128,phase_node_cases=512,graph=graph,MOS=12,
                function='X=NOTABC;Y=ABC*NOTD+NOTE+NOTF*NOTG',balanced_widths_nm=widths,length_nm=20,
                clock_load_over_C=19,clock_power='19*C*VDD^2*f for declared balanced sizing; no unspecified clock-generator/wire cap',
                nonunique_family='rho=RP2/RN5 in(0,1);WP2=40/rho;WP3,4,6,7=80/(1-rho);WP5=40/(1-rho)nm, equal N allocation selected',
                general_clock_power_equal_N='(13+2/rho)*C*VDD^2*f',protocol='primary inputs stable for evaluation; X may only fall,Ymayonlyrise')


def layout_graph():
    graph=[]
    for prefix,out,gate,column in(('I1','a','X',1),('C1','c1','CLK',3),('M1','m','b',4),('MF','b','m',5),
                                  ('C2','c2','CLKB',7),('S1','s','d',8),('SF','d','s',9),('O1','Y','s',10)):
        graph+=inv(prefix,out,gate,'feedback' if prefix in('MF','SF')else 'inverter',column)
    graph +=[mos('TGM_P','P','b','c1','a','pass',column=2),mos('TGM_N','N','b','CLK','a','pass',column=2),
             mos('TGS_P','P','d','c2','m','pass',column=6),mos('TGS_N','N','d','CLKB','m','pass',column=6)]
    return sorted(graph,key=lambda m:(m['column'],m['kind']=='N'))


def mixed_components(graph,values,extra=()):
    edges=adjacency(graph,values,extra);todo_nodes=set(edges);mixed=[]
    while todo_nodes:
        start=next(iter(todo_nodes));pending=[start];seen={start}
        for node in pending:
            for other,_ in edges.get(node,[]):
                if other not in seen:seen.add(other);pending.append(other)
        todo_nodes-=seen
        assigned={values[k]for k in seen if k in values}
        if len(assigned)>1:mixed.append(sorted(seen))
    return mixed


def q6():
    graph=layout_graph();assert len(graph)==20
    rows=[]
    for x,clk,b,d in itertools.product((0,1),repeat=4):
        vv=dict(VDD=1,VSS=0,X=x,CLK=clk,CLKB=1-clk,a=1-x,c1=1-clk,c2=clk,b=b,m=1-b,d=d,s=1-d,Y=d)
        mixed=mixed_components(graph,vv)
        consistent=(b==1-x)if clk else(d==1-b)
        assert bool(mixed)==(not consistent)
        rows.append(dict(X=x,CLK=clk,b=b,m=1-b,d=d,s=1-d,Y=d,settled_consistent=consistent,
                         mismatched_write_contention=bool(mixed),mixed_components=json.dumps(mixed),passed=True))
    csv_file('q6_layout_states.csv',rows);csv_file('q6_physical_MOS.csv',graph)
    events=[]
    for old,high_input,low_input in itertools.product((0,1),repeat=3):
        b=1-high_input;m=1-b;d=old
        for event,clk,x in(('high_tracking',1,high_input),('falling_capture',0,high_input),('low_input_change',0,low_input)):
            if clk==0:d=m
            assert d==(old if clk else high_input)
            events.append(dict(case=len(events)//3,event=event,CLK=clk,X=x,b=b,m=m,d=d,Y=d,
                               assumption='enabled write overrides feedback; source gives no strength values',passed=True))
    csv_file('q6_conditional_events.csv',events)
    return dict(device_count=20,graph=graph,input_memory_clock_states=16,
                consistent_states=8,write_contention_states=8,conditional_event_rows=24,
                topology='8inverters+2inputTGs;feedback permanently connected;localclockINV in each half',
                conditional_behavior='negative-edge noninverting Y=X capture, subject to ratioed write margins',
                source_columns_crop_x=[308,461,624,716,866,1053,1215,1305,1456,1622],
                no_analogue_writeability_claim=True)


def register_graph():
    return [mos('MIN_P','P','mi','CLKB','D','pass'),mos('MIN_N','N','mi','CLK','D','pass')]+inv('I1','mo','mi')+inv('MFB','mf','mo')+[
        mos('MFB_P','P','mi','CLK','mf','pass'),mos('MFB_N','N','mi','CLKB','mf','pass'),
        mos('SIN_P','P','si','CLK','mo','pass'),mos('SIN_N','N','si','CLKB','mo','pass')]+inv('I2','Q','si')+[
        mos('P2feedback','P','si','Q','VDD','ratioed_feedback'),mos('N2feedback','N','si','Q','VSS','ratioed_feedback')]


def q7():
    graph=register_graph();assert len(graph)==14
    rows=[]
    for d,clk,mi,si in itertools.product((0,1),repeat=4):
        vv=dict(VDD=1,VSS=0,D=d,CLK=clk,CLKB=1-clk,mi=mi,mo=1-mi,mf=mi,si=si,Q=1-si)
        extra=[('D','VDD'if d else 'VSS','Dsource')]
        mixed=mixed_components(graph,vv,extra)
        consistent=(mi==d)if clk else(si==1-mi)
        assert bool(mixed)==(not consistent)
        rows.append(dict(D=d,CLK=clk,mi=mi,mo=1-mi,si=si,Q=1-si,consistent=consistent,
                         write_contention=bool(mixed),passed=True))
    csv_file('q7_register_states.csv',rows)
    ratio=[]
    for driver,tg,feedback in((F(1),F(1,2),F(2)),(F(2),F(1),F(4))):
        hi=feedback/(driver+tg+feedback);lo=(driver+tg)/(feedback+driver+tg)
        assert hi>F(1,2)and lo<F(1,2)
        ratio.append(dict(driver_R=float(driver),TG_R=float(tg),feedback_R=float(feedback),
                          write_high_over_VDD=float(hi),write_low_over_VDD=float(lo),passed=True))
    csv_file('q7_ratio_bounds_examples.csv',ratio)
    return dict(MOS=14,graph=graph,switch_states=16,
                clocks='masterinput N=CLK/P=CLKB;masterfeedback andslaveinput N=CLKB/P=CLK',
                edge='negative',classroom_setup_ns=.25,classroom_clock_to_Q_ns=.3,
                setup_scope='input TG0.1+Inv1forwardsettling0.15;fullfeedback/analogue characterization not provided',
                inequalities=['RN2>RP1+RTS','RP2>RN1+RTS'],
                analogue_limit='feedback must be weaker than forward master drive through slave TG; no numeric widths given')


def logic8(q1,q2,q3):
    u=int(q1==q2);v=1-u;p=q2&q3;r=v&q3
    return dict(u=u,v=v,p=p,r=r,Y1=q3,Y2=p|r,Y3=int(u==q3))


def q8():
    rows=[]
    for bits in itertools.product((0,1),repeat=3):
        q1,q2,q3=bits;actual=logic8(*bits)
        assert(actual['Y1'],actual['Y2'],actual['Y3'])==(q3,q3&(q1|q2),q1^q2^q3)
        rows.append(dict(q1=q1,q2=q2,q3=q3,**actual,passed=True))
    csv_file('q8_truth.csv',rows)
    paths=[('R3','R4','direct',0),('R1','R5','XNOR,INV,AND,OR',1.6),
           ('R2','R5','XNOR,INV,AND,OR',1.6),('R2','R5','AND,OR',1),('R3','R5','AND,OR',1),
           ('R1','R6','XNOR,XNOR',.8),('R2','R6','XNOR,XNOR',.8),('R3','R6','XNOR',.4)]
    timing=[]
    for start,end,gates,delay in paths:
        fixed=.4 if gates=='direct'else delay
        timing.append(dict(launch=start,capture=end,path=gates,original_logic_prop_ns=delay,
                           fixed_logic_prop_ns=fixed,setup_min_period_ns=.4+fixed,
                           required_logic_contamination_ns=.1,
                           conditional_min_equals_printed_prop_hold_pass=(.1+fixed>=.2)))
    assert max(r['setup_min_period_ns']for r in timing)==2
    csv_file('q8_original_repaired_paths.csv',timing)
    # Four aligned cut registers: Ptop,Pbottom,Pu,Pq3. Two separate direct
    # paths need hold buffers, q3->Pq3 and Pq3->R4; two inversions each.
    pipeline_paths=[('stage1','R1/R2','Pbottom','XNOR,INV,AND',1.1),
                    ('stage1','R3','Pbottom','AND',.5),('stage1','R2/R3','Ptop','AND',.5),
                    ('stage1','R1/R2','Pu','XNOR',.4),('stage1','R3','Pq3','INV,INV',.4),
                    ('stage2','Ptop/Pbottom','R5','OR',.5),('stage2','Pu/Pq3','R6','XNOR',.4),
                    ('stage2','Pq3','R4','INV,INV',.4)]
    pipetime=[dict(stage=stage,launch=start,capture=end,path=gates,logic_prop_ns=delay,
                  setup_min_period_ns=round(.4+delay,10),target_period_ns=1.5,
                  conditional_min_equals_printed_prop_hold_pass=(.1+delay>=.2),
                  passed=(.4+delay<=1.5+1e-12))for stage,start,end,gates,delay in pipeline_paths]
    assert all(r['passed']for r in pipetime)and max(r['setup_min_period_ns']for r in pipetime)==1.5
    csv_file('q8_pipeline_paths.csv',pipetime)
    cycle_rows=[]
    for first,second in itertools.product(itertools.product((0,1),repeat=3),repeat=2):
        stored=logic8(*first);incoming=logic8(*second)
        out=(first[2],stored['p']|stored['r'],int(stored['u']==first[2]))
        expected=(first[2],first[2]&(first[0]|first[1]),first[0]^first[1]^first[2])
        assert out==expected
        cycle_rows.append(dict(first_q1=first[0],first_q2=first[1],first_q3=first[2],
                               next_q1=second[0],next_q2=second[1],next_q3=second[2],
                               stored_Ptop=stored['p'],stored_Pbottom=stored['r'],stored_Pu=stored['u'],stored_Pq3=first[2],
                               Y1=out[0],Y2=out[1],Y3=out[2],latency='one additional cycle; all three outputs aligned',passed=True))
    csv_file('q8_pipeline_consecutive_samples.csv',cycle_rows)
    return dict(truth_cases=8,original_paths=len(paths),pipeline_paths=len(pipeline_paths),consecutive_sample_cases=64,
                original_hold_failure='direct R3->R4:0.1<0.2ns;period increase doesnotfix',
                hold_buffer_requirements='logic_contam>=0.1ns andlogicprop<=1.6ns;2printed0.2nsINV used,minimumdelay conditional',
                alternative='low-level transparent lockup latch;timingproperties unspecified,conditions given in solution',
                original_repaired_period_ns=2,original_repaired_MHz=500,printed_multiplier='4/3',
                target_period_ns=1.5,pipeline_MHz=1000/1.5,new_registers=['Ptop','Pbottom','Pu','Pq3'],
                inserted_hold_buffers='2INV on q3->Pq3 and2INV on Pq3->R4, separate branches',
                added_latency_cycles=1,all_outputs_aligned=True,
                no_unconditional_hold_claim_from_propagation=True)


def main():
    result=dict(exam='EE3032 Fall2018 final',status='PASS',method='ideal MOS/Boolean graphs;ratioed contention checks;analytical RC,leak andtiming;no processsimulation',
                Q2=q2(),Q3=q3(),Q4=q4(),Q5=q5(),Q6=q6(),Q7=q7(),Q8=q8())
    (HERE/'logic_timing_verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('PASS: domino8;complex16;NP128;20MOSlayout16;register16;pipeline64 consecutive sample pairs and all timing/RC bounds.')


if __name__=='__main__':main()
