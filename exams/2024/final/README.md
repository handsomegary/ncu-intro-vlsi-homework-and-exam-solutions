# 2024 final: reconstructed exam and corrected solutions

The question set has two printed pages. Two handwritten answer sets were reviewed, one partial Q1 set and one full set; their scores are provenance, not correctness evidence.

[Reconstructed paper](exam.pdf) / [standalone TeX](exam.tex) has three pages and all six questions. [Worked solutions](solution.pdf) / [standalone TeX](solution.tex) has eleven pages. The printed allocations sum to **110 points** and are preserved. All reconstructed diagrams are editable TikZ, with no scan image embedded. Named terminals in solution MOS drawings are electrically connected; nMOS bodies use VSS, pMOS bodies VDD.

- Q3: the middle pMOS and footer use the barred clock; its printed output is Y-bar. Rewire the pMOS gate to Z AND remove the footer for a static inverter. The student's input-inverter/clock-change repair is valid with a different stated output polarity. Charge sharing is tested only when no real ground path exists: ABC=100 or001, giving33/46 or3/4 VDD under the specified nodal caps. Keepers address both dynamic polarities.
- Q4, approved dual presentation: fixed external-C classroom sizing gives3RC; counting the actual feedback-gate load gives72/7 RC for those sizes. The literal model has infimum24/7 RC, so3RC is infeasible. Floating open-switch gates and conditional equal-width hysteresis/current calculations are explicit.
- Q5: extract all14 physical crossings, including four always-off isolation MOS; z=not(a)+b+c.
- Q6, approved dual presentation: literal positive R4 capture delay gives416.667MHz; adverse-skew interpretation gives333.333MHz. Separate valid balanced clock trees meet400MHz. The original NOR is preserved: Y1=0 and Y2=A xor B xor C. The student's extra XOR term and launch-only buffering are corrected. Hold and physical SER claims are qualified by missing parameters.

```sh
python verify_dynamic_schmitt.py
python verify_logic_timing.py
pdflatex exam.tex
pdflatex exam.tex
pdflatex solution.tex
pdflatex solution.tex
```

The checks use Python's standard library and the exam's ideal switch/RC/timing models. No process file or measured HSPICE result is claimed. Saved CSV/JSON evidence includes exhaustive DPL/carry/layout/NP logic, dynamic-cycle charge-sharing states, Schmitt sizing bounds, clock-path constraints and conditional masking. See [sources.json](sources.json), [source review](SOURCES.md) and [PDF QA](pdf_qa.json).
