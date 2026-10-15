* 2017 full-adder verification
.protect
.lib 'D:/cic018.l' tt
.unprotect
vvdd vdd 0 1.8
vvss vss 0 0
.temp 25
.option ingold=2 lis_new=1 numdgt=8 delmax=2p
.include 'domino_full_adder.sp'
.param WPSS=3.10827u
.param WPSC=2.49524u
va a 0 pwl(
+ 0n 0 1n 0 1.1n 0 11n 0 11.1n 0
+ 21n 0 21.1n 0 31n 0 31.1n 0 41n 0
+ 41.1n 1.8 51n 1.8 51.1n 1.8 61n 1.8 61.1n 1.8
+ 71n 1.8 71.1n 1.8
+)
vb b 0 pwl(
+ 0n 0 1n 0 1.1n 0 11n 0 11.1n 0
+ 21n 0 21.1n 1.8 31n 1.8 31.1n 1.8 41n 1.8
+ 41.1n 0 51n 0 51.1n 0 61n 0 61.1n 1.8
+ 71n 1.8 71.1n 1.8
+)
vc c 0 pwl(
+ 0n 0 1n 0 1.1n 0 11n 0 11.1n 1.8
+ 21n 1.8 21.1n 0 31n 0 31.1n 1.8 41n 1.8
+ 41.1n 0 51n 0 51.1n 1.8 61n 1.8 61.1n 0
+ 71n 0 71.1n 1.8
+)
vclk clk 0 pulse(0 1.8 5n .1n .1n 4n 10n)
XF a b c clk s co vdd vss domino_fa
CLS s 0 1f
CLC co 0 1f
.tran 2p 82n
.print tran v(a) v(b) v(c) v(s) v(co)
.end
