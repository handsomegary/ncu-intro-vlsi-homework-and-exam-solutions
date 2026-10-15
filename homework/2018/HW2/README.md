# HW2 — Four complete answers and numerical verification

[LaTeX source](solution.tex) and [PDF](solution.pdf) cover input slew, unloaded
NOR fanin, mobility ratio and gate capacitance at node x. Original prompts
and source fingerprints are linked from the year README.

```sh
python reproduce.py --analytical-only
python reproduce.py --work /path/to/local/raw
```

Override `--model` and `--hspice` as required. Default process model is the user's
local `D:/cic018.l`, not redistributed. Standard-library Python only.
`q1_slew.sp` is an explicitly illustrative CIC018 TT inverter example;
`q2_pi_rc.sp` implements the separately stated ideal pi-RC model. Two real
HSPICE decks completed. All eight fanin first-moment checks passed, and the
100 ps input rise produces a shorter output fall than the 1 ns input rise.

The fixed-size RC ladder has rise first moment 2n²RpCd. The isolated-chain
single-on-NMOS fall has time constant (n+1)RnCd. `rc_checks.csv` distinguishes
first moments from 10–90% crossing times. `rc_expected.csv`, `mobility_examples.csv`
and `gate_capacitance.csv` are analytical checks; `_measurements.csv` files
are actual simulator exports. `validation.json` summarizes the checked conditions.
