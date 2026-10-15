"""Validate published 2020/2021/2023 question PDFs, report coverage and saved numerical evidence. No simulator is launched."""
from pathlib import Path
import csv,hashlib,itertools,json,math
ROOT=Path(__file__).resolve().parent/'homework'
def require(ok,message):
    if not ok:raise AssertionError(message)
def js(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def rows(p):
    with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def canonical(p):return (ROOT/p).read_bytes().replace(b'\r\n',b'\n')
def levels(values,expected):
    return all(math.isfinite(v) and (1.6<=v<=1.82 if (expected>>j)&1 else -.02<=v<=.2) for j,v in enumerate(values))
REPO_ROOT=ROOT.parent
CATALOG=ROOT/'PROMPTS.json'
EXPECTED={(year,h) for year in (2020,2021,2023) for h in range(1,5)}
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
    public_prompt_integrity()
    for year in ['2020','2021','2023']:
        for h in range(1,5):
            p=ROOT/year/f'HW{h}'
            require((p/'solution.tex').is_file() and (p/'solution.pdf').read_bytes().startswith(b'%PDF-'),f'{year} HW{h} report')
            require((p/'README.md').is_file(),f'{year} HW{h} README')
        require((ROOT/year/'SOURCES.md').is_file(),f'{year} source review')
        for p in (ROOT/year).rglob('*'):
            require(not p.is_file() or p.suffix.lower() not in {'.l','.lic','.gds','.pex'},f'Out-of-scope artifact {p}')
    for year in ['2020','2021']:
        require(js(year+'/HW1/verification.json')['all_pass'],f'{year} HW1 status')
        h1=rows(year+'/HW1/truth_tables.csv')
        require(len(h1)==32 and all(r['expected']==r['observed'] for r in h1),f'{year} HW1 rows')
        require(canonical(year+'/HW3/and2.sp')==canonical(year+'/HW4/and2.sp'),f'{year} HW4 netlist differs')
    r20=rows('2020/HW2/q2_electrical.csv')
    require(len(r20)==64,'2020 rotator count')
    for r in r20:
        d,k=int(r['data']),int(r['active_low_control'])
        expected=sum((d>>((j+k+1)%4)&1)<<j for j in range(4))
        require(int(r['controls'])==15^(1<<k),'2020 control encoding')
        require(int(r['observed_output'])==expected and levels([float(r[f'z{j}_V']) for j in range(4)],expected),'2020 electrical rotation')
    v20=js('2020/HW3/validation.json')
    require(v20['simulator_runs']==18 and v20['all_logic_levels_pass'],'2020 switching checks')
    require(v20['maximum_timestep_difference_ps']<.2,'2020 timestep convergence')
    d20=rows('2020/HW3/delays.csv')
    require(len(d20)==36 and all(float(r['delay_ps'])>0 for r in d20),'2020 delay rows')
    for r in rows('2020/HW3/waveform_delay_checks.csv'):require(float(r['difference_ps'])<.3,'2020 independent waveform delay')
    r21=rows('2021/HW2/results/rotator_electrical.csv')
    require(len(r21)==64,'2021 rotator count')
    for r in r21:
        require(r['passed']=='True','2021 rotator pass')
        d,k=int(r['data']),int(r['rotation'])
        expected=((d<<k)|(d>>(4-k if k else 4)))&15
        require(int(r['expected'])==expected and int(r['observed'])==expected,'2021 rotator integer')
        require(levels([float(r[f'Z{j}_V']) for j in range(4)],expected),'2021 rotator voltage')
    require(js('2021/HW2/results/summary.json')['all_rotator_pass'],'2021 electrical summary')
    for hw in ['HW3','HW4']:
        s=js('2021/'+hw+'/results/summary.json')
        require(s['all_logic_levels_pass'] and len(s['cases'])==3,'2021 simulation status')
        ds=rows('2021/'+hw+'/results/delays.csv')
        require(len(ds)==36 and all(float(r['delay_ps'])>0 for r in ds),'2021 delay rows')
    require(js('2023/HW1/verification.json')['total_functional_output_checks']==284,'2023 HW1 count')
    require(js('2023/HW1/verification.json')['status']=='PASS','2023 HW1 status')
    require(js('2023/HW2/validation.json')['status']=='PASS','2023 HW2 status')
    require(all(r['passed']=='True' for r in rows('2023/HW2/logic.csv')),'2023 HW2 logic')
    r3=rows('2023/HW3/results/exhaustive_128.csv');require(len(r3)==128,'2023 state count')
    seen=set()
    for r in r3:
        state=int(r['state']);expected=(state&7)+((state>>3)&7)+(state>>6);seen.add(state)
        require(int(r['expected'])==expected and int(r['observed'])==expected,'2023 sum expectation')
        require(levels([float(r[n+'_v']) for n in ['s0','s1','s2','cout']],expected),'2023 output bands')
    require(seen==set(range(128)),'2023 coverage')
    trs=rows('2023/HW3/results/transitions.csv');require(len(trs)==896,'2023 transition count')
    edges=set()
    for r in trs:
        a,b=int(r['old']),int(r['new']);edges.add((a,b));require((a^b).bit_count()==1,'2023 single-input edge')
        for phase,state in [('pre',a),('post',b)]:
            expected=(state&7)+((state>>3)&7)+(state>>6)
            require(levels([float(r[f'{phase}_{n}_v']) for n in ['s0','s1','s2','cout']],expected),'2023 transition levels')
    require(edges=={(a,a^(1<<bit)) for a in range(128) for bit in range(7)},'2023 directed edge coverage')
    ds=rows('2023/HW3/results/delays.csv');require(len(ds)==1552,'2023 changed-output delays')
    s=js('2023/HW3/results/summary.json')
    require(math.isclose(max(float(r['delay_ps']) for r in ds),s['worst_measured']['delay_ps'],rel_tol=1e-10),'2023 worst delay')
    require(s['sum_WL_um2']==53.46,'2023 width-length proxy')
    logic=js('2023/HW3/results/logic_verification.json')
    require(logic['status']=='PASS' and logic['transistors']==84 and logic['rca_cases']==128,'2023 ideal topology proof')
    require(math.isclose(s['energy_384ns_fJ'],s['average_supply_power_uW']*384,rel_tol=1e-8),'2023 energy units')
    require(canonical('2023/HW3/rca.sp')==canonical('2023/HW4/rca.sp'),'2023 identical netlist')
    require(hashlib.sha256(canonical('2023/HW3/rca.sp')).hexdigest()==s['netlist_sha256'],'2023 netlist fingerprint')
    h4=js('2023/HW4/validation.json');require(h4['independent_rerun_states']==128 and not h4['post_layout_results_available'],'2023 HW4 scope')
    v4=rows('2023/HW4/vectors.csv');require(len(v4)==128,'2023 HW4 vector count')
    require({int(r['state']) for r in v4}==set(range(128)),'2023 HW4 state coverage')
    for r in v4:
        state=int(r['state']);expected=(state&7)+((state>>3)&7)+(state>>6)
        require(int(r['observed'])==expected and levels([float(r[n+'_v']) for n in ['s0','s1','s2','cout']],expected),'2023 HW4 electrical output')
    refined=js('2023/HW3/results/refinement.json')
    require(refined['same_original_netlist'] and refined['all_logic_levels_pass'] and refined['difference_ps']<1,'2023 refinement')
    print('PASS: 2020, 2021, 2023; twelve complete reports, published numerical evidence, identical HW4 pre-layout netlists and scope.')
if __name__=='__main__':main()
