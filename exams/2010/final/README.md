# 2010 final

All three Fall 2010 question pages are reconstructed. [Reconstructed paper](exam.pdf) / [standalone TeX](exam.tex); [corrected solutions](solution.pdf) / [standalone TeX](solution.tex). All 130 printed points are retained.

Q2's positive-edge register and Q7's negative-edge, 16-MOS layout are different original circuits. Q4's fixed P1 and strict clock-power target are incompatible, as shown algebraically. Q5 preserves the 2010 values (Cz = 2 pF and PMOS threshold magnitude = 0.6 V); its legal sharing-only states pass the stated ideal voltage test. Q6 states signed skew and minimum-delay assumptions explicitly. Q8 uses square-law current balance to derive a beta ratio of 1; a graded resistor shortcut cannot establish that ratio.

`python verify.py` reproduces the ideal graph and analytical checks. Two pdfLaTeX passes compile each standalone source. No HSPICE measurement is asserted. See the sources and QA JSON.
