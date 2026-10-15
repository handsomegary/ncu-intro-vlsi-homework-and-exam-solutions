# Sources and comparison

Primary source: `111學年度第一學期超大型積體電路導論期中考 Li.pdf` in the supplied 2022 archive. Original PDF pages1–2/printed2-1 and2-2 have Fall2022 footers; Q1–Q6 sum to100 points. Graded handwritten answers are pages3–6; page7 is a separator; pages8–15 are supplemental notes. Personal identifiers are not repeated in reports. Embedded original-photo hashes before/after extraction are recorded in `sources.json`.

Q1: normalize the supplement's shifted lettering by wording. Correct SOI's exaggerated no-junction/no-leakage claim, normal subthreshold leakage in place of latch-up, via-first timing before FEOL, and the NMOS threshold's increase with VSB. Oxidation growth/deposition and bonding orientation/granularity are distinct classifications, not resolved by grading.

Q2: printed completion input/selector stubs are blank; handwritten A/B/C/D are not fixed constraints. Independently use outer B and inner D selectors, with C/1 and A/1 inputs. A TG binary tree uses14 TGs and an unbuffered distributed path has quadratic internal RC delay, correcting the sheet's linear-delay claim.

Q3: the printed buffer is noninverting. Eight inverters are stages0–7; the notes' additional stage8 is an off-by-one polarity error. Fixed nMOS and doubled pMOS change receiver input capacitance by1.5, including the first input; CL is unchanged. The independent delay is11.5f RCg for f=2980^(1/8), with altered NAND A load stated explicitly. Do not retain the sheet's nRC estimate.

Q4: supplied .8V and N1/N2 saturation,N3 cutoff are valid within the stated switch-R model after consistent voltage accounting. Region boundaries are separated from the open time interval.

Q5: source is a four-device rail-fed/pass XOR. The ideal settled full-rail paths are verified; drive exists but depends on input drivers. The sheet's 'no driving ability' wording is qualified, not copied as a literal absence of conductive drive.

Q6: positive a-function uses original inputs and a static output inverter; complemented-input alternatives require generators. For101→100→101, b has two same-type series devices on either active path, so p/n equivalent widths eachW/2. Rp/Rn and external load remain symbolic because Q6 does not specify them independently.

## Primary conceptual references

Only primary papers, university-authored course/lab documentation, foundry documentation, or device-maker technical pages were used. No secondary search-result explanations are relied on.

1. Photolithography sequence (a): BYU cleanroom positive-resist SOP, https://cleanroom.groups.et.byu.net/SOP_05PR.phtml ; additional full mask-to-substrate flow through etch/strip: Simon Fraser University microfabrication lecture, https://www.sfu.ca/~gchapman/e495/e495l3l.pdf . The latter explicitly lists coating, exposure, development, etching, and stripping in order.
2. SOI BOX isolation/electrostatic leakage benefit (b): STMicroelectronics FD-SOI technical page, https://www.st.com/content/st_com/en/about/innovation-and-technology/fd-soi.html . Its FD-SOI-specific strong electrostatic-control claim should not be generalized to every SOI structure.
3. Thermal oxide growth versus deposited oxide (c): BYU cleanroom film deposition/growth documentation, https://www.cleanroom.byu.edu/FilmDeposition . Dry/wet reactions and growth distinction: University of Texas at El Paso NanoMIL, https://www.utep.edu/engineering/nanomil/processes/oxidation_basics.html . These sources support the technical terminology, not the inferred grading intent.
4. Normal CMOS static junction/subthreshold leakage (e): Berkeley-hosted Digital Integrated Circuits lecture, https://people.eecs.berkeley.edu/~alanmi/research/timing/papers/lec25_bw_2xp.pdf ; independent course explanation, https://archive.nptel.ac.in/content/storage2/courses/117101058/Slides/26.5.htm .
5. Physically thicker high-k at same electrical thickness and lower tunneling (g): Intel technical reference, https://www.intel.com/pressroom/kits/advancedtech/doodle/ref_HiK-MG/high-k.htm .
6. Via-first before FEOL, via-middle between FEOL/BEOL, via-last after BEOL (h): Burkett et al., "Tutorial on forming through-silicon vias", JVST A 38, 031202 (2020), DOI https://doi.org/10.1116/6.0000026 ; publisher page https://pubs.aip.org/avs/jva/article/38/3/031202/1023659/Tutorial-on-forming-through-silicon-vias .
7. Body-effect threshold formula/direction (i): McMaster University MOSFET lecture, https://www.ece.mcmaster.ca/faculty/bakr/ece2ei4/Lecture16_Web.pdf . The stack-specific interpretation above is a circuit inference from the source-bias formula, not a claim that every output-connected device necessarily has body effect.
8. Antenna charge collection/oxide damage and diode protection (j): SkyWater SKY130 PDK antenna rules, https://skywater-pdk.readthedocs.io/en/main/rules/antenna.html ; University of Michigan lecture, https://www.eecs.umich.edu/courses/eecs427/w07/lecture2.pdf . Jumpers/higher layers: Jia Wang and Hai Zhou, "Optimal Jumper Insertion for Antenna Avoidance under Ratio Upper-Bound", DAC 2006, author-hosted paper https://users.ece.northwestern.edu/~haizhou/publications/dac06wang.pdf .
9. F2F/F2B/B2B styles (k): Boris Vaisband dissertation, University of Rochester, Figure 2.9, https://www.hajim.rochester.edu/ece/sites/friedman/Boris_Vaisband_PhD.pdf . Separate W2W/D2W/D2D classification: imec monolithic microsystems white paper, page 7, https://www.imec-int.com/sites/default/files/2024-06/imec_WP_Monolithic_microsystems_LORES.pdf . The graded answer establishes which classification was accepted for this exam.
10. IG/SG FinFET operation (m): Chaudhuri and Jha, "Ultra-Low-Leakage and High-Performance Logic Circuit Design Using Multiparameter Asymmetric FinFETs", ACM JETC 12(4), article 43 (2016), https://doi.org/10.1145/2832913 . Publisher search-visible abstract explicitly defines independent and shorted front/back gates; the direct DOI open returned an error, so do not claim the full paper was retrieved.
