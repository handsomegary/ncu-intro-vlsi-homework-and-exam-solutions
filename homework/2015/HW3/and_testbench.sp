* 2015 reproducible schematic simulation
.protect
.lib 'D:/cic018.l' TT
.unprotect
.option post=0 lis_new=1 ingold=2 numdgt=10 measdgt=10 measform=3 delmax=1p
.temp 25
.include 'and2.sp'
VDD dd 0 1.8
Va0 a0 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb0 b0 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X0 a0 b0 f0 z0 dd 0 and2
.measure tran d0f TRIG V(a0) VAL=.9 RISE=1 TD=1.9n TARG V(f0) VAL=.9 FALL=1 TD=1.9n
.measure tran q0f FIND V(f0) AT=4.9n
.measure tran d0z TRIG V(a0) VAL=.9 RISE=1 TD=1.9n TARG V(z0) VAL=.9 RISE=1 TD=1.9n
.measure tran q0z FIND V(z0) AT=4.9n
Va1 a1 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb1 b1 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X1 a1 b1 f1 z1 dd 0 and2
.measure tran d1f TRIG V(a1) VAL=.9 RISE=1 TD=1.9n TARG V(f1) VAL=.9 FALL=1 TD=1.9n
.measure tran q1f FIND V(f1) AT=4.9n
.measure tran d1z TRIG V(a1) VAL=.9 RISE=1 TD=1.9n TARG V(z1) VAL=.9 RISE=1 TD=1.9n
.measure tran q1z FIND V(z1) AT=4.9n
Va2 a2 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb2 b2 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X2 a2 b2 f2 z2 dd 0 and2
.measure tran d2f TRIG V(b2) VAL=.9 RISE=1 TD=1.9n TARG V(f2) VAL=.9 FALL=1 TD=1.9n
.measure tran q2f FIND V(f2) AT=4.9n
.measure tran d2z TRIG V(b2) VAL=.9 RISE=1 TD=1.9n TARG V(z2) VAL=.9 RISE=1 TD=1.9n
.measure tran q2z FIND V(z2) AT=4.9n
Va3 a3 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb3 b3 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X3 a3 b3 f3 z3 dd 0 and2
.measure tran d3f TRIG V(a3) VAL=.9 FALL=1 TD=1.9n TARG V(f3) VAL=.9 RISE=1 TD=1.9n
.measure tran q3f FIND V(f3) AT=4.9n
.measure tran d3z TRIG V(a3) VAL=.9 FALL=1 TD=1.9n TARG V(z3) VAL=.9 FALL=1 TD=1.9n
.measure tran q3z FIND V(z3) AT=4.9n
Va4 a4 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb4 b4 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X4 a4 b4 f4 z4 dd 0 and2
.measure tran d4f TRIG V(a4) VAL=.9 FALL=1 TD=1.9n TARG V(f4) VAL=.9 RISE=1 TD=1.9n
.measure tran q4f FIND V(f4) AT=4.9n
.measure tran d4z TRIG V(a4) VAL=.9 FALL=1 TD=1.9n TARG V(z4) VAL=.9 FALL=1 TD=1.9n
.measure tran q4z FIND V(z4) AT=4.9n
Va5 a5 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb5 b5 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X5 a5 b5 f5 z5 dd 0 and2
.measure tran d5f TRIG V(b5) VAL=.9 FALL=1 TD=1.9n TARG V(f5) VAL=.9 RISE=1 TD=1.9n
.measure tran q5f FIND V(f5) AT=4.9n
.measure tran d5z TRIG V(b5) VAL=.9 FALL=1 TD=1.9n TARG V(z5) VAL=.9 FALL=1 TD=1.9n
.measure tran q5z FIND V(z5) AT=4.9n
.tran 1p 5n
.print tran V(a0) V(b0) V(f0) V(z0) V(a1) V(b1) V(f1) V(z1) V(a2) V(b2) V(f2) V(z2) V(a3) V(b3) V(f3) V(z3) V(a4) V(b4) V(f4) V(z4) V(a5) V(b5) V(f5) V(z5)
.end
