.testbench
.protect
.lib 'D:/cic018.l' tt
.include 'four_bit_multbased_adder.sp'
.unprotect

.global vdd vss
vvdd vdd 0 dc 1.8v
vvss vss 0 dc 0v
vx0 x0 0 pwl(0n 0 0.9n 0 1n 1.8 3.9n 1.8 4n 0 4.9n 0 5n 1.8 5.9n 1.8 6n 0)
vx1 x1 0 pwl(0n 0 1.9n 0 2n 1.8 3.9n 1.8 4n 0 4.9n 0 5n 1.8 5.9n 1.8 6n 0 6.9n 0 7n 1.8)
vx2 x2 0 pwl(0n 0 1.9n 0 2n 1.8 2.9n 1.8 3n 0 3.9n 0 4n 1.8 4.9n 1.8 5n 0 5.9n 0 6n 1.8 6.9n 1.8 7n 0 7.9n 0 8n 1.8)
vx3 x3 0 pwl(0n 0 1.9n 0 2n 1.8 3.9n 1.8 4n 0 5.9n 0 6n 1.8 6.9n 1.8 7n 0)
vy0 y0 0 pwl(0n 0 0.9n 0 1n 1.8 3.9n 1.8 4n 0 4.9n 0 5n 1.8 5.9n 1.8 6n 0 6.9n 0 7n 1.8 7.9n 1.8 8n 0)
vy1 y1 0 pwl(0n 0 4.9n 0 5n 1.8)
vy2 y2 0 pwl(0n 0 0.9n 0 1n 1.8 2.9n 1.8 3n 0 4.9n 0 5n 1.8 7.9n 1.8 8n 0)
vy3 y3 0 pwl(0n 0 1.9n 0 2n 1.8 4.9n 1.8 5n 0 5.9n 0 6n 1.8)
vcin cin 0 dc 0


XADDER CIN X0 X1 X2 X3 Y0 Y1 Y2 Y3 S0 S1 S2 S3 COUT four_bit_multbased_adder

.meas tran pwr avg power
.op
.tran 0.1ns 9n
.temp 25
.option post
.end