* Q1 illustrative topology verification only
.include 'dual_vt_logic.sp'
.model N_LVT NMOS LEVEL=1 VTO=.4 KP=100u
.model P_LVT PMOS LEVEL=1 VTO=-.4 KP=50u
.model N_HVT NMOS LEVEL=1 VTO=.6 KP=100u
.model P_HVT PMOS LEVEL=1 VTO=-.6 KP=50u
vvdd vdd 0 1.8
vvss vss 0 0
.temp 25
.option measform=3 measdgt=9
va a 0 pwl(
+ 0n 0 39.9n 0 40n 1.8
+)
vb b 0 pwl(
+ 0n 0 19.9n 0 20n 1.8 39.9n 1.8 40n 0
+ 59.9n 0 60n 1.8
+)
vc c 0 pwl(
+ 0n 0 9.9n 0 10n 1.8 19.9n 1.8 20n 0
+ 29.9n 0 30n 1.8 39.9n 1.8 40n 0 49.9n 0
+ 50n 1.8 59.9n 1.8 60n 0 69.9n 0 70n 1.8
+)
XL a b c d e vdd vss dual_vt_logic
CD d 0 1f
CE e 0 1f
.tran 10p 80n 0 10p
.measure tran d0 find v(d) at=8n
.measure tran e0 find v(e) at=8n
.measure tran d1 find v(d) at=18n
.measure tran e1 find v(e) at=18n
.measure tran d2 find v(d) at=28n
.measure tran e2 find v(e) at=28n
.measure tran d3 find v(d) at=38n
.measure tran e3 find v(e) at=38n
.measure tran d4 find v(d) at=48n
.measure tran e4 find v(e) at=48n
.measure tran d5 find v(d) at=58n
.measure tran e5 find v(e) at=58n
.measure tran d6 find v(d) at=68n
.measure tran e6 find v(e) at=68n
.measure tran d7 find v(d) at=78n
.measure tran e7 find v(e) at=78n
.end
