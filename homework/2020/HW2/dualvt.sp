* 2020 HW2 Q1 topology. LVT/HVT are model labels, not CIC018 model aliases.
* Provide characterized N_LVT/P_LVT/N_HVT/P_HVT models before electrical use.
* All D-path MOSFETs are LVT; the four E NAND MOSFETs are HVT.
.subckt dualvt a b c d e vdd vss
MPA na a vdd vdd P_LVT W=1u L=0.18u
MNA na a vss vss N_LVT W=0.5u L=0.18u
MPB nb b vdd vdd P_LVT W=1u L=0.18u
MNB nb b vss vss N_LVT W=0.5u L=0.18u
* D = A XNOR B; PDN = A*nb + na*B, complementary PUN.
MND0 d a t0 vss N_LVT W=1u L=0.18u
MND1 t0 nb vss vss N_LVT W=1u L=0.18u
MND2 d na t1 vss N_LVT W=1u L=0.18u
MND3 t1 b vss vss N_LVT W=1u L=0.18u
MPD0 d a tp vdd P_LVT W=2u L=0.18u
MPD1 d nb tp vdd P_LVT W=2u L=0.18u
MPD2 tp na vdd vdd P_LVT W=2u L=0.18u
MPD3 tp b vdd vdd P_LVT W=2u L=0.18u
MPE0 e b vdd vdd P_HVT W=1u L=0.18u
MPE1 e c vdd vdd P_HVT W=1u L=0.18u
MNE0 e b te vss N_HVT W=1u L=0.18u
MNE1 te c vss vss N_HVT W=1u L=0.18u
.ends dualvt
