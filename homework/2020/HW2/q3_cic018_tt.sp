* 2020 HW2 Q3 supplementary CIC018 TT experiment (BSIM3)
.protect
.lib 'D:/cic018.l' TT
.unprotect
.option measform=3 numdgt=10 measdgt=10 ingold=2
.temp 25
.param NR=4.5 WP=0.5u
.subckt pseudo_nor a b y dd
MP y 0 dd dd P_18 W=WP L=0.18u
MN0 y a 0 0 N_18 W='NR*WP' L=0.18u
MN1 y b 0 0 N_18 W='NR*WP' L=0.18u
.ends pseudo_nor
VH h 0 1.8
VDD00 dd00 0 1.8
VDD01 dd01 0 1.8
VDD10 dd10 0 1.8
VDD11 dd11 0 1.8
X00 0 0 o00 dd00 pseudo_nor
X01 0 h o01 dd01 pseudo_nor
X10 h 0 o10 dd10 pseudo_nor
X11 h h o11 dd11 pseudo_nor
.data SIZES NR
1
4.5
5
.enddata
.tran 1p 1p SWEEP DATA=SIZES
.measure tran ratio PARAM='NR'
.measure tran v00 FIND V(o00) AT=1p
.measure tran idd00 FIND PAR('-I(VDD00)') AT=1p
.measure tran v01 FIND V(o01) AT=1p
.measure tran idd01 FIND PAR('-I(VDD01)') AT=1p
.measure tran v10 FIND V(o10) AT=1p
.measure tran idd10 FIND PAR('-I(VDD10)') AT=1p
.measure tran v11 FIND V(o11) AT=1p
.measure tran idd11 FIND PAR('-I(VDD11)') AT=1p
.end
