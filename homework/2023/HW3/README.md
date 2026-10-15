# 2023 HW3 — Three-bit static CMOS ripple-carry adder

Complete [LaTeX report](solution.tex), [PDF](solution.pdf), circuit [rca.sp](rca.sp)
and reproducible real HSPICE measurements are included.

The reconstructed compact full adder uses 28 transistors, so the RCA has 84.
Body terminals are tied to the rails and all four external outputs have 1 fF.
Conditions: CIC018 TT, 1.8 V, 25 C, 20 ps input slew, maximum step 2 ps.
The figure's three full adders determine the design despite the sentence's typo.

All 128 arithmetic states and 896 directed single-input transitions pass.
The 1,552 changing-output delays are recorded; the largest is
**833.526988 ps**, x0 falling while x goes 7→6,
y=0 and cin=1, causing s2 to rise. This characterizes all settled single-input
transitions at the stated conditions, not all simultaneous changes or PVT.

VDD-only average supply power is **177.082000 uW**
over the explicitly defined 128-vector, 384 ns binary-count workload;
energy is **67999.487960 fJ**. Ideal input-driver power is excluded.
The count/width-length proxy is 84T / 53.46 um², not layout area.

```sh
python reproduce.py --work /path/to/local/raw --results results
```

`--hspice` and `--model` override executable/model paths. Python standard
library only. `characterize.sp` contains the DC-reinitialized data sweep;
`testbench.sp` contains the power workload. Failed crossing measurements for
unchanged outputs are expected and excluded; every required changed output
must have a finite delay and valid before/after voltage bands.

See the report and [source review](../SOURCES.md) for comparison with the
three supplied answers. Saved CSVs are measured data, not synthesized values.

For a license-free independent topology proof, run `python verify_logic.py`.
It parses the actual MOS connections, checks rail exclusivity for all eight
full-adder states and all 128 RCA sums, and computes the transistor count and
width-length sum. This ideal switch proof is distinct from analog simulation.

Run `python refine_worst.py --work /path/to/local/raw` to regenerate the 1 ps
critical-case refinement. Standard Python regenerates CSV/JSON; optional
Matplotlib regenerates [the waveform PNG](results/worst_transition.png).
The refined delay is 833.905310 ps, 0.0454% above the complete 2 ps sweep result.
