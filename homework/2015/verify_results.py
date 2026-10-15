"""Check published 2015 question PDFs and numerical evidence without a simulator license."""
from pathlib import Path
from collections import defaultdict
import csv,json,hashlib,math
HERE=Path(__file__).resolve().parent

def rows(path):
    with path.open(newline='') as f:return list(csv.DictReader(f))

def crossing(points,node,rising,start,end):
    for a,b in zip(points,points[1:]):
        ta,tb=float(a['time_ns']),float(b['time_ns'])
        if ta<start or tb>end:continue
        va,vb=float(a[node+'_V']),float(b[node+'_V'])
        if (va<.9<=vb) if rising else (va>.9>=vb):return ta+(.9-va)/(vb-va)*(tb-ta)
    raise AssertionError(f'Missing {node} crossing')

def value(word,node):
    total=sum((word>>i)&1 for i in range(3))
    return int(total>=2) if node=='co' else (int(total<2) if node=='nco' else total&1)


REPO_ROOT=HERE.parents[1]
CATALOG=HERE.parent/'PROMPTS.json'
EXPECTED={(2015,h) for h in range(1,5)}
def public_prompt_integrity():
    catalog=json.loads(CATALOG.read_text(encoding='utf-8-sig'))
    selected=[p for p in catalog['prompts'] if (p['year'],p['homework']) in EXPECTED]
    assert {(p['year'],p['homework']) for p in selected}==EXPECTED,'Question PDF coverage'
    for prompt in selected:
        path=(REPO_ROOT/prompt['path']).resolve()
        assert path.is_relative_to((REPO_ROOT/'homework').resolve()),'Question PDF path'
        data=path.read_bytes()
        assert data.startswith(b'%PDF-'),'Question PDF format'
        assert hashlib.sha256(data).hexdigest()==prompt['sha256'],'Question PDF SHA256'
    print(f'PASS: {len(selected)} published question PDF hashes.')
    return {'status':'PASS','checked':len(selected)}

def main():
    prompt_integrity=public_prompt_integrity()
    h1=rows(HERE/'HW1/truth_tables.csv');assert len(h1)==32
    for r in h1:
        bits=[int(x) for x in r['input_bits']]
        if r['problem']=='Q3':
            a,b,c=bits;expected=int((not a and (b or not c)) or (a and not b and c))
        elif r['problem']=='Q4a':
            w,x,y,z=bits;expected=int(not((w and not(x or y)) or (y and z)))
        else:
            x,y,z=bits;expected=int(sum(bits)<2)
        assert int(r['expected'])==int(r['actual'])==expected
    clocks=rows(HERE/'HW2/clock_paths.csv')
    assert len(clocks)==3
    for r in clocks:
        assert math.isclose(float(r['wire_s']),.5*.05*30e-18*float(r['length_um'])**2,rel_tol=1e-12)
        assert r['wire_neglected']=='True'
    assert max(clocks,key=lambda r:float(r['specified_delay_s']))['path']=='A-C'
    margins=rows(HERE/'HW2/switching_points.csv')
    assert float(margins[0]['NMH_V'])>float(margins[0]['NML_V'])
    assert float(margins[2]['NMH_V'])<float(margins[2]['NML_V'])
    ad=rows(HERE/'HW3/and_delays.csv');assert len(ad)==24 and all(float(r['delay_ps'])>0 for r in ad)
    ac=rows(HERE/'HW3/and_level_checks.csv');assert len(ac)==24 and all(r['pass_level']=='True' for r in ac)
    power=rows(HERE/'HW3/power_vs_load.csv')
    assert [float(r['load_pF']) for r in power]==[.1,.3,.5,.7,1]
    for r in power:
        assert 'LX4' in r['definition'] and 'intrinsic channel' in r['definition']
        p=float(r['Psc_overlap_W']);assert p>0
        assert abs(float(r['overlap_cycle_energy_J'])/100e-9-p)<1e-12
        assert abs(float(r['trace_integration_power_W'])-p)<1e-9
        assert math.isclose(float(r['Psw_external_W']),float(r['load_pF'])*1e-12*1.8**2/100e-9,rel_tol=1e-12)
        assert float(r['settled_high_V'])>=1.6 and float(r['settled_low_V'])<=.2
    assert all(float(b['Psc_overlap_W'])<float(a['Psc_overlap_W']) for a,b in zip(power,power[1:]))
    summary=json.loads((HERE/'HW4/verification.json').read_text())
    for kind,count in [('mirror',28),('domino',38)]:
        text=(HERE/'HW4'/f'{kind}.sp').read_text(encoding='utf-8')
        devices=[l.split() for l in text.splitlines() if l.startswith('M')]
        assert len(devices)==summary[kind]['device_count']==count
        for d in devices:assert d[4]==('vdd' if d[5]=='P_18' else 'vss')
        assert hashlib.sha256(text.encode('utf-8')).hexdigest()==summary[kind]['netlist_SHA256_UTF8_LF']
        logic=rows(HERE/'HW4'/f'{kind}_logic.csv')
        assert len(logic)==(112 if kind=='mirror' else 24)
        for r in logic:
            word=int(r['inputs_after'] if kind=='mirror' else r['input_bits'],2)
            expected=value(word,r['node']);assert expected==int(r['expected'])
            voltage=float(r['voltage_V'] if kind=='mirror' else r['evaluate_V'])
            assert voltage>=1.6 if expected else voltage<=.2
            if kind=='domino':assert float(r['reset_V'])<=.2
        fine=rows(HERE/'HW4'/f'{kind}_fine_delays.csv')
        assert len(fine)==(64 if kind=='mirror' else 24)
        for node in ['co','s']:
            tr=max(float(r['slew_10_90_ps']) for r in fine if r['node']==node and r['direction']=='LH')
            tf=max(float(r['slew_10_90_ps']) for r in fine if r['node']==node and r['direction']=='HL')
            assert abs(tr-tf)/max(tr,tf)<.03
    # Independently interpolate the exported voltage traces for every headline
    # worst-case value. This catches swapped trigger/output/direction labels.
    comparisons=[]
    for kind in ['mirror','domino']:
        groups=defaultdict(list)
        for r in rows(HERE/'HW4'/f'{kind}_waveforms.csv'):groups[int(r['case'])].append(r)
        for r in summary[kind]['worst_delays']:
            points=groups[r['case']]
            up=r['direction']=='LH'
            if kind=='mirror':
                old,new=int(r['inputs_before'],2),int(r['inputs_after'],2)
                trigger,bit=next((n,i) for n,i in [('a',2),('b',1),('ci',0)] if ((old>>i)&1)!=((new>>i)&1))
                tin=crossing(points,trigger,bool((new>>bit)&1),1.9,2.4)
                tout=crossing(points,r['node'],up,1.9,2.6)
            else:
                start,end=(1.9,3.9) if up else (3.9,4.44)
                tin=crossing(points,'clock',up,start,end);tout=crossing(points,r['node'],up,start,end)
            delay=(tout-tin)*1000;difference=abs(delay-r['delay_ps']);assert difference<.2
            comparisons.append(dict(kind=kind,case=r['case'],node=r['node'],direction=r['direction'],HSPICE_delay_ps=r['delay_ps'],waveform_delay_ps=delay,difference_ps=difference))
    with (HERE/'HW4/waveform_delay_checks.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(comparisons[0]));wr.writeheader();wr.writerows(comparisons)
    for n in range(1,5):
        assert (HERE/f'HW{n}/solution.tex').is_file() and (HERE/f'HW{n}/solution.pdf').read_bytes().startswith(b'%PDF-')
    result={'all_pass':True,'scope':'Published question PDF hashes and independent numerical checks.',
            'public_question_PDFs':prompt_integrity['checked'],'standalone_reports':4,'HW1_boolean_cases':32,'HW2_analytical_checks':True,
            'HW3_AND_delay_rows':24,'HW3_intrinsic_channel_power_loads':5,'HW4_mirror_transitions':56,'HW4_domino_evaluate_words':8,
            'HW4_worstcase_independent_waveform_checks':8,'max_waveform_delay_difference_ps':max(r['difference_ps'] for r in comparisons),
            'HW4_rise_fall_slew_balance_below_3_percent':True,'model_not_distributed':True}
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
