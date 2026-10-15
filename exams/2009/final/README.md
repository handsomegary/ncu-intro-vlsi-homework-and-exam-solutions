# 2009 final

Complete Q1-Q7 occupy three pages; the printed weights total 90%. No missing ten-percent question is invented. No matching student answer was identified, so all solutions are derived independently.

exam.tex and solution.tex are standalone editable LaTeX/TikZ. Layout geometry is reconstructed with native PDF vector coordinates and every transistor/contact retained. Run `python verify.py` to regenerate standard-library analytical CSV/JSON evidence. Build PDFs with two passes of `pdflatex exam.tex` and `pdflatex solution.tex`, or the built-in standalone compiler.

Material qualifications: Q1 feedback is ratioed, Q2 is negative-edge and dynamically retains charge, Q3 needs strict alpha>1 rather than pooling a grounded node, Q3b explicitly completes the pass path as a TG, Q4 domino needs valid complemented inputs and changes sum reset polarity, Q6 retains all8MOS, and Q7's full overbar is essential. No process model or SPICE result is claimed. See SOURCES.md, sources.json, coverage-entry.json, verification.json and qa.json.
