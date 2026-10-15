# 2009 midterm

All six Fall 2009 questions, 105 printed points. [editable exam](exam.tex) / [PDF](exam.pdf), [corrected solutions](solution.tex) / [PDF](solution.pdf).

The original graph controls Q4's OR/NOR/NAND/OR/AND polarities and actual fanouts. Peak power is qualified as a settled interval estimate; missing current/transition information prevents a literal instantaneous peak or unconditional glitch claim. Dual-threshold examples explicitly require delay penalties fitting slack; minimum leakage is not provable from unspecified device data. Q6 retains all ten MOS and shared gate controls, all four node capacitances, and reachable dangling loads in its RC first moments.

Run `python verify.py` for standard-library ideal-graph, event and nodal RC checks. Compile each standalone TeX twice with pdfLaTeX. No measured process result is asserted.
