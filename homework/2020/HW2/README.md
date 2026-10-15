# 2020 HW2

Dual-Vt allocation, 40T one-hot rotator, and ratioed NOR sizing.

- `solution.tex` is standalone English LaTeX; `solution.pdf` is its rendered counterpart.
- Original assignment PDFs are in `../assignments`.
- Existing supplied answers were reviewed before the independent derivation; see `../SOURCES.md` and the report comparison.

```text
python reproduce.py --model D:/cic018.l --raw-dir <scratch>
```

Requires Python 3 and licensed HSPICE (default `C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com`); the CIC018 model is local and is not distributed. Keep raw simulator output in a scratch directory. Pass `--hspice <path>` to override the executable.
