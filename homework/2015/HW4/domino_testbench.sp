* 2015 reproducible schematic simulation
.protect
.lib 'D:/cic018.l' TT
.unprotect
.option post=0 lis_new=1 ingold=2 numdgt=10 measdgt=10 measform=3 delmax=0.2p
.temp 25
.include 'domino.sp'
VDD dd 0 1.8
VCLK clk 0 PWL(0 0 2n 0 2.02n 1.8 4n 1.8 4.02n 0 5n 0)
Va0 a0 0 0.0
Vb0 b0 0 0.0
Vci0 ci0 0 0.0
X0 a0 b0 ci0 clk co0 s0 nco0 dd 0 domino
CC0 co0 0 1f
CS0 s0 0 1f
.measure tran q0co FIND V(co0) AT=3.8n
.measure tran r0co FIND V(co0) AT=4.8n
.measure tran q0s FIND V(s0) AT=3.8n
.measure tran r0s FIND V(s0) AT=4.8n
.measure tran q0nco FIND V(nco0) AT=3.8n
.measure tran r0nco FIND V(nco0) AT=4.8n
.measure tran d0nco TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V(nco0) VAL=.9 RISE=1 TD=1.9n
.measure tran e0nco TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V(nco0) VAL=.9 FALL=1 TD=3.9n
.measure tran t0nco TRIG V(nco0) VAL=0.18 RISE=1 TD=1.9n TARG V(nco0) VAL=1.62 RISE=1 TD=1.9n
.measure tran u0nco TRIG V(nco0) VAL=1.62 FALL=1 TD=3.9n TARG V(nco0) VAL=0.18 FALL=1 TD=3.9n
Va1 a1 0 0.0
Vb1 b1 0 0.0
Vci1 ci1 0 1.8
X1 a1 b1 ci1 clk co1 s1 nco1 dd 0 domino
CC1 co1 0 1f
CS1 s1 0 1f
.measure tran q1co FIND V(co1) AT=3.8n
.measure tran r1co FIND V(co1) AT=4.8n
.measure tran q1s FIND V(s1) AT=3.8n
.measure tran r1s FIND V(s1) AT=4.8n
.measure tran d1s TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V(s1) VAL=.9 RISE=1 TD=1.9n
.measure tran e1s TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V(s1) VAL=.9 FALL=1 TD=3.9n
.measure tran t1s TRIG V(s1) VAL=0.18 RISE=1 TD=1.9n TARG V(s1) VAL=1.62 RISE=1 TD=1.9n
.measure tran u1s TRIG V(s1) VAL=1.62 FALL=1 TD=3.9n TARG V(s1) VAL=0.18 FALL=1 TD=3.9n
.measure tran q1nco FIND V(nco1) AT=3.8n
.measure tran r1nco FIND V(nco1) AT=4.8n
.measure tran d1nco TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V(nco1) VAL=.9 RISE=1 TD=1.9n
.measure tran e1nco TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V(nco1) VAL=.9 FALL=1 TD=3.9n
.measure tran t1nco TRIG V(nco1) VAL=0.18 RISE=1 TD=1.9n TARG V(nco1) VAL=1.62 RISE=1 TD=1.9n
.measure tran u1nco TRIG V(nco1) VAL=1.62 FALL=1 TD=3.9n TARG V(nco1) VAL=0.18 FALL=1 TD=3.9n
Va2 a2 0 0.0
Vb2 b2 0 1.8
Vci2 ci2 0 0.0
X2 a2 b2 ci2 clk co2 s2 nco2 dd 0 domino
CC2 co2 0 1f
CS2 s2 0 1f
.measure tran q2co FIND V(co2) AT=3.8n
.measure tran r2co FIND V(co2) AT=4.8n
.measure tran q2s FIND V(s2) AT=3.8n
.measure tran r2s FIND V(s2) AT=4.8n
.measure tran d2s TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V(s2) VAL=.9 RISE=1 TD=1.9n
.measure tran e2s TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V(s2) VAL=.9 FALL=1 TD=3.9n
.measure tran t2s TRIG V(s2) VAL=0.18 RISE=1 TD=1.9n TARG V(s2) VAL=1.62 RISE=1 TD=1.9n
.measure tran u2s TRIG V(s2) VAL=1.62 FALL=1 TD=3.9n TARG V(s2) VAL=0.18 FALL=1 TD=3.9n
.measure tran q2nco FIND V(nco2) AT=3.8n
.measure tran r2nco FIND V(nco2) AT=4.8n
.measure tran d2nco TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V(nco2) VAL=.9 RISE=1 TD=1.9n
.measure tran e2nco TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V(nco2) VAL=.9 FALL=1 TD=3.9n
.measure tran t2nco TRIG V(nco2) VAL=0.18 RISE=1 TD=1.9n TARG V(nco2) VAL=1.62 RISE=1 TD=1.9n
.measure tran u2nco TRIG V(nco2) VAL=1.62 FALL=1 TD=3.9n TARG V(nco2) VAL=0.18 FALL=1 TD=3.9n
Va3 a3 0 0.0
Vb3 b3 0 1.8
Vci3 ci3 0 1.8
X3 a3 b3 ci3 clk co3 s3 nco3 dd 0 domino
CC3 co3 0 1f
CS3 s3 0 1f
.measure tran q3co FIND V(co3) AT=3.8n
.measure tran r3co FIND V(co3) AT=4.8n
.measure tran d3co TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V(co3) VAL=.9 RISE=1 TD=1.9n
.measure tran e3co TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V(co3) VAL=.9 FALL=1 TD=3.9n
.measure tran t3co TRIG V(co3) VAL=0.18 RISE=1 TD=1.9n TARG V(co3) VAL=1.62 RISE=1 TD=1.9n
.measure tran u3co TRIG V(co3) VAL=1.62 FALL=1 TD=3.9n TARG V(co3) VAL=0.18 FALL=1 TD=3.9n
.measure tran q3s FIND V(s3) AT=3.8n
.measure tran r3s FIND V(s3) AT=4.8n
.measure tran q3nco FIND V(nco3) AT=3.8n
.measure tran r3nco FIND V(nco3) AT=4.8n
Va4 a4 0 1.8
Vb4 b4 0 0.0
Vci4 ci4 0 0.0
X4 a4 b4 ci4 clk co4 s4 nco4 dd 0 domino
CC4 co4 0 1f
CS4 s4 0 1f
.measure tran q4co FIND V(co4) AT=3.8n
.measure tran r4co FIND V(co4) AT=4.8n
.measure tran q4s FIND V(s4) AT=3.8n
.measure tran r4s FIND V(s4) AT=4.8n
.measure tran d4s TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V(s4) VAL=.9 RISE=1 TD=1.9n
.measure tran e4s TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V(s4) VAL=.9 FALL=1 TD=3.9n
.measure tran t4s TRIG V(s4) VAL=0.18 RISE=1 TD=1.9n TARG V(s4) VAL=1.62 RISE=1 TD=1.9n
.measure tran u4s TRIG V(s4) VAL=1.62 FALL=1 TD=3.9n TARG V(s4) VAL=0.18 FALL=1 TD=3.9n
.measure tran q4nco FIND V(nco4) AT=3.8n
.measure tran r4nco FIND V(nco4) AT=4.8n
.measure tran d4nco TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V(nco4) VAL=.9 RISE=1 TD=1.9n
.measure tran e4nco TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V(nco4) VAL=.9 FALL=1 TD=3.9n
.measure tran t4nco TRIG V(nco4) VAL=0.18 RISE=1 TD=1.9n TARG V(nco4) VAL=1.62 RISE=1 TD=1.9n
.measure tran u4nco TRIG V(nco4) VAL=1.62 FALL=1 TD=3.9n TARG V(nco4) VAL=0.18 FALL=1 TD=3.9n
Va5 a5 0 1.8
Vb5 b5 0 0.0
Vci5 ci5 0 1.8
X5 a5 b5 ci5 clk co5 s5 nco5 dd 0 domino
CC5 co5 0 1f
CS5 s5 0 1f
.measure tran q5co FIND V(co5) AT=3.8n
.measure tran r5co FIND V(co5) AT=4.8n
.measure tran d5co TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V(co5) VAL=.9 RISE=1 TD=1.9n
.measure tran e5co TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V(co5) VAL=.9 FALL=1 TD=3.9n
.measure tran t5co TRIG V(co5) VAL=0.18 RISE=1 TD=1.9n TARG V(co5) VAL=1.62 RISE=1 TD=1.9n
.measure tran u5co TRIG V(co5) VAL=1.62 FALL=1 TD=3.9n TARG V(co5) VAL=0.18 FALL=1 TD=3.9n
.measure tran q5s FIND V(s5) AT=3.8n
.measure tran r5s FIND V(s5) AT=4.8n
.measure tran q5nco FIND V(nco5) AT=3.8n
.measure tran r5nco FIND V(nco5) AT=4.8n
Va6 a6 0 1.8
Vb6 b6 0 1.8
Vci6 ci6 0 0.0
X6 a6 b6 ci6 clk co6 s6 nco6 dd 0 domino
CC6 co6 0 1f
CS6 s6 0 1f
.measure tran q6co FIND V(co6) AT=3.8n
.measure tran r6co FIND V(co6) AT=4.8n
.measure tran d6co TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V(co6) VAL=.9 RISE=1 TD=1.9n
.measure tran e6co TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V(co6) VAL=.9 FALL=1 TD=3.9n
.measure tran t6co TRIG V(co6) VAL=0.18 RISE=1 TD=1.9n TARG V(co6) VAL=1.62 RISE=1 TD=1.9n
.measure tran u6co TRIG V(co6) VAL=1.62 FALL=1 TD=3.9n TARG V(co6) VAL=0.18 FALL=1 TD=3.9n
.measure tran q6s FIND V(s6) AT=3.8n
.measure tran r6s FIND V(s6) AT=4.8n
.measure tran q6nco FIND V(nco6) AT=3.8n
.measure tran r6nco FIND V(nco6) AT=4.8n
Va7 a7 0 1.8
Vb7 b7 0 1.8
Vci7 ci7 0 1.8
X7 a7 b7 ci7 clk co7 s7 nco7 dd 0 domino
CC7 co7 0 1f
CS7 s7 0 1f
.measure tran q7co FIND V(co7) AT=3.8n
.measure tran r7co FIND V(co7) AT=4.8n
.measure tran d7co TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V(co7) VAL=.9 RISE=1 TD=1.9n
.measure tran e7co TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V(co7) VAL=.9 FALL=1 TD=3.9n
.measure tran t7co TRIG V(co7) VAL=0.18 RISE=1 TD=1.9n TARG V(co7) VAL=1.62 RISE=1 TD=1.9n
.measure tran u7co TRIG V(co7) VAL=1.62 FALL=1 TD=3.9n TARG V(co7) VAL=0.18 FALL=1 TD=3.9n
.measure tran q7s FIND V(s7) AT=3.8n
.measure tran r7s FIND V(s7) AT=4.8n
.measure tran d7s TRIG V(clk) VAL=.9 RISE=1 TD=1.9n TARG V(s7) VAL=.9 RISE=1 TD=1.9n
.measure tran e7s TRIG V(clk) VAL=.9 FALL=1 TD=3.9n TARG V(s7) VAL=.9 FALL=1 TD=3.9n
.measure tran t7s TRIG V(s7) VAL=0.18 RISE=1 TD=1.9n TARG V(s7) VAL=1.62 RISE=1 TD=1.9n
.measure tran u7s TRIG V(s7) VAL=1.62 FALL=1 TD=3.9n TARG V(s7) VAL=0.18 FALL=1 TD=3.9n
.measure tran q7nco FIND V(nco7) AT=3.8n
.measure tran r7nco FIND V(nco7) AT=4.8n
.tran 1p 5n
.print tran V(clk) V(co4) V(s4) V(nco4) V(co5) V(s5) V(nco5) V(co7) V(s7) V(nco7)
.end
