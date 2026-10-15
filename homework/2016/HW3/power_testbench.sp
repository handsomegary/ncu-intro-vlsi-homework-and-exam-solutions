* Inverter direct-path power versus CLOAD
.protect
.lib 'D:/cic018.l' tt
.unprotect
vvdd vdd 0 1.8
vin in 0 pulse(0 1.8 5n 3n 3n 40n 86n)
MP out in vdd vdd P_18 W=1.44u L=.18u
MN out in 0 0 N_18 W=.36u L=.18u
CL out 0 CLOAD
.temp 25
.option measform=3 measdgt=9 delmax=10p
.param CLOAD=.1p
.data capvals CLOAD
.1p
.3p
.5p
.7p
1p
.enddata
.tran 10p 180n sweep DATA=capvals
.measure tran isc AVG PAR('max(0,min(lx4(mp),lx4(mn)))') from=91n to=177n
.measure tran peaksc MAX PAR('max(0,min(lx4(mp),lx4(mn)))') from=91n to=177n
.measure tran ptotal AVG PAR('-1.8*i(vvdd)') from=91n to=177n
.measure tran psc PARAM='1.8*isc'
.measure tran elsc PARAM='psc*86n'
.measure tran out_high FIND v(out) at=175n
.measure tran out_low FIND v(out) at=125n
.end
