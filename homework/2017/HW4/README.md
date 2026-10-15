# 2017 HW4

Both original questions are completed as pre-layout `.sp` circuits, actual HSPICE data, and a standalone English `solution.tex`/rendered PDF.

- `mirror_full_adder.sp`: original 28-transistor mirror graph, systematic stack widths, individually calibrated output pMOS. All56 directed input transitions pass112 output voltage checks;64 intended output edges are measured.
- `domino_full_adder.sp`:34-transistor full adder with stable dual-rail sum minterms, independent dynamic carry, precharge/evaluate footers, weak keepers, and storage capacitance. All8 words pass16 evaluate and 16 reset output checks. It avoids the supplied answer's falling dynamic carry-select dependency.

Balanced tr=tf is defined as maximum output 10–90% rise and 90–10% fall within 1% for each output under TT,25C,1.8 V,100 ps input/clock slew,and 1 fF output loads. Saved results: mirror S55.403/54.956 ps,Cout47.484/47.467 ps; domino S51.086/51.597 ps,Cout47.557/47.792 ps. Static data-to-output worst delay and domino clock-to-output evaluation delay use different triggers, detailed in the report.

Run `python reproduce.py --model D:/cic018.l --work PATH --no-calibrate` to verify saved sizes, optionally `--hspice PATH`. Omit `--no-calibrate` for automatic balancing. Netlist defaults, sizes JSONs, and testbench parameters agree. `results/` holds actual measurements; raw listings remain in `--work`. The process model is not redistributed. No layout is requested in the original 2017 prompt.

See `../SOURCES.md` for references and corrections.
