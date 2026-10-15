* 2020 HW3 00->11, controlled 50-percent delays
.protect
.lib 'D:/cic018.l' TT
.unprotect
.include 'and2.sp'
.option post=0 measform=3 numdgt=10 measdgt=10 ingold=2 lis_new=1 delmax=1p
.temp 25
VDD vdd 0 1.8
VSS vss 0 0
VA a vss PWL(0 0.0 2n 0.0 2.020000000000e-09 1.8 5n 1.8)
VB b vss PWL(0 0.0 2n 0.0 2.020000000000e-09 1.8 5n 1.8)
XAND a b f z vdd vss and2
CL z vss 1f
.tran 1p 5n
.print tran V(a) V(b) V(f) V(z)
.measure tran delay_f TRIG V(a) VAL=0.9 RISE=1 TD=1.9n TARG V(f) VAL=0.9 FALL=1 TD=1.9n
.measure tran before_f FIND V(f) AT=1.9n
.measure tran after_f FIND V(f) AT=4.9n
.measure tran delay_z TRIG V(a) VAL=0.9 RISE=1 TD=1.9n TARG V(z) VAL=0.9 RISE=1 TD=1.9n
.measure tran before_z FIND V(z) AT=1.9n
.measure tran after_z FIND V(z) AT=4.9n
.end
