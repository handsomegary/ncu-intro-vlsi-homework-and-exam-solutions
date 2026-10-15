* 2024 HW4: single-DUT pre-layout SPICE verification only
* Original instructor PWL inputs preserved; no layout/PEX is claimed.
.protect
.lib 'D:/cic018.l' TT
.unprotect
.include 'four_bit_multbased_adder.sp'
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
.temp 25
.option post=0 measform=3 measdgt=9 numdgt=10 delmax=1p
.tran 1p 9n
.meas tran pavg avg power from=0 to=9n
.meas tran energy integ power from=0 to=9n
.meas tran supply_pavg avg par('-v(vdd)*i(vvdd)') from=0 to=9n
.meas tran v1_s0 find v(s0) at=1.8n
.meas tran v1_s1 find v(s1) at=1.8n
.meas tran v1_s2 find v(s2) at=1.8n
.meas tran v1_s3 find v(s3) at=1.8n
.meas tran v1_cout find v(cout) at=1.8n
.meas tran v2_s0 find v(s0) at=2.8n
.meas tran v2_s1 find v(s1) at=2.8n
.meas tran v2_s2 find v(s2) at=2.8n
.meas tran v2_s3 find v(s3) at=2.8n
.meas tran v2_cout find v(cout) at=2.8n
.meas tran v3_s0 find v(s0) at=3.8n
.meas tran v3_s1 find v(s1) at=3.8n
.meas tran v3_s2 find v(s2) at=3.8n
.meas tran v3_s3 find v(s3) at=3.8n
.meas tran v3_cout find v(cout) at=3.8n
.meas tran v4_s0 find v(s0) at=4.8n
.meas tran v4_s1 find v(s1) at=4.8n
.meas tran v4_s2 find v(s2) at=4.8n
.meas tran v4_s3 find v(s3) at=4.8n
.meas tran v4_cout find v(cout) at=4.8n
.meas tran v5_s0 find v(s0) at=5.8n
.meas tran v5_s1 find v(s1) at=5.8n
.meas tran v5_s2 find v(s2) at=5.8n
.meas tran v5_s3 find v(s3) at=5.8n
.meas tran v5_cout find v(cout) at=5.8n
.meas tran v6_s0 find v(s0) at=6.8n
.meas tran v6_s1 find v(s1) at=6.8n
.meas tran v6_s2 find v(s2) at=6.8n
.meas tran v6_s3 find v(s3) at=6.8n
.meas tran v6_cout find v(cout) at=6.8n
.meas tran v7_s0 find v(s0) at=7.8n
.meas tran v7_s1 find v(s1) at=7.8n
.meas tran v7_s2 find v(s2) at=7.8n
.meas tran v7_s3 find v(s3) at=7.8n
.meas tran v7_cout find v(cout) at=7.8n
.meas tran v8_s0 find v(s0) at=8.8n
.meas tran v8_s1 find v(s1) at=8.8n
.meas tran v8_s2 find v(s2) at=8.8n
.meas tran v8_s3 find v(s3) at=8.8n
.meas tran v8_cout find v(cout) at=8.8n
.end
