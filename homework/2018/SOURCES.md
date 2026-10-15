# Source review and integration decisions

Original prompt PDFs define the task. The published reports and scripts are
independently authored, with new recorded HSPICE runs and explicit assumptions.

The three-page handwritten `HW1.pdf` and two-page `HW2_SOL.pdf` were fully
read visually before solving. HW1 retains the valid series-inverter theory,
Shannon cofactors and CMOS dual networks; adds a complete complement-generating
MUX and a qualified high-Vt timing assignment. The Q4(a) full overbar is
verified directly against the printed prompt. Logic checks cover 40 cases and
5050 square-law stack points, with no false physical dual-Vt claim.

HW2 retains the reference's qualitative slew effect, matched-threshold
mobility ratio 2 and conventional 8/3 node capacitance. The fixed-size NOR RC
coefficient is independently derived with every diffusion capacitor counted;
first moment, exact one-pole fall time and distributed 10–90 rise time are
distinct. The input switching pattern and gate-strength definition are stated.
The reference coefficient mixes width-scaled and unscaled terms, so it is not
copied as the fixed-size model answer. All new analog results are actual runs.

Student-only HW3 material was inspected during inventory but is skipped because
there is no original prompt, following the user's explicit instruction.
