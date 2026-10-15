* 2016 AND gate, initial AB=00
.protect
.lib 'D:/cic018.l' tt
.unprotect
.include 'and2.sp'
vvdd vdd 0 1.8
vvss vss 0 0
va a 0 pulse(0 1.8 5n .1n .1n 4n 10n)
vb b 0 pulse(0 1.8 5n .1n .1n 4n 10n)
XG a b f z vdd vss and2
CL z 0 1f
.temp 25
.option measform=3 measdgt=9 ingold=2 lis_new=1 delmax=2p
.tran 2p 32n 0 2p
.measure tran f_hl1 trig v(a) val=.9 rise=1 targ v(f) val=.9 fall=1
.measure tran f_lh1 trig v(a) val=.9 fall=1 targ v(f) val=.9 rise=1
.measure tran z_lh1 trig v(a) val=.9 rise=1 targ v(z) val=.9 rise=1
.measure tran z_hl1 trig v(a) val=.9 fall=1 targ v(z) val=.9 fall=1
.measure tran f_hl2 trig v(a) val=.9 rise=2 targ v(f) val=.9 fall=2
.measure tran f_lh2 trig v(a) val=.9 fall=2 targ v(f) val=.9 rise=2
.measure tran z_lh2 trig v(a) val=.9 rise=2 targ v(z) val=.9 rise=2
.measure tran z_hl2 trig v(a) val=.9 fall=2 targ v(z) val=.9 fall=2
.measure tran f_hl3 trig v(a) val=.9 rise=3 targ v(f) val=.9 fall=3
.measure tran f_lh3 trig v(a) val=.9 fall=3 targ v(f) val=.9 rise=3
.measure tran z_lh3 trig v(a) val=.9 rise=3 targ v(z) val=.9 rise=3
.measure tran z_hl3 trig v(a) val=.9 fall=3 targ v(z) val=.9 fall=3
.measure tran f_at_initial find v(f) at=4n
.measure tran f_at_11 find v(f) at=9n
.measure tran z_at_initial find v(z) at=4n
.measure tran z_at_11 find v(z) at=9n
.print tran v(a) v(b) v(f) v(z)
.end
