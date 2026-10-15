# 2024 HW3: 4-bit multiplexer-based adder

## Assignment requirements

Implement the 4-bit serial-parallel multiplexer-based adder in Figure 1 of [homework3.pdf](../assignments/homework3.pdf) and verify it with HSPICE. The upper row computes each bit's XNOR in parallel, carry propagates through four cascaded multiplexers, and the lower XNOR row produces the sums. Here, serial-parallel describes a combinational architecture; there is no clock or cycle-by-cycle serial input.

The assignment and [instructor clarifications](../assignments/hw3_clarifications.en.md) specify CIC018 TT, 1.8 V, minimum W = 0.47 um, the instructor's testbench and signal names, and CIN = 0. Apply `(1,5), (15,13), (11,9), (4,8), (3,7), (12,14), (2,15), (6,10)` in order, then measure average power, worst-case delay, and `sum(WL)`. The additional grading metrics are area and energy over 9 ns. This solution uses L = 0.18 um and W = 0.47 um for every MOS device.

## Final design and source integration

Each bit uses a 4T upper XNOR, two CMOS inverters, and sum/carry networks that each contain two transmission gates: 16T per bit and **64T** overall. Let `e_i = X_i XNOR Y_i`. Then `S_i = e_i XNOR C_i` and `C_(i+1) = e_i ? Y_i : C_i`. The lower XNOR specifically uses `C_i` and its complement as data, and `e_i` and its complement as selects. This arrangement allows the external outputs to approach the supply rails despite the weak high level of the upper XNOR.

The review covered user-supplied student archive **111501026 for 2024 HW3** (88T, W = 0.47 um, L = 0.24 um) and the schematic `four_bit_multbased_adder.sp` in the same student's **HW4 archive** (64T). The corresponding logic was reconstructed, reproducible verification scripts were written independently, and the candidates were compared under identical PWL inputs, models, and measurement settings. Previously reported numbers are not presented as new measurements. Archive provenance is recorded in the repository's source documentation.

The public [CLA_cmos.sp in NCU_VLSI_Design_2023_HW](https://github.com/dOwOb1212/NCU_VLSI_Design_2023_HW/blob/main/hw1/CLA_cmos.sp) was also inspected. Despite the CLA filename, its carry still passes through a mux at each bit. It is an 8-bit design, some widths of 0.25/0.45 um fall below the 2024 minimum, and its input sequence differs. It was used only for an architecture cross-check.

The 64T design's internal upper-XNOR `e` nodes can exhibit NMOS threshold loss; not all internal nodes are claimed to have full swing. At the required TT/1.8 V condition, all five external outputs passed the specified sequence and 512 electrical cases. No certification across process corners, low voltages, or output loads is claimed.

## Measured results

HSPICE S-2021.09 win64, TT, 25 C, 1.8 V, without added output capacitance or layout parasitics. **The two measurement settings must be kept separate:**

| Setting | Average total power | Average VDD supply power | Total energy over 9 ns |
|---|---:|---:|---:|
| Original instructor `.tran 0.1ns 9n`, automatic DELMAX | 69.002216 uW | 37.998479 uW | 621.019943 fJ |
| Refined `.tran 1p 9n`, `.option delmax=1p` | 69.558498 uW | 37.432840 uW | 626.026482 fJ |

In the instructor's `.meas tran pwr avg power`, **POWER** is the net power delivered to the entire circuit by all independent sources, including input PWL sources. TG circuits also receive energy through their data inputs, so this differs from measuring only `-V(vdd) * I(vvdd)`. The grading energy uses total POWER multiplied by 9 ns; the smaller supply-only power is not substituted.

With the refined settings, the largest causal 50% delay in the specified sequence is **152.910320 ps**, at the eighth transition, `(2,15) -> (6,10)`, on the S0 falling edge. The input 50% point is 7.950 ns, and the final output 50% crossing is 8.102910320 ns. This is the worst case for the specified sequence, rather than a global worst case over every possible transition.

`sum(WL) = 64 * 0.47 * 0.18 = 5.4144 um^2`. This is the instructor's transistor gate-area proxy, not physical layout area.

| Candidate, identical refined settings | MOS count | sum(WL), um^2 | Total energy, fJ | Delay, ps | Delay * power, fJ |
|---|---:|---:|---:|---:|---:|
| Equivalent original HW3 88T | 88 | 9.9264 | 1005.327 | 247.239 | 27.617 |
| Full-swing 80T, minimum sizes | 80 | 6.7680 | 824.288 | 137.009 | 12.548 |
| 80T, inverter PMOS W = 0.94 um | 80 | 8.1216 | 947.745 | 133.867 | 14.097 |
| 80T, TG W = 0.70 um | 80 | 8.7552 | 1055.585 | 161.400 | 18.930 |
| **64T, minimum sizes, selected** | **64** | **5.4144** | **626.026** | **152.910** | **10.636** |
| 64T, PMOS W = 0.70 um | 64 | 6.0768 | 676.239 | 149.882 | 11.262 |

All six candidates passed the eight specified vectors. The selected 64T candidate has the lowest area, energy, and delay-times-power among this finite set. The 80T candidate is faster but uses more area and energy. A global optimum is not claimed.

## Verification and statistics

For the eight input pairs, `{COUT,S3,S2,S1,S0}` is respectively `00110, 11100, 10100, 01100, 01010, 11010, 10001, 10000`: **8/8 correct**. Samples at 1.8, 2.8, ..., 8.8 ns, 0.8 ns after each vector update, give a maximum low level of 0.00396849 V and a minimum high level of 1.7910275 V.

An additional real HSPICE transistor transient simulation covers X and Y from 0 through 15 and CIN = 0/1: **512/512 cases passed**. Cases are spaced 2 ns apart, input ramps last 0.1 ns, and samples are taken 1.8 ns after each case starts. All five external outputs satisfy low <= 0.2 V and high >= 1.6 V. The maximum low is 0.002939216 V, and the minimum high is 1.79601867 V. This checks transient samples for all steady input combinations; it does not enumerate all `512^2` transitions.

Delay uses the last 0.9 V crossing in the final output direction for each corresponding vector change, avoiding a glitch's first crossing as the apparent settled result. The specified sequence still contains glitches: 12 extra 50% crossings in total. The slowest sampled bound for all outputs to enter their correct 0.2/1.6 V bands is 394 ps, measured from that transition's input 50% point. Transient data is retained as CSV, so no GUI waveform screenshot is required.

## Files and reproduction

| File | Purpose |
|---|---|
| `../assignments/homework3.pdf` | Original assignment |
| `four_bit_multbased_adder.sp` | Final 64T transistor circuit with the instructor's subcircuit pin order |
| `testbench.sp` | Original instructor PWL inputs and `.tran 0.1ns 9n`; only the process path is changed to `D:/cic018.l` |
| `simulate.py` | Generates six candidates, refined power/delay measurements, and 512-case checks; also runs the original testbench |
| `solution.tex`, `solution.pdf` | Standalone technical report and compiled version |
| `results/candidates.csv` | Candidate dimensions, MOS counts, area, total/supply power, energy, and delay |
| `results/vectors.csv`, `results/delays.csv`, `results/settling.csv` | Specified-vector voltages, corresponding crossings, and glitch/settling statistics |
| `results/exhaustive_512.csv` | Five actual output voltages and correctness for every input case |
| `results/waveform.csv` | Refined output voltages and VDD current with 1 ps time resolution |
| `results/summary.json`, `results/instructor_exact.json` | Machine-readable summary and original-testbench results |

Run PowerShell from this directory. You must provide your own licensed HSPICE installation and authorized CIC018 model:

```powershell
$env:CIC018_MODEL = 'D:\cic018.l'
$env:HSPICE = 'C:\synopsys\Hspice_S-2021.09\WIN64\hspice.com'
python .\simulate.py --work .\.simulation --results .\results
```

Use `--model` and `--hspice` to specify other installation paths directly. Generated model references use the selected path. When running the original testbench manually, adjust its `.lib` path yourself:

```powershell
& $env:HSPICE -i .\testbench.sp -o .\.simulation\original
```

Create `.simulation` before the manual command. Process models, original student submissions, raw `.lis`/`.tr0` files, and license logs are excluded from the public repository. Public statistics come from the present simulations. Keep this explanation alongside the source so the assignment conditions and measurement definitions remain visible on GitHub.
