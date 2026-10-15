# Reference review: 2023 HW1

The original prompt and all three local submitted answers were rendered and read
visually. This was necessary because two submissions are image-only PDFs and PDF
text extraction loses the overbar in Q1(a). The final derivations and explicit
transistor graph were solved independently, then compared with these references.
Original student submissions are not republished here; source hashes are in
[sources.json](sources.json).

| Local supplied answer | Reviewed pages | Findings and integration |
| --- | --- | --- |
| `109501570_簡肇亨_hw1.pdf` | 1-2 | Q1(a) correctly uses the printed AOI polarity. Q1(b) is a valid 12-transistor realization. Its encoded two-level TG multiplexer implements the rotation, and Q3 correctly identifies XOR with complement-generating inverters. The final version keeps the AOI interpretation, uses a factored 10-transistor minority gate, and chooses direct control of the rotation bank. |
| `110501512_廖柏森_hw1.pdf` | 1-4; answer on 2-4 | Q1(a) has the correct AOI network. Q1(b)'s 5-NMOS/5-PMOS topology is valid; its intermediate written complement notation is ambiguous, so the final algebra is freshly derived from the printed minority function. Its direct TG rotation is the clearest and least complex of the three supplied rotation topologies. Q3's XOR core is correct but relies on available complements; the final version explicitly supplies two CMOS inverters. |
| `110501558_林意盛_hw1.pdf` | 1-2 | Q1(a) shows an added output inverter and states the positive AO function; this differs from the printed AOI target. That inverter is omitted in the final solution. The minority-function circuit and XOR idea agree with the requested functions. The final circuits factor the minority network and explicitly generate complemented XOR inputs. Its decoded rotation idea is unnecessary under the four specified valid control words. |

Final choices:

- Q1(a): `NOT(w(x+y)+yz)`, five NMOS and five PMOS, with no output inverter.
- Q1(b): `NOT(x(y+z)+yz)`, five NMOS and five PMOS, requiring true input wires only.
- Q2: 16 full-swing CMOS transmission gates and four shared control inverters,
  totaling 40 MOSFETs. The data index is `(j-k) mod 4`, avoiding reversal of rotation direction.
- Q3: XOR with an eight-transistor static CMOS core and two input inverters,
  totaling 12 MOSFETs.

No reported simulation numbers from the submissions are reused. HW1 asks for
logic designs; the evidence is an exhaustive ideal-switch connectivity check
against the original functions and table. The original prompt is copied without
modification to [2023/assignments/homework1.pdf](../assignments/homework1.pdf).
