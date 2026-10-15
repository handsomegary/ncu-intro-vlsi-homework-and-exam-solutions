# 2020 HW3

Six-transistor AND gate, six transitions, measured delays and timestep convergence.

- `solution.tex` is standalone English LaTeX; `solution.pdf` is its rendered counterpart.
- Original assignment PDFs are in `../assignments`.
- Existing supplied answers were reviewed before the independent derivation; see `../SOURCES.md` and the report comparison.

```text
python simulate.py --model D:/cic018.l --raw-dir <scratch>
```

Requires Python 3 and licensed HSPICE (default `C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com`); the CIC018 model is local and is not distributed. Keep raw simulator output in a scratch directory. Pass `--hspice <path>` to override the executable.
