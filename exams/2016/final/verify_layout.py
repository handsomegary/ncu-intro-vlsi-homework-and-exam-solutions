from pathlib import Path
from itertools import product
import csv
import json

OUT = Path(__file__).resolve().parent
devices_b = [
    ("P1", "p", "VDD", "u", "a"), ("N1", "n", "VSS", "u", "a"),
    ("P2", "p", "u", "VDD", "VDD"), ("N2", "n", "u", "VSS", "VSS"),
    ("P3", "p", "VDD", "s1", "u"), ("N3", "n", "VSS", "Z", "u"),
    ("P4", "p", "s1", "s2", "b"), ("N4", "n", "Z", "VSS", "b"),
    ("P5", "p", "s2", "Z", "c"), ("N5", "n", "VSS", "Z", "c"),
    ("P6", "p", "Z", "fp", "VDD"), ("N6", "n", "Z", "fn", "VSS"),
]
devices_a = [
    ("P1", "p", "VDD", "u", "Y"), ("N1", "n", "VSS", "u", "Y"),
    ("P2", "p", "u", "v", "C"), ("N2", "n", "u", "v", "Cbar"),
    ("P3", "p", "v", "r", "Cbar"), ("N3", "n", "v", "r", "C"),
    ("P4", "p", "r", "VDD", "X"), ("N4", "n", "r", "VSS", "X"),
    ("P5", "p", "VDD", "X", "v"), ("N5", "n", "VSS", "X", "v"),
    ("P6", "p", "X", "VDD", "X"), ("N6", "n", "X", "VSS", "X"),
]
for name, devices in (("q4a", devices_a), ("q4b", devices_b)):
    with (OUT / f"{name}_literal_netlist.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["device", "type", "left_channel", "right_channel", "gate"])
        w.writerows(devices)


def reachable(graph, start, end):
    seen, todo = set(), [start]
    while todo:
        n = todo.pop()
        if n == end:
            return True
        if n not in seen:
            seen.add(n); todo.extend(graph.get(n, set()) - seen)
    return False


rows = []
for a, b, c in product((0, 1), repeat=3):
    values = {"VDD": 1, "VSS": 0, "a": a, "b": b, "c": c, "u": 1-a}
    graph = {}
    for name, kind, left, right, gate in devices_b:
        on = values[gate] == (0 if kind == "p" else 1)
        if name in ("P2", "N2", "P6", "N6"):
            assert not on
        if on:
            graph.setdefault(left, set()).add(right)
            graph.setdefault(right, set()).add(left)
    high, low = reachable(graph, "Z", "VDD"), reachable(graph, "Z", "VSS")
    assert high != low
    expected = a and not b and not c
    assert high == expected
    assert reachable(graph, "u", "VDD") == (not a)
    assert reachable(graph, "u", "VSS") == bool(a)
    rows.append({"a": a, "b": b, "c": c, "u": 1-a, "Z_VDD_path": high,
                 "Z_VSS_path": low, "Z": int(high), "expected_a_bbar_cbar": int(expected)})
with (OUT / "q4b_switch_truth.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# Literal column 6 opposes either ideal rail value at X. This is a countercheck
# against silently identifying the extracted source with a clean digital latch.
col6 = [{"assumed_X": x, "P6_on": x == 0, "N6_on": x == 1,
         "opposing_rail": "VDD" if x == 0 else "VSS"} for x in (0, 1)]
result = {"q4b_12_device_switch_graph_rows": len(rows), "q4b_all_checks_passed": True,
          "q4b_function": "Z=a & ~b & ~c", "q4b_off_isolation_MOS": ["P2", "N2", "P6", "N6"],
          "q4a_literal_column6_countercheck": col6,
          "q4a_scope": "Literal extraction only. Analog levels/strengths are not characterized; normal rail-restoring latch behavior is not claimed."}
(OUT / "q4_verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
