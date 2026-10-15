"""2024 final: original-figure logic, MOS connectivity and both clock readings.

Python standard library only.  These are ideal Boolean/switch and analytical
timing checks, not transistor simulation.  The circuit functions are derived
from the original photographed prompt, independently of the graded answers.
Run from any directory: python verify_logic_timing.py
"""
from pathlib import Path
import csv
import itertools
import json
import math

HERE = Path(__file__).resolve().parent


def mos(name, kind, drain, gate, source, role="logic", weak=False):
    return dict(name=name, kind=kind, drain=drain, gate=gate, source=source,
                body="VDD" if kind == "P" else "VSS", role=role, weak=weak)


def inverter(prefix, out, gate):
    return [mos(prefix + "P", "P", out, gate, "VDD", "inverter"),
            mos(prefix + "N", "N", out, gate, "VSS", "inverter")]


def path_to(devices, values, start, rail, extra_edges=()):
    graph = {}
    for m in devices:
        assert m["body"] == ("VDD" if m["kind"] == "P" else "VSS")
        on = not values[m["gate"]] if m["kind"] == "P" else bool(values[m["gate"]])
        if on:
            a, b = m["drain"], m["source"]
            graph.setdefault(a, []).append((b, m["name"]))
            graph.setdefault(b, []).append((a, m["name"]))
    for a, b, label in extra_edges:
        graph.setdefault(a, []).append((b, label))
        graph.setdefault(b, []).append((a, label))
    seen = {start}
    queue = [(start, [])]
    for node, path in queue:
        if node == rail:
            return path
        for neighbor, label in graph.get(node, []):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, path + [label]))
    return None


def rails(devices, values, node, extra_edges=()):
    up = path_to(devices, values, node, "VDD", extra_edges)
    down = path_to(devices, values, node, "VSS", extra_edges)
    assert (up is not None) != (down is not None), (node, values, up, down)
    return int(up is not None), ";".join(up or []), ";".join(down or [])


def check_outputs(devices, values, outputs, extra_edges=()):
    evidence = {}
    for node, expected in outputs.items():
        actual, up, down = rails(devices, values, node, extra_edges)
        assert actual == expected, (node, actual, expected, values)
        evidence[node] = dict(value=actual, high_path=up, low_path=down)
    return evidence


def csv_file(name, rows):
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def dpl_graph():
    # Shannon decomposition on x1, then x2; x3/complement are data terminals.
    return [
        mos("NF1", "N", "f", "x1", "uf"),
        mos("NF0", "N", "f", "xb1", "xb3"),
        mos("NF11", "N", "uf", "x2", "VSS"),
        mos("NF10", "N", "uf", "xb2", "xb3"),
        mos("NG1", "N", "g", "x1", "ug"),
        mos("NG0", "N", "g", "xb1", "x3"),
        mos("NG11", "N", "ug", "x2", "VDD"),
        mos("NG10", "N", "ug", "xb2", "x3"),
        mos("PFrestore", "P", "f", "g", "VDD", "level_restorer", True),
        mos("PGrestore", "P", "g", "f", "VDD", "level_restorer", True),
    ]


def verify_dpl():
    graph = dpl_graph()
    rows = []
    for x1, x2, x3 in itertools.product((0, 1), repeat=3):
        values = dict(VDD=1, VSS=0, x1=x1, x2=x2, x3=x3,
                      xb1=1-x1, xb2=1-x2, xb3=1-x3)
        data_sources = [("x3", "VDD" if x3 else "VSS", "x3_source"),
                        ("xb3", "VSS" if x3 else "VDD", "xb3_source")]
        pass_only = [m for m in graph if m["kind"] == "N"]
        f, _, _ = rails(pass_only, values, "f", data_sources)
        g, _, _ = rails(pass_only, values, "g", data_sources)
        reference = int(not ((x1 and x2) or x3))
        assert f == reference and g == 1-reference
        values.update(f=f, g=g)
        evidence = check_outputs(graph, values, {"f": f, "g": g}, data_sources)
        rows.append(dict(x1=x1, x2=x2, x3=x3, f=f, complement=g,
                         expected=reference, f_high_path=evidence["f"]["high_path"],
                         f_low_path=evidence["f"]["low_path"], passed=True))
    csv_file("dpl_checks.csv", rows)
    return dict(cases=len(rows), function="f=NOT(x1*x2+x3)",
                core_MOS=10, complementary_inputs="x1bar,x2bar,x3bar assumed available; 3 static inverters add6MOS",
                includes_level_restoration=True, graph=graph)


def carry_graph():
    # One shared evaluation footer.  Earlier carries drive later GATES; the
    # dynamic nodes are never directly joined by a propagation channel.
    graph = [mos("Nfooter", "N", "eval", "phi", "VSS", "evaluation")]
    for i in range(3):
        d, c, u = f"d{i+1}", f"c{i+1}", f"u{i}"
        previous = "c0" if i == 0 else f"c{i}"
        graph += [mos(f"Ppre{i}", "P", d, "phi", "VDD", "precharge"),
                  mos(f"Ng{i}", "N", d, f"g{i}", "eval", "evaluation"),
                  mos(f"Np{i}", "N", d, f"p{i}", u, "evaluation"),
                  mos(f"Nc{i}", "N", u, previous, "eval", "evaluation"),
                  mos(f"Pkeep{i}", "P", d, c, "VDD", "keeper", True)]
        graph += inverter(f"Icarry{i}", c, d)
    return graph


def verify_carry():
    graph = carry_graph()
    evaluation = [m for m in graph if m["role"] == "evaluation"]
    rows, phases = [], []
    for bits in itertools.product((0, 1), repeat=7):
        source = dict(zip(("c0", "p0", "p1", "p2", "g0", "g1", "g2"), bits))
        values = dict(VDD=1, VSS=0, phi=1, **source)
        dynamic = [1, 1, 1]
        carries = [0, 0, 0]
        # Three successive positive-output stage evaluations suffice.
        for _ in range(3):
            values.update({f"c{i+1}": carries[i] for i in range(3)})
            discharge = [path_to(evaluation, values, f"d{i+1}", "VSS") is not None
                         for i in range(3)]
            dynamic = [d and not active for d, active in zip(dynamic, discharge)]
            carries = [1-int(d) for d in dynamic]
        expected, previous = [], source["c0"]
        for i in range(3):
            previous = int(source[f"g{i}"] or (source[f"p{i}"] and previous))
            expected.append(previous)
        assert carries == expected
        rows.append(dict(**source, c1=carries[0], c2=carries[1], c3=carries[2],
                         expected_c1=expected[0], expected_c2=expected[1], expected_c3=expected[2], passed=True))
        for phase in ("precharge", "evaluate"):
            out = [0, 0, 0] if phase == "precharge" else carries
            nodes = {**{f"c{i+1}": out[i] for i in range(3)},
                     **{f"d{i+1}": 1-out[i] for i in range(3)}}
            values.update(nodes, phi=int(phase == "evaluate"))
            check_outputs(graph, values, nodes)
            phases.append(dict(**source, phase=phase, c1=out[0], c2=out[1], c3=out[2],
                               rail_exclusive=True, passed=True))
    csv_file("carry_checks.csv", rows)
    csv_file("carry_phase_checks.csv", phases)
    return dict(input_cases=len(rows), phase_cases=len(phases), core_MOS=len(graph),
                equation="c[i+1]=g[i] OR(p[i] AND c[i])", shared_element="one common clocked NMOS footer/evaluation rail",
                propagation="positive inverter carry outputs drive subsequent NMOS gates",
                no_propagate_generate_exclusivity_assumption=True,
                input_protocol="c0,p0..2,g0..2 stable before and throughout evaluate; carries rise monotonically from precharge0",
                keeper_scope="weak keepers; final stable switch connectivity verified, contention strength requires analogue sizing",
                graph=graph)


P_NODES = ["VDD", "x", "VDD", "p1", "p2", "w", "VDD", "z"]
N_NODES = ["VSS", "x", "VSS", "w", "VSS", "w", "VSS", "z"]
P_GATES = ["a", "VDD", "x", "b", "c", "VDD", "w"]
N_GATES = ["a", "VSS", "x", "b", "c", "VSS", "w"]


def layout_graph():
    graph = []
    for kind, nodes, gates in (("P", P_NODES, P_GATES), ("N", N_NODES, N_GATES)):
        for i, gate in enumerate(gates):
            graph.append(mos(f"{kind}col{i+1}", kind, nodes[i], gate, nodes[i+1],
                             "off_isolation" if i in (1, 5) else "logic"))
    return graph


def verify_layout():
    graph, rows = layout_graph(), []
    for a, b, c in itertools.product((0, 1), repeat=3):
        values = dict(VDD=1, VSS=0, a=a, b=b, c=c)
        for column, out in ((1, "x"), (None, "w"), (7, "z")):
            stage = [m for m in graph if (m["name"][1:] == f"col{column}" if column is not None
                                         else m["name"][1:] in ("col3", "col4", "col5"))]
            value, _, _ = rails(stage, values, out)
            values[out] = value
        expected = int((not a) or b or c)
        assert values["z"] == expected
        evidence = check_outputs(graph, values, {n: values[n] for n in ("x", "w", "z")})
        rows.append(dict(a=a, b=b, c=c, x=values["x"], w=values["w"], z=values["z"],
                         expected=expected, z_high_path=evidence["z"]["high_path"],
                         z_low_path=evidence["z"]["low_path"], passed=True))
    csv_file("layout_checks.csv", rows)
    return dict(cases=len(rows), physical_MOS=len(graph), functional_MOS=10, off_isolation_MOS=4,
                physical_columns_per_row=7, function="z=NOT(a) OR b OR c",
                stages=["x=NOT(a)", "w=NOR(x,b,c)", "z=NOT(w)"],
                p_diffusion_nodes_left_to_right=P_NODES, n_diffusion_nodes_left_to_right=N_NODES,
                p_gates_left_to_right=P_GATES, n_gates_left_to_right=N_GATES, graph=graph)


def original_q6(a, b, c):
    x = a ^ b
    u = int(not (a and b))
    v = int(not (x and c))
    return dict(x=x, nand_ab=u, nand_xc=v, y1=int(not (u or v)), y2=x ^ c)


def verify_original_q6():
    rows = []
    for a, b, c in itertools.product((0, 1), repeat=3):
        actual = original_q6(a, b, c)
        assert actual["y1"] == 0 and actual["y2"] == (a ^ b ^ c)
        rows.append(dict(a=a, b=b, c=c, **actual, expected_y1=0, expected_y2=a ^ b ^ c, passed=True))
    csv_file("q6_original_truth.csv", rows)
    # Uniform independent bits; a one-input bit inversion never changes y1,
    # but always changes the three-input parity.  This is logical masking,
    # not a quantitative physical register SER prediction.
    masks = []
    for a, b, c in itertools.product((0, 1), repeat=3):
        before = original_q6(a, b, c)
        for position, name in enumerate(("a", "b", "c")):
            upset = [a, b, c]
            upset[position] ^= 1
            after = original_q6(*upset)
            masks.append(dict(a=a, b=b, c=c, upset_input=name,
                              y1_changed=after["y1"] != before["y1"],
                              y2_changed=after["y2"] != before["y2"]))
    csv_file("q6_logical_masking.csv", masks)
    internal = []
    for a, b, c in itertools.product((0, 1), repeat=3):
        before = original_q6(a, b, c)
        upset_x = 1-before["x"]
        after_y1 = int(not (before["nand_ab"] or (not (upset_x and c))))
        after_y2 = upset_x ^ c
        internal.append(dict(a=a, b=b, c=c, original_x=before["x"], upset_x=upset_x,
                             original_y1=before["y1"], upset_y1=after_y1,
                             original_y2=before["y2"], upset_y2=after_y2,
                             y1_changed=after_y1 != before["y1"],
                             y2_changed=after_y2 != before["y2"]))
    assert sum(r["y1_changed"] for r in internal) == 1
    assert sum(r["y2_changed"] for r in internal) == 8
    csv_file("q6_internal_x_masking.csv", internal)
    return dict(cases=len(rows), gates=["XOR(A,B)", "NAND(A,B)", "NAND(X,C)",
                                      "NOR(NAND(A,B),NAND(X,C))", "XOR(X,C)"],
                y1="AB*(A XOR B)*C=0", y2="A XOR B XOR C",
                primary_input_upset_cases=len(masks), y1_changed_cases=sum(r["y1_changed"] for r in masks),
                y2_changed_cases=sum(r["y2_changed"] for r in masks),
                internal_x_upset_cases=8, internal_x_y1_changed_cases=1, internal_x_y2_changed_cases=8,
                internal_x_y1_unmasked_word="111",
                SER_limit="Logical sensitivity only; physical SER also depends on strike sites, capacitance, pulse width, masking and register characteristics")


def np_graph():
    graph = []
    for var in ("a", "b", "c"):
        graph += inverter("Iinput" + var, var + "b", var)
    graph.append(mos("Nnpfooter", "N", "en", "phi", "VSS", "n_evaluation"))
    # raw_x discharges for XNOR, so its held evaluated value is XOR.
    for out, products, feedback in (("raw_x", (("a", "b"), ("ab", "bb")), "kx"),
                                   ("raw_xb", (("ab", "b"), ("a", "bb")), "kxb")):
        graph.append(mos("Ppre_" + out, "P", out, "phi", "VDD", "precharge"))
        for j, product in enumerate(products):
            mid = out + f"_u{j}"
            graph += [mos(out+f"N{j}0", "N", out, product[0], mid, "n_evaluation"),
                      mos(out+f"N{j}1", "N", mid, product[1], "en", "n_evaluation")]
        graph += inverter("Ifb_" + out, feedback, out)
        graph.append(mos("Pkeep_" + out, "P", out, feedback, "VDD", "keeper", True))
    # Both raw rails begin HIGH, then at most one falls.  A p-type stage can
    # therefore evaluate monotonically from its LOW reset value.
    graph += [mos("Pnpheader", "P", "ep", "phib", "VDD", "p_evaluation"),
              mos("NresetY", "N", "y2", "phib", "VSS", "reset")]
    for j, product in enumerate((("raw_xb", "c"), ("raw_x", "cb"))):
        mid = f"yp{j}"
        graph += [mos(f"PY{j}0", "P", "ep", product[0], mid, "p_evaluation"),
                  mos(f"PY{j}1", "P", mid, product[1], "y2", "p_evaluation")]
    graph += inverter("Ifb_y", "ky", "y2")
    graph.append(mos("Nkeep_y", "N", "y2", "ky", "VSS", "keeper", True))
    return graph


def verify_np():
    graph, rows = np_graph(), []
    n_evaluation = [m for m in graph if m["role"] == "n_evaluation"]
    p_evaluation = [m for m in graph if m["role"] == "p_evaluation"]
    for a, b, c in itertools.product((0, 1), repeat=3):
        values = dict(VDD=1, VSS=0, a=a, b=b, c=c, ab=1-a, bb=1-b, cb=1-c, phi=1, phib=0)
        raw_x = int(path_to(n_evaluation, values, "raw_x", "VSS") is None)
        raw_xb = int(path_to(n_evaluation, values, "raw_xb", "VSS") is None)
        values.update(raw_x=raw_x, raw_xb=raw_xb)
        y2 = int(path_to(p_evaluation, values, "y2", "VDD") is not None)
        assert raw_x == (a ^ b) and raw_xb == 1-raw_x and y2 == (a ^ b ^ c)
        for phase in ("precharge", "evaluate"):
            rx, rxb, y = (1, 1, 0) if phase == "precharge" else (raw_x, raw_xb, y2)
            values.update(phi=int(phase == "evaluate"), phib=int(phase == "precharge"),
                          raw_x=rx, raw_xb=rxb, y2=y, kx=1-rx, kxb=1-rxb, ky=1-y)
            outputs = {n: values[n] for n in ("ab", "bb", "cb", "raw_x", "raw_xb", "kx", "kxb", "y2", "ky")}
            check_outputs(graph, values, outputs)
            rows.append(dict(a=a, b=b, c=c, phase=phase, raw_x=rx, raw_xb=rxb,
                             y1_tied_VSS=0, y2=y, expected_y2=0 if phase == "precharge" else a ^ b ^ c,
                             rail_exclusive=True, passed=True))
    csv_file("np_domino_checks.csv", rows)
    return dict(input_cases=8, phase_cases=len(rows), MOS_including_input_inverters_and_keepers=len(graph),
                y1_implementation="VSS constant, from independently derived original function",
                y2_implementation="N-type dual-rail XOR raw nodes, directly followed by P-type parity stage",
                clock_protocol="phi0/phib1: Nprecharge HIGH, Preset LOW; phi1/phib0: evaluate; stable A/B/C and complements",
                monotonicity="Nraw_x/Nraw_xb only fall; the Pstage y2 only rises during evaluate",
                synthesis_scope="Part6(c) functional reimplementation; its sizing/timing is not the original part6(a) gate-delay network",
                keeper_scope="Weak side-branch feedback keepers; final stable connectivity only, not transient contention sizing", graph=graph)


PATHS = [
    ("R1", "R4", "NAND(A,B)->NOR", 1.0),
    ("R2", "R4", "NAND(A,B)->NOR", 1.0),
    ("R1", "R4", "XOR->NAND(X,C)->NOR", 2.0),
    ("R2", "R4", "XOR->NAND(X,C)->NOR", 2.0),
    ("R3", "R4", "NAND(X,C)->NOR", 1.0),
    ("R1", "R5", "XOR->XOR", 2.0),
    ("R2", "R5", "XOR->XOR", 2.0),
    ("R3", "R5", "XOR", 1.0),
]


def verify_timing():
    configs = {
        "literal_positive_R4_capture_delay": dict(R1=0, R2=0, R3=0, R4=.6, R5=0),
        "classroom_adverse_R4_capture_skew": dict(R1=.6, R2=.6, R3=.6, R4=0, R5=.6),
        "literal_student_launch_only_insertion": dict(R1=.6, R2=.6, R3=.6, R4=.6, R5=0),
        "literal_balanced_clock_redesign": dict(R1=.6, R2=.6, R3=.6, R4=.6, R5=.6),
        "classroom_add_two_inverters_to_R4_capture": dict(R1=.6, R2=.6, R3=.6, R4=.6, R5=.6),
    }
    rows, summaries = [], {}
    for name, clocks in configs.items():
        local = []
        for launch, capture, sequence, gate_delay in PATHS:
            skew = clocks[capture] - clocks[launch]
            period = .2 + gate_delay + .2 - skew
            # Gate contamination delays were not separately specified.  This
            # hold value assumes the stated scalar gate delay also bounds min.
            hold_slack = .1 + gate_delay - .2 - skew
            row = dict(interpretation=name, launch=launch, capture=capture, path=sequence,
                       gate_delay_ns=gate_delay, launch_clock_ns=clocks[launch], capture_clock_ns=clocks[capture],
                       capture_minus_launch_skew_ns=skew, setup_min_period_ns=period,
                       required_logic_contamination_ns=.2+skew-.1,
                       hold_slack_ns_equal_gate_delay_assumption=hold_slack,
                       conditional_hold_pass=hold_slack >= -1e-12)
            local.append(row)
            rows.append(row)
        period = max(r["setup_min_period_ns"] for r in local)
        summaries[name] = dict(clock_arrival_ns=clocks, minimum_period_ns=period,
                              maximum_frequency_MHz=1000/period,
                              meets_400MHz=period <= 2.5+1e-12,
                              conditional_min_hold_slack_ns=min(r["hold_slack_ns_equal_gate_delay_assumption"] for r in local),
                              conditional_hold_pass=all(r["conditional_hold_pass"] for r in local))
    assert math.isclose(summaries["literal_positive_R4_capture_delay"]["minimum_period_ns"], 2.4)
    assert math.isclose(summaries["classroom_adverse_R4_capture_skew"]["minimum_period_ns"], 3.0)
    assert not summaries["literal_student_launch_only_insertion"]["meets_400MHz"]
    assert summaries["literal_balanced_clock_redesign"]["meets_400MHz"]
    assert summaries["classroom_add_two_inverters_to_R4_capture"]["meets_400MHz"]
    csv_file("timing_paths.csv", rows)
    return dict(path_count=len(PATHS), configurations=len(configs), row_count=len(rows),
                tpcq_ns=.2, tccq_ns=.1, setup_ns=.2, hold_ns=.2, inverter_delay_ns=.3,
                setup_equation="T >= t_launch+tpcq+tlogic+tsetup-t_capture",
                hold_equation="t_launch+tccq+t_cd >= t_capture+thold",
                hold_scope="t_cd of each logic gate is unspecified; reported hold results are conditional on using stated scalar gate delays as minimum delays too",
                literal_original_hold_requirements_ns={"any_launch_to_R4": .7, "any_launch_to_R5": .1},
                balanced_tree_hold_requirement_ns=.1,
                ambiguity="Figure places delay on R4 capture branch, but classroom answer treats +0.6 as adverse; both preserved with explicit sign",
                literal_redesign="Add2inverters to each launch clockR1/R2/R3 AND toR5capture; R4alreadyhas0.6ns delay; all arrivals0.6ns",
                classroom_redesign="Normalize adverse reading to launch/R5 arrivals0.6ns andR4arrival0; add2inverters(0.6ns) toR4branch, making all arrivals0.6ns",
                structural_path_scope="Use printed primitive-gate path delays; do not reuse these delays for optimized NP synthesis",
                results=summaries)


def main():
    results = dict(status="PASS", method="Standard-library ideal MOS switch graphs, exhaustive truth tables and analytical timing",
                   Q1i=verify_dpl(), Q2=verify_carry(), Q5=verify_layout(),
                   Q6_original=verify_original_q6(), Q6_NP=verify_np(), Q6_timing=verify_timing())
    (HERE / "logic_timing_verification.json").write_text(json.dumps(results, indent=2)+"\n", encoding="utf-8")
    print("PASS: DPL8; carry128/256phases; layout8/14MOS; originalQ6truth8; NP16phases; timing40paths across5interpretations.")


if __name__ == "__main__":
    main()
