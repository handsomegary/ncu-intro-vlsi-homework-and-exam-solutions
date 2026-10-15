# 2021 final - partial original

The available question views contain overlapping photographed fragments and a later typed Q7 supplement. Editable standalone `exam.tex` reconstructs readable Q1-Q5, the surviving Q6 opening/(c)/diagram, and Q7(a)-(c), and marks original missing wording. `solution.tex` derives corrected solutions for intact questions. Missing Q6 timing text is not inferred from student answers; Q6 is unanswerable and skipped. Original Q7(d)-(f) is likewise missing; its secondary typed transcription and conditional concept notes are explicitly qualified.

Important distinctions: Q2 has an explicit external C and series N4/P4 control paths; Q3 has one full-expression complement, and DSL loads use opposite low-swing internal gates plus Vref clamps; Q5 all-transition activity is 0.5 but charging activity is 0.25 per input step, and equal NAND delays alone do not exclude input-skew glitches. Exact physical model limits are labeled. The printed question totals are 105, with no normalization or invented missing point labels.

Q4 extracts all 20 MOS as eight inverters and two transmission gates. Its latch feedback stays continuously connected, so writeability depends on unspecified driver/feedback strengths. The graph checks preserve and detect attempted-write contention rather than replacing the original with an invented switched-feedback latch. Successful writes give conditional falling-edge storage Y=X.

Run `python verify.py` and `python verify_layout.py` for the included ideal logic/algebra/contact-extraction checks. All diagrams are editable TikZ; repeated MOS net labels are electrically connected. No HSPICE measurements are claimed.
