# 2020 HW4

HW3 circuit packaged as the requested pre-layout .sp-only deliverable.

- `solution.tex` is standalone English LaTeX; `solution.pdf` is its rendered counterpart.
- Original assignment PDFs are in `../assignments`.
- Existing supplied answers were reviewed before the independent derivation; see `../SOURCES.md` and the report comparison.

```text
python simulate.py --model D:/cic018.l --raw-dir <scratch>
```

Requires Python 3 and licensed HSPICE; the authorized CIC018 model is external and is not distributed. Select your paths with `--hspice` and `--model`, or `HSPICE`/`CIC018_MODEL`. Add `--check-environment` to verify paths without simulation. Keep raw simulator output in a scratch directory. See the [fresh-download guide](../../../REPRODUCING.md).
HW4 intentionally stops at schematic SPICE; no layout/extraction is claimed. Its checked-in result data are the identical-circuit HW3 measurements, explicitly recorded in `provenance.json`.
