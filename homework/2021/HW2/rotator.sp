* Active-low one-hot 4-bit cyclic rotator.
* Legal controls: 0111,1011,1101,1110 (C3..C0).
* Invalid controls are unspecified; do not activate two data paths.
.subckt inv a z vdd vss
MP z a vdd vdd p_18 w=1u l=.18u
MN z a vss vss n_18 w=.5u l=.18u
.ends inv
.subckt tg a z cn cp vdd vss
MN z cn a vss n_18 w=.5u l=.18u
MP z cp a vdd p_18 w=1u l=.18u
.ends tg
.subckt rotate4 a0 a1 a2 a3 c0 c1 c2 c3 z0 z1 z2 z3 vdd vss
XI0 c0 cb0 vdd vss inv
XI1 c1 cb1 vdd vss inv
XI2 c2 cb2 vdd vss inv
XI3 c3 cb3 vdd vss inv
XT00 a0 z0 cb3 c3 vdd vss tg
XT01 a3 z0 cb2 c2 vdd vss tg
XT02 a2 z0 cb1 c1 vdd vss tg
XT03 a1 z0 cb0 c0 vdd vss tg
XT10 a1 z1 cb3 c3 vdd vss tg
XT11 a0 z1 cb2 c2 vdd vss tg
XT12 a3 z1 cb1 c1 vdd vss tg
XT13 a2 z1 cb0 c0 vdd vss tg
XT20 a2 z2 cb3 c3 vdd vss tg
XT21 a1 z2 cb2 c2 vdd vss tg
XT22 a0 z2 cb1 c1 vdd vss tg
XT23 a3 z2 cb0 c0 vdd vss tg
XT30 a3 z3 cb3 c3 vdd vss tg
XT31 a2 z3 cb2 c2 vdd vss tg
XT32 a1 z3 cb1 c1 vdd vss tg
XT33 a0 z3 cb0 c0 vdd vss tg
.ends rotate4
