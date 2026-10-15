# 2024 HW1: Static CMOS and Data Selection

Complete solutions to HW1 in EE3032 Introduction to VLSI Design (Li, Fall 2024). This is a written derivation assignment. The LaTeX solution includes transistor diagrams, truth tables, and reproducible ideal-switch connectivity checks.

## Assignment requirements and solution overview

| Problem | Requirement | Selected implementation |
| --- | --- | --- |
| 1(a) | Implement `f = NOT(x + y + wyz)` in static CMOS using only true input literals; show the transistor diagram. | Absorption gives `y + wyz = y`, so `f = NOT(x+y)`. Two series pMOS and two parallel nMOS form a 4T NOR. Inputs `w,z` do not affect the output. |
| 1(b) | Implement `f = x'y' + x'z' + y'z'` in static CMOS using only true input literals. | Factor as `f = NOT[xy + z(x+y)]`. The dual PDN/PUN each use 5T, for 10T total, without input inverters. |
| 2 | Use four data inputs, four controls, and four outputs to implement the four cyclic selections in the assignment table. | Sixteen CMOS transmission gates and four shared control inverters use 40T total. The diagrams specify every data connection and both control polarities. The assigned controls are one-hot. |
| 3(a) | Determine the logic function of the given pass-transistor circuit. | `F = AB + A'B'`, the XNOR function. |
| 3(b) | Implement the same function in CMOS. | Primary answer: an 8T static CMOS core, or 12T including two input inverters. An optional TG implementation uses 8T including its input inverters. |

Here `'` means NOT, `+` means OR, and juxtaposition means AND. In Problem 1(a), the original PDF's overbar covers the entire expression `x + y + wyz`.

Problem 2 uses the following output ordering:

| Active control | `(z3,z2,z1,z0)` |
| --- | --- |
| `c3=1` | `(a3,a2,a1,a0)` |
| `c2=1` | `(a2,a1,a0,a3)` |
| `c1=1` | `(a1,a0,a3,a2)` |
| `c0=1` | `(a0,a3,a2,a1)` |

All other controls are zero. The assignment does not specify non-one-hot operation. With no active control, the TG selector leaves the outputs floating; with multiple active controls, different data sources may be connected together. The solution also describes a complete static CMOS AND-OR implementation if defined behavior for every control word is required.

## Files

| File | Purpose |
| --- | --- |
| [solutions.tex](solutions.tex) | Standalone English LaTeX solution with embedded TikZ transistor diagrams; no external figures are needed. |
| [solutions.pdf](solutions.pdf) | Compiled reading copy. |
| [verify_logic.py](verify_logic.py) | Python standard-library checker that builds conducting graphs from the actual MOS terminal lists in the diagrams. |
| [truth_tables.csv](truth_tables.csv) | All 96 main-circuit input cases, with expected outputs, observed outputs, and PASS status. |
| [verification.json](verification.json) | Test counts, device counts, and the LaTeX source SHA-256. |

The unchanged instructor assignment is [2024/assignments/homework1.pdf](../assignments/homework1.pdf). Two pre-existing handwritten references were supplied locally by the user. Their provenance and comparison are acknowledged in the solution and the repository's source inventory. Their content is not presented as newly authored work.

## Verification and results

Run in this directory:

```powershell
python .\verify_logic.py
```

Result: **PASS, 100 cases**.

| Check | Cases |
| --- | ---: |
| 1(a): all `w,x,y,z`; original/simplified expression equivalence, complementary PUN/PDN operation, and no floating output or rail short | 16 |
| 1(b): all `x,y,z`; SOP/POS/factored equivalence and 10T conducting graphs | 8 |
| 2: four one-hot choices times all 16 data words; complete expanded-MOS data connectivity | 64 |
| 3: all `A,B` for the static CMOS implementation | 4 |
| 3: all `A,B` for the TG implementation | 4 |
| Shared inverter at both input levels | 2 |
| Unspecified-control examples in Problem 2: zero selection and multiple selection | 2 |

These are ideal binary MOS-switch checks, not HSPICE simulations. They do not establish process behavior, transistor sizing, delay, analog voltage swing, or switching-transient performance. HW1 does not request those simulations. The solution explains body connections and the original nMOS-only circuit's possible high-level threshold loss.

## Reference review and selection rationale

All pages of the one-page original assignment and both references were reviewed:

- **Reference A:** a user-supplied four-page HW1 correction/reference, including a cover.
- **Reference B:** a three-page student HW1 solution.

The original local-file provenance is recorded in the repository's source inventory.

- **1(a):** Both references retain a redundant branch in their 10T networks. The selected 4T NOR uses only true input literals. Reference A labels the redundant branch with `z'`, which does not satisfy the true-literal restriction; absorption means that this branch does not change the output logic.
- **1(b):** Both reference 12T minority networks are valid. Independent factoring gives the selected 10T implementation; all truth values and supply connectivity are checked.
- **2:** The reference cyclic data wiring is valid. The TG architecture is retained, with explicit shared complementary controls, the 40T device count, and the one-hot assumption.
- **3:** Both references correctly identify XNOR. Enlarging Reference A reveals its complementary control bars; its upper MOS-type symbol is unclear. That ambiguity does not establish same-polarity control or an incorrect connection. The TG alternative is redrawn with explicit nMOS/pMOS gate labels. Reference B's static CMOS network is valid and agrees with the independent derivation.

## Compile

```powershell
pdflatex -interaction=nonstopmode -halt-on-error .\solutions.tex
```

The source uses pdfLaTeX, Latin Modern fonts, TikZ, and standard mathematical typesetting packages. It requires no CJK package or system-specific font. The final source was checked with the built-in LaTeX compiler, exported to PDF locally, and reviewed visually on every page.
