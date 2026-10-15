# 2012 archive midterm

All seven questions are available; the printed points total **100** across three printed pages. `exam.tex` reconstructs three editable pages; `solution.tex` gives ten pages of independent derivations, inline TikZ and explicit model conditions. Both compile independently with pdfLaTeX, without external figure inputs.

**Year attribution:** no printed year is visible in the question views. The paper is attributed to 2012. Duplicated student-answer pages do not independently establish the year. Matching functions, edges and numeric premises establish relevance; the grade does not establish correctness.

- Q1: correct CMP/density/antenna reasoning, noise-margin definitions, and general mobility/threshold sizing; no unprovided2x width assumption.
- Q2: full output-connected capacitance graph yields worst Elmore first moments Rp(3C+2Cout), Rn(3C+2Cout), attained by010↔110 in the declared constant-R/full-level step model. The graded C+2Cout formula omits attached opposite-network capacitors. First moment is distinguished from a one-pole10–90estimate. Internal power uses supply×swing with a declared charging-activity convention.
- Q3:24MOS preserved. Conditional12L/12H candidate includes two high-threshold short-path parallel nMOS branches; explicit slack conditions govern eligibility. Missing high-Vt delay/leak characterization prevents an unconditional globally optimal allocation. The graded14L/10H is a conservative reference assumption.
- Q4: Ymax1.0V/Zmax1.4V with constantVt0.4; the upper helper degrades the second transistor's gate. The six bottom gates remain atVDD. m1 can be linear/saturation; m2–m6 are linear while conducting, with boundary/cutoff limits.
- Q5: exact8RC gives alpha1 or3; alpha1 halves modeled first-two-node switching power relative to3.
- Q6: source variable isw, confirmed from native crop. Q6a has8MOS. Conventional complementary XOR has12 including input inverters; a separately labeled static TG interpretation has8. The student's10MOS XOR instead outputs constant0.
- Q7: true-input28MOS static full adder, complete intermediate carry and both output inverters. Student truth/SOPs agree; complement-literal carry polarity can be correct, but complement generators are omitted in the supplied diagram.

Run `python verify_logic_timing.py` from any directory to regenerate CSV/JSON evidence. Standard library only: exhaustive rail/switch graphs, exact resistor-matrix first moments, conditional slack checks, pass-region inequalities, sizing and arithmetic truth tables. These are analytical ideal-model checks, not measured process simulations. `qa.json` records evidence/page review and `coverage-entry.json` records coverage and six original PDF pages.

Primary concept references are [Li, Chapter3 fabrication lecture](https://www.ee.ncu.edu.tw/jfli/public_html/VLSI/lecture/ch03.pdf), [Berkeley double-gate FinFET lecture](https://www2.eecs.berkeley.edu/Colloquium/Archives/11-12/Fall2011/kingliu-presentation.pdf), and [Intel's2011Tri-Gate announcement](https://www.intc.com/news-events/press-releases/detail/655/intel-reinvents-transistors-using-new-3-d-structure). Source access limitations are recorded honestly in `sources.json`.
