# 2016 source ledger

Original course prompts: Li, EE3032, National Central University, Fall 2016. Original PDFs are original-format copies with only the author first name removed.

- `assignments/homework3.pdf`: SHA-256 `6be83e172ba28cfe3bce6b97bcd101afd9c2480ba90714c27d70080bcdb2004a`.

## Supplied completed answers

These references were read and compared with the independent derivation before finalizing the solutions. Answer PDFs/JPGs/DOCX files, student numbers, and proprietary process-model contents are not redistributed.

- Reference DOCX A, attributed to 林琦靜: SHA-256 `66fe3e576a0163b5e820b22c2870e5a66113d813b1500e8103407101ea847d99`.
- Reference DOCX B, attributed to 劉治硯: SHA-256 `2740374226c51ddc982ecf7a9a8109266b6cc85692d2fe1274551542bb09459d`.

## Independent comparisons

- Both supplied DOCX answers were read, including embedded netlist/screenshots. The correct equal-size six-transistor graph is retained. One reference omits some transitions and has inconsistent direction/word labels; the other ties the upper nMOS body to its moving source. This solution covers all six changing-output transitions, uses standard VSS/VDD bodies, and reports declared supply/load/slew conditions.
- One reference plots peak short-circuit power instead of a cycle average; the other divides an AVG current by a period, which has incorrect units. This solution uses HSPICE intrinsic channel IDS probes and a full steady-period integral. The qualitative decreasing load trend is verified under the stated3 ns slew and fixed sizing.
- The original 0.5pdf spelling is interpreted as0.5 pF from the surrounding values. HW1/HW2/HW4 prompts are absent; nothing is reconstructed from student-only material.

## Verification

All available reports compile as standalone pdfLaTeX sources with embedded diagrams/plots. HSPICE runs use only the local CIC018 TT process file. Actual numerical CSV/JSON results are in each `results/` directory. Theory checks explicitly state their ideal-model assumptions. No unverified public-web answer is used.
