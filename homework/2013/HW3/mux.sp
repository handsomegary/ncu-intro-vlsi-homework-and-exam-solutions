* Fixed TG dimensions; geometry is a declared schematic estimate.
.subckt inv a z vdd vss
MP z a vdd vdd P_18 W=20u L=.18u
MN z a vss vss N_18 W=10u L=.18u
.ends inv
.subckt tg a z cn cp vdd vss
MN z cn a vss N_18 W=10u L=.18u
+ AD='10u*.18u' AS='10u*.18u' PD='2*(10u+.18u)' PS='2*(10u+.18u)'
MP z cp a vdd P_18 W=20u L=.18u
+ AD='20u*.18u' AS='20u*.18u' PD='2*(20u+.18u)' PS='2*(20u+.18u)'
.ends tg
.subckt baseline a0 a1 a2 a3 a4 a5 a6 a7 s0 s1 s2 z vdd vss
XI0 s0 b0 vdd vss inv
XI1 s1 b1 vdd vss inv
XI2 s2 b2 vdd vss inv
XT0_0 a0 q0_0 b0 s0 vdd vss tg
XT0_1 q0_0 q0_1 b1 s1 vdd vss tg
XT0_2 q0_1 z b2 s2 vdd vss tg
XT1_0 a1 q1_0 s0 b0 vdd vss tg
XT1_1 q1_0 q1_1 b1 s1 vdd vss tg
XT1_2 q1_1 z b2 s2 vdd vss tg
XT2_0 a2 q2_0 b0 s0 vdd vss tg
XT2_1 q2_0 q2_1 s1 b1 vdd vss tg
XT2_2 q2_1 z b2 s2 vdd vss tg
XT3_0 a3 q3_0 s0 b0 vdd vss tg
XT3_1 q3_0 q3_1 s1 b1 vdd vss tg
XT3_2 q3_1 z b2 s2 vdd vss tg
XT4_0 a4 q4_0 b0 s0 vdd vss tg
XT4_1 q4_0 q4_1 b1 s1 vdd vss tg
XT4_2 q4_1 z s2 b2 vdd vss tg
XT5_0 a5 q5_0 s0 b0 vdd vss tg
XT5_1 q5_0 q5_1 b1 s1 vdd vss tg
XT5_2 q5_1 z s2 b2 vdd vss tg
XT6_0 a6 q6_0 b0 s0 vdd vss tg
XT6_1 q6_0 q6_1 s1 b1 vdd vss tg
XT6_2 q6_1 z s2 b2 vdd vss tg
XT7_0 a7 q7_0 s0 b0 vdd vss tg
XT7_1 q7_0 q7_1 s1 b1 vdd vss tg
XT7_2 q7_1 z s2 b2 vdd vss tg
.ends baseline
.subckt tree a0 a1 a2 a3 a4 a5 a6 a7 s0 s1 s2 z vdd vss
XI0 s0 b0 vdd vss inv
XI1 s1 b1 vdd vss inv
XI2 s2 b2 vdd vss inv
XT0_0L a0 q0_0 b0 s0 vdd vss tg
XT0_0H a1 q0_0 s0 b0 vdd vss tg
XT0_1L a2 q0_1 b0 s0 vdd vss tg
XT0_1H a3 q0_1 s0 b0 vdd vss tg
XT0_2L a4 q0_2 b0 s0 vdd vss tg
XT0_2H a5 q0_2 s0 b0 vdd vss tg
XT0_3L a6 q0_3 b0 s0 vdd vss tg
XT0_3H a7 q0_3 s0 b0 vdd vss tg
XT1_0L q0_0 q1_0 b1 s1 vdd vss tg
XT1_0H q0_1 q1_0 s1 b1 vdd vss tg
XT1_1L q0_2 q1_1 b1 s1 vdd vss tg
XT1_1H q0_3 q1_1 s1 b1 vdd vss tg
XT2_0L q1_0 z b2 s2 vdd vss tg
XT2_0H q1_1 z s2 b2 vdd vss tg
.ends tree
