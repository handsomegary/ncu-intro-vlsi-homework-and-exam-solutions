# Source comparison and decisions

Primary question source: `112學年度第一學期超大型積體電路導論期中考 Li.pdf`, supplied 2023 archive, PDF page 1 / printed 2-2 with Fall 2023 footer. Its photograph contains complete Q5/Q6/Q7 and a Q4 tail whose premise starts on absent page 2-1. Missing questions are not reconstructed from answers.

Student set A: PDF pages 2–5; relevant Q5/Q6 on page 4, Q7 on page 5. Student set B: PDF pages 6–10; relevant Q5 on page 8 and Q7 on page 10. No complete readable Q6 answer is present in set B; a cropped neighboring-page edge is insufficient. Personal names/IDs are not reproduced. Grading marks are provenance rather than proof.

Q5: both sets give conventional NAND `NML>NMH` and NOR `NML<NMH`; retained conditionally under matched thresholds. The final solution adds source-specific gate outputs and masking at G2/1101 and G3/1110. The source specifies no numeric thresholds or margins.

Q6: set A's doubled NAND devices and n1/p2 inverter give 3Cg internal load and 7RCg total; independent RC accounting and truth checks support them. The source defines Cg per single W/L device.

Q7: both sets' b network has the correct series Y/Z pMOS dual. Their a/c approach uses complemented primary inputs and can be valid, but requires complement generators not present in the visible drawings. The final solution factors the original positive functions and uses original-input cores plus output inverters, yielding 10/6/8 transistors for a/b/c, with explicit body-tie conventions.

Question 4: students' .8V answer is not imported because the opening with required R/VT values is missing. Figure 2 also has no intact question stem, so it is not presented as an answerable question. All source functions, Q5 patterns 0011/0101/1101/1110 and 35 complete printed points were read from the original photo.
