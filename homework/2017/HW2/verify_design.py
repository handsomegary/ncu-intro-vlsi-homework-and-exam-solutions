"""2017 HW2 symbolic/numerical calculator and consistency checks.
All defaults are declared examples, not process-model measurements.
"""
from pathlib import Path
import argparse,json,math
H=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--rn',type=float,default=1000);p.add_argument('--rp',type=float,default=2000);p.add_argument('--cf-ff',type=float,default=10);p.add_argument('--cz-ff',type=float,default=5);p.add_argument('--vdd',type=float,default=1.8);p.add_argument('--vtn',type=float,default=.4);p.add_argument('--vtp-abs',type=float,default=.4);p.add_argument('--beta-p-over-n',type=float,default=1);a=p.parse_args()
assert all(v>0 for v in [a.rn,a.rp,a.cf_ff,a.cz_ff,a.vdd,a.beta_p_over_n])
fhl=2*a.rn*a.cf_ff*1e-15;flh=a.rp*a.cf_ff*1e-15
zhl=flh+a.rn*a.cz_ff*1e-15;zlh=fhl+a.rp*a.cz_ff*1e-15
u_n=a.vdd/2-a.vtn;u_p=a.vdd/2-a.vtp_abs
if min(u_n,u_p)<=0:raise ValueError('Both devices must conduct at the midpoint')
mu_ratio=2*(u_p/u_n)**2
cx=(2+6*a.beta_p_over_n)/(1+2*a.beta_p_over_n)
q=dict(provenance='analytical, declared example values',inputs=vars(a),elmore_time_constant_ps={k:v*1e12 for k,v in [('F_HL',fhl),('F_LH',flh),('Z_HL',zhl),('Z_LH',zlh)]},approx_50_percent_delay_ps={k:math.log(2)*v*1e12 for k,v in [('F_HL',fhl),('F_LH',flh),('Z_HL',zhl),('Z_LH',zlh)]},mu_n_over_mu_p=mu_ratio,Cx_over_Cg=cx,matched_thresholds=math.isclose(a.vtn,a.vtp_abs),balanced_inverter=math.isclose(a.beta_p_over_n,1))
if a.beta_p_over_n==1:assert abs(cx-8/3)<1e-12
if a.vtn==a.vtp_abs:assert mu_ratio==2
(H/'verification.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2))
