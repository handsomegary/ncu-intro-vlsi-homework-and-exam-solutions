* Independently reconstructed 28T static CMOS full adder.
* All pMOS bulks are vdd, all nMOS bulks vss; dimensions in micrometres.
.subckt inv a z vdd vss
MP z a vdd vdd P_18 W=2u L=0.18u
MN z a vss vss N_18 W=1u L=0.18u
.ends inv
.subckt fa a b ci s co vdd vss
* cn = NOT[ab + ci(a+b)] : complementary 10T carry gate.
MP0 pu a vdd vdd P_18 W=4u L=0.18u
MP1 pu b vdd vdd P_18 W=4u L=0.18u
MP2 p2 a pu vdd P_18 W=4u L=0.18u
MP3 cn b p2 vdd P_18 W=4u L=0.18u
MP4 cn ci pu vdd P_18 W=4u L=0.18u
MN0 cn ci n0 vss N_18 W=2u L=0.18u
MN1 n0 a vss vss N_18 W=2u L=0.18u
MN2 n0 b vss vss N_18 W=2u L=0.18u
MN3 cn a n3 vss N_18 W=2u L=0.18u
MN4 n3 b vss vss N_18 W=2u L=0.18u
XC cn co vdd vss inv
* sn = NOT[cn(a+b+ci) + abci] : complementary 14T sum gate.
MPS0 ps a vdd vdd P_18 W=6u L=0.18u
MPS1 ps b vdd vdd P_18 W=6u L=0.18u
MPS2 ps ci vdd vdd P_18 W=6u L=0.18u
MPS3 sn cn ps vdd P_18 W=6u L=0.18u
MPS4 p4 a ps vdd P_18 W=6u L=0.18u
MPS5 p5 b p4 vdd P_18 W=6u L=0.18u
MPS6 sn ci p5 vdd P_18 W=6u L=0.18u
MNS0 sn cn ns vss N_18 W=3u L=0.18u
MNS1 ns a vss vss N_18 W=3u L=0.18u
MNS2 ns b vss vss N_18 W=3u L=0.18u
MNS3 ns ci vss vss N_18 W=3u L=0.18u
MNS4 sn a n4 vss N_18 W=3u L=0.18u
MNS5 n4 b n5 vss N_18 W=3u L=0.18u
MNS6 n5 ci vss vss N_18 W=3u L=0.18u
XS sn s vdd vss inv
.ends fa
.subckt rca cin x0 x1 x2 y0 y1 y2 s0 s1 s2 cout vdd vss
XF0 x0 y0 cin s0 c1 vdd vss fa
XF1 x1 y1 c1 s1 c2 vdd vss fa
XF2 x2 y2 c2 s2 cout vdd vss fa
.ends rca
