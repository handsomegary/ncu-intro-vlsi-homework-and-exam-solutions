# 2023 HW4 — Pre-layout SPICE only

[rca.sp](rca.sp) is the same verified netlist as HW3. The [report](solution.tex)
([PDF](solution.pdf)) explains the user's narrower scope and distinguishes the
HW3 delay characterization from the independent HW4 functional/power rerun.

```sh
python reproduce.py --work /path/to/local/raw
```

All 128 states pass an independent actual HSPICE run with the same 1 fF loads.
`vectors.csv` and `validation.json` record the evidence. The script checks the
HW3/HW4 normalized netlist hashes. No layout, DRC, LVS, PEX or post-layout
result is included. The original assignment remains unchanged separately.
