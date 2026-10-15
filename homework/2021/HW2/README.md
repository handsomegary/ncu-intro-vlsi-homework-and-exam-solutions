# 2021 HW2

All three original design questions are answered in the standalone `solution.tex` and `solution.pdf`.

- Q1: correct transistor-level dual-Vt mapping; NAND E has one delay unit of slack. Keeping the original two-unit circuit delay requires the high-Vt NAND delay to be at most two units. `dual_vt_logic.sp` is a topology with symbolic LVT/HVT model names; a dual-Vt PDK is required to simulate its physical leakage/timing. The supplied CIC018 TT model does not provide those characterized variants. `dual_vt_boolean_testbench.sp` supplies explicit educational Level-1 models so the topology is runnable; its eight verified logic states are labeled illustrative and do not constitute process leakage/timing measurements.
- Q2: 40-transistor active-low one-hot 4-bit rotator, with one transmission gate per selected data path. Invalid control patterns are unspecified by the prompt.
- Q3: pseudo-NMOS NOR, minimum equal-length width ratio WN/WP >= 4.5 in the specified constant-resistance model; supplementary BSIM simulation confirms the chosen widths satisfy the low-voltage condition.

Run `python verify_logic.py` for exhaustive theory checks. Run `python reproduce.py --model D:/cic018.l --work PATH` for real HSPICE (use `--hspice PATH` if needed). All 64 real-CIC018 rotator cases, four real-CIC018 pseudo-NOR cases, and eight illustrative Level-1 Q1 topology cases passed. `results/` contains measured data; raw simulator output stays outside this package. The CIC018 process model is a local prerequisite and is not redistributed.

Reference comparison and attribution: `../SOURCES.md`.
