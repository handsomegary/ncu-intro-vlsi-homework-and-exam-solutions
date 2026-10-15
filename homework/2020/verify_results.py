"""Validate the committed 2020 evidence without requiring a simulator license.

In addition to table-level checks, independently interpolate the sampled
waveforms and compare the 50-percent propagation delays to HSPICE .MEASURE.
"""
from pathlib import Path
import csv,json,hashlib
from collections import defaultdict
HERE=Path(__file__).resolve().parent

def rows(path):
    with path.open(newline='') as f:return list(csv.DictReader(f))

def canonical_text_bytes(path):
    # Universal-newline reading makes provenance stable in LF Git clones and
    # CRLF Windows checkouts without modifying the source file.
    return path.read_text(encoding='utf-8').encode('utf-8')

def crossing(trace,node,rising):
    for a,b in zip(trace,trace[1:]):
        if float(a['time_ns'])<1.9:continue
        va,vb=float(a[node+'_V']),float(b[node+'_V'])
        crossed=va<.9<=vb if rising else va>.9>=vb
        if crossed:
            return float(a['time_ns'])+(.9-va)/(vb-va)*(float(b['time_ns'])-float(a['time_ns']))
    raise AssertionError(f'No crossing for {node}')

def main():
    h1=rows(HERE/'HW1/truth_tables.csv')
    assert len(h1)==32 and all(r['expected']==r['observed'] for r in h1)
    h2=rows(HERE/'HW2/q2_electrical.csv')
    assert len(h2)==64 and {int(r['index']) for r in h2}==set(range(64))
    for r in h2:
        data,k=int(r['data']),int(r['active_low_control'])
        expected=sum(((data>>((j+k+1)%4))&1)<<j for j in range(4))
        assert int(r['observed_output'])==expected
        assert int(r['controls'])==15^(1<<k)
        for j in range(4):
            v=float(r[f'z{j}_V'])
            assert v>=1.6 if expected>>j&1 else v<=.2
    resistor=rows(HERE/'HW2/q3_fixed_resistance_measurements.csv')
    assert len(resistor)==3
    for r in resistor:
        ratio=float(r['ratio'])
        for ab in ['00','01','10','11']:
            count=ab.count('1')
            expected=1.8 if not count else 1.8/(2*ratio*count+1)
            assert abs(float(r['v'+ab])-expected)<1e-8
    delays=rows(HERE/'HW3/delays.csv')
    primary=[r for r in delays if r['slew_ps']=='20' and r['step_ps']=='1']
    assert len(delays)==36 and len(primary)==12
    groups=defaultdict(list)
    for r in rows(HERE/'HW3/waveforms.csv'):groups[r['transition']].append(r)
    interpolation=[]
    for r in primary:
        before,after=[int(v,2) for v in r['transition'].split('->')]
        trigger='a' if (before>>1)!=(after>>1) else 'b'
        rise=((after>>1)>(before>>1)) if trigger=='a' else ((after&1)>(before&1))
        output_rise=(after!=3) if r['node']=='f' else (after==3)
        assert r['direction']==('LH' if output_rise else 'HL')
        t_in=crossing(groups[r['transition']],trigger,rise)
        t_out=crossing(groups[r['transition']],r['node'],output_rise)
        interpolated=(t_out-t_in)*1000
        difference=abs(interpolated-float(r['delay_ps']))
        assert difference<.3
        interpolation.append(dict(transition=r['transition'],node=r['node'],hspice_delay_ps=float(r['delay_ps']),
                                  waveform_delay_ps=interpolated,difference_ps=difference))
    with (HERE/'HW3/waveform_delay_checks.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(interpolation[0]));w.writeheader();w.writerows(interpolation)
    checks=rows(HERE/'HW3/level_checks.csv')
    assert len(checks)==36 and all(r['pass_logic_levels']=='True' for r in checks)
    convergence=rows(HERE/'HW3/convergence.csv')
    assert len(convergence)==12 and max(float(r['difference_ps']) for r in convergence)<.2
    for file in ['and2.sp','testbench.sp','delays.csv','worst_delays.csv','level_checks.csv','waveforms.csv','convergence.csv']:
        assert canonical_text_bytes(HERE/'HW3'/file)==canonical_text_bytes(HERE/'HW4'/file),file
    provenance=json.loads((HERE/'HW4/provenance.json').read_text())
    assert provenance['hash_normalization']=='UTF-8 LF'
    assert provenance['netlist_sha256']==hashlib.sha256(canonical_text_bytes(HERE/'HW4/and2.sp')).hexdigest()
    for hw in ['HW1','HW2','HW3','HW4']:
        assert (HERE/hw/'solution.tex').is_file() and (HERE/hw/'solution.pdf').read_bytes().startswith(b'%PDF-')
    summary={'all_pass':True,'HW1_Boolean_cases':32,'HW2_electrical_cases':64,'HW3_HSPICE_delay_rows':36,
             'HW3_independent_waveform_checks':12,'max_waveform_measurement_difference_ps':max(r['difference_ps'] for r in interpolation),
             'HW4_identical_netlist_and_explicit_result_reuse':True,'PDF_reports':4}
    (HERE/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
