# 2021 Introduction to VLSI Design solutions

Public questions: [HW1 PDF](assignments/homework1.pdf), [HW2 PDF](assignments/homework2.pdf), [HW3 PDF](assignments/homework3.pdf), [HW4 PDF](assignments/homework4.pdf).

Complete assignment question PDFs are public in `assignments/`, with the original page layout and circuit figures preserved. Only the author first name in the footer is removed; surname Li remains.

Each homework has an English standalone `solution.tex`, its rendered PDF, runnable verification, and a README. Complete original-format prompts are public in `assignments/`, with the author first name removed.

| Homework | Scope | Verification |
| --- | --- | --- |
| HW1 | All MOS theory, mux design, and CMOS diagrams | 32 Boolean cases and 5,050 ideal square-law operating points |
| HW2 | All three theory/design questions plus code/netlists | 64 real-CIC018 rotator cases, 4 real-CIC018 pseudo-NOR cases; 8 illustrative Level-1 Q1 cases |
| HW3 | Complete AND-gate pre-layout simulation and both-node delay measurements | 3 switching families, 3 cycles, 36 actual HSPICE delays, rail checks |
| HW4 | Requested pre-layout `.sp` and measurements; layout excluded | Independent repeat of all HW3 switching measurements |

For HW1: `cd HW1` and run `python verify_logic.py`. For HW2: run both `python verify_logic.py` and `python reproduce.py`. For HW3/HW4: run `python reproduce.py`. All simulation drivers accept `--hspice`, `--model`, and `--work`. The defaults use the user's local installed HSPICE and `D:/cic018.l`. Supply a writable raw-output directory with `--work` to retain listings. No process model is redistributed.

CIC018 TT does not provide characterized low/high-threshold variants. Therefore Q1's dual-Vt placement is answered using the prompt's delay/slack assumptions; an explicitly educational Level-1 deck checks its topology only. Physical dual-Vt leakage and timing are not fabricated.

The supplied answers were read and compared first; independently verified improvements were integrated with attribution. See `SOURCES.md` for every source, hashes, and the comparison decisions.
