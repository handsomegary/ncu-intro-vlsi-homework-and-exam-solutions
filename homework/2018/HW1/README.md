# 2018 HW1

Complete [LaTeX](solution.tex) and [PDF](solution.pdf), with all required MOS
diagrams, dual-Vt assignment, four-MUX construction and complementary CMOS
networks. The original full overbar in Q4(a) is retained.

```sh
python verify_logic.py
```

40 Boolean cases and 5050 ideal square-law stack points pass. `truth_tables.csv`
and `verification.json` record this ideal-model evidence. No analog timing
or physical dual-Vt leakage is asserted without the corresponding PDK.
The supplied three-page answer was read and compared first; see the report
and [year source review](../SOURCES.md).
