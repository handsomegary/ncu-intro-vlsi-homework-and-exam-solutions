# 2024 Homework 2: Non-ideal effects and pseudo-NMOS NOR

The original [homework2.pdf](../assignments/homework2.pdf) contains two analytical problems. This directory includes complete LaTeX derivations, a compiled PDF, and supplementary HSPICE verification that was actually executed.

## Assignment requirements and solutions

1. **Non-ideal Effect (5 points):** A PMOS precharges the circuit, and an NMOS controls the connection between the storage capacitor and BL. The NMOS threshold is `Vt`, its junction leakage is `IL`, and the buffer switching threshold is `0.4 Vdd`. Find `(a)` the capacitor's precharge voltage and `(b)` the retention time of stored data 1 after both transistors turn off.
   - Constant-threshold approximation: `VC(0) = Vdd - Vt`.
   - Constant-leakage approximation: `tret = C(0.6 Vdd - Vt)/IL`. A positive valid retention interval requires `Vt < 0.6 Vdd`.
   - **Read-topology qualification:** In the original figure, the buffer connects to BL, while the capacitor is on the opposite side of the access NMOS. After SL turns off, Out does not directly monitor the capacitor. The formula is therefore the intended stored-charge retention result, assuming a subsequent ideal read with negligible BL loading. A literal requirement that Out remain readable while both transistors stay off also requires BL capacitance, BL leakage, and a read protocol. The solution explains this limitation and charge sharing upon reselection.
2. **Logic Gate (5 points):** The upper PMOS gate connects to ground, and the two lower NMOS devices are in parallel. At equal sizes, `Rp = 2 Rn`. The problem explicitly treats on-resistance as constant, regardless of the linear or saturation region. Find `(a)` the Boolean function and `(b)` transistor sizes for a logic-low limit of `0.2 Vdd`.
   - The function is `Y = NOT(A OR B)`, a pseudo-NMOS NOR.
   - The wording "smallest voltage of logic 0" is interpreted as the **maximum acceptable logic-low voltage**, consistent with the circuit requirement.
   - The worst low occurs when only one NMOS is on. Each NMOS must satisfy `(W/L)n >= 2 (W/L)p`. For equal channel lengths, each NMOS width must be at least twice the PMOS width.
   - At the minimum symmetric ratio, `Vo/Vdd` for inputs `00/01/10/11` is `1, 1/5, 1/5, 1/9`. The assignment determines size ratios, rather than unique absolute W and L values.

## Files and reproduction

| File | Purpose |
|---|---|
| `solution.tex`, `solution.pdf` | Standalone derivations, diagrams, assumptions, numerical tables, and reference-answer comparison |
| `q1_constant_leakage.sp` | Capacitor and constant-current abstraction that verifies retention; not the complete MOS circuit in the original figure |
| `q2_constant_resistance.sp` | The assignment's fixed-resistance model for all four input cases |
| `q2_cic018_tt.sp` | Supplementary CIC BSIM3 pseudo-NMOS NOR check at size ratios `1, 2, 3, 4, 6, 8` |
| `reproduce.py` | Runs all three decks and exports actual measurement tables as clean CSV; raw logs stay in a local temporary directory |
| `validate_results.py` | Compares analytical expectations, checks CIC logic levels and symmetry, and verifies supply current against power |
| `*_measurements.csv` | Actual HSPICE measurements: voltages in V, currents in A, times in s, and power in W |
| `analytic_expected.csv` | Independently calculated expectations, explicitly marked `closed_form`; these are not simulation measurements |
| `simulation_status.csv`, `validation_summary.json` | Actual execution status and model conditions for the three decks |
| `validation_checks.csv` | Observations, expectations, and tolerances for 43 checks |

Run in Windows PowerShell:

```powershell
python .\reproduce.py --hspice 'C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com'
python .\validate_results.py
pdflatex -interaction=nonstopmode -halt-on-error solution.tex
pdflatex -interaction=nonstopmode -halt-on-error solution.tex
```

Use `--raw-dir 'another-local-directory'` to select a raw-log directory. A valid HSPICE license service is required. An execution environment with network isolation must allow the simulator to connect to the existing license service.

## Model and actual verification results

All three decks completed with PrimeSim HSPICE **S-2021.09 win64**, exit code **0**, on 2026-10-13. The local process file is `D:/cic018.l` (CIC 0.18 um, BSIM3, version 1.3, 2008-01-21). **The model is not distributed in this public repository** and must be supplied locally. The model include is enclosed by `.protect/.unprotect`. Raw `.lis` files, execution logs, and license information remain local.

- **Retention example:** The illustrative choices are `Vdd = 1.8 V, Vt = 0.45 V, C = 20 fF, IL = 1 pA`; these values are not assignment data. The analytical result is `12.600000 ms`, versus an HSPICE measurement of `12.600025 ms`, a relative error of approximately `0.000198%`. The voltage at 12.6 ms is `0.72000125 V`.
- **Fixed-resistance check:** With illustrative values `Rn = 1 kOhm, Rp = 4 kOhm, Vdd = 1.8 V`, the measured outputs for `00/01/10/11` are `1.8/0.36/0.36/0.20 V`, matching the derivation.
- **CIC check:** TT, 25 C, 1.8 V; `Lp = Ln = 0.18 um, Wp = 0.5 um, Wn = ratio * Wp`. No external output load is added. The `.tran` analysis first obtains a DC operating point and measures settled voltages. This does not verify process-dependent speed or retention.

| Wn/Wp | V00 (V) | V01 = V10 (V) | V11 (V) | P01 (mW) |
|---:|---:|---:|---:|---:|
| 1 | 1.800000 | 0.176482 | 0.078389 | 0.242883 |
| 2 | 1.800000 | 0.078122 | 0.036908 | 0.245440 |
| 3 | 1.800000 | 0.049900 | 0.024040 | 0.246127 |
| 4 | 1.800000 | 0.036566 | 0.017786 | 0.246445 |
| 6 | 1.800000 | 0.023779 | 0.011676 | 0.246746 |
| 8 | 1.800000 | 0.017604 | 0.008684 | 0.246891 |

At ratio 2, the supply current with one NMOS on is `0.1363557 mA`. Ratio 1 also satisfies `VOL <= 0.36 V` for this TT model and bias. However, **BSIM3 does not use fixed on-resistances or enforce equal-size `Rp = 2 Rn`**. These measurements therefore do not change the assignment's analytical minimum ratio of 2. They do not guarantee a minimum size across process corners, voltage, or temperature. See the [UC Berkeley BSIM3v3.2 manual](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1998/ERL-98-51.pdf) for model physics.

All **43/43 numerical checks passed**. CSV files preserve the simulator's reported precision; the tables above are rounded for readability.

## Integration with the existing student answer

The problems were solved independently before reviewing the locally supplied handwritten `VLSI_HW2.pdf`. Its precharge formula, retention formula, NOR identification, `Rp = 4 Rn` boundary, and size ratio of 2 agree with the independent derivation and are retained.

This version adds the initial-readability condition, BL/storage isolation qualification, general size inequalities, and the distinction between fixed resistors and BSIM3 devices. The reference opens part 2(a) with `A=1 AND B=1` as an on-condition. If interpreted as the condition for the entire parallel pull-down network, that is incorrect: either high input enables a path. Its subsequent case analysis does use the correct OR condition. The student's answers or waveforms are not presented as results of the present simulation.
