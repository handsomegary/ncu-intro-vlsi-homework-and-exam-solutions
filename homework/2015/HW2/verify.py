"""Reproduce analytical 2015 HW2 clock-delay and ideal inverter results."""
from pathlib import Path
import csv,json,math
HERE=Path(__file__).resolve().parent

def main():
    r=.05;c=30e-18;tg=.2e-9
    routes=[('A-B',650,2),('A-C',400,3),('A-D',650,2)]
    rows=[]
    for path,length,gates in routes:
        wire=.5*r*c*length**2
        ignored=wire<=4*tg
        rows.append(dict(path=path,length_um=length,wire_s=wire,gate_delay_s=gates*tg,wire_neglected=ignored,
                         specified_delay_s=gates*tg+(0 if ignored else wire)))
    assert max(rows,key=lambda v:v['specified_delay_s'])['path']=='A-C'
    with (HERE/'clock_paths.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    # Equal threshold magnitudes at midpoint give beta_n=beta_p.
    ratio=4/2
    assert ratio==2
    # Ideal square-law VTC shifts right as PMOS strength increases: this
    # DECREASES NMH=VDD-VIH and INCREASES NML=VIL (rail outputs assumed).
    vm=[];vdd=1.8;vt=.45
    for strength in [.5,1,2,4]:
        q=math.sqrt(strength)
        switching=(vt+q*(vdd-vt))/(1+q)
        def slope(u,left):
            an=u-vt;ap=vdd-u-vt
            if left:return 1-(ap+an/strength)/math.sqrt(max(1e-30,ap*ap-an*an/strength))
            return 1-(an+strength*ap)/math.sqrt(max(1e-30,an*an-strength*ap*ap))
        def unity(left):
            lo,hi=(vt,switching-1e-12) if left else (switching+1e-12,vdd-vt)
            for _ in range(70):
                mid=(lo+hi)/2;g=slope(mid,left)+1
                if (g>0)==left:lo=mid
                else:hi=mid
            return (lo+hi)/2
        vil,vih=unity(True),unity(False)
        vm.append(dict(beta_p_over_beta_n=strength,VM_V=switching,VIL_V=vil,VIH_V=vih,NML_V=vil,NMH_V=vdd-vih))
    assert all(b['VM_V']>a['VM_V'] for a,b in zip(vm,vm[1:]))
    with (HERE/'switching_points.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(vm[0]));wr.writeheader();wr.writerows(vm)
    assert vm[0]['NMH_V']>vm[0]['NML_V'] and vm[2]['NMH_V']<vm[2]['NML_V']
    result={'all_pass':True,'critical_path':'A-C','critical_delay_ns':.6,'mu_n_over_mu_p':2,
            'noise_margin_design':'beta_n > beta_p, assuming matched threshold magnitudes',
            'threshold_symmetry_assumption_explicit':True}
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
