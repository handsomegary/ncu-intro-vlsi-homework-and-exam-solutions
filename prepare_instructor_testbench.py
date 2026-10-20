"""Prepare a runnable copy of the published 2024 HW3 testbench."""
import argparse
import json
from pathlib import Path
import re
import shutil

from reproduce_saved import fresh_output
from simulation_environment import default_model, resolve_model

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',default=default_model())
    parser.add_argument('--outdir',required=True)
    args=parser.parse_args()
    try:
        model=resolve_model(args.model)
        output=fresh_output(args.outdir)
    except ValueError as exc:
        parser.error(str(exc))
    if "'" in output.as_posix():
        parser.error('Choose an output path without an apostrophe for HSPICE .include quoting.')
    original=ROOT/'homework/2024/HW3/testbench.sp'
    deck=original.read_text(encoding='ascii')
    circuit=output/'four_bit_multbased_adder.sp'
    deck,count_model=re.subn(r"(?im)^(\s*\.lib\s+)'[^']+'",lambda m:m[1]+"'"+model.as_posix()+"'",deck)
    deck,count_include=re.subn(r"(?im)^(\s*\.include\s+)'four_bit_multbased_adder\.sp'",
                               lambda m:m[1]+"'"+circuit.as_posix()+"'",deck)
    if count_model!=1 or count_include!=1:
        raise ValueError('Unexpected published testbench structure')
    output.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/'homework/2024/HW3/four_bit_multbased_adder.sp',circuit)
    target=output/'instructor_testbench.sp'
    target.write_text(deck,encoding='utf-8',newline='\n')
    print(json.dumps({'status':'prepared','deck':str(target),
                      'published_source_testbench':'unchanged',
                      'run':'hspice -i "'+str(target)+'" -o "'+str(output/'instructor')+'"'},indent=2))


if __name__=='__main__':
    main()
