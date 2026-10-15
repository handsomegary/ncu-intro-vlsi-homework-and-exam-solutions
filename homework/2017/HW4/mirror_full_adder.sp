* 28T mirror full adder. Explicit VDD/VSS and bulk terminals.
.param WOSC=2.017930000u WOSS=2.727010000u
.subckt mirror_fa a b c s co vdd vss
* Complementary carry node cb = NOT(AB + C(A+B)).
MPA1 cp1 a vdd vdd P_18 w=3.6u l=.18u
MPB1 cp1 b vdd vdd P_18 w=3.6u l=.18u
MPC1 cb c cp1 vdd P_18 w=3.6u l=.18u
MPA2 cp2 a vdd vdd P_18 w=3.6u l=.18u
MPB2 cb b cp2 vdd P_18 w=3.6u l=.18u
MNA1 cn1 a vss vss N_18 w=1.2u l=.18u
MNB1 cn1 b vss vss N_18 w=1.2u l=.18u
MNC1 cb c cn1 vss N_18 w=1.2u l=.18u
MNA2 cn2 a vss vss N_18 w=1.2u l=.18u
MNB2 cb b cn2 vss N_18 w=1.2u l=.18u
* Complementary sum: discharge predicate cb(A+B+C)+ABC.
MPA3 sp1 a vdd vdd P_18 w=3.6u l=.18u
MPB3 sp1 b vdd vdd P_18 w=3.6u l=.18u
MPC2 sp1 c vdd vdd P_18 w=3.6u l=.18u
MPU sb cb sp1 vdd P_18 w=3.6u l=.18u
MPA4 sp2 a vdd vdd P_18 w=5.4u l=.18u
MPB4 sp3 b sp2 vdd P_18 w=5.4u l=.18u
MPC3 sb c sp3 vdd P_18 w=5.4u l=.18u
MNA3 sn1 a vss vss N_18 w=1.2u l=.18u
MNB3 sn1 b vss vss N_18 w=1.2u l=.18u
MNC2 sn1 c vss vss N_18 w=1.2u l=.18u
MND sb cb sn1 vss N_18 w=1.2u l=.18u
MNA4 sn2 a vss vss N_18 w=1.8u l=.18u
MNB4 sn3 b sn2 vss N_18 w=1.8u l=.18u
MNC3 sb c sn3 vss N_18 w=1.8u l=.18u
* Separately calibrated output inverters.
MPOC co cb vdd vdd P_18 w=WOSC l=.18u
MNOC co cb vss vss N_18 w=.6u l=.18u
MPOS s sb vdd vdd P_18 w=WOSS l=.18u
MNOS s sb vss vss N_18 w=.6u l=.18u
.ends mirror_fa
