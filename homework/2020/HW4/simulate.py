"""Reproduce all changing-output transitions of the 2020 AND gate in HSPICE.

Local CIC018 model is a prerequisite, never distributed. Raw simulator files
go to --raw-dir; only measurements, sampled waveforms and checks are exported.
"""
from pathlib import Path
import argparse, csv, json, re, subprocess, shutil, hashlib

HERE = Path(__file__).resolve().parent
TRANSITIONS = [(0,3),(1,3),(2,3),(3,0),(3,1),(3,2)]

def write_csv(path, rows):
    with Path(path).open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def run(hspice, folder, deck):
    folder.mkdir(parents=True, exist_ok=True)
    (folder/'testbench.sp').write_text(deck, encoding='ascii')
    shutil.copy2(HERE/'and2.sp', folder/'and2.sp')
    p=subprocess.run([hspice,'-i','testbench.sp','-o','run'],cwd=folder,capture_output=True,text=True,errors='replace',timeout=120)
    (folder/'console.log').write_text(p.stdout+p.stderr,encoding='utf-8')
    lis=(folder/'run.lis').read_text(errors='replace') if (folder/'run.lis').exists() else ''
    if p.returncode or 'job concluded' not in lis.lower() or '**error**' in lis.lower():
        raise RuntimeError(f'HSPICE did not complete: {folder}; inspect console.log and run.lis')
    return lis

def read_measures(lis):
    return {m.group(1).lower():float(m.group(2)) for m in re.finditer(r'^\s*([a-zA-Z][\w]*)\s*=\s*([+-]?[\d.]+e[+-]?\d+)',lis,re.M|re.I)}

def read_trace(path):
    rows={};names=[];armed=False
    lines=path.read_text(errors='replace').splitlines()
    for i,line in enumerate(lines):
        if line.strip().lower().startswith('time '):
            names=lines[i+1].lower().split();armed=True;continue
        if not armed:continue
        try:vals=[float(x.replace('D','e')) for x in line.split()]
        except ValueError:continue
        if len(vals)==len(names)+1 and vals:
            rows.setdefault(vals[0],{}).update(dict(zip(names, vals[1:])))
    return [(t,v) for t,v in sorted(rows.items()) if all(n in v for n in ['a','b','f','z'])]

def deck(model, initial, final, slew_ps, timestep_ps):
    a0,b0=(initial>>1)&1,initial&1
    a1,b1=(final>>1)&1,final&1
    s=f'''* 2020 HW3 {initial:02b}->{final:02b}, controlled 50-percent delays
.protect
.lib '{model.as_posix()}' TT
.unprotect
.include 'and2.sp'
.option post=0 measform=3 numdgt=10 measdgt=10 ingold=2 lis_new=1 delmax={timestep_ps}p
.temp 25
VDD vdd 0 1.8
VSS vss 0 0
VA a vss PWL(0 {a0*1.8} 2n {a0*1.8} {2e-9+slew_ps*1e-12:.12e} {a1*1.8} 5n {a1*1.8})
VB b vss PWL(0 {b0*1.8} 2n {b0*1.8} {2e-9+slew_ps*1e-12:.12e} {b1*1.8} 5n {b1*1.8})
XAND a b f z vdd vss and2
CL z vss 1f
.tran {timestep_ps}p 5n
.print tran V(a) V(b) V(f) V(z)
'''
    trigger='a' if a0!=a1 else 'b'
    rise=(a1>a0) if trigger=='a' else (b1>b0)
    direction='RISE' if rise else 'FALL'
    f_direction='FALL' if final==3 else 'RISE'
    z_direction='RISE' if final==3 else 'FALL'
    for node,target in [('f',f_direction),('z',z_direction)]:
        s+=f'.measure tran delay_{node} TRIG V({trigger}) VAL=0.9 {direction}=1 TD=1.9n TARG V({node}) VAL=0.9 {target}=1 TD=1.9n\n'
        s+=f'.measure tran before_{node} FIND V({node}) AT=1.9n\n'
        s+=f'.measure tran after_{node} FIND V({node}) AT=4.9n\n'
    return s+'.end\n'

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hspice',default='C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com')
    ap.add_argument('--model',default='D:/cic018.l')
    ap.add_argument('--raw-dir',default=str(HERE.parents[2]/'2020-simulation'/'HW3'))
    args=ap.parse_args();model=Path(args.model).resolve();raw=Path(args.raw_dir).resolve()
    if not model.is_file():raise FileNotFoundError('Local model file missing; not distributed in this repository')
    rows=[];checks=[];trace_rows=[]
    # Primary fixed-slew result, timestep convergence, and a slower input check.
    for slew,step in [(20,1),(20,0.2),(1000,1)]:
        for initial,final in TRANSITIONS:
            folder=raw/f'{initial:02b}_{final:02b}_slew{slew}_step{step}'
            listing=run(args.hspice,folder,deck(model,initial,final,slew,step))
            m=read_measures(listing)
            if not all(k in m for k in ['delay_f','delay_z','before_f','before_z','after_f','after_z']):
                raise RuntimeError(f'Missing delay/level measurement: {folder}')
            for node in ['f','z']:
                rising=(final!=3) if node=='f' else (final==3)
                expected_before=int((initial!=3) if node=='f' else (initial==3))
                expected_after=int((final!=3) if node=='f' else (final==3))
                level_ok=lambda v,x:v>=1.6 if x else v<=0.2
                ok=level_ok(m['before_'+node],expected_before) and level_ok(m['after_'+node],expected_after)
                if m['delay_'+node]<=0:raise AssertionError('Measured propagation delay must be positive')
                checks.append(dict(transition=f'{initial:02b}->{final:02b}',node=node,slew_ps=slew,step_ps=step,
                                   before_V=m['before_'+node],after_V=m['after_'+node],pass_logic_levels=ok))
                rows.append(dict(transition=f'{initial:02b}->{final:02b}',node=node,direction='LH' if rising else 'HL',
                                 slew_ps=slew,step_ps=step,delay_ps=m['delay_'+node]*1e12))
            if slew==20 and step==1:
                for t,v in read_trace(folder/'run.printtr0'):
                    trace_rows.append(dict(transition=f'{initial:02b}->{final:02b}',time_ns=t*1e9,**{n+'_V':v[n] for n in ['a','b','f','z']}))
    write_csv(HERE/'delays.csv',rows);write_csv(HERE/'level_checks.csv',checks);write_csv(HERE/'waveforms.csv',trace_rows)
    worst=[]
    for node in ['f','z']:
        for direction in ['HL','LH']:
            candidates=[r for r in rows if r['node']==node and r['direction']==direction and r['slew_ps']==20 and r['step_ps']==1]
            winner=max(candidates,key=lambda r:r['delay_ps']);worst.append(winner)
    write_csv(HERE/'worst_delays.csv',worst)
    convergence=[]
    for r in [r for r in rows if r['slew_ps']==20 and r['step_ps']==1]:
        fine=next(v for v in rows if v['transition']==r['transition'] and v['node']==r['node'] and v['slew_ps']==20 and v['step_ps']==.2)
        convergence.append(dict(transition=r['transition'],node=r['node'],delay_1ps=r['delay_ps'],delay_02ps=fine['delay_ps'],difference_ps=abs(r['delay_ps']-fine['delay_ps'])))
    write_csv(HERE/'convergence.csv',convergence)
    summary=dict(simulator='PrimeSim HSPICE S-2021.09 WIN64',model_corner='CIC018 TT',temperature_C=25,vdd_V=1.8,
                 load_fF=1,input_slew_ps=20,transitions=len(TRANSITIONS),simulator_runs=18,
                 all_logic_levels_pass=all(c['pass_logic_levels'] for c in checks),
                 maximum_timestep_difference_ps=max(c['difference_ps'] for c in convergence),worst_delays=worst,
                 circuit_sha256=hashlib.sha256((HERE/'and2.sp').read_text(encoding='utf-8').encode('utf-8')).hexdigest(),
                 circuit_hash_normalization='UTF-8 LF')
    (HERE/'validation.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    # Ready-to-run primary example, also valid from this directory.
    (HERE/'testbench.sp').write_text(deck(model,0,3,20,1),encoding='ascii')
    print(json.dumps(summary,indent=2))
    if not summary['all_logic_levels_pass']:raise AssertionError('Logic-level verification failed')

if __name__=='__main__':main()
