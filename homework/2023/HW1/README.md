# 2023 Homework 1

Complete English solution to the three handwritten circuit-design questions.
The original [assignment PDF](../assignments/homework1.pdf) is preserved separately.

- [solution.tex](solution.tex): standalone LaTeX source, with transistor diagrams.
- [solution.pdf](solution.pdf): compiled and visually checked six-page solution.
- [REFERENCE_COMPARISON.md](REFERENCE_COMPARISON.md): review of all three supplied submissions and integration decisions.
- [check_logic.py](check_logic.py): exhaustive ideal-switch connectivity checker; standard Python only.
- [verification.json](verification.json): machine-readable result summary.
- [circuits.json](circuits.json): physical transistor connectivity and gate signals.
- [truth_tables.csv](truth_tables.csv): all 28 static CMOS logic cases.
- [mux_connectivity.csv](mux_connectivity.csv): all 256 legal data-to-output checks.
- [illegal_controls.csv](illegal_controls.csv): characterization of control combinations omitted by the prompt.
- [sources.json](sources.json): original source filenames and SHA-256 hashes.

```sh
python check_logic.py
pdflatex -interaction=nonstopmode -halt-on-error solution.tex
pdflatex -interaction=nonstopmode -halt-on-error solution.tex
```

The checker passes **284 functional output checks**. It determines outputs by graph
reachability through enabled NMOS/PMOS switches and compares them with independent
printed equations or table mappings. Every static CMOS output reaches exactly one
rail; every legal TG output reaches exactly its specified data input. CMOS input
inverters are checked explicitly. This verifies settled digital connectivity, not
analog timing, power, transistor sizing or voltage margins.

Important interpretation: the original Q1(a) has an overbar over the entire
`w(x+y)+yz` expression. It asks for an AOI gate. Adding an output inverter would
produce the wrong polarity. Question 2 assumes exactly one of `c3,c2,c1,c0` is low,
as in the four provided table rows. Unspecified controls may float outputs or
connect several data inputs; the checker records them without inventing a specification.
