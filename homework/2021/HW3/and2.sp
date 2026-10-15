* 2021 CMOS AND gate; terminals A B F Z VDD VSS.
* F is the internal NAND output; Z is the final AND output.
* W/L in micrometres. PMOS bulk=VDD; NMOS bulk=VSS.
.subckt and2 a b f z vdd vss
mp1 f a vdd vdd p_18 w=3u l=.18u
mp2 f b vdd vdd p_18 w=3u l=.18u
mn3 f a x vss n_18 w=2u l=.18u
mn4 x b vss vss n_18 w=2u l=.18u
mp5 z f vdd vdd p_18 w=3u l=.18u
mn6 z f vss vss n_18 w=1u l=.18u
.ends and2
