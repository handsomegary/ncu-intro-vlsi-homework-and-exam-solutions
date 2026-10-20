"""Verify the download and regenerate an analysis index from published evidence."""
import argparse
import csv
import json
import math
from pathlib import Path
import statistics

import verify_package

ROOT = Path(__file__).resolve().parent
HW = ROOT/'homework'


def fresh_output(value):
    path = Path(value).expanduser().resolve()
    # Keep the allowlist lexical: a reproduced/ symlink into homework/ must
    # not turn the protected destination itself into an allowed source tree.
    generated = ROOT/'reproduced'
    if path == ROOT or (path.is_relative_to(ROOT) and not path.is_relative_to(generated)):
        raise ValueError('Choose an output outside the repository or under its reproduced/ directory.')
    if path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise ValueError('The output directory must be new or empty.')
    return path


def write_csv(path, rows, fields):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outdir', required=True, help='New/empty output directory')
    parser.add_argument('--plots', action='store_true', help='Also plot the saved 2024 HW3 waveform')
    args = parser.parse_args()
    try:
        output = fresh_output(args.outdir)
    except ValueError as exc:
        parser.error(str(exc))
    if args.plots:
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
        except ImportError:
            parser.error('Plots require: python -m pip install -r requirements-plots.txt')
    verify_package.main()
    catalog = json.loads((HW/'COVERAGE.json').read_text(encoding='utf-8-sig'))
    index, delays = [], []
    for folder in sorted(HW.glob('[12][0-9][0-9][0-9]/HW[1-4]')):
        report = folder/'solution.pdf'
        if not report.is_file():
            report = folder/'solutions.pdf'
        if not report.is_file():
            continue
        index.append({'year':folder.parent.name,'homework':folder.name,
                      'report':report.relative_to(ROOT).as_posix(),
                      'spice_inputs':len(list(folder.glob('*.sp'))),
                      'saved_csv_files':len(list(folder.rglob('*.csv')))})
        for source in sorted(folder.rglob('*delays.csv')):
            with source.open(encoding='utf-8-sig', newline='') as stream:
                records = list(csv.DictReader(stream))
            if not records:
                continue
            for field in records[0]:
                if not field.endswith('delay_ps'):
                    continue
                values = [float(row[field]) for row in records if row.get(field)]
                if not values or not all(math.isfinite(v) for v in values):
                    continue
                delays.append({'source':source.relative_to(ROOT).as_posix(),
                               'field':field,'samples':len(values),
                               'minimum_ps':min(values),'median_ps':statistics.median(values),
                               'maximum_ps':max(values)})
    if len(index) != catalog['completed_assignments']:
        raise ValueError('Published assignment index differs from declared coverage')
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output/'assignment_index.csv', index,
              ['year','homework','report','spice_inputs','saved_csv_files'])
    write_csv(output/'delay_summary.csv', delays,
              ['source','field','samples','minimum_ps','median_ps','maximum_ps'])
    summary = {'status':'PASS','source':'published saved evidence; no simulator launched',
               'completed_assignments':len(index),
               'public_question_pdfs':json.loads((HW/'PROMPTS.json').read_text(encoding='utf-8-sig'))['pdf_files'],
               'delay_series':len(delays), 'plots':args.plots,
               'comparability':'Each delay series retains its own source conditions; no cross-year performance ranking.'}
    if args.plots:
        source = HW/'2024/HW3/results/waveform.csv'
        with source.open(encoding='utf-8-sig', newline='') as stream:
            wave = list(csv.DictReader(stream))
        figure, axes = plt.subplots(5,1,figsize=(10,8),sharex=True)
        times = [float(row['time_s'])*1e9 for row in wave]
        for axis, signal in zip(axes,['s0','s1','s2','s3','cout']):
            axis.plot(times,[float(row[signal]) for row in wave],linewidth=.8)
            axis.set_ylabel(signal+' (V)')
            axis.grid(alpha=.25)
        axes[-1].set_xlabel('Time (ns)')
        figure.suptitle('2024 HW3 published pre-layout waveform')
        figure.tight_layout()
        figure.savefig(output/'2024_hw3_waveform.png',dpi=160)
        plt.close(figure)
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
