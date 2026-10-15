"""Independent source-derived checks for 2016 final Q5 and Q6.

Q5 uses the one gate delay given in the exam as both min and max delay;
all unspecified wire delays are zero. This is not a transistor simulation.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import csv
import json

OUT = Path(__file__).resolve().parent
GATE_DELAY = {"XU": F(1, 2), "XV": F(1, 2), "IV": F(1, 5),
              "NOR": F(3, 10), "XNOR": F(2, 5), "R4wire": F(1, 10)}
EDGES = {"R1": ["XV", "XNOR", "R4wire"], "R2": ["XU"],
         "R3": ["XU", "XV"], "XU": ["NOR"], "XV": ["IV", "R6"],
         "IV": ["NOR"], "NOR": ["XNOR"], "XNOR": ["R5"],
         "R4wire": ["R4"]}


def paths(start, node=None, route=None):
    node = start if node is None else node
    route = [start] if route is None else route
    if node in ("R4", "R5", "R6"):
        return [route]
    return [p for nxt in EDGES.get(node, []) for p in paths(start, nxt, route + [nxt])]


def delay(route, repair):
    base = sum((GATE_DELAY.get(n, F(0)) for n in route), F(0))
    if route[-1] == "R4":
        base += F(2, 5) if repair == "zero_skew" else F(4, 5) if repair == "skew_safe" else F(0)
    if repair == "skew_safe" and route[-1] == "R6":
        base += F(2, 5)
    if repair == "skew_safe" and route == ["R1", "XNOR", "R5"]:
        base += F(2, 5)
    return base


all_paths = [p for r in ("R1", "R2", "R3") for p in paths(r)]
assert len(all_paths) == 8
rows = []
report = {}
for repair in ("original", "zero_skew", "skew_safe"):
    delays = [delay(p, repair) for p in all_paths]
    assert max(delays) == F(7, 5)
    for s in (F(-1, 2), F(0), F(1, 2)):
        key = f"{repair},s={float(s):+.1f}ns"
        tmin = F(3, 10) + max(delays) + F(3, 10) - s
        failures = [" -> ".join(p) for p, d in zip(all_paths, delays)
                    if F(1, 10) + d < F(2, 5) + s]
        report[key] = {"setup_period_ns": float(tmin),
                       "setup_bound_MHz": float(F(1000) / tmin),
                       "hold_violations": failures,
                       "valid_at_setup_bound": not failures}
    for p, d in zip(all_paths, delays):
        rows.append({"repair": repair, "path": " -> ".join(p), "data_delay_ns": float(d)})
assert len(report["original,s=+0.0ns"]["hold_violations"]) == 1
assert report["zero_skew,s=+0.0ns"]["valid_at_setup_bound"]
assert len(report["zero_skew,s=+0.5ns"]["hold_violations"]) == 4
assert all(report[f"skew_safe,s={float(s):+.1f}ns"]["valid_at_setup_bound"]
           for s in (F(-1, 2), F(0), F(1, 2)))
with (OUT / "q5_path_delays.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# Branch-only even inverter additions preserve all three output functions.
truth = []
for a, b, c in product((0, 1), repeat=3):
    u, v = b ^ c, a ^ c
    w = 1 - v
    z = 1 - (u | w)
    y = 1 - (z ^ a)
    for n in (2, 4):
        assert (a ^ (n % 2)) == a
    repaired_a = 1 - (1 - a)
    repaired_v = 1 - (1 - v)
    assert 1 - (z ^ repaired_a) == y
    assert repaired_v == v
    truth.append({"R1": a, "R2": b, "R3": c, "R4_D": a, "R5_D": y, "R6_D": v})
with (OUT / "q5_boolean_truth.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=truth[0].keys()); w.writeheader(); w.writerows(truth)

# Q6: independently compare each divider condition with its algebraic result.
# Old Q=0, P2 on, drive slave input down through TG + N1.
# Old Q=1, N2 on, drive slave input up through P1 + TG.
divider_cases = []
for rtg, rn1, rp1, rp2, rn2 in product((F(1), F(2), F(4)), repeat=5):
    low = (rtg + rn1) / (rp2 + rtg + rn1)
    high = rn2 / (rp1 + rtg + rn2)
    assert (low < F(1, 2)) == (rp2 > rtg + rn1)
    assert (high > F(1, 2)) == (rn2 > rp1 + rtg)
    divider_cases.append({"R_TG": float(rtg), "R_N1": float(rn1), "R_P1": float(rp1),
                          "R_P2": float(rp2), "R_N2": float(rn2),
                          "V_slave_low_over_VDD": float(low), "V_slave_high_over_VDD": float(high),
                          "low_write_pass": low < F(1, 2), "high_write_pass": high > F(1, 2)})
with (OUT / "q6_divider_cases.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=divider_cases[0].keys()); w.writeheader(); w.writerows(divider_cases)
report["Q6"] = {"forward_path_nominal_setup_ns": 0.3,
                 "TG_phase_table": {"CLK=0": {"master_input": "on", "master_feedback": "off", "slave_input": "off"},
                                    "CLK=1": {"master_input": "off", "master_feedback": "on", "slave_input": "on"}},
                 "low_write_condition": "R_P2 > R_TG + R_N1",
                 "high_write_condition": "R_N2 > R_TG + R_P1",
                 "divider_cases_checked": len(divider_cases),
                 "model_limit": "Linear ON-resistor / fixed-threshold approximation, not SPICE or a physical setup characterization."}
(OUT / "timing-verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"paths": len(all_paths), "boolean_rows": len(truth), "divider_cases": len(divider_cases), "all_checks_passed": True}))
