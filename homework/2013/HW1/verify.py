"""Independent truth-table, switch-connectivity and unequal-length MOS checks."""
from pathlib import Path
from itertools import product
from collections import defaultdict
import csv,json,math
H=Path(__file__).resolve().parent
def csvout(name,rows):
 with (H/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def solve(devices,values,out):
 edges=defaultdict(set)
 for kind,g,a,b in devices:
  if values[g]==(1 if kind=='n' else 0):edges[a].add(b);edges[b].add(a)
 seen={out};todo=[out]
 while todo:
  for n in edges[todo.pop()]:
   if n not in seen:seen.add(n);todo.append(n)
 hi,lo='VDD' in seen,'GND' in seen
 assert hi!=lo,(values,out,seen)
 return int(hi)
nor=[('n','x','h','GND'),('n','y','h','GND'),('p','x','VDD','p'),('p','y','p','h')]
aoi22=[('n','w','f','n1'),('n','h','n1','GND'),('n','y','f','n2'),('n','z','n2','GND'),
       ('p','w','VDD','p1'),('p','h','VDD','p1'),('p','y','p1','f'),('p','z','p1','f')]
minority=[('n','x','f','n1'),('n','y','n1','GND'),('n','z','n1','GND'),('n','y','f','n2'),('n','z','n2','GND'),
          ('p','x','VDD','p1'),('p','y','VDD','p2'),('p','z','p2','p1'),('p','y','p1','f'),('p','z','p1','f')]
rows=[]
for a,b,c in product((0,1),repeat=3):
 expected=int((not a and (b or not c)) or (a and not b and c))
 actual=[1-c,1,c,0][2*a+b]
 assert actual==expected
 rows.append(dict(question='Q3',inputs=f'{a}{b}{c}',expected=expected,actual=actual,passed=True))
for w,x,y,z in product((0,1),repeat=4):
 v=dict(w=w,x=x,y=y,z=z);v['h']=solve(nor,v,'h')
 actual=solve(aoi22,v,'f');expected=int(not(w and not(x or y) or y and z))
 assert actual==expected
 rows.append(dict(question='Q4a',inputs=f'{w}{x}{y}{z}',expected=expected,actual=actual,passed=True))
for x,y,z in product((0,1),repeat=3):
 v=dict(x=x,y=y,z=z);actual=solve(minority,v,'f');expected=int(x+y+z<2)
 assert actual==expected
 rows.append(dict(question='Q4b',inputs=f'{x}{y}{z}',expected=expected,actual=actual,passed=True))
csvout('truth_tables.csv',rows)
err=0;points=0
for l1,l2 in product((.5,1.,2.,4.),repeat=2):
 for i in range(1,51):
  u0=i/50
  for j in range(101):
   v=2*u0*j/100
   u=u0*(1-math.sqrt(l2/(l1+l2))) if v>=u0 else u0-math.sqrt(u0*u0-2*l1/(l1+l2)*(u0*v-v*v/2))
   lower=(u0*u-u*u/2)/l1
   upper=((u0-u)*(v-u)-(v-u)**2/2)/l2 if v<u0 else (u0-u)**2/(2*l2)
   eq=(u0*v-v*v/2)/(l1+l2) if v<u0 else u0*u0/(2*(l1+l2))
   err=max(err,abs(lower-upper),abs(lower-eq));points+=1
assert err<1e-12
r={'status':'PASS','truth_table_cases':len(rows),'q3_cases':8,'q4a_cases':16,'q4b_cases':8,'unequal_length_current_points':points,'maximum_normalized_current_error':err,'q4a_transistors':12,'q4b_transistors':10,'model_scope':'ideal MOS switches and long-channel square law, no body effect or channel-length modulation'}
(H/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
