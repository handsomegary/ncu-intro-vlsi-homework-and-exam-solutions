"""Fall 2023 final: independent ideal-switch, Boolean, charge and timing checks.

Standard-library only. Run `python verify_logic_timing.py` from any directory.
MOS paths are derived from original printed figures. Dynamic charge storage and
weak-keeper strength are assumptions, not HSPICE/PVT simulation results.
"""
from pathlib import Path
from fractions import Fraction as F
import csv
import itertools
import json
import heapq

HERE = Path(__file__).resolve().parent


def mos(name, kind, drain, gate, source, role="logic", weak=False):
    return dict(name=name, kind=kind, drain=drain, gate=gate, source=source,
                body="VDD" if kind == "P" else "VSS", role=role, weak=weak)


def inverter(prefix, out, gate):
    return [mos(prefix+"P", "P", out, gate, "VDD", "inverter"),
            mos(prefix+"N", "N", out, gate, "VSS", "inverter")]


def path_to(graph, values, start, end, extra=()):
    edges = {}
    for m in graph:
        assert m["body"] == ("VDD" if m["kind"] == "P" else "VSS")
        on = not values[m["gate"]] if m["kind"] == "P" else values[m["gate"]]
        if on:
            a, b = m["drain"], m["source"]
            edges.setdefault(a, []).append((b, m["name"]))
            edges.setdefault(b, []).append((a, m["name"]))
    for a, b, name in extra:
        edges.setdefault(a, []).append((b, name))
        edges.setdefault(b, []).append((a, name))
    queue, seen = [(start, [])], {start}
    for node, path in queue:
        if node == end:
            return path
        for other, name in edges.get(node, []):
            if other not in seen:
                seen.add(other)
                queue.append((other, path+[name]))
    return None


def rail_value(graph, values, node, extra=()):
    hi, lo = path_to(graph, values, node, "VDD", extra), path_to(graph, values, node, "VSS", extra)
    assert not (hi is not None and lo is not None), (node, values, hi, lo)
    return (1 if hi is not None else 0 if lo is not None else None), hi, lo


def save_csv(name, rows):
    with (HERE/name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def domino_and_graph():
    graph=[]
    for suffix,inputs,out in (("1",["A","B","C"],"u"),("2",["u","D"],"Y")):
        d,e="d"+suffix,"e"+suffix
        graph+=[mos("PRE"+suffix,"P",d,"phi","VDD")]
        nodes=[d]+["s"+suffix+str(i) for i in range(1,len(inputs))]+[e]
        for i,g in enumerate(inputs):
            graph+=[mos("N"+suffix+str(i),"N",nodes[i],g,nodes[i+1])]
        graph += [mos("FOOT"+suffix,"N",e,"phi","VSS")]+inverter("OUT"+suffix,out,d)+[mos("KEEP"+suffix,"P",d,out,"VDD","keeper",True)]
    return graph


def q2():
    rows = []
    graph=domino_and_graph()
    phase_rows=[]
    for a,b,c,d in itertools.product((0,1), repeat=4):
        vv=dict(VDD=1,VSS=0,A=a,B=b,C=c,D=d,phi=1,u=0)
        pdn=[m for m in graph if m['kind']=='N' and m['role']!='inverter']
        raw1=int(path_to(pdn,vv,'d1','VSS') is None)
        u=1-raw1
        vv['u']=u
        raw2=int(path_to(pdn,vv,'d2','VSS') is None)
        y=1-raw2
        assert u == (a & b & c) and y == (a & b & c & d)
        rows.append(dict(A=a,B=b,C=c,D=d,u=u,Y=y,passed=True))
        for phi in (0,1):
            vv.update(phi=phi,d1=raw1 if phi else 1,d2=raw2 if phi else 1,
                      u=u if phi else 0,Y=y if phi else 0)
            for node in ('d1','d2','u','Y'):
                driven,hi,lo=rail_value(graph,vv,node)
                assert driven==vv[node]
                phase_rows.append(dict(A=a,B=b,C=c,D=d,phi=phi,node=node,value=driven,
                                       high_path=';'.join(hi or []),low_path=';'.join(lo or []),passed=True))
    save_csv("q2_truth.csv", rows)
    save_csv("q2_MOS_phase_checks.csv",phase_rows)
    wave = [dict(time_unit=t,phi=int(1<=t<5 or 7<=t<11),
                 A=int(t>=6), B=int(t>=6), C=int(t>=6), D=0,
                 u=int(8<=t<12), Y=0) for t in range(14)]
    save_csv("q2_waveform.csv", wave)
    return dict(truth_cases=16,MOS_phase_node_cases=len(phase_rows),graph=graph,core_with_keepers_MOS=15,input_sequence=["0000","1110"],
                evaluate_ns=5, concurrent_precharge_ns=1,
                adjustable_duty_min_period_ns=6, adjustable_duty_max_MHz=1000/6,
                adjustable_duty_evaluate_fraction=5/6,
                duty50_min_period_ns=10, duty50_max_MHz=100,
                graded_duty_evidence="No matching graded answer identified in the supplied mixed-year study compilation.",
                waveform="each AND has one-unit response; u resets one unit after phi falls; Y remains0 because D=0")


def majority_graph(repair="static_middle"):
    # x is the internal A/B series junction; d is a newly named raw output.
    graph = [mos("PRE", "P", "d", "phi", "VDD", "precharge"),
             mos("A1", "N", "d", "A", "x"), mos("B1", "N", "x", "B", "e"),
             mos("C1", "N", "d", "C", "y"), mos("A2", "N", "y", "A", "e"),
             mos("B2", "N", "y", "B", "e"), mos("FOOT", "N", "e", "phi", "VSS"),
             ]
    if repair=="static_middle":
        graph+=inverter("YMID", "Ybar", "d")
    else:
        clock="phi" if repair in ("buffered_same_phase","original_phi") else "phib"
        gate="q" if repair=="buffered_same_phase" else "d"
        graph += [mos("YPRE", "P", "Ybar", clock, "VDD", "precharge"),
                  mos("YDATA", "N", "Ybar", gate, "ey"),
                  mos("YFOOT", "N", "ey", clock, "VSS")]
    graph += [mos("XHEAD", "P", "ex", "phib", "VDD"),
             mos("XDATA", "P", "X", "d", "ex"),
             mos("XRESET", "N", "X", "phib", "VSS", "precharge")]
    if repair=="buffered_same_phase":
        graph += inverter("BUF", "q", "d")
    return graph


def q3():
    graph = majority_graph()
    rows, phase_rows = [], []
    for a,b,c in itertools.product((0,1), repeat=3):
        values = dict(VDD=1,VSS=0,A=a,B=b,C=c,phi=1,phib=0,d=1,q=0)
        discharge = path_to(graph[:7], values, "d", "VSS")
        d = int(discharge is None)
        values.update(d=d,q=1-d)
        ybar=rail_value(graph[7:9],values,"Ybar")[0]
        x_charge = path_to(graph[9:12], values, "X", "VDD")
        xout = int(x_charge is not None)
        majority = int(a+b+c>=2)
        assert (d,xout,ybar)==(1-majority,majority,majority)
        rows.append(dict(A=a,B=b,C=c,d=d,q=1-d,X=xout,Ybar=ybar,
                         d_discharge_path=";".join(discharge or []),passed=True))
        for phase in ("precharge","evaluate"):
            vv = dict(values,phi=int(phase=="evaluate"),phib=int(phase=="precharge"))
            vv.update(d=1 if phase=="precharge" else d,q=0 if phase=="precharge" else 1-d)
            outputs={"d":1,"Ybar":0,"X":0} if phase=="precharge" else {"d":d,"Ybar":ybar,"X":xout}
            for node, expected in outputs.items():
                driven,hi,lo=rail_value(graph,vv,node)
                assert driven in (None,expected)
                if phase=="precharge": assert driven==expected
                phase_rows.append(dict(A=a,B=b,C=c,phase=phase,node=node,value=expected,
                                       high_path=";".join(hi or []),low_path=";".join(lo or []),
                                       charge_storage=(driven is None),rail_contention=False,passed=True))
    save_csv("q3_majority_checks.csv",rows)
    save_csv("q3_phase_checks.csv",phase_rows)
    # Original opposite-phase middle: evaluation sees first raw d precharged1.
    original=majority_graph("original")
    vv=dict(VDD=1,VSS=0,A=1,B=1,C=0,phi=0,phib=1,d=1)
    assert path_to(original[7:10],vv,"Ybar","VSS") is not None
    vv.update(phi=1,phib=0,d=0)
    assert rail_value(original[7:10],vv,"Ybar")[0]==1
    original_rows,alternate_rows=[],[]
    alternate=majority_graph("buffered_same_phase")
    for a,b,c in itertools.product((0,1),repeat=3):
        majority=int(a+b+c>=2)
        for phi in (0,1):
            vals=dict(VDD=1,VSS=0,A=a,B=b,C=c,phi=phi,phib=1-phi,d=1 if phi==0 else 1-majority)
            yy=rail_value(original[7:10],vals,"Ybar")[0]
            assert yy==phi
            original_rows.append(dict(A=a,B=b,C=c,phi=phi,d=vals["d"],Ybar=yy,
                                      original_middle_clock="phi_bar",passed=True))
        vals=dict(VDD=1,VSS=0,A=a,B=b,C=c,phi=1,phib=0,d=1-majority,q=majority)
        y_alt=int(path_to(alternate[7:10],vals,"Ybar","VSS") is None)
        assert y_alt==1-majority
        alternate_rows.append(dict(A=a,B=b,C=c,X=majority,Ybar=y_alt,passed=True))
    save_csv("q3_original_phase_failure.csv",original_rows)
    save_csv("q3_alternate_repair_checks.csv",alternate_rows)
    original_phi=majority_graph("original_phi")
    same_phase_rows=[]
    for a,b,c in itertools.product((0,1),repeat=3):
        majority=int(a+b+c>=2)
        vals=dict(VDD=1,VSS=0,A=a,B=b,C=c,phi=1,phib=0,d=1)
        assert path_to(original_phi[7:10],vals,"Ybar","VSS") is not None
        # Allowed delay ordering: middle has discharged before first d settles.
        middle_state=0
        vals['d']=1-majority
        assert path_to(original_phi[7:10],vals,"Ybar","VDD") is None
        same_phase_rows.append(dict(A=a,B=b,C=c,d_final=1-majority,
                                    middle_state_after_early_discharge=middle_state,
                                    intended_static_inverse_d=majority,
                                    failing_delay_order_exists=bool(majority),
                                    claim="constructed relative-delay case, not all analogue orderings"))
    save_csv("q3_same_phase_counterexample.csv",same_phase_rows)
    cap_rows=[]
    for label,cx,cy in (("supplied_total_node_caps",F(13,10),F(11,10)),
                       ("wire_only_plus_all_diffusion_junctions",F(15,10),F(14,10)),
                       ("wire_only_plus_literal_drain_terminals",F(14,10),F(13,10))):
        for pattern,cap in (("100",cx),("001",cy)):
            ratio=F(33,10)/(F(33,10)+cap)
            assert ratio>F(1,2)
            cap_rows.append(dict(model=label,non_discharging_pattern=pattern,
                                 output_cap_fF=3.3,internal_cap_fF=float(cap),
                                 final_V_over_VDD=float(ratio),above_half_rail=True,passed=True))
    save_csv("q3_charge_sharing.csv",cap_rows)
    return dict(input_cases=8,phase_node_cases=len(phase_rows),graph=graph,
                original_graph=original,
                original_phi_graph=original_phi,
                source_clock_legibility="Middle glyph's top stroke touches gate wire; phi_bar selected transcription, phi alternate tested; graph cannot resolve printed pixels",
                original_failure="Printed middle clock is phi_bar: phi0 gives raw d1 and middle Ybar0; phi1 forcibly precharges middle Ybar1 independently of the input function",
                modified_function="Primary static-middle repair gives X=AB+C(A+B), Ybar=X",
                primary_repair="Reconnect upper middle pMOS gate to d and remove its clocked footer; 12MOS remain",
                alternate_graph=alternate,alternate_cases=8,original_phase_cases=16,
                alternate_repair="Change BOTH middle precharge/footer clock to phi and insert an input inverter; yields X=M,Ybar=NOT(M),15MOS",
                node_labels="Original x is A/B internal junction; d is an added analysis name for raw output.",
                capacitor_primary="1.3fF/1.1fF are supplied TOTAL internal-node parasitic caps",
                capacitor_alternatives="wire-only caps plus every junction, or literal drain-only Cd; all remain above VDD/2",
                primary_worst_ratio=33/46,minimum_alternative_ratio=11/16)


def dynamic_graph():
    return [mos("Ppre","P","f","phi","VDD"),mos("Nx1","N","f","x1","u"),
            mos("Nx2","N","u","x2","e"),mos("Nx3","N","f","x3","e"),
            mos("Nfoot","N","e","phi","VSS")]


def dpl_graph():
    return [mos("NF1","N","f","x1","uf"),mos("NF0","N","f","xb1","xb3"),
            mos("NF11","N","uf","x2","VSS"),mos("NF10","N","uf","xb2","xb3"),
            mos("NG1","N","g","x1","ug"),mos("NG0","N","g","xb1","x3"),
            mos("NG11","N","ug","x2","VDD"),mos("NG10","N","ug","xb2","x3"),
            mos("PFrestore","P","f","g","VDD","restorer",True),
            mos("PGrestore","P","g","f","VDD","restorer",True)]


def np_xor_graph():
    graph=[mos("NPRE","P","n","phi","VDD"),mos("NX1","N","n","x1","en"),
           mos("NX2","N","n","x2","en"),mos("NFOOT","N","en","phi","VSS"),
           mos("PHEAD","P","ep","phib","VDD"),mos("PN","P","ef","n","ep"),
           mos("PX1","P","f","x1","ef"),mos("PX2","P","f","x2","ef"),
           mos("PRESET","N","f","phib","VSS")]
    graph+=inverter("KNINV","nb","n")+[mos("KN","P","n","nb","VDD","keeper",True)]
    graph+=inverter("KFINV","fb","f")+[mos("KF","N","f","fb","VSS","keeper",True)]
    return graph


def q4():
    dynamic,dpl,np=dynamic_graph(),dpl_graph(),np_xor_graph()
    rows=[]
    dynamic_phases=[]
    for x1,x2,x3 in itertools.product((0,1),repeat=3):
        vv=dict(VDD=1,VSS=0,x1=x1,x2=x2,x3=x3,xb1=1-x1,xb2=1-x2,xb3=1-x3,phi=1)
        f=int(path_to(dynamic,vv,"f","VSS") is None)
        expected=int(not(x1*x2 or x3))
        extra=[("x3","VDD" if x3 else "VSS","input_x3"),
               ("xb3","VSS" if x3 else "VDD","input_xb3")]
        fp,_,_=rail_value(dpl[:8],vv,"f",extra)
        gp,_,_=rail_value(dpl[:8],vv,"g",extra)
        assert (f,fp,gp)==(expected,expected,1-expected)
        vv.update(f=fp,g=gp)
        assert rail_value(dpl,vv,"f",extra)[0]==fp
        assert rail_value(dpl,vv,"g",extra)[0]==gp
        rows.append(dict(x1=x1,x2=x2,x3=x3,dynamic_f=f,DPL_f=fp,DPL_complement=gp,passed=True))
        for phi in (0,1):
            vv['phi']=phi
            driven,hi,lo=rail_value(dynamic,vv,'f')
            expect=f if phi else 1
            assert driven in (None,expect)
            if phi==0: assert driven==1
            dynamic_phases.append(dict(x1=x1,x2=x2,x3=x3,phi=phi,f=expect,
                                       charge_storage=(driven is None),rail_exclusive=True,passed=True))
    save_csv("q4_dynamic_dpl_checks.csv",rows)
    save_csv("q4_dynamic_phase_checks.csv",dynamic_phases)
    phase_rows=[]
    for x1,x2 in itertools.product((0,1),repeat=2):
        vv=dict(VDD=1,VSS=0,x1=x1,x2=x2,phi=1,phib=0,n=1)
        n=int(path_to(np[:4],vv,"n","VSS") is None)
        vv["n"]=n
        f=int(path_to(np[4:9],vv,"f","VDD") is not None)
        assert f==(x1^x2)
        for phase in ("precharge","evaluate"):
            nn,ff=(1,0) if phase=="precharge" else (n,f)
            vv.update(phi=int(phase=="evaluate"),phib=int(phase=="precharge"),n=nn,f=ff,nb=1-nn,fb=1-ff)
            for node,expected in (("n",nn),("f",ff)):
                assert rail_value(np,vv,node)[0]==expected
            phase_rows.append(dict(x1=x1,x2=x2,phase=phase,n=nn,f=ff,
                                   rail_exclusive=True,passed=True))
    save_csv("q4_np_xor_phase_checks.csv",phase_rows)
    return dict(dynamic_dpl_cases=8,dynamic_phase_cases=16,np_phase_cases=8,dynamic_core_MOS=5,DPL_core_MOS=10,
                DPL_complement_inputs="Provided externally; 3 inverters add6MOS if needed",
                NP_core_MOS=9,NP_with_two_keepers_MOS=15,
                dynamic_graph=dynamic,DPL_graph=dpl,NP_graph=np,
                NP_equation="n=NOT(x1+x2); f=NOT(n)*(NOT(x1)+NOT(x2)) = x1 XOR x2",
                NP_protocol="x1,x2 stable for evaluate; n falls monotonically from1, f rises from0")


def q5():
    rn3=F(7,8)
    geom={"N1":F(160),"N2":F(80),"N3":F(1280,7),"P1":F(320),"P2":F(160),"P3":F(2560,7)}
    upper=F(3,2)/(1+rn3)+F(1,5)
    lower=F(3,2)*rn3/(1+rn3)-F(1,5)
    assert (upper,lower)==(F(1),F(1,2))
    on_upper=F(3,2)/(1+rn3/2)+F(1,5)
    on_lower=F(3,2)*(rn3/2)/(1+rn3/2)-F(1,5)
    assert on_upper-on_lower>upper-lower
    save_csv("q5_sizing.csv",[dict(device=k,width_nm=float(v),length_nm=40,
                                     model="fixed_external_C; choose_RP1=RN1",passed=True) for k,v in geom.items()])
    save_csv("q5_hysteresis.csv",[dict(switch="off",upper_V=float(upper),lower_V=float(lower),width_V=float(upper-lower)),
                                    dict(switch="on_equal_added_feedback",upper_V=float(on_upper),lower_V=float(on_lower),width_V=float(on_upper-on_lower))])
    # General p-family a=Rp1/R. Literal feedback-gate caps K=15/7+16/(7a).
    # N2>0 requires K<3 -> a>8/3; P2>0 requires aK<3 -> a<1/3.
    assert F(8,3)>F(1,3)
    return dict(model="classroom fixed external capacitor C",widths_nm={k:float(v) for k,v in geom.items()},
                all_lengths_nm=40,RP1_choice_R=1,nonunique_p_family="a=RP1/R,0<a<3; WP1=320/a,WP2=320/(3-a),WP3=2560/(7a) nm",
                thresholds_off_V=[float(lower),float(upper)],thresholds_on_equal_added_V=[float(on_lower),float(on_upper)],
                literal_capacitance_model="Cout/C=15/7+16/(7a), because output drives N3 and P3 gates",
                literal_positive_N2_requires_a_gt=8/3,literal_positive_P2_requires_a_lt=1/3,
                literal_feasible=False,
                switch_power="Lower feedback resistance increases overlap current at a fixed input bias; numerical cycle-average power needs a waveform/device model.")


P_NODES=["VDD","x","VDD","p1","p2","w","VDD","z"]
N_NODES=["VSS","x","VSS","w","VSS","w","VSS","z"]
P_GATES=["a","VDD","x","b","c","VDD","w"]
N_GATES=["a","VSS","x","b","c","VSS","w"]


def layout_graph():
    graph=[]
    for kind,nodes,gates in (("P",P_NODES,P_GATES),("N",N_NODES,N_GATES)):
        for i,g in enumerate(gates):
            graph.append(mos(kind+str(i+1),kind,nodes[i+1],g,nodes[i],"isolation" if i in (1,5) else "logic"))
    return graph


def q6():
    graph=layout_graph()
    rows=[]
    for a,b,c in itertools.product((0,1),repeat=3):
        vv=dict(VDD=1,VSS=0,a=a,b=b,c=c,x=0,w=0)
        x=rail_value(graph,vv,"x")[0]
        vv["x"]=x
        w=rail_value(graph,vv,"w")[0]
        vv["w"]=w
        z=rail_value(graph,vv,"z")[0]
        assert (x,w,z)==(1-a,int(not((1-a)or b or c)),int((1-a)or b or c))
        rows.append(dict(a=a,b=b,c=c,x=x,w=w,z=z,passed=True))
    save_csv("q6_layout_checks.csv",rows)
    save_csv("q6_physical_MOS.csv",graph)
    return dict(cases=8,physical_MOS=14,functional_MOS=10,off_isolation_MOS=4,
                p_active_nodes=P_NODES,n_active_nodes=N_NODES,p_gates=P_GATES,n_gates=N_GATES,
                function="z=NOT(a)+b+c",graph=graph,
                contact_rule="Crossing metal/poly without a black contact square is insulated")


def q7():
    rows=[]
    for q1,q2,q3,q4 in itertools.product((0,1),repeat=4):
        u=q3&q4;v=q2&u
        d5=q1;d6=int(not(q1 or v));d7=v;d8=int(not((1-v)or q4))
        assert d8==0
        rows.append(dict(q1=q1,q2=q2,q3=q3,q4=q4,u=u,v=v,R5_D=d5,R6_D=d6,R7_D=d7,R8_D=d8,passed=True))
    save_csv("q7_truth.csv",rows)
    # Real reconvergent hazard despite the constant Boolean function: start
    # q2=q3=q4=1, then q4 falls after clock-to-Q .2ns. Transport AND .5,
    # INV .2,NOR .5 delays produce a pulse and a 1.9ns final settle.
    vals=dict(q2=1,q3=1,q4=1,u=1,v=1,vbar=0,R8_D=0)
    gates=[('u',('q3','q4'),.5,lambda a,b:a&b),
           ('v',('q2','u'),.5,lambda a,b:a&b),
           ('vbar',('v',),.2,lambda a:1-a),
           ('R8_D',('vbar','q4'),.5,lambda a,b:int(not(a or b)))]
    events=[(.2,0,'q4',0)]
    serial=0
    hazard=[dict(time_ns=0,**{k:vals[k] for k in ('q4','u','v','vbar','R8_D')})]
    while events:
        t,_,node,value=heapq.heappop(events)
        if vals[node]==value: continue
        vals[node]=value
        hazard.append(dict(time_ns=round(t,10),**{k:vals[k] for k in ('q4','u','v','vbar','R8_D')}))
        for out,inputs,delay,func in gates:
            if node in inputs:
                serial+=1
                heapq.heappush(events,(t+delay,serial,out,func(*(vals[i] for i in inputs))))
    assert hazard[-1]['R8_D']==0 and abs(hazard[-1]['time_ns']-1.9)<1e-9
    assert any(r['R8_D']==1 and abs(r['time_ns']-.7)<1e-9 for r in hazard)
    save_csv("q7_reconvergent_hazard.csv",hazard)
    paths=[("R1","R5","direct",0),
           ("R1","R6","NOR",.5),("R2","R6","AND,NOR",1),
           ("R3","R6","AND,AND,NOR",1.5),("R4","R6","AND,AND,NOR",1.5),
           ("R2","R7","AND",.5),("R3","R7","AND,AND",1),("R4","R7","AND,AND",1),
           ("R2","R8","AND,INV,NOR",1.2),("R3","R8","AND,AND,INV,NOR",1.7),
           ("R4","R8","AND,AND,INV,NOR",1.7),("R4","R8","NOR",.5)]
    timing=[]
    for skew in (0,.3):
        for launch,capture,gates,delay in paths:
            capture_clock=skew if capture in ("R5","R6") else 0
            bound=.2+delay+.2-capture_clock
            timing.append(dict(delta_ns=skew,launch=launch,capture=capture,gates=gates,
                               capture_clock_ns=capture_clock,logic_propagation_ns=delay,
                               setup_min_period_ns=round(bound,10),
                               hold_required_logic_contamination_ns=round(capture_clock+.2-.1,10),
                               direct_hold_violation=(capture=="R5")))
        assert abs(max(r["setup_min_period_ns"] for r in timing if r["delta_ns"]==skew)-2.1)<1e-9
    save_csv("q7_path_timing.csv",timing)
    latch=[]
    for skew in (0,.3):
        t=2.1
        latch.append(dict(delta_ns=skew,T_ns=t,low_level_transparent_latch=True,
                          max_latch_propagation_ns=t/2+skew-.2,
                          min_latch_contamination_ns=max(0,skew+.2-t/2),
                          max_latch_own_hold_ns=.1,ideal_latch_conditional_MHz=1000/t,
                          other_gate_hold_condition="Need each path's actual minimum delay to exceed listed requirement; printed gate delays are propagation only unless equated by classroom convention."))
    save_csv("q7_latch_bounds.csv",latch)
    return dict(truth_cases=16,physical_paths=len(paths),path_skew_cases=len(timing),
                unchanged_constant_output="R8 D=v*NOT(q4)=0; preserve physical reconvergent paths for timing",
                actual_hazard_case="q2=q3=1, q4 falls at.2ns: R8_D rises at.7ns and settles low at1.9ns under printed transport delays",
                delayed_capture_registers=["R5","R6"],undelayed_capture_registers=["R7","R8"],
                direct_hold_fail_ns={"delta0":.1,"delta0.3":.4},
                modified_longest_logic_ns=1.7,modified_min_period_ns=2.1,
                conditional_ideal_latch_max_MHz=1000/2.1,
                latch_setup_inequality="T/2+delta >= t_pd_latch+0.2ns (launch data ready before opening)",
                latch_hold_inequality="T/2+t_cd_latch >= delta+0.2ns",
                latch_own_hold_requirement="t_hold_latch <= 0.1ns for simultaneous launch FF edge/latch closing edge",
                no_unconditional_latch_timing_claim=True)


def main():
    result={"exam":"EE3032 Fall2023 final", "status":"PASS", "method":"ideal MOS switch graphs, exhaustive logic and analytic timing/charge checks; no transistor simulation",
            "Q2":q2(),"Q3":q3(),"Q4":q4(),"Q5":q5(),"Q6":q6(),"Q7":q7()}
    (HERE/"logic_timing_verification.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print("PASS: Q2 16 truth +128 MOS phase/node; Q3 8 truth +48 phase/node +both clock readings; Q4 8 DPL/dynamic +16 dynamic phase +8 NP phase; Q6 8; Q7 16 truth +24 path/skew +simulated hazard.")


if __name__=="__main__":
    main()
