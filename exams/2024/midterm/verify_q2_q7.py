"""Exhaustive independent checks of the 2024 midterm Q2/Q7 diagrams.

Uses Python's standard library only.  The MUX leaf constants and MOS switch
graphs transcribe the supplied student's correct diagrams; the reference
Boolean functions come independently from the photographed printed prompt.
Run from any directory: python verify_q2_q7.py
"""
from pathlib import Path
import csv
import itertools
import json

HERE = Path(__file__).resolve().parent

# Every 2:1 cell in the supplied diagram marks the left input 1, right input 0.
# Four select levels, from the root/output toward the leaves: s, y, x, z.
# Thus the printed sixteen leaves run from (s,y,x,z)=1111 to 0000.
CONTROL_ORDER = ("s", "y", "x", "z")
LEAVES = (1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0)

# An edge is (device label, gate variable, first terminal, second terminal).
# Source/drain terminals are undirected in this ideal connectivity check.
# Bodies and analogue effects are outside a Boolean switch-model proof.
NETWORKS = {
    "a": {
        "variables": "XYZ",
        "pdn": [("NX", "X", "F", "n1"),
                ("NY", "Y", "n1", "VSS"),
                ("NZ", "Z", "n1", "VSS")],
        "pun": [("PX", "X", "VDD", "F"),
                ("PY", "Y", "VDD", "p1"),
                ("PZ", "Z", "p1", "F")],
        "reference": "NOT[X(Y+Z)]",
    },
    "b": {
        "variables": "XYZ",
        "pdn": [("NX", "X", "F", "n1"),
                ("NY", "Y", "n1", "VSS"),
                ("NZ", "Z", "F", "VSS")],
        "pun": [("PZ", "Z", "VDD", "p1"),
                ("PX", "X", "p1", "F"),
                ("PY", "Y", "p1", "F")],
        "reference": "NOT[XY+Z]",
    },
    "c": {
        "variables": "WXYZ",
        "pdn": [("NX", "X", "F", "VSS"),
                ("NY", "Y", "F", "n1"),
                ("NW", "W", "n1", "VSS"),
                ("NZ", "Z", "n1", "VSS")],
        "pun": [("PX", "X", "VDD", "p1"),
                ("PY", "Y", "p1", "F"),
                ("PW", "W", "p1", "p2"),
                ("PZ", "Z", "p2", "F")],
        "reference": "NOT[X+Y(W+Z)]",
    },
}


def mux_value(inputs):
    values = list(LEAVES)
    for select in reversed(CONTROL_ORDER):
        values = [values[i if inputs[select] else i + 1]
                  for i in range(0, len(values), 2)]
    assert len(values) == 1
    return values[0]


def conducting_path(edges, inputs, pmos, rail):
    graph = {}
    for name, gate, a, b in edges:
        on = not inputs[gate] if pmos else bool(inputs[gate])
        if on:
            graph.setdefault(a, []).append((b, name))
            graph.setdefault(b, []).append((a, name))
    seen = {"F"}
    queue = [("F", [])]
    for node, path in queue:
        if node == rail:
            return path
        for neighbor, device in graph.get(node, []):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, path + [device]))
    return None


def reference_q7(part, inputs):
    x, y, z = (bool(inputs[k]) for k in "XYZ")
    if part == "a":
        return int(not (x and (y or z)))
    if part == "b":
        return int(not ((x and y) or z))
    return int(not (x or (y and (bool(inputs["W"]) or z))))


def export_csv(name, rows):
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    mux_rows = []
    for bits in itertools.product((0, 1), repeat=4):
        inputs = dict(zip(CONTROL_ORDER, bits))
        s, x, y, z = (inputs[k] for k in ("s", "x", "y", "z"))
        selected_cofactor = int((x and y) or (y and z)) if s else int(x or y or z)
        actual = mux_value(inputs)
        leaf_index = 15 - sum(inputs[name] << (3 - i)
                              for i, name in enumerate(CONTROL_ORDER))
        row = dict(s=s, x=x, y=y, z=z, leaf_index_left_to_right=leaf_index,
                   mux_output=actual, expected=selected_cofactor,
                   passed=actual == selected_cofactor)
        assert row["passed"], row
        assert actual == LEAVES[leaf_index]
        mux_rows.append(row)

    cmos_rows = []
    counts = {}
    for part, net in NETWORKS.items():
        count = 0
        for bits in itertools.product((0, 1), repeat=len(net["variables"])):
            inputs = dict(zip(net["variables"], bits))
            down = conducting_path(net["pdn"], inputs, False, "VSS")
            up = conducting_path(net["pun"], inputs, True, "VDD")
            grounded, powered = down is not None, up is not None
            exclusive = grounded != powered
            actual = int(powered) if exclusive else "UNDEFINED"
            expected = reference_q7(part, inputs)
            row = dict(part=part, W=inputs.get("W", ""),
                       X=inputs["X"], Y=inputs["Y"], Z=inputs["Z"],
                       pdn_connected=grounded, pun_connected=powered,
                       rail_exclusive=exclusive, output=actual,
                       expected=expected, pdn_path=";".join(down or []),
                       pun_path=";".join(up or []),
                       passed=exclusive and actual == expected)
            assert row["passed"], row
            cmos_rows.append(row)
            count += 1
        counts[part] = count

    export_csv("q2_mux_truth.csv", mux_rows)
    export_csv("q7_switch_checks.csv", cmos_rows)
    summary = {
        "status": "PASS",
        "scope": "Ideal switch connectivity and Boolean polarity, not analogue timing",
        "source": "2024 midterm printed pages 1–2 and supplied answer pages 4 and 6",
        "q2": {
            "cases": len(mux_rows),
            "cofactor_s1": "xy+yz",
            "cofactor_s0": "x+y+z",
            "control_order_root_to_leaf": list(CONTROL_ORDER),
            "cell_convention": "left input is selected by 1; right by 0",
            "leaf_input_words_left_to_right": [format(i, "04b") for i in range(15, -1, -1)],
            "leaf_constants_left_to_right": list(LEAVES),
            "mux_cells": 15,
            "data_path_stages": 4,
            "student_diagram_logic": "correct",
            "csv": "q2_mux_truth.csv",
        },
        "q7": {
            "case_counts": counts,
            "total_cases": len(cmos_rows),
            "reference_functions": {part: net["reference"] for part, net in NETWORKS.items()},
            "transistor_counts": {part: len(net["pdn"]) + len(net["pun"])
                                  for part, net in NETWORKS.items()},
            "all_rails_exclusive": all(r["rail_exclusive"] for r in cmos_rows),
            "all_output_polarities_correct": all(r["passed"] for r in cmos_rows),
            "student_diagrams_logic": "all three correct",
            "csv": "q7_switch_checks.csv",
        },
    }
    (HERE / "q2_q7_verification.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("PASS: 16 MUX cases; Q7 CMOS 8+8+16 cases; exclusive rails and correct polarity.")


if __name__ == "__main__":
    main()
