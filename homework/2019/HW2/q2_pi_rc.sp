* HW2 Q2: fixed-size ideal pi-RC networks, no process-model substitution.
.option post=0 measform=3 measdgt=10 numdgt=10 delmax=50f
VR rail 0 1.8
RP1_1 rail r1_1 1k
CP1_1 r1_1 0 2f
RN1 f1 0 1k
CN1 f1 0 2f
.meas tran tau_r1 integ par('1-v(r1_1)/1.8') from=0 to=5n
.meas tran tau_f1 integ par('v(f1)/1.8') from=0 to=5n
.meas tran r1_10 when v(r1_1)=0.18 rise=1
.meas tran f1_10 when v(f1)=0.18 fall=1
.meas tran r1_90 when v(r1_1)=1.62 rise=1
.meas tran f1_90 when v(f1)=1.62 fall=1
.meas tran tr1 param='r1_90-r1_10'
.meas tran tf1 param='f1_10-f1_90'
RP2_1 rail r2_1 1k
CP2_1 r2_1 0 2f
RP2_2 r2_1 r2_2 1k
CP2_2 r2_2 0 3f
RN2 f2 0 1k
CN2 f2 0 3f
.meas tran tau_r2 integ par('1-v(r2_2)/1.8') from=0 to=5n
.meas tran tau_f2 integ par('v(f2)/1.8') from=0 to=5n
.meas tran r2_10 when v(r2_2)=0.18 rise=1
.meas tran f2_10 when v(f2)=0.18 fall=1
.meas tran r2_90 when v(r2_2)=1.62 rise=1
.meas tran f2_90 when v(f2)=1.62 fall=1
.meas tran tr2 param='r2_90-r2_10'
.meas tran tf2 param='f2_10-f2_90'
RP3_1 rail r3_1 1k
CP3_1 r3_1 0 2f
RP3_2 r3_1 r3_2 1k
CP3_2 r3_2 0 2f
RP3_3 r3_2 r3_3 1k
CP3_3 r3_3 0 4f
RN3 f3 0 1k
CN3 f3 0 4f
.meas tran tau_r3 integ par('1-v(r3_3)/1.8') from=0 to=5n
.meas tran tau_f3 integ par('v(f3)/1.8') from=0 to=5n
.meas tran r3_10 when v(r3_3)=0.18 rise=1
.meas tran f3_10 when v(f3)=0.18 fall=1
.meas tran r3_90 when v(r3_3)=1.62 rise=1
.meas tran f3_90 when v(f3)=1.62 fall=1
.meas tran tr3 param='r3_90-r3_10'
.meas tran tf3 param='f3_10-f3_90'
RP4_1 rail r4_1 1k
CP4_1 r4_1 0 2f
RP4_2 r4_1 r4_2 1k
CP4_2 r4_2 0 2f
RP4_3 r4_2 r4_3 1k
CP4_3 r4_3 0 2f
RP4_4 r4_3 r4_4 1k
CP4_4 r4_4 0 5f
RN4 f4 0 1k
CN4 f4 0 5f
.meas tran tau_r4 integ par('1-v(r4_4)/1.8') from=0 to=5n
.meas tran tau_f4 integ par('v(f4)/1.8') from=0 to=5n
.meas tran r4_10 when v(r4_4)=0.18 rise=1
.meas tran f4_10 when v(f4)=0.18 fall=1
.meas tran r4_90 when v(r4_4)=1.62 rise=1
.meas tran f4_90 when v(f4)=1.62 fall=1
.meas tran tr4 param='r4_90-r4_10'
.meas tran tf4 param='f4_10-f4_90'
RP5_1 rail r5_1 1k
CP5_1 r5_1 0 2f
RP5_2 r5_1 r5_2 1k
CP5_2 r5_2 0 2f
RP5_3 r5_2 r5_3 1k
CP5_3 r5_3 0 2f
RP5_4 r5_3 r5_4 1k
CP5_4 r5_4 0 2f
RP5_5 r5_4 r5_5 1k
CP5_5 r5_5 0 6f
RN5 f5 0 1k
CN5 f5 0 6f
.meas tran tau_r5 integ par('1-v(r5_5)/1.8') from=0 to=5n
.meas tran tau_f5 integ par('v(f5)/1.8') from=0 to=5n
.meas tran r5_10 when v(r5_5)=0.18 rise=1
.meas tran f5_10 when v(f5)=0.18 fall=1
.meas tran r5_90 when v(r5_5)=1.62 rise=1
.meas tran f5_90 when v(f5)=1.62 fall=1
.meas tran tr5 param='r5_90-r5_10'
.meas tran tf5 param='f5_10-f5_90'
RP6_1 rail r6_1 1k
CP6_1 r6_1 0 2f
RP6_2 r6_1 r6_2 1k
CP6_2 r6_2 0 2f
RP6_3 r6_2 r6_3 1k
CP6_3 r6_3 0 2f
RP6_4 r6_3 r6_4 1k
CP6_4 r6_4 0 2f
RP6_5 r6_4 r6_5 1k
CP6_5 r6_5 0 2f
RP6_6 r6_5 r6_6 1k
CP6_6 r6_6 0 7f
RN6 f6 0 1k
CN6 f6 0 7f
.meas tran tau_r6 integ par('1-v(r6_6)/1.8') from=0 to=5n
.meas tran tau_f6 integ par('v(f6)/1.8') from=0 to=5n
.meas tran r6_10 when v(r6_6)=0.18 rise=1
.meas tran f6_10 when v(f6)=0.18 fall=1
.meas tran r6_90 when v(r6_6)=1.62 rise=1
.meas tran f6_90 when v(f6)=1.62 fall=1
.meas tran tr6 param='r6_90-r6_10'
.meas tran tf6 param='f6_10-f6_90'
RP7_1 rail r7_1 1k
CP7_1 r7_1 0 2f
RP7_2 r7_1 r7_2 1k
CP7_2 r7_2 0 2f
RP7_3 r7_2 r7_3 1k
CP7_3 r7_3 0 2f
RP7_4 r7_3 r7_4 1k
CP7_4 r7_4 0 2f
RP7_5 r7_4 r7_5 1k
CP7_5 r7_5 0 2f
RP7_6 r7_5 r7_6 1k
CP7_6 r7_6 0 2f
RP7_7 r7_6 r7_7 1k
CP7_7 r7_7 0 8f
RN7 f7 0 1k
CN7 f7 0 8f
.meas tran tau_r7 integ par('1-v(r7_7)/1.8') from=0 to=5n
.meas tran tau_f7 integ par('v(f7)/1.8') from=0 to=5n
.meas tran r7_10 when v(r7_7)=0.18 rise=1
.meas tran f7_10 when v(f7)=0.18 fall=1
.meas tran r7_90 when v(r7_7)=1.62 rise=1
.meas tran f7_90 when v(f7)=1.62 fall=1
.meas tran tr7 param='r7_90-r7_10'
.meas tran tf7 param='f7_10-f7_90'
RP8_1 rail r8_1 1k
CP8_1 r8_1 0 2f
RP8_2 r8_1 r8_2 1k
CP8_2 r8_2 0 2f
RP8_3 r8_2 r8_3 1k
CP8_3 r8_3 0 2f
RP8_4 r8_3 r8_4 1k
CP8_4 r8_4 0 2f
RP8_5 r8_4 r8_5 1k
CP8_5 r8_5 0 2f
RP8_6 r8_5 r8_6 1k
CP8_6 r8_6 0 2f
RP8_7 r8_6 r8_7 1k
CP8_7 r8_7 0 2f
RP8_8 r8_7 r8_8 1k
CP8_8 r8_8 0 9f
RN8 f8 0 1k
CN8 f8 0 9f
.meas tran tau_r8 integ par('1-v(r8_8)/1.8') from=0 to=5n
.meas tran tau_f8 integ par('v(f8)/1.8') from=0 to=5n
.meas tran r8_10 when v(r8_8)=0.18 rise=1
.meas tran f8_10 when v(f8)=0.18 fall=1
.meas tran r8_90 when v(r8_8)=1.62 rise=1
.meas tran f8_90 when v(f8)=1.62 fall=1
.meas tran tr8 param='r8_90-r8_10'
.meas tran tf8 param='f8_10-f8_90'
.ic v(r1_1)=0 v(f1)=1.8 v(r2_1)=0 v(r2_2)=0 v(f2)=1.8 v(r3_1)=0 v(r3_2)=0 v(r3_3)=0 v(f3)=1.8 v(r4_1)=0 v(r4_2)=0 v(r4_3)=0 v(r4_4)=0 v(f4)=1.8 v(r5_1)=0 v(r5_2)=0 v(r5_3)=0 v(r5_4)=0 v(r5_5)=0 v(f5)=1.8 v(r6_1)=0 v(r6_2)=0 v(r6_3)=0 v(r6_4)=0 v(r6_5)=0 v(r6_6)=0 v(f6)=1.8 v(r7_1)=0 v(r7_2)=0 v(r7_3)=0 v(r7_4)=0 v(r7_5)=0 v(r7_6)=0 v(r7_7)=0 v(f7)=1.8 v(r8_1)=0 v(r8_2)=0 v(r8_3)=0 v(r8_4)=0 v(r8_5)=0 v(r8_6)=0 v(r8_7)=0 v(r8_8)=0 v(f8)=1.8
.tran 50f 5n UIC
.end
