* 2013 HW3 actual HSPICE, 1.8V TT 25C
.protect
.lib 'D:/cic018.l' TT
.unprotect
.option post=0 measform=3 measdgt=10 numdgt=10 ingold=2 delmax=1p
.temp 25
VDD vdd 0 1.8
* Positive intrinsic-channel-current overlap estimates direct through current.
.param LOAD=.1p
MP out vin vdd vdd P_18 W=20u L=.18u
MN out vin 0 0 N_18 W=10u L=.18u
CL out 0 'LOAD'
VIN vin 0 pulse(0 1.8 3n 3n 3n 7n 20n)
.data LOADS LOAD
.1p
.3p
.5p
.7p
1p
.enddata
.tran 1p 63n sweep data=LOADS
.meas tran capacitance param='LOAD'
.meas tran pdd avg par('-v(vdd)*i(VDD)') from=23n to=43n
.meas tran isc avg par('max(0,min(lx4(MP),lx4(MN)))') from=23n to=43n
.meas tran psc param='1.8*isc'
.meas tran esc integ par('1.8*max(0,min(lx4(MP),lx4(MN)))') from=23n to=43n
.meas tran high_level find v(out) at=42.9n
.meas tran low_level find v(out) at=32.9n
.end
