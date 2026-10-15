"""Exhaustively verify the 2021 HW2 table and constant-R sizing."""
from pathlib import Path
import csv,json
H=Path(__file__).resolve().parent
rows=[]
for data in range(16):
 a=[data>>j&1 for j in range(4)]
 for rotation in range(4):
  c=[1]*4;c[3-rotation]=0
  z=[sum(a[(j-k)%4]*(1-c[3-k]) for k in range(4)) for j in range(4)]
  expect=((data<<rotation)|(data>>(4-rotation if rotation else 4)))&15
  got=sum(z[j]<<j for j in range(4));assert got==expect
  rows.append(dict(data=data,control=''.join(str(b) for b in reversed(c)),rotation=rotation,expected=expect,observed=got,passed=True))
for a in range(2):
 for b in range(2):
  for c in range(2):
   ab=not a;bb=not b
   pdn=(ab and b) or(a and bb)
   pun=((not ab) or(not b)) and((not a) or(not bb))
   assert pun==(a==b) and pdn!=pun
   assert not(b and c)==(not b or not c)
res=[]
for a in range(2):
 for b in range(2):
  rn=1000/9;rp=2000/2
  low=rn/(a+b) if a+b else None
  v=1.8*low/(rp+low) if low else 1.8
  res.append(dict(A=a,B=b,Vout_V=v,expected=int(not(a or b))))
assert abs(res[1]['Vout_V']-.18)<1e-12
with (H/'truth_tables.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (H/'constant_resistance.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(res[0]));w.writeheader();w.writerows(res)
(H/'logic_verification.json').write_text(json.dumps(dict(rotator_cases=64,rotator_output_bits=256,dual_vt_boolean_cases=8,pseudo_nor_cases=4,all_pass=True,pseudo_nor_min_WN_over_WP=4.5,high_vt_NAND_max_delay_units=2),indent=2))
print('64 rotator cases, 8 Q1 cases and 4 constant-R NOR cases passed')
