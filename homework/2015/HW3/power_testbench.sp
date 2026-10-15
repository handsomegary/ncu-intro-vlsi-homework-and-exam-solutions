* 2015 reproducible schematic simulation
.protect
.lib 'D:/cic018.l' TT
.unprotect
.option post=0 lis_new=1 ingold=2 numdgt=10 measdgt=10 measform=3 delmax=2p
.temp 25
VIN a 0 PULSE(0 1.8 0 3n 3n 47n 100n)
VDD0 dd0 0 1.8
MP0 pd0 a dd0 dd0 P_18 W=1.88u L=0.18u
VP0 pd0 out0 0
VN0 out0 nd0 0
MN0 nd0 a 0 0 N_18 W=.47u L=.18u
CL0 out0 0 0.1p
EIP0 icp0 0 VOL='LX4(MP0)'
EIN0 icn0 0 VOL='LX4(MN0)'
.measure tran isc0 AVG PAR('max(0,min(LX4(MP0),LX4(MN0)))') FROM=200n TO=300n
.measure tran erise0 INTEG PAR('1.8*max(0,min(LX4(MP0),LX4(MN0)))') FROM=200n TO=203n
.measure tran efall0 INTEG PAR('1.8*max(0,min(LX4(MP0),LX4(MN0)))') FROM=250n TO=253n
.measure tran ecycle0 INTEG PAR('1.8*max(0,min(LX4(MP0),LX4(MN0)))') FROM=200n TO=300n
.measure tran psupply0 AVG PAR('-1.8*I(VDD0)') FROM=200n TO=300n
.measure tran high0 FIND V(out0) AT=299n
.measure tran low0 FIND V(out0) AT=249n
VDD1 dd1 0 1.8
MP1 pd1 a dd1 dd1 P_18 W=1.88u L=0.18u
VP1 pd1 out1 0
VN1 out1 nd1 0
MN1 nd1 a 0 0 N_18 W=.47u L=.18u
CL1 out1 0 0.3p
EIP1 icp1 0 VOL='LX4(MP1)'
EIN1 icn1 0 VOL='LX4(MN1)'
.measure tran isc1 AVG PAR('max(0,min(LX4(MP1),LX4(MN1)))') FROM=200n TO=300n
.measure tran erise1 INTEG PAR('1.8*max(0,min(LX4(MP1),LX4(MN1)))') FROM=200n TO=203n
.measure tran efall1 INTEG PAR('1.8*max(0,min(LX4(MP1),LX4(MN1)))') FROM=250n TO=253n
.measure tran ecycle1 INTEG PAR('1.8*max(0,min(LX4(MP1),LX4(MN1)))') FROM=200n TO=300n
.measure tran psupply1 AVG PAR('-1.8*I(VDD1)') FROM=200n TO=300n
.measure tran high1 FIND V(out1) AT=299n
.measure tran low1 FIND V(out1) AT=249n
VDD2 dd2 0 1.8
MP2 pd2 a dd2 dd2 P_18 W=1.88u L=0.18u
VP2 pd2 out2 0
VN2 out2 nd2 0
MN2 nd2 a 0 0 N_18 W=.47u L=.18u
CL2 out2 0 0.5p
EIP2 icp2 0 VOL='LX4(MP2)'
EIN2 icn2 0 VOL='LX4(MN2)'
.measure tran isc2 AVG PAR('max(0,min(LX4(MP2),LX4(MN2)))') FROM=200n TO=300n
.measure tran erise2 INTEG PAR('1.8*max(0,min(LX4(MP2),LX4(MN2)))') FROM=200n TO=203n
.measure tran efall2 INTEG PAR('1.8*max(0,min(LX4(MP2),LX4(MN2)))') FROM=250n TO=253n
.measure tran ecycle2 INTEG PAR('1.8*max(0,min(LX4(MP2),LX4(MN2)))') FROM=200n TO=300n
.measure tran psupply2 AVG PAR('-1.8*I(VDD2)') FROM=200n TO=300n
.measure tran high2 FIND V(out2) AT=299n
.measure tran low2 FIND V(out2) AT=249n
VDD3 dd3 0 1.8
MP3 pd3 a dd3 dd3 P_18 W=1.88u L=0.18u
VP3 pd3 out3 0
VN3 out3 nd3 0
MN3 nd3 a 0 0 N_18 W=.47u L=.18u
CL3 out3 0 0.7p
EIP3 icp3 0 VOL='LX4(MP3)'
EIN3 icn3 0 VOL='LX4(MN3)'
.measure tran isc3 AVG PAR('max(0,min(LX4(MP3),LX4(MN3)))') FROM=200n TO=300n
.measure tran erise3 INTEG PAR('1.8*max(0,min(LX4(MP3),LX4(MN3)))') FROM=200n TO=203n
.measure tran efall3 INTEG PAR('1.8*max(0,min(LX4(MP3),LX4(MN3)))') FROM=250n TO=253n
.measure tran ecycle3 INTEG PAR('1.8*max(0,min(LX4(MP3),LX4(MN3)))') FROM=200n TO=300n
.measure tran psupply3 AVG PAR('-1.8*I(VDD3)') FROM=200n TO=300n
.measure tran high3 FIND V(out3) AT=299n
.measure tran low3 FIND V(out3) AT=249n
VDD4 dd4 0 1.8
MP4 pd4 a dd4 dd4 P_18 W=1.88u L=0.18u
VP4 pd4 out4 0
VN4 out4 nd4 0
MN4 nd4 a 0 0 N_18 W=.47u L=.18u
CL4 out4 0 1p
EIP4 icp4 0 VOL='LX4(MP4)'
EIN4 icn4 0 VOL='LX4(MN4)'
.measure tran isc4 AVG PAR('max(0,min(LX4(MP4),LX4(MN4)))') FROM=200n TO=300n
.measure tran erise4 INTEG PAR('1.8*max(0,min(LX4(MP4),LX4(MN4)))') FROM=200n TO=203n
.measure tran efall4 INTEG PAR('1.8*max(0,min(LX4(MP4),LX4(MN4)))') FROM=250n TO=253n
.measure tran ecycle4 INTEG PAR('1.8*max(0,min(LX4(MP4),LX4(MN4)))') FROM=200n TO=300n
.measure tran psupply4 AVG PAR('-1.8*I(VDD4)') FROM=200n TO=300n
.measure tran high4 FIND V(out4) AT=299n
.measure tran low4 FIND V(out4) AT=249n
.tran 2p 300n
.print tran V(a) V(out0) V(icp0) V(icn0) I(VDD0) V(out1) V(icp1) V(icn1) I(VDD1) V(out2) V(icp2) V(icn2) I(VDD2) V(out3) V(icp3) V(icn3) I(VDD3) V(out4) V(icp4) V(icn4) I(VDD4)
.end
