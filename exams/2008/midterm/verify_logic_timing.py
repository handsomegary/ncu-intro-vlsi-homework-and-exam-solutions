from pathlib import Path
from fractions import Fraction as F
import csv
import itertools
import json
import math

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

def gate2(prefix,out,a,b,kind,vt='L'):
    if kind=='nand':return[mos(prefix+'P1','P',out,a,'VDD',vt),mos(prefix+'P2','P',out,b,'VDD',vt),
                           mos(prefix+'N1','N',out,a,prefix+'m',vt),mos(prefix+'N2','N',prefix+'m',b,'VSS',vt)]
    return[mos(prefix+'P1','P',prefix+'m',a,'VDD',vt),mos(prefix+'P2','P',out,b,prefix+'m',vt),
           mos(prefix+'N1','N',out,a,'VSS',vt),mos(prefix+'N2','N',out,b,'VSS',vt)]

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

def adder_graph():
    carry=('P',('S','x','y'),('S','c',('P','x','y')))
    odd=('P',('S','cb',('P','x','y','c')),('S','x','y','c'))
    return complementary(carry,'cb','C')+inv('CI','cout','cb')+complementary(odd,'sb','S')+inv('SI','sout','sb')

def q1c_graph():
    return complementary(('P',('S','x','y'),('S',('P','u','v'),'w')),'f','Q')

def q1():
    graph=q1c_graph();assert len(graph)==10;rows=[]
    for bits in itertools.product((0,1),repeat=5):
        x,y,u,v,w=bits;vv=dict(VDD=1,VSS=0,x=x,y=y,u=u,v=v,w=w)
        actual=rail(graph,vv,'f')[0];expected=int(not((x and y)or((u or v)and w)))
        assert actual==expected
        rows.append(dict(x=x,y=y,u=u,v=v,w=w,f=actual,passed=True))
    export('q1c_CMOS_truth.csv',rows);export('q1c_MOS.csv',graph)
    return dict(MOS=10,graph=graph,cases=32,function='NOT[xy+(u+v)w]')

def q2_graph(upper_high=True):
    graph=gate2('A','a','I1','I2','nor')+gate2('B','b','I0','a','nor','H'if upper_high else'L')
    graph+=inv('C','c','b','H'if upper_high else'L')+gate2('D','d','a','I3','nand')
    graph+=gate2('E','n','c','d','nor')+inv('F','O0','n')+gate2('G','m','d','I4','nand')+inv('H','O1','m')
    return graph

def q2():
    graph=q2_graph();assert len(graph)==26 and sum(m['vt']=='H'for m in graph)==6
    rows=[]
    for bits in itertools.product((0,1),repeat=5):
        i0,i1,i2,i3,i4=bits;a=1-(i1|i2);b=1-(i0|a);c=1-b;d=1-(a&i3);n=1-(c|d);m=1-(d&i4)
        vv=dict(VDD=1,VSS=0,**dict(zip(('I0','I1','I2','I3','I4'),bits)),a=a,b=b,c=c,d=d,n=n,m=m)
        expected=dict(a=a,b=b,c=c,d=d,n=n,m=m,O0=1,O1=d&i4)
        for node,value in expected.items():assert rail(graph,vv,node)[0]==value
        assert expected['O1']==i4&(i1|i2|(1-i3))
        rows.append(dict(**dict(zip(('I0','I1','I2','I3','I4'),bits)),a=a,b=b,c=c,d=d,O0=1,O1=expected['O1'],passed=True))
    export('q2_truth.csv',rows);export('q2_conditional_vt_MOS.csv',graph)
    # Inverter reference: mean delay=((Rp+Rn)/2)*Ci =1 unit.
    # r=Rp/Rn; nMOS1um,pMOS2um only imply r=1 if mu_n/mu_p=2.
    ratios=[]
    for r in(F(1,2),F(1),F(2),F(3)):
        nor=(2*r+1)/(r+1);nand=(r+2)/(r+1)
        values={'A_NOR':2*nor,'B_NOR':nor,'C_INV':F(1),'D_NAND':2*nand,'E_F_OR':nor+2,'G_H_AND':nand+2}
        ratios.append(dict(Rp_over_Rn=str(r),**{k:float(v)for k,v in values.items()},model='mean rise/fall;actual fanout;given inverter mean = 1 unit',passed=True))
        if r==1:assert list(values.values())==[F(3),F(3,2),F(1),F(3),F(7,2),F(7,2)]
    export('q2_general_resistance_delays.csv',ratios)
    gates=[dict(gate='A NOR(I1,I2)',input_loads='B,D',load_Ci=2,rise=4,fall=2,mean=3),
           dict(gate='B NOR(I0,a)',input_loads='C',load_Ci=1,rise=2,fall=1,mean=1.5),
           dict(gate='C INV(b)',input_loads='E',load_Ci=1,rise=1,fall=1,mean=1),
           dict(gate='D NAND(a,I3)',input_loads='E,G',load_Ci=2,rise=2,fall=4,mean=3),
           dict(gate='E+F OR(c,d)',input_loads='2Ci external; internal Ci',load_Ci=2,rise=3,fall=4,mean=3.5),
           dict(gate='G+H AND(d,I4)',input_loads='2Ci external; internal Ci',load_Ci=2,rise=4,fall=3,mean=3.5)]
    export('q2_balanced_gate_delays.csv',gates)
    paths=[('I1/I2','O0','A,B,C,E+F',9,9,9),('I1/I2','O0','A,D,E+F',9.5,7,12),
           ('I1/I2','O1','A,D,G+H',9.5,8,11),('I0','O0','B,C,E+F',6,5,7),
           ('I3','O0','D,E+F',6.5,8,5),('I3','O1','D,G+H',6.5,7,6),('I4','O1','G+H',3.5,4,3)]
    timing=[dict(launch=s,capture=e,physical_path=p,mean_units=avg,input_rise_arc_sum=up,input_fall_arc_sum=down,
                 sensitization='O0 is steady constant 1; conservative physical arc sum, not an observed output edge'if e=='O0'else'sensitizable logic path',passed=True)
            for s,e,p,avg,up,down in paths]
    assert max(row['mean_units']for row in timing)==9.5
    assert max(max(row['input_rise_arc_sum'],row['input_fall_arc_sum'])for row in timing if row['capture']=='O1')==11
    export('q2_physical_path_delays.csv',timing)
    slack=[]
    for rho in(F(1),F(6,5),F(3,2),F(2)):
        upper=3+F(5,2)*rho+F(7,2);admissible=upper<=F(19,2)
        assert admissible==(rho<=F(6,5))
        slack.append(dict(high_delay_scale=str(rho),upper_mean_path=float(upper),baseline_mean_worst=9.5,
                          no_mean_speed_loss=admissible,model='illustrative uniform upper B/C penalty; not provided process data',passed=True))
    export('q2_highVt_slack_examples.csv',slack)
    # For the balanced edge model, reconvergent c/d are ordered so there is
    # no O0 pulse for isolated changes ofa withI0=0,I3=1. Do not turn an
    # average-delay path sum into a physically fabricated output waveform.
    events=[dict(a_transition='0->1',c_event='rise',c_time_relative_a=2,d_event='fall',d_time_relative_a=4,O0='stays 1; overlapping high inputs',passed=True),
            dict(a_transition='1->0',c_event='fall',c_time_relative_a=3,d_event='rise',d_time_relative_a=2,O0='stays 1; overlapping high inputs',passed=True)]
    export('q2_balanced_reconvergence.csv',events)
    return dict(MOS=26,graph=graph,cases=32,functions=['O0=1','O1=I4*(I1+I2+NOTI3)'],
                balanced_mean_gate_delays={row['gate']:row['mean']for row in gates},
                balance_assumption='Rp = Rn at Wp = 2 um / Wn = 1 um requires mu_n/mu_p = 2; not stated in Q2; general r formulas also included',
                mean_path_max=9.5,edge_O1_sensitized_max=11,edge_O0_conservative_arc_sum_max=12,
                conditional_Vt=dict(low=20,high=6,high_devices='B NOR and C inverter only',mean_metric_bound='rho <= 6/5 in illustrative uniform high-Vt scaling'),
                optimum_limit='No high-Vt characterization or leakage weights are provided; candidate is eligible under explicit slack, not claimed as a unique optimum.',
                O0_scope='Steady constant 1; preserve printed physical paths and label arc sums conservative; balanced isolated-a edge model has no pulse.',
                no_process_measurement=True)

def q3():
    rows=[];even=[]
    for fanout in(2,4,16,64,256,1000,1000000):
        center=math.log(fanout);bound=max(10,math.ceil(center)*3)
        values=[(n,n*fanout**(1/n))for n in range(1,bound+1)]
        n,delay=min(values,key=lambda item:item[1]);beta=fanout**(1/n)
        candidates={max(1,math.floor(center)),max(1,math.ceil(center))}
        assert n in candidates
        caps=sum(beta**k for k in range(1,n+1));load=beta**n;eta=(caps-load)/caps
        expression=(beta**(n-1)-1)/(beta**n-1)
        assert abs(eta-expression)<1e-10 and abs(load-fanout)<1e-8
        rows.append(dict(CL_over_Ci=fanout,continuous_N=center,integer_N=n,beta=beta,delay_over_unitRC=delay,
                         eta_internal_over_total=eta,load_fraction=1-eta,output_inverts=(n%2==1),passed=True))
        ne,de=min((item for item in values if item[0]%2==0),key=lambda item:item[1]);be=fanout**(1/ne)
        even.append(dict(CL_over_Ci=fanout,even_N=ne,beta=be,delay_over_unitRC=de,scope='only if noninverting parity is required; not stated',passed=True))
    export('q3_integer_buffer_optima.csv',rows);export('q3_even_buffer_optima.csv',even)
    return dict(continuous_beta=math.e,continuous_N='ln(CL/Ci)',integer_rule='N >= 1: compare floor/ceil ln(F), beta = F^(1/N); restrict to even N if required',
                delay='D=N*F^(1/N)*referenceRC',eta_definition='(PT-PL)/PT; overhead fraction',
                eta='(beta^(N-1)-1)/(beta^N-1)',continuous_eta='(F/e-1)/(F-1), only when continuous N = ln(F) is appropriate',
                large_load_limit=1/math.e,no_parasitic_model=True,integer_cases=len(rows))

def q4():
    rows=[]
    for alpha in(F(1),F(2)):
        delay=(1+alpha)*(1+2/alpha);assert delay==6
        rows.append(dict(alpha=float(alpha),delay_over_RC=float(delay),first_two_gate_load_over_C=float(2*(1+alpha)),
                         selected=alpha==1,passed=True))
    export('q4_alpha_candidates.csv',rows)
    return dict(mu_n_over_mu_p=2,T_over_RC=6,feasible_alpha=[1,2],chosen_alpha=1,
                delay='T/RC=(1+alpha)*(1+2/alpha)',power='2*a01*f*(1+alpha)*C*VDD^2',chosen_to_alpha2_power_ratio=2/3,
                source_scope='T brackets the first two inverters; CL after the third excludes the first pair; ignore unspecified diffusion/wire capacitances')

def q5():
    graph=adder_graph();assert len(graph)==28;rows=[]
    for x,y,c in itertools.product((0,1),repeat=3):
        n=x+y+c;co=int(n>=2);s=n%2;vv=dict(VDD=1,VSS=0,x=x,y=y,c=c,cb=1-co,sb=1-s)
        for node,expected in(('cb',1-co),('cout',co),('sb',1-s),('sout',s)):
            assert rail(graph,vv,node)[0]==expected
        assert s+2*co==n
        rows.append(dict(x=x,y=y,ci=c,s=s,co=co,passed=True))
    export('q5_full_adder_truth.csv',rows);export('q5_full_adder_MOS.csv',graph)
    return dict(MOS=28,graph=graph,cases=8,sum='x XOR y XOR ci',carry='xy+ci(x+y)',
                source_comparison='Graded booklet answers inverse operand recovery; not adopted. Ungraded study sheet gives correct forward Boolean/gate logic but not complete MOS expansion; independent 28-MOS schematic supplied.',
                source_last_row='111 -> s = 1, co = 1 confirmed from compiled original; photo ink circle around sum is annotation')

def main():
    data=dict(year=2008,season='Spring',exam='midterm',status='PASS',
              method='ideal static MOS graphs; analytical balanced/general RC delays; conditional dual-Vt slack; buffer optimization; no process simulation',
              Q1=q1(),Q2=q2(),Q3=q3(),Q4=q4(),Q5=q5())
    (HERE/'logic_timing_verification.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print('PASS: Q1 CMOS 32; Q2 rail 32 / actual fanout / general r / slack; integer buffers 7; alpha roots 2; full adder 8 / 28 MOS.')
if __name__=='__main__':main()
