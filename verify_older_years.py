"""Validate published 2013-2019 question PDFs, report coverage and saved numerical evidence. No simulator is launched."""
from pathlib import Path
import csv,hashlib,json,math
ROOT=Path(__file__).resolve().parent/'homework'
ACTIVE={2013:[1,2,3],2015:[1,2,3,4],2016:[3],2017:[1,2,3,4],2018:[1,2],2019:[2]}
def need(ok,msg):
    if not ok:raise AssertionError(msg)
def js(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8-sig'))
def rows(rel):
    with (ROOT/rel).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def near(a,b,rtol=1e-6):return math.isclose(float(a),float(b),rel_tol=rtol,abs_tol=1e-12)
def adder_bit(bits,node):
    total=sum(map(int,bits))
    return total%2 if node.lower()=='s' else (1-int(total>=2) if node.lower()=='nco' else int(total>=2))
def level(bit,value):
    v=float(value)
    return math.isfinite(v) and (-.02<=v<=.2 if bit==0 else 1.6<=v<=1.82)
REPO_ROOT=ROOT.parent
CATALOG=ROOT/'PROMPTS.json'
EXPECTED={(year,h) for year,homeworks in ACTIVE.items() for h in homeworks}
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
    catalog=js('COVERAGE.json')
    need(catalog['completed_assignments']==31 and catalog['newly_added_older_assignments']==15,'Coverage counts')
    for y,hwlist in ACTIVE.items():
        year=ROOT/str(y)
        need((year/'SOURCES.md').is_file(),'Source review missing')
        for h in range(1,5):
            folder=year/f'HW{h}'
            if h in hwlist:
                need((folder/'solution.tex').is_file() and (folder/'solution.pdf').read_bytes().startswith(b'%PDF-'),f'{y} HW{h} reports')
                need((folder/'README.md').is_file(),f'{y} HW{h} reproduction README')
            else:need(not (folder/'solution.tex').exists(),f'Unrequested student-only task {y}/HW{h}')
        for p in year.rglob('*'):
            need(not p.is_file() or p.suffix.lower() not in {'.l','.lic','.gds','.pex','.docx','.zip','.7z'},f'Out-of-scope artifact {p}')
            if p.is_file() and p.suffix=='.csv':
                for r in rows(p.relative_to(ROOT).as_posix()):
                    for k in ['passed','pass','pass_','pass_level','all_logic_pass','logic_pass','pass_logic_levels']:
                        if k in r:need(r[k].lower() in ['true','1'],f'Failed saved check {p}: {r}')
    for y in [2012,2014]:
        p=ROOT/str(y)
        need(not any(p.rglob('solution.tex')) if p.exists() else True,f'Student-only year {y} should be skipped')
    need(js('2013/HW1/verification.json')['status']=='PASS','2013 HW1')
    v=js('2013/HW1/verification.json');need(v['truth_table_cases']==32 and v['unequal_length_current_points']==80800,'2013 proof counts')
    v=js('2013/HW2/verification.json');need(v['status']=='PASS' and near(v['critical_delay_ns'],.6),'2013 clock calculation')
    v=js('2013/HW3/results/summary.json')
    need(v['status']=='PASS' and v['TG_dimensions_um']=={'WN':10,'WP':20,'L':.18} and v['mux_output_load_fF']==10,'2013 prescribed geometry/load')
    need(v['logic_cases']==2048 and v['mux_electrical_transition_cases']==16,'2013 logic/electrical coverage distinction')
    ds=rows('2013/HW3/results/mux_delays.csv');need(len(ds)==16,'2013 mux rows')
    need(all(float(r['tree_delay_ps'])<float(r['baseline_delay_ps']) for r in ds),'2013 same-condition improvement')
    for which in ['baseline','tree']:
        need(near(max(float(r[which+'_delay_ps']) for r in ds),v[which+'_worst_delay_ps']),'2013 maximum from saved rows')
    power=rows('2013/HW3/results/inverter_power.csv');need(len(power)==5,'2013 inverter curve')
    for r,load in zip(power,[.1,.3,.5,.7,1]):
        need(near(r['CL_pF'],load),'2013 prescribed power loads')
        need(near(r['E_sc_overlap_fJ'],float(r['Psc_overlap_uW'])*v['inverter_period_ns']),'2013 power/energy units')
        need(near(r['external_load_switching_power_uW'],load*v['VDD_V']**2/v['inverter_period_ns']*1000),'2013 external load power')
        need(float(r['high_V'])>=1.6 and float(r['low_V'])<=.2,'2013 settled power levels')
    need('LX4' in v['Psc_method'],'2013 intrinsic channel-current definition')
    need(js('2015/HW1/verification.json')['all_pass'] and js('2015/HW2/verification.json')['all_pass'],'2015 theory checks')
    v=js('2015/HW3/verification.json');need(v['all_levels_pass'] and v['max_AND_timestep_difference_ps']<.2,'2015 AND/convergence')
    need(v['power_loads_pF']==[.1,.3,.5,.7,1],'2015 prescribed power loads')
    need('LX4' in v['Psc_definition'],'2015 intrinsic channel-current definition')
    ps=rows('2015/HW3/power_vs_load.csv');need(len(ps)==5,'2015 power curve')
    for r,load in zip(ps,[.1,.3,.5,.7,1]):
        need(near(r['load_pF'],load),'2015 saved power loads')
        need(math.isclose(float(r['overlap_cycle_energy_J']),float(r['Psc_overlap_W'])*v['period_power_ns']*1e-9,rel_tol=1e-8,abs_tol=1e-20),'2015 power/energy units')
        need(near(r['Psw_external_W'],load*1e-12*v['VDD_V']**2/(v['period_power_ns']*1e-9)),'2015 external load power')
        need(float(r['settled_high_V'])>=1.6 and float(r['settled_low_V'])<=.2,'2015 settled power levels')
        need(abs(float(r['trace_integration_power_W'])-float(r['Psc_overlap_W']))<3e-13,'2015 independent trace integration')
    need(all(float(a['Psc_overlap_W'])>float(b['Psc_overlap_W'])>0 for a,b in zip(ps,ps[1:])),'2015 measured power trend')
    v=js('2015/HW4/verification.json')
    for design in ['mirror','domino']:
        need(v[design]['all_logic_pass'],'2015 FA levels')
        for metric in v[design]['fine_step_balance'].values():need(metric['relative_difference']<.03,'2015 slew balance')
        need(v[design]['max_delay_timestep_difference_ps']<.3,'2015 FA convergence')
    need(v['mirror']['device_count']==28 and v['domino']['device_count']==38,'2015 circuit counts')
    for design in ['mirror','domino']:
        data=(ROOT/'2015'/'HW4'/(design+'.sp')).read_bytes().replace(b'\r\n',b'\n')
        need(hashlib.sha256(data).hexdigest()==v[design]['netlist_SHA256_UTF8_LF'],'2015 verified netlist provenance')
        logic=rows('2015/HW4/'+design+'_logic.csv')
        need(len(logic)==(112 if design=='mirror' else 24),'2015 measured logic coverage')
        for r in logic:
            expected=adder_bit(r['inputs_after'] if design=='mirror' else r['input_bits'],r['node'])
            need(int(r['expected'])==expected and level(expected,r['voltage_V'] if design=='mirror' else r['evaluate_V']),'2015 independent sum/carry and voltage check')
            if design=='domino':need(level(0,r['reset_V']),'2015 domino precharge output')
    for y in ['2016','2017']:
        v=js(y+'/HW3/results/and_gate/summary.json')
        need(v['all_logic_levels_pass'] and len(v['cases'])==3,'Equal-size AND cases')
        ds=rows(y+'/HW3/results/and_gate/delays.csv');need(len(ds)==36 and all(float(r['delay_ps'])>0 for r in ds),'AND delays')
        p=js(y+'/HW3/results/power/summary.json');need(len(p['rows'])==5 and p['input_rise_fall_ns']==3,'Power input/curve')
        values=[r['Psc_uW'] for r in p['rows']]
        need(all(a>b>0 for a,b in zip(values,values[1:])),'Recorded Psc trend')
        for r in p['rows']:
            need(near(r['Eshort_fJ'],r['Psc_uW']*p['period_ns']),'Psc energy units')
            need(near(r['Pload_switching_uW'],r['CL_pF']*1e-12*p['VDD_V']**2/(p['period_ns']*1e-9)*1e6),'External load switching power')
            need(r['Vhigh']>=1.6 and r['Vlow']<=.2,'Settled power levels')
    need(js('2017/HW1/verification.json')['all_pass'],'2017 logic')
    v=js('2017/HW4/results/summary.json');need(v['mirror_directed_transitions']==56 and v['domino_input_states']==8,'2017 FA coverage')
    for design in ['mirror','domino']:
        d=v['designs'][design];need(d['all_logic_pass'] and d['balanced'],'2017 FA status')
        for metric in d['statistics'].values():need(metric['imbalance_percent']<=1.01,'2017 slew balance')
        logic=rows('2017/HW4/results/'+design+'_logic.csv')
        need(len(logic)==(112 if design=='mirror' else 32),'2017 measured logic coverage')
        for r in logic:
            expected=0 if r['old']=='precharge' else adder_bit(r['new'],r['node'])
            need(int(r['expected'])==expected and level(expected,r['voltage_V']),'2017 independent sum/carry and voltage check')
    need(js('2018/HW1/verification.json')['boolean_cases']==40,'2018 logic counts')
    need(js('2018/HW1/verification.json')['square_law_points']==5050,'2018 square law')
    for y in ['2018','2019']:
        v=js(y+'/HW2/validation.json');need(v['status']=='PASS' and v['rc_fanins']==8 and v['slew_cases']==2,'HW2 simulations')
        need(v['fast_input_output_fall_ps']<v['slow_input_output_fall_ps'],'Input slew ordering')
        rs=rows(y+'/HW2/rc_checks.csv');need(len(rs)==8,'RC fanin count')
        for r in rs:
            n=int(r['fanin']);need(near(r['expected_rise_ps'],2*n*n) and near(r['expected_fall_ps'],n+1),'Independent RC formula')
            need(near(r['measured_rise_first_moment_ps'],2*n*n,.002) and near(r['measured_fall_first_moment_ps'],n+1,.002),'Measured RC first moments')
        need(near(v['node_x_Cg_ratio'],8/3),'Gate capacitance ratio')
    print('PASS: 15 older assignments; reports, geometry, published numeric evidence, power units, sizing and source omissions.')
if __name__=='__main__':main()
