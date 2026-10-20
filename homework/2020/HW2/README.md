# 2020 HW2

Dual-Vt allocation, 40T one-hot rotator, and ratioed NOR sizing.

- `solution.tex` is standalone English LaTeX; `solution.pdf` is its rendered counterpart.
- Original assignment PDFs are in `../assignments`.
- Existing supplied answers were reviewed before the independent derivation; see `../SOURCES.md` and the report comparison.

```text
python reproduce.py --model D:/cic018.l --raw-dir <scratch>
```

Requires Python 3 and licensed HSPICE; the authorized CIC018 model is external and is not distributed. Select your paths with `--hspice` and `--model`, or `HSPICE`/`CIC018_MODEL`. Add `--check-environment` to verify paths without simulation. Keep raw simulator output in a scratch directory. See the [fresh-download guide](../../../REPRODUCING.md).
