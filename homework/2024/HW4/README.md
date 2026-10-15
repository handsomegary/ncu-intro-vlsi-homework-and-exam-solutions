# 2024 HW4: Simulation-ready SPICE deliverable

## Original assignment and scope of this delivery

The original [homework4.pdf](../assignments/homework4.pdf) requires a layout of the HW3 four-bit adder, extracted netlists, and pre/post-layout comparisons. As requested by the user, this delivery contains a **pre-layout transistor-level `.sp`, runnable testbench, actual statistics, and LaTeX report**.

Layout, DRC, LVS, PEX, post-layout simulation, and physical layout area are outside this delivery's scope and are not claimed as completed. The complete course submission requirements are preserved in the [instructor clarifications](../assignments/hw4_clarifications.en.md).

## Files

| File | Purpose |
|---|---|
| [four_bit_multbased_adder.sp](four_bit_multbased_adder.sp) | Copy of the final HW3 64T netlist, with identical devices, dimensions, and pin order |
| [testbench.sp](testbench.sp) | One DUT, the instructor's original nine input sources, TT/1.8 V/25 C, and a 9 ns run; adds a 1 ps maximum time step and output measurements |
| [reproduce.py](reproduce.py) | Calls local HSPICE, checks the eight specified vectors and energy consistency, and accepts alternate model/executable paths |
| [vectors.csv](vectors.csv) | Each input pair, expected integer sum, five actual output voltages, and check result |
| [statistics.json](statistics.json) | Measured power/energy, conditions, case count, and netlist/model SHA-256 hashes |
| [solution.tex](solution.tex), [solution.pdf](solution.pdf) | Compilable report and preview, including carry/sum equations, reference review, and scope limitations |

## Design and measured results

Each bit uses `e = X XNOR Y`, `S = e XNOR CIN`, and `COUT = e ? Y : CIN`; four cells are cascaded. The upper 4T XNOR's internal `e` node may exhibit threshold loss. The lower TG-XNOR uses CIN/CINbar as data and e/ebar as selects. Output levels are verified by transistor simulation; internal nodes are not assumed to be ideal 1.8 V logic levels.

This directory was simulated independently:

| Condition or quantity | Result |
|---|---|
| Process / simulator | User's local CIC018 TT / HSPICE S-2021.09 |
| Supply / temperature / interval | 1.8 V / 25 C / 0-9 ns |
| Added output load | None; equal performance under arbitrary loads is not implied |
| Maximum time step | 1 ps |
| MOS count / each W and L | 64 / 0.47 um and 0.18 um |
| Schematic `sum(WL)` | 5.4144 um^2; not physical layout area |
| HSPICE total average power | 69.558498 uW |
| VDD supply average power | 37.4328403 uW, reported separately from total power |
| Total energy | 626.026482 fJ = 0.626026482 pJ over the full 9 ns |
| Eight specified vectors | 8/8 passed; energy agrees with `Pavg * 9 ns` |

The input sequence is `(1,5), (15,13), (11,9), (4,8), (3,7), (12,14), (2,15), (6,10)`, with CIN = 0. Samples are taken at 1.8, 2.8, ..., 8.8 ns. Expected zero bits are checked against -0.02 to 0.2 V, and expected one bits against 1.6 to 1.82 V. Every actual voltage is available in the CSV. These acceptance bands do not guarantee operation at untested process/voltage/temperature conditions or loads.

[HW3](../HW3/) additionally contains a 512/512-case transistor transient check of the same netlist, the largest measured delay in the specified sequence, six-candidate comparisons, and results from the original testbench with a 0.1 ns output step. Results from different time-step settings must remain distinguishable.

## Reproduction

Run from this directory; Python uses only the standard library:

```powershell
python reproduce.py --model "D:/cic018.l" --hspice "C:/synopsys/Hspice_S-2021.09/WIN64/hspice.com"
```

Alternatively, set `CIC018_MODEL` and `HSPICE`. The model is read locally and is not committed to GitHub. Raw simulation artifacts go to `run_artifacts/`; CSV/JSON files provide compact results suitable for public inspection. If the license cannot be obtained or the model is missing, the script fails rather than reporting an unexecuted simulation as successful.

## Comparison with the existing answer

The review covered the three-page report, pre-layout `.sp`, test program, and PEX in the user-supplied **HW4 student archive 111501026**. Its 4T XNOR/TG/mux architecture was considered as a candidate, while interfaces and shared complementary signals were organized independently and verified under identical conditions. The selected minimum-size 64T candidate has better energy, area, and power-delay product within the six-candidate comparison documented in HW3. A global optimum is not claimed. Archive provenance is recorded in the repository's source documentation.

The existing report reverses its pre/post labels. Its original testbench also includes both pre-layout and post-layout DUTs simultaneously, so a direct `avg power` measurement combines their power. This delivery instantiates one DUT and does not reuse another person's layout area, PEX, or reported energy values. The older circuit also passed 512 DC input cases; the new netlist's 512-case transient check is a separate verification, and the two are not conflated.
