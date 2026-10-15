* 2021 HW2 functional simulation
.protect
.lib 'D:/cic018.l' tt
.unprotect
vvdd vdd 0 1.8
vvss vss 0 0
.temp 25
.option measform=3 measdgt=9
.include 'pseudo_nor.sp'
va a 0 pwl(
+ 0n 0 19.9n 0 20n 1.8
+)
vb b 0 pwl(
+ 0n 0 9.9n 0 10n 1.8 19.9n 1.8 20n 0
+ 29.9n 0 30n 1.8
+)
XN a b z vdd vss pseudo_nor
CL z 0 1f
.tran 10p 40n 0 10p
.measure tran v0 find v(z) at=8n
.measure tran v1 find v(z) at=18n
.measure tran v2 find v(z) at=28n
.measure tran v3 find v(z) at=38n
.end
