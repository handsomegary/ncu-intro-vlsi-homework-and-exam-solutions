"""Independently rerun the identical HW3 pre-layout netlist. No layout/PEX."""
from pathlib import Path
import sys as _simulation_sys
_simulation_sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from simulation_environment import default_hspice, default_model, add_environment_check, resolve_simulation_args
import argparse,hashlib,importlib.util,json,os
HERE=Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hspice',default=default_hspice())
    ap.add_argument('--model',type=Path,default=default_model())
    ap.add_argument('--work',type=Path,default=HERE/'.simulation');add_environment_check(ap);a=ap.parse_args();resolve_simulation_args(ap,a)
    spec=importlib.util.spec_from_file_location('h3',HERE.parent/'HW3'/'reproduce.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    assert m.sha(HERE/'rca.sp')==m.sha(HERE.parent/'HW3'/'rca.sp')
    deck=m.power(a.model.resolve());(HERE/'testbench.sp').write_text(deck)
    r=m.run(a.hspice,a.work.resolve(),deck,HERE/'rca.sp')[0];states=[]
    for k in range(128):
        target=m.value(k);v=[float(r[f'v{k}_{n}']) for n in m.OUTS];got=sum(int(q>.9)<<j for j,q in enumerate(v));passed=got==target and all(m.voltage_ok(q,target>>j&1) for j,q in enumerate(v));assert passed
        row={'state':k,'expected':target,'observed':got,'passed':passed};row.update({n+'_v':q for n,q in zip(m.OUTS,v)});states.append(row)
    m.write_csv(HERE/'vectors.csv',states)
    result={'status':'PASS','scope':'pre-layout SPICE only','independent_rerun_states':128,'netlist_sha256':m.sha(HERE/'rca.sp'),'average_supply_power_uW':float(r['pavg'])*1e6,'energy_384ns_fJ':float(r['energy'])*1e15,'post_layout_results_available':False}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
