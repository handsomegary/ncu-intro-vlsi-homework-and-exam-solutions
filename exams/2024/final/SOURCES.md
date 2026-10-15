# Source review and correction decisions

Source: local2024 archive, `113學年度第一學期超大型積體電路導論期末考 Li.pdf`, seven pages. Pages1–2 are original exam photographs; page3 is a separate partial Q1 handwritten set; pages4–7 are a full matching handwritten set. All were reviewed. Only original prompt pages are redistributed. The original photographs include incidental writing; the clean reconstruction omits annotations but preserves printed questions, 110-point allocation, complement bars and circuit connections. Extraction fingerprints are in [sources.json](sources.json).

Independent derivation precedes comparison with student work. Clear errors are repaired directly. Two genuine original-model conflicts were submitted to the user, who explicitly chose parallel literal and classroom interpretations for both Q4 and Q6. Neither the feedback capacitance nor the sign of clock skew is silently altered.

| Part | Independent conclusion and student correction |
|---|---|
| Q1 | Correct physical mechanisms; DPL full-expression complement verified for all8 words. Complementary inputs are explicit. |
| Q2 | Multioutput domino uses three separate dynamic nodes sharing an evaluation footer, with earlier carries driving gates.128 arbitrary inputs pass without an unstated propagate/generate exclusion. |
| Q3 | Original middle pMOS is a clocked precharge device and shares the barred clock with its footer; Y-bar is forced high during left-gate evaluation. The static repair rewires its pMOS gate and removes its footer. The student's clock-change/input-inverter repair is valid with the explicitly complemented output. ABC=101 is a legitimate discharge, not sharing-only. |
| Q4 | Original C is N1 gate capacitance. Fixed external-C answer is identified as a classroom convention; literal feedback gate load makes3RC infeasible. Auxiliary series current uses a sum of resistances. |
| Q5 | Four rail-tied isolation devices omitted by the student are part of the physical extraction. Uncontacted metal/poly crossings remain insulated. |
| Q6 | Original NAND/NAND/NOR path yields constant Y1, XOR/XOR path yields parity. Clock skew has two approved readings. Original physical paths remain in settling analysis; optimized NP circuit is separately verified. |

Technical references appear directly in the solution: TI latchup documentation, Synopsys aging discussion and MIT6.374 dynamic-logic exercises. They support mechanisms; all circuit equations follow this original exam. No instructor answer key, unstated simulation measurement or process-specific numeric result is asserted.
