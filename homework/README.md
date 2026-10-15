# NCU Introduction to VLSI Design — Homework archive

National Central University, EE3032. Complete original-format question PDFs are public;
English LaTeX reports, transistor diagrams, runnable SPICE and measured evidence
are organized by course year.

The homework collection covers **31 assignments across ten years from 2013 to 2024**.
The latest extension adds **15 assignments from 2013–2019**. Only work with
an authentic original prompt is included; student-only material is skipped.

## Public assignment questions

These PDFs preserve the original questions, figures, point values and page layout. The author footer uses surname Li only. [Prompt catalog and preservation checks](PROMPTS.json).

| Year | HW1 | HW2 | HW3 | HW4 |
|---|---|---|---|---|
| 2024 | [PDF](2024/assignments/homework1.pdf) | [PDF](2024/assignments/homework2.pdf) | [PDF](2024/assignments/homework3.pdf) | [PDF](2024/assignments/homework4.pdf) |
| 2023 | [PDF](2023/assignments/homework1.pdf) | [PDF](2023/assignments/homework2.pdf) | [PDF](2023/assignments/homework3.pdf) | [PDF](2023/assignments/homework4.pdf) |
| 2021 | [PDF](2021/assignments/homework1.pdf) | [PDF](2021/assignments/homework2.pdf) | [PDF](2021/assignments/homework3.pdf) | [PDF](2021/assignments/homework4.pdf) |
| 2020 | [PDF](2020/assignments/homework1.pdf) | [PDF](2020/assignments/homework2.pdf) | [PDF](2020/assignments/homework3.pdf) | [PDF](2020/assignments/homework4.pdf) |
| 2019 | Not supplied | [PDF](2019/assignments/homework2.pdf) | Not supplied | Not supplied |
| 2018 | [PDF](2018/assignments/homework1.pdf) | [PDF](2018/assignments/homework2.pdf) | Not supplied | Not supplied |
| 2017 | [PDF](2017/assignments/homework1.pdf) | [PDF](2017/assignments/homework2.pdf) | [PDF](2017/assignments/homework3.pdf) | [PDF](2017/assignments/homework4.pdf) |
| 2016 | Not supplied | Not supplied | [PDF](2016/assignments/homework3.pdf) | Not supplied |
| 2015 | [PDF](2015/assignments/homework1.pdf) | [PDF](2015/assignments/homework2.pdf) | [PDF](2015/assignments/homework3.pdf) | [PDF](2015/assignments/homework4.pdf) |
| 2013 | [PDF](2013/assignments/homework1.pdf) | [PDF](2013/assignments/homework2.pdf) | [PDF](2013/assignments/homework3.pdf) | Not supplied |

The supplied duplicate [2020 HW4 version2](2020/assignments/homework4_version2.pdf) is also preserved.

## Solutions and evidence

| Year | Completed original-prompt assignments | Reports and evidence |
|---|---|---|
| [2024](2024/README.md) | [HW1](2024/HW1/), [HW2](2024/HW2/), [HW3](2024/HW3/), [HW4](2024/HW4/) | Existing four reports; 100 HW1 checks, 43 HW2 checks, 512 RCA states and prescribed HW4 vectors |
| [2023](2023/README.md) | [HW1](2023/HW1/), [HW2](2023/HW2/), [HW3](2023/HW3/), [HW4](2023/HW4/) | 284 switch-connectivity checks; three HW2 decks; 128 RCA states and 896 single-input transitions |
| [2021](2021/README.md) | [HW1](2021/HW1/), [HW2](2021/HW2/), [HW3](2021/HW3/), [HW4](2021/HW4/) | 32 Boolean cases and 5050 stack points; 64 electrical rotator cases; measured AND delays |
| [2020](2020/README.md) | [HW1](2020/HW1/), [HW2](2020/HW2/), [HW3](2020/HW3/), [HW4](2020/HW4/) | 32 Boolean cases; 64 electrical rotator cases; 18 AND runs and timestep/slew checks |
| [2019](2019/README.md) | [HW2](2019/HW2/) | Independent four-question HW2; new slew and pi-RC runs |
| [2018](2018/README.md) | [HW1](2018/HW1/), [HW2](2018/HW2/) | 40 Boolean checks and 5050 stack points; slew and ideal pi-RC HSPICE verification |
| [2017](2017/README.md) | [HW1](2017/HW1/), [HW2](2017/HW2/), [HW3](2017/HW3/), [HW4](2017/HW4/) | Four reports; analytical/program checks; AND/Psc measurements; balanced mirror and domino SPICE |
| [2016](2016/README.md) | [HW3](2016/HW3/) | Independent HW3: equal-size AND delay and specified five-load Psc curve |
| [2015](2015/README.md) | [HW1](2015/HW1/), [HW2](2015/HW2/), [HW3](2015/HW3/), [HW4](2015/HW4/) | Four reports; theory/CMOS checks; equal-size AND and Psc; balanced mirror and domino SPICE |
| [2013](2013/README.md) | [HW1](2013/HW1/), [HW2](2013/HW2/), [HW3](2013/HW3/) | 32 CMOS/MUX checks, 80,800 square-law points; clock/noise analysis; fixed-size TG MUX comparison and Psc sweep |

## Coverage and missing material

- **Homework years 2012 and 2014:** skipped because only student answers are available; this does not exclude the original 2012 exam papers.
- **2013:** HW1–HW3; HW4 missing.
- **2016:** HW3 only.
- **2018:** HW1/HW2 only; student-only HW3 and missing HW4 skipped.
- **2019:** HW2 only.
- **Homework year 2022:** absent and explicitly skipped; the separate 2022 midterm original is included in the exam archive.

See [COVERAGE.json](COVERAGE.json) for every year and homework status.
2019 HW2 and 2016 HW3 are self-contained and require no previous homework circuit.
Public question PDFs retain all original questions and figures; only the author first name is removed from the footer.
The two original 2020 HW4 archive copies are both preserved.

## Reports, source comparison and requested scope

Each included homework contains a standalone `.tex` report, a compiled and
visually inspected PDF, a README, source comparison and reproducible checks.
HW1 retains full derivations and transistor diagrams. HW2/HW3 contain complete
analytical answers and applicable executable verification.

Existing supplied answers were read first, independently checked and integrated
with explicit attribution and corrections. 2019 has no same-year answer; its
identical 2018 HW2 questions allow an attributed cross-year comparison. See the
[source index](SOURCES.md) and each year’s `SOURCES.md`.

**HW4 stops at pre-layout SPICE.** In 2015/2017 the original HW4 asks for mirror
and domino full-adder circuits; both are implemented and simulated. In 2020
and later, HW4 uses the verified HW3 circuit, with rerun/reuse provenance
explained. No layout, DRC, LVS, PEX or invented post-layout results are claimed.

The reports distinguish ideal/square-law reasoning from actual process
simulation, RC first moments from threshold-crossing times, VDD supply power
from an explicitly defined short-circuit-current overlap estimate, and bounded
tested delays from a global PVT guarantee. Numerical conditions differ by year.

## Reproduction and package verification

- Python 3; the package checker uses the standard library.
- PrimeSim HSPICE S-2021.09; default `C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com`.
- The local CIC018 model, default `D:/cic018.l`; it is not redistributed.
- PDFLaTeX for standalone reports. Optional Matplotlib regenerates selected plots.

```sh
python ../verify_package.py
```

This checks public report coverage, artifact hashes, saved numerical results,
scope, README links and applicable HW3/HW4 netlist consistency. It does not
launch new HSPICE runs. Each homework README provides reproduction commands,
model/executable overrides and precise limitations.

`../MANIFEST.json` uses SHA256 with text line endings normalized to LF; binaries
remain unchanged. Raw simulator/compiler and license outputs stay local.
The detailed existing 2024 course work is indexed in [2024/README.md](2024/README.md).
