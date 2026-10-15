"""2012-archive midterm: independent analytical and ideal-switch verification.

Standard library only. Elmore values are first moments of the complete final
ON-resistor graph, not measured 10--90 edge times. The dual-Vt delay example is
explicitly conditional; no absent process characterization is invented.
"""
from pathlib import Path
from fractions import Fraction as F
import csv
import itertools
import json

HERE=Path(__file__).resolve().parent
def mos(name,kind,drain,gate,source,vt='L'):
    return dict(name=name,kind=kind,drain=drain,gate=gate,source=source,
                body='VDD'if kind=='P'else'VSS',vt=vt)
def inv(prefix,out,gate,vt='L'):
    return[mos(prefix+'P','P',out,gate,'VDD',vt),mos(prefix+'N','N',out,gate,'VSS',vt)]
def adjacency(graph,values,extra=()):
    edges={}
    for m in graph:
        assert m['body']==('VDD'if m['kind']=='P'else'VSS')
        if (not values[m['gate']])if m['kind']=='P'else values[m['gate']]:
            a,b=m['drain'],m['source'];edges.setdefault(a,[]).append((b,m['name']));edges.setdefault(b,[]).append((a,m['name']))
    for a,b,name in extra:
        edges.setdefault(a,[]).append((b,name));edges.setdefault(b,[]).append((a,name))
    return edges
def path(graph,values,start,end,extra=()):
    edges=adjacency(graph,values,extra);queue=[(start,[])];seen={start}
    for node,route in queue:
        if node==end:return route
        for other,name in edges.get(node,[]):
            if other not in seen:seen.add(other);queue.append((other,route+[name]))
    return None
def rail(graph,values,node,extra=()):
    hi,lo=path(graph,values,node,'VDD',extra),path(graph,values,node,'VSS',extra)
    assert (hi is None)!=(lo is None),(node,values,hi,lo)
    return (int(hi is not None),hi or [],lo or [])
def export(name,rows):
    with(HERE/name).open('w',encoding='utf-8',newline='')as fp:
        writer=csv.DictWriter(fp,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def majority_graph():
    return[mos('P1','P','n1','Xb','VDD'),mos('P2','P','n1','Yb','VDD'),mos('P3','P','f','Zb','n1'),
           mos('P4','P','n2','Xb','VDD'),mos('P5','P','f','Yb','n2'),
           mos('N1','N','f','Zb','n3'),mos('N2','N','n3','Xb','VSS'),mos('N3','N','n3','Yb','VSS'),
           mos('N4','N','f','Yb','n4'),mos('N5','N','n4','Xb','VSS')]

def solve(matrix,rhs):
    a=[list(row)+[v]for row,v in zip(matrix,rhs)];n=len(a)
    for k in range(n):
        pivot=next(i for i in range(k,n)if a[i][k]);a[k],a[pivot]=a[pivot],a[k]
        scale=a[k][k];a[k]=[v/scale for v in a[k]]
        for i in range(n):
            if i!=k:
                scale=a[i][k];a[i]=[v-scale*w for v,w in zip(a[i],a[k])]
    return[row[-1]for row in a]

def moments(graph,values,root,rn,rp):
    edges=adjacency(graph,values);nodes={'f'};queue=['f']
    for node in queue:
        for other,_ in edges.get(node,[]):
            if other not in nodes:nodes.add(other);queue.append(other)
    assert root in nodes and ('VSS'if root=='VDD'else'VDD')not in nodes
    unknown=sorted(nodes-{root});index={node:i for i,node in enumerate(unknown)}
    g=[[F(0)for _ in unknown]for _ in unknown]
    for m in graph:
        if not any(name==m['name']for _,name in edges.get(m['drain'],[])):continue
        a,b=m['drain'],m['source'];res=rp if m['kind']=='P'else rn;conductance=1/res
        if a in index:g[index[a]][index[a]]+=conductance
        if b in index:g[index[b]][index[b]]+=conductance
        if a in index and b in index:g[index[a]][index[b]]-=conductance;g[index[b]][index[a]]-=conductance
    weights={}
    for capnode in('n1','n2','n3','n4','f'):
        if capnode not in index:weights[capnode]=F(0);continue
        rhs=[F(int(node==capnode))for node in unknown]
        weights[capnode]=solve(g,rhs)[index['f']]
    return weights

def q2():
    graph=majority_graph();rows=[];rc=[]
    allowed={'010','100','110','000','101','111'}
    for x,y,z in itertools.product((0,1),repeat=3):
        vv=dict(VDD=1,VSS=0,Xb=1-x,Yb=1-y,Zb=1-z);out,hi,lo=rail(graph,vv,'f')
        assert out==int(x+y+z>=2)
        bits=f'{x}{y}{z}';rows.append(dict(X=x,Y=y,Z=z,f=out,allowed=bits in allowed,high_path=';'.join(hi),low_path=';'.join(lo),passed=True))
        if bits not in allowed:continue
        for rn,rp in((F(1),F(3)),(F(2),F(5))):
            weights=moments(graph,vv,'VDD'if out else'VSS',rn,rp)
            scale=rp if out else rn;normalized={k:v/scale for k,v in weights.items()}
            if rn==1:reference=normalized
            else:assert normalized==reference
        ccoef=sum(reference[k]for k in('n1','n2','n3','n4'));ocoef=reference['f']
        assert(ccoef,ocoef)==((F(5,7),F(6,7))if bits in('000','111')else(F(3),F(2)))
        rc.append(dict(X=x,Y=y,Z=z,edge='rise'if out else'fall',R_unit='Rp'if out else'Rn',
                       C1_weight=str(reference['n1']),C2_weight=str(reference['n2']),C3_weight=str(reference['n3']),C4_weight=str(reference['n4']),
                       C_coefficient=str(ccoef),Cout_coefficient=str(ocoef),model='complete final ON graph;first moment;all connected cap initial errors equal',passed=True))
    export('q2_majority_truth.csv',rows);export('q2_elmore_coefficients.csv',rc)
    # Both worst moments are physically attained on the allowed X-only
    # transition010<->110: the attached internal caps have full initial error.
    export('q2_worst_transitions.csv',[
        dict(old='010',new='110',changing_input='X rise',edge='rise',series_devices='P4,P5',main_internal_cap='C2',attached_other_network_cap='C3 viaN1',first_moment='Rp*(3*C+2*Cout)',passed=True),
        dict(old='110',new='010',changing_input='X fall',edge='fall',series_devices='N1,N2',main_internal_cap='C3',attached_other_network_cap='C2 viaP5',first_moment='Rn*(3*C+2*Cout)',passed=True)])
    return dict(MOS=10,graph=graph,truth_cases=8,allowed_states=sorted(allowed),elmore_states=6,
                function='XY+XZ+YZ',worst_rise_first_moment='Rp*(3*C+2*Cout)',worst_fall_first_moment='Rn*(3*C+2*Cout)',
                attainable_transition='010<->110',student_omission='attached C3 during rise and C2 during fall',
                time_convention='Elmore first moment;2.2tau is single-pole10–90 estimate only, not exact multipole edge',
                internal_power='f*VDD*sum(alpha01_i*C_i*Vi);i1..4 only;alpha01charging probability;excludeCout',no_process_measurement=True)

def gate2(prefix,out,a,b,kind,vt='L'):
    if kind=='nand':return[mos(prefix+'P1','P',out,a,'VDD',vt),mos(prefix+'P2','P',out,b,'VDD',vt),
                           mos(prefix+'N1','N',out,a,prefix+'m',vt),mos(prefix+'N2','N',prefix+'m',b,'VSS',vt)]
    return[mos(prefix+'P1','P',prefix+'m',a,'VDD',vt),mos(prefix+'P2','P',out,b,prefix+'m',vt),
           mos(prefix+'N1','N',out,a,'VSS',vt),mos(prefix+'N2','N',out,b,'VSS',vt)]
def dualvt_graph(short_branch_high=True):
    graph=gate2('A','a','I1','I2','nand')+gate2('B','b','I0','a','nor')+gate2('C','c','b','I3','nor')+inv('D','O0','c')
    graph+=gate2('E','e','I3','I4','nor','H')+inv('F','v','I5','H')+gate2('G','O1','e','v','nand','H')
    if short_branch_high:
        for m in graph:
            if m['name']in('BN1','CN2'):m['vt']='H'
    return graph
def q3():
    graph=dualvt_graph();assert len(graph)==24 and sum(m['vt']=='H'for m in graph)==12
    rows=[]
    for bits in itertools.product((0,1),repeat=6):
        i0,i1,i2,i3,i4,i5=bits;a=1-(i1&i2);b=1-(i0|a);c=1-(b|i3);e=1-(i3|i4);v=1-i5
        vv=dict(VDD=1,VSS=0,**dict(zip(('I0','I1','I2','I3','I4','I5'),bits)),a=a,b=b,c=c,e=e,v=v)
        o0=b|i3;o1=1-(e&v)
        for node,expected in(('a',a),('b',b),('c',c),('e',e),('v',v),('O0',o0),('O1',o1)):
            assert rail(graph,vv,node)[0]==expected
        assert o0==((1-i0)&i1&i2)|i3 and o1==(i3|i4|i5)
        rows.append(dict(**dict(zip(('I0','I1','I2','I3','I4','I5'),bits)),a=a,b=b,O0=o0,O1=o1,passed=True))
    export('q3_logic_truth.csv',rows);export('q3_conditional_vt_netlist.csv',graph)
    # A declared educational gate-delay example: INV2,NAND/NOR3,OR5.
    # Original problem supplies no high-Vt scale; test both admissible and
    # inadmissible scales to reject any unconditional no-speed-loss claim.
    delay=[]
    for rho in(F(1),F(3,2),F(11,6),F(2)):
        lower=max(6*rho,5*rho);pass_slack=lower<=11
        assert pass_slack==(rho<=F(11,6))
        delay.append(dict(high_over_low_delay=str(rho),low_critical_delay_RC=11,high_O1_worst_RC=float(lower),
                          no_speed_loss=pass_slack,scope='illustrative homogeneous gate scale, student normalized delay model;not processdata',passed=True))
    export('q3_slack_examples.csv',delay)
    return dict(MOS=24,graph=graph,truth_cases=64,marked_low=12,marked_high=12,
                outputs=['O0=NOT(I0)*I1*I2+I3','O1=I3+I4+I5'],
                conditional_marking='O1tenMOS high;BN1(I0parallel nMOS),CN2(I3parallel nMOS) high only if own short paths meet slack;other12low',
                student_marking='upper14low/lower10high;conservative;no process delay data;not a proven global optimum',
                symbolic_constraints=['max(dNOR_H+dNAND_H,dINV_H+dNAND_H)<=dNAND_L+2*dNOR_L+dINV_L','I0 andI3high-nMOS shortpath delays<=same low critical bound'],
                optimum_limit='unique leakage optimum cannot be established without high/low device delays,loading,leakweights/inputdistribution;marking has explicit eligibility conditions',
                illustrative_uniform_scale_bound='rho<=11/6 forO1cone only;short branch bounds separate')

def region(g,a,b,vt):
    s,d=min(a,b),max(a,b);vgs=g-s;vds=d-s
    if vgs<=vt:return 'cutoff'
    if vds>vgs-vt:return 'saturation'
    if vds==vgs-vt:return 'boundary'
    return 'linear'
def q4():
    vdd,vt=F(18,10),F(4,10);z=vdd-vt;y=vdd-2*vt
    assert(z,y)==(F(14,10),F(1))
    export('q4_levels.csv',[dict(X_V=0,gate_degraded_V=0,Y_V=0,Z_V=0,scope='initialized low;constantVT;no bodyeffect',passed=True),
                            dict(X_V=1.8,gate_degraded_V=1.4,Y_V=1,Z_V=1.4,scope='settled high;constantVT;no bodyeffect',passed=True)])
    rows=[]
    for name,g,a,b in(('m1',vdd,F(18,10),F(5,10)),('m1',vdd,F(8,10),F(2,10)),
                       ('m2',vdd,F(12,10),F(4,10)),('m3',vdd,F(10,10),F(4,10)),
                       ('m4',vdd,F(9,10),F(4,10)),('m5',vdd,F(8,10),F(4,10)),('m6',vdd,F(7,10),F(4,10))):
        r=region(g,a,b,vt);assert r==('saturation'if name=='m1'and a==vdd else'linear')
        rows.append(dict(device=name,gate_V=float(g),terminal_a_V=float(a),terminal_b_V=float(b),region=r,
                         scope='admissible bias example;not simulated waveform or measured transition',passed=True))
    export('q4_region_examples.csv',rows)
    # Exact bound independent of unknown widths: downstream terminals<=1.4.
    count=0
    for a,b in itertools.product((F(i,10)for i in range(15)),repeat=2):
        assert region(vdd,a,b,vt)!='saturation';count+=1
    return dict(VDD=1.8,VT=0.4,high_Y=1,high_Z=1.4,low_Y=0,low_Z=0,
                source_topology='Yupper pass takesX data and gate fromaVDD-gated nMOS passingX;ZsixnMOSallgatesVDD',
                m1='can saturation orlinear dependingbias;ideal abrupthigh phase is saturation before cutoff',
                m2_to_m6='linear while conducting, possible saturation boundary/cutoff atlimit;never interior saturation withbothends<=VDD-VT',
                downstream_bound_cases=count,no_process_measurement=True,
                waveform_scope='settled levels and qualitative rise;edge time/cap values unspecified;bodyeffect raisesVT andwouldlowerlevels')
def q5():
    widths=[]
    for alpha in(F(1),F(3)):
        delay=(1+alpha)*(1+3/alpha);assert delay==8
        widths.append(dict(alpha=float(alpha),first_two_delay_over_RC=float(delay),first_two_clocked_cap_over_C=float(2*(1+alpha)),
                           chosen_for_min_power=alpha==1,passed=True))
    export('q5_alpha_candidates.csv',widths)
    return dict(mu_n_over_mu_p=3,delay='T/RC=(1+alpha)*(1+3/alpha)',required_T_over_RC=8,
                feasible_alpha=[1,3],minimum_power_alpha=1,
                switching_power='2*alpha01*f*(1+alpha)*C*VDD^2;two interstage gates;ignoreunspecifieddiffusion/wirecaps',
                chosen_power_ratio_to_alpha3=.5,third_external_load='CL doesnot enter bracketed first-two-stage delay/power;thirdstage gatecap does')

def dual(expr):
    return expr if isinstance(expr,str)else('P'if expr[0]=='S'else'S',*[dual(x)for x in expr[1:]])
def network(expr,out,root,kind,prefix):
    devices=[];node_count=0
    def build(e,a,b):
        nonlocal node_count
        if isinstance(e,str):devices.append(mos(prefix+str(len(devices)+1),kind,a,e,b));return
        children=e[1:]
        if e[0]=='P':
            for child in children:build(child,a,b)
        else:
            prev=a
            for j,child in enumerate(children):
                if j==len(children)-1:nxt=b
                else:node_count+=1;nxt=prefix+'j'+str(node_count)
                build(child,prev,nxt);prev=nxt
    build(expr,out,root);return devices
def complementary(expr,out,prefix):
    return network(expr,out,'VSS','N',prefix+'N')+network(dual(expr),out,'VDD','P',prefix+'P')
def q6a_graph():return complementary(('S','w',('P','x','y','z')),'f','A')
def q6b_graph():return inv('IX','xb','x')+inv('IY','yb','y')+complementary(('P',('S','x','y'),('S','xb','yb')),'f','B')
def tgxor_graph():
    return inv('IX','xb','x')+inv('IY','yb','y')+[
        mos('TY_P','P','f','x','y'),mos('TY_N','N','f','xb','y'),mos('TYB_P','P','f','xb','yb'),mos('TYB_N','N','f','x','yb')]
def q6():
    a=q6a_graph();b=q6b_graph();tg=tgxor_graph();rowsa=[];rowsb=[]
    assert(len(a),len(b),len(tg))==(8,12,8)
    for w,x,y,z in itertools.product((0,1),repeat=4):
        vv=dict(VDD=1,VSS=0,w=w,x=x,y=y,z=z);actual=rail(a,vv,'f')[0];assert actual==int(not(w and(x or y or z)))
        rowsa.append(dict(w=w,x=x,y=y,z=z,f=actual,passed=True))
    for x,y in itertools.product((0,1),repeat=2):
        vv=dict(VDD=1,VSS=0,x=x,y=y,xb=1-x,yb=1-y)
        pad=[(k,'VDD'if vv[k]else'VSS','input'+k)for k in('x','y')]
        actual=rail(b,vv,'f')[0];alternative=rail(tg,vv,'f',pad)[0]
        assert actual==alternative==(x^y)
        # Student's10T: k=NAND(x,y), f=NOT[k+xy], identically zero.
        k=1-(x&y);student=1-int(k or(x and y));assert student==0
        rowsb.append(dict(x=x,y=y,f=actual,TG_f=alternative,student_10T_f=student,student_wrong=(student!=actual),passed=True))
    export('q6a_logic.csv',rowsa);export('q6b_logic_and_reference.csv',rowsb)
    export('q6a_MOS.csv',a);export('q6b_complementary_MOS.csv',b);export('q6b_TG_alternative_MOS.csv',tg)
    return dict(Q6a=dict(MOS=8,graph=a,cases=16),Q6b=dict(MOS=12,graph=b,cases=4),TG_alternative=dict(MOS=8,graph=tg),
                minimum_scope='8forQ6a,12forQ6b inconventional fullycomplementary CMOSwithgeneratedliteralcomplements;8TGXORifbroader staticpasslogicallowed',
                student_error='10T NAND(x,y) feedscompound PDNk+xy ->constant0;fails01and10')
def adder_graph():
    carry=('P',('S','x','y'),('S','c',('P','x','y')))
    odd=('P',('S','cb',('P','x','y','c')),('S','x','y','c'))
    return complementary(carry,'cb','C')+inv('CI','cout','cb')+complementary(odd,'sb','S')+inv('SI','sout','sb')
def q7():
    graph=adder_graph();assert len(graph)==28;rows=[]
    for x,y,c in itertools.product((0,1),repeat=3):
        n=x+y+c;co=int(n>=2);s=n%2;vv=dict(VDD=1,VSS=0,x=x,y=y,c=c,cb=1-co,sb=1-s)
        for node,expected in(('cb',1-co),('cout',co),('sb',1-s),('sout',s)):
            assert rail(graph,vv,node)[0]==expected
        assert s+2*co==n
        rows.append(dict(x=x,y=y,cin=c,sout=s,cout=co,passed=True))
    export('q7_full_adder_truth.csv',rows);export('q7_full_adder_MOS.csv',graph)
    return dict(MOS=28,graph=graph,cases=8,carry='xy+c(x+y)',sum='xXORyXORc=cb(x+y+c)+xyc',
                internal='cb=NOTcarry,sb=NOTsum;twooutputinverters;providedinternalcbavoidsinputcomplementgeneration',
                source_comparison='studenttruth/SOPcorrect;complementliteral PDNs can produce trueoutputs whencomplementsprovided, but localinputINV generators omitted;complete28MOS usesonlytrueprimaryinputs')
def main():
    data=dict(year=2012,exam='midterm',year_basis='archivefolder;printeddateabsent;matchingreferencephotosduplicatedunder2013',
              status='PASS',method='ideal MOSrailgraphs;complete resistor-matrix firstmoments;analyticalslack/region/sizing;no processsimulation',
              Q2=q2(),Q3=q3(),Q4=q4(),Q5=q5(),Q6=q6(),Q7=q7())
    (HERE/'logic_timing_verification.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print('PASS: majority8/fullRC6;dualVt64;passregion225;alpha2;CMOS16+4;adder8/28MOS.')
if __name__=='__main__':main()
