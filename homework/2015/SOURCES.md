# 2015 source reconciliation

All four original instructor PDFs are available and copied in original format with only the author first name removed into `assignments`. The answer PDFs/JPGs/DOCX/code archives were inspected before independent work. No process library or historical simulator/license logs are redistributed.

| Source | Retained | Corrections / scope |
|---|---|---|
| HW1/solution (1).jpg and solution (2).jpg; author not shown | M1/M4 argument, long-channel series-current proof, MUX cofactors, CMOS diagrams | Visually confirmed the original Q4(a) outer AND inner complement; independently checked the exact Boolean expression |
| HW2/solution.jpg; author not shown | Input-ramp explanation, A-C critical path, mobility result | State symmetric-threshold assumption; resolve inconsistent noise-margin signs using actual definitions and unity-slope VTC points |
| HW3/VLSI-HW3.docx and 3-1.zip / 3-2.zip, 劉家維 / J.-W. Liu, 102501556 | Authentic 2015 6T AND topology, all widths 0.47um; power inverter widths 0.47um / 1.88um | Historical Z delays trigger from F, not A/B; coarse time interval and partial transition set corrected. Replace threshold-window averages by explicitly defined full-cycle overlap estimator, separate supply/switching quantities, and sufficient settling time |
| HW3/hw3.docx; author unclear | Qualitative current-overlap discussion only | Its 8-to-1 MUX task does not match the authentic 2015 AND prompt and is not substituted for it |
| HW4/black.txt, 4-1 code.jpg, archived 4.sp | Instructor's 28T mirror topology | Size using explicit worst-output-slew target; trigger delays from primary inputs, exhaustively cover all56 transitions |
| HW4/4-2 code.jpg and archived 4D.sp | Dynamic-logic comparison | Historical mixed n/p dynamic circuit is not conventional n-type domino. Replace with separately evaluated positive carry-complement rail, proper keepers/footers, and all8 evaluate/reset cases |

The legacy `VLSI-HW4.doc` is available locally but its binary body was not used as evidence; the visually inspected code JPGs, authenticated original PDF, and readable archive netlists provide the reviewed topology. The numerous historical wave screenshots are not reused as measurements of the new circuit.

## Fingerprints of reviewed source files

- `HW1/solution (1).jpg`: SHA-256 `74e411e920f416b90239b540353ff73d4890114ed419712f65e761b82b587eba`
- `HW1/solution (2).jpg`: SHA-256 `7def21606cca857e70d90437e85b6a85d69a4aceda1d50268ed2fa94510a4289`
- `HW2/solution.jpg`: SHA-256 `e7dfe56eb9d9de56dc2e99155686f44e3c0302a5480e7eead805b048da837c7c`
- `HW3/VLSI-HW3.docx`: SHA-256 `0f043fa642ec03ad50ab168b305a58cd775a1d985c338e16634753bdc6b8270d`
- `HW3/hw3.docx`: SHA-256 `3b8adb70881303ee8374d159a69d565094f064e68281c693b5b8f779548f4da1`
- `HW3/3-1.zip`: SHA-256 `0b7ba9811862b8aae4991a91b670a8eccb7b2bf617be589853668560f3522331`
- `HW3/3-2.zip`: SHA-256 `3c561f076d6a8df66195f332ef40175fe4c3dd146ddeafa073896ba1201d3d28`
- `HW4/black.txt`: SHA-256 `7fe7e8435d6200162951a7447bd65d947fab109655cb41685a34f179d19eb28a`
- `HW4/4-1 code.jpg`: SHA-256 `c5ded7914610b0306c18d73fa49d9817e348f5102ff37867c392672cfd3c2659`
- `HW4/4-2 code.jpg`: SHA-256 `7f5ff353a321b161e8d2166df54201a61a553045067c804d24d760e6f447536f`
- `HW4/HW4.zip`: SHA-256 `6dbdf9b6e4eea57f60073dd69addf73e52349d1702d22abe3ba3f144f3bae2d6`

2014 is excluded because its local folder contains student-only material and no original prompt, per the user's explicit scope.
