"""2015 HW3 HSPICE: equal-size AND delays and intrinsic-channel overlap power."""
from pathlib import Path
import sys,argparse,json
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from sim_utils import header,run,measurements,trace,write_csv,integral
HERE=Path(__file__).resolve().parent
TRANS=[(0,3),(1,3),(2,3),(3,0),(3,1),(3,2)]
LOADS=[.1,.3,.5,.7,1]

def and_deck(model,step):
    s=header(model,step)+".include 'and2.sp'\nVDD dd 0 1.8\n"
    for k,(before,after) in enumerate(TRANS):
        for n,bit in [('a',1),('b',0)]:
            lo=1.8*((before>>bit)&1);hi=1.8*((after>>bit)&1)
            s+=f'V{n}{k} {n}{k} 0 PWL(0 {lo} 2n {lo} 2.02n {hi} 5n {hi})\n'
        s+=f'X{k} a{k} b{k} f{k} z{k} dd 0 and2\n'
        trig='a' if (before>>1)!=(after>>1) else 'b'
        rise=((after>>1)>(before>>1)) if trig=='a' else ((after&1)>(before&1))
        for node in ['f','z']:
            up=(after!=3) if node=='f' else (after==3)
            s+=f'.measure tran d{k}{node} TRIG V({trig}{k}) VAL=.9 {"RISE" if rise else "FALL"}=1 TD=1.9n TARG V({node}{k}) VAL=.9 {"RISE" if up else "FALL"}=1 TD=1.9n\n'
            s+=f'.measure tran q{k}{node} FIND V({node}{k}) AT=4.9n\n'
    s+='.tran 1p 5n\n.print tran '+ ' '.join(f'V({n}{k})' for k in range(6) for n in ['a','b','f','z'])+'\n.end\n'
    return s

def power_deck(model):
    s=header(model,2)+'''VIN a 0 PULSE(0 1.8 0 3n 3n 47n 100n)
'''
    for k,cl in enumerate(LOADS):
        s+=f'''VDD{k} dd{k} 0 1.8
MP{k} pd{k} a dd{k} dd{k} P_18 W=1.88u L=0.18u
VP{k} pd{k} out{k} 0
VN{k} out{k} nd{k} 0
MN{k} nd{k} a 0 0 N_18 W=.47u L=.18u
CL{k} out{k} 0 {cl}p
EIP{k} icp{k} 0 VOL='LX4(MP{k})'
EIN{k} icn{k} 0 VOL='LX4(MN{k})'
'''
        expr=f'max(0,min(LX4(MP{k}),LX4(MN{k})))'
        s+=f".measure tran isc{k} AVG PAR('{expr}') FROM=200n TO=300n\n"
        s+=f".measure tran erise{k} INTEG PAR('1.8*{expr}') FROM=200n TO=203n\n"
        s+=f".measure tran efall{k} INTEG PAR('1.8*{expr}') FROM=250n TO=253n\n"
        s+=f".measure tran ecycle{k} INTEG PAR('1.8*{expr}') FROM=200n TO=300n\n"
        s+=f".measure tran psupply{k} AVG PAR('-1.8*I(VDD{k})') FROM=200n TO=300n\n"
        s+=f".measure tran high{k} FIND V(out{k}) AT=299n\n.measure tran low{k} FIND V(out{k}) AT=249n\n"
    s+='.tran 2p 300n\n.print tran V(a) '+ ' '.join(f'V(out{k}) V(icp{k}) V(icn{k}) I(VDD{k})' for k in range(5))+'\n.end\n'
    return s

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hspice',default='C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com');ap.add_argument('--model',default='D:/cic018.l')
    ap.add_argument('--raw-dir',default=str(HERE.parents[2]/'2015-simulation'/'HW3'))
    ap.add_argument('--power-only',action='store_true',help='Recompute only the five-load intrinsic-channel power sweep')
    args=ap.parse_args();raw=Path(args.raw_dir).resolve();delays=[];checks=[]
    previous=json.loads((HERE/'verification.json').read_text()) if args.power_only else None
    for step in ([] if args.power_only else [1,.2]):
        deck=and_deck(args.model,step);lis=run(args.hspice,raw/f'and_step{step}',deck,[HERE/'and2.sp']);m=measurements(lis)
        for k,(before,after) in enumerate(TRANS):
            for node in ['f','z']:
                direction='LH' if ((after!=3) if node=='f' else after==3) else 'HL'
                delays.append(dict(transition=f'{before:02b}->{after:02b}',node=node,direction=direction,step_ps=step,delay_ps=m[f'd{k}{node}']*1e12))
                expected=(after!=3) if node=='f' else after==3
                checks.append(dict(transition=f'{before:02b}->{after:02b}',node=node,step_ps=step,output_V=m[f'q{k}{node}'],pass_level=(m[f'q{k}{node}']>=1.6 if expected else m[f'q{k}{node}']<=.2)))
        if step==1:(HERE/'and_testbench.sp').write_text(deck,encoding='ascii',newline='\n')
    if not args.power_only:
        write_csv(HERE/'and_delays.csv',delays);write_csv(HERE/'and_level_checks.csv',checks)
        worst=[max([r for r in delays if r['step_ps']==1 and r['node']==node and r['direction']==di],key=lambda r:r['delay_ps']) for node in ['f','z'] for di in ['HL','LH']]
        write_csv(HERE/'and_worst_delays.csv',worst)
        convergence=max(abs(r['delay_ps']-next(v['delay_ps'] for v in delays if v['step_ps']==.2 and v['node']==r['node'] and v['transition']==r['transition'])) for r in delays if r['step_ps']==1)
    else:worst=previous['AND_worst_delays'];convergence=previous['max_AND_timestep_difference_ps']
    pdeck=power_deck(args.model);plis=run(args.hspice,raw/'power',pdeck);pm=measurements(plis)
    points=trace(raw/'power'/'run.printtr0',required=['a','out0','icp0','icn0','vdd0'])
    if not points:raise RuntimeError('No power trace')
    period=100e-9;power=[];wave=[]
    # Integrate a fully settled third cycle, not start-up or threshold-only mean.
    for k,cl in enumerate(LOADS):
        derived=[]
        for t,v in points:
            ip=max(0,v[f'icp{k}']);inn=max(0,v[f'icn{k}']);overlap=min(ip,inn)
            derived.append((t,{'overlap':overlap,'supply':-v[f'vdd{k}']}))
        e_rise=pm[f'erise{k}'];e_fall=pm[f'efall{k}'];e_total=pm[f'ecycle{k}'];supply=pm[f'psupply{k}']
        sampled_power=1.8*integral(derived,'overlap',200e-9,300e-9)/period
        measured_power=1.8*pm[f'isc{k}']
        if abs(sampled_power-measured_power)>1e-9:raise AssertionError('Intrinsic-channel trace and HSPICE integration disagree')
        if pm[f'high{k}']<1.6 or pm[f'low{k}']>.2:raise AssertionError('Power sweep output does not settle to both logic rails')
        switch=cl*1e-12*1.8**2/period
        power.append(dict(load_pF=cl,energy_input_rise_J=e_rise,energy_input_fall_J=e_fall,overlap_cycle_energy_J=e_total,
                          Psc_overlap_W=measured_power,Psupply_W=supply,Psw_external_W=switch,residual_W=supply-switch,
                          settled_high_V=pm[f'high{k}'],settled_low_V=pm[f'low{k}'],trace_integration_power_W=sampled_power,
                          definition='VDD*average(max(0,min(LX4(PMOS),LX4(NMOS)))), positive intrinsic channel currents'))
        for i,(t,v) in enumerate(points):
            if 200e-9<=t<=300e-9 and i%25==0:wave.append(dict(load_pF=cl,time_ns=t*1e9,input_V=v['a'],output_V=v[f'out{k}'],Ip_channel_A=v[f'icp{k}'],In_channel_A=v[f'icn{k}'],Isc_overlap_A=max(0,min(v[f'icp{k}'],v[f'icn{k}']))))
    write_csv(HERE/'power_vs_load.csv',power);write_csv(HERE/'power_waveforms.csv',wave)
    (HERE/'power_testbench.sp').write_text(pdeck,encoding='ascii',newline='\n')
    summary={'all_levels_pass':previous['all_levels_pass'] if args.power_only else all(v['pass_level'] for v in checks),'and_same_size_W_um':.47,'L_um':.18,
             'and_no_external_load':True,'input_slew_AND_ps':20,'input_slew_power_ns':3,'period_power_ns':100,
             'max_AND_timestep_difference_ps':convergence,'power_loads_pF':LOADS,'AND_worst_delays':worst,
             'Psc_monotonic_decrease':all(b['Psc_overlap_W']<=a['Psc_overlap_W'] for a,b in zip(power,power[1:])),
             'Psc_definition':'VDD * cycle-average max(0,min(LX4(PMOS),LX4(NMOS))); positive intrinsic channel currents, displacement excluded',
             'corner':'CIC018 TT','VDD_V':1.8,'temperature_C':25,'simulator':'HSPICE S-2021.09 WIN64'}
    (HERE/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    if not summary['all_levels_pass']:raise AssertionError('AND logic failure')

if __name__=='__main__':main()
