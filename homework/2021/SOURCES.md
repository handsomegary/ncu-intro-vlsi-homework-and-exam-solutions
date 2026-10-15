# 2021 sources and integration decisions

## Original course prompts

Author: Li, EE3032, National Central University, Fall 2021. The public question PDFs retain their original page layout, with surname Li in the footer.

- HW1: source `homework1.pdf` -> `assignments/homework1.pdf`; SHA-256 `3de7e17b66b89624c86d8285d124e8185f0045d9f4b06bd51863d119c620f11d`.
- HW2: source `homework2.pdf` -> `assignments/homework2.pdf`; SHA-256 `fc0bf6510726bd472dd5979de6781c646bcee3b26120a4fcc64bb19b18110034`.
- HW3: source `homework3 .pdf` -> `assignments/homework3.pdf`; SHA-256 `c8b17f2d1ad3de1ed0e322393e5b3a7d6fd0bf9871b35d7b22734f82e66d4efd`.
- HW4: source `homework4.pdf` -> `assignments/homework4.pdf`; SHA-256 `cb8b2f35e268cae534c830cd62567327c2b20e43ca3dbfabf10e3a70cc53f797`.

## User-supplied completed answers

Attributed author: Lin Yan-Yu (as printed in the supplied PDFs). They are used as comparison references; their PDFs and identifying student number are not redistributed. These local references were read before deriving and authoring the present solutions.

- HW1: `VLSI HW1-1 (1).pdf`; SHA-256 `05ff35d09f8a38e28ee18b72577c7dec91d36b780ded20ba4c4413959d470dc7`.
- HW1: `VLSI HW1-2 (1).pdf`; SHA-256 `724ec2bd9fcac97c4f3d591366fe2d7f6ab018b9ac4b96c9290720c4b68bf275`.
- HW1: `VLSI HW1-3 (1).pdf`; SHA-256 `cdc14523f3329b94ee87aa44477b7fde17055349f6c70459754cc4b175100ea2`.
- HW2: `VLSI HW2.pdf`; SHA-256 `2a43d7c5e80bd224b0af954359343eaab6fde636703ff7628e6bcfe41a88bfcb`.
- HW3: `VLSI hw3.pdf`; SHA-256 `f29300e70a459601f0f62675ba642841f9d790aa49e8db2531d2743c54beed87`.
- HW4: `VLSI hw4.pdf`; SHA-256 `3e483f17d66fc1d5546b83f5fd67814a86c4070b6f9c173d93c3fc4dfdc66a70`.

## Integrated solution decisions

### HW1

Retain correct rail-side non-saturation and half-aspect-ratio result; extend the derivation to linear-region equivalence. Reduce the full seven-mux Shannon tree to four muxes. Preserve the overbar in Q3(a) and its correct ten-transistor AOI network. Factor Q3(b) from the supplied twelve-transistor product network to ten transistors.

### HW2

Retain high-Vt NAND selection, but explicitly require its delay to remain at most two gate units. Use a direct one-hot 40-transistor rotator in place of the supplied four-pass-stage decoding network. Retain pseudo-NMOS NOR and n:p aspect-ratio 9:2 choice, state the general >=4.5 ratio, and verify it with the stated resistance model and the local BSIM model.

### HW3

Retain the reference widths (PMOS 3 um, NAND NMOS 2 um, inverter NMOS 1 um), L=0.18 um, 1 ns slew, and 1 fF load. Replace manual cursor measurements with reproducible .measure statements, explicit node-0 supply references, three measured cycles, rail checks, and exported waveforms. F=NAND and Z=AND are correct in both prompt and reference.

### HW4

The supplied report uses W/L=2/1 um and includes layout. This solution retains the smaller verified HW3 sizing permitted by the prompt, repeats pre-layout SPICE only, and excludes the supplied layout/post-layout material as requested.

## Independent verification and limitations

- HW1: exhaustive switch-level Boolean evaluation and ideal long-channel equal-current equations; neither is claimed to be a BSIM simulation.
- HW2: exhaustive logic checks, actual CIC018 TT rotator and pseudo-NOR simulation, plus an explicitly illustrative Level-1 dual-Vt topology test. The provided model has no characterized dual-Vt variants, so no physical leakage saving or unqualified timing guarantee is reported.
- HW3/HW4: actual PrimeSim HSPICE S-2021.09 win64 runs with the local process model at TT, 25 C, 1.8 V, 1 fF, 1 ns input edges, and 2 ps requested output timestep. The four directional worst delays are reported from 36 measurements per homework.
- Reports were compiled and rendered for visual inspection. Standalone LaTeX embeds every diagram and waveform.
- Public search in this task did not identify a trustworthy complete original 2021 solution; no unverified web answer was used.
- `D:/cic018.l` is used locally as authorized, and is not copied, quoted, or redistributed.
