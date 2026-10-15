# 2012 final

Complete Q1-Q8 have a printed total of 140 points across three Fall 2012 question pages. `exam.tex` and its PDF reconstruct every readable question and editable vector figure; `solution.tex` and its PDF independently solve them and compare two handwritten answer sets anonymously.

Run `python verify.py` with Python3 to regenerate saved analytical CSV/JSON checks. No process model or SPICE result is claimed.

Material qualifications: Q4(b) is infeasible with fixed P1; Q5 follows the printed per-gate mean-delay convention, checks shared-control reachability, and adds no unstated output loads; Q6 frequency ceilings require the documented short-path hold repair and unsigned-skew bounds; Q7 retains every physical MOS, including the last self-connected X pair and rail-gated OFF devices; Q8 uses the explicit upper trip and square-law onset model.

Student images, identities, grades and unrelated files are excluded. See SOURCES.md, sources.json, student-comparison.csv, coverage-entry.json and qa.json for provenance, scope and validation.
