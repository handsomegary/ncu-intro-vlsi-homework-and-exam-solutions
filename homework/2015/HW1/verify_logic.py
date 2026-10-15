"""Exhaustive checks of the visually confirmed 2015 double-bar expression."""
from pathlib import Path
from itertools import product
import csv,json
HERE=Path(__file__).resolve().parent

def main():
    rows=[]
    for a,b,c in product([0,1],repeat=3):
        f=int((not a and (b or not c)) or (a and not b and c))
        mux=[1-c,1,c,0][2*a+b]
        assert mux==f
        rows.append(dict(problem='Q3',input_bits=f'{a}{b}{c}',expected=f,actual=mux))
    for w,x,y,z in product([0,1],repeat=4):
        t=not(x or y)
        expected=int(not((w and t) or (y and z)))
        pdn=(w and t) or (y and z)
        pun=((not w) or (not t)) and ((not y) or (not z))
        assert int(pun)==expected and pun!=pdn
        rows.append(dict(problem='Q4a',input_bits=f'{w}{x}{y}{z}',expected=expected,actual=int(pun)))
    for x,y,z in product([0,1],repeat=3):
        expected=int((not x and not y) or (not x and not z) or (not y and not z))
        pdn=(x or y) and (x or z) and (y or z)
        assert int(not pdn)==expected
        rows.append(dict(problem='Q4b',input_bits=f'{x}{y}{z}',expected=expected,actual=int(not pdn)))
    with (HERE/'truth_tables.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    summary={'all_pass':True,'Q3_cases':8,'Q4a_cases':16,'Q4b_cases':8,'Q4a_expression':'NOT[w*NOT(x+y)+y*z]'}
    (HERE/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
