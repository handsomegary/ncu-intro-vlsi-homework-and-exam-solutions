# 2023 midterm: available latter questions

The original archive supplies only printed page 2-2. Complete Q5–Q7 are reconstructed and solved (35 points); the visible Q4 continuation and Figure 3 are preserved, but the missing premise is not inferred. Q1–Q3 are omitted. The extracted original question photograph retains its original image bytes; local student answer pages are reviewed but not redistributed.

- `exam.tex` / `exam.pdf`: editable reconstruction of the surviving source questions and Q4 fragment.
- `solution.tex` / `solution.pdf`: independent solutions, corrected sizing/networks, and comparison with both supplied student sets.
- `sources.json`: exact source/coverage/image-byte provenance.
- `verify.py`, CSV files and `verification.json`: analytical checks; run `python verify.py`.

Compile either standalone TeX document with `pdflatex -interaction=nonstopmode -halt-on-error exam.tex` (or `solution.tex`). Each includes its TikZ source and needs no external images or proprietary process model. Q5 qualitative margins state their matched-threshold VTC assumption; masked single-input scenarios are distinguished. No numerical margins or simulation evidence is invented.
