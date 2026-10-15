* 2021 HW2 functional simulation
.protect
.lib 'D:/cic018.l' tt
.unprotect
vvdd vdd 0 1.8
vvss vss 0 0
.temp 25
.option measform=3 measdgt=9
.include 'rotator.sp'
va0 a0 0 pwl(
+ 0n 0 9.9n 0 10n 1.8 19.9n 1.8 20n 0
+ 29.9n 0 30n 1.8 39.9n 1.8 40n 0 49.9n 0
+ 50n 1.8 59.9n 1.8 60n 0 69.9n 0 70n 1.8
+ 79.9n 1.8 80n 0 89.9n 0 90n 1.8 99.9n 1.8
+ 100n 0 109.9n 0 110n 1.8 119.9n 1.8 120n 0
+ 129.9n 0 130n 1.8 139.9n 1.8 140n 0 149.9n 0
+ 150n 1.8 159.9n 1.8 160n 0 169.9n 0 170n 1.8
+ 179.9n 1.8 180n 0 189.9n 0 190n 1.8 199.9n 1.8
+ 200n 0 209.9n 0 210n 1.8 219.9n 1.8 220n 0
+ 229.9n 0 230n 1.8 239.9n 1.8 240n 0 249.9n 0
+ 250n 1.8 259.9n 1.8 260n 0 269.9n 0 270n 1.8
+ 279.9n 1.8 280n 0 289.9n 0 290n 1.8 299.9n 1.8
+ 300n 0 309.9n 0 310n 1.8 319.9n 1.8 320n 0
+ 329.9n 0 330n 1.8 339.9n 1.8 340n 0 349.9n 0
+ 350n 1.8 359.9n 1.8 360n 0 369.9n 0 370n 1.8
+ 379.9n 1.8 380n 0 389.9n 0 390n 1.8 399.9n 1.8
+ 400n 0 409.9n 0 410n 1.8 419.9n 1.8 420n 0
+ 429.9n 0 430n 1.8 439.9n 1.8 440n 0 449.9n 0
+ 450n 1.8 459.9n 1.8 460n 0 469.9n 0 470n 1.8
+ 479.9n 1.8 480n 0 489.9n 0 490n 1.8 499.9n 1.8
+ 500n 0 509.9n 0 510n 1.8 519.9n 1.8 520n 0
+ 529.9n 0 530n 1.8 539.9n 1.8 540n 0 549.9n 0
+ 550n 1.8 559.9n 1.8 560n 0 569.9n 0 570n 1.8
+ 579.9n 1.8 580n 0 589.9n 0 590n 1.8 599.9n 1.8
+ 600n 0 609.9n 0 610n 1.8 619.9n 1.8 620n 0
+ 629.9n 0 630n 1.8
+)
va1 a1 0 pwl(
+ 0n 0 19.9n 0 20n 1.8 39.9n 1.8 40n 0
+ 59.9n 0 60n 1.8 79.9n 1.8 80n 0 99.9n 0
+ 100n 1.8 119.9n 1.8 120n 0 139.9n 0 140n 1.8
+ 159.9n 1.8 160n 0 179.9n 0 180n 1.8 199.9n 1.8
+ 200n 0 219.9n 0 220n 1.8 239.9n 1.8 240n 0
+ 259.9n 0 260n 1.8 279.9n 1.8 280n 0 299.9n 0
+ 300n 1.8 319.9n 1.8 320n 0 339.9n 0 340n 1.8
+ 359.9n 1.8 360n 0 379.9n 0 380n 1.8 399.9n 1.8
+ 400n 0 419.9n 0 420n 1.8 439.9n 1.8 440n 0
+ 459.9n 0 460n 1.8 479.9n 1.8 480n 0 499.9n 0
+ 500n 1.8 519.9n 1.8 520n 0 539.9n 0 540n 1.8
+ 559.9n 1.8 560n 0 579.9n 0 580n 1.8 599.9n 1.8
+ 600n 0 619.9n 0 620n 1.8
+)
va2 a2 0 pwl(
+ 0n 0 39.9n 0 40n 1.8 79.9n 1.8 80n 0
+ 119.9n 0 120n 1.8 159.9n 1.8 160n 0 199.9n 0
+ 200n 1.8 239.9n 1.8 240n 0 279.9n 0 280n 1.8
+ 319.9n 1.8 320n 0 359.9n 0 360n 1.8 399.9n 1.8
+ 400n 0 439.9n 0 440n 1.8 479.9n 1.8 480n 0
+ 519.9n 0 520n 1.8 559.9n 1.8 560n 0 599.9n 0
+ 600n 1.8
+)
va3 a3 0 pwl(
+ 0n 0 79.9n 0 80n 1.8 159.9n 1.8 160n 0
+ 239.9n 0 240n 1.8 319.9n 1.8 320n 0 399.9n 0
+ 400n 1.8 479.9n 1.8 480n 0 559.9n 0 560n 1.8
+)
vc0 c0 0 pwl(
+ 0n 1.8 479.9n 1.8 480n 0
+)
vc1 c1 0 pwl(
+ 0n 1.8 319.9n 1.8 320n 0 479.9n 0 480n 1.8
+)
vc2 c2 0 pwl(
+ 0n 1.8 159.9n 1.8 160n 0 319.9n 0 320n 1.8
+)
vc3 c3 0 pwl(
+ 0n 0 159.9n 0 160n 1.8
+)
XR a0 a1 a2 a3 c0 c1 c2 c3 z0 z1 z2 z3 vdd vss rotate4
CL0 z0 0 1f
CL1 z1 0 1f
CL2 z2 0 1f
CL3 z3 0 1f
.tran 10p 640n 0 50p
.measure tran q0b0 find v(z0) at=8n
.measure tran q0b1 find v(z1) at=8n
.measure tran q0b2 find v(z2) at=8n
.measure tran q0b3 find v(z3) at=8n
.measure tran q1b0 find v(z0) at=18n
.measure tran q1b1 find v(z1) at=18n
.measure tran q1b2 find v(z2) at=18n
.measure tran q1b3 find v(z3) at=18n
.measure tran q2b0 find v(z0) at=28n
.measure tran q2b1 find v(z1) at=28n
.measure tran q2b2 find v(z2) at=28n
.measure tran q2b3 find v(z3) at=28n
.measure tran q3b0 find v(z0) at=38n
.measure tran q3b1 find v(z1) at=38n
.measure tran q3b2 find v(z2) at=38n
.measure tran q3b3 find v(z3) at=38n
.measure tran q4b0 find v(z0) at=48n
.measure tran q4b1 find v(z1) at=48n
.measure tran q4b2 find v(z2) at=48n
.measure tran q4b3 find v(z3) at=48n
.measure tran q5b0 find v(z0) at=58n
.measure tran q5b1 find v(z1) at=58n
.measure tran q5b2 find v(z2) at=58n
.measure tran q5b3 find v(z3) at=58n
.measure tran q6b0 find v(z0) at=68n
.measure tran q6b1 find v(z1) at=68n
.measure tran q6b2 find v(z2) at=68n
.measure tran q6b3 find v(z3) at=68n
.measure tran q7b0 find v(z0) at=78n
.measure tran q7b1 find v(z1) at=78n
.measure tran q7b2 find v(z2) at=78n
.measure tran q7b3 find v(z3) at=78n
.measure tran q8b0 find v(z0) at=88n
.measure tran q8b1 find v(z1) at=88n
.measure tran q8b2 find v(z2) at=88n
.measure tran q8b3 find v(z3) at=88n
.measure tran q9b0 find v(z0) at=98n
.measure tran q9b1 find v(z1) at=98n
.measure tran q9b2 find v(z2) at=98n
.measure tran q9b3 find v(z3) at=98n
.measure tran q10b0 find v(z0) at=108n
.measure tran q10b1 find v(z1) at=108n
.measure tran q10b2 find v(z2) at=108n
.measure tran q10b3 find v(z3) at=108n
.measure tran q11b0 find v(z0) at=118n
.measure tran q11b1 find v(z1) at=118n
.measure tran q11b2 find v(z2) at=118n
.measure tran q11b3 find v(z3) at=118n
.measure tran q12b0 find v(z0) at=128n
.measure tran q12b1 find v(z1) at=128n
.measure tran q12b2 find v(z2) at=128n
.measure tran q12b3 find v(z3) at=128n
.measure tran q13b0 find v(z0) at=138n
.measure tran q13b1 find v(z1) at=138n
.measure tran q13b2 find v(z2) at=138n
.measure tran q13b3 find v(z3) at=138n
.measure tran q14b0 find v(z0) at=148n
.measure tran q14b1 find v(z1) at=148n
.measure tran q14b2 find v(z2) at=148n
.measure tran q14b3 find v(z3) at=148n
.measure tran q15b0 find v(z0) at=158n
.measure tran q15b1 find v(z1) at=158n
.measure tran q15b2 find v(z2) at=158n
.measure tran q15b3 find v(z3) at=158n
.measure tran q16b0 find v(z0) at=168n
.measure tran q16b1 find v(z1) at=168n
.measure tran q16b2 find v(z2) at=168n
.measure tran q16b3 find v(z3) at=168n
.measure tran q17b0 find v(z0) at=178n
.measure tran q17b1 find v(z1) at=178n
.measure tran q17b2 find v(z2) at=178n
.measure tran q17b3 find v(z3) at=178n
.measure tran q18b0 find v(z0) at=188n
.measure tran q18b1 find v(z1) at=188n
.measure tran q18b2 find v(z2) at=188n
.measure tran q18b3 find v(z3) at=188n
.measure tran q19b0 find v(z0) at=198n
.measure tran q19b1 find v(z1) at=198n
.measure tran q19b2 find v(z2) at=198n
.measure tran q19b3 find v(z3) at=198n
.measure tran q20b0 find v(z0) at=208n
.measure tran q20b1 find v(z1) at=208n
.measure tran q20b2 find v(z2) at=208n
.measure tran q20b3 find v(z3) at=208n
.measure tran q21b0 find v(z0) at=218n
.measure tran q21b1 find v(z1) at=218n
.measure tran q21b2 find v(z2) at=218n
.measure tran q21b3 find v(z3) at=218n
.measure tran q22b0 find v(z0) at=228n
.measure tran q22b1 find v(z1) at=228n
.measure tran q22b2 find v(z2) at=228n
.measure tran q22b3 find v(z3) at=228n
.measure tran q23b0 find v(z0) at=238n
.measure tran q23b1 find v(z1) at=238n
.measure tran q23b2 find v(z2) at=238n
.measure tran q23b3 find v(z3) at=238n
.measure tran q24b0 find v(z0) at=248n
.measure tran q24b1 find v(z1) at=248n
.measure tran q24b2 find v(z2) at=248n
.measure tran q24b3 find v(z3) at=248n
.measure tran q25b0 find v(z0) at=258n
.measure tran q25b1 find v(z1) at=258n
.measure tran q25b2 find v(z2) at=258n
.measure tran q25b3 find v(z3) at=258n
.measure tran q26b0 find v(z0) at=268n
.measure tran q26b1 find v(z1) at=268n
.measure tran q26b2 find v(z2) at=268n
.measure tran q26b3 find v(z3) at=268n
.measure tran q27b0 find v(z0) at=278n
.measure tran q27b1 find v(z1) at=278n
.measure tran q27b2 find v(z2) at=278n
.measure tran q27b3 find v(z3) at=278n
.measure tran q28b0 find v(z0) at=288n
.measure tran q28b1 find v(z1) at=288n
.measure tran q28b2 find v(z2) at=288n
.measure tran q28b3 find v(z3) at=288n
.measure tran q29b0 find v(z0) at=298n
.measure tran q29b1 find v(z1) at=298n
.measure tran q29b2 find v(z2) at=298n
.measure tran q29b3 find v(z3) at=298n
.measure tran q30b0 find v(z0) at=308n
.measure tran q30b1 find v(z1) at=308n
.measure tran q30b2 find v(z2) at=308n
.measure tran q30b3 find v(z3) at=308n
.measure tran q31b0 find v(z0) at=318n
.measure tran q31b1 find v(z1) at=318n
.measure tran q31b2 find v(z2) at=318n
.measure tran q31b3 find v(z3) at=318n
.measure tran q32b0 find v(z0) at=328n
.measure tran q32b1 find v(z1) at=328n
.measure tran q32b2 find v(z2) at=328n
.measure tran q32b3 find v(z3) at=328n
.measure tran q33b0 find v(z0) at=338n
.measure tran q33b1 find v(z1) at=338n
.measure tran q33b2 find v(z2) at=338n
.measure tran q33b3 find v(z3) at=338n
.measure tran q34b0 find v(z0) at=348n
.measure tran q34b1 find v(z1) at=348n
.measure tran q34b2 find v(z2) at=348n
.measure tran q34b3 find v(z3) at=348n
.measure tran q35b0 find v(z0) at=358n
.measure tran q35b1 find v(z1) at=358n
.measure tran q35b2 find v(z2) at=358n
.measure tran q35b3 find v(z3) at=358n
.measure tran q36b0 find v(z0) at=368n
.measure tran q36b1 find v(z1) at=368n
.measure tran q36b2 find v(z2) at=368n
.measure tran q36b3 find v(z3) at=368n
.measure tran q37b0 find v(z0) at=378n
.measure tran q37b1 find v(z1) at=378n
.measure tran q37b2 find v(z2) at=378n
.measure tran q37b3 find v(z3) at=378n
.measure tran q38b0 find v(z0) at=388n
.measure tran q38b1 find v(z1) at=388n
.measure tran q38b2 find v(z2) at=388n
.measure tran q38b3 find v(z3) at=388n
.measure tran q39b0 find v(z0) at=398n
.measure tran q39b1 find v(z1) at=398n
.measure tran q39b2 find v(z2) at=398n
.measure tran q39b3 find v(z3) at=398n
.measure tran q40b0 find v(z0) at=408n
.measure tran q40b1 find v(z1) at=408n
.measure tran q40b2 find v(z2) at=408n
.measure tran q40b3 find v(z3) at=408n
.measure tran q41b0 find v(z0) at=418n
.measure tran q41b1 find v(z1) at=418n
.measure tran q41b2 find v(z2) at=418n
.measure tran q41b3 find v(z3) at=418n
.measure tran q42b0 find v(z0) at=428n
.measure tran q42b1 find v(z1) at=428n
.measure tran q42b2 find v(z2) at=428n
.measure tran q42b3 find v(z3) at=428n
.measure tran q43b0 find v(z0) at=438n
.measure tran q43b1 find v(z1) at=438n
.measure tran q43b2 find v(z2) at=438n
.measure tran q43b3 find v(z3) at=438n
.measure tran q44b0 find v(z0) at=448n
.measure tran q44b1 find v(z1) at=448n
.measure tran q44b2 find v(z2) at=448n
.measure tran q44b3 find v(z3) at=448n
.measure tran q45b0 find v(z0) at=458n
.measure tran q45b1 find v(z1) at=458n
.measure tran q45b2 find v(z2) at=458n
.measure tran q45b3 find v(z3) at=458n
.measure tran q46b0 find v(z0) at=468n
.measure tran q46b1 find v(z1) at=468n
.measure tran q46b2 find v(z2) at=468n
.measure tran q46b3 find v(z3) at=468n
.measure tran q47b0 find v(z0) at=478n
.measure tran q47b1 find v(z1) at=478n
.measure tran q47b2 find v(z2) at=478n
.measure tran q47b3 find v(z3) at=478n
.measure tran q48b0 find v(z0) at=488n
.measure tran q48b1 find v(z1) at=488n
.measure tran q48b2 find v(z2) at=488n
.measure tran q48b3 find v(z3) at=488n
.measure tran q49b0 find v(z0) at=498n
.measure tran q49b1 find v(z1) at=498n
.measure tran q49b2 find v(z2) at=498n
.measure tran q49b3 find v(z3) at=498n
.measure tran q50b0 find v(z0) at=508n
.measure tran q50b1 find v(z1) at=508n
.measure tran q50b2 find v(z2) at=508n
.measure tran q50b3 find v(z3) at=508n
.measure tran q51b0 find v(z0) at=518n
.measure tran q51b1 find v(z1) at=518n
.measure tran q51b2 find v(z2) at=518n
.measure tran q51b3 find v(z3) at=518n
.measure tran q52b0 find v(z0) at=528n
.measure tran q52b1 find v(z1) at=528n
.measure tran q52b2 find v(z2) at=528n
.measure tran q52b3 find v(z3) at=528n
.measure tran q53b0 find v(z0) at=538n
.measure tran q53b1 find v(z1) at=538n
.measure tran q53b2 find v(z2) at=538n
.measure tran q53b3 find v(z3) at=538n
.measure tran q54b0 find v(z0) at=548n
.measure tran q54b1 find v(z1) at=548n
.measure tran q54b2 find v(z2) at=548n
.measure tran q54b3 find v(z3) at=548n
.measure tran q55b0 find v(z0) at=558n
.measure tran q55b1 find v(z1) at=558n
.measure tran q55b2 find v(z2) at=558n
.measure tran q55b3 find v(z3) at=558n
.measure tran q56b0 find v(z0) at=568n
.measure tran q56b1 find v(z1) at=568n
.measure tran q56b2 find v(z2) at=568n
.measure tran q56b3 find v(z3) at=568n
.measure tran q57b0 find v(z0) at=578n
.measure tran q57b1 find v(z1) at=578n
.measure tran q57b2 find v(z2) at=578n
.measure tran q57b3 find v(z3) at=578n
.measure tran q58b0 find v(z0) at=588n
.measure tran q58b1 find v(z1) at=588n
.measure tran q58b2 find v(z2) at=588n
.measure tran q58b3 find v(z3) at=588n
.measure tran q59b0 find v(z0) at=598n
.measure tran q59b1 find v(z1) at=598n
.measure tran q59b2 find v(z2) at=598n
.measure tran q59b3 find v(z3) at=598n
.measure tran q60b0 find v(z0) at=608n
.measure tran q60b1 find v(z1) at=608n
.measure tran q60b2 find v(z2) at=608n
.measure tran q60b3 find v(z3) at=608n
.measure tran q61b0 find v(z0) at=618n
.measure tran q61b1 find v(z1) at=618n
.measure tran q61b2 find v(z2) at=618n
.measure tran q61b3 find v(z3) at=618n
.measure tran q62b0 find v(z0) at=628n
.measure tran q62b1 find v(z1) at=628n
.measure tran q62b2 find v(z2) at=628n
.measure tran q62b3 find v(z3) at=628n
.measure tran q63b0 find v(z0) at=638n
.measure tran q63b1 find v(z1) at=638n
.measure tran q63b2 find v(z2) at=638n
.measure tran q63b3 find v(z3) at=638n
.end
