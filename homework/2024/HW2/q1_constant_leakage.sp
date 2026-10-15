* HW2 Q1: ideal constant-leakage retention, illustrative numbers only
* This is the analytical storage-node abstraction, NOT the full BL circuit.
.option post=0 measform=3 numdgt=10 measdgt=10
.param VSUP=1.8 VTH=0.45 CS=20f ILEAK=1p
CSTORE q 0 'CS'
ILEAKAGE q 0 DC 'ILEAK'
.ic V(q)='VSUP-VTH'
.tran 100n 15m UIC
.measure tran v_initial FIND V(q) AT=0
.measure tran retention WHEN V(q)='0.4*VSUP' FALL=1
.measure tran v_at_12m6 FIND V(q) AT=12.6m
.measure tran t_expected PARAM='CS*(0.6*VSUP-VTH)/ILEAK'
.end
