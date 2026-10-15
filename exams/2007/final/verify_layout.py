"""Independent Fall 2007 Q3 literal graph audit; standard library only.

This proves ideal Boolean equilibria and exposes opposing active write drivers.
It does not infer transistor ratios or establish analog overwrite robustness.
"""
from pathlib import Path
import csv
import itertools
import json

HERE = Path(__file__).resolve().parent

def save_csv(name, rows):
    with (HERE/name).open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def rail_paths(devices, values):
    links = {}
    for mos in devices:
        on = values[mos['gate']] == (1 if mos['type']=='N' else 0)
        if on:
            a,b = mos['terminal_1'],mos['terminal_2']
            links.setdefault(a,set()).add(b)
            links.setdefault(b,set()).add(a)
    def rails(node):
        seen={node}; stack=[node]
        while stack:
            for other in links.get(stack.pop(),()):
                if other not in seen:
                    seen.add(other); stack.append(other)
        return ('VDD' in seen,'VSS' in seen)
    return {node:rails(node) for node in ('dbar','CLKB','u','O')}

def main():
    with (HERE/'q3-literal-netlist.csv').open(encoding='utf-8', newline='') as handle:
        mos=list(csv.DictReader(handle))
    assert len(mos)==10
    assert sum(m['type']=='P' for m in mos)==5
    assert sum(m['type']=='N' for m in mos)==5
    assert {m['gate'] for m in mos if m['device'].endswith('_T')}=={'CLK','CLKB'}
    states=[]; equilibria=[]
    for D,CLK,u,O in itertools.product((0,1), repeat=4):
        values=dict(VDD=1,VSS=0,D=D,CLK=CLK,dbar=1-D,CLKB=1-CLK,u=u,O=O)
        rails=rail_paths(mos,values)
        stable=all(pair==(bool(values[node]),not bool(values[node])) for node,pair in rails.items())
        shorted=[node for node,pair in rails.items() if pair==(True,True)]
        states.append(dict(D=D,CLK=CLK,u=u,O=O,dbar=1-D,CLKB=1-CLK,
                           stable_equilibrium=stable,rail_short_nodes=';'.join(shorted),
                           u_to_VDD=rails['u'][0],u_to_VSS=rails['u'][1],
                           O_to_VDD=rails['O'][0],O_to_VSS=rails['O'][1],checked=True))
        if stable: equilibria.append((D,CLK,u,O))
    expected={(D,0,1-O,O) for D,O in itertools.product((0,1),repeat=2)}
    expected|={(D,1,1-D,D) for D in (0,1)}
    assert set(equilibria)==expected
    save_csv('q3-equilibrium-check.csv',states)
    transitions=[]
    for D,CLK,old_O in itertools.product((0,1),repeat=3):
        values=dict(VDD=1,VSS=0,D=D,CLK=CLK,dbar=1-D,CLKB=1-CLK,u=1-old_O,O=old_O)
        rails=rail_paths(mos,values)
        write_contention=rails['u']==(True,True)
        assert write_contention == bool(CLK and D!=old_O)
        transitions.append(dict(D=D,CLK=CLK,old_O=old_O,old_u=1-old_O,
            TG_on=bool(CLK),opposing_input_and_feedback_drivers=write_contention,
            conditional_next_O=D if CLK else old_O,
            condition='write must overcome permanent feedback' if write_contention else 'ideal stable Boolean state',
            checked=True))
    save_csv('q3-write-contention-check.csv',transitions)
    data=dict(status='PASS',year=2007,exam='final',question=3,
        all_independent_checks_passed=True,check_scope='Independent contact graph and ideal circuit equilibria.',
        physical_MOS=10,device_types=dict(P=5,N=5),inverters=4,transmission_gates=1,
        source_columns=['D input inverter','split CLKB / CLK transmission gate','CLK inverter','continuous u storage inverter','O feedback inverter'],
        devices=mos,equilibrium_cases=16,stable_equilibria=6,write_cases=8,
        operation=dict(CLK0='TG off; two complementary static loop states retain old O.',
                       CLK1='TG on; ideal consistent equilibrium is u = NOT D and O = D.',
                       changed_write='Old O opposite D activates opposing input and permanent-feedback drivers. Numerical ratios are absent; successful analog overwrite is conditional.',
                       scope='No transient or process simulation; no guaranteed write margin or frequency claimed.'),
        contact_trace=[
            'First internal poly has separated p/n segments: upper bends to CLK inverter drain contact around source x510,y540; lower bends along bottom to named CLK poly.',
            'Central CLK poly is continuous across both active rows; right p/n terminals contact VDD/VSS, while left drains generate CLKB.',
            'Second internal poly is continuous across p/n; upper and lower U arms contact rightmost O inverter left drains u.',
            'Second internal inverter right drains join Metal1 that contacts named O poly in the middle gap.',
            'The u Metal1 bridge crosses CLK active without a contact; it does not short to CLKB. Simple cross-layer overlaps are not contacts.',
            'No complementary clock is externally assumed and no second feedback TG is hidden: its two absent devices are not invented.',
            'Rightmost upper/lower u drain Metal1 stubs are separate across the central O-feed route. Their common u connection is through the continuous U-poly and its two contacts.',
        ])
    (HERE/'q3-layout-verification.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print('PASS: 10 MOS; 16 ideal equilibrium cases; 8 hold/write cases; fixed-feedback contention explicit.')

if __name__=='__main__':main()
