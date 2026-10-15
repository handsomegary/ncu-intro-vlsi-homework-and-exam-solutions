# 2013 HW3

[Original prompt](../assignments/homework3.pdf), [standalone LaTeX](solution.tex),
and [compiled solution](solution.pdf).

Both printed questions are completed using the user's local CIC018 model and
actual HSPICE. Each transmission gate keeps the required NMOS 10 um, PMOS
20 um and length 0.18 um. Both multiplexer topologies use the required **10 fF**
output load and identical 20 ps data edges. The 54-MOS baseline's measured maximum
delay is **220.507 ps**; the 34-MOS binary tree's maximum is **76.191 ps**, a
**65.447%** reduction over the declared data-edge tests.

The inverter uses explicitly selected WP=20 um/WN=10 um, 3 ns input rise/fall
and a declared 20 ns period. `Psc` is the complete-cycle positive intrinsic
channel-current overlap estimator using HSPICE `LX4`, averaged from 23 to 43 ns.
Supply power and external-load switching power are separate columns. All five
specified 0.1-1 pF loads are measured. Total transistor dissipation, terminal
displacement currents and edge-window averages are not substituted for `Psc`.

```sh
python reproduce.py --model D:/cic018.l --work PATH
# Optional: --hspice PATH
```

`--prepare-only` regenerates decks and the 2048-case ideal truth table without
claiming a physical simulation. Actual results are in [results](results):
16 paired electrical transitions/32 measured delays and five power-load cases.
The data-edge delay scope excludes switching-select hazards and PVT extremes.
Raw simulator/license files remain outside the repository; the process model
is never redistributed.

The supplied DOCX answer's useful binary-tree idea is retained. Its baseline
uses 1 fF rather than 10 fF, its improved experiment changes input slew and
omits the load, and its inverter ALTER capacitors target `vout` instead of the
actual `out` node. Those results are therefore not imported as validated numbers.
