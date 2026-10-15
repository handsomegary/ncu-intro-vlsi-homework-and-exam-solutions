"""Check actual HSPICE measurement CSVs against HW2 equations and logic levels."""
import csv
import json
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    checks = []

    def rows(stem):
        with (here / (stem + "_measurements.csv")).open(newline="", encoding="utf-8") as f:
            return [{k: float(v) for k, v in row.items()} for row in csv.DictReader(f)]

    def check(name, observed, expected, tolerance, kind="absolute"):
        error = abs(observed - expected)
        if kind == "relative":
            error /= abs(expected)
        checks.append(dict(check=name, observed=observed, expected=expected,
                           error=error, tolerance=tolerance, kind=kind,
                           passed=error <= tolerance))

    q1 = rows("q1_constant_leakage")[0]
    check("q1_initial_V", q1["v_initial"], 1.35, 1e-9)
    check("q1_retention_s", q1["retention"], 0.0126, 1e-4, "relative")
    check("q1_voltage_at_12m6_V", q1["v_at_12m6"], 0.72, 1e-5)
    ideal = rows("q2_constant_resistance")[0]
    for ab, expected in {"00": 1.8, "01": 0.36, "10": 0.36, "11": 0.2}.items():
        check("q2_resistor_v" + ab, ideal["v" + ab], expected, 1e-9)
    cic = rows("q2_cic018_tt")
    for row in cic:
        tag = f"q2_CIC_TT_ratio_{row['ratio']:g}"
        check(tag + "_symmetry_V", row["v01"], row["v10"], 1e-9)
        check(tag + "_high_V", row["v00"], 1.8, 1e-5)
        for ab in ["01", "10", "11"]:
            observed = row["v" + ab]
            checks.append(dict(check=tag + "_logic_low_" + ab, observed=observed,
                               expected="<=0.36", error=max(0, observed - 0.36),
                               tolerance=0, kind="upper_bound", passed=0 <= observed <= 0.36))
        check(tag + "_supply_power_W", row["p01"], 1.8 * row["idd01"], 1e-8, "relative")
    with (here / "validation_checks.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["check", "observed", "expected", "error", "tolerance", "kind", "passed"])
        writer.writeheader()
        writer.writerows(checks)
    failures = [row["check"] for row in checks if not row["passed"]]
    summary_path = here / "validation_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
    summary["numerical_validation"] = {"total": len(checks), "passed": len(checks) - len(failures), "failures": failures}
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"{len(checks) - len(failures)}/{len(checks)} numerical checks passed")
    for failure in failures:
        print("FAILED: " + failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
