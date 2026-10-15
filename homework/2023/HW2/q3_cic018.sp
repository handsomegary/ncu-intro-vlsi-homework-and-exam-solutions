* 2023 HW2 Q3: supplementary BSIM3 numerical check, NOT the resistor model
* Keep D:/cic018.l local; do not redistribute the process library.
.protect
.lib 'D:/cic018.l' TT
.unprotect
.option post=0 measform=3 numdgt=10 measdgt=10
.temp 25
.param VSUP=1.8 WP=0.5u LP=0.18u LN=0.18u NR=4.5
.subckt PNOR a b y vdd
MP y 0 vdd vdd P_18 W='WP' L='LP'
+ AD='WP*0.18u' AS='WP*0.18u' PD='2*(WP+0.18u)' PS='2*(WP+0.18u)'
MN_A y a 0 0 N_18 W='NR*WP' L='LN'
+ AD='NR*WP*0.18u' AS='NR*WP*0.18u'
+ PD='2*(NR*WP+0.18u)' PS='2*(NR*WP+0.18u)'
MN_B y b 0 0 N_18 W='NR*WP' L='LN'
+ AD='NR*WP*0.18u' AS='NR*WP*0.18u'
+ PD='2*(NR*WP+0.18u)' PS='2*(NR*WP+0.18u)'
.ends
V00 dd00 0 'VSUP'
V01 dd01 0 'VSUP'
V10 dd10 0 'VSUP'
V11 dd11 0 'VSUP'
VH high 0 'VSUP'
X00 0 0 o00 dd00 PNOR
X01 0 high o01 dd01 PNOR
X10 high 0 o10 dd10 PNOR
X11 high high o11 dd11 PNOR
.data SIZES NR
1
2
2.25
3
4.5
4
6
8
.enddata
.tran 1p 1p SWEEP DATA=SIZES
.measure tran ratio PARAM='NR'
.measure tran v00 FIND V(o00) AT=1p
.measure tran v01 FIND V(o01) AT=1p
.measure tran v10 FIND V(o10) AT=1p
.measure tran v11 FIND V(o11) AT=1p
.measure tran idd00 FIND PAR('-I(V00)') AT=1p
.measure tran idd01 FIND PAR('-I(V01)') AT=1p
.measure tran idd10 FIND PAR('-I(V10)') AT=1p
.measure tran idd11 FIND PAR('-I(V11)') AT=1p
.measure tran p01 PARAM='VSUP*idd01'
.end
