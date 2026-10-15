* Robust dual-rail domino full adder. Data stable before CLK rises.
* No falling dynamic carry node drives the sum NMOS gates.
.param WPSC=2.495240000u WPSS=3.108270000u
.subckt domino_fa a b c clk s co vdd vss
* Static complements settle during precharge.
MPA ab a vdd vdd P_18 w=1.8u l=.18u
MNA ab a vss vss N_18 w=.6u l=.18u
MPB bb b vdd vdd P_18 w=1.8u l=.18u
MNB bb b vss vss N_18 w=.6u l=.18u
MPC cb c vdd vdd P_18 w=1.8u l=.18u
MNC cb c vss vss N_18 w=.6u l=.18u
* Independent dynamic carry; co=AB+AC+BC.
MPREC cd clk vdd vdd P_18 w=WPSC l=.18u
MNCA cd a cn1 vss N_18 w=1.8u l=.18u
MNCB cn1 b cf vss N_18 w=1.8u l=.18u
MNCC cd a cn2 vss N_18 w=1.8u l=.18u
MNCD cn2 c cf vss N_18 w=1.8u l=.18u
MNCE cd b cn3 vss N_18 w=1.8u l=.18u
MNCF cn3 c cf vss N_18 w=1.8u l=.18u
MNFC cf clk vss vss N_18 w=3.6u l=.18u
MPKC cd co vdd vdd P_18 w=.3u l=.36u
MPOC co cd vdd vdd P_18 w=2.1u l=.18u
MNOC co cd vss vss N_18 w=.6u l=.18u
* Independent dynamic sum: ab*bb*c + ab*b*cb + a*bb*cb + a*b*c.
MPRES sd clk vdd vdd P_18 w=WPSS l=.18u
MNS0A sd ab sn0a vss N_18 w=2.4u l=.18u
MNS0B sn0a bb sn0b vss N_18 w=2.4u l=.18u
MNS0C sn0b c sf vss N_18 w=2.4u l=.18u
MNS1A sd ab sn1a vss N_18 w=2.4u l=.18u
MNS1B sn1a b sn1b vss N_18 w=2.4u l=.18u
MNS1C sn1b cb sf vss N_18 w=2.4u l=.18u
MNS2A sd a sn2a vss N_18 w=2.4u l=.18u
MNS2B sn2a bb sn2b vss N_18 w=2.4u l=.18u
MNS2C sn2b cb sf vss N_18 w=2.4u l=.18u
MNS3A sd a sn3a vss N_18 w=2.4u l=.18u
MNS3B sn3a b sn3b vss N_18 w=2.4u l=.18u
MNS3C sn3b c sf vss N_18 w=2.4u l=.18u
MNFS sf clk vss vss N_18 w=3.6u l=.18u
MPKS sd s vdd vdd P_18 w=.3u l=.36u
MPOS s sd vdd vdd P_18 w=2.1u l=.18u
MNOS s sd vss vss N_18 w=.6u l=.18u
* Explicit storage capacitance to limit charge sharing.
CSD sd vss 2f
CCD cd vss 2f
.ends domino_fa
