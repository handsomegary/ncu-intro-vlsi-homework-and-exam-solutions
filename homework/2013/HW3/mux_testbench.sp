* 2013 HW3 actual HSPICE, 1.8V TT 25C
.protect
.lib 'D:/cic018.l' TT
.unprotect
.option post=0 measform=3 measdgt=10 numdgt=10 ingold=2 delmax=1p
.temp 25
VDD vdd 0 1.8
.include 'mux.sp'
.param a0a=0 a0b=0 a1a=0 a1b=0 a2a=0 a2b=0 a3a=0 a3b=0 a4a=0 a4b=0 a5a=0 a5b=0 a6a=0 a6b=0 a7a=0 a7b=0 s0v=0 s1v=0 s2v=0
VS0 s0 0 's0v'
VS1 s1 0 's1v'
VS2 s2 0 's2v'
VA0 a0 0 pwl(0 'a0a' 1n 'a0a' 1.02n 'a0b' 3n 'a0b')
VA1 a1 0 pwl(0 'a1a' 1n 'a1a' 1.02n 'a1b' 3n 'a1b')
VA2 a2 0 pwl(0 'a2a' 1n 'a2a' 1.02n 'a2b' 3n 'a2b')
VA3 a3 0 pwl(0 'a3a' 1n 'a3a' 1.02n 'a3b' 3n 'a3b')
VA4 a4 0 pwl(0 'a4a' 1n 'a4a' 1.02n 'a4b' 3n 'a4b')
VA5 a5 0 pwl(0 'a5a' 1n 'a5a' 1.02n 'a5b' 3n 'a5b')
VA6 a6 0 pwl(0 'a6a' 1n 'a6a' 1.02n 'a6b' 3n 'a6b')
VA7 a7 0 pwl(0 'a7a' 1n 'a7a' 1.02n 'a7b' 3n 'a7b')
VREF ref 0 pwl(0 0 1n 0 1.02n 1.8 3n 1.8)
Xbaseline a0 a1 a2 a3 a4 a5 a6 a7 s0 s1 s2 z_baseline vdd 0 baseline
CL_baseline z_baseline 0 10f
Xtree a0 a1 a2 a3 a4 a5 a6 a7 s0 s1 s2 z_tree vdd 0 tree
CL_tree z_tree 0 10f
.data CASES caseid a0a a0b a1a a1b a2a a2b a3a a3b a4a a4b a5a a5b a6a a6b a7a a7b s0v s1v s2v
1 0 1.8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 1.8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 1.8 0 0 0 0 0 0 0 0 0 0 0 0 1.8 0 0
4 0 0 1.8 0 0 0 0 0 0 0 0 0 0 0 0 0 1.8 0 0
5 0 0 0 0 0 1.8 0 0 0 0 0 0 0 0 0 0 0 1.8 0
6 0 0 0 0 1.8 0 0 0 0 0 0 0 0 0 0 0 0 1.8 0
7 0 0 0 0 0 0 0 1.8 0 0 0 0 0 0 0 0 1.8 1.8 0
8 0 0 0 0 0 0 1.8 0 0 0 0 0 0 0 0 0 1.8 1.8 0
9 0 0 0 0 0 0 0 0 0 1.8 0 0 0 0 0 0 0 0 1.8
10 0 0 0 0 0 0 0 0 1.8 0 0 0 0 0 0 0 0 0 1.8
11 0 0 0 0 0 0 0 0 0 0 0 1.8 0 0 0 0 1.8 0 1.8
12 0 0 0 0 0 0 0 0 0 0 1.8 0 0 0 0 0 1.8 0 1.8
13 0 0 0 0 0 0 0 0 0 0 0 0 0 1.8 0 0 0 1.8 1.8
14 0 0 0 0 0 0 0 0 0 0 0 0 1.8 0 0 0 0 1.8 1.8
15 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.8 1.8 1.8 1.8
16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.8 0 1.8 1.8 1.8
.enddata
.tran 1p 3n sweep data=CASES
.meas tran pre_baseline find v(z_baseline) at=.9n
.meas tran post_baseline find v(z_baseline) at=2.9n
.meas tran d_baseline trig v(ref) val=.9 rise=1 targ v(z_baseline) val=.9 cross=last
.meas tran pre_tree find v(z_tree) at=.9n
.meas tran post_tree find v(z_tree) at=2.9n
.meas tran d_tree trig v(ref) val=.9 rise=1 targ v(z_tree) val=.9 cross=last
.end
