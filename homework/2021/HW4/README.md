# 2021 HW4

Complete requested pre-layout scope only: part (a), circuit `.sp`, testbench, and actual measurements. Layout/extraction/DRC/LVS/post-layout work is excluded as requested.

`solution.tex` is a standalone pdfLaTeX report with embedded figures/data; `solution.pdf` is the rendered version. `and2.sp` is the six-transistor subcircuit, with F=NAND and Z=AND and explicit supply/bulk terminals. `testbench.sp` runs 00-to-11 and back; `reproduce.py` generates and measures all three bidirectional switching families over three cycles (36 measurements).

Run `python reproduce.py --model D:/cic018.l --work PATH` (optional `--hspice PATH`). The process model is a local prerequisite and is not redistributed. Actual checked measurements are in `results/`. Raw logs remain in the chosen work directory.

TT, 25 C, 1.8 V, 1 fF, input rise/fall 1 ns. Worst delays: F H-L 132.577 ps; F L-H 162.579 ps; Z H-L 193.782 ps; Z L-H 161.193 ps. Both the first-cycle table and three-cycle maxima are reported. All measured truth-table levels pass.

The supplied HW3 sizing is retained and numerically reproduced. Source attribution and comparison are in `../SOURCES.md`.
