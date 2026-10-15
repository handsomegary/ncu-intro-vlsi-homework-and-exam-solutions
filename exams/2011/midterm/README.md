# NCU Introduction to VLSI — Fall 2011 Midterm

All six questions and 110 printed points are reconstructed from a three-page paper. No matching student answers were identified. Overlapping question views were cross-checked before reconstruction.

The editable exam/solution LaTeX is standalone and every figure is vector TikZ.

Q2 retains the printed power equation and states the threshold convention it requires; the course e≈2 taper is separated from the actual four-stage discrete minimum. Q3 cannot yield a unique leakage optimum without high-VT timing/leakage data, so it supplies the complete transistor circuit and conditional delay constraints. Q4 uses the user-approved VDD-bus junction, clearly marked; ideal threshold levels, body-effect limits, and initial-capacitor assumptions are explicit. Q5 uses the finite uniform RC ladder calculation: one buffer after the third TG gives 29 ns and four internal buffers give 19 ns. The continuum n² approximation is explained as a different model.

Run `python verify.py` for independent connectivity, power, taper, glitch, region, and all 16 buffer-partition checks. Compile `exam.tex` and `solution.tex` twice with pdfLaTeX. PDF rendering and visual QA are recorded in `visual-qa.json`.
