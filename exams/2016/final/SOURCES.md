# Source provenance and independent solution

Printed Fall 2016 footers establish the year. Complete Q1-Q8 appear on pages 3-1 through 3-3 and total 120 points. Native question views and enlarged circuit/contact details were read visually because text extraction did not reliably capture them.

No matching supplied student answer was found. All answers were derived from the original. A second independent audit checked Q5–Q6 timing and Q4's 24 physical MOS. The significant correction during that audit was that Q4b's third column is driven by the first inverter OUTPUT, not its input a; the output is therefore a·bar(b)·bar(c). The original Q4a final gate/output self-connection was independently confirmed and retained.

Conceptual primary sources inspected:

- [Li, NCU Chapter3](https://www.ee.ncu.edu.tw/jfli/public_html/VLSI/lecture/ch03.pdf), slides 31–36: latchup and guard rings.
- [Li, NCU Chapter6](https://www.ee.ncu.edu.tw/jfli/public_html/VLSI/lecture/ch06.pdf), slides 13–18,29–33: dynamic/domino retention/cascade limitations, fully differential and split-level load topology. DSL controls the pMOS loads from opposite INTERNAL low-swing nodes.
- [Shivakumar et al., DSN 2002](https://users.cs.utah.edu/~rajeev/cs7810/papers/shivakumar02.pdf), *Modeling the effect of technology trends on the soft error rate of combinational logic*: masking and scaling trends. Its conclusions do not justify a universal assertion that electrical masking always vanishes with scaling.

Q1 uses both literal per-node balance and a clearly labelled extra common-time design. Q2 retains the unresolved upper trip; no student noise-peak inference is adopted. Q3 gives a sizing family and one balanced conducting-path solution. Q5 reports both skew directions and the extra positive-skew hold repairs. Q6 is a resistor-divider/writeability approximation, not a simulated transient. No process model is included.
