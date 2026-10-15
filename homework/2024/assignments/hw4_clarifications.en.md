# HW4 instructor clarifications - English translation

English translation of the instructor clarification. Dated updates and grading rules are retained, including the later change in base credit.

## December 17

Area is length times width.

## December 22

Required submission:

1. PDF containing layout, DRC, LVS, pre/post-simulation waveform screenshots.
2. SPICE file after PEX.
3. Excel table with area in um² and energy in p-units, as labeled in the original notice.

Grading rules:

1. Complete deliverables with no deductions receive 10 base points.
2. Missing layout, DRC, LVS, pre/post-simulation waveform screenshots, written explanation, or calculations results in zero points.
3. Logic 1 must be 1.6-1.8 V; logic 0 must be 0-0.2 V. Deduct one point per violating signal, up to five points. Glitches are allowed if the output eventually reaches a valid level.
4. Measure layout length and width with a ruler and include a screenshot.
5. Rank only area and energy, not delay.
6. Apply deductions after ranking.

## December 23

Architecture and dimensions may change, but update the SPICE file accordingly. Include pre/post-simulation waveform screenshots.

## December 25

The measurement rectangle must cover **all used materials**, including NW, NIMP, POLY, and metal (spelled `MATAL` in the original).

HW4 base credit is 15 points; the remaining 5 points come from ranking.

## Scope used here

The user limited this delivery to runnable pre-layout `.sp` and numerical statistics. Layout, DRC, LVS, PEX, physical layout area, and post-layout simulation are outside this delivery, which is narrower than the original full assignment translated above.
