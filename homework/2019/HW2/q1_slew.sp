* HW2 Q1: illustrative process simulation, not specified assignment sizes.
.protect
.lib 'D:/cic018.l' TT
.unprotect
.option post=0 measform=3 measdgt=10 numdgt=10 delmax=1p
.temp 25
.param SLEW=100p
VDD vdd 0 1.8
VIN in 0 pwl(0 0 1n 0 '1n+SLEW' 1.8 5n 1.8)
MP out in vdd vdd P_18 W=1u L=.18u
MN out in 0 0 N_18 W=.5u L=.18u
CL out 0 10f
.data SLEWS SLEW
100p
1n
.enddata
.tran 1p 5n sweep data=SLEWS
.meas tran slew_value param='SLEW'
.meas tran t90 when v(out)=1.62 fall=1
.meas tran t10 when v(out)=.18 fall=1
.meas tran tf param='t10-t90'
.meas tran vin50 when v(in)=.9 rise=1
.meas tran out50 when v(out)=.9 fall=1
.meas tran delay50 param='out50-vin50'
.end
