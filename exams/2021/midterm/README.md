# 2021 midterm

Complete Q1-Q6 span two question pages. The paper does not print a date; 2021 is the attributed year. `exam.tex` reconstructs the questions and figures as editable text/TikZ, and `solution.tex` derives corrected answers.

Q4 uses the lecture-board documented fixed-resistance threshold (0.8 V) and labels its approximation. During the conducting output-discharge phase before the Vin/Vout crossing, N1 is linear while N2 and N3 are saturated. The solution proves this from actual gate/source/drain voltage inequalities and separately gives the earlier onset/off phase. Exact transistor transients are not determined by the supplied resistance model. The printed 15-point Q4 label and its 9+6 subparts are preserved.

Key corrections: Q1(f) asks for leakage mechanisms; Q1(k) asks for W2W/D2W/D2D bonding categories; Q5 is XOR rather than an inverter; Q6(b)'s fixed X=1,Y=0 transition selects two series devices on each edge, giving W/(2L) for both equivalent transistor aspect ratios.

Run `python verify.py` for exhaustive ideal-logic/connectivity and labeled algebra checks. CSV and JSON evidence is included. No circuit simulation results are claimed. All diagrams are standalone editable TikZ; named terminals with the same net label are electrically connected.
