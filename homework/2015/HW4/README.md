# 2015 HW4

28T mirror and 38T valid domino full adders; measured slew balancing and exhaustive electrical checks.

- `solution.tex` is standalone English LaTeX; `solution.pdf` is its compiled counterpart.
- Original instructor PDFs are in `../assignments`.
- Source review and corrections are recorded in `../SOURCES.md`.

```text
python reproduce.py --model D:/cic018.l --raw-dir <scratch>
```

Requires licensed HSPICE (default `C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com`) and the local CIC018 library, which is not distributed. Raw output stays in the chosen scratch directory. Pass `--hspice <path>` as needed.
