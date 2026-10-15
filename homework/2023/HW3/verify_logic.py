"""Independent ideal MOS switch-connectivity proof parsed from rca.sp.

This verifies static Boolean logic, body ties, transistor count and sum(WL).
Actual voltage/timing/power checks are in reproduce.py's HSPICE evidence.
"""
from pathlib import Path
from itertools import product
from collections import defaultdict
import re,json,hashlib
HERE=Path(__file__).resolve().parent
text=(HERE/'rca.sp').read_text(encoding='utf-8')
blocks={}
for match in re.finditer(r'\.subckt\s+(\w+)[^\n]*\n(.*?)\.ends[^\n]*',text,re.I|re.S):
    devices=[]
    for line in match.group(2).splitlines():
        if line.startswith('M'):
            name,d,g,s,b,model,*rest=line.split()
            w=float(re.search(r'W=([\d.]+)u',line,re.I).group(1))
            l=float(re.search(r'L=([\d.]+)u',line,re.I).group(1))
            devices.append(dict(name=name,d=d,g=g,s=s,b=b,kind=model[0].lower(),w=w,l=l))
    blocks[match.group(1)]=devices
def solve(devices,values,out):
    graph=defaultdict(set)
    for d in devices:
        assert d['b']==('vdd' if d['kind']=='p' else 'vss')
        if values[d['g']]==(0 if d['kind']=='p' else 1):
            graph[d['d']].add(d['s']);graph[d['s']].add(d['d'])
    seen={out};todo=[out]
    while todo:
        for n in graph[todo.pop()]:
            if n not in seen:seen.add(n);todo.append(n)
    high,low='vdd' in seen,'vss' in seen
    assert high!=low,(out,values)
    return int(high)
carry=[d for d in blocks['fa'] if not d['name'].startswith(('MPS','MNS'))]
summer=[d for d in blocks['fa'] if d['name'].startswith(('MPS','MNS'))]
def inv(a):return solve(blocks['inv'],{'a':a},'z')
def fa(a,b,ci):
    vals={'a':a,'b':b,'ci':ci};vals['cn']=solve(carry,vals,'cn')
    return inv(solve(summer,vals,'sn')),inv(vals['cn'])
for a,b,c in product((0,1),repeat=3):
    s,co=fa(a,b,c);assert s+2*co==a+b+c
for x,y,c in product(range(8),range(8),range(2)):
    co=c;s=0
    for j in range(3):
        z,co=fa(x>>j&1,y>>j&1,co);s+=z<<j
    assert s+8*co==x+y+c
area=3*(sum(d['w']*d['l'] for d in blocks['fa'])+2*sum(d['w']*d['l'] for d in blocks['inv']))
count=3*(len(blocks['fa'])+2*len(blocks['inv']))
assert abs(area-53.46)<1e-9 and count==84
result={'status':'PASS','full_adder_cases':8,'rca_cases':128,'transistors':count,'sum_WL_um2':area,
        'netlist_sha256':hashlib.sha256((HERE/'rca.sp').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        'model':'ideal on/off switch connectivity, not process-model simulation'}
(HERE/'results'/'logic_verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
