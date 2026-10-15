"""Exhaustively verify the 2020 HW1 MUX and CMOS conduction networks."""
from itertools import product
from pathlib import Path
import csv,json
HERE=Path(__file__).resolve().parent

def mux(s,d0,d1):return d1 if s else d0

def main():
    rows=[]
    for x1,x2,x3 in product([0,1],repeat=3):
        expected=int((not x1 and x2 and x3) or (x1 and not x2 and x3) or (x1 and x2 and not x3))
        nx3=mux(x3,1,0)
        out=mux(x1,mux(x2,0,x3),mux(x2,x3,nx3))
        assert out==expected
        rows.append(dict(problem='Q2',inputs=f'{x1}{x2}{x3}',expected=expected,observed=out))
    for w,x,y,z in product([0,1],repeat=4):
        pdn=bool((w and (x or y)) or (y and z))
        pun=bool(((not w) or ((not x) and (not y))) and ((not y) or (not z)))
        expected=int(not pdn)
        assert pun==bool(expected) and pun!=pdn
        rows.append(dict(problem='Q3a',inputs=f'{w}{x}{y}{z}',expected=expected,observed=int(pun)))
    for x,y,z in product([0,1],repeat=3):
        expected=int((not x and not y) or (not x and not z) or (not y and not z))
        pdn=bool((x or y) and (x or z) and (y or z))
        pun=bool((not x and not y) or (not x and not z) or (not y and not z))
        assert int(not pdn)==expected and pun!=pdn
        rows.append(dict(problem='Q3b',inputs=f'{x}{y}{z}',expected=expected,observed=int(pun)))
    with (HERE/'truth_tables.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    result={'Q2_cases':8,'Q3a_cases':16,'Q3b_cases':8,'all_pass':True,'complementary_networks_mutually_exclusive':True}
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
