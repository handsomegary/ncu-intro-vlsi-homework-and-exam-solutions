#!/usr/bin/env python3
"""Analytical verification of the original 2024 final Q3 and Q4.

Run: python verify_dynamic_schmitt.py
This script uses graph reachability, ideal charge conservation, and the
ON-resistance model specified by the paper. It performs NO SPICE simulation.
The Q4 classroom fixed-output-C interpretation and literal feedback gate-cap
interpretation are deliberately separate. An equal-size N4/N3 and P4/P3
example for Q4(b) is declared as an illustration, not a supplied dimension.
"""

from __future__ import annotations

import csv
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path

OUT = Path(__file__).resolve().parent


def save_csv(name: str, rows: list[dict]) -> None:
    with (OUT/name).open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def component(edges: list[tuple[str, str]], start: str) -> set[str]:
    seen = {start}
    while True:
        expanded = seen | {v for u, v in edges if u in seen} | {u for u, v in edges if v in seen}
        if expanded == seen:
            return seen
        seen = expanded


def left_pdn(a: int, b: int, c: int, phi: int = 1) -> list[tuple[str, str]]:
    # Source Fig.1: AB series branch || C(A||B) branch, common phi footer.
    # w is the node immediately above the footer; x and y are source labels.
    edges = []
    for control, nodes in [(a, ('z', 'x')), (b, ('x', 'w')),
                           (c, ('z', 'y')), (a, ('y', 'w')),
                           (b, ('y', 'w')), (phi, ('w', 'GND'))]:
        if control:
            edges.append(nodes)
    return edges


def q3() -> dict:
    cd, cg = F(1, 10), F(1)
    # Polarity-preserving repair: remove the middle footer, making an
    # ordinary static inverter. Rewire its pMOS gate from bar(phi) to z;
    # both n/p gates then use z, as does the right P input gate.
    z_drain_count, z_gate_count = 3, 3
    cz = z_drain_count*cd + z_gate_count*cg
    # These are the explicit NODE parasitic capacitances in Q3(b).
    # Do not add source/drain terms to already supplied total node values.
    cx, cy = F(13, 10), F(11, 10)
    assert cz == F(33, 10)
    rows = []
    for a, b, c in itertools.product([0, 1], repeat=3):
        edges = left_pdn(a, b, c)
        connected = component(edges, 'z')
        discharged = 'GND' in connected
        majority = int(a*b or a*c or b*c)
        assert discharged == bool(majority)
        internal = sorted(connected & {'x', 'y'})
        if discharged:
            status, cap_shared, ratio = 'legitimate full pull-down', F(0), F(0)
        else:
            assert len(internal) <= 1  # pooling x+y cannot be a sharing-only case
            cap_shared = (cx if 'x' in connected else 0) + (cy if 'y' in connected else 0)
            ratio = cz/(cz+cap_shared)
            status = 'isolated charge sharing' if cap_shared else 'no charge sharing'
            assert ratio > F(1, 2)
        rows.append({'ABC': f'{a}{b}{c}', 'A': a, 'B': b, 'C': c,
                     'majority_F_AB_AC_BC': majority,
                     'z_component': '|'.join(sorted(connected)),
                     'ground_path': discharged, 'internal_nodes_connected_to_z': '|'.join(internal),
                     'case': status, 'CZ_fF': float(cz),
                     'isolated_added_cap_fF': float(cap_shared),
                     'Vz_over_VDD_under_zero_initial_internal_charge': float(ratio),
                     'threshold_half_VDD_crossed_erroneously': (not discharged and ratio <= F(1, 2))})
    sharing = [r for r in rows if r['case'] == 'isolated charge sharing']
    assert [r['ABC'] for r in sharing] == ['001', '100']
    assert math.isclose(next(r for r in sharing if r['ABC']=='100')['Vz_over_VDD_under_zero_initial_internal_charge'], 33/46)
    assert math.isclose(next(r for r in sharing if r['ABC']=='001')['Vz_over_VDD_under_zero_initial_internal_charge'], 3/4)
    student_case = next(r for r in rows if r['ABC']=='101')
    assert student_case['ground_path']
    save_csv('q3_pdn_charge_sharing.csv', rows)

    # Original middle gate: clocked precharge/footer bar(phi), data z.
    # Exhaustively check its opposite phase, then the static repair.
    trace=[]
    for a,b,c in itertools.product([0,1],repeat=3):
        majority=int(a*b or a*c or b*c)
        for phi in [0,1]:
            z=1 if phi==0 else 1-majority
            p_on=(1-phi)==0
            n_ground=(1-phi)==1 and z==1
            assert p_on != n_ground
            original=int(p_on)
            repaired=1-z
            assert original==phi and repaired==(majority if phi else 0)
            trace.append({'clock_reading':'bar(phi)','ABC':f'{a}{b}{c}','event':'precharge' if phi==0 else 'evaluation',
                'phi':phi,'bar_phi':1-phi,'z':z,'original_middle_Ybar':original,
                'static_repair_Ybar':repaired,'right_X':majority if phi else 0,
                'original_middle_condition':'bar_phi precharges high' if phi else 'z and bar_phi pull down'})
    # Touching clock wire obscures the original overbar. Under an unbarred
    # reading, early middle discharge can occur before the complex PDN falls.
    for a,b,c in itertools.product([0,1],repeat=3):
        majority=int(a*b or a*c or b*c)
        for phi in [0,1]:
            z=1 if phi==0 else 1-majority
            original=1-phi  # precharged high, then early irreversible discharge
            repaired=1-z
            trace.append({'clock_reading':'phi (possible early-discharge order)','ABC':f'{a}{b}{c}',
                'event':'precharge' if phi==0 else 'evaluation','phi':phi,'bar_phi':1-phi,'z':z,
                'original_middle_Ybar':original,'static_repair_Ybar':repaired,
                'right_X':majority if phi else 0,'original_middle_condition':
                'precharge pMOS on' if phi==0 else 'initial z=1 discharges Ybar; pMOS remains off'})
    save_csv('q3_repeat_cycle_trace.csv', trace)
    # Weak keepers change capacitance after part (b); do not reuse CZ=3.3fF
    # for a numerical post-keeper calculation without new device sizes.
    keepers = {
        'z_high_keeper': {'device': 'weak pMOS', 'drain': 'z', 'source_body': 'VDD',
                          'gate': 'Ybar', 'feedback': 'Ybar=not(z) from repaired middle static inverter'},
        'X_low_keeper': {'device': 'weak nMOS', 'drain': 'X', 'source_body': 'GND',
                         'gate': 'XB', 'feedback': 'XB=not(X) from an added static inverter'},
        'Ybar': 'No keeper needed after both pMOS gate rewiring and footer removal; output statically driven',
    }
    return {
        'source_pages': {'printed': 1, 'student_Q3': 5},
        'source_clocks': {'left_N_dynamic': 'phi', 'middle_pMOS_and_footer': 'bar(phi)',
                          'right_P_dynamic_precharge_evaluation': 'bar(phi)'},
        'middle_clock_scan_limit': 'The possible overbar touches the footer gate wire; bar(phi) is the selected transcription. An unbarred phi reading is also analyzed. The static repair is valid for both.',
        'left_PDN_function': 'F=AB+C(A+B)=AB+AC+BC (three-input majority)',
        'left_dynamic_node': 'z=not(F) after evaluation, precharged high',
        'original_outputs_at_settled_evaluation': 'X=F; original middle Ybar is forced high while phi=1, independent of F',
        'part_a_repair': 'Rewire middle pMOS gate from bar(phi) to z AND remove/tie-ON footer; both inverter gates use z',
        'right_branch': 'Keep its pMOS input on raw z; falling input is the correct P-dynamic monotonicity',
        'repaired_outputs': 'X=Ybar=F; both reset low and can only rise during evaluation',
        'student_part_a': 'Student input inverter plus changing middle clock to phi is a valid alternate N-domino repair giving Ybar=not(F); its polarity differs from the selected static repair',
        'CZ_count_before_part_c': {'drains': ['left precharge pMOS', 'top nMOS A', 'top nMOS C'],
                                 'gates': ['middle static-inverter nMOS', 'middle static-inverter pMOS', 'right input pMOS'],
                                 'Cd_per_device_fF': float(cd), 'Cg_per_device_fF': float(cg), 'CZ_fF': float(cz)},
        'source_internal_node_caps_fF': {'x': float(cx), 'y': float(cy)},
        'node_cap_interpretation': 'Use the explicitly given x,y NODE capacitances as totals; no extra diffusion capacitance is double-counted',
        'sharing_initial_conditions': 'z initially VDD and the isolated internal node initially zero; switch the enabling input on after precharge, a conservative worst case',
        'worst_sharing_ratio': '33/46 VDD for ABC=100; ABC=001 gives 3/4 VDD',
        'part_b_conclusion': 'Sharing-only cases remain strictly above VDD/2 and therefore do not falsely switch a following gate under the stipulated model',
        'student_part_b_error': 'ABC=101 has the real C-A path to ground; pooling x+y and using 3.3/(3.3+1.3+1.1) is not a charge-sharing-only test',
        'optional_additional_wire_cap_reading': {'note': 'Only if 1.3/1.1 fF meant EXTRA wire capacitances rather than total node values; source does not say wire',
            'x_total_including_two_diffusions_fF': 1.5, 'y_total_including_three_diffusions_fF': 1.4,
            'x_sharing_ratio': 3.3/4.8, 'y_sharing_ratio': 3.3/4.7,
            'conclusion': 'Still above VDD/2; qualitative answer unchanged'},
        'part_c_cause': 'Leakage eventually changes floating z-high and X-low evaluation states when the clock is stopped',
        'part_c_feedback_keepers': keepers,
        'keeper_requirements': 'Overcome leakage but remain weaker than evaluation networks; no numeric sizing or hold-time is determined by the paper',
        'hold_scope': 'Correct logic under a prolonged phase with stable valid inputs; dynamic primary inputs must still obey evaluation monotonicity',
        'student_part_c': 'Weak rail keepers are a useful idea; feedback gating avoids permanent contention and both dynamic polarities require restoration',
        'part_c_new_caps': 'Added keeper drains/feedback gates alter capacitance; part(b) numbers belong to the repair before keepers',
        'truth_and_sharing_rows': rows, 'possible_repeat_cycle_trace': trace,
    }


def q4() -> dict:
    # Widths are relative to source N1 W0=160nm; common L=40nm.
    vdd, vt, vt_plus, vt_minus = F(3, 2), F(1, 5), F(1), F(1, 2)
    w0, length = F(160), F(40)
    rn1 = F(1)
    # Positive feedback RC dividers immediately before output switching.
    vn, vp = vt_plus-vt, vt_minus+vt
    rn3 = vdd/vn - 1  # VN=VDD*RN1/(RN1+RN3)
    rp1 = F(1)       # Classroom choice; equal rise/fall path resistances.
    rp3 = rp1*vp/(vdd-vp)
    assert rn3 == rp3 == F(7, 8)
    rn2 = rp2 = F(2)  # Each series path totals 3R in classroom model.
    resistances = {'N1': rn1, 'N2': rn2, 'N3': rn3,
                   'P1': rp1, 'P2': rp2, 'P3': rp3}
    widths = {name: w0*(1 if name.startswith('N') else 2)/resistance
              for name, resistance in resistances.items()}
    expected = {'N1': F(160), 'N2': F(80), 'N3': F(1280, 7),
                'P1': F(320), 'P2': F(160), 'P3': F(2560, 7)}
    assert widths == expected
    output_cap = (widths['N3']+widths['P3'])/w0
    assert output_cap == F(24, 7)
    rise_path, fall_path = rp1+rp2, rn1+rn2
    literal_tr, literal_tf = rise_path*output_cap, fall_path*output_cap
    assert literal_tr == literal_tf == F(72, 7)
    width_rows = [{'transistor': name, 'exact_width_nm': str(width), 'width_nm': float(width),
                   'common_length_nm': float(length), 'resistance_over_R': float(resistances[name]),
                   'gate_capacitance_over_C_N1': float(width/w0)}
                  for name, width in widths.items()]
    save_csv('q4_classroom_widths.csv', width_rows)
    delay_rows = [
        {'model': 'classroom stipulated fixed output load C', 'output_cap_over_C': 1.0,
         'pull_up_resistance_over_R': float(rise_path), 'pull_down_resistance_over_R': float(fall_path),
         'tr_over_RC': float(rise_path), 'tf_over_RC': float(fall_path), 'meets_3_RC': True},
        {'model': 'literal output feedback gate capacitances', 'output_cap_over_C': float(output_cap),
         'pull_up_resistance_over_R': float(rise_path), 'pull_down_resistance_over_R': float(fall_path),
         'tr_over_RC': float(literal_tr), 'tf_over_RC': float(literal_tf), 'meets_3_RC': False},
    ]
    save_csv('q4_delay_model_comparison.csv', delay_rows)

    # Impossibility proof including intrinsic feedback gate load:
    # Let a=WP3/W0>0. Thresholds fix WN3/W0=8/7 and WP1/W0=7a/8.
    # c=Cout/C=8/7+a, RN1/R=1, RP1/R=16/(7a).
    # N2/P2 finite widths add positive series resistances, so delay bounds
    # are STRICT. Their best possible max is minimized at a=16/7.
    a_star, min_bound = F(16, 7), F(24, 7)
    assert min_bound > 3
    # Meeting tf<=3RC needs a<13/7; meeting tr<=3RC needs a>128/35.
    upper_a_fall, lower_a_rise = F(13, 7), F(128, 35)
    assert lower_a_rise > upper_a_fall
    lower_bound_rows = []
    for a in [F(1, 2), F(1), F(13, 7), a_star, F(3), lower_a_rise, F(5)]:
        cap = F(8, 7)+a
        lower_fall, lower_rise = cap, F(16, 7)*cap/a
        worst = max(lower_fall, lower_rise)
        assert worst >= min_bound
        lower_bound_rows.append({'P3_width_relative_N1': float(a), 'P3_width_relative_N1_exact': str(a),
                                 'output_cap_over_C': float(cap),
                                 'fall_lower_bound_over_RC': float(lower_fall),
                                 'rise_lower_bound_over_RC': float(lower_rise),
                                 'worst_lower_bound_over_RC': float(worst),
                                 'note': 'Infimum as N2/P2 widths go to infinity; finite devices are slower'})
    save_csv('q4_literal_delay_lower_bounds.csv', lower_bound_rows)

    # Q4(b) only asks qualitative changes; widths of P4/N4 are not supplied.
    # Illustrative case below assumes P4=P3 and N4=N3 and ideal ON switches.
    # The drawn switches disconnect GATES when open. Comparing against Fig2a
    # also assumes the disconnected added devices are disabled/off-clamped;
    # an unspecified floating gate charge does not ensure they are OFF.
    switch_rows = []
    for label, k in [('switches_off', F(0)), ('switches_on_equal_added_feedback_devices', F(1))]:
        nfeedback, pfeedback = rn3/(1+k), rp3/(1+k)
        vplus = vt+vdd*rn1/(rn1+nfeedback)
        vminus = vdd*pfeedback/(rp1+pfeedback)-vt
        # Aux feedback rail current while the opposing input transistor is
        # also ON. This is a current level, not an average switching power.
        inormalized = F(1)/(rn1+nfeedback)
        ipnormalized = F(1)/(rp1+pfeedback)
        switch_rows.append({'case': label, 'added_feedback_conductance_ratio': float(k),
                            'effective_N3_resistance_over_R': float(nfeedback),
                            'effective_P3_resistance_over_R': float(pfeedback),
                            'VT_plus_V': float(vplus), 'VT_minus_V': float(vminus),
                            'hysteresis_width_V': float(vplus-vminus),
                            'N_aux_current_over_VDD_over_R': float(inormalized),
                            'P_aux_current_over_VDD_over_R': float(ipnormalized),
                            'extra_widths_assumption': ('N4=N3 and P4=P3' if k else 'switches open AND added devices assumed disabled')})
    off, on = switch_rows
    assert math.isclose(off['VT_plus_V'], 1) and math.isclose(off['VT_minus_V'], .5)
    assert math.isclose(on['VT_plus_V'], 143/115)
    assert math.isclose(on['VT_minus_V'], 59/230)
    assert on['hysteresis_width_V'] > off['hysteresis_width_V']
    assert on['N_aux_current_over_VDD_over_R'] > off['N_aux_current_over_VDD_over_R']
    save_csv('q4_switch_hysteresis.csv', switch_rows)
    return {
        'source_pages': {'printed': [1, 2], 'student_Q4': [5, 6]},
        'source_values': {'VDD_V': float(vdd), 'Vtn_V': float(vt), 'abs_Vtp_V': float(vt),
                          'mu_n_over_mu_p': 2, 'N1_width_nm': float(w0), 'common_length_nm': float(length),
                          'R_definition': 'N1 ON resistance', 'C_definition': 'N1 gate capacitance',
                          'specified_tr_tf_over_RC': 3, 'drain_parasitics': 'explicitly ignored'},
        'threshold_targets_from_original_waveform': {'falling_input_output_rise_at_t2_VT_minus_V': .5,
                                                   'rising_input_output_fall_at_t4_VT_plus_V': 1.0,
                                                   'input_noise_lobes_between_thresholds': 'do not switch output'},
        'threshold_equations': {'VT_plus': 'Vtn+VDD*RN1/(RN1+RN3)',
                               'VT_minus': 'VDD*RP3/(RP1+RP3)-abs(Vtp)'},
        'derived_ratios': {'RN3_over_RN1': '7/8', 'N3_width_over_N1': '8/7',
                           'RP1_over_RP3': '8/7', 'P3_width_over_P1': '8/7'},
        'classroom_model': {'convention': 'STIPULATE output load C, omit feedback gate-load scaling in delay',
                            'widths_exact_nm': {name: str(width) for name, width in widths.items()},
                            'widths_nm': {name: float(width) for name, width in widths.items()},
                            'length_nm_all': 40, 'pull_up_down_resistance_over_R': 3,
                            'tr_tf_over_RC': 3,
                            'status': 'Intended resistance-only answer, with the extra output-load convention made explicit'},
        'literal_gate_cap_model': {'output_gate_loads': ['N3 gate', 'P3 gate'],
                                  'output_cap_over_C': '24/7', 'tr_tf_over_RC_for_classroom_widths': '72/7',
                                  'target_3_RC_possible': False,
                                  'a_definition': 'a=WP3/WN1>0', 'c_definition': 'c=Cout/C=8/7+a',
                                  'rise_strict_lower_bound_over_RC': '16(8/7+a)/(7a)',
                                  'fall_strict_lower_bound_over_RC': '8/7+a',
                                  'optimal_a_for_joint_infimum': '16/7',
                                  'joint_delay_infimum_over_RC': '24/7',
                                  'necessary_fall_condition_for_target': 'a<13/7',
                                  'necessary_rise_condition_for_target': 'a>128/35',
                                  'reason_impossible': 'The necessary intervals do not overlap; even ideal infinite N2/P2 widths cannot reduce joint worst delay below 24/7 RC'},
        'student_a': 'Rounded widths agree with the classroom resistance choice; the graded 3RC delay does not include actual N3/P3 gate loading',
        'switches_on_qualitative': 'Stronger parallel feedback raises VT+, lowers VT-, widens hysteresis and increases noise tolerance',
        'source_open_switch_caveat': 'The drawing disconnects added MOS gates when sw is open and supplies no off-bias clamp. Floating gate charge is not specified; the intended comparison assumes P4/N4 disabled when open',
        'switches_on_numeric_example_assumption': 'Ideal switches, N4=N3 and P4=P3; these widths are NOT supplied by part(b)',
        'switches_on_equal_device_results': {'VT_plus_V': 143/115, 'VT_minus_V': 59/230,
                                            'hysteresis_width_V': 227/230,
                                            'auxiliary_current_increase_ratio': 30/23},
        'short_circuit_current_equations': {'before_N_path': 'VDD/(RN1+RN3)',
                                           'after_equal_added_N_path': 'VDD/(RN1+RN3/2)',
                                           'before_P_path': 'VDD/(RP1+RP3)',
                                           'after_equal_added_P_path': 'VDD/(RP1+RP3/2)'},
        'short_circuit_scope': 'The auxiliary VDD-to-ground feedback paths carry more current when enabled; this supports the intended increased short-circuit-power answer for slow transitions. Exact total cycle energy/average power is not determined without device/slew/duty information and the newly added gate loads',
        'student_b_correction': 'The denominator after adding a parallel device must contain PLUS RN3/2, not a subtraction. Equal extra widths must be labeled an assumption; use exact thresholds1.2434782609/.2565217391 and hysteresis.9869565217 only for that example',
        'delay_model_rows': delay_rows, 'width_rows': width_rows,
        'joint_lower_bound_rows': lower_bound_rows, 'switch_rows': switch_rows,
    }


def main() -> None:
    result = {'exam': '2024 Introduction to VLSI Final',
              'method': 'Analytical source-derived checks; no process simulation',
              'Q3': q3(), 'Q4': q4()}
    (OUT/'q3_q4_verification.json').write_text(
        json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print('Q3 graph: all 8 inputs match majority; sharing-only ABC=001 or100, both safe')
    print('Q3 original middle opposite-clock phase checked on all8 inputs; static repair verified')
    print('Q4 classroom widths: thresholds1.0/.5V and resistance-only delay3RC')
    print('Q4 literal gate load24/7 C: delay72/7 RC; any sizing has joint lower bound24/7 RC>3RC')
    print('Q4 equal added feedback illustration: hysteresis increases .5V to227/230V')


if __name__ == '__main__':
    main()
