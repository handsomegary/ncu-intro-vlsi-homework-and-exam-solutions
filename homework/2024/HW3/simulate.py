"""Reproduce HW3: real HSPICE, exact instructor PWL, 512 electrical cases.

No process model is distributed. Set CIC018_MODEL and HSPICE or use CLI flags.
Raw simulator files stay in --work; only derived data enter --results.
"""
from pathlib import Path
import argparse, csv, json, os, re, subprocess, hashlib

HERE = Path(__file__).absolute().parent
SIGNALS = ['s0', 's1', 's2', 's3', 'cout']
VECTORS = [(0,0),(1,5),(15,13),(11,9),(4,8),(3,7),(12,14),(2,15),(6,10)]
CANDIDATES = [
    ('reference88', 88, .47, .47, .47, .24),
    ('full80_min', 80, .47, .47, .47, .18),
    ('full80_p94', 80, .47, .94, .47, .18),
    ('full80_t70', 80, .47, .47, .70, .18),
    ('compact64_min', 64, .47, .47, .47, .18),
    ('compact64_p70', 64, .47, .70, .47, .18),
]

def circuit(count=64, wn=.47, wp=.47, wt=.47, lg=.18):
    """All variants preserve Figure 1's two-XNOR and carry-mux graph."""
    s = f'''* Figure 1 serial-parallel multiplexer-based adder, {count} MOSFETs.
* Dimensions in micrometres; global rails vdd/vss provided by testbench.
.param WN={wn}u WP={wp}u WT={wt}u LG={lg}u
.subckt inv a z
MP z a vdd vdd P_18 W=WP L=LG
MN z a vss vss N_18 W=WN L=LG
.ends inv
.subckt tg a z s sb
MP z sb a vdd P_18 W=WT L=LG
MN z s a vss N_18 W=WT L=LG
.ends tg
.subckt mux_fa x y ci s co
'''
    if count == 64:
        s += '''* Compact 4T upper XNOR: e can be threshold-degraded internally.
MPU0 ep x vdd vdd P_18 W=WP L=LG
MPU1 e y ep vdd P_18 W=WP L=LG
MNU0 e y x vss N_18 W=WN L=LG
MNU1 e x y vss N_18 W=WN L=LG
'''
    else:
        s += '''* Full-swing 8T upper XNOR.
XI0 x xb inv
XI1 y yb inv
XT0 x e y yb tg
XT1 xb e yb y tg
'''
    s += '''XI2 e en inv
XI3 ci cib inv
* Lower XNOR uses ci/cib as DATA; e/en as SELECT.
* This choice restores the external sum even when compact e is degraded.
XT2 ci s e en tg
XT3 cib s en e tg
'''
    if count == 88:
        s += 'XI4 e enc inv\n'
        cb = 'enc'
    else:
        cb = 'en'
    s += f'''* Carry: co = e ? y : ci. Shared complementary select.
XT4 y co e {cb} tg
XT5 ci co {cb} e tg
.ends mux_fa
.subckt four_bit_multbased_adder cin x0 x1 x2 x3 y0 y1 y2 y3 s0 s1 s2 s3 cout
XF0 x0 y0 cin s0 c1 mux_fa
XF1 x1 y1 c1 s1 c2 mux_fa
XF2 x2 y2 c2 s2 c3 mux_fa
XF3 x3 y3 c3 s3 cout mux_fa
.ends four_bit_multbased_adder
'''
    # The reference's second XNOR selects by ci and passes e/en.
    if count == 88:
        s=s.replace('XT2 ci s e en tg\nXT3 cib s en e tg',
                    'XT2 e s ci cib tg\nXT3 en s cib ci tg')
    return s

def area(count,wn,wp,wt,lg):
    # 64T: 4 PMOS + 4 NMOS + 8 TG MOS per bit. 80T: 4+4+12.
    # 88T: the same plus a redundant 2T inverter per bit.
    ni, nt = (16,32) if count==64 else ((16,48) if count==80 else (20,48))
    return lg*(ni*wn + ni*wp + nt*wt)

def header(model):
    return f"* HW3 measurement deck\n.protect\n.lib '{model.as_posix()}' tt\n.unprotect\n.include 'adder.sp'\n.global vdd vss\nvvdd vdd 0 dc 1.8\nvvss vss 0 dc 0\n"

def run(hspice, folder, deck):
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'testbench.sp').write_text(deck,encoding='ascii')
    p=subprocess.run([hspice,'-i','testbench.sp','-o','run'],cwd=folder,
                     capture_output=True,text=True,errors='replace')
    (folder/'console.log').write_text(p.stdout+p.stderr,encoding='utf-8')
    lis=(folder/'run.lis').read_text(errors='replace') if (folder/'run.lis').exists() else ''
    if p.returncode or 'job concluded' not in lis.lower() or '**error**' in lis.lower():
        raise RuntimeError(f'HSPICE failed: {folder}; inspect local console.log / run.lis')
    return lis

def measurements(lis):
    return {m.group(1).lower():float(m.group(2)) for m in
            re.finditer(r'^\s*([a-zA-Z][\w]*)\s*=\s*([+-]?[\d.]+e[+-]?\d+)',lis,re.M|re.I)}

def trace(path):
    """Read HSPICE LIS_NEW .printtr0 blocks, which split after 4 variables."""
    lines=path.read_text(errors='replace').splitlines(); rows={}; names=[]; armed=False
    for i,line in enumerate(lines):
        if line.strip().lower().startswith('time '):
            names=lines[i+1].lower().split(); armed=True; continue
        if not armed: continue
        fields=line.split()
        try: nums=[float(x.replace('D','e')) for x in fields]
        except ValueError: continue
        if len(nums)==len(names)+1 and nums:
            rows.setdefault(nums[0],{}).update(dict(zip(names,nums[1:])))
    return [(t,d) for t,d in sorted(rows.items()) if all(n in d for n in SIGNALS)]

def interpolate(rows,t,node):
    import bisect
    ts=[r[0] for r in rows]; k=bisect.bisect_left(ts,t)
    if k==0:return rows[0][1][node]
    if k==len(rows):return rows[-1][1][node]
    a,b=rows[k-1],rows[k]
    return a[1][node]+(b[1][node]-a[1][node])*(t-a[0])/(b[0]-a[0])

def metrics(rows):
    samples=[]; delays=[]
    for k,(x,y) in enumerate(VECTORS[1:],1):
        sample_t=(k+.8)*1e-9; expected=x+y
        volts=[interpolate(rows,sample_t,n) for n in SIGNALS]
        bits=[v>.9 for v in volts]; got=sum(int(b)<<i for i,b in enumerate(bits))
        levels=all((v>=1.6 if expected>>i&1 else v<=.2) for i,v in enumerate(volts))
        sample={'vector':k,'x':x,'y':y,'expected':expected,'observed':got,'pass':got==expected and levels}
        sample.update({n+'_v':v for n,v in zip(SIGNALS,volts)})
        samples.append(sample)
        previous=sum(VECTORS[k-1])
        for bit,node in enumerate(SIGNALS):
            if ((previous>>bit)&1)==((expected>>bit)&1):continue
            crossings=[]
            for a,b in zip(rows,rows[1:]):
                if a[0] < (k-.1)*1e-9 or b[0] > (k+.9)*1e-9:continue
                va,vb=a[1][node],b[1][node]
                if (va-.9)*(vb-.9)<0:
                    crossings.append(a[0]+(.9-va)/(vb-va)*(b[0]-a[0]))
            if not crossings: raise RuntimeError(f'Missing crossing vector {k} {node}')
            end=max(crossings)
            delays.append({'vector':k,'x':x,'y':y,'output':node,
                           'direction':'rise' if expected>>bit&1 else 'fall',
                           'input_50_ns':k-.05,'output_50_ns':end*1e9,
                           'delay_ps':(end-(k-.05)*1e-9)*1e12})
    return samples,delays

def settling_metrics(rows):
    result=[]
    for k,(x,y) in enumerate(VECTORS[1:],1):
        target=x+y; old=sum(VECTORS[k-1])
        for bit,node in enumerate(SIGNALS):
            high=bool(target>>bit&1); changed=bool((target^old)>>bit&1)
            section=[(t,d[node]) for t,d in rows if (k-.1)*1e-9<=t<=(k+.8)*1e-9]
            crossings=sum((a[1]-.9)*(b[1]-.9)<0 for a,b in zip(section,section[1:]))
            bad=[j for j,(t,v) in enumerate(section) if (v<1.6 if high else v>.2)]
            # Conservative 1 ps sampled band-settling bound, including unchanged-output glitches.
            if not bad: settle=section[0][0]
            elif bad[-1]+1<len(section):settle=section[bad[-1]+1][0]
            else:settle=None
            result.append(dict(vector=k,output=node,expected_bit=int(high),expected_change=changed,
                               crossings_50pct=crossings,
                               extra_crossings=max(0,crossings-int(changed)),
                               settled=settle is not None,
                               settling_delay_ps=max(0,(settle-(k-.05)*1e-9)*1e12) if settle is not None else None))
    return result

def write_csv(p,rows):
    if not rows:return
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader();w.writerows(rows)

def exhaustive_deck(model):
    cases=[(x,y,c) for c in range(2) for x in range(16) for y in range(16)]
    s=header(model)
    for bit,node in enumerate(['x0','x1','x2','x3','y0','y1','y2','y3','cin']):
        vals=[(x>>bit&1) if bit<4 else ((y>>(bit-4)&1) if bit<8 else c) for x,y,c in cases]
        points=['0n '+str(1.8*vals[0])]
        for k in range(1,len(cases)):
            if vals[k]!=vals[k-1]:
                points.extend([f'{2*k-.1:g}n {1.8*vals[k-1]:g}',f'{2*k:g}n {1.8*vals[k]:g}'])
        s+=f'v{node} {node} 0 pwl(\n'
        for j in range(0,len(points),6):s+='+ '+' '.join(points[j:j+6])+'\n'
        s+='+)\n'
    s+='XADDER CIN X0 X1 X2 X3 Y0 Y1 Y2 Y3 S0 S1 S2 S3 COUT four_bit_multbased_adder\n'
    s+='.temp 25\n.option lis_new=1 ingold=2 measdgt=8\n.tran 10p 1024n\n'
    for k in range(512):
        for node in SIGNALS:
            s+=f'.meas tran q{k}_{node} find v({node}) at={2*k+1.8:g}n\n'
    return s+'.end\n',cases

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--model',default=os.getenv('CIC018_MODEL','D:/cic018.l'))
    ap.add_argument('--hspice',default=os.getenv('HSPICE',r'C:\synopsys\Hspice_S-2021.09\WIN64\hspice.com'))
    ap.add_argument('--work',type=Path,default=HERE/'.simulation')
    ap.add_argument('--results',type=Path,default=HERE/'results')
    ap.add_argument('--selected',default='compact64_min')
    args=ap.parse_args(); model=Path(args.model).absolute(); args.work=args.work.absolute()
    if not model.is_file():raise FileNotFoundError('Set CIC018_MODEL to the licensed CIC018 library.')
    args.results.mkdir(parents=True,exist_ok=True)
    instructor=(HERE/'testbench.sp').read_text()
    stimulus='\n'.join(line for line in instructor.splitlines() if re.match(r'^v[xy]|^vcin',line,re.I))+'\n'
    common=header(model)+stimulus+'XADDER CIN X0 X1 X2 X3 Y0 Y1 Y2 Y3 S0 S1 S2 S3 COUT four_bit_multbased_adder\n'
    common+=".meas tran pwr avg power from=0 to=9n\n.meas tran psupply avg par('-v(vdd)*i(vvdd)') from=0 to=9n\n"
    common+='.temp 25\n.option lis_new=1 ingold=2 numdgt=8 measdgt=8 delmax=1p\n.tran 1p 9n\n.print tran v(s0) v(s1) v(s2) v(s3) v(cout) i(vvdd)\n.end\n'
    summaries=[]; selected=None
    for name,count,wn,wp,wt,lg in CANDIDATES:
        folder=args.work/name; folder.mkdir(parents=True,exist_ok=True)
        (folder/'adder.sp').write_text(circuit(count,wn,wp,wt,lg))
        lis=run(args.hspice,folder,common); m=measurements(lis)
        rows=trace(folder/'run.printtr0'); samples,delays=metrics(rows)
        a=area(count,wn,wp,wt,lg); worst=max(delays,key=lambda d:d['delay_ps'])
        summary=dict(candidate=name,transistors=count,wn_um=wn,wp_um=wp,wt_um=wt,l_um=lg,
                     area_um2=a,pavg_total_uW=m['pwr']*1e6,pavg_supply_uW=m['psupply']*1e6,
                     energy_9ns_fJ=m['pwr']*9e6,worst_delay_ps=worst['delay_ps'],
                     energy_area_fJ_um2=m['pwr']*9e6*a,
                     delay_power_fJ=worst['delay_ps']*m['pwr']*1e3,passed_vectors=sum(d['pass'] for d in samples))
        summaries.append(summary);print(json.dumps(summary),flush=True)
        if name==args.selected:
            selected=(name,count,wn,wp,wt,lg)
            selected_samples=samples
            selected_settling=settling_metrics(rows)
            write_csv(args.results/'vectors.csv',samples);write_csv(args.results/'delays.csv',delays)
            write_csv(args.results/'settling.csv',selected_settling)
            write_csv(args.results/'waveform.csv',[dict(time_s=t,**{n:d[n] for n in SIGNALS},i_vdd_A=d['vvdd']) for t,d in rows])
    if selected is None:raise ValueError('selected candidate not found')
    write_csv(args.results/'candidates.csv',summaries)
    name,count,wn,wp,wt,lg=selected
    (HERE/'four_bit_multbased_adder.sp').write_text(circuit(count,wn,wp,wt,lg))
    folder=args.work/'exhaustive';folder.mkdir(parents=True,exist_ok=True)
    (folder/'adder.sp').write_text(circuit(count,wn,wp,wt,lg))
    deck,cases=exhaustive_deck(model); m=measurements(run(args.hspice,folder,deck))
    checks=[]
    for k,(x,y,c) in enumerate(cases):
        expected=x+y+c; volts=[m[f'q{k}_{n}'] for n in SIGNALS]
        got=sum(int(v>.9)<<i for i,v in enumerate(volts))
        levels=all((v>=1.6 if expected>>i&1 else v<=.2) for i,v in enumerate(volts))
        checks.append(dict(x=x,y=y,cin=c,expected=expected,observed=got,
                           passed=(got==expected and levels),**{n+'_v':v for n,v in zip(SIGNALS,volts)}))
    write_csv(args.results/'exhaustive_512.csv',checks)
    # Also run the supplied instructor .tran 0.1ns 9n, without refined DELMAX.
    folder=args.work/'instructor_exact';folder.mkdir(parents=True,exist_ok=True)
    (folder/'adder.sp').write_text(circuit(count,wn,wp,wt,lg))
    exact=re.sub(r"\.lib\s+'[^']+'\s+tt",f".lib '{model.as_posix()}' tt",instructor,flags=re.I)
    exact=exact.replace(".include 'four_bit_multbased_adder.sp'",".include 'adder.sp'")
    exact=exact.replace('.end',".meas tran psupply avg par('-v(vdd)*i(vvdd)') from=0 to=9n\n.option lis_new=1 ingold=2 measdgt=8\n.end")
    exact_m=measurements(run(args.hspice,folder,exact))
    exact_info=dict(pavg_total_uW=exact_m['pwr']*1e6,pavg_supply_uW=exact_m['psupply']*1e6,
                    energy_9ns_fJ=exact_m['pwr']*9e6,tstep_ps=100,delmax='HSPICE automatic')
    (args.results/'instructor_exact.json').write_text(json.dumps(exact_info,indent=2)+'\n')
    lows=[r[n+'_v'] for r in checks for i,n in enumerate(SIGNALS) if not r['expected']>>i&1]
    highs=[r[n+'_v'] for r in checks for i,n in enumerate(SIGNALS) if r['expected']>>i&1]
    meta=dict(selected_candidate=name,hspice_version='S-2021.09 win64',corner='TT',temperature_C=25,
              supply_V=1.8,load='No added output load; instructor testbench',
              simulation_date='2026-10-13',model_sha256=hashlib.sha256(model.read_bytes()).hexdigest(),
              model_in_repository=False,exhaustive_cases=512,exhaustive_passes=sum(r['passed'] for r in checks),
              max_logic_low_V=max(lows),min_logic_high_V=min(highs),
              candidates=summaries,delay_definition='Last 50% output crossing minus common input 50% crossing in each required vector transition; only expected-changing outputs.')
    meta['instructor_exact']=exact_info
    meta['required_vectors_max_low_V']=max(r[n+'_v'] for r in selected_samples for i,n in enumerate(SIGNALS) if not r['expected']>>i&1)
    meta['required_vectors_min_high_V']=min(r[n+'_v'] for r in selected_samples for i,n in enumerate(SIGNALS) if r['expected']>>i&1)
    meta['max_band_settling_delay_ps']=max(r['settling_delay_ps'] for r in selected_settling)
    meta['total_extra_50pct_crossings']=sum(r['extra_crossings'] for r in selected_settling)
    (args.results/'summary.json').write_text(json.dumps(meta,indent=2)+'\n')
    if meta['exhaustive_passes']!=512:raise RuntimeError('Electrical exhaustive validation failed')
    print('PASS: 512/512 electrical cases; public results contain no process model or license metadata.')

if __name__=='__main__':main()
