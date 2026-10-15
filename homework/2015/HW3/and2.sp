* 2015 HW3 Q1: ALL SIX TRANSISTORS have W=0.47um L=0.18um.
* F is the NAND intermediate node; Z is the final AND output.
* No external output capacitor is specified. All diffusion extensions 0.18um.
.subckt and2 a b f z vdd vss
MPA f a vdd vdd P_18 W=0.47u L=0.18u AD='0.47u*0.18u' AS='0.47u*0.18u'
+ PD='2*(0.47u+0.18u)' PS='2*(0.47u+0.18u)'
MPB f b vdd vdd P_18 W=0.47u L=0.18u AD='0.47u*0.18u' AS='0.47u*0.18u'
+ PD='2*(0.47u+0.18u)' PS='2*(0.47u+0.18u)'
MNA f a mid vss N_18 W=0.47u L=0.18u AD='0.47u*0.18u' AS='0.47u*0.18u'
+ PD='2*(0.47u+0.18u)' PS='2*(0.47u+0.18u)'
MNB mid b vss vss N_18 W=0.47u L=0.18u AD='0.47u*0.18u' AS='0.47u*0.18u'
+ PD='2*(0.47u+0.18u)' PS='2*(0.47u+0.18u)'
MPZ z f vdd vdd P_18 W=0.47u L=0.18u AD='0.47u*0.18u' AS='0.47u*0.18u'
+ PD='2*(0.47u+0.18u)' PS='2*(0.47u+0.18u)'
MNZ z f vss vss N_18 W=0.47u L=0.18u AD='0.47u*0.18u' AS='0.47u*0.18u'
+ PD='2*(0.47u+0.18u)' PS='2*(0.47u+0.18u)'
.ends and2
