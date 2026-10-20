"""Analytical checks plus three actual HSPICE measurements, kept distinct."""
from pathlib import Path
import sys as _simulation_sys
_simulation_sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from simulation_environment import default_hspice, default_model, add_environment_check, resolve_simulation_args
import argparse,csv,itertools,json,os,subprocess
HERE=Path(__file__).resolve().parent
def csvwrite(p,rows):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def logical_checks():
    rows=[]
    for a,b,c in itertools.product(range(2),repeat=3):
        d=(not a)^bool(b);e=not(b and c)
        # Independent XOR PDN expression and NAND expression.
        pdn=(not a and b) or (a and not b)
        assert d == (not pdn)
        rows.append({'A':a,'B':b,'C':c,'D':int(d),'E':int(e),'passed':True})
    csvwrite(HERE/'logic.csv',rows)
    ratios=[]
    for r in (2.25,4.5,5.):
        one=1/(1+2*r);two=1/(1+4*r)
        ratios.append({'n_to_p_aspect_ratio':r,'v01_over_vdd':one,'v10_over_vdd':one,'v11_over_vdd':two,'maximum_low_le_0_1':one<=.1+1e-12})
    assert abs(ratios[0]['v11_over_vdd']-.1)<1e-12
    assert abs(ratios[1]['v01_over_vdd']-.1)<1e-12
    csvwrite(HERE/'sizing.csv',ratios)
    return len(rows)
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hspice',default=default_hspice())
    ap.add_argument('--model',type=Path,default=default_model())
    ap.add_argument('--work',type=Path,default=HERE/'.simulation');ap.add_argument('--logic-only',action='store_true')
    add_environment_check(ap);a=ap.parse_args();resolve_simulation_args(ap,a,skip=a.logic_only);n=logical_checks()
    if a.logic_only:print(f'{n} logic checks; sizing checks passed');return
    a.work=a.work.resolve();a.work.mkdir(parents=True,exist_ok=True);status=[]
    for stem in ('q2_retention','q3_resistance','q3_cic018'):
        deck=(HERE/(stem+'.sp')).read_text().replace('D:/cic018.l',a.model.resolve().as_posix());(a.work/(stem+'.sp')).write_text(deck)
        p=subprocess.run([a.hspice,'-i',stem+'.sp','-o',stem],cwd=a.work,capture_output=True,timeout=180)
        (a.work/(stem+'.console.log')).write_bytes(p.stdout+p.stderr)
        lis=(a.work/(stem+'.lis')).read_text(errors='replace')
        assert p.returncode==0 and 'job concluded' in lis.lower() and '**error**' not in lis.lower()
        lines=(a.work/(stem+'.mt0.csv')).read_text().splitlines()
        rows=[{k.strip():v.strip() for k,v in r.items()} for r in csv.DictReader(l for l in lines if l.strip() and not l.startswith(('$','.')))]
        assert all('failed' not in str(r).lower() for r in rows)
        csvwrite(HERE/(stem+'_measurements.csv'),rows);status.append({'deck':stem+'.sp','status':'PASS','rows':len(rows)})
        if stem=='q2_retention':assert abs(float(rows[0]['retention'])-.009)<1e-7
        elif stem=='q3_resistance':
            for k,expected in [('v00',1.8),('v01',.18),('v10',.18),('v11',1.8/19)]:assert abs(float(rows[0][k])-expected)<1e-8
    summary={'status':'PASS','logic_rows':n,'analytical_retention_example_ms':9.,'retention_example':'Vdd=1.8V, Vt=0.45V, C=20fF, IL=1pA; illustrative only','runs':status,'multi_vt_scope':'symbolic topology and gate-level timing only; CIC TT library provides no separate high/low threshold pair','literal_minimum_low_ratio':2.25,'conventional_maximum_low_ratio':4.5}
    (HERE/'validation.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
