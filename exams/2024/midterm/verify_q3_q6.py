#!/usr/bin/env python3
"""Reproduce the analytical checks for the scanned 2024 midterm Q3--Q6.

Run: python verify_q3_q6.py
Outputs are written beside this script. Only the exam's ideal switch/RC model
is used for Q3, Q4 and Q6; no process model, SPICE or fitted values are used.
Q5 numerical margins are OPTIONAL ILLUSTRATIONS of a declared equivalent
long-channel square-law inverter with assumed VDD=1.2 V and |VT|=0.3 V.
Neither those voltages nor numerical noise margins are supplied by Q5.

Important distinct units: Q3 defines Cg as the TOTAL input capacitance of a
W/L nMOS + W/L pMOS inverter. Q6 defines Cg per ONE W/L transistor.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent


def write_csv(name: str, rows: list[dict]) -> None:
    with (OUT / name).open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def chain_delay(h: float, total_stages: int) -> dict:
    """A is stage 1; all later stages are inserted in the dashed buffer.

    For fixed stage count, AM--GM gives equal ratios h**(1/N). The inserted
    stage count must be even to preserve A's inversion and the buffer's
    noninverting behavior. Widths are relative to W/L for BOTH nMOS/pMOS.
    """
    if h <= 0 or total_stages < 1 or total_stages % 2 != 1:
        raise ValueError('Positive fanout and odd total stage count required')
    ratio = h ** (1 / total_stages)
    sizes = [ratio ** k for k in range(total_stages)]
    loads = sizes[1:] + [h]
    terms = [load / size for size, load in zip(sizes, loads)]
    assert all(math.isclose(term, ratio, rel_tol=1e-12) for term in terms)
    return {
        'total_stages_including_A': total_stages,
        'inserted_inverters': total_stages - 1,
        'inserted_buffer_noninverting': (total_stages - 1) % 2 == 0,
        'fanout_H_C_D_over_Cg': h,
        'equal_stage_ratio': ratio,
        'widths_n_and_p_relative_W_over_L': sizes,
        'delay_T_over_R_Cg': sum(terms),
    }


def q3() -> dict:
    # tr = Rp*C = 0.05*R*C, hence Rp/R=.05 and pMOS width =20.
    p_width = 1 / 0.05
    # A's equal-width two transistors together have input capacitance Cg.
    # NAND input cap is consequently (p_width+n_width)/2 times that Cg.
    cases = [('intended_equal_width', 20.0), ('balanced_NAND', 40.0),
             ('minimum_nMOS_example', 1.0), ('wide_nMOS_example', 88.0)]
    rows, summaries = [], []
    for label, n_width in cases:
        h = (p_width + n_width) / 2
        results = [chain_delay(h, stages) for stages in range(1, 20, 2)]
        best = min(results, key=lambda result: result['delay_T_over_R_Cg'])
        summaries.append({'case': label, 'nand_p_width': p_width,
                          'nand_n_width': n_width, 'input_cap_over_Cg': h,
                          'best': best})
        for result in results:
            rows.append({'case': label, 'nand_p_width': p_width,
                         'nand_n_width': n_width, 'input_cap_over_Cg': h,
                         'total_stages_including_A': result['total_stages_including_A'],
                         'inserted_inverters': result['inserted_inverters'],
                         'stage_ratio': result['equal_stage_ratio'],
                         'delay_over_R_Cg': result['delay_T_over_R_Cg'],
                         'best_among_odd_stages_1_to_19': result is best})
    assert summaries[0]['best']['total_stages_including_A'] == 3
    assert summaries[1]['best']['total_stages_including_A'] == 3
    assert summaries[3]['best']['total_stages_including_A'] == 5
    # Rounded e values printed in the exam give almost the same RC sum.
    rounded_sizes = [1.0, 2.7, 7.2]
    rounded_loads = [2.7, 7.2, 20.0]
    rounded_delay = sum(c / w for c, w in zip(rounded_loads, rounded_sizes))
    write_csv('q3_stage_checks.csv', rows)
    return {
        'model': 'Ideal switch RC; no parasitics; equal n/p mobilities as in Q3',
        'Cg_definition': 'TOTAL input capacitance of A: one W/L nMOS plus one W/L pMOS',
        'T_path': 'Includes fixed inverter A and inserted inverters, ends at NAND D input',
        'derived_nand_p_width_relative_W_over_L': p_width,
        'source_gap': 'D nMOS width is not stated; per-input D capacitance is not unique',
        'parameterized_input_cap_C_D_over_Cg': '(20 + w_n)/2',
        'intended_convention': 'Assume D nMOS and pMOS both 20W/L, hence C_D=20Cg',
        'graded_answer': 'A plus two inserted inverters, widths 1:e:e^2, T=3e R Cg',
        'rounded_exam_e_sizes': rounded_sizes,
        'rounded_exam_size_delay_T_over_R_Cg': rounded_delay,
        'cases': summaries,
    }


def nmos_region(vgs: float, vds: float, threshold: float) -> str:
    if vgs <= threshold:
        return 'cutoff (threshold boundary if equal)'
    if vds >= vgs - threshold:
        return 'saturation (triode boundary if equal)'
    return 'triode'


def q4() -> dict:
    vdd, vt, r1, r2 = 1.2, 0.4, 1.0, 2.0
    vx = vdd * r1 / (r1 + r2)
    trigger = vx + vt
    assert math.isclose(vx, 0.4) and math.isclose(trigger, 0.8)
    rows = []
    # Open interval t1<t<t2, under the exam's ON-resistance divider model.
    # N2 drain=VDD, gate=Vout=VDD, source=VX; N3 source=VX.
    for vin in [0.45, 0.5, 0.6, 0.7, 0.75]:
        triples = [('N1', vin, vx), ('N2', vdd-vx, vdd-vx),
                   ('N3', vin-vx, vdd-vx)]
        for name, vgs, vds in triples:
            region = nmos_region(vgs, vds, vt)
            rows.append({'Vin_V': vin, 'Vout_V': vdd, 'VX_V': vx,
                         'transistor': name, 'VGS_V': vgs, 'VDS_V': vds,
                         'threshold_V': vt, 'region': region})
            assert region.startswith('cutoff' if name == 'N3' else 'saturation')
    write_csv('q4_regions.csv', rows)
    return {
        'model': 'Constant ON resistances specified by the exam, not a MOS DC solver',
        'assumed_pretransition_output_V': vdd,
        'threshold_V': vt,
        'internal_node_divider_V': vx,
        'rising_input_switch_onset_V': trigger,
        't1': 'Vin=0.4 V: N1 reaches threshold',
        'open_interval_t1_t2': {'N1': 'saturation', 'N2': 'saturation', 'N3': 'cutoff'},
        't2': 'Vin=0.8 V: N3 reaches threshold; N1 is at the saturation/triode boundary',
        'scope': 'The internal node is the ON-resistance approximation in the open interval; no assertion of a continuous transient or exact device switching threshold',
    }


def bisect_root(function, low: float, high: float) -> float:
    flo, fhi = function(low), function(high)
    if flo * fhi > 0:
        raise ValueError('Root not bracketed')
    for _ in range(100):
        mid = (low + high) / 2
        fm = function(mid)
        if fm == 0 or high-low < 1e-14:
            return mid
        if flo * fm <= 0:
            high = mid
        else:
            low, flo = mid, fm
    return (low + high) / 2


def illustrative_equivalent_inverter_margins(r: float) -> dict:
    """Illustration ONLY: assume equal |VT|=.3V, VDD=1.2V, beta_n=1.

    r=beta_p/beta_n. Solve the long-channel square-law DC equations at
    gain=-1. Stack conductance approximation is not a transistor-level
    multi-input gate model; these margins are not exam/source values.
    """
    vdd, vt = 1.2, 0.3
    vm = (vt + math.sqrt(r)*(vdd-vt)) / (1+math.sqrt(r))
    # VIL: nMOS saturated, pMOS triode; gain=-1 fixes output y(x).
    low_y = lambda x: (vdd+x+vt+(x-vt)/r)/2
    low_residual = lambda x: (x-vt)**2/2-r*((vdd-x-vt)*(vdd-low_y(x))-(vdd-low_y(x))**2/2)
    vil = bisect_root(low_residual, vt, vm)
    # VIH: nMOS triode, pMOS saturated.
    high_y = lambda x: (x-vt-r*(vdd-x-vt))/2
    high_residual = lambda x: (x-vt)*high_y(x)-high_y(x)**2/2-r*(vdd-x-vt)**2/2
    vih = bisect_root(high_residual, vm, vdd-vt)
    assert low_y(vil) > vil+vt  # pMOS triode
    assert low_y(vil) >= vil-vt  # nMOS saturation
    assert high_y(vih) < vih-vt  # nMOS triode
    assert high_y(vih) <= vih+vt  # pMOS saturation
    return {'illustrative_only': True, 'assumed_VDD_V': vdd,
            'assumed_equal_threshold_magnitudes_V': vt,
            'assumed_beta_p_over_beta_n': r, 'VIL_V': vil, 'VIH_V': vih,
            'NML_V_with_ideal_VOL_0': vil, 'NMH_V_with_ideal_VOH_VDD': vdd-vih}


def q5() -> dict:
    rows = []
    for pattern in ['0011', '0101', '1101', '1001']:
        a, b, c, d = map(int, pattern)
        q = 1 - (b & c)
        g2, g3 = 1-(a | q), 1-(q & d)
        assert q == 1 and d == 1 and g2 == 0 and g3 == 0
        rows.append({'ABCD': pattern, 'A': a, 'B': b, 'C': c, 'D': d,
                     'G1_NAND_output': q, 'G2_NOR_output': g2, 'G3_NAND_output': g3,
                     'G2_branch_sensitized_to_G1_noise': a == 0,
                     'G2_intended_comparison': 'NML<NMH',
                     'G3_intended_comparison': 'NML>NMH',
                     'G2_specific_input_note': ('A=0 sensitizes the G1-driven NOR input'
                         if a == 0 else 'A=1 masks noise on only the G1-driven NOR input'),
                     'G3_specific_input_note': 'D=1 sensitizes the G1-driven NAND input'})
    examples = {}
    for label, r in [('NOR_sensitized_equivalent', 0.5),
                     ('NAND_sensitized_equivalent', 2.0),
                     ('NOR_tied_inputs_equivalent', 0.25),
                     ('NAND_tied_inputs_equivalent', 4.0)]:
        margins = illustrative_equivalent_inverter_margins(r)
        if r < 1:
            assert margins['NML_V_with_ideal_VOL_0'] < margins['NMH_V_with_ideal_VOH_VDD']
        else:
            assert margins['NML_V_with_ideal_VOL_0'] > margins['NMH_V_with_ideal_VOH_VDD']
        examples[label] = margins
    write_csv('q5_noise_scenarios.csv', rows)
    return {
        'source_quantitative_noise_margins': None,
        'source_gap': 'Q5 supplies mobility/width ratios but no VDD or transistor thresholds',
        'intended_qualitative_assumption': 'Standard static-CMOS VTC with equal threshold magnitudes and ideal output rails',
        'source_widths': {'nMOS': 'W/L', 'pMOS': '2W/L', 'mu_n_over_mu_p': 2},
        'equal_single_device_strength': 'beta_n=beta_p=beta',
        'sensitized_NOR_strengths': {'beta_n': 'beta', 'beta_p': 'beta/2'},
        'sensitized_NAND_strengths': {'beta_n': 'beta/2', 'beta_p': 'beta'},
        'graded_comparisons': {'G2_NOR': 'NML<NMH', 'G3_NAND': 'NML>NMH'},
        'specific_input_caveat': 'For A=1, G2 output is held low when only the G1 branch is disturbed; a unique switching VTC for that unsensitized input does not exist',
        'illustrative_model': 'Equivalent square-law inverter, constant series/parallel beta approximation, zero channel-length modulation, equal assumed thresholds, ideal rails; not SPICE or a fitted model',
        'illustrative_only_margins': examples,
        'functional_scenarios': rows,
    }


def and_delay(nand_n: float, nand_p: float,
              inverter_n: float, inverter_p: float) -> dict:
    """All sizes multiply W/L; all capacitances use Q6 per-device Cg.

    nMOS resistance R/w, pMOS resistance 2R/w. Output load=4Cg.
    Worst NAND pull-up uses just one active pMOS. NAND pull-down has
    both series nMOS ON. Drain and wire capacitances are explicitly ignored.
    """
    ci = inverter_n + inverter_p
    nand_up, nand_down = 2/nand_p, 2/nand_n
    inv_up, inv_down = 2/inverter_p, 1/inverter_n
    out_rise = nand_down*ci + inv_up*4
    out_fall = nand_up*ci + inv_down*4
    return {'nand_n_width_relative_W_over_L': nand_n,
            'nand_p_width_relative_W_over_L': nand_p,
            'inverter_n_width_relative_W_over_L': inverter_n,
            'inverter_p_width_relative_W_over_L': inverter_p,
            'inverter_input_cap_over_Cg': ci,
            'NAND_pull_up_resistance_over_R': nand_up,
            'NAND_pull_down_resistance_over_R': nand_down,
            'INV_pull_up_resistance_over_R': inv_up,
            'INV_pull_down_resistance_over_R': inv_down,
            'AND_output_rise_delay_over_R_Cg': out_rise,
            'AND_output_fall_delay_over_R_Cg': out_fall,
            'worst_delay_over_R_Cg': max(out_rise, out_fall),
            'strictly_below_8_R_Cg': max(out_rise, out_fall) < 8}


def q6() -> dict:
    student = and_delay(1, 2, 1, 2)
    corrected = and_delay(2, 2, 1, 2)
    assert student['inverter_input_cap_over_Cg'] == 3
    assert student['worst_delay_over_R_Cg'] == 10
    assert not student['strictly_below_8_R_Cg']
    assert corrected['AND_output_rise_delay_over_R_Cg'] == 7
    assert corrected['AND_output_fall_delay_over_R_Cg'] == 7
    assert corrected['strictly_below_8_R_Cg']
    write_csv('q6_delay_checks.csv', [dict(case='student_native_drawing', **student),
                                    dict(case='corrected_NAND_nMOS_widths', **corrected)])
    return {
        'Cg_definition': 'ONE W/L nMOS or pMOS transistor gate capacitance',
        'model': 'Ideal ON-resistance RC sum; no drain/wire parasitics; output load=4Cg',
        'source_mu_n_over_mu_p': 2,
        'student_drawing_read_from': 'Original PDF page 5 embedded image; NAND p2/n1, inverter p2/n1',
        'student_capacitance_error': 'Student uses 1.5Cg for inverter input; Q6 units require (1+2)Cg=3Cg',
        'student_design_recomputed': student,
        'corrected_design': corrected,
        'correction': 'Double each NAND series nMOS to 2W/L; keep the two NAND pMOS 2W/L and inverter nMOS W/L, pMOS 2W/L',
        'limitations': 'This analytical 7RCg result is for the stipulated ideal RC model, not a process-dependent numerical delay',
    }


def main() -> None:
    result = {'exam': '2024 Introduction to VLSI Midterm',
              'verification_type': 'Reproducible analytical checks, not simulation',
              'Q3': q3(), 'Q4': q4(), 'Q5': q5(), 'Q6': q6()}
    (OUT/'q3_q6_verification.json').write_text(
        json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    intended = result['Q3']['cases'][0]['best']
    print(f"Q3 intended H=20: {intended['total_stages_including_A']} total stages, "
          f"T={intended['delay_T_over_R_Cg']:.9f} R Cg")
    print('Q4 ideal RC switch onset: Vin=0.8 V; open-interval regions verified')
    print('Q5 four functional scenarios verified; numerical margins are assumed-model illustrations only')
    print('Q6 student worst delay=10 R Cg; corrected worst delay=7 R Cg <8 R Cg')


if __name__ == '__main__':
    main()
