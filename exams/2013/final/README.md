# NCU Introduction to VLSI — 2013 Final

The complete three-page photographed paper is reconstructed in editable English LaTeX/TikZ. All eight questions and all 150 printed points are retained, including the printed note about attainable points. Student answers were independently audited, not assumed correct.

- `exam.tex` / `exam.pdf`: editable original-question reconstruction.
- `solution.tex` / `solution.pdf`: independently derived answers and source/model qualifications.
- `verify.py`, JSON/CSV evidence: analytical, truth-table, connectivity and timing checks.
- `sources.json`, `SOURCES.md`: source hashes and comparison provenance.

Q3 has a shared N3 and nonunique valid balanced width families. Q4 shows symbolic external loads and the printed unloaded approximation; exact conduction includes parallel paths and state correlation. Q5(d) allows exactly three added FFs, so the optimized cut is after NOR, middle XOR, and the lower inverter, with an explicit output-polarity restoration and hold repairs. Q7 is underdetermined: no rising-input output transition fixes its upper threshold; no numeric pair is invented.

Run `python verify.py` for independent checks. Compile each standalone TeX file with pdfLaTeX twice. All figures are editable vectors and no raster source photograph is embedded in either reconstructed TeX document.
