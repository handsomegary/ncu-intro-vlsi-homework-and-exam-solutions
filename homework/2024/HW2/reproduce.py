"""Run HW2 HSPICE decks and keep simulator output separate from calculations.

Usage: python reproduce.py --hspice C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com
The CIC library is a local prerequisite at D:/cic018.l and is not distributed.
Only HSPICE measurement tables represent simulated results.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import subprocess
import tempfile
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hspice", default="C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com")
    parser.add_argument("--raw-dir", default=str(Path(tempfile.gettempdir()) / "intro-vlsi-2024" / "HW2"))
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    rawdir = Path(args.raw_dir).resolve()
    rawdir.mkdir(parents=True, exist_ok=True)
    decks = ["q1_constant_leakage", "q2_constant_resistance", "q2_cic018_tt"]
    # These are independently evaluated closed-form expectations, NOT simulation.
    with (here / "analytic_expected.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["model", "case", "quantity", "value", "unit", "provenance"])
        writer.writerow(["constant_leakage", "illustrative", "v_initial", 1.8 - 0.45, "V", "closed_form"])
        writer.writerow(["constant_leakage", "illustrative", "retention", 20e-15 * (0.6 * 1.8 - 0.45) / 1e-12, "s", "closed_form"])
        for ab, resistance in [("00", None), ("01", 1000.0), ("10", 1000.0), ("11", 500.0)]:
            vout = 1.8 if resistance is None else 1.8 * resistance / (4000 + resistance)
            writer.writerow(["constant_resistance", ab, "vout", vout, "V", "closed_form"])
    statuses = []
    for stem in decks:
        command = [args.hspice, "-i", str(here / f"{stem}.sp"), "-o", str(rawdir / stem)]
        try:
            result = subprocess.run(command, cwd=here, capture_output=True, timeout=180)
            # Keep the actual stdout/stderr; .lis is independently created by HSPICE.
            raw = result.stdout + result.stderr
            (rawdir / f"{stem}.console.log").write_bytes(raw)
            output = raw.decode("utf-8", errors="replace")
            listing = rawdir / f"{stem}.lis"
            text = output + (listing.read_text(errors="replace") if listing.exists() else "")
            tables = list(rawdir.glob(f"{stem}.mt*.csv"))
            ok = result.returncode == 0 and "job concluded" in text.lower() and bool(tables)
            if "cannot connect to license server" in text.lower():
                detail = "FLEXlm service connection failed; check local network permissions and existing license service"
            else:
                detail = "HSPICE completed; measurements exported" if ok else "HSPICE failed or measurement table absent; inspect local raw logs"
            exported = []
            for table in tables if ok else []:
                lines = table.read_text(errors="replace").splitlines()
                rows = list(csv.DictReader(line for line in lines if line.strip() and not line.startswith(("$", "."))))
                if not rows or any("failed" in str(v).lower() for row in rows for v in row.values()):
                    ok = False
                    detail = "Measurement table contains missing or failed measurements"
                    break
                clean = here / f"{stem}_measurements.csv"
                with clean.open("w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
                    writer.writeheader()
                    writer.writerows({k: v.strip() if isinstance(v, str) else v for k, v in row.items()} for row in rows)
                exported.append(clean.name)
            statuses.append(dict(deck=f"{stem}.sp", status="completed" if ok else "failed", exit_code=result.returncode,
                                 detail=detail, measurement_files=";".join(exported) if ok else ""))
        except (OSError, subprocess.TimeoutExpired) as exc:
            statuses.append(dict(deck=f"{stem}.sp", status="failed", exit_code="", detail=str(exc), measurement_files=""))
    with (here / "simulation_status.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["deck", "status", "exit_code", "detail", "measurement_files"])
        writer.writeheader()
        writer.writerows(statuses)
    (here / "validation_summary.json").write_text(json.dumps({"simulator": "PrimeSim HSPICE S-2021.09 win64", "model": "CIC018 BSIM3 TT, local model not redistributed", "temperature_C": 25, "voltage_V": 1.8, "runs": statuses}, indent=2), encoding="utf-8")
    print(json.dumps(statuses, indent=2))
    if all(s["status"] == "completed" for s in statuses):
        return subprocess.run([sys.executable, str(here / "validate_results.py")], cwd=here).returncode
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
