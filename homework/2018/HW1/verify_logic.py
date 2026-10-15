"""Exhaustively verify the 2018 HW1 MUX and CMOS conduction networks."""
from itertools import product
from pathlib import Path
import csv,json,math
HERE=Path(__file__).resolve().parent

def mux(s,d0,d1):return d1 if s else d0

def main():
    rows=[]
    for x1,x2,x3 in product([0,1],repeat=3):
        expected=int((not x1 and x2 and x3) or (x1 and not x2 and x3) or (x1 and x2 and not x3))
        nx3=mux(x3,1,0)
        out=mux(x1,mux(x2,0,x3),mux(x2,x3,nx3))
        assert out==expected
        rows.append(dict(problem='Q3',inputs=f'{x1}{x2}{x3}',expected=expected,observed=out))
    for w,x,y,z in product([0,1],repeat=4):
        pdn=bool((w and (x or y)) or (y and z))
        pun=bool(((not w) or ((not x) and (not y))) and ((not y) or (not z)))
        expected=int(not pdn)
        assert pun==bool(expected) and pun!=pdn
        rows.append(dict(problem='Q4a',inputs=f'{w}{x}{y}{z}',expected=expected,observed=int(pun)))
    for x,y,z in product([0,1],repeat=3):
        expected=int((not x and not y) or (not x and not z) or (not y and not z))
        pdn=bool((x or y) and (x or z) and (y or z))
        pun=bool((not x and not y) or (not x and not z) or (not y and not z))
        assert int(not pdn)==expected and pun!=pdn
        rows.append(dict(problem='Q4b',inputs=f'{x}{y}{z}',expected=expected,observed=int(pun)))
    for a,b,c in product([0,1],repeat=3):
        u,v=1-a,1-b
        pdn=(u and b) or (a and v)
        pun=((not u) or (not b)) and ((not a) or (not v))
        expected=int(a==b)
        assert int(pun)==expected and bool(pdn)!=bool(pun)
        assert int(not(b and c))==int((not b) or(not c))
        rows.append(dict(problem='Q2',inputs=f'{a}{b}{c}',expected=expected,observed=int(pun)))
    maxerr=0.0
    for i in range(1,51):
        U=i/50
        for j in range(101):
            drain=2*U*j/100
            u=U*(1-1/math.sqrt(2)) if drain>=U else U-math.sqrt(U*U-U*drain+drain*drain/2)
            i1=U*u-u*u/2; U2=U-u;dv=drain-u
            i2=U2*dv-dv*dv/2 if dv<U2 else U2*U2/2
            equiv=.5*(U*drain-drain*drain/2) if drain<U else U*U/4
            maxerr=max(maxerr,abs(i1-i2),abs(i1-equiv))
    assert maxerr<1e-12
    with (HERE/'truth_tables.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    result={'Q2_cases':8,'Q3_cases':8,'Q4a_cases':16,'Q4b_cases':8,'boolean_cases':40,'square_law_points':5050,'max_current_error':maxerr,'all_pass':True,'complementary_networks_mutually_exclusive':True}
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
