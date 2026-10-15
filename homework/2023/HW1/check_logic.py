"""Exhaustive ideal-switch verification of the transistor topologies in solution.tex.

No third-party packages. Expected functions are independently evaluated from the
printed formulas/table, while actual outputs are found by graph reachability.
This is digital connectivity verification, not a SPICE or timing simulation.
"""
from pathlib import Path
from itertools import product
from collections import defaultdict
import csv
import json

HERE = Path(__file__).resolve().parent


def transistor(name, kind, gate, a, b):
    return {"name": name, "kind": kind, "gate": gate, "a": a, "b": b}


def aoi(g1, g2, g3, g4, g5):
    """PDN = g1(g2+g3)+g4*g5. PUN is the graph-theoretic series/parallel dual."""
    return [
        transistor("N1", "n", g1, "OUT", "n1"),
        transistor("N2", "n", g2, "n1", "GND"),
        transistor("N3", "n", g3, "n1", "GND"),
        transistor("N4", "n", g4, "OUT", "n2"),
        transistor("N5", "n", g5, "n2", "GND"),
        transistor("P1", "p", g1, "VDD", "p1"),
        transistor("P2", "p", g2, "VDD", "p2"),
        transistor("P3", "p", g3, "p2", "p1"),
        transistor("P4", "p", g4, "p1", "OUT"),
        transistor("P5", "p", g5, "p1", "OUT"),
    ]


def inverter(prefix, signal, complement):
    return [transistor(prefix + "N", "n", signal, complement, "GND"),
            transistor(prefix + "P", "p", signal, complement, "VDD")]


def reached(devices, values, start):
    edges = defaultdict(set)
    for d in devices:
        enabled = values[d["gate"]] == (1 if d["kind"] == "n" else 0)
        if enabled:
            edges[d["a"]].add(d["b"])
            edges[d["b"]].add(d["a"])
    seen = {start}
    todo = [start]
    while todo:
        for other in edges[todo.pop()]:
            if other not in seen:
                seen.add(other)
                todo.append(other)
    return seen


def logic_output(devices, values, output="OUT"):
    seen = reached(devices, values, output)
    high, low = "VDD" in seen, "GND" in seen
    assert high != low, f"Floating or rail contention at {output}: {values}"
    return int(high), high, low


def rows_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    q1a = aoi("w", "x", "y", "y", "z")
    q1b = aoi("x", "y", "z", "y", "z")
    xor = [
        transistor("N1", "n", "A", "OUT", "n1"),
        transistor("N2", "n", "B", "n1", "GND"),
        transistor("N3", "n", "Abar", "OUT", "n2"),
        transistor("N4", "n", "Bbar", "n2", "GND"),
        transistor("P1", "p", "A", "VDD", "p1"),
        transistor("P2", "p", "B", "VDD", "p1"),
        transistor("P3", "p", "Abar", "p1", "OUT"),
        transistor("P4", "p", "Bbar", "p1", "OUT"),
    ]
    xor_inverters = inverter("IA", "A", "Abar") + inverter("IB", "B", "Bbar")
    mux = []
    for j in range(4):
        for k in range(4):
            control = f"c{3-k}"
            data = f"a{(j-k)%4}"
            mux += [transistor(f"T{j}{k}N", "n", control + "bar", data, f"z{j}"),
                    transistor(f"T{j}{k}P", "p", control, data, f"z{j}")]
    control_inverters = sum((inverter(f"IC{i}", f"c{i}", f"c{i}bar") for i in range(4)), [])
    circuits = {"q1a": q1a, "q1b": q1b, "q3_xor": xor,
                "q3_inverters": xor_inverters, "q2_tg_bank": mux,
                "q2_control_inverters": control_inverters}
    (HERE / "circuits.json").write_text(json.dumps(circuits, indent=2) + "\n", encoding="utf-8")

    logic_rows = []
    for label, names, devices, oracle in [
        ("Q1(a)", "wxyz", q1a, lambda v: int(not (v["w"] and (v["x"] or v["y"]) or v["y"] and v["z"]))),
        ("Q1(b)", "xyz", q1b, lambda v: int((not v["x"] and not v["y"]) or (not v["x"] and not v["z"]) or (not v["y"] and not v["z"]))),
        ("Q3", "AB", xor, lambda v: v["A"] ^ v["B"]),
    ]:
        for bits in product((0, 1), repeat=len(names)):
            values = dict(zip(names, bits))
            if label == "Q3":
                # Solve the two actual CMOS inverters, rather than inject ideal complements.
                values["Abar"], _, _ = logic_output(inverter("IA", "A", "Abar"), values, "Abar")
                values["Bbar"], _, _ = logic_output(inverter("IB", "B", "Bbar"), values, "Bbar")
            actual, high, low = logic_output(devices, values)
            expected = oracle(values)
            assert actual == expected, (label, bits, actual, expected)
            logic_rows.append({"question": label, "input_order": names,
                               "inputs": "".join(map(str, bits)), "expected": expected,
                               "actual": actual, "pun_connected": int(high),
                               "pdn_connected": int(low), "pass": True})
    rows_csv(HERE / "truth_tables.csv", logic_rows)

    # Each table row is evaluated for all 16 data words. No invented requirements
    # are assigned to the 12 control words omitted by the problem.
    legal_control_mapping = {
        (0, 1, 1, 1): (0, 1, 2, 3),  # c3 c2 c1 c0 -> z0 z1 z2 z3
        (1, 0, 1, 1): (3, 0, 1, 2),
        (1, 1, 0, 1): (2, 3, 0, 1),
        (1, 1, 1, 0): (1, 2, 3, 0),
    }
    mux_rows, illegal_rows = [], []
    for cbits in product((0, 1), repeat=4):
        controls = dict(zip(("c3", "c2", "c1", "c0"), cbits))
        for abit in product((0, 1), repeat=4):
            vals = {**controls, **dict(zip(("a3", "a2", "a1", "a0"), abit))}
            for i in range(4):
                ci = f"c{i}"
                vals[ci + "bar"], _, _ = logic_output(inverter(f"IC{i}", ci, ci + "bar"), vals, ci + "bar")
            for j in range(4):
                seen = reached(mux, vals, f"z{j}")
                sources = sorted(n for n in seen if len(n) == 2 and n[0] == "a")
                possible_values = {vals[n] for n in sources}
                if cbits in legal_control_mapping:
                    expected_source = f"a{legal_control_mapping[cbits][j]}"
                    assert sources == [expected_source], (cbits, j, sources, expected_source)
                    actual = next(iter(possible_values))
                    assert actual == vals[expected_source]
                    mux_rows.append({"controls_c3_to_c0": "".join(map(str, cbits)),
                                     "data_a3_to_a0": "".join(map(str, abit)), "output": f"z{j}",
                                     "expected_source": expected_source, "connected_sources": "+".join(sources),
                                     "expected_value": vals[expected_source], "actual_value": actual,
                                     "pass": True})
                else:
                    state = "floating" if not sources else "contention" if len(possible_values) > 1 else "multiple_sources_same_value"
                    illegal_rows.append({"controls_c3_to_c0": "".join(map(str, cbits)),
                                         "data_a3_to_a0": "".join(map(str, abit)), "output": f"z{j}",
                                         "connected_sources": "+".join(sources), "state": state})
    rows_csv(HERE / "mux_connectivity.csv", mux_rows)
    rows_csv(HERE / "illegal_controls.csv", illegal_rows)
    result = {"status": "PASS", "model": "ideal on/off MOS switch connectivity",
              "q1a_cases": 16, "q1b_cases": 8, "q3_cases": 4,
              "q2_legal_control_data_cases": 64, "q2_output_checks": len(mux_rows),
              "total_functional_output_checks": len(logic_rows) + len(mux_rows),
              "q2_invalid_control_output_characterizations": len(illegal_rows),
              "transistor_counts": {"q1a": 10, "q1b": 10, "q2_including_control_inverters": len(mux)+len(control_inverters),
                                    "q3_including_input_inverters": 12},
              "checks": ["Exact truth tables", "Exactly one rail connected in every static CMOS state",
                         "Actual CMOS inverter topology used to generate complements",
                         "Each legal transmission-gate output reaches exactly the required data input"],
              "limitations": ["No analog voltage/timing/power simulation", "Q2 assumes exactly one control is low",
                              "Unspecified control combinations are characterized, not declared correct"]}
    (HERE / "verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
