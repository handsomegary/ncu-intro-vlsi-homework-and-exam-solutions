# 2015 HW3

Equal-size 6T AND delays and a settled full-cycle short-circuit overlap-power load sweep.

- `solution.tex` is standalone English LaTeX; `solution.pdf` is its compiled counterpart.
- Original instructor PDFs are in `../assignments`.
- Source review and corrections are recorded in `../SOURCES.md`.

```text
python reproduce.py --model D:/cic018.l --raw-dir <scratch>
```

Requires licensed HSPICE and an authorized CIC018 library, which is not distributed. Select your paths with `--hspice` and `--model`, or `HSPICE`/`CIC018_MODEL`. Add `--check-environment` to verify paths without simulation. Raw output stays in the chosen scratch directory. See the [fresh-download guide](../../../REPRODUCING.md).
