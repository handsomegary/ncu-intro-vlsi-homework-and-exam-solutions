# Fall 2023 final

The complete paper has two question pages. `exam.tex` reconstructs all seven questions and printed connections with editable inline vectors. The original points sum to 115. `solution.tex` gives independent derivations, rather than adopting the mixed-year study compilation as a graded answer key.

Important conditional answers:

- Q2 has no numerical duty cycle: adjustable duty gives 166.667 MHz; 50% duty gives 100 MHz. No matching graded duty evidence was identified.
- Q3's middle clock overbar touches the gate wire in the scan: opposite-phase is the selected transcription, and a same-phase reading is also covered. The primary static-inverter repair works under both. A separately identified same-phase/input-inverter repair has a different output polarity. Node x is internal to the A/B stack. Supplied node caps are treated as totals first, with wire-only alternatives.
- Q5's fixed-external-C classroom sizing is one member of a pMOS family. Including feedback gate loads literally makes the specified 3RC edges infeasible with positive widths.
- Q6 preserves all 14 physical MOS; four are rail-tied off isolation devices.
- Q7 delays R5/R6 clocks, not R7/R8. A low-level lockup latch repairs the direct hold path under explicit latch/minimum-delay bounds. The conditional ideal-latch limit is 476.190 MHz for both skews. The constant R8 function does not remove its original physical STA path; the verifier reproduces a reconvergent pulse that settles at 1.9 ns.

Run `python verify_logic_timing.py` to regenerate all CSV and JSON evidence. Standard library only; these are ideal switch/Boolean and analytical checks, not measured transistor simulations. Compile each standalone `.tex` with pdfLaTeX; no external raster or figure inputs are required. Primary course references and local-source comparison are recorded in `sources.json` and the solution.
