# Sources and correction decisions

The source is the local archive's `2024/113學年度第一學期超大型積體電路導論期中考 Li.pdf`. Pages 1-2 are photographed original exam sheets; pages 3-6 are a matching graded handwritten answer by 陳建均. All six pages were visually read before authoring. A printed score of 100 is recorded as provenance, not treated as proof that every derivation is correct. Source fingerprint and extraction decisions are in [sources.json](sources.json).

The original two prompt pages are published in a rebuilt PDF container. Their page-content streams and embedded photograph bytes were checked against the source and are unchanged. The four student-answer pages and identifying number are not republished. The typeset reconstruction preserves all question text, part marks, full-expression complement bars, MUX conventions and circuit connections; perspective, incidental handwritten annotations and original page spacing are not replicated. It is a transcription, not an instructor-issued original.

| Question | Retained | Corrected or qualified |
|---|---|---|
| Q1(a)-(j) | Oxide-field reason; photolithography idea; fin count; non-ratioed/full restoration; subthreshold/junction leakage; interposer microbumps; backside power; body bias; charge/current speed; capacitance components | Add omitted patterning steps and power cost; explain body/source voltage rather than saturation labels; give representative assembly steps with process-dependent order |
| Q2 | Exact sixteen constants, selector order z/x/y/s leaf-to-root, left1/right0; passive RC-ladder quadratic scaling | Distinguish fifteen cells, four path stages and conditional first-moment coefficient |
| Q3 | A plus two added inverters, approximate e/e^2 widths and 3eRCg | NAND pMOS20W/L follows from its rise resistance, but nMOS width is absent; 20Cg is explicit convention, not a unique deduction. General C_D=(20+w_n)Cg/2 and exact optimum are provided |
| Q4 | 0.8 V onset, interior saturation/saturation/cutoff | State threshold/boundary endpoints and switch-R model scope |
| Q5 | NOR NML<NMH and NAND NML>NMH | State matched-threshold/effective-strength comparison; A=1 masks a single-G1-input VTC; illustrative values are not original/process measurements |
| Q6 | Six-MOS NAND-plus-inverter topology and balanced final inverter | Cg is per W/L transistor here, so final-inverter input is3Cg. Student nMOS sizes give10RCg worst, exceeding8. Change both NAND nMOS to2W/L, preserving pMOS and inverter sizes, giving7RCg |
| Q7 | All three correct student complementary CMOS graphs | Independently check32 words for exactly one conducting rail and correct full-bar polarity; no inner input complements introduced |

## Primary technical references for Q1

- [Synopsys FinFET design article](https://www.synopsys.com/articles/finfet-design.html): electrical width and constrained/quantized sizing.
- [Intel PowerVia technical announcement](https://www.intel.com/content/www/us/en/newsroom/news/powervia-test-shows-industry-leading-performance.html): separate backside power/frontside signals and lower droop. Historical release forecasts are not used.
- [TSMC CoWoS technology](https://www.tsmc.com/english/dedicatedFoundry/technology/cowos): silicon-interposer die integration.
- [TSMC US11094671B2, Figure11](https://patents.google.com/patent/US11094671B2/en): representative die-to-wafer, encapsulation and backside/substrate assembly flow; one disclosed embodiment, not a universal commercial recipe.

All derivations and published editable diagrams are newly authored after comparison. No layout, analog simulation or fabricated measurement is claimed for this analytical exam.
