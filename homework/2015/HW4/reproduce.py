"""2015 HW4: 28T mirror adder and valid cascaded domino adder, pre-layout only.

Match worst 10-90% output rise/fall slews to within 3% at the declared TT
condition. Report all 56 static input transitions and all 8 domino evaluate
words. The separate monotone carry-complement domino rail enables sum logic.
"""
from pathlib import Path
import sys,argparse,json,hashlib,re
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from sim_utils import header,run,measurements,trace,write_csv
HERE=Path(__file__).resolve().parent
WN=.47
CASES=[(a,b) for a in range(8) for b in range(8) if a!=b]

def expected(word,node):
    total=(word&1)+((word>>1)&1)+((word>>2)&1)
    if node=='co':return int(total>=2)
    if node=='nco':return int(total<2)
    return total&1

def mos(name,d,g,s,b,p,w,l='0.18u'):
    return f"M{name} {d} {g} {s} {b} {'P_18' if p else 'N_18'} W='{w}' L={l} AD='({w})*0.18u' AS='({w})*0.18u' PD='2*(({w})+0.18u)' PS='2*(({w})+0.18u)'\n"

def mirror(pc,ps):
    s=f'* 28T mirror adder; channel geometry and body ties are explicit.\n.param WN={WN}u PG=4 PC={pc:.10f} PS={ps:.10f}\n.subckt mirror a b ci co s vdd vss\n'
    # Carry complement = NOT[C*(A+B)+A*B], 5+5 core MOS.
    for p in [False,True]:
        rail='vdd' if p else 'vss';w='PG*WN' if p else 'WN';prefix='P' if p else 'N'
        for label,d,g,src,factor in [('C0','cb','ci',prefix+'c0',2),('C1',prefix+'c0','a',rail,2),('C2',prefix+'c0','b',rail,2),
                                     ('C3','cb','a',prefix+'c1',2),('C4',prefix+'c1','b',rail,2)]:
            s+=mos(prefix+label,d,g,src,rail,p,f'{factor}*{w}')
        # Sum complement core: cb*(A+B+C)+ABC, 7+7 core MOS.
        for label,d,g,src,factor in [('S0','sb','cb',prefix+'s0',2),('S1',prefix+'s0','a',rail,2),('S2',prefix+'s0','b',rail,2),('S3',prefix+'s0','ci',rail,2),
                                     ('S4','sb','a',prefix+'s1',3),('S5',prefix+'s1','b',prefix+'s2',3),('S6',prefix+'s2','ci',rail,3)]:
            s+=mos(prefix+label,d,g,src,rail,p,f'{factor}*{w}')
    for node,drive,ratio in [('co','cb','PC'),('s','sb','PS')]:
        s+=mos('P'+node,node,drive,'vdd','vdd',True,ratio+'*WN')+mos('N'+node,node,drive,'vss','vss',False,'WN')
    return s+'.ends mirror\n'

def domino(pc,ps):
    s=f'* 38T domino adder including 3 input inverters and weak keepers.\n.param WN={WN}u PC={pc:.10f} PS={ps:.10f}\n.subckt domino a b ci clk co s nco vdd vss\n'
    for n in ['a','b','ci']:
        s+=mos('PI'+n,n+'b',n,'vdd','vdd',True,'4*WN')+mos('NI'+n,n+'b',n,'vss','vss',False,'WN')
    for prefix,out,inputs,ratio in [('c','co',['a','b','ci'],'PC'),('nc','nco',['ab','bb','cib'],'4')]:
        dyn=prefix+'d';foot=prefix+'f';aa,bb,cc=inputs
        s+=mos(prefix+'PRE',dyn,'clk','vdd','vdd',True,'4*WN')
        s+=mos(prefix+'KEEP',dyn,out,'vdd','vdd',True,'WN','0.5u')
        s+=mos(prefix+'FOOT',foot,'clk','vss','vss',False,'3*WN')
        for label,d,g,src in [('0',dyn,cc,prefix+'m'),('1',prefix+'m',aa,foot),('2',prefix+'m',bb,foot),('3',dyn,aa,prefix+'n'),('4',prefix+'n',bb,foot)]:
            s+=mos(prefix+'N'+label,d,g,src,'vss',False,'3*WN')
        s+=mos(prefix+'OP',out,dyn,'vdd','vdd',True,ratio+'*WN')+mos(prefix+'ON',out,dyn,'vss','vss',False,'WN')
    s+=mos('SPRE','sd','clk','vdd','vdd',True,'4*WN')+mos('SKEEP','sd','s','vdd','vdd',True,'WN','0.5u')
    s+=mos('SFOOT','sf','clk','vss','vss',False,'4*WN')
    for label,d,g,src,factor in [('0','sd','nco','sm',3),('1','sm','a','sf',3),('2','sm','b','sf',3),('3','sm','ci','sf',3),
                                 ('4','sd','a','sn',4),('5','sn','b','sp',4),('6','sp','ci','sf',4)]:
        s+=mos('SN'+label,d,g,src,'vss',False,f'{factor}*WN')
    s+=mos('SOP','s','sd','vdd','vdd',True,'PS*WN')+mos('SON','s','sd','vss','vss',False,'WN')
    return s+'.ends domino\n'

def static_deck(model,step):
    deck=header(model,step)+".include 'mirror.sp'\nVDD dd 0 1.8\n"
    for k,(before,after) in enumerate(CASES):
        for n,bit in [('a',2),('b',1),('ci',0)]:
            v0=1.8*((before>>bit)&1);v1=1.8*((after>>bit)&1)
            deck+=f'V{n}{k} {n}{k} 0 PWL(0 {v0} 2n {v0} 2.02n {v1} 5n {v1})\n'
        deck+=f'X{k} a{k} b{k} ci{k} co{k} s{k} dd 0 mirror\nCC{k} co{k} 0 1f\nCS{k} s{k} 0 1f\n'
        changed=next((n,bit) for n,bit in [('a',2),('b',1),('ci',0)] if ((before>>bit)&1)!=((after>>bit)&1))
        trig,bit=changed;dirin='RISE' if ((after>>bit)&1) else 'FALL'
        for node in ['co','s']:
            deck+=f'.measure tran q{k}{node} FIND V({node}{k}) AT=4.9n\n'
            if expected(before,node)==expected(after,node):continue
            up=expected(after,node);di='RISE' if up else 'FALL';v0=.18 if up else 1.62;v1=1.62 if up else .18
            deck+=f'.measure tran d{k}{node} TRIG V({trig}{k}) VAL=.9 {dirin}=1 TD=1.9n TARG V({node}{k}) VAL=.9 {di}=1 TD=1.9n\n'
            deck+=f'.measure tran t{k}{node} TRIG V({node}{k}) VAL={v0} {di}=1 TD=1.9n TARG V({node}{k}) VAL={v1} {di}=1 TD=1.9n\n'
    return deck+'.tran 1p 5n\n.print tran V(a0) V(b0) V(ci0) V(co0) V(s0)\n.end\n'

def domino_deck(model,step):
    deck=header(model,step)+".include 'domino.sp'\nVDD dd 0 1.8\nVCLK clk 0 PWL(0 0 2n 0 2.02n 1.8 4n 1.8 4.02n 0 5n 0)\n"
    for k in range(8):
        for n,bit in [('a',2),('b',1),('ci',0)]:deck+=f'V{n}{k} {n}{k} 0 {1.8*((k>>bit)&1)}\n'
        deck+=f'X{k} a{k} b{k} ci{k} clk co{k} s{k} nco{k} dd 0 domino\nCC{k} co{k} 0 1f\nCS{k} s{k} 0 1f\n'
        for node in ['co','s','nco']:
            deck+=f'.measure tran q{k}{node} FIND V({node}{k}) AT=3.8n\n.measure tran r{k}{node} FIND V({node}{k}) AT=4.8n\n'
            if not expected(k,node):continue
            deck+=f'.measure tran d{k}{node} TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V({node}{k}) VAL=.9 RISE=1 TD=1.9n\n'
            deck+=f'.measure tran e{k}{node} TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V({node}{k}) VAL=.9 FALL=1 TD=3.9n\n'
            for pref,di,v0,v1,td in [('t','RISE',.18,1.62,1.9),('u','FALL',1.62,.18,3.9)]:
                deck+=f'.measure tran {pref}{k}{node} TRIG V({node}{k}) VAL={v0} {di}=1 TD={td}n TARG V({node}{k}) VAL={v1} {di}=1 TD={td}n\n'
    return deck+'.tran 1p 5n\n.print tran V(clk) V(co0) V(s0) V(nco0) V(co1) V(s1) V(nco1) V(co7) V(s7) V(nco7)\n.end\n'

def collect(kind,m,step):
    rows=[];checks=[]
    if kind=='mirror':
        for k,(before,after) in enumerate(CASES):
            for node in ['co','s']:
                y=expected(after,node);v=m[f'q{k}{node}'];ok=v>=1.6 if y else v<=.2
                checks.append(dict(case=k,inputs_before=f'{before:03b}',inputs_after=f'{after:03b}',node=node,expected=y,voltage_V=v,pass_level=ok))
                if expected(before,node)!=y:rows.append(dict(case=k,inputs_before=f'{before:03b}',inputs_after=f'{after:03b}',node=node,direction='LH' if y else 'HL',delay_ps=m[f'd{k}{node}']*1e12,slew_10_90_ps=m[f't{k}{node}']*1e12,step_ps=step))
    else:
        for k in range(8):
            for node in ['co','s','nco']:
                y=expected(k,node);v=m[f'q{k}{node}'];reset=m[f'r{k}{node}'];ok=(v>=1.6 if y else v<=.2) and reset<=.2
                checks.append(dict(case=k,input_bits=f'{k:03b}',node=node,expected=y,evaluate_V=v,reset_V=reset,pass_level=ok))
                if y:
                    rows.append(dict(case=k,input_bits=f'{k:03b}',node=node,direction='LH',delay_ps=m[f'd{k}{node}']*1e12,slew_10_90_ps=m[f't{k}{node}']*1e12,step_ps=step))
                    rows.append(dict(case=k,input_bits=f'{k:03b}',node=node,direction='HL',delay_ps=m[f'e{k}{node}']*1e12,slew_10_90_ps=m[f'u{k}{node}']*1e12,step_ps=step))
    if not all(r['pass_level'] for r in checks):raise AssertionError(f'{kind} functional verification failed')
    if not all(r['delay_ps']>0 and r['slew_10_90_ps']>0 for r in rows):raise AssertionError('Invalid timing measurement')
    return rows,checks

def balance(rows):
    result={}
    for node in ['co','s']:
        tr=max(r['slew_10_90_ps'] for r in rows if r['node']==node and r['direction']=='LH')
        tf=max(r['slew_10_90_ps'] for r in rows if r['node']==node and r['direction']=='HL')
        result[node]=dict(worst_rise_ps=tr,worst_fall_ps=tf,relative_difference=abs(tr-tf)/max(tr,tf),ratio=tr/tf)
    return result

def export_waveforms(kind,model,raw,hspice,worst):
    indices=sorted({r['case'] for r in worst})
    deck=(static_deck if kind=='mirror' else domino_deck)(model,.2)
    names=([f'{n}{k}' for k in indices for n in ['a','b','ci','co','s']] if kind=='mirror' else ['clk']+[f'{n}{k}' for k in indices for n in ['co','s','nco']])
    deck=re.sub(r'\.print tran[^\n]*', '.print tran '+' '.join(f'V({n})' for n in names),deck)
    folder=raw/(kind+'_waveforms');run(hspice,folder,deck,[HERE/(kind+'.sp')])
    points=trace(folder/'run.printtr0',required=names)
    if not points:raise RuntimeError('No full-adder waveform samples')
    data=[]
    for k in indices:
        for i,(t,v) in enumerate(points):
            if not 1.8e-9<=t<=(2.65e-9 if kind=='mirror' else 4.45e-9) or i%2:continue
            if kind=='mirror':
                before,after=CASES[k]
                data.append(dict(case=k,inputs_before=f'{before:03b}',inputs_after=f'{after:03b}',time_ns=t*1e9,
                                 **{n+'_V':v[f'{n}{k}'] for n in ['a','b','ci','co','s']}))
            else:data.append(dict(case=k,input_bits=f'{k:03b}',time_ns=t*1e9,clock_V=v['clk'],**{n+'_V':v[f'{n}{k}'] for n in ['co','s','nco']}))
    write_csv(HERE/(kind+'_waveforms.csv'),data)
    (HERE/(kind+'_testbench.sp')).write_text(deck,encoding='ascii',newline='\n')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--hspice',default='C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com');ap.add_argument('--model',default='D:/cic018.l');ap.add_argument('--raw-dir',default=str(HERE.parents[2]/'2015-simulation'/'HW4'));ap.add_argument('--waveforms-only',action='store_true')
    args=ap.parse_args();raw=Path(args.raw_dir).resolve();history=[];summary={}
    if args.waveforms_only:
        summary=json.loads((HERE/'verification.json').read_text())
        for kind in ['mirror','domino']:export_waveforms(kind,args.model,raw,args.hspice,summary[kind]['worst_delays'])
        print('Exported measured worst-case waveforms without repeating the sizing search.')
        return
    for kind,build,deckfn in [('mirror',mirror,static_deck),('domino',domino,domino_deck)]:
        pc,ps=3.6,3.6
        for iteration in range(14):
            circuit=build(pc,ps);(HERE/(kind+'.sp')).write_text(circuit,encoding='ascii',newline='\n')
            folder=raw/f'{kind}_tune{iteration}';lis=run(args.hspice,folder,deckfn(args.model,1),[HERE/(kind+'.sp')]);rows,checks=collect(kind,measurements(lis),1);b=balance(rows)
            for node,ratio in [('co',pc),('s',ps)]:history.append(dict(kind=kind,iteration=iteration,node=node,output_Wp_Wn=ratio,**b[node]))
            print(json.dumps({'kind':kind,'iteration':iteration,'PC':pc,'PS':ps,'balance':b}),flush=True)
            if max(v['relative_difference'] for v in b.values())<=.02:break
            pc*=b['co']['ratio']**.8;ps*=b['s']['ratio']**.8
        else:raise RuntimeError('Slew balancing did not converge; inspect tuning evidence')
        write_csv(HERE/(kind+'_delays.csv'),rows);write_csv(HERE/(kind+'_logic.csv'),checks)
        primary=rows
        # Verify sizing still meets target under a five-times tighter step.
        fine_deck=deckfn(args.model,.2);lis=run(args.hspice,raw/f'{kind}_fine',fine_deck,[HERE/(kind+'.sp')]);fine,fc=collect(kind,measurements(lis),.2)
        convergence=[dict(case=r['case'],node=r['node'],direction=r['direction'],delay_1ps=r['delay_ps'],delay_02ps=f['delay_ps'],difference_ps=abs(r['delay_ps']-f['delay_ps'])) for r,f in zip(primary,fine)]
        write_csv(HERE/(kind+'_convergence.csv'),convergence);write_csv(HERE/(kind+'_fine_delays.csv'),fine)
        bf=balance(fine)
        if max(v['relative_difference'] for v in bf.values())>.03:raise AssertionError('Final fine-step slew balance exceeds3percent')
        worst=[]
        for node in ['co','s']:
            for direction in ['LH','HL']:worst.append(max([r for r in fine if r['node']==node and r['direction']==direction],key=lambda r:r['delay_ps']))
        write_csv(HERE/(kind+'_worst_delays.csv'),worst)
        (HERE/(kind+'_testbench.sp')).write_text(fine_deck,encoding='ascii',newline='\n')
        summary[kind]={'all_logic_pass':True,'output_Wp_Wn_CO':pc,'output_Wp_Wn_S':ps,'fine_step_balance':bf,'worst_delays':worst,
                       'max_delay_timestep_difference_ps':max(r['difference_ps'] for r in convergence),
                       'netlist_SHA256_UTF8_LF':hashlib.sha256(circuit.encode('ascii')).hexdigest(),'device_count':sum(l.startswith('M') for l in circuit.splitlines()),
                       'truth_checks':len(checks),'timing_rows':len(fine)}
        export_waveforms(kind,args.model,raw,args.hspice,worst)
    write_csv(HERE/'sizing_search.csv',history)
    summary.update({'corner':'CIC018 TT','VDD_V':1.8,'temperature_C':25,'input_clock_slew_ps':20,'output_load_fF':1,
                    'slew_definition':'worst10to90rise versus worst90to10fall, eachoutput, tolerance3percent',
                    'domino_delay_definition':'clock50tooutput50; precharge/resetreportedseparately','scope':'pre-layoutonly'})
    (HERE/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
