"""Exhaustive, dependency-free Boolean/switch-connectivity checks for HW1.

Run: python verify_logic.py
This verifies actual transistor edge lists matching solutions.tex, not SPICE.
MOS body diodes, thresholds, capacitances and switching transients are excluded.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def lit(name: str, values: dict[str, int]) -> int:
    return 1 - values[name[1:]] if name.startswith("!") else values[name]


def reachable(edges: list[tuple[str, str, str, str]], values: dict[str, int], start: str) -> set[str]:
    """Edges are (terminal_1, terminal_2, gate_literal, n_or_p)."""
    graph: dict[str, set[str]] = defaultdict(set)
    for u, v, gate, kind in edges:
        if lit(gate, values) == (1 if kind == "n" else 0):
            graph[u].add(v)
            graph[v].add(u)
    seen, todo = {start}, [start]
    while todo:
        for target in graph[todo.pop()] - seen:
            seen.add(target)
            todo.append(target)
    return seen


def static_output(edges, values, expected):
    connected = reachable(edges, values, "F")
    up, down = "VDD" in connected, "VSS" in connected
    assert up != down, ("floating or rail short", values, connected)
    assert int(up) == expected, ("wrong output", values, connected, expected)
    return int(up), int(down)


# Device order follows P1, P2, ... N1, N2, ... in each figure.
NOR4 = [
    ("VDD", "p1", "x", "p"), ("p1", "F", "y", "p"),
    ("F", "VSS", "x", "n"), ("F", "VSS", "y", "n"),
]
MINORITY10 = [
    ("VDD", "pm", "x", "p"), ("VDD", "pm", "y", "p"),
    ("pm", "F", "z", "p"), ("pm", "pxy", "x", "p"),
    ("pxy", "F", "y", "p"),
    ("F", "nxy", "x", "n"), ("nxy", "VSS", "y", "n"),
    ("F", "nz", "z", "n"), ("nz", "VSS", "x", "n"),
    ("nz", "VSS", "y", "n"),
]
XNOR8_CORE = [
    ("VDD", "pab", "A", "p"), ("pab", "F", "B", "p"),
    ("VDD", "pnot", "!A", "p"), ("pnot", "F", "!B", "p"),
    ("F", "nm", "A", "n"), ("F", "nm", "B", "n"),
    ("nm", "VSS", "!A", "n"), ("nm", "VSS", "!B", "n"),
]


def tg(u: str, v: str, control: str):
    inverted = control[1:] if control.startswith("!") else "!" + control
    return [(u, v, control, "n"), (u, v, inverted, "p")]


def main():
    counts = {}
    rows = []

    for bits in itertools.product((0, 1), repeat=4):
        v = dict(zip("wxyz", bits))
        w, x, y, z = bits
        specified = int(not (x or y or (w and y and z)))
        assert specified == int(not (x or y))
        out, pdn = static_output(NOR4, v, specified)
        rows.append(dict(problem="1a", inputs="".join(map(str, bits)), expected=specified,
                         actual=out, pdn=pdn, status="PASS"))
    counts["1a_all_wxyz"] = 16

    for bits in itertools.product((0, 1), repeat=3):
        v = dict(zip("xyz", bits))
        x, y, z = bits
        specified = int((not x and not y) or (not x and not z) or (not y and not z))
        pos = int((x or y) and (x or z) and (y or z))
        factored = int((x and y) or (z and (x or y)))
        assert pos == factored == 1 - specified
        out, pdn = static_output(MINORITY10, v, specified)
        rows.append(dict(problem="1b", inputs="".join(map(str, bits)), expected=specified,
                         actual=out, pdn=pdn, status="PASS"))
    counts["1b_all_xyz"] = 8

    # Each entry is the original problem table's [z3,z2,z1,z0] input-index tuple.
    original_table = {3: (3, 2, 1, 0), 2: (2, 1, 0, 3),
                      1: (1, 0, 3, 2), 0: (0, 3, 2, 1)}
    selector_edges = []
    for i in range(4):
        for j in range(4):
            data_index = (i + j - 3) % 4
            selector_edges += tg(f"a{data_index}", f"z{i}", f"c{j}")
    assert len(selector_edges) == 32
    for selected in range(4):
        for bits in itertools.product((0, 1), repeat=4):
            # bits is a0,a1,a2,a3; output strings use z3,z2,z1,z0.
            v = {f"a{i}": bit for i, bit in enumerate(bits)}
            v.update({f"c{j}": int(j == selected) for j in range(4)})
            expected = [bits[k] for k in original_table[selected]]
            actual = []
            for output in (3, 2, 1, 0):
                connected = reachable(selector_edges, v, f"z{output}")
                data_nodes = {n for n in connected if n.startswith("a")}
                expected_node = f"a{original_table[selected][3-output]}"
                assert data_nodes == {expected_node}, (v, output, connected, expected_node)
                actual.append(v[expected_node])
            assert actual == expected
            rows.append(dict(problem="2", inputs=f"c{selected}=1;a3a2a1a0=" + "".join(map(str, bits[::-1])),
                             expected="".join(map(str, expected)), actual="".join(map(str, actual)),
                             pdn="n/a", status="PASS"))
    counts["2_one_hot_controls_times_all_data"] = 64

    tg_xnor = tg("B_data", "F", "A") + tg("Bbar_data", "F", "!A")
    for bits in itertools.product((0, 1), repeat=2):
        v = dict(zip("AB", bits))
        A, B = bits
        specified = int(A == B)
        original_pass = B if A else 1 - B
        assert original_pass == specified
        out, pdn = static_output(XNOR8_CORE, v, specified)
        rows.append(dict(problem="3_static", inputs="".join(map(str, bits)), expected=specified,
                         actual=out, pdn=pdn, status="PASS"))
        connected = reachable(tg_xnor, v, "F")
        expected_node = "B_data" if A else "Bbar_data"
        assert {n for n in connected if n.endswith("_data")} == {expected_node}
        out = B if expected_node == "B_data" else 1 - B
        assert out == specified
        rows.append(dict(problem="3_TG", inputs="".join(map(str, bits)), expected=specified,
                         actual=out, pdn="n/a", status="PASS"))
    counts["3_static_all_AB"] = 4
    counts["3_TG_all_AB"] = 4

    inverter = [("VDD", "F", "u", "p"), ("F", "VSS", "u", "n")]
    for u in (0, 1):
        static_output(inverter, {"u": u}, 1 - u)
    counts["shared_inverter_truth_values"] = 2

    # Explicitly confirm why unused control codes are outside the TG specification.
    zero_control = {f"c{j}": 0 for j in range(4)}
    assert reachable(selector_edges, zero_control, "z0") == {"z0"}
    multi_control = {f"c{j}": int(j in (2, 3)) for j in range(4)}
    assert {"a0", "a3"} <= reachable(selector_edges, multi_control, "z0")
    counts["out_of_spec_control_examples"] = 2

    with (HERE / "truth_tables.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=["problem", "inputs", "expected", "actual", "pdn", "status"])
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "status": "PASS", "model": "ideal binary MOS switch connectivity; not SPICE",
        "test_counts": counts, "total_asserted_cases": sum(counts.values()),
        "truth_table_rows": len(rows),
        "device_counts": {"1a": 4, "1b": 10, "2_including_control_inverters": 40,
                          "3_static_core": 8, "3_static_with_input_inverters": 12,
                          "3_TG_with_input_inverters": 8},
        "solutions_tex_sha256": hashlib.sha256((HERE / "solutions.tex").read_bytes()).hexdigest(),
        "limitations": ["No transistor sizing or process-model evaluation",
                        "No analog swing, delay, capacitance or switching-transient validation",
                        "Problem 2 checked against only its four specified one-hot controls"],
    }
    (HERE / "verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "test_counts": counts,
                      "total_asserted_cases": report["total_asserted_cases"]}, indent=2))


if __name__ == "__main__":
    main()
