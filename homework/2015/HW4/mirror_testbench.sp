* 2015 reproducible schematic simulation
.protect
.lib 'D:/cic018.l' TT
.unprotect
.option post=0 lis_new=1 ingold=2 numdgt=10 measdgt=10 measform=3 delmax=0.2p
.temp 25
.include 'mirror.sp'
VDD dd 0 1.8
Va0 a0 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vb0 b0 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vci0 ci0 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X0 a0 b0 ci0 co0 s0 dd 0 mirror
CC0 co0 0 1f
CS0 s0 0 1f
.measure tran q0co FIND V(co0) AT=4.9n
.measure tran q0s FIND V(s0) AT=4.9n
.measure tran d0s TRIG V(ci0) VAL=.9 RISE=1 TD=1.9n TARG V(s0) VAL=.9 RISE=1 TD=1.9n
.measure tran t0s TRIG V(s0) VAL=0.18 RISE=1 TD=1.9n TARG V(s0) VAL=1.62 RISE=1 TD=1.9n
Va1 a1 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vb1 b1 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci1 ci1 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
X1 a1 b1 ci1 co1 s1 dd 0 mirror
CC1 co1 0 1f
CS1 s1 0 1f
.measure tran q1co FIND V(co1) AT=4.9n
.measure tran q1s FIND V(s1) AT=4.9n
.measure tran d1s TRIG V(b1) VAL=.9 RISE=1 TD=1.9n TARG V(s1) VAL=.9 RISE=1 TD=1.9n
.measure tran t1s TRIG V(s1) VAL=0.18 RISE=1 TD=1.9n TARG V(s1) VAL=1.62 RISE=1 TD=1.9n
Va2 a2 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vb2 b2 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci2 ci2 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X2 a2 b2 ci2 co2 s2 dd 0 mirror
CC2 co2 0 1f
CS2 s2 0 1f
.measure tran q2co FIND V(co2) AT=4.9n
.measure tran d2co TRIG V(b2) VAL=.9 RISE=1 TD=1.9n TARG V(co2) VAL=.9 RISE=1 TD=1.9n
.measure tran t2co TRIG V(co2) VAL=0.18 RISE=1 TD=1.9n TARG V(co2) VAL=1.62 RISE=1 TD=1.9n
.measure tran q2s FIND V(s2) AT=4.9n
Va3 a3 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb3 b3 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vci3 ci3 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
X3 a3 b3 ci3 co3 s3 dd 0 mirror
CC3 co3 0 1f
CS3 s3 0 1f
.measure tran q3co FIND V(co3) AT=4.9n
.measure tran q3s FIND V(s3) AT=4.9n
.measure tran d3s TRIG V(a3) VAL=.9 RISE=1 TD=1.9n TARG V(s3) VAL=.9 RISE=1 TD=1.9n
.measure tran t3s TRIG V(s3) VAL=0.18 RISE=1 TD=1.9n TARG V(s3) VAL=1.62 RISE=1 TD=1.9n
Va4 a4 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb4 b4 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vci4 ci4 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X4 a4 b4 ci4 co4 s4 dd 0 mirror
CC4 co4 0 1f
CS4 s4 0 1f
.measure tran q4co FIND V(co4) AT=4.9n
.measure tran d4co TRIG V(a4) VAL=.9 RISE=1 TD=1.9n TARG V(co4) VAL=.9 RISE=1 TD=1.9n
.measure tran t4co TRIG V(co4) VAL=0.18 RISE=1 TD=1.9n TARG V(co4) VAL=1.62 RISE=1 TD=1.9n
.measure tran q4s FIND V(s4) AT=4.9n
Va5 a5 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb5 b5 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci5 ci5 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
X5 a5 b5 ci5 co5 s5 dd 0 mirror
CC5 co5 0 1f
CS5 s5 0 1f
.measure tran q5co FIND V(co5) AT=4.9n
.measure tran d5co TRIG V(a5) VAL=.9 RISE=1 TD=1.9n TARG V(co5) VAL=.9 RISE=1 TD=1.9n
.measure tran t5co TRIG V(co5) VAL=0.18 RISE=1 TD=1.9n TARG V(co5) VAL=1.62 RISE=1 TD=1.9n
.measure tran q5s FIND V(s5) AT=4.9n
Va6 a6 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb6 b6 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci6 ci6 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X6 a6 b6 ci6 co6 s6 dd 0 mirror
CC6 co6 0 1f
CS6 s6 0 1f
.measure tran q6co FIND V(co6) AT=4.9n
.measure tran d6co TRIG V(a6) VAL=.9 RISE=1 TD=1.9n TARG V(co6) VAL=.9 RISE=1 TD=1.9n
.measure tran t6co TRIG V(co6) VAL=0.18 RISE=1 TD=1.9n TARG V(co6) VAL=1.62 RISE=1 TD=1.9n
.measure tran q6s FIND V(s6) AT=4.9n
.measure tran d6s TRIG V(a6) VAL=.9 RISE=1 TD=1.9n TARG V(s6) VAL=.9 RISE=1 TD=1.9n
.measure tran t6s TRIG V(s6) VAL=0.18 RISE=1 TD=1.9n TARG V(s6) VAL=1.62 RISE=1 TD=1.9n
Va7 a7 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vb7 b7 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vci7 ci7 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X7 a7 b7 ci7 co7 s7 dd 0 mirror
CC7 co7 0 1f
CS7 s7 0 1f
.measure tran q7co FIND V(co7) AT=4.9n
.measure tran q7s FIND V(s7) AT=4.9n
.measure tran d7s TRIG V(ci7) VAL=.9 FALL=1 TD=1.9n TARG V(s7) VAL=.9 FALL=1 TD=1.9n
.measure tran t7s TRIG V(s7) VAL=1.62 FALL=1 TD=1.9n TARG V(s7) VAL=0.18 FALL=1 TD=1.9n
Va8 a8 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vb8 b8 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci8 ci8 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X8 a8 b8 ci8 co8 s8 dd 0 mirror
CC8 co8 0 1f
CS8 s8 0 1f
.measure tran q8co FIND V(co8) AT=4.9n
.measure tran q8s FIND V(s8) AT=4.9n
Va9 a9 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vb9 b9 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci9 ci9 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X9 a9 b9 ci9 co9 s9 dd 0 mirror
CC9 co9 0 1f
CS9 s9 0 1f
.measure tran q9co FIND V(co9) AT=4.9n
.measure tran d9co TRIG V(b9) VAL=.9 RISE=1 TD=1.9n TARG V(co9) VAL=.9 RISE=1 TD=1.9n
.measure tran t9co TRIG V(co9) VAL=0.18 RISE=1 TD=1.9n TARG V(co9) VAL=1.62 RISE=1 TD=1.9n
.measure tran q9s FIND V(s9) AT=4.9n
.measure tran d9s TRIG V(b9) VAL=.9 RISE=1 TD=1.9n TARG V(s9) VAL=.9 FALL=1 TD=1.9n
.measure tran t9s TRIG V(s9) VAL=1.62 FALL=1 TD=1.9n TARG V(s9) VAL=0.18 FALL=1 TD=1.9n
Va10 a10 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb10 b10 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vci10 ci10 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X10 a10 b10 ci10 co10 s10 dd 0 mirror
CC10 co10 0 1f
CS10 s10 0 1f
.measure tran q10co FIND V(co10) AT=4.9n
.measure tran q10s FIND V(s10) AT=4.9n
Va11 a11 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb11 b11 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vci11 ci11 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X11 a11 b11 ci11 co11 s11 dd 0 mirror
CC11 co11 0 1f
CS11 s11 0 1f
.measure tran q11co FIND V(co11) AT=4.9n
.measure tran d11co TRIG V(a11) VAL=.9 RISE=1 TD=1.9n TARG V(co11) VAL=.9 RISE=1 TD=1.9n
.measure tran t11co TRIG V(co11) VAL=0.18 RISE=1 TD=1.9n TARG V(co11) VAL=1.62 RISE=1 TD=1.9n
.measure tran q11s FIND V(s11) AT=4.9n
.measure tran d11s TRIG V(a11) VAL=.9 RISE=1 TD=1.9n TARG V(s11) VAL=.9 FALL=1 TD=1.9n
.measure tran t11s TRIG V(s11) VAL=1.62 FALL=1 TD=1.9n TARG V(s11) VAL=0.18 FALL=1 TD=1.9n
Va12 a12 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb12 b12 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci12 ci12 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X12 a12 b12 ci12 co12 s12 dd 0 mirror
CC12 co12 0 1f
CS12 s12 0 1f
.measure tran q12co FIND V(co12) AT=4.9n
.measure tran d12co TRIG V(a12) VAL=.9 RISE=1 TD=1.9n TARG V(co12) VAL=.9 RISE=1 TD=1.9n
.measure tran t12co TRIG V(co12) VAL=0.18 RISE=1 TD=1.9n TARG V(co12) VAL=1.62 RISE=1 TD=1.9n
.measure tran q12s FIND V(s12) AT=4.9n
.measure tran d12s TRIG V(a12) VAL=.9 RISE=1 TD=1.9n TARG V(s12) VAL=.9 FALL=1 TD=1.9n
.measure tran t12s TRIG V(s12) VAL=1.62 FALL=1 TD=1.9n TARG V(s12) VAL=0.18 FALL=1 TD=1.9n
Va13 a13 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb13 b13 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci13 ci13 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X13 a13 b13 ci13 co13 s13 dd 0 mirror
CC13 co13 0 1f
CS13 s13 0 1f
.measure tran q13co FIND V(co13) AT=4.9n
.measure tran d13co TRIG V(a13) VAL=.9 RISE=1 TD=1.9n TARG V(co13) VAL=.9 RISE=1 TD=1.9n
.measure tran t13co TRIG V(co13) VAL=0.18 RISE=1 TD=1.9n TARG V(co13) VAL=1.62 RISE=1 TD=1.9n
.measure tran q13s FIND V(s13) AT=4.9n
Va14 a14 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vb14 b14 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci14 ci14 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
X14 a14 b14 ci14 co14 s14 dd 0 mirror
CC14 co14 0 1f
CS14 s14 0 1f
.measure tran q14co FIND V(co14) AT=4.9n
.measure tran q14s FIND V(s14) AT=4.9n
.measure tran d14s TRIG V(b14) VAL=.9 FALL=1 TD=1.9n TARG V(s14) VAL=.9 FALL=1 TD=1.9n
.measure tran t14s TRIG V(s14) VAL=1.62 FALL=1 TD=1.9n TARG V(s14) VAL=0.18 FALL=1 TD=1.9n
Va15 a15 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vb15 b15 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci15 ci15 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X15 a15 b15 ci15 co15 s15 dd 0 mirror
CC15 co15 0 1f
CS15 s15 0 1f
.measure tran q15co FIND V(co15) AT=4.9n
.measure tran q15s FIND V(s15) AT=4.9n
Va16 a16 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vb16 b16 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vci16 ci16 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X16 a16 b16 ci16 co16 s16 dd 0 mirror
CC16 co16 0 1f
CS16 s16 0 1f
.measure tran q16co FIND V(co16) AT=4.9n
.measure tran d16co TRIG V(ci16) VAL=.9 RISE=1 TD=1.9n TARG V(co16) VAL=.9 RISE=1 TD=1.9n
.measure tran t16co TRIG V(co16) VAL=0.18 RISE=1 TD=1.9n TARG V(co16) VAL=1.62 RISE=1 TD=1.9n
.measure tran q16s FIND V(s16) AT=4.9n
.measure tran d16s TRIG V(ci16) VAL=.9 RISE=1 TD=1.9n TARG V(s16) VAL=.9 FALL=1 TD=1.9n
.measure tran t16s TRIG V(s16) VAL=1.62 FALL=1 TD=1.9n TARG V(s16) VAL=0.18 FALL=1 TD=1.9n
Va17 a17 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb17 b17 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci17 ci17 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
X17 a17 b17 ci17 co17 s17 dd 0 mirror
CC17 co17 0 1f
CS17 s17 0 1f
.measure tran q17co FIND V(co17) AT=4.9n
.measure tran q17s FIND V(s17) AT=4.9n
Va18 a18 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb18 b18 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci18 ci18 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X18 a18 b18 ci18 co18 s18 dd 0 mirror
CC18 co18 0 1f
CS18 s18 0 1f
.measure tran q18co FIND V(co18) AT=4.9n
.measure tran d18co TRIG V(a18) VAL=.9 RISE=1 TD=1.9n TARG V(co18) VAL=.9 RISE=1 TD=1.9n
.measure tran t18co TRIG V(co18) VAL=0.18 RISE=1 TD=1.9n TARG V(co18) VAL=1.62 RISE=1 TD=1.9n
.measure tran q18s FIND V(s18) AT=4.9n
.measure tran d18s TRIG V(a18) VAL=.9 RISE=1 TD=1.9n TARG V(s18) VAL=.9 FALL=1 TD=1.9n
.measure tran t18s TRIG V(s18) VAL=1.62 FALL=1 TD=1.9n TARG V(s18) VAL=0.18 FALL=1 TD=1.9n
Va19 a19 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb19 b19 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vci19 ci19 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
X19 a19 b19 ci19 co19 s19 dd 0 mirror
CC19 co19 0 1f
CS19 s19 0 1f
.measure tran q19co FIND V(co19) AT=4.9n
.measure tran d19co TRIG V(a19) VAL=.9 RISE=1 TD=1.9n TARG V(co19) VAL=.9 RISE=1 TD=1.9n
.measure tran t19co TRIG V(co19) VAL=0.18 RISE=1 TD=1.9n TARG V(co19) VAL=1.62 RISE=1 TD=1.9n
.measure tran q19s FIND V(s19) AT=4.9n
.measure tran d19s TRIG V(a19) VAL=.9 RISE=1 TD=1.9n TARG V(s19) VAL=.9 FALL=1 TD=1.9n
.measure tran t19s TRIG V(s19) VAL=1.62 FALL=1 TD=1.9n TARG V(s19) VAL=0.18 FALL=1 TD=1.9n
Va20 a20 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb20 b20 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vci20 ci20 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X20 a20 b20 ci20 co20 s20 dd 0 mirror
CC20 co20 0 1f
CS20 s20 0 1f
.measure tran q20co FIND V(co20) AT=4.9n
.measure tran d20co TRIG V(a20) VAL=.9 RISE=1 TD=1.9n TARG V(co20) VAL=.9 RISE=1 TD=1.9n
.measure tran t20co TRIG V(co20) VAL=0.18 RISE=1 TD=1.9n TARG V(co20) VAL=1.62 RISE=1 TD=1.9n
.measure tran q20s FIND V(s20) AT=4.9n
Va21 a21 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vb21 b21 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci21 ci21 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X21 a21 b21 ci21 co21 s21 dd 0 mirror
CC21 co21 0 1f
CS21 s21 0 1f
.measure tran q21co FIND V(co21) AT=4.9n
.measure tran d21co TRIG V(b21) VAL=.9 FALL=1 TD=1.9n TARG V(co21) VAL=.9 FALL=1 TD=1.9n
.measure tran t21co TRIG V(co21) VAL=1.62 FALL=1 TD=1.9n TARG V(co21) VAL=0.18 FALL=1 TD=1.9n
.measure tran q21s FIND V(s21) AT=4.9n
Va22 a22 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vb22 b22 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci22 ci22 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X22 a22 b22 ci22 co22 s22 dd 0 mirror
CC22 co22 0 1f
CS22 s22 0 1f
.measure tran q22co FIND V(co22) AT=4.9n
.measure tran d22co TRIG V(b22) VAL=.9 FALL=1 TD=1.9n TARG V(co22) VAL=.9 FALL=1 TD=1.9n
.measure tran t22co TRIG V(co22) VAL=1.62 FALL=1 TD=1.9n TARG V(co22) VAL=0.18 FALL=1 TD=1.9n
.measure tran q22s FIND V(s22) AT=4.9n
.measure tran d22s TRIG V(b22) VAL=.9 FALL=1 TD=1.9n TARG V(s22) VAL=.9 RISE=1 TD=1.9n
.measure tran t22s TRIG V(s22) VAL=0.18 RISE=1 TD=1.9n TARG V(s22) VAL=1.62 RISE=1 TD=1.9n
Va23 a23 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vb23 b23 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vci23 ci23 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X23 a23 b23 ci23 co23 s23 dd 0 mirror
CC23 co23 0 1f
CS23 s23 0 1f
.measure tran q23co FIND V(co23) AT=4.9n
.measure tran d23co TRIG V(ci23) VAL=.9 FALL=1 TD=1.9n TARG V(co23) VAL=.9 FALL=1 TD=1.9n
.measure tran t23co TRIG V(co23) VAL=1.62 FALL=1 TD=1.9n TARG V(co23) VAL=0.18 FALL=1 TD=1.9n
.measure tran q23s FIND V(s23) AT=4.9n
.measure tran d23s TRIG V(ci23) VAL=.9 FALL=1 TD=1.9n TARG V(s23) VAL=.9 RISE=1 TD=1.9n
.measure tran t23s TRIG V(s23) VAL=0.18 RISE=1 TD=1.9n TARG V(s23) VAL=1.62 RISE=1 TD=1.9n
Va24 a24 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb24 b24 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci24 ci24 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X24 a24 b24 ci24 co24 s24 dd 0 mirror
CC24 co24 0 1f
CS24 s24 0 1f
.measure tran q24co FIND V(co24) AT=4.9n
.measure tran d24co TRIG V(a24) VAL=.9 RISE=1 TD=1.9n TARG V(co24) VAL=.9 FALL=1 TD=1.9n
.measure tran t24co TRIG V(co24) VAL=1.62 FALL=1 TD=1.9n TARG V(co24) VAL=0.18 FALL=1 TD=1.9n
.measure tran q24s FIND V(s24) AT=4.9n
.measure tran d24s TRIG V(a24) VAL=.9 RISE=1 TD=1.9n TARG V(s24) VAL=.9 RISE=1 TD=1.9n
.measure tran t24s TRIG V(s24) VAL=0.18 RISE=1 TD=1.9n TARG V(s24) VAL=1.62 RISE=1 TD=1.9n
Va25 a25 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb25 b25 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci25 ci25 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X25 a25 b25 ci25 co25 s25 dd 0 mirror
CC25 co25 0 1f
CS25 s25 0 1f
.measure tran q25co FIND V(co25) AT=4.9n
.measure tran q25s FIND V(s25) AT=4.9n
Va26 a26 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb26 b26 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vci26 ci26 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X26 a26 b26 ci26 co26 s26 dd 0 mirror
CC26 co26 0 1f
CS26 s26 0 1f
.measure tran q26co FIND V(co26) AT=4.9n
.measure tran q26s FIND V(s26) AT=4.9n
Va27 a27 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vb27 b27 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vci27 ci27 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X27 a27 b27 ci27 co27 s27 dd 0 mirror
CC27 co27 0 1f
CS27 s27 0 1f
.measure tran q27co FIND V(co27) AT=4.9n
.measure tran q27s FIND V(s27) AT=4.9n
.measure tran d27s TRIG V(a27) VAL=.9 RISE=1 TD=1.9n TARG V(s27) VAL=.9 RISE=1 TD=1.9n
.measure tran t27s TRIG V(s27) VAL=0.18 RISE=1 TD=1.9n TARG V(s27) VAL=1.62 RISE=1 TD=1.9n
Va28 a28 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb28 b28 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vci28 ci28 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
X28 a28 b28 ci28 co28 s28 dd 0 mirror
CC28 co28 0 1f
CS28 s28 0 1f
.measure tran q28co FIND V(co28) AT=4.9n
.measure tran q28s FIND V(s28) AT=4.9n
.measure tran d28s TRIG V(a28) VAL=.9 FALL=1 TD=1.9n TARG V(s28) VAL=.9 FALL=1 TD=1.9n
.measure tran t28s TRIG V(s28) VAL=1.62 FALL=1 TD=1.9n TARG V(s28) VAL=0.18 FALL=1 TD=1.9n
Va29 a29 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb29 b29 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vci29 ci29 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X29 a29 b29 ci29 co29 s29 dd 0 mirror
CC29 co29 0 1f
CS29 s29 0 1f
.measure tran q29co FIND V(co29) AT=4.9n
.measure tran q29s FIND V(s29) AT=4.9n
Va30 a30 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb30 b30 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci30 ci30 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
X30 a30 b30 ci30 co30 s30 dd 0 mirror
CC30 co30 0 1f
CS30 s30 0 1f
.measure tran q30co FIND V(co30) AT=4.9n
.measure tran q30s FIND V(s30) AT=4.9n
Va31 a31 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb31 b31 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci31 ci31 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X31 a31 b31 ci31 co31 s31 dd 0 mirror
CC31 co31 0 1f
CS31 s31 0 1f
.measure tran q31co FIND V(co31) AT=4.9n
.measure tran d31co TRIG V(a31) VAL=.9 FALL=1 TD=1.9n TARG V(co31) VAL=.9 RISE=1 TD=1.9n
.measure tran t31co TRIG V(co31) VAL=0.18 RISE=1 TD=1.9n TARG V(co31) VAL=1.62 RISE=1 TD=1.9n
.measure tran q31s FIND V(s31) AT=4.9n
.measure tran d31s TRIG V(a31) VAL=.9 FALL=1 TD=1.9n TARG V(s31) VAL=.9 FALL=1 TD=1.9n
.measure tran t31s TRIG V(s31) VAL=1.62 FALL=1 TD=1.9n TARG V(s31) VAL=0.18 FALL=1 TD=1.9n
Va32 a32 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb32 b32 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vci32 ci32 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X32 a32 b32 ci32 co32 s32 dd 0 mirror
CC32 co32 0 1f
CS32 s32 0 1f
.measure tran q32co FIND V(co32) AT=4.9n
.measure tran d32co TRIG V(ci32) VAL=.9 RISE=1 TD=1.9n TARG V(co32) VAL=.9 RISE=1 TD=1.9n
.measure tran t32co TRIG V(co32) VAL=0.18 RISE=1 TD=1.9n TARG V(co32) VAL=1.62 RISE=1 TD=1.9n
.measure tran q32s FIND V(s32) AT=4.9n
.measure tran d32s TRIG V(ci32) VAL=.9 RISE=1 TD=1.9n TARG V(s32) VAL=.9 FALL=1 TD=1.9n
.measure tran t32s TRIG V(s32) VAL=1.62 FALL=1 TD=1.9n TARG V(s32) VAL=0.18 FALL=1 TD=1.9n
Va33 a33 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb33 b33 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci33 ci33 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
X33 a33 b33 ci33 co33 s33 dd 0 mirror
CC33 co33 0 1f
CS33 s33 0 1f
.measure tran q33co FIND V(co33) AT=4.9n
.measure tran d33co TRIG V(b33) VAL=.9 RISE=1 TD=1.9n TARG V(co33) VAL=.9 RISE=1 TD=1.9n
.measure tran t33co TRIG V(co33) VAL=0.18 RISE=1 TD=1.9n TARG V(co33) VAL=1.62 RISE=1 TD=1.9n
.measure tran q33s FIND V(s33) AT=4.9n
.measure tran d33s TRIG V(b33) VAL=.9 RISE=1 TD=1.9n TARG V(s33) VAL=.9 FALL=1 TD=1.9n
.measure tran t33s TRIG V(s33) VAL=1.62 FALL=1 TD=1.9n TARG V(s33) VAL=0.18 FALL=1 TD=1.9n
Va34 a34 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb34 b34 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci34 ci34 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X34 a34 b34 ci34 co34 s34 dd 0 mirror
CC34 co34 0 1f
CS34 s34 0 1f
.measure tran q34co FIND V(co34) AT=4.9n
.measure tran d34co TRIG V(b34) VAL=.9 RISE=1 TD=1.9n TARG V(co34) VAL=.9 RISE=1 TD=1.9n
.measure tran t34co TRIG V(co34) VAL=0.18 RISE=1 TD=1.9n TARG V(co34) VAL=1.62 RISE=1 TD=1.9n
.measure tran q34s FIND V(s34) AT=4.9n
Va35 a35 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb35 b35 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vci35 ci35 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X35 a35 b35 ci35 co35 s35 dd 0 mirror
CC35 co35 0 1f
CS35 s35 0 1f
.measure tran q35co FIND V(co35) AT=4.9n
.measure tran d35co TRIG V(a35) VAL=.9 FALL=1 TD=1.9n TARG V(co35) VAL=.9 FALL=1 TD=1.9n
.measure tran t35co TRIG V(co35) VAL=1.62 FALL=1 TD=1.9n TARG V(co35) VAL=0.18 FALL=1 TD=1.9n
.measure tran q35s FIND V(s35) AT=4.9n
Va36 a36 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb36 b36 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vci36 ci36 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X36 a36 b36 ci36 co36 s36 dd 0 mirror
CC36 co36 0 1f
CS36 s36 0 1f
.measure tran q36co FIND V(co36) AT=4.9n
.measure tran d36co TRIG V(a36) VAL=.9 FALL=1 TD=1.9n TARG V(co36) VAL=.9 FALL=1 TD=1.9n
.measure tran t36co TRIG V(co36) VAL=1.62 FALL=1 TD=1.9n TARG V(co36) VAL=0.18 FALL=1 TD=1.9n
.measure tran q36s FIND V(s36) AT=4.9n
.measure tran d36s TRIG V(a36) VAL=.9 FALL=1 TD=1.9n TARG V(s36) VAL=.9 RISE=1 TD=1.9n
.measure tran t36s TRIG V(s36) VAL=0.18 RISE=1 TD=1.9n TARG V(s36) VAL=1.62 RISE=1 TD=1.9n
Va37 a37 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb37 b37 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci37 ci37 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X37 a37 b37 ci37 co37 s37 dd 0 mirror
CC37 co37 0 1f
CS37 s37 0 1f
.measure tran q37co FIND V(co37) AT=4.9n
.measure tran d37co TRIG V(a37) VAL=.9 FALL=1 TD=1.9n TARG V(co37) VAL=.9 FALL=1 TD=1.9n
.measure tran t37co TRIG V(co37) VAL=1.62 FALL=1 TD=1.9n TARG V(co37) VAL=0.18 FALL=1 TD=1.9n
.measure tran q37s FIND V(s37) AT=4.9n
.measure tran d37s TRIG V(a37) VAL=.9 FALL=1 TD=1.9n TARG V(s37) VAL=.9 RISE=1 TD=1.9n
.measure tran t37s TRIG V(s37) VAL=0.18 RISE=1 TD=1.9n TARG V(s37) VAL=1.62 RISE=1 TD=1.9n
Va38 a38 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb38 b38 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci38 ci38 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X38 a38 b38 ci38 co38 s38 dd 0 mirror
CC38 co38 0 1f
CS38 s38 0 1f
.measure tran q38co FIND V(co38) AT=4.9n
.measure tran q38s FIND V(s38) AT=4.9n
Va39 a39 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb39 b39 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
Vci39 ci39 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X39 a39 b39 ci39 co39 s39 dd 0 mirror
CC39 co39 0 1f
CS39 s39 0 1f
.measure tran q39co FIND V(co39) AT=4.9n
.measure tran d39co TRIG V(ci39) VAL=.9 FALL=1 TD=1.9n TARG V(co39) VAL=.9 FALL=1 TD=1.9n
.measure tran t39co TRIG V(co39) VAL=1.62 FALL=1 TD=1.9n TARG V(co39) VAL=0.18 FALL=1 TD=1.9n
.measure tran q39s FIND V(s39) AT=4.9n
.measure tran d39s TRIG V(ci39) VAL=.9 FALL=1 TD=1.9n TARG V(s39) VAL=.9 RISE=1 TD=1.9n
.measure tran t39s TRIG V(s39) VAL=0.18 RISE=1 TD=1.9n TARG V(s39) VAL=1.62 RISE=1 TD=1.9n
Va40 a40 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb40 b40 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci40 ci40 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X40 a40 b40 ci40 co40 s40 dd 0 mirror
CC40 co40 0 1f
CS40 s40 0 1f
.measure tran q40co FIND V(co40) AT=4.9n
.measure tran q40s FIND V(s40) AT=4.9n
Va41 a41 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb41 b41 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
Vci41 ci41 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X41 a41 b41 ci41 co41 s41 dd 0 mirror
CC41 co41 0 1f
CS41 s41 0 1f
.measure tran q41co FIND V(co41) AT=4.9n
.measure tran q41s FIND V(s41) AT=4.9n
.measure tran d41s TRIG V(b41) VAL=.9 RISE=1 TD=1.9n TARG V(s41) VAL=.9 RISE=1 TD=1.9n
.measure tran t41s TRIG V(s41) VAL=0.18 RISE=1 TD=1.9n TARG V(s41) VAL=1.62 RISE=1 TD=1.9n
Va42 a42 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb42 b42 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci42 ci42 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
X42 a42 b42 ci42 co42 s42 dd 0 mirror
CC42 co42 0 1f
CS42 s42 0 1f
.measure tran q42co FIND V(co42) AT=4.9n
.measure tran d42co TRIG V(a42) VAL=.9 FALL=1 TD=1.9n TARG V(co42) VAL=.9 FALL=1 TD=1.9n
.measure tran t42co TRIG V(co42) VAL=1.62 FALL=1 TD=1.9n TARG V(co42) VAL=0.18 FALL=1 TD=1.9n
.measure tran q42s FIND V(s42) AT=4.9n
Va43 a43 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb43 b43 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci43 ci43 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X43 a43 b43 ci43 co43 s43 dd 0 mirror
CC43 co43 0 1f
CS43 s43 0 1f
.measure tran q43co FIND V(co43) AT=4.9n
.measure tran d43co TRIG V(a43) VAL=.9 FALL=1 TD=1.9n TARG V(co43) VAL=.9 FALL=1 TD=1.9n
.measure tran t43co TRIG V(co43) VAL=1.62 FALL=1 TD=1.9n TARG V(co43) VAL=0.18 FALL=1 TD=1.9n
.measure tran q43s FIND V(s43) AT=4.9n
.measure tran d43s TRIG V(a43) VAL=.9 FALL=1 TD=1.9n TARG V(s43) VAL=.9 RISE=1 TD=1.9n
.measure tran t43s TRIG V(s43) VAL=0.18 RISE=1 TD=1.9n TARG V(s43) VAL=1.62 RISE=1 TD=1.9n
Va44 a44 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb44 b44 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vci44 ci44 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
X44 a44 b44 ci44 co44 s44 dd 0 mirror
CC44 co44 0 1f
CS44 s44 0 1f
.measure tran q44co FIND V(co44) AT=4.9n
.measure tran d44co TRIG V(a44) VAL=.9 FALL=1 TD=1.9n TARG V(co44) VAL=.9 FALL=1 TD=1.9n
.measure tran t44co TRIG V(co44) VAL=1.62 FALL=1 TD=1.9n TARG V(co44) VAL=0.18 FALL=1 TD=1.9n
.measure tran q44s FIND V(s44) AT=4.9n
.measure tran d44s TRIG V(a44) VAL=.9 FALL=1 TD=1.9n TARG V(s44) VAL=.9 RISE=1 TD=1.9n
.measure tran t44s TRIG V(s44) VAL=0.18 RISE=1 TD=1.9n TARG V(s44) VAL=1.62 RISE=1 TD=1.9n
Va45 a45 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb45 b45 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vci45 ci45 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X45 a45 b45 ci45 co45 s45 dd 0 mirror
CC45 co45 0 1f
CS45 s45 0 1f
.measure tran q45co FIND V(co45) AT=4.9n
.measure tran q45s FIND V(s45) AT=4.9n
Va46 a46 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb46 b46 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci46 ci46 0 PWL(0 0.0 2n 0.0 2.02n 0.0 5n 0.0)
X46 a46 b46 ci46 co46 s46 dd 0 mirror
CC46 co46 0 1f
CS46 s46 0 1f
.measure tran q46co FIND V(co46) AT=4.9n
.measure tran d46co TRIG V(b46) VAL=.9 FALL=1 TD=1.9n TARG V(co46) VAL=.9 FALL=1 TD=1.9n
.measure tran t46co TRIG V(co46) VAL=1.62 FALL=1 TD=1.9n TARG V(co46) VAL=0.18 FALL=1 TD=1.9n
.measure tran q46s FIND V(s46) AT=4.9n
.measure tran d46s TRIG V(b46) VAL=.9 FALL=1 TD=1.9n TARG V(s46) VAL=.9 RISE=1 TD=1.9n
.measure tran t46s TRIG V(s46) VAL=0.18 RISE=1 TD=1.9n TARG V(s46) VAL=1.62 RISE=1 TD=1.9n
Va47 a47 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb47 b47 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci47 ci47 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X47 a47 b47 ci47 co47 s47 dd 0 mirror
CC47 co47 0 1f
CS47 s47 0 1f
.measure tran q47co FIND V(co47) AT=4.9n
.measure tran q47s FIND V(s47) AT=4.9n
Va48 a48 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb48 b48 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vci48 ci48 0 PWL(0 0.0 2n 0.0 2.02n 1.8 5n 1.8)
X48 a48 b48 ci48 co48 s48 dd 0 mirror
CC48 co48 0 1f
CS48 s48 0 1f
.measure tran q48co FIND V(co48) AT=4.9n
.measure tran q48s FIND V(s48) AT=4.9n
.measure tran d48s TRIG V(ci48) VAL=.9 RISE=1 TD=1.9n TARG V(s48) VAL=.9 RISE=1 TD=1.9n
.measure tran t48s TRIG V(s48) VAL=0.18 RISE=1 TD=1.9n TARG V(s48) VAL=1.62 RISE=1 TD=1.9n
Va49 a49 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb49 b49 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci49 ci49 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X49 a49 b49 ci49 co49 s49 dd 0 mirror
CC49 co49 0 1f
CS49 s49 0 1f
.measure tran q49co FIND V(co49) AT=4.9n
.measure tran d49co TRIG V(a49) VAL=.9 FALL=1 TD=1.9n TARG V(co49) VAL=.9 FALL=1 TD=1.9n
.measure tran t49co TRIG V(co49) VAL=1.62 FALL=1 TD=1.9n TARG V(co49) VAL=0.18 FALL=1 TD=1.9n
.measure tran q49s FIND V(s49) AT=4.9n
.measure tran d49s TRIG V(a49) VAL=.9 FALL=1 TD=1.9n TARG V(s49) VAL=.9 FALL=1 TD=1.9n
.measure tran t49s TRIG V(s49) VAL=1.62 FALL=1 TD=1.9n TARG V(s49) VAL=0.18 FALL=1 TD=1.9n
Va50 a50 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb50 b50 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci50 ci50 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X50 a50 b50 ci50 co50 s50 dd 0 mirror
CC50 co50 0 1f
CS50 s50 0 1f
.measure tran q50co FIND V(co50) AT=4.9n
.measure tran d50co TRIG V(a50) VAL=.9 FALL=1 TD=1.9n TARG V(co50) VAL=.9 FALL=1 TD=1.9n
.measure tran t50co TRIG V(co50) VAL=1.62 FALL=1 TD=1.9n TARG V(co50) VAL=0.18 FALL=1 TD=1.9n
.measure tran q50s FIND V(s50) AT=4.9n
Va51 a51 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb51 b51 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vci51 ci51 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X51 a51 b51 ci51 co51 s51 dd 0 mirror
CC51 co51 0 1f
CS51 s51 0 1f
.measure tran q51co FIND V(co51) AT=4.9n
.measure tran d51co TRIG V(a51) VAL=.9 FALL=1 TD=1.9n TARG V(co51) VAL=.9 FALL=1 TD=1.9n
.measure tran t51co TRIG V(co51) VAL=1.62 FALL=1 TD=1.9n TARG V(co51) VAL=0.18 FALL=1 TD=1.9n
.measure tran q51s FIND V(s51) AT=4.9n
Va52 a52 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vb52 b52 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vci52 ci52 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X52 a52 b52 ci52 co52 s52 dd 0 mirror
CC52 co52 0 1f
CS52 s52 0 1f
.measure tran q52co FIND V(co52) AT=4.9n
.measure tran q52s FIND V(s52) AT=4.9n
.measure tran d52s TRIG V(a52) VAL=.9 FALL=1 TD=1.9n TARG V(s52) VAL=.9 FALL=1 TD=1.9n
.measure tran t52s TRIG V(s52) VAL=1.62 FALL=1 TD=1.9n TARG V(s52) VAL=0.18 FALL=1 TD=1.9n
Va53 a53 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb53 b53 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci53 ci53 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X53 a53 b53 ci53 co53 s53 dd 0 mirror
CC53 co53 0 1f
CS53 s53 0 1f
.measure tran q53co FIND V(co53) AT=4.9n
.measure tran d53co TRIG V(b53) VAL=.9 FALL=1 TD=1.9n TARG V(co53) VAL=.9 FALL=1 TD=1.9n
.measure tran t53co TRIG V(co53) VAL=1.62 FALL=1 TD=1.9n TARG V(co53) VAL=0.18 FALL=1 TD=1.9n
.measure tran q53s FIND V(s53) AT=4.9n
Va54 a54 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb54 b54 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
Vci54 ci54 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
X54 a54 b54 ci54 co54 s54 dd 0 mirror
CC54 co54 0 1f
CS54 s54 0 1f
.measure tran q54co FIND V(co54) AT=4.9n
.measure tran q54s FIND V(s54) AT=4.9n
.measure tran d54s TRIG V(b54) VAL=.9 FALL=1 TD=1.9n TARG V(s54) VAL=.9 FALL=1 TD=1.9n
.measure tran t54s TRIG V(s54) VAL=1.62 FALL=1 TD=1.9n TARG V(s54) VAL=0.18 FALL=1 TD=1.9n
Va55 a55 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vb55 b55 0 PWL(0 1.8 2n 1.8 2.02n 1.8 5n 1.8)
Vci55 ci55 0 PWL(0 1.8 2n 1.8 2.02n 0.0 5n 0.0)
X55 a55 b55 ci55 co55 s55 dd 0 mirror
CC55 co55 0 1f
CS55 s55 0 1f
.measure tran q55co FIND V(co55) AT=4.9n
.measure tran q55s FIND V(s55) AT=4.9n
.measure tran d55s TRIG V(ci55) VAL=.9 FALL=1 TD=1.9n TARG V(s55) VAL=.9 FALL=1 TD=1.9n
.measure tran t55s TRIG V(s55) VAL=1.62 FALL=1 TD=1.9n TARG V(s55) VAL=0.18 FALL=1 TD=1.9n
.tran 1p 5n
.print tran V(a5) V(b5) V(ci5) V(co5) V(s5) V(a19) V(b19) V(ci19) V(co19) V(s19) V(a22) V(b22) V(ci22) V(co22) V(s22) V(a46) V(b46) V(ci46) V(co46) V(s46)
.end
