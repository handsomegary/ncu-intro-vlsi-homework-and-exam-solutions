* Pseudo-NMOS NOR, WN/WP=4.5, equal L.
.subckt pseudo_nor a b z vdd vss
MP z vss vdd vdd p_18 w=1u l=.18u
MN0 z a vss vss n_18 w=4.5u l=.18u
MN1 z b vss vss n_18 w=4.5u l=.18u
.ends pseudo_nor
