# NCU Introduction to VLSI Design

National Central University, EE3032. Editable LaTeX papers and solutions, transistor diagrams, SPICE programs and numerical verification are organized in two parallel archives.

| Archive | Coverage | Contents |
|---|---|---|
| [Homework archive](homework/README.md) | 31 assignments, 2013–2024 | Complete public question PDFs, written derivations, reports, programs and measured evidence; HW4 stops at pre-layout SPICE. |
| [Exam archive](exams/README.md) | 20 papers, 2007–2024 | Reconstructed papers and independently checked corrected solutions; incomplete source questions are labeled. |

## Questions and solutions

The [homework archive](homework/README.md#public-assignment-questions) includes complete public question PDFs in the original page format. Only the author first name is removed from the footer; all question text, circuit figures, marks, dates and pagination are preserved. Instructor references use surname Li only.

Public exam readers can use the reconstructed papers and corrected solutions here.

## Processing workflow

[整理流程與重現方法](PROCESSING.md) explains the tools and checks used to reconstruct papers, derive and verify solutions, run SPICE simulations, and decide which TXT, PNG, JSON and other artifacts belong in the published collection.

## Verification

Python 3.10+ can verify the saved results without CAD. The [fresh-download guide](REPRODUCING.md) also covers saved-data analysis, optional plots, portable HSPICE/model configuration and preparing a runnable copy of the published testbench.

```sh
python verify_package.py
python reproduce_saved.py --outdir reproduced/saved
```

The checker verifies public artifact hashes, coverage, links, mathematical checks and saved simulation evidence. It does not launch HSPICE. Each assignment provides its own reproduction instructions. The CIC018 process model is not redistributed.

New process simulations require your own licensed HSPICE installation and authorized CIC018 model. The simulation drivers accept `--hspice`, `--model` and `--check-environment`; the environment check verifies paths without starting CAD or contacting its license service.

[MANIFEST.json](MANIFEST.json) records SHA256 hashes, with text line endings normalized to LF and binary files unchanged.
