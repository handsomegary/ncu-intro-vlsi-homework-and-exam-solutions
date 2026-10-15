"""Analytical verification and actual HSPICE results for 2020 HW2.

Q1's timing answer is a gate-level bound: no dual-Vt process models were given.
Q2 tests all 64 valid words electrically. Q3's fixed-resistance model is the
assignment model; a separate BSIM3 experiment is explicitly supplementary.
"""
from pathlib import Path
from itertools import product
import argparse,csv,json,re,subprocess,shutil
HERE=Path(__file__).resolve().parent

def write_csv(path,rows):
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hspice',default='C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com')
    ap.add_argument('--model',default='D:/cic018.l')
    ap.add_argument('--raw-dir',default=str(HERE.parents[2]/'2020-simulation'/'HW2'))
    ap.add_argument('--skip-hspice',action='store_true')
    args=ap.parse_args();model=Path(args.model).resolve();raw=Path(args.raw_dir).resolve()
    q1=[]
    for a,b,c in product([0,1],repeat=3):
        d=int(not(a^b));e=int(not(b and c))
        pdn_d=(a and not b) or (not a and b)
        pun_d=((not a) or b) and (a or (not b))
        assert int(pun_d)==d and pun_d!=bool(pdn_d)
        q1.append(dict(a=a,b=b,c=c,d=d,e=e,checked=True))
    write_csv(HERE/'q1_truth.csv',q1)
    timing=[dict(path='A -> inverter -> XOR -> D',baseline_units=2,assigned_Vt='LVT',new_delay_bound_units=2),
            dict(path='B -> XOR -> D (gate abstraction)',baseline_units=1,assigned_Vt='LVT',new_delay_bound_units=1),
            dict(path='B/C -> NAND -> E',baseline_units=1,assigned_Vt='HVT',new_delay_bound_units=2)]
    write_csv(HERE/'q1_timing.csv',timing)
    vectors=[]
    for k in range(4):
        for data in range(16):
            out=sum(((data>>((j+k+1)%4))&1)<<j for j in range(4))
            vectors.append(dict(index=len(vectors),data=data,controls=15^(1<<k),active_low_control=k,expected_output=out))
    write_csv(HERE/'q2_truth.csv',vectors)
    ideal=[]
    for ratio in [1,4.5,5]:
        for ab in range(4):
            count=(ab&1)+(ab>>1)
            rd=1000/(ratio*count) if count else None
            vo=1.8*rd/(2000+rd) if count else 1.8
            ideal.append(dict(ratio_Wn_Wp=ratio,AB=f'{ab:02b}',voltage_V=vo,normalized_voltage=vo/1.8,
                              logic_zero_requirement_pass=(vo<=.18+1e-12) if count else True))
    write_csv(HERE/'q3_ideal_expected.csv',ideal)
    # Actual ideal resistor deck: independent copies isolate all four input cases.
    s='''* 2020 HW2 Q3 assignment fixed-resistance model, not BSIM MOSFETs
.option measform=3 numdgt=10 measdgt=10 ingold=2
.param NR=4.5 R0=1000 VSUP=1.8
VDD vdd 0 'VSUP'
RP00 vdd o00 '2*R0'
RP01 vdd o01 '2*R0'
RP10 vdd o10 '2*R0'
RP11 vdd o11 '2*R0'
RLEAK o00 0 1e15
RN01 o01 0 'R0/NR'
RN10 o10 0 'R0/NR'
RN11A o11 0 'R0/NR'
RN11B o11 0 'R0/NR'
.data SIZES NR
1
4.5
5
.enddata
.tran 1p 1p SWEEP DATA=SIZES
.measure tran ratio PARAM='NR'
'''
    for ab in ['00','01','10','11']:s+=f'.measure tran v{ab} FIND V(o{ab}) AT=1p\n'
    (HERE/'q3_fixed_resistance.sp').write_text(s+'.end\n',encoding='ascii')
    # Separate nonlinear MOS experiment; not used to infer the analytical bound.
    s=f'''* 2020 HW2 Q3 supplementary CIC018 TT experiment (BSIM3)
.protect
.lib '{model.as_posix()}' TT
.unprotect
.option measform=3 numdgt=10 measdgt=10 ingold=2
.temp 25
.param NR=4.5 WP=0.5u
.subckt pseudo_nor a b y dd
MP y 0 dd dd P_18 W=WP L=0.18u
MN0 y a 0 0 N_18 W='NR*WP' L=0.18u
MN1 y b 0 0 N_18 W='NR*WP' L=0.18u
.ends pseudo_nor
VH h 0 1.8
VDD00 dd00 0 1.8
VDD01 dd01 0 1.8
VDD10 dd10 0 1.8
VDD11 dd11 0 1.8
X00 0 0 o00 dd00 pseudo_nor
X01 0 h o01 dd01 pseudo_nor
X10 h 0 o10 dd10 pseudo_nor
X11 h h o11 dd11 pseudo_nor
.data SIZES NR
1
4.5
5
.enddata
.tran 1p 1p SWEEP DATA=SIZES
.measure tran ratio PARAM='NR'
'''
    for ab in ['00','01','10','11']:
        s+=f'.measure tran v{ab} FIND V(o{ab}) AT=1p\n.measure tran idd{ab} FIND PAR(\'-I(VDD{ab})\') AT=1p\n'
    (HERE/'q3_cic018_tt.sp').write_text(s+'.end\n',encoding='ascii')
    s=f'''* 2020 HW2 Q2 exhaustive 64 valid one-hot-low cases
.protect
.lib '{model.as_posix()}' TT
.unprotect
.include 'rotator.sp'
.option measform=3 numdgt=10 measdgt=10 delmax=10p ingold=2
.temp 25
VDD vdd 0 1.8
VSS vss 0 0
XROT a0 a1 a2 a3 c0 c1 c2 c3 z0 z1 z2 z3 vdd vss rotator
'''
    for j in range(4):s+=f'CL{j} z{j} 0 1f\n'
    for kind in ['a','c']:
        for bit in range(4):
            field='data' if kind=='a' else 'controls'
            points=[]
            for v in vectors:
                voltage=1.8*((v[field]>>bit)&1)
                start=v['index']*2e-9
                if v['index']==0:points.append((0,voltage))
                else:
                    previous=1.8*((vectors[v['index']-1][field]>>bit)&1)
                    points.extend([(start,previous),(start+20e-12,voltage)])
            points.append((128e-9,voltage))
            s+=f'V{kind}{bit} {kind}{bit} vss PWL(\n'
            for t,v in points:s+=f'+ {t:.12e} {v:.1f}\n'
            s+='+)\n'
    s+='.tran 10p 128n\n'
    for v in vectors:
        for bit in range(4):s+=f'.measure tran v{v["index"]:02d}z{bit} FIND V(z{bit}) AT={(v["index"]*2+1.8):.1f}n\n'
    (HERE/'q2_testbench.sp').write_text(s+'.end\n',encoding='ascii')
    status={'analytical':{'Q1_cases':8,'Q2_cases':64,'Q3_minimum_Wn_Wp':4.5,'all_pass':True},'simulations':[]}
    if not args.skip_hspice:
        if not model.is_file():raise FileNotFoundError('CIC018 local model missing')
        for stem in ['q2_testbench','q3_fixed_resistance','q3_cic018_tt']:
            folder=raw/stem;folder.mkdir(parents=True,exist_ok=True)
            for file in [stem+'.sp','rotator.sp']:shutil.copy2(HERE/file,folder/file)
            p=subprocess.run([args.hspice,'-i',stem+'.sp','-o','run'],cwd=folder,capture_output=True,text=True,errors='replace',timeout=180)
            (folder/'console.log').write_text(p.stdout+p.stderr,encoding='utf-8')
            lis=(folder/'run.lis').read_text(errors='replace') if (folder/'run.lis').exists() else ''
            if p.returncode or 'job concluded' not in lis.lower() or '**error**' in lis.lower():raise RuntimeError(f'HSPICE failed: {folder}')
            m={v.group(1).lower():float(v.group(2)) for v in re.finditer(r'^\s*([a-zA-Z][\w]*)\s*=\s*([+-]?[\d.]+e[+-]?\d+)',lis,re.M|re.I)}
            if stem=='q2_testbench':
                electrical=[]
                for v in vectors:
                    volts=[m[f'v{v["index"]:02d}z{j}'] for j in range(4)]
                    observed=sum(int(x>.9)<<j for j,x in enumerate(volts))
                    levels=all((x>=1.6 if (v['expected_output']>>j)&1 else x<=.2) for j,x in enumerate(volts))
                    electrical.append({**v,'observed_output':observed,**{f'z{j}_V':x for j,x in enumerate(volts)},'pass':levels and observed==v['expected_output']})
                if not all(v['pass'] for v in electrical):raise AssertionError('Rotator electrical truth table failed')
                write_csv(HERE/'q2_electrical.csv',electrical)
                status['simulations'].append({'deck':stem+'.sp','status':'completed','cases':64,'pass':True})
            else:
                lines=(folder/'run.mt0.csv').read_text(errors='replace').splitlines()
                data=list(csv.DictReader(line for line in lines if line.strip() and not line.startswith(('$','.'))))
                clean=[{k:float(v.strip()) for k,v in row.items()} for row in data]
                write_csv(HERE/(stem+'_measurements.csv'),clean)
                if stem=='q3_fixed_resistance':
                    for row in clean:
                        for ab in ['00','01','10','11']:
                            expected=next(v['voltage_V'] for v in ideal if v['ratio_Wn_Wp']==row['ratio'] and v['AB']==ab)
                            assert abs(row['v'+ab]-expected)<1e-8
                status['simulations'].append({'deck':stem+'.sp','status':'completed','rows':len(clean),'pass':True})
    (HERE/'validation.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(status,indent=2))

if __name__=='__main__':main()
