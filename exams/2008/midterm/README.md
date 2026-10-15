# Spring 2008 midterm

Complete EE332 Introduction to VLSI midterm: Q1-Q5, intended 100 points. Q5 literally prints **10%**; this mark is preserved, with the ten-point interpretation recorded separately.

The paper has two printed pages and five questions, with a Spring 2008 footer. Printed content governs the editable `exam.tex`; handwritten study annotations are excluded from reconstruction.

`solution.tex` independently solves all questions, then compares the matching graded booklet and the ungraded duplicate study sheets. The upper Q2 output is **constant 1** because the original output gate is OR. The original physical circuit is retained. Actual fanout is included, and physical timing arc sums are distinguished from sensitizable output edges. General resistance-ratio timing and conditional high-threshold slack are explicit. Q3 retains the printed overhead definition of eta and corrects the continuous result to an implementable integer chain. Q4 includes both delay-equality width roots and selects the lower-power root. Q5 supplies the requested complete 28-MOS forward adder.

Both TeX documents are standalone, with inline editable TikZ and no external figures. Compile with `pdflatex exam.tex` and `pdflatex solution.tex`. The saved PDFs were compiled with the built-in compiler and two local MiKTeX passes; all 12 original/reconstructed/solution pages were rendered and visually inspected.

Run `python verify_logic_timing.py` to reproduce `logic_timing_verification.json` and the 14 CSV files (175 data rows). It uses only the Python standard library and checks rail exclusivity and Boolean outputs for 32 Q1, 32 Q2 and eight full-adder cases, fanout-aware RC timing, conditional threshold slack, seven integer/even-stage taper cases and both sizing roots. These are declared ideal/analytical models, not transistor measurements.

`sources.json` records local hashes, authentic extraction checks, reference page order, duplicate references and the course lecture used for qualitative context. `coverage-entry.json` records coverage and the printed-mark interpretation. `qa.json` records compile, visual and verification evidence. No original question is missing.
