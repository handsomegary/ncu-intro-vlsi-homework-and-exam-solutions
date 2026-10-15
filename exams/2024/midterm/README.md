# 2024 Midterm - reconstructed paper and corrected answers

The two-page question set and four matching handwritten-answer pages were reviewed before independent derivation.

- [Reconstructed paper PDF](exam.pdf) and [standalone LaTeX](exam.tex): all seven questions, original 100-point total, equations, and four figures redrawn as editable TikZ. No scan image is embedded.
- [Corrected worked-answer PDF](solution.pdf) and [standalone LaTeX](solution.tex): six pages covering every part, with source comparison and explicit ideal-model assumptions.

The supplied graded answer is the starting reference. Q2's sixteen MUX constants and Q7's three CMOS graphs are retained after independent verification. Q3's 20Cg NAND-input convention needs an additional nMOS-width assumption; the general expression and alternate balanced sizing are provided. Q4's endpoints and Q5's masked-input case are qualified. In Q6 the minimum final inverter has 3Cg input capacitance under the per-transistor definition, making the student's worst delay 10RCg. Doubling both NAND nMOS widths gives 7RCg in both directions, strictly below 8RCg.

```sh
python verify_q2_q7.py
python verify_q3_q6.py
pdflatex exam.tex
pdflatex exam.tex
pdflatex solution.tex
pdflatex solution.tex
```

Python uses the standard library. No local process model or HSPICE run is required: the exam specifies analytical ideal models. Saved CSV/JSON evidence covers 16 MUX cases, 32 CMOS connectivity cases, 40 buffer comparisons, 15 device-region samples, four functional noise scenarios and the student/corrected AND dimensions. Reproduction of the student design's failed bound is intentional evidence, not a failed package check.

See [SOURCES.md](SOURCES.md), [sources.json](sources.json) and [pdf_qa.json](pdf_qa.json).
