"""Verify 2012 final Q2, Q7 and Q8 using only the Python standard library.

Q2/Q7 use independently transcribed ideal MOS switch graphs, not image OCR or
transistor simulation. Q8 uses the fixed-threshold long-channel square-law
model at the onset of the rising Schmitt transition. No device beta magnitude,
body-effect parameter, channel-length modulation, or unprinted threshold is
assigned. The Q7 input CSVs are read and checked, never overwritten.

Run: python verify_logic_layout.py
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
from collections import Counter
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parent
FIELDS = ('device', 'type', 'left_channel', 'right_channel', 'gate')


def write_csv(name, rows):
    assert rows
    with (ROOT / name).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def as_rows(devices):
    return [dict(zip(FIELDS, device)) for device in devices]


def switch_graph(devices, values):
    graph, on_devices = {}, []
    for name, kind, left, right, gate in devices:
        assert kind in ('p', 'n')
        assert gate in values, (name, gate)
        on = values[gate] == (0 if kind == 'p' else 1)
        if on:
            graph.setdefault(left, set()).add(right)
            graph.setdefault(right, set()).add(left)
            on_devices.append(name)
    return graph, on_devices


def connected(graph, start, end):
    seen, todo = set(), [start]
    while todo:
        node = todo.pop()
        if node == end:
            return True
        if node not in seen:
            seen.add(node)
            todo.extend(graph.get(node, set()) - seen)
    return False


def rail_flags(graph, node):
    return connected(graph, node, 'VDD'), connected(graph, node, 'VSS')


def rail_consistent(graph, node, value):
    high, low = rail_flags(graph, node)
    return (high, low) == ((True, False) if value else (False, True))


def counts(devices):
    c = Counter(device[1] for device in devices)
    return {'pMOS': c['p'], 'nMOS': c['n'], 'total': len(devices)}


def read_literal_csv(name, expected):
    path = ROOT / name
    with path.open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        assert tuple(reader.fieldnames) == FIELDS
        devices = [tuple(row[field] for field in FIELDS) for row in reader]
    assert len(devices) == 12
    assert len({d[0] for d in devices}) == 12
    # Left/right channel order is electrically interchangeable in this ideal
    # switch check. Gate, type, and unordered channel pair must match source.
    def canonical(ds):
        return {name: (kind, tuple(sorted((left, right))), gate)
                for name, kind, left, right, gate in ds}
    assert canonical(devices) == canonical(expected), f'Source contact-map mismatch: {name}'
    assert counts(devices) == {'pMOS': 6, 'nMOS': 6, 'total': 12}
    # CSV identities follow the collection's LF-normalized text hash policy.
    return devices, hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


# Q2: the printed bar covers all of A(B+C)+C. Absorption reduces it to AB+C.
# Dynamic output F is precharged high and conditionally discharged by AB+C.
DYNAMIC = [
    ('Ppre', 'p', 'VDD', 'F', 'phi'),
    ('Nfoot', 'n', 'foot', 'VSS', 'phi'),
    ('NA', 'n', 'F', 'ab', 'A'),
    ('NB', 'n', 'ab', 'foot', 'B'),
    ('NC', 'n', 'F', 'foot', 'C'),
]
DIFFERENTIAL_CORE = [
    ('PL', 'p', 'VDD', 'F', 'Fbar'),
    ('PR', 'p', 'VDD', 'Fbar', 'F'),
    ('NLA', 'n', 'F', 'ab', 'A'),
    ('NLB', 'n', 'ab', 'VSS', 'B'),
    ('NLC', 'n', 'F', 'VSS', 'C'),
    ('NRCbar', 'n', 'Fbar', 'cbar', 'Cbar'),
    ('NRAbar', 'n', 'cbar', 'VSS', 'Abar'),
    ('NRBbar', 'n', 'cbar', 'VSS', 'Bbar'),
]
COMPLEMENT_INVERTERS = [device for signal in ('A', 'B', 'C') for device in (
    (f'P{signal}bar', 'p', 'VDD', f'{signal}bar', signal),
    (f'N{signal}bar', 'n', f'{signal}bar', 'VSS', signal),
)]
assert counts(DYNAMIC) == {'pMOS': 1, 'nMOS': 4, 'total': 5}
assert counts(DIFFERENTIAL_CORE) == {'pMOS': 2, 'nMOS': 6, 'total': 8}
assert counts(DIFFERENTIAL_CORE + COMPLEMENT_INVERTERS) == {'pMOS': 5, 'nMOS': 9, 'total': 14}
write_csv('q2_dynamic_netlist.csv', as_rows(DYNAMIC))
write_csv('q2_differential_complete_netlist.csv', as_rows(DIFFERENTIAL_CORE + COMPLEMENT_INVERTERS))

q2_truth, q2_phases, q2_candidates = [], [], []
for a, b, c in product((0, 1), repeat=3):
    printed_f = int(not (a and (b or c) or c))
    simplified_f = int(not (a and b or c))
    assert printed_f == simplified_f
    values = {'VDD': 1, 'VSS': 0, 'A': a, 'B': b, 'C': c,
              'Abar': 1-a, 'Bbar': 1-b, 'Cbar': 1-c}
    complement_graph, _ = switch_graph(COMPLEMENT_INVERTERS, values)
    for signal in ('A', 'B', 'C'):
        assert rail_consistent(complement_graph, signal+'bar', values[signal+'bar'])
    for phi in (0, 1):
        graph, on = switch_graph(DYNAMIC, {**values, 'phi': phi})
        high, low = rail_flags(graph, 'F')
        if phi == 0:
            assert high and not low
            dynamic_f, mode = 1, 'precharge high'
        else:
            assert not high
            dynamic_f = int(not low)  # Undischarged node retains precharge 1.
            assert dynamic_f == simplified_f
            mode = 'discharged' if low else 'floating, retains precharged high'
        q2_phases.append({'A': a, 'B': b, 'C': c, 'phi': phi, 'F_to_VDD': high,
                          'F_to_VSS': low, 'F_after_phase': dynamic_f, 'mode': mode})
    stable = []
    for candidate_f, candidate_fbar in product((0, 1), repeat=2):
        graph, on = switch_graph(DIFFERENTIAL_CORE + COMPLEMENT_INVERTERS,
                                 {**values, 'F': candidate_f, 'Fbar': candidate_fbar})
        valid = (rail_consistent(graph, 'F', candidate_f)
                 and rail_consistent(graph, 'Fbar', candidate_fbar))
        if valid:
            for signal in ('A', 'B', 'C'):
                assert rail_consistent(graph, signal+'bar', values[signal+'bar'])
        q2_candidates.append({'A': a, 'B': b, 'C': c, 'candidate_F': candidate_f,
                              'candidate_Fbar': candidate_fbar, 'rail_consistent': valid})
        if valid:
            stable.append((candidate_f, candidate_fbar))
    assert stable == [(simplified_f, 1-simplified_f)]
    q2_truth.append({'A': a, 'B': b, 'C': c, 'printed_F': printed_f,
                    'simplified_F': simplified_f, 'dynamic_evaluation_F': simplified_f,
                    'differential_F': stable[0][0], 'differential_Fbar': stable[0][1],
                    'differential_stable_assignments': len(stable)})
write_csv('q2_truth.csv', q2_truth)
write_csv('q2_dynamic_phases.csv', q2_phases)
write_csv('q2_differential_candidates.csv', q2_candidates)
write_csv('q2_transistor_counts.csv', [
    {'implementation': 'dynamic simplified', **counts(DYNAMIC)},
    {'implementation': 'differential core, complements supplied', **counts(DIFFERENTIAL_CORE)},
    {'implementation': 'differential complete, original A/B/C inputs', **counts(DIFFERENTIAL_CORE + COMPLEMENT_INVERTERS)},
])

# Q7: literal source extraction. These contact maps were independently read
# from the native 2012 photo; Q7b is not the input-inverter variant in 2016.
EXPECTED_Q7A = [
    ('P1','p','VDD','u','Y'), ('N1','n','VSS','u','Y'),
    ('P2','p','u','v','C'), ('N2','n','u','v','Cbar'),
    ('P3','p','v','r','Cbar'), ('N3','n','v','r','C'),
    ('P4','p','r','VDD','X'), ('N4','n','r','VSS','X'),
    ('P5','p','VDD','X','v'), ('N5','n','VSS','X','v'),
    ('P6','p','X','VDD','X'), ('N6','n','X','VSS','X'),
]
EXPECTED_Q7B = [
    ('P1','p','p0','p1','VDD'), ('N1','n','n0','n1','VSS'),
    ('P2','p','p1','VDD','VDD'), ('N2','n','n1','VSS','VSS'),
    ('P3','p','VDD','p3','a'), ('N3','n','VSS','Z','a'),
    ('P4','p','p3','p4','b'), ('N4','n','Z','VSS','b'),
    ('P5','p','p4','Z','c'), ('N5','n','VSS','Z','c'),
    ('P6','p','Z','p6','VDD'), ('N6','n','Z','n6','VSS'),
]
q7a, hash_a = read_literal_csv('q7a_literal_netlist.csv', EXPECTED_Q7A)
q7b, hash_b = read_literal_csv('q7b_literal_netlist.csv', EXPECTED_Q7B)
q7a_rows, q7a_phase = [], []
for clock in (0, 1):
    values = {'VDD': 1, 'VSS': 0, 'Y': 0, 'C': clock, 'Cbar': 1-clock,
              'u': 1, 'v': 1, 'r': 1, 'X': 0}
    _, on = switch_graph(q7a, values)
    input_tg = all(n in on for n in ('P2', 'N2'))
    feedback_tg = all(n in on for n in ('P3', 'N3'))
    assert input_tg == (clock == 0)
    assert feedback_tg == (clock == 1)
    q7a_phase.append({'C': clock, 'Cbar': 1-clock, 'P2_N2_input_TG_on': input_tg,
                      'P3_N3_feedback_TG_on': feedback_tg})
for y, clock, u, v, r, x in product((0, 1), repeat=6):
    values = {'VDD': 1, 'VSS': 0, 'Y': y, 'C': clock, 'Cbar': 1-clock,
              'u': u, 'v': v, 'r': r, 'X': x}
    graph, on = switch_graph(q7a, values)
    high, low = rail_flags(graph, 'X')
    opposing_device = 'P6' if x == 0 else 'N6'
    opposing_rail = 'VDD' if x == 0 else 'VSS'
    assert opposing_device in on
    assert connected(graph, 'X', opposing_rail)
    assert not rail_consistent(graph, 'X', x)
    q7a_rows.append({'Y': y, 'C': clock, 'u': u, 'v': v, 'r': r, 'candidate_X': x,
                     'X_to_VDD': high, 'X_to_VSS': low, 'opposing_device': opposing_device,
                     'opposing_rail': opposing_rail, 'X_ideal_rail_consistent': False,
                     'ON_devices': ' '.join(on)})
write_csv('q7a_clock_phases.csv', q7a_phase)
write_csv('q7a_full_switch_connectivity.csv', q7a_rows)
q7b_rows = []
off_names = {'P1', 'N1', 'P2', 'N2', 'P6', 'N6'}
floating_stubs = {'p0', 'p1', 'p6', 'n0', 'n1', 'n6'}
for a, b, c in product((0, 1), repeat=3):
    values = {'VDD': 1, 'VSS': 0, 'a': a, 'b': b, 'c': c}
    graph, on = switch_graph(q7b, values)
    assert off_names.isdisjoint(on)
    high, low = rail_flags(graph, 'Z')
    expected_z = int(not (a or b or c))
    assert high != low
    assert int(high) == expected_z
    for stub in floating_stubs:
        assert not connected(graph, stub, 'Z')
        assert not connected(graph, stub, 'VDD')
        assert not connected(graph, stub, 'VSS')
    q7b_rows.append({'a': a, 'b': b, 'c': c, 'Z_to_VDD': high, 'Z_to_VSS': low,
                     'Z': int(high), 'expected_NOR3': expected_z,
                     'fixed_gate_OFF_devices': ' '.join(sorted(off_names)),
                     'ON_devices': ' '.join(on)})
write_csv('q7b_full_switch_truth.csv', q7b_rows)

# Q8: pre-switch Vout~VDD, upper N2 is at onset VGS=Vtn.
VDD, VT_PLUS, VTN = F(9, 5), F(6, 5), F(3, 5)
INTERNAL = VT_PLUS - VTN
VGS1, VDS1 = VT_PLUS, INTERNAL
VGS3, VDS3 = VDD-INTERNAL, VDD-INTERNAL
OV1, OV3 = VGS1-VTN, VGS3-VTN
assert INTERNAL == F(3, 5)
assert VDS1 == OV1 and VDS3 > OV3  # N1 boundary; N3 firmly saturation.
assert VGS1 == VGS3 == F(6, 5)
I1_PER_BETA, I3_PER_BETA = OV1**2/2, OV3**2/2
RATIO = I3_PER_BETA / I1_PER_BETA
assert RATIO == 1
assert VDS3 == F(6, 5) and VDS1 == F(3, 5)
q8_regions = [
    {'device': 'N1', 'VGS_V': float(VGS1), 'VDS_V': float(VDS1),
     'Vtn_V': float(VTN), 'overdrive_V': float(OV1),
     'region': 'triode/saturation boundary', 'Id_over_beta_V2': str(I1_PER_BETA)},
    {'device': 'N3', 'VGS_V': float(VGS3), 'VDS_V': float(VDS3),
     'Vtn_V': float(VTN), 'overdrive_V': float(OV3),
     'region': 'saturation', 'Id_over_beta_V2': str(I3_PER_BETA)},
]
write_csv('q8_square_law_regions.csv', q8_regions)
q8_balance = []
for candidate_ratio in (F(1, 2), F(1), F(2)):
    i1 = candidate_ratio * I1_PER_BETA
    i3 = I3_PER_BETA
    balanced = i1 == i3
    assert balanced == (candidate_ratio == 1)
    q8_balance.append({'candidate_betaN1_over_betaN3': str(candidate_ratio),
                        'I_N1_over_betaN3_V2': str(i1), 'I_N3_over_betaN3_V2': str(i3),
                        'onset_current_balance': balanced})
write_csv('q8_current_balance.csv', q8_balance)

report = {
    'all_checks_passed': True,
    'source': {'exam': '2012 final', 'printed_footer': 'Fall 2012',
               'Q2_page': '3-1', 'Q7_Q8_page': '3-3',
               'method': 'Independent native-original visual transcription; exact switch and square-law checks.'},
    'Q2': {'printed_function': 'NOT(A*(B+C)+C)', 'simplified_function': 'NOT(A*B+C)',
           'complement_function': 'Cbar*(Abar+Bbar)', 'truth_rows': len(q2_truth),
           'dynamic_phase_rows': len(q2_phases), 'differential_candidate_rows': len(q2_candidates),
           'unique_complementary_differential_state_per_input': True,
           'transistor_counts': {'dynamic': counts(DYNAMIC),
                                  'differential_core': counts(DIFFERENTIAL_CORE),
                                  'differential_original_inputs_complete': counts(DIFFERENTIAL_CORE + COMPLEMENT_INVERTERS)},
           'scope': 'Dynamic evaluation starts from high precharge; undischarged output retains charge. Differential count includes explicit A/B/C complement generators for complete design.'},
    'Q7': {'literal_netlists_verified': {'q7a_literal_netlist.csv': hash_a, 'q7b_literal_netlist.csv': hash_b},
           'a': {'device_counts': counts(q7a), 'full_switch_assignments_checked': len(q7a_rows),
                 'clock_phase_rows': len(q7a_phase), 'input_TG_on_C': 0, 'feedback_TG_on_C': 1,
                 'self_connected_pair': ['P6', 'N6'], 'self_connected_gate_and_output': 'X',
                 'ideal_rail_consistent_X_assignments': 0,
                 'scope': 'Literal 12-MOS extraction. P6 opposes an assumed X=0; N6 opposes X=1. This ideal switch countercheck does not prove absence of analog equilibria or determine real logic levels; device strengths and analog characterization are unprovided.'},
           'b': {'device_counts': counts(q7b), 'functional_MOS': 6, 'OFF_isolation_MOS': 6,
                 'OFF_devices': sorted(off_names), 'truth_rows': len(q7b_rows),
                 'function': 'Z=NOT(a+b+c)', 'exactly_one_output_rail_for_each_input': True,
                 'floating_stubs': sorted(floating_stubs),
                 'scope': 'All 12 devices retained. Columns 1/2/6 are split, supply-tied OFF isolation; no input inverter precedes a.'}},
    'Q8': {'source_values_V': {'VDD': float(VDD), 'VT_plus': float(VT_PLUS), 'Vtn': float(VTN)},
           'pre_switch_Vout_V': float(VDD), 'internal_N2_source_V': float(INTERNAL),
           'N1_VDS_V': float(VDS1), 'N3_VDS_V': float(VDS3),
           'N1_current_coefficient_Id_over_beta_V2': str(I1_PER_BETA),
           'N3_current_coefficient_Id_over_beta_V2': str(I3_PER_BETA),
           'betaN1_over_betaN3': str(RATIO), 'balance_candidates_checked': len(q8_balance),
           'model': 'Fixed Vtn=0.6 V; pre-switch Vout=VDD; N2 at threshold onset; long-channel saturation Id=beta*(VGS-Vtn)^2/2. Body effect and channel-length modulation omitted because no parameters are supplied. No absolute beta or other threshold is assigned.',
           'student_resistor_ratio_2': 'Not the square-law result: N3 has VDS=1.2 V and is saturated; constant ON-resistor division at the trip point is unjustified.'},
    'limitations': 'Boolean/switch and square-law analytical verification only. No process-model simulation, layout DRC, or timing characterization.',
}
(ROOT/'logic-layout-verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'all_checks_passed': True, 'Q2_truth': len(q2_truth),
                  'Q2_dynamic_phases': len(q2_phases), 'Q2_differential_candidates': len(q2_candidates),
                  'Q7a_switch_assignments': len(q7a_rows), 'Q7b_truth': len(q7b_rows),
                  'Q8_beta_ratio': str(RATIO)}))

