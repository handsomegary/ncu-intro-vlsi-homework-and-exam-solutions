# Source review and decisions

## Added exam archive

The first individually selected exam is the 2024 midterm, reconstructed from its two photographed original pages after reading all four matching handwritten-answer pages. Its [source comparison](../exams/2024/midterm/SOURCES.md) retains verified work, identifies the Q6 capacitance-unit correction, and qualifies the Q3 missing NAND sizing assumption. The [exam index](../exams/README.md) records known incomplete/misfiled material for future selections.

## Older original-prompt assignments

The repository is `ncu-intro-vlsi-homework-and-exam-solutions`, following the
account's `ncu-digital-system-design-exams` course-prefix naming style.
The extension includes only authentic original-prompt tasks: [2019 HW2](2019/SOURCES.md),
[2018 HW1/HW2](2018/SOURCES.md), [2017 HW1–HW4](2017/SOURCES.md),
[2016 HW3](2016/SOURCES.md), [2015 HW1–HW4](2015/SOURCES.md), and
[2013 HW1–HW3](2013/SOURCES.md). Student-only material in 2012/2014 and 2018 HW3
is explicitly omitted following the user's clarification. The root coverage
catalog records every omitted assignment, without substituting neighbouring years.

The official [Fall 2013 course page](https://www.ee.ncu.edu.tw/jfli/public_html/vlsi1/Syllabus.htm)
directs homework downloads to Blackboard. The supplied 2013 `HW1.pdf`–`HW3.pdf`
were individually inspected and are genuine printed prompts, despite filenames
that differ from later `homework*.pdf` names. All supplied references were read
before independent derivation. Their reports/code are not republished as new work.

## Added 2020, 2021 and 2023 reviews

All twelve newly requested homeworks have supplied completed answers. They were read and compared with independent derivations and new simulations. See [2023](2023/SOURCES.md), [2021](2021/SOURCES.md) and [2020](2020/SOURCES.md) for per-source adoption/correction decisions and original-file fingerprints. That earlier extension covered 2023 through 2020, skipping 2022; HW4 remains pre-layout SPICE only.

The following existing section records the 2024 review.

Review date: 2026-10-13. The supplied **Fall 2024** PDFs and instructor clarifications define the requirements. Code from other years is used only as an architectural reference. All repository content is in English, including the translated instructor clarifications. The four original assignment PDFs are already in English; their public question content is retained, with a surname-only author footer.

## Assignment question sources

- [2024 assignment question PDFs](2024/assignments/README.md): complete original page format with a surname-only author footer.
- `hw3_instructor_testbench.sp`: original PWL sources, I/O names, 9 ns duration, CIN=0.
- HW3 instructor clarification specifying W>=0.47 um, 1.8 V swing, energy=Pavg times 9 ns, and required patterns. See the [English translation](2024/assignments/hw3_clarifications.en.md).
- HW4 instructor clarification of the full layout/DRC/LVS/PEX requirements. See the [English translation](2024/assignments/hw4_clarifications.en.md). This delivery follows the user's narrower request for pre-layout `.sp` files.

## Compared student answers

| Material | Content reviewed | Adoption or correction |
| --- | --- | --- |
| HW1 Reference A: supplied four-page correction/reference; Reference B: three-page `VLSI HW1.pdf` | All handwritten solutions and transistor connections; enlarged control complement bar | Independently simplify and verify connectivity, remove absorbed branches, and redraw complementary TG controls. A's central complement mark is visible, but its upper MOS symbol is unclear; no same-polarity-control fault is attributed to it. |
| HW2 `VLSI_HW2.pdf` | Stored voltage, leakage retention, pseudo-NMOS NOR sizing | Cross-check derivations; add retention conditions, sizing inequalities, and the BL readout qualification. |
| Supplied 2024 HW3 student archive, student ID 111501026 | Report and 88T XNOR/TG/mux code | Rerun an equivalent circuit under identical conditions and compare with reconstructed candidates; see HW3 measurements. |
| Supplied 2024 HW4 student archive, student ID 111501026 | Three-page report, 64T schematic, actual PEX files, testbench | Use the architecture as a candidate. The report reverses pre/post labels and its testbench combines two DUTs, so total power is not a single-design measurement. Its layout area and PEX are not results of this work. |

Reference labels identify the compared student work. Existing student documents are used as fallible references and are not presented as new solutions.

## Public search

Queries included `Li 2024 homework VLSI github`, `EE3032 Homework github`, `NCU VLSI 2024`, `four_bit_multbased_adder`, and `NCU VLSI`. Search visibility is limited; no claim is made that other 2024 solutions do not exist.

- [dOwOb1212/NCU_VLSI_Design_2023_HW](https://github.com/dOwOb1212/NCU_VLSI_Design_2023_HW): reviewed [`hw1/CLA_cmos.sp`](https://github.com/dOwOb1212/NCU_VLSI_Design_2023_HW/blob/main/hw1/CLA_cmos.sp), Git blob SHA `9bee2ead3081e2abb2e5e19fee6f47c9414c267c`. Its two-XNOR/carry-mux unit checks the carry equation, but carry still propagates bit by bit despite the CLA filename. This is an **8-bit** implementation with W=0.25/0.45 um and different vectors, below the 2024 minimum W=0.47 um. The full program was not copied into this repository.
- [Yeimaoz/NCU_VLSI](https://github.com/Yeimaoz/NCU_VLSI): found in search, but the API returned `409 Git Repository is empty`; no solution was available to read.

Each report records its derivation, sources, and verification conditions. Unverified values from existing answers are not presented as new measurements.

## HSPICE measurement definitions

The installed official PrimeSim HSPICE documentation was checked: `docs_help/hspice_6/selecting_simulation_output_parameters.htm`, **Power Output**. `POWER` includes dissipation and changes in stored energy. Its sign convention gives the negative sum of power absorbed by all independent sources, including PWL input drivers. It differs from VDD-only supply power. Both are reported, and the instructor's total `POWER` definition is used for 9 ns energy.
