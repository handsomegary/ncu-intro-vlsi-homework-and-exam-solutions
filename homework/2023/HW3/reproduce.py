"""Actual HSPICE sweep: 128 states, all 896 directed single-input transitions.

Each sweep starts from its own DC solution. Delay is the last 50% output
crossing minus the 50% input crossing. Unchanged outputs have no required delay.
The power workload is a separate 128-vector binary-count sequence.
"""
from pathlib import Path
import sys as _simulation_sys
_simulation_sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from simulation_environment import default_hspice, default_model, add_environment_check, resolve_simulation_args
import argparse, csv, hashlib, itertools, json, os, shutil, subprocess
HERE=Path(__file__).resolve().parent
INS=['x0','x1','x2','y0','y1','y2','cin']; OUTS=['s0','s1','s2','cout']
def value(state): return (state&7)+((state>>3)&7)+(state>>6)
def sha(p): return hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def write_csv(p,rows):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def run(hspice, folder, deck, netlist):
    folder.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(netlist,folder/'rca.sp');(folder/'testbench.sp').write_text(deck)
    p=subprocess.run([hspice,'-i','testbench.sp','-o','run'],cwd=folder,capture_output=True,timeout=600)
    (folder/'console.log').write_bytes(p.stdout+p.stderr)
    lis=(folder/'run.lis').read_text(errors='replace')
    if p.returncode or 'job concluded' not in lis.lower() or '**error**' in lis.lower():
        raise RuntimeError(f'HSPICE failed: {folder}')
    lines=(folder/'run.mt0.csv').read_text(errors='replace').splitlines()
    return [{k.strip().lower():v.strip() for k,v in r.items()} for r in csv.DictReader(l for l in lines if l.strip() and not l.startswith(('$','.')))]
def header(model):
    return f"* 2023 HW3: TT, 1.8V, 25C; model remains external.\n.protect\n.lib '{model.as_posix()}' TT\n.unprotect\n.include 'rca.sp'\nVDD vdd 0 1.8\n.option post=0 measform=3 measdgt=10 numdgt=10 delmax=2p\n.temp 25\nXADD cin x0 x1 x2 y0 y1 y2 s0 s1 s2 cout vdd 0 rca\n"+''.join(f'C{n} {n} 0 1f\n' for n in OUTS)
def sweep(model):
    s=header(model)+'.param '+ ' '.join(f'{n}a=0 {n}b=0' for n in INS)+'\n'
    s+='VREF ref 0 pwl(0 0 1n 0 1.02n 1.8 3n 1.8)\n'
    for n in INS:s+=f"V{n} {n} 0 pwl(0 '{n}a' 1n '{n}a' 1.02n '{n}b' 3n '{n}b')\n"
    s+='.data CASES caseid '+' '.join(f'{n}a {n}b' for n in INS)+'\n'
    cases=[]
    for old in range(128):
        for bit in range(7):
            new=old^(1<<bit); cases.append((old,new,bit))
            s+=str(len(cases))+' '+ ' '.join(f'{1.8*((old>>b)&1):g} {1.8*((new>>b)&1):g}' for b in range(7))+'\n'
    s+='.enddata\n.tran 2p 3n sweep data=CASES\n'
    for n in OUTS:
        s+=f'.meas tran pre_{n} find v({n}) at=0.9n\n.meas tran post_{n} find v({n}) at=2.9n\n'
        s+=f'.meas tran d_{n} trig v(ref) val=0.9 rise=1 targ v({n}) val=0.9 cross=last\n'
    return s+'.end\n',cases
def power(model):
    s=header(model); period=3.; slew=.02
    for bit,n in enumerate(INS):
        points=[f'0n {1.8*((0>>bit)&1):g}']
        for k in range(1,128):
            if (k>>bit&1)!=((k-1)>>bit&1):points.extend([f'{k*period:g}n {1.8*(((k-1)>>bit)&1):g}',f'{k*period+slew:g}n {1.8*((k>>bit)&1):g}'])
        s+=f'V{n} {n} 0 pwl(\n'
        for j in range(0,len(points),8):s+='+ '+' '.join(points[j:j+8])+'\n'
        s+='+)\n'
    s+='.tran 2p 384n\n.meas tran pavg avg par(\'-v(vdd)*i(VDD)\') from=0 to=384n\n'
    s+='.meas tran energy integ par(\'-v(vdd)*i(VDD)\') from=0 to=384n\n'
    for k in range(128):
        for n in OUTS:s+=f'.meas tran v{k}_{n} find v({n}) at={k*period+2.9:g}n\n'
    return s+'.end\n'
def voltage_ok(v,bit):return 1.6<=v<=1.82 if bit else -.02<=v<=.2
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hspice',default=default_hspice())
    ap.add_argument('--model',type=Path,default=default_model())
    ap.add_argument('--work',type=Path,default=HERE/'.simulation');ap.add_argument('--results',type=Path,default=HERE/'results')
    add_environment_check(ap);args=ap.parse_args();resolve_simulation_args(ap,args);args.work=args.work.resolve();args.results.mkdir(parents=True,exist_ok=True)
    deck,cases=sweep(args.model.resolve());(HERE/'characterize.sp').write_text(deck)
    rows=run(args.hspice,args.work/'characterize',deck,HERE/'rca.sp')
    if len(rows)!=896:raise AssertionError(f'Expected 896 sweeps, got {len(rows)}')
    volts=[];delays=[]
    for row,(old,new,bit) in zip(rows,cases):
        assert int(float(row['caseid']))==len(volts)+1
        a,b=value(old),value(new);v={'case':len(volts)+1,'old':old,'new':new,'input':INS[bit],'expected_before':a,'expected_after':b}
        passed=True
        for j,n in enumerate(OUTS):
            for phase,target in [('pre',a),('post',b)]:
                voltage=float(row[f'{phase}_{n}']);v[f'{phase}_{n}_v']=voltage;passed &= voltage_ok(voltage,(target>>j)&1)
            if ((a^b)>>j)&1:
                delay=float(row[f'd_{n}']);assert 0<delay<1.8e-9
                delays.append({'case':v['case'],'old':old,'new':new,'input':INS[bit],'output':n,'direction':'rise' if b>>j&1 else 'fall','delay_ps':delay*1e12})
        v['passed']=bool(passed);volts.append(v)
    assert all(v['passed'] for v in volts)
    pdeck=power(args.model.resolve());(HERE/'testbench.sp').write_text(pdeck)
    prow=run(args.hspice,args.work/'workload',pdeck,HERE/'rca.sp')[0]
    states=[]
    for k in range(128):
        target=value(k);v={'state':k,'x':k&7,'y':(k>>3)&7,'cin':k>>6,'expected':target}
        levels=[float(prow[f'v{k}_{n}']) for n in OUTS];v.update({n+'_v':q for n,q in zip(OUTS,levels)})
        v['observed']=sum(int(q>.9)<<j for j,q in enumerate(levels));v['passed']=v['observed']==target and all(voltage_ok(q,target>>j&1) for j,q in enumerate(levels));states.append(v)
    assert all(v['passed'] for v in states)
    write_csv(args.results/'transitions.csv',volts);write_csv(args.results/'delays.csv',delays);write_csv(args.results/'exhaustive_128.csv',states)
    worst=max(delays,key=lambda x:x['delay_ps']);rise=max(x['delay_ps'] for x in delays if x['direction']=='rise');fall=max(x['delay_ps'] for x in delays if x['direction']=='fall')
    summary={'status':'PASS','simulator':'PrimeSim HSPICE S-2021.09','voltage_V':1.8,'temperature_C':25,'corner':'TT','output_load_fF':1,'input_slew_ps':20,'max_timestep_ps':2,'dc_states':128,'directed_single_input_transitions':896,'measured_output_transitions':len(delays),'worst_measured':worst,'max_rise_ps':rise,'max_fall_ps':fall,'average_supply_power_uW':float(prow['pavg'])*1e6,'energy_384ns_fJ':float(prow['energy'])*1e15,'power_workload':'states 0..127; x=state&7, y=(state>>3)&7, cin=state>>6; 3ns each','transistors':84,'sum_WL_um2':53.46,'netlist_sha256':sha(HERE/'rca.sp'),'model_sha256':hashlib.sha256(args.model.read_bytes()).hexdigest(),'delay_scope':'all directed single-input transitions between settled inputs at specified TT, supply, load, slew; not a PVT bound or all simultaneous transitions'}
    (args.results/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
