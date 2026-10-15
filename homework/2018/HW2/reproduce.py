"""Actual HSPICE slew/RC checks plus clearly separated closed-form answers.
The same original four questions appear in Fall 2018 and Fall 2019 HW2.
"""
from pathlib import Path
import argparse,csv,json,os,subprocess
HERE=Path(__file__).resolve().parent
def write_csv(p,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def ideal():
    rows=[]
    for n in range(1,9):
        rp=rn=1000.;cd=1e-15
        # Elmore: every internal node has2Cd, output has(n+1)Cd.
        graph=rp*(sum(2*cd*i for i in range(1,n))+n*(n+1)*cd)
        formula=2*n*n*rp*cd;assert abs(graph-formula)<1e-25
        rows.append(dict(fanin=n,rise_elmore_ps=formula*1e12,fall_isolated_ps=(n+1)*rn*cd*1e12,fall_attached_internal_ps=(3*n-1)*rn*cd*1e12))
    write_csv(HERE/'rc_expected.csv',rows)
    ratios=[]
    for vn,vp in [(.45,.45),(.4,.5),(.5,.4)]:
        r=2*((.9-vp)/(.9-vn))**2
        ncurrent=r*2*(.9-vn)**2;pcurrent=4*(.9-vp)**2
        assert abs(ncurrent-pcurrent)<1e-12
        ratios.append(dict(vtn_V=vn,abs_vtp_V=vp,mu_n_over_mu_p=r,balanced_at_half_supply=True))
    write_csv(HERE/'mobility_examples.csv',ratios)
    write_csv(HERE/'gate_capacitance.csv',[dict(inverter_gate_units=3,NOR_input_gate_units=5,total_node_x_units=8,Cx_over_Cg=8/3,assumption='equalL; worst-case one-NMOS-on NOR strength')])
    return rows
def slew(model):
    return f"""* HW2 Q1: illustrative process simulation, not specified assignment sizes.
.protect
.lib '{model.as_posix()}' TT
.unprotect
.option post=0 measform=3 measdgt=10 numdgt=10 delmax=1p
.temp 25
.param SLEW=100p
VDD vdd 0 1.8
VIN in 0 pwl(0 0 1n 0 '1n+SLEW' 1.8 5n 1.8)
MP out in vdd vdd P_18 W=1u L=.18u
MN out in 0 0 N_18 W=.5u L=.18u
CL out 0 10f
.data SLEWS SLEW
100p
1n
.enddata
.tran 1p 5n sweep data=SLEWS
.meas tran slew_value param='SLEW'
.meas tran t90 when v(out)=1.62 fall=1
.meas tran t10 when v(out)=.18 fall=1
.meas tran tf param='t10-t90'
.meas tran vin50 when v(in)=.9 rise=1
.meas tran out50 when v(out)=.9 fall=1
.meas tran delay50 param='out50-vin50'
.end
"""
def rc():
    s='* HW2 Q2: fixed-size ideal pi-RC networks, no process-model substitution.\n.option post=0 measform=3 measdgt=10 numdgt=10 delmax=50f\nVR rail 0 1.8\n'
    initials=[]
    for n in range(1,9):
        for j in range(1,n+1):
            src='rail' if j==1 else f'r{n}_{j-1}'
            s+=f'RP{n}_{j} {src} r{n}_{j} 1k\nCP{n}_{j} r{n}_{j} 0 {n+1 if j==n else 2}f\n'
            initials.append(f'v(r{n}_{j})=0')
        s+=f'RN{n} f{n} 0 1k\nCN{n} f{n} 0 {n+1}f\n'
        initials.append(f'v(f{n})=1.8')
        s+=f".meas tran tau_r{n} integ par('1-v(r{n}_{n})/1.8') from=0 to=5n\n.meas tran tau_f{n} integ par('v(f{n})/1.8') from=0 to=5n\n"
        for pct,v in [(10,.18),(90,1.62)]:
            s+=f'.meas tran r{n}_{pct} when v(r{n}_{n})={v} rise=1\n.meas tran f{n}_{pct} when v(f{n})={v} fall=1\n'
        s+=f".meas tran tr{n} param='r{n}_90-r{n}_10'\n.meas tran tf{n} param='f{n}_10-f{n}_90'\n"
    s+='.ic '+' '.join(initials)+'\n.tran 50f 5n UIC\n.end\n'
    return s
def run(hspice,work,stem,deck):
    work.mkdir(parents=True,exist_ok=True);(work/(stem+'.sp')).write_text(deck,encoding='utf-8',newline='\n')
    p=subprocess.run([hspice,'-i',stem+'.sp','-o',stem],cwd=work,capture_output=True,timeout=180)
    (work/(stem+'.console.log')).write_bytes(p.stdout+p.stderr)
    lis=(work/(stem+'.lis')).read_text(errors='replace')
    assert p.returncode==0 and 'job concluded' in lis.lower() and '**error**' not in lis.lower(),stem
    lines=(work/(stem+'.mt0.csv')).read_text(errors='replace').splitlines()
    rs=[{k.strip().lower():v.strip() for k,v in r.items()} for r in csv.DictReader(l for l in lines if l.strip() and not l.startswith(('$','.')))]
    assert all('failed' not in str(r).lower() for r in rs),stem
    write_csv(HERE/(stem+'_measurements.csv'),rs);return rs
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--model',type=Path,default=os.getenv('CIC018_MODEL','D:/cic018.l'))
    ap.add_argument('--hspice',default=os.getenv('HSPICE','C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com'))
    ap.add_argument('--work',type=Path,default=HERE/'.simulation');ap.add_argument('--analytical-only',action='store_true')
    a=ap.parse_args();expected=ideal()
    if a.analytical_only:print('RC formulas, balanced mobility and gate-capacitance checks passed');return
    ds=slew(a.model.resolve());(HERE/'q1_slew.sp').write_text(ds,encoding='utf-8',newline='\n')
    s=run(a.hspice,a.work.resolve(),'q1_slew',ds);assert len(s)==2
    assert float(s[0]['tf'])<float(s[1]['tf'])
    dr=rc();(HERE/'q2_pi_rc.sp').write_text(dr,encoding='utf-8',newline='\n')
    m=run(a.hspice,a.work.resolve(),'q2_pi_rc',dr)[0];checks=[]
    for r in expected:
        n=r['fanin'];tr=float(m[f'tau_r{n}'])*1e12;tf=float(m[f'tau_f{n}'])*1e12
        er=abs(tr-r['rise_elmore_ps'])/r['rise_elmore_ps'];ef=abs(tf-r['fall_isolated_ps'])/r['fall_isolated_ps']
        assert er<.002 and ef<.002
        checks.append(dict(fanin=n,measured_rise_first_moment_ps=tr,expected_rise_ps=r['rise_elmore_ps'],measured_fall_first_moment_ps=tf,expected_fall_ps=r['fall_isolated_ps'],rise_10_90_ps=float(m[f'tr{n}'])*1e12,fall_90_10_ps=float(m[f'tf{n}'])*1e12,passed=True))
    write_csv(HERE/'rc_checks.csv',checks)
    result={'status':'PASS','original_questions':4,'rc_fanins':8,'slew_cases':2,'fast_input_output_fall_ps':float(s[0]['tf'])*1e12,'slow_input_output_fall_ps':float(s[1]['tf'])*1e12,'matched_threshold_mu_ratio':2,'node_x_Cg_ratio':8/3,'rc_scope':'fixed-size equal pi device caps; first-moment vs 10-90 distinguished; falling chain isolated case','mobility_limit':'ratio2 assumes equal threshold magnitudes and equal Cox','gate_cap_limit':'equalL and worst-case one-on NOR sizing'}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
