# Introduction to VLSI Design - 2020

Public questions: [HW1 PDF](assignments/homework1.pdf), [HW2 PDF](assignments/homework2.pdf), [HW3 PDF](assignments/homework3.pdf), [HW4 PDF](assignments/homework4.pdf).

Complete assignment question PDFs are public in `assignments/`, with the original page layout and circuit figures preserved. Only the author first name in the footer is removed; surname Li remains.

Complete HW1-HW3 solutions, original assignment PDFs, and HW4 up to the requested pre-layout SPICE stage.

| Homework | Deliverables | Verification |
|---|---|---|
| HW1 | MOS derivation, 4-MUX circuit, transistor schematics | 32 exhaustive Boolean cases |
| HW2 | Dual-Vt schematic and timing bound, 40T rotator, corrected NOR sizing | 8 logical cases, 64 electrical rotator cases, ideal resistor and BSIM checks |
| HW3 | 6T AND netlist, all output-changing transitions, delay report | 18 HSPICE runs, level checks, 1 ps / 0.2 ps convergence |
| HW4 | Identical AND pre-layout `.sp`, testbench, report | Explicit reuse of verified HW3 data; no layout/extracted results |

Each homework has a standalone English `solution.tex` and compiled `solution.pdf`. Read `SOURCES.md` for the supplied-answer review and corrections. Model files remain local at `D:/cic018.l`. Numerical data are actual HSPICE measurements unless explicitly labeled analytical or reused from HW3.

Run each folder's README command with Python 3 and licensed HSPICE. `HW2/reproduce.py --skip-hspice` performs the independent analytical checks only. The multi-Vt timing answer is conditional on a high-Vt NAND delay no greater than two gate units, because the assignment supplies no characterized high-Vt models.
