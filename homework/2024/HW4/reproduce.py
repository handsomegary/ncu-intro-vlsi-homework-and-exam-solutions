"""Run the HW4 pre-layout netlist, verify all assigned outputs, export statistics.

Requires only Python standard library, a licensed HSPICE, and an external CIC018
model. Raw simulator artifacts stay in run_artifacts/ (excluded from Git).
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import os
import re
import subprocess

HERE=Path(__file__).resolve().parent
DEFAULT_HSPICE=r'C:\synopsys\Hspice_S-2021.09\WIN64\hspice.com'

def run():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--hspice',default=os.environ.get('HSPICE', DEFAULT_HSPICE))
    p.add_argument('--model',default=os.environ.get('CIC018_MODEL','D:/cic018.l'))
    args=p.parse_args()
    model=Path(args.model).resolve()
    if not model.is_file(): raise SystemExit(f'Missing external process model: {model}')
    raw=HERE/'run_artifacts';raw.mkdir(exist_ok=True)
    source=(HERE/'testbench.sp').read_text(encoding='ascii')
    deck=re.sub(r"\.lib\s+'[^']+'\s+tt",f".lib '{model.as_posix()}' TT",source,flags=re.I)
    runtime=HERE/'.run_testbench.sp'
    runtime.write_text(deck,encoding='ascii')
    try:
        proc=subprocess.run([args.hspice,'-i',str(runtime),'-o',str(raw/'hw4')],cwd=HERE,capture_output=True,text=True)
    finally:
        runtime.unlink(missing_ok=True)
    (raw/'console.log').write_text(proc.stdout+proc.stderr,encoding='utf-8')
    listing=raw/'hw4.lis'
    if proc.returncode or not listing.exists() or 'job concluded' not in listing.read_text(errors='replace').lower():
        raise SystemExit(f'HSPICE did not complete (exit {proc.returncode}); see {raw}')
    mt=raw/'hw4.mt0.csv'
    lines=[line for line in mt.read_text().splitlines() if line.strip() and not line.startswith(('$','.'))]
    values=next(csv.DictReader(lines))
    measured={k.strip().lower():float(v) for k,v in values.items()}
    vectors=[(1,5),(15,13),(11,9),(4,8),(3,7),(12,14),(2,15),(6,10)]
    results=[]
    outputs=['s0','s1','s2','s3','cout']
    for index,(x,y) in enumerate(vectors,1):
        v=[measured[f'v{index}_{name}'] for name in outputs]
        expected=x+y
        ok=all((-0.02<=voltage<=0.2 if not ((expected>>bit)&1) else 1.6<=voltage<=1.82) for bit,voltage in enumerate(v))
        results.append(dict(index=index,x=x,y=y,cin=0,expected=expected,time_ns=index+0.8,passed=ok,**dict(zip(outputs,v))))
    with (HERE/'vectors.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=results[0].keys());writer.writeheader();writer.writerows(results)
    summary={
        'scope':'pre-layout only; no layout/PEX/post-layout',
        'simulator':'PrimeSim HSPICE S-2021.09', 'corner':'TT','vdd_V':1.8,'temperature_C':25,
        'duration_ns':9,'added_output_capacitance_F':0,'model_sha256':hashlib.sha256(model.read_bytes()).hexdigest(),
        'source_hash_line_endings':'LF',
        'netlist_sha256':hashlib.sha256((HERE/'four_bit_multbased_adder.sp').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        'testbench_sha256':hashlib.sha256((HERE/'testbench.sp').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        'assigned_vectors':8,'passed_vectors':sum(r['passed'] for r in results),
        'total_power_W':measured['pavg'], 'total_energy_J':measured['energy'],
        'supply_power_W':measured['supply_pavg'],
        'energy_identity_relative_error':abs(measured['energy']-measured['pavg']*9e-9)/max(abs(measured['energy']),1e-30),
    }
    (HERE/'statistics.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    if summary['passed_vectors']!=8: raise SystemExit('Assigned-vector electrical check FAILED; see vectors.csv')
    if summary['energy_identity_relative_error']>0.001: raise SystemExit('Energy / power integration consistency FAILED')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': run()
