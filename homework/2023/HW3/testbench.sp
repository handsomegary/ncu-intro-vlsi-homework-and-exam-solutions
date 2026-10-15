* 2023 HW3: TT, 1.8V, 25C; model remains external.
.protect
.lib 'D:/cic018.l' TT
.unprotect
.include 'rca.sp'
VDD vdd 0 1.8
.option post=0 measform=3 measdgt=10 numdgt=10 delmax=2p
.temp 25
XADD cin x0 x1 x2 y0 y1 y2 s0 s1 s2 cout vdd 0 rca
Cs0 s0 0 1f
Cs1 s1 0 1f
Cs2 s2 0 1f
Ccout cout 0 1f
Vx0 x0 0 pwl(
+ 0n 0 3n 0 3.02n 1.8 6n 1.8 6.02n 0 9n 0 9.02n 1.8 12n 1.8
+ 12.02n 0 15n 0 15.02n 1.8 18n 1.8 18.02n 0 21n 0 21.02n 1.8 24n 1.8
+ 24.02n 0 27n 0 27.02n 1.8 30n 1.8 30.02n 0 33n 0 33.02n 1.8 36n 1.8
+ 36.02n 0 39n 0 39.02n 1.8 42n 1.8 42.02n 0 45n 0 45.02n 1.8 48n 1.8
+ 48.02n 0 51n 0 51.02n 1.8 54n 1.8 54.02n 0 57n 0 57.02n 1.8 60n 1.8
+ 60.02n 0 63n 0 63.02n 1.8 66n 1.8 66.02n 0 69n 0 69.02n 1.8 72n 1.8
+ 72.02n 0 75n 0 75.02n 1.8 78n 1.8 78.02n 0 81n 0 81.02n 1.8 84n 1.8
+ 84.02n 0 87n 0 87.02n 1.8 90n 1.8 90.02n 0 93n 0 93.02n 1.8 96n 1.8
+ 96.02n 0 99n 0 99.02n 1.8 102n 1.8 102.02n 0 105n 0 105.02n 1.8 108n 1.8
+ 108.02n 0 111n 0 111.02n 1.8 114n 1.8 114.02n 0 117n 0 117.02n 1.8 120n 1.8
+ 120.02n 0 123n 0 123.02n 1.8 126n 1.8 126.02n 0 129n 0 129.02n 1.8 132n 1.8
+ 132.02n 0 135n 0 135.02n 1.8 138n 1.8 138.02n 0 141n 0 141.02n 1.8 144n 1.8
+ 144.02n 0 147n 0 147.02n 1.8 150n 1.8 150.02n 0 153n 0 153.02n 1.8 156n 1.8
+ 156.02n 0 159n 0 159.02n 1.8 162n 1.8 162.02n 0 165n 0 165.02n 1.8 168n 1.8
+ 168.02n 0 171n 0 171.02n 1.8 174n 1.8 174.02n 0 177n 0 177.02n 1.8 180n 1.8
+ 180.02n 0 183n 0 183.02n 1.8 186n 1.8 186.02n 0 189n 0 189.02n 1.8 192n 1.8
+ 192.02n 0 195n 0 195.02n 1.8 198n 1.8 198.02n 0 201n 0 201.02n 1.8 204n 1.8
+ 204.02n 0 207n 0 207.02n 1.8 210n 1.8 210.02n 0 213n 0 213.02n 1.8 216n 1.8
+ 216.02n 0 219n 0 219.02n 1.8 222n 1.8 222.02n 0 225n 0 225.02n 1.8 228n 1.8
+ 228.02n 0 231n 0 231.02n 1.8 234n 1.8 234.02n 0 237n 0 237.02n 1.8 240n 1.8
+ 240.02n 0 243n 0 243.02n 1.8 246n 1.8 246.02n 0 249n 0 249.02n 1.8 252n 1.8
+ 252.02n 0 255n 0 255.02n 1.8 258n 1.8 258.02n 0 261n 0 261.02n 1.8 264n 1.8
+ 264.02n 0 267n 0 267.02n 1.8 270n 1.8 270.02n 0 273n 0 273.02n 1.8 276n 1.8
+ 276.02n 0 279n 0 279.02n 1.8 282n 1.8 282.02n 0 285n 0 285.02n 1.8 288n 1.8
+ 288.02n 0 291n 0 291.02n 1.8 294n 1.8 294.02n 0 297n 0 297.02n 1.8 300n 1.8
+ 300.02n 0 303n 0 303.02n 1.8 306n 1.8 306.02n 0 309n 0 309.02n 1.8 312n 1.8
+ 312.02n 0 315n 0 315.02n 1.8 318n 1.8 318.02n 0 321n 0 321.02n 1.8 324n 1.8
+ 324.02n 0 327n 0 327.02n 1.8 330n 1.8 330.02n 0 333n 0 333.02n 1.8 336n 1.8
+ 336.02n 0 339n 0 339.02n 1.8 342n 1.8 342.02n 0 345n 0 345.02n 1.8 348n 1.8
+ 348.02n 0 351n 0 351.02n 1.8 354n 1.8 354.02n 0 357n 0 357.02n 1.8 360n 1.8
+ 360.02n 0 363n 0 363.02n 1.8 366n 1.8 366.02n 0 369n 0 369.02n 1.8 372n 1.8
+ 372.02n 0 375n 0 375.02n 1.8 378n 1.8 378.02n 0 381n 0 381.02n 1.8
+)
Vx1 x1 0 pwl(
+ 0n 0 6n 0 6.02n 1.8 12n 1.8 12.02n 0 18n 0 18.02n 1.8 24n 1.8
+ 24.02n 0 30n 0 30.02n 1.8 36n 1.8 36.02n 0 42n 0 42.02n 1.8 48n 1.8
+ 48.02n 0 54n 0 54.02n 1.8 60n 1.8 60.02n 0 66n 0 66.02n 1.8 72n 1.8
+ 72.02n 0 78n 0 78.02n 1.8 84n 1.8 84.02n 0 90n 0 90.02n 1.8 96n 1.8
+ 96.02n 0 102n 0 102.02n 1.8 108n 1.8 108.02n 0 114n 0 114.02n 1.8 120n 1.8
+ 120.02n 0 126n 0 126.02n 1.8 132n 1.8 132.02n 0 138n 0 138.02n 1.8 144n 1.8
+ 144.02n 0 150n 0 150.02n 1.8 156n 1.8 156.02n 0 162n 0 162.02n 1.8 168n 1.8
+ 168.02n 0 174n 0 174.02n 1.8 180n 1.8 180.02n 0 186n 0 186.02n 1.8 192n 1.8
+ 192.02n 0 198n 0 198.02n 1.8 204n 1.8 204.02n 0 210n 0 210.02n 1.8 216n 1.8
+ 216.02n 0 222n 0 222.02n 1.8 228n 1.8 228.02n 0 234n 0 234.02n 1.8 240n 1.8
+ 240.02n 0 246n 0 246.02n 1.8 252n 1.8 252.02n 0 258n 0 258.02n 1.8 264n 1.8
+ 264.02n 0 270n 0 270.02n 1.8 276n 1.8 276.02n 0 282n 0 282.02n 1.8 288n 1.8
+ 288.02n 0 294n 0 294.02n 1.8 300n 1.8 300.02n 0 306n 0 306.02n 1.8 312n 1.8
+ 312.02n 0 318n 0 318.02n 1.8 324n 1.8 324.02n 0 330n 0 330.02n 1.8 336n 1.8
+ 336.02n 0 342n 0 342.02n 1.8 348n 1.8 348.02n 0 354n 0 354.02n 1.8 360n 1.8
+ 360.02n 0 366n 0 366.02n 1.8 372n 1.8 372.02n 0 378n 0 378.02n 1.8
+)
Vx2 x2 0 pwl(
+ 0n 0 12n 0 12.02n 1.8 24n 1.8 24.02n 0 36n 0 36.02n 1.8 48n 1.8
+ 48.02n 0 60n 0 60.02n 1.8 72n 1.8 72.02n 0 84n 0 84.02n 1.8 96n 1.8
+ 96.02n 0 108n 0 108.02n 1.8 120n 1.8 120.02n 0 132n 0 132.02n 1.8 144n 1.8
+ 144.02n 0 156n 0 156.02n 1.8 168n 1.8 168.02n 0 180n 0 180.02n 1.8 192n 1.8
+ 192.02n 0 204n 0 204.02n 1.8 216n 1.8 216.02n 0 228n 0 228.02n 1.8 240n 1.8
+ 240.02n 0 252n 0 252.02n 1.8 264n 1.8 264.02n 0 276n 0 276.02n 1.8 288n 1.8
+ 288.02n 0 300n 0 300.02n 1.8 312n 1.8 312.02n 0 324n 0 324.02n 1.8 336n 1.8
+ 336.02n 0 348n 0 348.02n 1.8 360n 1.8 360.02n 0 372n 0 372.02n 1.8
+)
Vy0 y0 0 pwl(
+ 0n 0 24n 0 24.02n 1.8 48n 1.8 48.02n 0 72n 0 72.02n 1.8 96n 1.8
+ 96.02n 0 120n 0 120.02n 1.8 144n 1.8 144.02n 0 168n 0 168.02n 1.8 192n 1.8
+ 192.02n 0 216n 0 216.02n 1.8 240n 1.8 240.02n 0 264n 0 264.02n 1.8 288n 1.8
+ 288.02n 0 312n 0 312.02n 1.8 336n 1.8 336.02n 0 360n 0 360.02n 1.8
+)
Vy1 y1 0 pwl(
+ 0n 0 48n 0 48.02n 1.8 96n 1.8 96.02n 0 144n 0 144.02n 1.8 192n 1.8
+ 192.02n 0 240n 0 240.02n 1.8 288n 1.8 288.02n 0 336n 0 336.02n 1.8
+)
Vy2 y2 0 pwl(
+ 0n 0 96n 0 96.02n 1.8 192n 1.8 192.02n 0 288n 0 288.02n 1.8
+)
Vcin cin 0 pwl(
+ 0n 0 192n 0 192.02n 1.8
+)
.tran 2p 384n
.meas tran pavg avg par('-v(vdd)*i(VDD)') from=0 to=384n
.meas tran energy integ par('-v(vdd)*i(VDD)') from=0 to=384n
.meas tran v0_s0 find v(s0) at=2.9n
.meas tran v0_s1 find v(s1) at=2.9n
.meas tran v0_s2 find v(s2) at=2.9n
.meas tran v0_cout find v(cout) at=2.9n
.meas tran v1_s0 find v(s0) at=5.9n
.meas tran v1_s1 find v(s1) at=5.9n
.meas tran v1_s2 find v(s2) at=5.9n
.meas tran v1_cout find v(cout) at=5.9n
.meas tran v2_s0 find v(s0) at=8.9n
.meas tran v2_s1 find v(s1) at=8.9n
.meas tran v2_s2 find v(s2) at=8.9n
.meas tran v2_cout find v(cout) at=8.9n
.meas tran v3_s0 find v(s0) at=11.9n
.meas tran v3_s1 find v(s1) at=11.9n
.meas tran v3_s2 find v(s2) at=11.9n
.meas tran v3_cout find v(cout) at=11.9n
.meas tran v4_s0 find v(s0) at=14.9n
.meas tran v4_s1 find v(s1) at=14.9n
.meas tran v4_s2 find v(s2) at=14.9n
.meas tran v4_cout find v(cout) at=14.9n
.meas tran v5_s0 find v(s0) at=17.9n
.meas tran v5_s1 find v(s1) at=17.9n
.meas tran v5_s2 find v(s2) at=17.9n
.meas tran v5_cout find v(cout) at=17.9n
.meas tran v6_s0 find v(s0) at=20.9n
.meas tran v6_s1 find v(s1) at=20.9n
.meas tran v6_s2 find v(s2) at=20.9n
.meas tran v6_cout find v(cout) at=20.9n
.meas tran v7_s0 find v(s0) at=23.9n
.meas tran v7_s1 find v(s1) at=23.9n
.meas tran v7_s2 find v(s2) at=23.9n
.meas tran v7_cout find v(cout) at=23.9n
.meas tran v8_s0 find v(s0) at=26.9n
.meas tran v8_s1 find v(s1) at=26.9n
.meas tran v8_s2 find v(s2) at=26.9n
.meas tran v8_cout find v(cout) at=26.9n
.meas tran v9_s0 find v(s0) at=29.9n
.meas tran v9_s1 find v(s1) at=29.9n
.meas tran v9_s2 find v(s2) at=29.9n
.meas tran v9_cout find v(cout) at=29.9n
.meas tran v10_s0 find v(s0) at=32.9n
.meas tran v10_s1 find v(s1) at=32.9n
.meas tran v10_s2 find v(s2) at=32.9n
.meas tran v10_cout find v(cout) at=32.9n
.meas tran v11_s0 find v(s0) at=35.9n
.meas tran v11_s1 find v(s1) at=35.9n
.meas tran v11_s2 find v(s2) at=35.9n
.meas tran v11_cout find v(cout) at=35.9n
.meas tran v12_s0 find v(s0) at=38.9n
.meas tran v12_s1 find v(s1) at=38.9n
.meas tran v12_s2 find v(s2) at=38.9n
.meas tran v12_cout find v(cout) at=38.9n
.meas tran v13_s0 find v(s0) at=41.9n
.meas tran v13_s1 find v(s1) at=41.9n
.meas tran v13_s2 find v(s2) at=41.9n
.meas tran v13_cout find v(cout) at=41.9n
.meas tran v14_s0 find v(s0) at=44.9n
.meas tran v14_s1 find v(s1) at=44.9n
.meas tran v14_s2 find v(s2) at=44.9n
.meas tran v14_cout find v(cout) at=44.9n
.meas tran v15_s0 find v(s0) at=47.9n
.meas tran v15_s1 find v(s1) at=47.9n
.meas tran v15_s2 find v(s2) at=47.9n
.meas tran v15_cout find v(cout) at=47.9n
.meas tran v16_s0 find v(s0) at=50.9n
.meas tran v16_s1 find v(s1) at=50.9n
.meas tran v16_s2 find v(s2) at=50.9n
.meas tran v16_cout find v(cout) at=50.9n
.meas tran v17_s0 find v(s0) at=53.9n
.meas tran v17_s1 find v(s1) at=53.9n
.meas tran v17_s2 find v(s2) at=53.9n
.meas tran v17_cout find v(cout) at=53.9n
.meas tran v18_s0 find v(s0) at=56.9n
.meas tran v18_s1 find v(s1) at=56.9n
.meas tran v18_s2 find v(s2) at=56.9n
.meas tran v18_cout find v(cout) at=56.9n
.meas tran v19_s0 find v(s0) at=59.9n
.meas tran v19_s1 find v(s1) at=59.9n
.meas tran v19_s2 find v(s2) at=59.9n
.meas tran v19_cout find v(cout) at=59.9n
.meas tran v20_s0 find v(s0) at=62.9n
.meas tran v20_s1 find v(s1) at=62.9n
.meas tran v20_s2 find v(s2) at=62.9n
.meas tran v20_cout find v(cout) at=62.9n
.meas tran v21_s0 find v(s0) at=65.9n
.meas tran v21_s1 find v(s1) at=65.9n
.meas tran v21_s2 find v(s2) at=65.9n
.meas tran v21_cout find v(cout) at=65.9n
.meas tran v22_s0 find v(s0) at=68.9n
.meas tran v22_s1 find v(s1) at=68.9n
.meas tran v22_s2 find v(s2) at=68.9n
.meas tran v22_cout find v(cout) at=68.9n
.meas tran v23_s0 find v(s0) at=71.9n
.meas tran v23_s1 find v(s1) at=71.9n
.meas tran v23_s2 find v(s2) at=71.9n
.meas tran v23_cout find v(cout) at=71.9n
.meas tran v24_s0 find v(s0) at=74.9n
.meas tran v24_s1 find v(s1) at=74.9n
.meas tran v24_s2 find v(s2) at=74.9n
.meas tran v24_cout find v(cout) at=74.9n
.meas tran v25_s0 find v(s0) at=77.9n
.meas tran v25_s1 find v(s1) at=77.9n
.meas tran v25_s2 find v(s2) at=77.9n
.meas tran v25_cout find v(cout) at=77.9n
.meas tran v26_s0 find v(s0) at=80.9n
.meas tran v26_s1 find v(s1) at=80.9n
.meas tran v26_s2 find v(s2) at=80.9n
.meas tran v26_cout find v(cout) at=80.9n
.meas tran v27_s0 find v(s0) at=83.9n
.meas tran v27_s1 find v(s1) at=83.9n
.meas tran v27_s2 find v(s2) at=83.9n
.meas tran v27_cout find v(cout) at=83.9n
.meas tran v28_s0 find v(s0) at=86.9n
.meas tran v28_s1 find v(s1) at=86.9n
.meas tran v28_s2 find v(s2) at=86.9n
.meas tran v28_cout find v(cout) at=86.9n
.meas tran v29_s0 find v(s0) at=89.9n
.meas tran v29_s1 find v(s1) at=89.9n
.meas tran v29_s2 find v(s2) at=89.9n
.meas tran v29_cout find v(cout) at=89.9n
.meas tran v30_s0 find v(s0) at=92.9n
.meas tran v30_s1 find v(s1) at=92.9n
.meas tran v30_s2 find v(s2) at=92.9n
.meas tran v30_cout find v(cout) at=92.9n
.meas tran v31_s0 find v(s0) at=95.9n
.meas tran v31_s1 find v(s1) at=95.9n
.meas tran v31_s2 find v(s2) at=95.9n
.meas tran v31_cout find v(cout) at=95.9n
.meas tran v32_s0 find v(s0) at=98.9n
.meas tran v32_s1 find v(s1) at=98.9n
.meas tran v32_s2 find v(s2) at=98.9n
.meas tran v32_cout find v(cout) at=98.9n
.meas tran v33_s0 find v(s0) at=101.9n
.meas tran v33_s1 find v(s1) at=101.9n
.meas tran v33_s2 find v(s2) at=101.9n
.meas tran v33_cout find v(cout) at=101.9n
.meas tran v34_s0 find v(s0) at=104.9n
.meas tran v34_s1 find v(s1) at=104.9n
.meas tran v34_s2 find v(s2) at=104.9n
.meas tran v34_cout find v(cout) at=104.9n
.meas tran v35_s0 find v(s0) at=107.9n
.meas tran v35_s1 find v(s1) at=107.9n
.meas tran v35_s2 find v(s2) at=107.9n
.meas tran v35_cout find v(cout) at=107.9n
.meas tran v36_s0 find v(s0) at=110.9n
.meas tran v36_s1 find v(s1) at=110.9n
.meas tran v36_s2 find v(s2) at=110.9n
.meas tran v36_cout find v(cout) at=110.9n
.meas tran v37_s0 find v(s0) at=113.9n
.meas tran v37_s1 find v(s1) at=113.9n
.meas tran v37_s2 find v(s2) at=113.9n
.meas tran v37_cout find v(cout) at=113.9n
.meas tran v38_s0 find v(s0) at=116.9n
.meas tran v38_s1 find v(s1) at=116.9n
.meas tran v38_s2 find v(s2) at=116.9n
.meas tran v38_cout find v(cout) at=116.9n
.meas tran v39_s0 find v(s0) at=119.9n
.meas tran v39_s1 find v(s1) at=119.9n
.meas tran v39_s2 find v(s2) at=119.9n
.meas tran v39_cout find v(cout) at=119.9n
.meas tran v40_s0 find v(s0) at=122.9n
.meas tran v40_s1 find v(s1) at=122.9n
.meas tran v40_s2 find v(s2) at=122.9n
.meas tran v40_cout find v(cout) at=122.9n
.meas tran v41_s0 find v(s0) at=125.9n
.meas tran v41_s1 find v(s1) at=125.9n
.meas tran v41_s2 find v(s2) at=125.9n
.meas tran v41_cout find v(cout) at=125.9n
.meas tran v42_s0 find v(s0) at=128.9n
.meas tran v42_s1 find v(s1) at=128.9n
.meas tran v42_s2 find v(s2) at=128.9n
.meas tran v42_cout find v(cout) at=128.9n
.meas tran v43_s0 find v(s0) at=131.9n
.meas tran v43_s1 find v(s1) at=131.9n
.meas tran v43_s2 find v(s2) at=131.9n
.meas tran v43_cout find v(cout) at=131.9n
.meas tran v44_s0 find v(s0) at=134.9n
.meas tran v44_s1 find v(s1) at=134.9n
.meas tran v44_s2 find v(s2) at=134.9n
.meas tran v44_cout find v(cout) at=134.9n
.meas tran v45_s0 find v(s0) at=137.9n
.meas tran v45_s1 find v(s1) at=137.9n
.meas tran v45_s2 find v(s2) at=137.9n
.meas tran v45_cout find v(cout) at=137.9n
.meas tran v46_s0 find v(s0) at=140.9n
.meas tran v46_s1 find v(s1) at=140.9n
.meas tran v46_s2 find v(s2) at=140.9n
.meas tran v46_cout find v(cout) at=140.9n
.meas tran v47_s0 find v(s0) at=143.9n
.meas tran v47_s1 find v(s1) at=143.9n
.meas tran v47_s2 find v(s2) at=143.9n
.meas tran v47_cout find v(cout) at=143.9n
.meas tran v48_s0 find v(s0) at=146.9n
.meas tran v48_s1 find v(s1) at=146.9n
.meas tran v48_s2 find v(s2) at=146.9n
.meas tran v48_cout find v(cout) at=146.9n
.meas tran v49_s0 find v(s0) at=149.9n
.meas tran v49_s1 find v(s1) at=149.9n
.meas tran v49_s2 find v(s2) at=149.9n
.meas tran v49_cout find v(cout) at=149.9n
.meas tran v50_s0 find v(s0) at=152.9n
.meas tran v50_s1 find v(s1) at=152.9n
.meas tran v50_s2 find v(s2) at=152.9n
.meas tran v50_cout find v(cout) at=152.9n
.meas tran v51_s0 find v(s0) at=155.9n
.meas tran v51_s1 find v(s1) at=155.9n
.meas tran v51_s2 find v(s2) at=155.9n
.meas tran v51_cout find v(cout) at=155.9n
.meas tran v52_s0 find v(s0) at=158.9n
.meas tran v52_s1 find v(s1) at=158.9n
.meas tran v52_s2 find v(s2) at=158.9n
.meas tran v52_cout find v(cout) at=158.9n
.meas tran v53_s0 find v(s0) at=161.9n
.meas tran v53_s1 find v(s1) at=161.9n
.meas tran v53_s2 find v(s2) at=161.9n
.meas tran v53_cout find v(cout) at=161.9n
.meas tran v54_s0 find v(s0) at=164.9n
.meas tran v54_s1 find v(s1) at=164.9n
.meas tran v54_s2 find v(s2) at=164.9n
.meas tran v54_cout find v(cout) at=164.9n
.meas tran v55_s0 find v(s0) at=167.9n
.meas tran v55_s1 find v(s1) at=167.9n
.meas tran v55_s2 find v(s2) at=167.9n
.meas tran v55_cout find v(cout) at=167.9n
.meas tran v56_s0 find v(s0) at=170.9n
.meas tran v56_s1 find v(s1) at=170.9n
.meas tran v56_s2 find v(s2) at=170.9n
.meas tran v56_cout find v(cout) at=170.9n
.meas tran v57_s0 find v(s0) at=173.9n
.meas tran v57_s1 find v(s1) at=173.9n
.meas tran v57_s2 find v(s2) at=173.9n
.meas tran v57_cout find v(cout) at=173.9n
.meas tran v58_s0 find v(s0) at=176.9n
.meas tran v58_s1 find v(s1) at=176.9n
.meas tran v58_s2 find v(s2) at=176.9n
.meas tran v58_cout find v(cout) at=176.9n
.meas tran v59_s0 find v(s0) at=179.9n
.meas tran v59_s1 find v(s1) at=179.9n
.meas tran v59_s2 find v(s2) at=179.9n
.meas tran v59_cout find v(cout) at=179.9n
.meas tran v60_s0 find v(s0) at=182.9n
.meas tran v60_s1 find v(s1) at=182.9n
.meas tran v60_s2 find v(s2) at=182.9n
.meas tran v60_cout find v(cout) at=182.9n
.meas tran v61_s0 find v(s0) at=185.9n
.meas tran v61_s1 find v(s1) at=185.9n
.meas tran v61_s2 find v(s2) at=185.9n
.meas tran v61_cout find v(cout) at=185.9n
.meas tran v62_s0 find v(s0) at=188.9n
.meas tran v62_s1 find v(s1) at=188.9n
.meas tran v62_s2 find v(s2) at=188.9n
.meas tran v62_cout find v(cout) at=188.9n
.meas tran v63_s0 find v(s0) at=191.9n
.meas tran v63_s1 find v(s1) at=191.9n
.meas tran v63_s2 find v(s2) at=191.9n
.meas tran v63_cout find v(cout) at=191.9n
.meas tran v64_s0 find v(s0) at=194.9n
.meas tran v64_s1 find v(s1) at=194.9n
.meas tran v64_s2 find v(s2) at=194.9n
.meas tran v64_cout find v(cout) at=194.9n
.meas tran v65_s0 find v(s0) at=197.9n
.meas tran v65_s1 find v(s1) at=197.9n
.meas tran v65_s2 find v(s2) at=197.9n
.meas tran v65_cout find v(cout) at=197.9n
.meas tran v66_s0 find v(s0) at=200.9n
.meas tran v66_s1 find v(s1) at=200.9n
.meas tran v66_s2 find v(s2) at=200.9n
.meas tran v66_cout find v(cout) at=200.9n
.meas tran v67_s0 find v(s0) at=203.9n
.meas tran v67_s1 find v(s1) at=203.9n
.meas tran v67_s2 find v(s2) at=203.9n
.meas tran v67_cout find v(cout) at=203.9n
.meas tran v68_s0 find v(s0) at=206.9n
.meas tran v68_s1 find v(s1) at=206.9n
.meas tran v68_s2 find v(s2) at=206.9n
.meas tran v68_cout find v(cout) at=206.9n
.meas tran v69_s0 find v(s0) at=209.9n
.meas tran v69_s1 find v(s1) at=209.9n
.meas tran v69_s2 find v(s2) at=209.9n
.meas tran v69_cout find v(cout) at=209.9n
.meas tran v70_s0 find v(s0) at=212.9n
.meas tran v70_s1 find v(s1) at=212.9n
.meas tran v70_s2 find v(s2) at=212.9n
.meas tran v70_cout find v(cout) at=212.9n
.meas tran v71_s0 find v(s0) at=215.9n
.meas tran v71_s1 find v(s1) at=215.9n
.meas tran v71_s2 find v(s2) at=215.9n
.meas tran v71_cout find v(cout) at=215.9n
.meas tran v72_s0 find v(s0) at=218.9n
.meas tran v72_s1 find v(s1) at=218.9n
.meas tran v72_s2 find v(s2) at=218.9n
.meas tran v72_cout find v(cout) at=218.9n
.meas tran v73_s0 find v(s0) at=221.9n
.meas tran v73_s1 find v(s1) at=221.9n
.meas tran v73_s2 find v(s2) at=221.9n
.meas tran v73_cout find v(cout) at=221.9n
.meas tran v74_s0 find v(s0) at=224.9n
.meas tran v74_s1 find v(s1) at=224.9n
.meas tran v74_s2 find v(s2) at=224.9n
.meas tran v74_cout find v(cout) at=224.9n
.meas tran v75_s0 find v(s0) at=227.9n
.meas tran v75_s1 find v(s1) at=227.9n
.meas tran v75_s2 find v(s2) at=227.9n
.meas tran v75_cout find v(cout) at=227.9n
.meas tran v76_s0 find v(s0) at=230.9n
.meas tran v76_s1 find v(s1) at=230.9n
.meas tran v76_s2 find v(s2) at=230.9n
.meas tran v76_cout find v(cout) at=230.9n
.meas tran v77_s0 find v(s0) at=233.9n
.meas tran v77_s1 find v(s1) at=233.9n
.meas tran v77_s2 find v(s2) at=233.9n
.meas tran v77_cout find v(cout) at=233.9n
.meas tran v78_s0 find v(s0) at=236.9n
.meas tran v78_s1 find v(s1) at=236.9n
.meas tran v78_s2 find v(s2) at=236.9n
.meas tran v78_cout find v(cout) at=236.9n
.meas tran v79_s0 find v(s0) at=239.9n
.meas tran v79_s1 find v(s1) at=239.9n
.meas tran v79_s2 find v(s2) at=239.9n
.meas tran v79_cout find v(cout) at=239.9n
.meas tran v80_s0 find v(s0) at=242.9n
.meas tran v80_s1 find v(s1) at=242.9n
.meas tran v80_s2 find v(s2) at=242.9n
.meas tran v80_cout find v(cout) at=242.9n
.meas tran v81_s0 find v(s0) at=245.9n
.meas tran v81_s1 find v(s1) at=245.9n
.meas tran v81_s2 find v(s2) at=245.9n
.meas tran v81_cout find v(cout) at=245.9n
.meas tran v82_s0 find v(s0) at=248.9n
.meas tran v82_s1 find v(s1) at=248.9n
.meas tran v82_s2 find v(s2) at=248.9n
.meas tran v82_cout find v(cout) at=248.9n
.meas tran v83_s0 find v(s0) at=251.9n
.meas tran v83_s1 find v(s1) at=251.9n
.meas tran v83_s2 find v(s2) at=251.9n
.meas tran v83_cout find v(cout) at=251.9n
.meas tran v84_s0 find v(s0) at=254.9n
.meas tran v84_s1 find v(s1) at=254.9n
.meas tran v84_s2 find v(s2) at=254.9n
.meas tran v84_cout find v(cout) at=254.9n
.meas tran v85_s0 find v(s0) at=257.9n
.meas tran v85_s1 find v(s1) at=257.9n
.meas tran v85_s2 find v(s2) at=257.9n
.meas tran v85_cout find v(cout) at=257.9n
.meas tran v86_s0 find v(s0) at=260.9n
.meas tran v86_s1 find v(s1) at=260.9n
.meas tran v86_s2 find v(s2) at=260.9n
.meas tran v86_cout find v(cout) at=260.9n
.meas tran v87_s0 find v(s0) at=263.9n
.meas tran v87_s1 find v(s1) at=263.9n
.meas tran v87_s2 find v(s2) at=263.9n
.meas tran v87_cout find v(cout) at=263.9n
.meas tran v88_s0 find v(s0) at=266.9n
.meas tran v88_s1 find v(s1) at=266.9n
.meas tran v88_s2 find v(s2) at=266.9n
.meas tran v88_cout find v(cout) at=266.9n
.meas tran v89_s0 find v(s0) at=269.9n
.meas tran v89_s1 find v(s1) at=269.9n
.meas tran v89_s2 find v(s2) at=269.9n
.meas tran v89_cout find v(cout) at=269.9n
.meas tran v90_s0 find v(s0) at=272.9n
.meas tran v90_s1 find v(s1) at=272.9n
.meas tran v90_s2 find v(s2) at=272.9n
.meas tran v90_cout find v(cout) at=272.9n
.meas tran v91_s0 find v(s0) at=275.9n
.meas tran v91_s1 find v(s1) at=275.9n
.meas tran v91_s2 find v(s2) at=275.9n
.meas tran v91_cout find v(cout) at=275.9n
.meas tran v92_s0 find v(s0) at=278.9n
.meas tran v92_s1 find v(s1) at=278.9n
.meas tran v92_s2 find v(s2) at=278.9n
.meas tran v92_cout find v(cout) at=278.9n
.meas tran v93_s0 find v(s0) at=281.9n
.meas tran v93_s1 find v(s1) at=281.9n
.meas tran v93_s2 find v(s2) at=281.9n
.meas tran v93_cout find v(cout) at=281.9n
.meas tran v94_s0 find v(s0) at=284.9n
.meas tran v94_s1 find v(s1) at=284.9n
.meas tran v94_s2 find v(s2) at=284.9n
.meas tran v94_cout find v(cout) at=284.9n
.meas tran v95_s0 find v(s0) at=287.9n
.meas tran v95_s1 find v(s1) at=287.9n
.meas tran v95_s2 find v(s2) at=287.9n
.meas tran v95_cout find v(cout) at=287.9n
.meas tran v96_s0 find v(s0) at=290.9n
.meas tran v96_s1 find v(s1) at=290.9n
.meas tran v96_s2 find v(s2) at=290.9n
.meas tran v96_cout find v(cout) at=290.9n
.meas tran v97_s0 find v(s0) at=293.9n
.meas tran v97_s1 find v(s1) at=293.9n
.meas tran v97_s2 find v(s2) at=293.9n
.meas tran v97_cout find v(cout) at=293.9n
.meas tran v98_s0 find v(s0) at=296.9n
.meas tran v98_s1 find v(s1) at=296.9n
.meas tran v98_s2 find v(s2) at=296.9n
.meas tran v98_cout find v(cout) at=296.9n
.meas tran v99_s0 find v(s0) at=299.9n
.meas tran v99_s1 find v(s1) at=299.9n
.meas tran v99_s2 find v(s2) at=299.9n
.meas tran v99_cout find v(cout) at=299.9n
.meas tran v100_s0 find v(s0) at=302.9n
.meas tran v100_s1 find v(s1) at=302.9n
.meas tran v100_s2 find v(s2) at=302.9n
.meas tran v100_cout find v(cout) at=302.9n
.meas tran v101_s0 find v(s0) at=305.9n
.meas tran v101_s1 find v(s1) at=305.9n
.meas tran v101_s2 find v(s2) at=305.9n
.meas tran v101_cout find v(cout) at=305.9n
.meas tran v102_s0 find v(s0) at=308.9n
.meas tran v102_s1 find v(s1) at=308.9n
.meas tran v102_s2 find v(s2) at=308.9n
.meas tran v102_cout find v(cout) at=308.9n
.meas tran v103_s0 find v(s0) at=311.9n
.meas tran v103_s1 find v(s1) at=311.9n
.meas tran v103_s2 find v(s2) at=311.9n
.meas tran v103_cout find v(cout) at=311.9n
.meas tran v104_s0 find v(s0) at=314.9n
.meas tran v104_s1 find v(s1) at=314.9n
.meas tran v104_s2 find v(s2) at=314.9n
.meas tran v104_cout find v(cout) at=314.9n
.meas tran v105_s0 find v(s0) at=317.9n
.meas tran v105_s1 find v(s1) at=317.9n
.meas tran v105_s2 find v(s2) at=317.9n
.meas tran v105_cout find v(cout) at=317.9n
.meas tran v106_s0 find v(s0) at=320.9n
.meas tran v106_s1 find v(s1) at=320.9n
.meas tran v106_s2 find v(s2) at=320.9n
.meas tran v106_cout find v(cout) at=320.9n
.meas tran v107_s0 find v(s0) at=323.9n
.meas tran v107_s1 find v(s1) at=323.9n
.meas tran v107_s2 find v(s2) at=323.9n
.meas tran v107_cout find v(cout) at=323.9n
.meas tran v108_s0 find v(s0) at=326.9n
.meas tran v108_s1 find v(s1) at=326.9n
.meas tran v108_s2 find v(s2) at=326.9n
.meas tran v108_cout find v(cout) at=326.9n
.meas tran v109_s0 find v(s0) at=329.9n
.meas tran v109_s1 find v(s1) at=329.9n
.meas tran v109_s2 find v(s2) at=329.9n
.meas tran v109_cout find v(cout) at=329.9n
.meas tran v110_s0 find v(s0) at=332.9n
.meas tran v110_s1 find v(s1) at=332.9n
.meas tran v110_s2 find v(s2) at=332.9n
.meas tran v110_cout find v(cout) at=332.9n
.meas tran v111_s0 find v(s0) at=335.9n
.meas tran v111_s1 find v(s1) at=335.9n
.meas tran v111_s2 find v(s2) at=335.9n
.meas tran v111_cout find v(cout) at=335.9n
.meas tran v112_s0 find v(s0) at=338.9n
.meas tran v112_s1 find v(s1) at=338.9n
.meas tran v112_s2 find v(s2) at=338.9n
.meas tran v112_cout find v(cout) at=338.9n
.meas tran v113_s0 find v(s0) at=341.9n
.meas tran v113_s1 find v(s1) at=341.9n
.meas tran v113_s2 find v(s2) at=341.9n
.meas tran v113_cout find v(cout) at=341.9n
.meas tran v114_s0 find v(s0) at=344.9n
.meas tran v114_s1 find v(s1) at=344.9n
.meas tran v114_s2 find v(s2) at=344.9n
.meas tran v114_cout find v(cout) at=344.9n
.meas tran v115_s0 find v(s0) at=347.9n
.meas tran v115_s1 find v(s1) at=347.9n
.meas tran v115_s2 find v(s2) at=347.9n
.meas tran v115_cout find v(cout) at=347.9n
.meas tran v116_s0 find v(s0) at=350.9n
.meas tran v116_s1 find v(s1) at=350.9n
.meas tran v116_s2 find v(s2) at=350.9n
.meas tran v116_cout find v(cout) at=350.9n
.meas tran v117_s0 find v(s0) at=353.9n
.meas tran v117_s1 find v(s1) at=353.9n
.meas tran v117_s2 find v(s2) at=353.9n
.meas tran v117_cout find v(cout) at=353.9n
.meas tran v118_s0 find v(s0) at=356.9n
.meas tran v118_s1 find v(s1) at=356.9n
.meas tran v118_s2 find v(s2) at=356.9n
.meas tran v118_cout find v(cout) at=356.9n
.meas tran v119_s0 find v(s0) at=359.9n
.meas tran v119_s1 find v(s1) at=359.9n
.meas tran v119_s2 find v(s2) at=359.9n
.meas tran v119_cout find v(cout) at=359.9n
.meas tran v120_s0 find v(s0) at=362.9n
.meas tran v120_s1 find v(s1) at=362.9n
.meas tran v120_s2 find v(s2) at=362.9n
.meas tran v120_cout find v(cout) at=362.9n
.meas tran v121_s0 find v(s0) at=365.9n
.meas tran v121_s1 find v(s1) at=365.9n
.meas tran v121_s2 find v(s2) at=365.9n
.meas tran v121_cout find v(cout) at=365.9n
.meas tran v122_s0 find v(s0) at=368.9n
.meas tran v122_s1 find v(s1) at=368.9n
.meas tran v122_s2 find v(s2) at=368.9n
.meas tran v122_cout find v(cout) at=368.9n
.meas tran v123_s0 find v(s0) at=371.9n
.meas tran v123_s1 find v(s1) at=371.9n
.meas tran v123_s2 find v(s2) at=371.9n
.meas tran v123_cout find v(cout) at=371.9n
.meas tran v124_s0 find v(s0) at=374.9n
.meas tran v124_s1 find v(s1) at=374.9n
.meas tran v124_s2 find v(s2) at=374.9n
.meas tran v124_cout find v(cout) at=374.9n
.meas tran v125_s0 find v(s0) at=377.9n
.meas tran v125_s1 find v(s1) at=377.9n
.meas tran v125_s2 find v(s2) at=377.9n
.meas tran v125_cout find v(cout) at=377.9n
.meas tran v126_s0 find v(s0) at=380.9n
.meas tran v126_s1 find v(s1) at=380.9n
.meas tran v126_s2 find v(s2) at=380.9n
.meas tran v126_cout find v(cout) at=380.9n
.meas tran v127_s0 find v(s0) at=383.9n
.meas tran v127_s1 find v(s1) at=383.9n
.meas tran v127_s2 find v(s2) at=383.9n
.meas tran v127_cout find v(cout) at=383.9n
.end
