* 2023 HW2 Q3: exact stated constant-on-resistance abstraction
.option post=0 measform=3 numdgt=10 measdgt=10
.param VSUP=1.8 RN=1k RP=9k
VSUPPLY vdd 0 'VSUP'
RP00 vdd o00 'RP'
RP01 vdd o01 'RP'
RN01 o01 0 'RN'
RP10 vdd o10 'RP'
RN10 o10 0 'RN'
RP11 vdd o11 'RP'
RN11A o11 0 'RN'
RN11B o11 0 'RN'
.tran 1p 1p
.measure tran v00 FIND V(o00) AT=1p
.measure tran v01 FIND V(o01) AT=1p
.measure tran v10 FIND V(o10) AT=1p
.measure tran v11 FIND V(o11) AT=1p
.end
