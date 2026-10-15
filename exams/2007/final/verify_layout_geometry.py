"""Check the actual reconstructed Q3 Metal1 paths for unintended same-layer shorts."""
from pathlib import Path
from fractions import Fraction as F
import csv,json,re

here=Path(__file__).resolve().parent
text=(here/'exam.tex').read_text(encoding='utf-8').split(r'\newcommand{\OriginalLayout}',1)[1].split(r'\newcommand{\SolutionLayout}',1)[0]
section='rails';routes=[]
for line in text.splitlines():
 for label in ['dbar','u','CLKB','O']:
  if line.startswith('% '+label+':'):section=label
 if line.startswith('% Supply contacts'):section='supplies'
 for match in re.finditer(r'\\draw\[metal\]\(([-.\d]+),([-.\d]+)\)--\(([-.\d]+),([-.\d]+)\)',line):
  x1,y1,x2,y2=map(F,match.groups())
  if x1>8 or x2>9:continue  # legend only
  assert x1==x2 or y1==y2
  name=section
  if section in ['rails','supplies']:name='VDD'if max(y1,y2)>4 else 'VSS'
  routes.append(dict(net=name,x1=str(x1),y1=str(y1),x2=str(x2),y2=str(y2)))
assert len(routes)==18

def intersects(a,b):
 ax1,ay1,ax2,ay2=[F(a[k])for k in ['x1','y1','x2','y2']]
 bx1,by1,bx2,by2=[F(b[k])for k in ['x1','y1','x2','y2']]
 if ay1==ay2 and by1==by2:
  return ay1==by1 and max(min(ax1,ax2),min(bx1,bx2))<=min(max(ax1,ax2),max(bx1,bx2))
 if ax1==ax2 and bx1==bx2:
  return ax1==bx1 and max(min(ay1,ay2),min(by1,by2))<=min(max(ay1,ay2),max(by1,by2))
 if ax1==ax2:return intersects(b,a)
 return min(ax1,ax2)<=bx1<=max(ax1,ax2)and min(by1,by2)<=ay1<=max(by1,by2)

cross_net=[]
for i,a in enumerate(routes):
 for j,b in enumerate(routes[:i]):
  if a['net']!=b['net']and intersects(a,b):cross_net.append([i,j,a['net'],b['net']])
assert not cross_net, f'Unintended same-Metal1 intersections: {cross_net}'
bad_return=dict(net='u',x1='7.16',y1='4.0',x2='7.16',y2='1.1')
assert any(r['net']=='O'and intersects(bad_return,r)for r in routes), 'Negative control must detect an erroneous full u metal return.'
with (here/'q3-normalized-metal-routes.csv').open('w',newline='',encoding='utf-8')as out:
 writer=csv.DictWriter(out,fieldnames=list(routes[0]));writer.writeheader();writer.writerows(routes)
report={'actual_TikZ_metal_routes_checked':len(routes),'cross_net_same_Metal1_intersections':cross_net,'contact_netlist_is_checked_separately':True,'important_source_feature':'upper/lower final u drain stubs connect through continuous u poly with two contacts; no metal bridge across O feed','status':'passed'}
(here/'q3-layer-geometry-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
