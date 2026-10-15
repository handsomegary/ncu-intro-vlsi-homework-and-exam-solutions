# 2023 HW2

[solution.tex](solution.tex) and [solution.pdf](solution.pdf) cover all three
questions, with a complete dual-Vt CMOS drawing and source comparison.

The literal **smallest** logic-zero voltage yields symmetric n/p aspect ratio
2.25; the conventional **maximum acceptable** low yields 4.5. These are different
requirements. Retention is `C*(VDD/2-Vt)/IL`; the storage/BL read qualification
is explicitly included.

```sh
python reproduce.py --logic-only
python reproduce.py --work /path/to/local/raw
```

Override `--model` and `--hspice` if needed. `logic.csv` and `sizing.csv` contain
analytical checks. The three `_measurements.csv` files are actual HSPICE outputs.
`q2_retention.sp` and `q3_resistance.sp` implement the stipulated ideal models;
`q3_cic018.sp` is a distinct BSIM3 example. All three runs pass. Dual-Vt timing
is a symbolic gate/slack condition because the supplied TT library has no
separate dual-threshold model pair.
