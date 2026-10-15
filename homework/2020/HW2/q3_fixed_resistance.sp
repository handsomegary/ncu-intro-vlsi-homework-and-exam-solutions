* 2020 HW2 Q3 assignment fixed-resistance model, not BSIM MOSFETs
.option measform=3 numdgt=10 measdgt=10 ingold=2
.param NR=4.5 R0=1000 VSUP=1.8
VDD vdd 0 'VSUP'
RP00 vdd o00 '2*R0'
RP01 vdd o01 '2*R0'
RP10 vdd o10 '2*R0'
RP11 vdd o11 '2*R0'
RLEAK o00 0 1e15
RN01 o01 0 'R0/NR'
RN10 o10 0 'R0/NR'
RN11A o11 0 'R0/NR'
RN11B o11 0 'R0/NR'
.data SIZES NR
1
4.5
5
.enddata
.tran 1p 1p SWEEP DATA=SIZES
.measure tran ratio PARAM='NR'
.measure tran v00 FIND V(o00) AT=1p
.measure tran v01 FIND V(o01) AT=1p
.measure tran v10 FIND V(o10) AT=1p
.measure tran v11 FIND V(o11) AT=1p
.end
