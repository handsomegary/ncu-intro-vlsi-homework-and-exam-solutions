# 2013 HW1

[Original prompt](../assignments/homework1.pdf), [standalone LaTeX](solution.tex),
and [compiled solution](solution.pdf).

All four original questions are answered. The series-MOS proof covers both
linear and saturated regions and unequal channel lengths. Q3 uses exactly one
4:1 multiplexer. Q4(a) retains both overbars in the printed formula:
`NOT(w*NOT(x+y)+y*z)`; a four-transistor NOR followed by AOI22 uses 12 MOSFETs.
The minority gate in Q4(b) uses 10 MOSFETs and true external inputs only.

Run `python verify.py`. All 32 Boolean/switch cases and 80,800 square-law current
points pass. Evidence: [truth_tables.csv](truth_tables.csv),
[verification.json](verification.json). The checks are ideal logic/model
calculations, not SPICE timing claims.

The supplied `MOS prove.pdf` supports the conducting-region contradiction and
linear length-addition proof; this solution extends the proof to saturation.
No complete local HW1 submitted answer accompanies the original prompt.
