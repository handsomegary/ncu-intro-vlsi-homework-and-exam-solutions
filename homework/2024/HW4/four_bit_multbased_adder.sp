* Figure 1 serial-parallel multiplexer-based adder, 64 MOSFETs.
* Dimensions in micrometres; global rails vdd/vss provided by testbench.
.param WN=0.47u WP=0.47u WT=0.47u LG=0.18u
.subckt inv a z
MP z a vdd vdd P_18 W=WP L=LG
MN z a vss vss N_18 W=WN L=LG
.ends inv
.subckt tg a z s sb
MP z sb a vdd P_18 W=WT L=LG
MN z s a vss N_18 W=WT L=LG
.ends tg
.subckt mux_fa x y ci s co
* Compact 4T upper XNOR: e can be threshold-degraded internally.
MPU0 ep x vdd vdd P_18 W=WP L=LG
MPU1 e y ep vdd P_18 W=WP L=LG
MNU0 e y x vss N_18 W=WN L=LG
MNU1 e x y vss N_18 W=WN L=LG
XI2 e en inv
XI3 ci cib inv
* Lower XNOR uses ci/cib as DATA; e/en as SELECT.
* This choice restores the external sum even when compact e is degraded.
XT2 ci s e en tg
XT3 cib s en e tg
* Carry: co = e ? y : ci. Shared complementary select.
XT4 y co e en tg
XT5 ci co en e tg
.ends mux_fa
.subckt four_bit_multbased_adder cin x0 x1 x2 x3 y0 y1 y2 y3 s0 s1 s2 s3 cout
XF0 x0 y0 cin s0 c1 mux_fa
XF1 x1 y1 c1 s1 c2 mux_fa
XF2 x2 y2 c2 s2 c3 mux_fa
XF3 x3 y3 c3 s3 cout mux_fa
.ends four_bit_multbased_adder
