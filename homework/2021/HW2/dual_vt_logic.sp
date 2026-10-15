* Transistor topology for Q1. LVT/HVT names are placeholders for a
* true dual-Vt PDK. CIC018 TT supplies only N_18/P_18; do NOT claim
* this topology verifies physical dual-Vt leakage/delay.
.subckt dual_vt_logic a b c d e vdd vss
* Low-Vt inverter A and complementary B driver.
MPA ab a vdd vdd P_LVT w=1u l=.18u
MNA ab a vss vss N_LVT w=.5u l=.18u
MPB bb b vdd vdd P_LVT w=1u l=.18u
MNB bb b vss vss N_LVT w=.5u l=.18u
* D = AB + A'B' = A' XOR B. Static CMOS pull-down:
MN1 d ab n1 vss N_LVT w=1u l=.18u
MN2 n1 b vss vss N_LVT w=1u l=.18u
MN3 d a n2 vss N_LVT w=1u l=.18u
MN4 n2 bb vss vss N_LVT w=1u l=.18u
* Dual pull-up: (pAB || pB) series (pA || pBB).
MP1 vdd ab p1 vdd P_LVT w=2u l=.18u
MP2 vdd b p1 vdd P_LVT w=2u l=.18u
MP3 p1 a d vdd P_LVT w=2u l=.18u
MP4 p1 bb d vdd P_LVT w=2u l=.18u
* High-Vt NAND E has one unit of gate-delay slack.
MP5 e b vdd vdd P_HVT w=1u l=.18u
MP6 e c vdd vdd P_HVT w=1u l=.18u
MN5 e b ne vss N_HVT w=1u l=.18u
MN6 ne c vss vss N_HVT w=1u l=.18u
.ends dual_vt_logic
