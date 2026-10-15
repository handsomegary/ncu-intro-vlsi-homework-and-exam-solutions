* 2020 HW2 Q2. Exactly one control input is zero (active-low one-hot).
* For c[k]=0, z[j] = a[(j+k+1) mod 4]. 16 TGs + 4 inverters = 40 MOS.
.subckt tg dat out c cb vdd vss
* A low c enables the PMOS; its inverted cb enables the NMOS.
MP out c dat vdd P_18 W=1u L=0.18u
MN out cb dat vss N_18 W=0.5u L=0.18u
.ends tg
.subckt inv inp out vdd vss
MP out inp vdd vdd P_18 W=1u L=0.18u
MN out inp vss vss N_18 W=0.5u L=0.18u
.ends inv
.subckt rotator a0 a1 a2 a3 c0 c1 c2 c3 z0 z1 z2 z3 vdd vss
XI0 c0 cb0 vdd vss inv
XI1 c1 cb1 vdd vss inv
XI2 c2 cb2 vdd vss inv
XI3 c3 cb3 vdd vss inv
X00 a1 z0 c0 cb0 vdd vss tg
X01 a2 z0 c1 cb1 vdd vss tg
X02 a3 z0 c2 cb2 vdd vss tg
X03 a0 z0 c3 cb3 vdd vss tg
X10 a2 z1 c0 cb0 vdd vss tg
X11 a3 z1 c1 cb1 vdd vss tg
X12 a0 z1 c2 cb2 vdd vss tg
X13 a1 z1 c3 cb3 vdd vss tg
X20 a3 z2 c0 cb0 vdd vss tg
X21 a0 z2 c1 cb1 vdd vss tg
X22 a1 z2 c2 cb2 vdd vss tg
X23 a2 z2 c3 cb3 vdd vss tg
X30 a0 z3 c0 cb0 vdd vss tg
X31 a1 z3 c1 cb1 vdd vss tg
X32 a2 z3 c2 cb2 vdd vss tg
X33 a3 z3 c3 cb3 vdd vss tg
.ends rotator
