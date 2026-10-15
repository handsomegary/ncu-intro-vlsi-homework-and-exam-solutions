# Contact audit, 2013 final Q6

The six poly crossings in each p/n strip are counted before functional reduction. Black contact squares, rather than visual proximity, determine connections. The 2012 final Figure 5 comparison is used solely to clarify the same figure. It does not supply missing numeric premises for 2013.

(a) The literal 12-MOS table contains two TG pairs, three ordinary inverter pairs and a final self-connected pair. The middle inverter output r feeds a TG to v; its gate is X. The right ordinary inverter has gate v and output X. P6/N6 have both gate and one channel terminal at X. At a binary-low X P6 conducts toward VDD; at a binary-high X N6 conducts toward VSS. These devices therefore cannot be silently replaced by a normal output inverter or omitted to claim an ordinary latch. Q6 asks for extraction, so show the literal schematic and identify the nonstandard connection. Source-drain directions are not inferred from horizontal order.

(b) Central gates a,b,c form a three-series-pMOS pullup and three-parallel-nMOS pulldown. Poly columns 1,2,6 are split and tied to VDD (p) / VSS (n), so all six corresponding MOS are OFF. Their floating active-strip stubs are retained as p0,p1,p6 / n0,n1,n6. This is not the input-inverter variant in 2016 Q4b. The full 12-MOS switch graph independently exhausts all 8 cases and gives Z=NOT(a OR b OR c), with exactly one rail reachable in every case.

Vector redraws normalize geometry while retaining every crossing, contact and net. Small junction dots mark contacts; crossing wires with no dot are not connected. The labelled solution schematics pair each drawn transistor with its gate and two channel nets, avoiding an implied gate-terminal repair.
