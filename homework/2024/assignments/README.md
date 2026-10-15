# Original 2024 assignments and instructor clarifications

These are complete public question PDFs in the original page format. Only the author first name is removed from the footer; surname Li remains. All question text, circuit figures, marks, dates and pagination are retained. [Preservation catalog](../../PROMPTS.json) records the public PDF hashes.

The original PDFs define the assignments. This table describes the requirements and delivered scope.

| Assignment | Original requirement | Delivered scope |
| --- | --- | --- |
| [HW1](homework1.pdf) | Static CMOS logic, controlled four-input/four-output circuit, pass-transistor analysis, CMOS implementation | [HW1](../HW1/): derivations, transistor diagrams, truth tables |
| [HW2](homework2.pdf) | Nonideal NMOS transmission and retention; ratioed logic function and sizing | [HW2](../HW2/): analytical solutions with HSPICE checks. The original 2024 questions are analytical. |
| [HW3](homework3.pdf) | Four-bit serial-parallel multiplexer-based adder; worst-case delay, power, transistor WL area, energy/area comparison | [HW3](../HW3/): transistor-level `.sp`, prescribed patterns, verification and candidate comparison |
| [HW4](homework4.pdf) | HW3 layout, extracted netlist, pre/post-layout comparison | [HW4](../HW4/): runnable pre-layout `.sp` as requested; no layout, DRC, LVS, PEX, or post-layout results |

## HW3 instructor conditions

- Preserve the specified testbench signal names and PWL, CIN=0, duration 9 ns.
- Apply `(X,Y)=(1,5),(15,13),(11,9),(4,8),(3,7),(12,14),(2,15),(6,10)` in order.
- Supply is 1.8 V, output levels should approach 0 V/1.8 V, minimum W=0.47 um.
- `energy = average power x 9 ns`; HW3 area is `sum(W_i L_i)` for all transistors.
- Read the [English clarification translation](hw3_clarifications.en.md). At the user's request, numerical statistics and reproducible checks replace GUI waveform screenshots in this delivery.

## HW4 area and scope

The [English clarification translation](hw4_clarifications.en.md) specifies a layout rectangle covering all materials, **not** HW3's `sum(W_i L_i)`. No physical layout area or post-layout results are claimed, and previous students' layout values are not reused.
