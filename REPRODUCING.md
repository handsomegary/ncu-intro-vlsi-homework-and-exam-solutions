# Reproducing a fresh download

The published homework collection contains 31 delivered assignments and 32
complete question PDFs, together with editable reports, circuit netlists,
input stimuli, analysis scripts and saved measurements. [Homework coverage](homework/COVERAGE.json)
records unavailable assignments; [exam coverage](exams/COVERAGE.json) records the
20 delivered papers and any missing premises. HW4 follows the documented
pre-layout scope. The overall preparation method is described in [PROCESSING.md](PROCESSING.md).

## Start without a CAD installation

Python 3.10 or later is sufficient. From the repository root:

```sh
python verify_package.py
python reproduce_saved.py --outdir reproduced/saved
python -m unittest discover -s tests -v
```

The verifier checks package hashes, links and numerical evidence and regenerates
deterministic exam-analysis evidence. It does not run HSPICE. The saved-result
demo repeats those checks, then writes `assignment_index.csv`,
`delay_summary.csv` and `summary.json` using published data and the standard
library. The summary counts the 32 homework question PDFs separately from report
and exam PDFs. Delay statistics retain each source's own conditions and do not
rank performance across years.

Choose a new or empty output directory outside the repository, or under its
`reproduced/` directory. Generators reject output paths in `homework/`, `exams/`
and the other source directories. Regeneration scripts and the exam verifier can
rewrite deterministic evidence; use a disposable copy when comparing release
bytes. Changing a tracked artifact requires updating its manifest and applicable
QA hashes before package verification will pass again.

To plot the saved 2024 HW3 waveform:

```sh
python -m pip install -r requirements-plots.txt
python reproduce_saved.py --outdir reproduced/plots --plots
```

This figure uses retained samples and is not a new process simulation.

## Configure a new process simulation

Provide a licensed HSPICE installation and an authorized CIC018 TT process
library. Neither is distributed here. Every direct simulation driver listed in
[simulation_entries.json](simulation_entries.json) accepts `--hspice`, `--model`
and `--check-environment`. These Python drivers have no machine-specific C:/D:
fallback locations. Explicit flags override `HSPICE` and `CIC018_MODEL`; HSPICE
can also be located on PATH.

```sh
python check_environment.py --hspice "/path/to/hspice" --model "/path/to/cic018.l"
python homework/2024/HW3/simulate.py --hspice "/path/to/hspice" --model "/path/to/cic018.l" --check-environment
```

Preflight checks file locations and executable availability. It does not run CAD,
contact a license server, read model contents, or certify model compatibility.
After preflight, remove `--check-environment` and follow the relevant homework
README to select scratch and output directories. The simulator uses its normal
license configuration. Model paths containing an apostrophe cannot be embedded
in single-quoted HSPICE `.lib` statements; use a compatible local path.

PowerShell alternative:

```powershell
$env:HSPICE = 'C:\your-installed-tools\hspice.com'
$env:CIC018_MODEL = 'C:\your-authorized-models\cic018.l'
python .\check_environment.py
python .\homework\2024\HW2\reproduce.py --check-environment
```

Static SPICE decks and saved run descriptions retain their documented earlier
model paths. Python drivers substitute the selected model into runtime decks;
configure static decks before executing them directly. The 2024 HW2 driver
rewrites scratch copies of its model-dependent deck and preserves its published
SPICE files. The 2016/2017 HW3 wrapper commands forward flags to both child
drivers. Only actual HSPICE output constitutes a fresh electrical measurement.

These modes require neither simulator nor process model:

```sh
python homework/2018/HW2/reproduce.py --analytical-only
python homework/2019/HW2/reproduce.py --analytical-only
python homework/2020/HW2/reproduce.py --skip-hspice
python homework/2023/HW2/reproduce.py --logic-only
python homework/2013/HW3/reproduce.py --prepare-only
```

They can regenerate files in their homework directories. Unexecuted decks
prepared without a model use the explicit `CIC018_MODEL_REQUIRED.l` placeholder;
a real authorized model is required before running them.

## Prepare the published HW3 testbench

[homework/2024/HW3/testbench.sp](homework/2024/HW3/testbench.sp) contains the assigned
PWL inputs, eight input words, power measurement and 9 ns transient setting.
The helper retains its historical filename `prepare_instructor_testbench.py`
and uses this public deck and the delivered final HW3 circuit:

```sh
python prepare_instructor_testbench.py --model "/path/to/cic018.l" --outdir reproduced/instructor
hspice -i reproduced/instructor/instructor_testbench.sp -o reproduced/instructor/run
```

Use your selected executable instead of `hspice` if it is not on PATH. The helper
copies the circuit and replaces only the `.lib` and `.include` paths, making the
copy independent of the simulator's working directory. It preserves the public
source files, PWL inputs, vectors and duration. It prepares files without
launching the simulator.

## Reports and optional packages

Compiled PDFs are included. Rebuilding standalone reports requires pdfLaTeX and
the packages declared in each document, commonly TikZ/PGFPlots, AMS math,
geometry, booktabs, fontenc/lmodern, listings and hyperref. Preserve relative
figure/data paths when present. The optional Matplotlib requirement is used only
for Python-generated plots. The automated environment tests use a path fixture
and a mocked CAD boundary; they do not test HSPICE licensing or validate a new
process-model result.
