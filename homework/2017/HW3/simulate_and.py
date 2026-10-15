"""Reproduce actual CIC018-TT HSPICE delays and logic levels.
Uses the user's local D:/cic018.l; the model is not redistributed.
python reproduce.py --hspice PATH --model PATH --work PATH
"""
from pathlib import Path
import argparse,csv,json,re,subprocess,os
HERE=Path(__file__).resolve().parent
CASES=[('00',0,0,'a'),('01',0,1,'a'),('10',1,0,'b')]
def table(path):
    lines=path.read_text(errors='replace').splitlines()
    rows=list(csv.DictReader(l for l in lines if l.strip() and not l.startswith(('$','.'))))
    if len(rows)!=1: raise RuntimeError('Unexpected HSPICE measurement table')
    return {k:float(v) for k,v in rows[0].items() if k not in ['alter#','temper']}
def trace(path):
    rows={}; names=[]; armed=False
    lines=path.read_text(errors='replace').splitlines()
    for i,l in enumerate(lines):
        if l.strip().lower().startswith('time '):
            names=lines[i+1].lower().split();armed=True;continue
        if not armed:continue
        try:n=[float(x.replace('D','e')) for x in l.split()]
        except ValueError:continue
        if len(n)==len(names)+1:rows.setdefault(n[0],{}).update(dict(zip(names,n[1:])))
    return [(t,d) for t,d in sorted(rows.items()) if all(n in d for n in ['a','b','f','z'])]
def deck(case,model):
    name,a,b,trig=case
    s=f"* 2017 AND gate, initial AB={name}\n.protect\n.lib '{model.as_posix()}' tt\n.unprotect\n.include 'and2.sp'\nvvdd vdd 0 1.8\nvvss vss 0 0\n"
    for node,value in [('a',a),('b',b)]:
        s+=f'v{node} {node} 0 '+('1.8\n' if value else 'pulse(0 1.8 5n .1n .1n 4n 10n)\n')
    s+='XG a b f z vdd vss and2\nCL z 0 1f\n.temp 25\n.option measform=3 measdgt=9 ingold=2 lis_new=1 delmax=2p\n.tran 2p 32n 0 2p\n'
    for cycle in range(1,4):
        for key,ie,oe in [('f_hl','rise','fall'),('f_lh','fall','rise'),('z_lh','rise','rise'),('z_hl','fall','fall')]:
            s+=f'.measure tran {key}{cycle} trig v({trig}) val=.9 {ie}={cycle} targ v({key[0]}) val=.9 {oe}={cycle}\n'
    for node in ['f','z']:
        s+=f'.measure tran {node}_at_initial find v({node}) at=4n\n.measure tran {node}_at_11 find v({node}) at=9n\n'
    s+='.print tran v(a) v(b) v(f) v(z)\n.end\n'
    return s

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hspice',default=os.environ.get('HSPICE','C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com'))
    ap.add_argument('--model',default=os.environ.get('CIC018_MODEL','D:/cic018.l'))
    ap.add_argument('--work',default=str(HERE.parents[2]/'scratch'/('2017_'+HERE.name)))
    a=ap.parse_args(); raw=Path(a.work).resolve();model=Path(a.model).resolve()
    if not model.is_file():raise FileNotFoundError('Local CIC018 model required: '+str(model))
    results=HERE/'results'/'and_gate';results.mkdir(parents=True,exist_ok=True)
    delays=[];levels=[];waves=[];statuses=[]
    for case in CASES:
        name=case[0];folder=raw/name;folder.mkdir(parents=True,exist_ok=True)
        (folder/'and2.sp').write_text((HERE/'and2.sp').read_text(),encoding='ascii')
        text=deck(case,model);(folder/'testbench.sp').write_text(text,encoding='ascii')
        if name=='00':(HERE/'testbench.sp').write_text(text,encoding='ascii')
        p=subprocess.run([a.hspice,'-i','testbench.sp','-o','run'],cwd=folder,capture_output=True,text=True,errors='replace',timeout=180)
        (folder/'console.log').write_text(p.stdout+p.stderr,encoding='utf-8')
        lis=(folder/'run.lis').read_text(errors='replace') if (folder/'run.lis').exists() else ''
        good=p.returncode==0 and 'job concluded' in lis.lower() and '**error**' not in lis.lower()
        if not good:raise RuntimeError(f'HSPICE failed in {folder}, inspect local logs')
        m=table(folder/'run.mt0.csv')
        for cycle in range(1,4):
            for key in ['f_hl','f_lh','z_lh','z_hl']:
                v=m[key+str(cycle)]*1e12
                if not 0<v<1000:raise AssertionError('Unexpected propagation delay')
                delays.append(dict(initial_ab=name,cycle=cycle,node=key[0].upper(),direction=key[2:].upper(),delay_ps=v))
        for state,key in [(name,'initial'),('11','11')]:
            expected_f=int(state!='11');expected_z=1-expected_f
            vf=m['f_at_'+key];vz=m['z_at_'+key]
            passed=(vf>1.6 if expected_f else vf<.2) and (vz>1.6 if expected_z else vz<.2)
            levels.append(dict(case=name,input_ab=state,F_V=vf,Z_V=vz,expected_F=expected_f,expected_Z=expected_z,pass_=bool(passed)))
            if not passed:raise AssertionError('Functional voltage check failed')
        tr=trace(folder/'run.printtr0')
        for t,d in tr:
            if 4e-9<=t<=12e-9 and round(t/2e-12)%5==0:
                waves.append(dict(case=name,time_ns=t*1e9,**{k.upper()+'_V':d[k] for k in ['a','b','f','z']}))
        statuses.append(dict(case=name,status='completed',exit_code=p.returncode))
    for fn,rows in [('delays.csv',delays),('logic_levels.csv',levels),('waveforms.csv',waves)]:
        with (results/fn).open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    worst=[]
    for node in ['F','Z']:
        for direction in ['HL','LH']:
            v=max((r for r in delays if r['node']==node and r['direction']==direction),key=lambda r:r['delay_ps']);worst.append(v)
    summary=dict(simulator='PrimeSim HSPICE S-2021.09 win64',model='CIC018 TT BSIM3 (local)',VDD_V=1.8,temperature_C=25,load_fF=1.0,input_slew_0_to_100_ns=0.1,max_time_step_ps=2.0,delay_definition='input and output 50 percent crossings; input-to-F and input-to-Z',cases=statuses,functional_samples=len(levels),all_logic_levels_pass=True,worst_case=worst)
    (results/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
