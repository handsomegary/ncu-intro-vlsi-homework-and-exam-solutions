# Fall 2023 source review

Review date: 2026-10-13. The original PDFs define the questions; existing
submissions are references, not authoritative answers. All three HW1/HW2/HW3
submissions and four supplied HW4 reports/pre-layout files were read before
independent reconstruction. Source hashes are in `reference_sources.json`.

| Homework | Existing material | Integration decision |
|---|---|---|
| HW1 | Lin 110501558, Liao 110501512, Jian 109501570 | Correct printed AOI polarity; compact 10T minority network; complementary 40T rotator; 12T XOR. Full source-by-source review is in HW1/REFERENCE_COMPARISON.md. |
| HW2 | Same three submissions | Keep valid voltage-drop, charge conservation and NOR logic; restore missing C factor in Lin; explain BL disconnection; mark dual-Vt timing condition; separate literal “smallest” and conventional “highest” low specifications. |
| HW3 | Lin 28T mirror-style FA, Liao 36T XOR/NAND FA, Jian decomposed AND/OR FA | Reconstruct 28T compact architecture, fix HW3 internal body ties and output loading; do not reuse average of two selected delays as an exhaustive worst case. Test all128 states and896 directed single-input transitions. |
| HW4 | Lin 110501558, Liao110501512, Jian109501570 and Lin111501559 reports and pre-layout code | Retain correct rail-body principle and reuse independently verified HW3 circuit. Other students' layouts/PEX and post-layout measurements are not results of this circuit. |

The 28T architecture has fewer devices than the 36T gate decomposition,
but no optimal area, speed or power claim is made across differently sized
designs. The published results are new simulations of the explicit netlist.
Raw model contents and prior students' reports/layouts are not redistributed.

Public searches for the 2020/2021/2023 course returned mainly duplicates of
assignment text, not a more useful directly matching complete solution set.
This is a bounded search, not a claim that no other solutions exist.
The supplied complete answer collections were the principal comparison source.
