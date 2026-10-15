* 2020 HW3: pre-layout static CMOS AND, F=NAND internal node, Z=AND output.
* All lengths 0.18 um. 2 um NAND NMOS compensates its two-device stack.
* Diffusion geometry uses a declared 0.18 um extension (not layout extraction).
.subckt and2 a b f z vdd vss
MPA f a vdd vdd P_18 W=2.5u L=0.18u
+ AD='2.5u*0.18u' AS='2.5u*0.18u' PD='2*(2.5u+0.18u)' PS='2*(2.5u+0.18u)'
MPB f b vdd vdd P_18 W=2.5u L=0.18u
+ AD='2.5u*0.18u' AS='2.5u*0.18u' PD='2*(2.5u+0.18u)' PS='2*(2.5u+0.18u)'
MNA f a mid vss N_18 W=2u L=0.18u
+ AD='2u*0.18u' AS='2u*0.18u' PD='2*(2u+0.18u)' PS='2*(2u+0.18u)'
MNB mid b vss vss N_18 W=2u L=0.18u
+ AD='2u*0.18u' AS='2u*0.18u' PD='2*(2u+0.18u)' PS='2*(2u+0.18u)'
MPZ z f vdd vdd P_18 W=2.5u L=0.18u
+ AD='2.5u*0.18u' AS='2.5u*0.18u' PD='2*(2.5u+0.18u)' PS='2*(2.5u+0.18u)'
MNZ z f vss vss N_18 W=1u L=0.18u
+ AD='1u*0.18u' AS='1u*0.18u' PD='2*(1u+0.18u)' PS='2*(1u+0.18u)'
.ends and2
