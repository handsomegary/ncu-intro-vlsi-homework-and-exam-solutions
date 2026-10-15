# 2020 source review and reconciliation

The instructor's local assignment PDFs are authoritative. Visual inspection confirmed the overbar on HW1 Q3(a) and the internal **F** / final **Z** labels in HW3/HW4. Supplied student material was reviewed before independent derivation and simulation. It is attributed below and is not redistributed as new original work.

| Source | Author | Retained | Corrected / limits |
|---|---|---|---|
| HW1/HW1_answer.pdf (2 pages) | 吳佳媚 / J.-M. Wu, 107501503 | M1/M4 result, half-size equivalence, Shannon expansion, CMOS networks | Expanded nonzero-current proof and static-model caveat; fourth MUX generates complement |
| HW2/HW2_answer.pdf (4 pages) | 吳佳媚 / J.-M. Wu, 107501503 | XNOR/NAND, valid rotation mapping, NOR, final corrected 9/2 ratio | Early strength inversion discarded; high-Vt delay assumption made explicit; replaced large cascaded rotator by 40T direct TG design |
| HW3/HW3 107501503 吳佳媚.pdf | 吳佳媚 / J.-M. Wu | Six-transistor topology and explicit 1 fF load | 3.3 V on 1.8 V models, upper NMOS body at stack node, incomplete direction coverage corrected |
| HW3/VLSI HW3.docx | 孫書業 / S.-Y. Sun, 107501566 | 1.8 V supply, grounded NMOS bodies, both direction discussion | Listed code omits 1 fF; coarse 0.1 ns interval, manual/inconsistent values not adopted |
| HW4/1/VLSI HW4.docx and 1.inv.sp | 孫書業 / S.-Y. Sun | Schematic topology only | No layout, extracted parasitics, or post-layout claims adopted |
| HW4/2/HW4 107501503 吳佳媚.pdf and pre-sim.sp | 吳佳媚 / J.-M. Wu | Corrected VSS body tie in pre-sim.sp | 3.3 V and missing standalone load corrected; layout/post-sim outside scope |

All headline HW3 numbers are new HSPICE results for a documented 1.8 V TT design with declared geometry, 1 fF load, and 20 ps input ramps. HW4 explicitly reuses these same-circuit results. Choosing a smaller number across incompatible model/supply/load assumptions would not be a valid integration of answers.

## Original-file fingerprints

- `HW1/HW1_answer.pdf`: SHA-256 `3cb44c186e1a3427d4fe85bb3461e96591cefd961706b5894880e3617160c019`
- `HW2/HW2_answer.pdf`: SHA-256 `991af466a26a571d0bda6abe2d1bac4b0bd208afe9e56cae98613f1b4d942da8`
- `HW3/HW3 107501503 吳佳媚.pdf`: SHA-256 `e000a351dd3a59de5114f7cdcb1f42e2867f1a8a9e931204f2214aa6e6359185`
- `HW3/VLSI HW3.docx`: SHA-256 `f78fa2cb3c9a865306dc4981e7f8d5b5692381c9b423e0ea7916bdfde18cbf70`
- `HW4/1/VLSI HW4.docx`: SHA-256 `0d675e2d2d492e6413e469ee601d498dee75b4fb4f67b33c02f91fb7893efe13`
- `HW4/1/1.inv.sp`: SHA-256 `55a57ef7e04f26a03883512f01d4622f6c2be6d8064acc0f15ad0de9df58f84a`
- `HW4/2/HW4 107501503 吳佳媚.pdf`: SHA-256 `f9ef88b9b4246d7ef76b9e2a4f7dc97120dbcaf2316479350af049be9f1e7acb`
- `HW4/2/pre-sim.sp`: SHA-256 `9bbcd965536cf330c43fdcef580ce2be443890d57fff2524e26ff28c74d7eb0c`

The process model is used locally from `D:/cic018.l`; its contents and license information are not redistributed.
