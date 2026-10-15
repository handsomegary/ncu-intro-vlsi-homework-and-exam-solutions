#!/usr/bin/env python3
"""Reproduce source-derived Q5--Q7 checks; no missing Q4 premises assumed."""
import csv,itertools,json
from pathlib import Path
OUT=Path(__file__).resolve().parent

def save(name,rows):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def reach(edges,start):
    found={start}
    while True:
        new=found|{b for a,b in edges if a in found}|{a for a,b in edges if b in found}
        if new==found:return found
        found=new

def complex_core(primary,terms,values):
    # nMOS: primary in series with parallel terms. Dual pMOS:
    # primary pMOS in parallel with a series chain of term pMOS.
    n=[];p=[]
    if values[primary]:n.append(('U','n'))
    for t in terms:
        if values[t]:n.append(('n','GND'))
    if not values[primary]:p.append(('U','VDD'))
    chain=['U']+[f'p{i}' for i in range(len(terms)-1)]+['VDD']
    for i,t in enumerate(terms):
        if not values[t]:p.append((chain[i],chain[i+1]))
    low='GND' in reach(n,'U');high='VDD' in reach(p,'U')
    assert low != high
    return int(high),low,high

def main():
    noise=[]
    for s in ['0011','0101','1101','1110']:
        a,b,c,d=map(int,s);g1=1-(b&c);g2=1-(a|g1);g3=1-(g1&d)
        noise.append({'ABCD':s,'G1':g1,'G2':g2,'G3':g3,
            'G1_conventional_margin':'NML>NMH','G2_conventional_margin':'NML<NMH',
            'G3_conventional_margin':'NML>NMH',
            'G2_any_single_input_masked':bool(a==1 and g1==1),
            'G3_any_single_input_masked':bool(g1==0 and d==0)})
    assert [x['G2_any_single_input_masked'] for x in noise]==[False,False,True,False]
    assert [x['G3_any_single_input_masked'] for x in noise]==[False,False,False,True]
    save('q5_noise_context.csv',noise)
    # Q6: Cg per W/L transistor. NAND n2/p2, inverter n1/p2.
    cap=1+2;rup=rdown=1;invup=invdown=1
    tr=rdown*cap+invup*4;tf=rup*cap+invdown*4
    assert tr==tf==7 and max(tr,tf)<8
    delays=[{'transition':'AND output rise','NAND_delay_over_RCg':rdown*cap,
             'inverter_delay_over_RCg':invup*4,'total_over_RCg':tr},
            {'transition':'AND output fall','NAND_delay_over_RCg':rup*cap,
             'inverter_delay_over_RCg':invdown*4,'total_over_RCg':tf}]
    save('q6_rc_delays.csv',delays)
    sizing_rows=[]
    for a,b in itertools.product([0,1],repeat=2):
        u=1-(a&b);f=1-u
        assert f==(a&b)
        sizing_rows.append({'A':a,'B':b,'NAND_U':u,'AND_F':f})
    save('q6_truth.csv',sizing_rows)
    checks=[]
    specs=[('a','X',['Y','Z','W'],True),('b','X',['Y','Z'],False),('c','Y',['X','Z'],True)]
    for part,primary,terms,positive in specs:
        names=['X','Y','Z','W'] if part=='a' else ['X','Y','Z']
        for bits in itertools.product([0,1],repeat=len(names)):
            v=dict(zip(names,bits));u,lo,hi=complex_core(primary,terms,v)
            output=1-u if positive else u
            if part=='a':wanted=int((v['X'] and(v['Y']or v['Z']))or(v['X']and v['W']))
            elif part=='b':wanted=int(not(v['X']and(v['Y']or v['Z'])))
            else:wanted=int((v['X']and v['Y'])or(v['Y']and v['Z']))
            assert output==wanted
            checks.append({'part':part,**{k:v.get(k,'') for k in ['X','Y','Z','W']},
                           'core_U':u,'PDN_conducts':lo,'PUN_conducts':hi,
                           'output_inverter_present':positive,'F':output,'expected':wanted})
    save('q7_switch_checks.csv',checks)
    report={'source_complete_questions':[5,6,7],'source_complete_point_total':35,
        'Q4_answer_status':'omitted: opening with thresholds and resistances is missing',
        'Q5':{'qualitative_assumption':'Standard matched-threshold static CMOS VTC, ideal rails; width/mobility ratio determines pull-strength bias',
              'source_quantitative_margins':None,'single_transistor_beta_n_equals_beta_p':True,
              'NAND_sensitized_beta_p_over_beta_n':2,'NOR_sensitized_beta_p_over_beta_n':0.5,
              'masked_input_contexts':'G2 at1101; G3 at1110; a single-input switching VTC is not sensitized',
              'rows':noise},
        'Q6':{'Cg_definition':'Gate capacitance of ONE W/L nMOS or pMOS',
              'NAND_sizes_relative_W_over_L':{'nMOS_each':2,'pMOS_each':2},
              'inverter_sizes_relative_W_over_L':{'nMOS':1,'pMOS':2},
              'inverter_input_cap_over_Cg':3,'output_load_over_Cg':4,
              'worst_delay_over_RCg':7,'strictly_below_8_RCg':True,'model':'ON-resistance RC sum with no parasitics; no process simulation'},
        'Q7':{'truth_rows_checked':len(checks),'PDN_PUN_complementarity':True,
              'a':{'factorization':'X(Y+Z+W)','core':'U=not[X(Y+Z+W)]','output_inverter':True,'transistor_count':10},
              'b':{'core':'F=not[X(Y+Z)]','output_inverter':False,'transistor_count':6},
              'c':{'factorization':'Y(X+Z)','core':'U=not[Y(X+Z)]','output_inverter':True,'transistor_count':8}}}
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Verified Q5 four contexts; Q6 7RCg both directions; Q7 all32 input rows and rail exclusivity.')
if __name__=='__main__':main()
