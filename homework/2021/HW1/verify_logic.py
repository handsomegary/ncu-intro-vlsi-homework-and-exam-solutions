"""Exhaustive independent Boolean and long-channel checks for 2021 HW1."""
import csv,json,math
from pathlib import Path
H=Path(__file__).resolve().parent
mux=lambda s,d0,d1:d1 if s else d0
rows=[]
for word in range(8):
 x1,x2,x3=[(word>>i)&1 for i in [2,1,0]]
 want=int(x1+x2+x3==2)
 nx3=mux(x3,1,0)
 and23=mux(x2,0,x3)
 xor23=mux(x2,x3,nx3)
 got=mux(x1,and23,xor23)
 assert want==got
 rows.append(dict(problem='2',input=f'{word:03b}',expected=want,observed=got))
for word in range(16):
 w,x,y,z=[bool(word>>i&1) for i in [3,2,1,0]]
 want=not(w and(x or y) or y and z)
 pdn=w and(x or y) or y and z
 pun=((not w) or ((not x) and(not y))) and ((not y) or(not z))
 assert pun==want and pdn!=pun
 rows.append(dict(problem='3a',input=f'{word:04b}',expected=int(want),observed=int(pun)))
for word in range(8):
 x,y,z=[bool(word>>i&1) for i in [2,1,0]]
 want=((not x) and(not y)) or((not x) and(not z)) or((not y) and(not z))
 pdn=x and(y or z) or y and z
 pun=((not x) or((not y) and(not z))) and((not y) or(not z))
 assert pun==want and pdn!=pun
 rows.append(dict(problem='3b',input=f'{word:03b}',expected=int(want),observed=int(pun)))
maxerr=0
for i in range(1,51):
 U=i/50
 for j in range(101):
  v=2*U*j/100
  u=U*(1-1/math.sqrt(2)) if v>=U else U-math.sqrt(U*U-U*v+v*v/2)
  i1=U*u-u*u/2
  U2=U-u;dv=v-u
  i2=U2*dv-dv*dv/2 if dv<U2 else U2*U2/2
  equiv=.5*(U*v-v*v/2) if v<U else U*U/4
  maxerr=max(maxerr,abs(i1-i2),abs(i1-equiv))
assert maxerr<1e-12
with (H/'truth_tables.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(H/'verification.json').write_text(json.dumps(dict(boolean_cases=32,all_pass=True,long_channel_points=5050,max_normalized_current_error=maxerr,body_effect=False,channel_length_modulation=False),indent=2))
print('32 Boolean cases and 5050 square-law stack points passed')
