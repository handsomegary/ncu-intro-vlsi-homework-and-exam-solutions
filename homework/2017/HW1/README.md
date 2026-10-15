# 2017 HW1

All four original questions are answered in standalone `solution.tex` and rendered `solution.pdf`: series-MOS region/equivalence, dual-Vt placement, a 4:1 mux, and both transistor diagrams. `python verify_logic.py` checks 48 Boolean output cases and 5050 ideal square-law stack points. The complete overbar in 4(a) is preserved.

The high-Vt NAND must fit within the original two-unit timing budget; no characterized dual-Vt PDK is supplied. The mux BC cofactors match the supplied solution. The majority-complement network is reduced from 12 to 10 transistors. References and corrections are in `../SOURCES.md`.
