"""Small HSPICE utilities; raw output always stays in a separate scratch folder."""
from pathlib import Path
import csv,re,subprocess,shutil

def header(model,step_ps=1):
    return f"* 2015 reproducible schematic simulation\n.protect\n.lib '{Path(model).resolve().as_posix()}' TT\n.unprotect\n.option post=0 lis_new=1 ingold=2 numdgt=10 measdgt=10 measform=3 delmax={step_ps}p\n.temp 25\n"

def run(hspice,folder,deck,includes=()):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    for src in includes:shutil.copy2(src,folder/Path(src).name)
    (folder/'testbench.sp').write_text(deck,encoding='ascii',newline='\n')
    p=subprocess.run([hspice,'-i','testbench.sp','-o','run'],cwd=folder,capture_output=True,text=True,errors='replace',timeout=240)
    (folder/'console.log').write_text(p.stdout+p.stderr,encoding='utf-8')
    lis=(folder/'run.lis').read_text(errors='replace') if (folder/'run.lis').exists() else ''
    if p.returncode or 'job concluded' not in lis.lower() or '**error**' in lis.lower():raise RuntimeError(f'HSPICE failed: {folder}; inspect local listing')
    return lis

def measurements(lis):
    return {m.group(1).lower():float(m.group(2)) for m in re.finditer(r'^\s*([A-Za-z][\w]*)\s*=\s*([+-]?[\d.]+e[+-]?\d+)',lis,re.M|re.I)}

def trace(path,required=()):
    lines=Path(path).read_text(errors='replace').splitlines();result={};names=[];armed=False
    for i,line in enumerate(lines):
        if line.strip().lower().startswith('time '):names=lines[i+1].lower().split();armed=True;continue
        if not armed:continue
        try:nums=[float(v.replace('D','e')) for v in line.split()]
        except ValueError:continue
        if len(nums)==len(names)+1 and nums:result.setdefault(nums[0],{}).update(dict(zip(names,nums[1:])))
    return [(t,v) for t,v in sorted(result.items()) if all(n in v for n in required)]

def write_csv(path,rows):
    if not rows:raise ValueError('No rows to export')
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def crossing(points,key,val,rising,start=0,end=float('inf')):
    for (ta,a),(tb,b) in zip(points,points[1:]):
        if ta<start or tb>end:continue
        va,vb=a[key],b[key]
        if (va<val<=vb) if rising else (va>val>=vb):return ta+(val-va)/(vb-va)*(tb-ta)
    raise ValueError(f'Missing crossing {key} at {val}')

def integral(points,key,start,end):
    selected=[(t,v[key]) for t,v in points if start-1e-17<=t<=end+1e-17]
    if len(selected)<2:raise ValueError('Missing integration samples')
    return sum((tb-ta)*(a+b)/2 for (ta,a),(tb,b) in zip(selected,selected[1:]))
