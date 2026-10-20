# Introduction to VLSI Design - 2024

Public questions: [HW1 PDF](assignments/homework1.pdf), [HW2 PDF](assignments/homework2.pdf), [HW3 PDF](assignments/homework3.pdf), [HW4 PDF](assignments/homework4.pdf).

Complete assignment question PDFs are public in `assignments/`, with the original page layout and circuit figures preserved. Only the author first name in the footer is removed; surname Li remains.

National Central University, EE3032 Introduction to VLSI Design, Li, Fall 2024.

This year covers **2024 HW1–HW4**. The four complete assignment question PDFs are public in [assignments](assignments/README.md), with the author first name removed. All solution reports and repository explanations are in **English**, with compilable LaTeX, transistor-level HSPICE netlists, and reproducible numerical verification.

| Assignment | Deliverables |
| --- | --- |
| [HW1](HW1/) | CMOS derivations, transistor diagrams, truth tables, and switch-connectivity verification |
| [HW2](HW2/) | Complete analytical answers plus ideal-model and CIC018 HSPICE checks |
| [HW3](HW3/) | Four-bit XNOR/multiplexer-based adder, prescribed 9 ns stimulus, area/energy statistics, and exhaustive input checks |
| [HW4](HW4/) | Verified HW3 netlist and pre-layout testbench; layout, DRC, LVS, PEX, and post-layout results are outside the requested scope |

Each homework README explains the requirements, design choices, file purposes, reproduction commands, and validation results.

## Local requirements

- PrimeSim HSPICE S-2021.09. The executable used here was `C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com`.
- Your external authorized CIC018 model, selected with `--model` or `CIC018_MODEL`: TT, 1.8 V, 25 C. The model is read locally and is not redistributed. Use `--check-environment` to check your installation paths first; see the [fresh-download guide](../../REPRODUCING.md).
- Python 3; see each homework folder for reproduction instructions.
- Each English `.tex` report is standalone and compiles with PDFLaTeX; a PDF preview is included. Diagrams and statistics come from source or simulation data, without hspui screenshots.

## Sources and comparison

Existing supplied answers were reviewed, then checked against independent derivations, truth tables, and simulations. Adoption and correction decisions appear in the reports and [SOURCES.md](../SOURCES.md). Previous students' layouts and PEX are not presented as results of this design.

Instructor clarifications are provided in English as public Markdown translations, linked from the assignment [README](assignments/README.md).

## Verification results

| Assignment | Completed checks and measurements |
| --- | --- |
| HW1 | 100 ideal MOS switch/logic checks passed; 96 truth-table rows. These are not process-model simulations. |
| HW2 | Three HSPICE decks completed; 43/43 numerical checks passed. Retention example: 12.6 ms analytical, 12.600025 ms measured. |
| HW3 | 512/512 transistor-level transient cases passed. Six candidates were compared; the selected 64T design has `sum(WL)=5.4144 um²`. |
| HW4 | The identical HW3 netlist was rerun independently; all 8 prescribed vectors passed. Pre-layout only. |

Refined HW3/HW4 settings (TT, 1.8 V, 25 C, no added output load, maximum timestep 1 ps): total power **69.558498 uW**, total energy over 9 ns **626.026482 fJ**. The maximum measured 50% delay within the prescribed sequence is **152.910320 ps**, not a global worst case across all transitions or PVT conditions. The original instructor `.tran 0.1ns 9n` result is reported separately: **69.002216 uW, 621.019943 fJ**. The two timestep settings are not mixed.

The 64T version has the lowest energy, area, and PDP among the six evaluated candidates. PDP is delay times power; full-sequence energy is power times 9 ns. See [HW3](HW3/README.md) for the comparison and selection rationale.

## Reports

| Assignment | LaTeX source | PDF preview |
| --- | --- | --- |
| HW1 | [solutions.tex](HW1/solutions.tex) | [solutions.pdf](HW1/solutions.pdf) |
| HW2 | [solution.tex](HW2/solution.tex) | [solution.pdf](HW2/solution.pdf) |
| HW3 | [solution.tex](HW3/solution.tex) | [solution.pdf](HW3/solution.pdf) |
| HW4 | [solution.tex](HW4/solution.tex) | [solution.pdf](HW4/solution.pdf) |

All four reports have been compiled and their rendered pages inspected.

## Reproduction and package checks

Each homework README provides HSPICE commands and model-path overrides. To check downloaded artifacts, saved measurements, source hashes, and links without rerunning HSPICE, run from the repository root:

```powershell
python verify_package.py
```

This reads saved simulation data; it does not claim to run a new simulation. The root `MANIFEST.json` records the external model fingerprint and public artifact SHA256 hashes. Text line endings are canonicalized to LF to avoid Windows/Git conversion mismatches. Raw simulator and compiler outputs remain in the local workspace; the public repository contains compact results.
