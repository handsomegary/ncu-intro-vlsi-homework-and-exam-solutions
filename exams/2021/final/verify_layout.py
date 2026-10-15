"""Connectivity checks for the literal 2021 final Figure 3 layout.

An ideal switch test verifies settled states and detects write contention;
it does not assert that an un-sized ratioed latch can always be written.
"""
from pathlib import Path
import csv
import itertools
import json

OUT = Path(__file__).resolve().parent
columns = [325, 450, 576, 640, 775, 918, 1047, 1112, 1236, 1360]
# D/S order is a schematic convention; pass-device terminals are symmetric.
devices = [
 ('P1','p','X','VDD','a',1,'input inverter'),
 ('N1','n','X','a','GND',1,'input inverter'),
 ('P2','p','c1','a','b',2,'master input TG'),
 ('N2','n','CLK','a','b',2,'master input TG'),
 ('P3','p','CLK','VDD','c1',3,'local clock inverter'),
 ('N3','n','CLK','c1','GND',3,'local clock inverter'),
 ('P4','p','b','VDD','m',4,'master forward inverter'),
 ('N4','n','b','m','GND',4,'master forward inverter'),
 ('P5','p','m','VDD','b',5,'master feedback inverter'),
 ('N5','n','m','b','GND',5,'master feedback inverter'),
 ('P6','p','c2','m','d',6,'slave input TG'),
 ('N6','n','CLKB','m','d',6,'slave input TG'),
 ('P7','p','CLKB','VDD','c2',7,'local clock inverter'),
 ('N7','n','CLKB','c2','GND',7,'local clock inverter'),
 ('P8','p','d','VDD','s',8,'slave forward inverter'),
 ('N8','n','d','s','GND',8,'slave forward inverter'),
 ('P9','p','s','VDD','d',9,'slave feedback inverter'),
 ('N9','n','s','d','GND',9,'slave feedback inverter'),
 ('P10','p','s','VDD','Y',10,'output inverter'),
 ('N10','n','s','Y','GND',10,'output inverter')
]
def conductive_components(values):
    adjacency = {name:set() for name in values}
    for _,kind,gate,left,right,_,_ in devices:
        if values[gate] == (0 if kind == 'p' else 1):
            adjacency[left].add(right); adjacency[right].add(left)
    components=[]
    while adjacency:
        first=next(iter(adjacency)); todo=[first]; seen=set()
        while todo:
            node=todo.pop()
            if node not in seen:
                seen.add(node); todo.extend(adjacency[node]-seen)
        components.append(seen)
        for node in seen: del adjacency[node]
    return components

assert len(devices)==20
assert sum(row[1]=='p' for row in devices)==10
assert sum(row[1]=='n' for row in devices)==10
rows=[]
for X,CLK,b,d in itertools.product((0,1),repeat=4):
    values={'VDD':1,'GND':0,'X':X,'CLK':CLK,'CLKB':1-CLK,
            'a':1-X,'c1':1-CLK,'c2':CLK,'b':b,'m':1-b,
            'd':d,'s':1-d,'Y':d}
    components=conductive_components(values)
    mixed=[sorted(component) for component in components
           if len({values[node] for node in component})>1]
    master_write=CLK==1
    slave_write=CLK==0
    consistent=(b==values['a'] if master_write else d==values['m'])
    assert bool(mixed) == (not consistent)
    rows.append({'X':X,'CLK':CLK,'CLKB':1-CLK,'a':values['a'],
                 'master_b':b,'master_m':values['m'],'slave_d':d,
                 'slave_s':values['s'],'Y':d,
                 'master_TG_on':int(master_write),'slave_TG_on':int(slave_write),
                 'settled_rail_consistent':int(consistent),
                 'write_contention_components':json.dumps(mixed)})
with (OUT/'layout-checks.csv').open('w',encoding='utf-8',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)

events=[]
for initial_d,X_before,X_after in itertools.product((0,1),repeat=3):
    # Conditional ideal latch model: each enabled TG must override feedback.
    b=1-X_before; m=1-b; d=initial_d
    events.append({'case':len(events)//3,'event':'CLK=1 tracking',
                   'CLK':1,'X':X_before,'b':b,'m':m,'d':d,'Y':d})
    d=m
    assert d==X_before
    events.append({'case':len(events)//3,'event':'CLK falls, slave captures master',
                   'CLK':0,'X':X_before,'b':b,'m':m,'d':d,'Y':d})
    events.append({'case':len(events)//3,'event':'X changes while CLK=0',
                   'CLK':0,'X':X_after,'b':b,'m':m,'d':d,'Y':d})
    assert events[-1]['Y']==X_before
with (OUT/'layout-conditional-events.csv').open('w',encoding='utf-8',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=events[0].keys());writer.writeheader();writer.writerows(events)

contacts=[
 {'net':'a','description':'First inverter right drains to first TG left diffusion; vertical M1 x355 joins p/n, then x419 branch.'},
 {'net':'b','description':'First TG right p/n diffusion joined at x485; upper M1 reaches x737. Poly x640 wraps continuously top to bottom and contacts x737 at y247 and y542, joining both feedback inverter drains.'},
 {'net':'c1','description':'M1 x547 joins left p/n diffusion of CLK column x576 and contacts upper x450 poly at y405.'},
 {'net':'CLK','description':'Continuous poly x576; lower x450 poly joins its lower stem at y585. M1 supply crossings have no poly contacts.'},
 {'net':'m','description':'Right p/n diffusion of x640 joins M1 x673; contacts x775 inverter gates at y405 and continues to second TG left diffusion at x890.'},
 {'net':'d','description':'Second TG right p/n diffusion x955; upper M1 reaches x1190. Continuous wrapping poly x1112 contacts x1190 at upper/lower positions, joining both second feedback inverter drains.'},
 {'net':'c2','description':'M1 x1018 joins left p/n diffusion of CLKB column x1047 and contacts upper x918 poly at y399.'},
 {'net':'CLKB','description':'Continuous poly x1047; lower x918 poly joins lower stem. Source external label is bar(CLK).'},
 {'net':'s','description':'Right p/n diffusion of x1112 joins M1 x1140, then gate contacts x1236 and x1358; input wire ends at final gate contact.'},
 {'net':'Y','description':'Final inverter right p/n drains joined by M1 x1390, with separate rightward output segment. It does not join the final gate-input segment ending at x1358.'}
]
report={
 'status':'verified literal source connectivity',
 'source':'2021 final original Figure 3; source5.png, 1532x1149',
 'device_count':20,'pMOS_count':10,'nMOS_count':10,
 'devices':[{'name':name,'type':kind,'gate':gate,'terminal_1':left,'terminal_2':right,
             'physical_column':column,'approx_source_gate_x':columns[column-1],
             'body_convention':'VDD' if kind=='p' else 'GND','role':role}
             for name,kind,gate,left,right,column,role in devices],
 'contacts':contacts,
 'net_names':'a,c1,b,m,c2,d,s are analysis labels, absent from the original.',
 'body_note':'Standard bulk CMOS body ties are shown as schematic conventions; explicit well/body tap extraction is not specified by this symbolic layout.',
 'phases':{'CLK=1':'master input TG on; slave input TG off',
           'CLK=0':'master input TG off; slave input TG on'},
 'logic':'Conditional negative-edge noninverting data storage Y=X sampled on CLK falling edge, if the enabled input drive overrides the always-connected feedback inverter.',
 'writeability':'Not proved: source has no device sizing or drive-strength data. These are ratioed input-TG latches, not switched-feedback 2-TG latches.',
 'checks':{'MOS_connectivity_states':len(rows),'consistent_settled_states':sum(row['settled_rail_consistent'] for row in rows),
           'write_contention_states':sum(not row['settled_rail_consistent'] for row in rows),
           'conditional_event_rows':len(events),'all_assertions_passed':True},
 'lecture_comparison':'NCU ch07 slide 9 top unconditional-feedback latch is the relevant circuit family. Slide 10 two-TG layout is not an exact contact match.',
 'simulation':'No process-model simulation or electrical write-margin claim.'
}
(OUT/'layout-connectivity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report['checks'],indent=2))
