# NCU Introduction to VLSI — Fall 2007 Final

The complete two-page paper is reconstructed in standalone English LaTeX/TikZ. All seven printed percentages are retained (sum 105%, not rescaled). Both supplied answer sources are ungraded and were compared after independent derivation.

Q2's cross-connected pseudo-NMOS circuit implements XNOR under valid ratioed-level assumptions. Q3 is the literal 10-MOS, four-inverter/one-transmission-gate latch, whose fixed feedback requires adequate input drive to overwrite. Q4's smaller sum-node capacitor controls leakage retention: evaluation time below 2.34 µs; minimum frequency depends on duty D. Q5 explicitly restores the requested complement after the domino core and verifies differential/static polarities. Q6's 12-MOS dynamic circuit samples on the falling edge. Q7's 20 ns setup bound is distinguished from missing minimum-delay hold data.

Run `python verify.py`, `python verify_layout.py` and `python verify_layout_geometry.py` for independent checks. The last script verifies the actual normalized Metal1 routes and rejects unintended same-layer shorts. Compile exam.tex and solution.tex twice with pdfLaTeX. Visual/compiler/source-hash evidence is recorded beside the documents.
