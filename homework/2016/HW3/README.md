# 2016 HW3

Both original questions are completed in standalone `solution.tex` and rendered `solution.pdf`.

- Q1 uses equal W=0.6um/L=0.18 um for all six transistors,1.8 V,100 ps input edges,and a declared1 fF Z load. All36 actual delay measurements and six voltage checks pass. F is NAND; Z is AND. Correct VSS/VDD bulk ties are explicit.
- Q2 sweeps0.1,0.3,0.5,0.7,1 pF with 3 ns input ramps,T86 ns. Psc is integrated over a steady full period using positive intrinsic channel IDS probes `LX4`, not peak power or edge-window averages. Corrected Psc is0.786014,0.442160,0.313114,0.243484,0.183094 uW, respectively.

Run `python reproduce.py --model D:/cic018.l --work PATH`, optionally `--hspice PATH`. The separate drivers are `simulate_and.py` and `simulate_power.py`. `results/` contains actual measurements; the process model is a local prerequisite and is not redistributed. Source attribution and specific reference corrections are in `../SOURCES.md`.
