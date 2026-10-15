# Fall 2018 final

All eight questions are available on printed pages F-1 through F-3; the points total **115**. The Fall 2018 footer establishes the year. Duplicate copies and handwritten notes do not add questions or change the printed premises.

`exam.tex` and `solution.tex` are standalone English documents with editable inline TikZ figures, and their compiled PDFs contain 4 and 12 pages. Student annotations are excluded from reconstruction. The four-page graded booklet was read and compared after independent derivation. Scores do not override independent derivation.

- Q2: explicitly 50% duty, 4 ns/250 MHz; raw-node retention is 1.1 microseconds, not 1.1 ns. The positive AND-output edge explanation is corrected.
- Q3: balanced N100/P200 nm sizes are one valid effective-load RC solution. Literal feedback-gate loading is parameterized because this paper does not specify its ratio to C. Part(b) changes trip parameters; its complete fixed-resistor overlap network is 11R/5 versus the feedback-removed inverter's4R. Real cycle-average power is not determined without waveform/current models.
- Q4: complement PDN is Ab+Db(Bb+Cb). DSL reference-clamp and opposite lower-node load connections follow official course slide32; unspecified bias/noise margins are not invented.
- Q5: Y=ABC·notD+notE+notF·notG. The declared equal-path sizing matches the graded dimensions and gives direct clock loading19C; other valid header allocations are shown.
- Q6: all20 physical MOS are retained (8INV+2TG), including local clock inverters and permanently attached feedback. Falling-edge capture is conditional on write strength.
- Q7: the low-cost slave's feedback remains attached. Forward-settling setup is0.25ns; write inequalities include the TG resistance.
- Q8: original hold fails. Two branch-only inverters repair it under explicit minimum-delay requirements; an optional low-level latch is specified by bounds. The repaired500MHz circuit reaches the printed4/3 target (666.667MHz) with four aligned cut registers and separate hold pairs on both new bypass paths.

Run `python verify_logic_timing.py` from any directory to regenerate all CSV/JSON evidence. It uses only the standard library: exhaustive MOS/Boolean connectivity, ratioed-contention states, analytical retention/sizing and timing. These are not process simulations. Compile either `.tex` with pdfLaTeX; no external figures are needed. `qa.json` records the PDF and evidence checks, and `coverage-entry.json` supplies year/exam coverage.

The DSL primary reference is [Li, Chapter6 lecture, slide32](https://www.ee.ncu.edu.tw/jfli/public_html/VLSI/lecture/ch06.pdf). Exact source and graded-page comparisons are in `sources.json`.
