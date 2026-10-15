"""Check saved logic results, measured voltages and package hashes.

This does not claim to rerun HSPICE. See each homework README for live simulation.
Public checks use the Python standard library.
Exam verifiers regenerate deterministic analytical evidence files.
"""
from pathlib import Path
import csv
import hashlib
import itertools
import json
import math
import re
import verify_multi_year
import verify_older_years
import verify_exams

ROOT=Path(__file__).resolve().parent
HW=ROOT/'homework'
TEXT={'.md','.tex','.sp','.py','.csv','.json','.txt'}

def require(condition,message):
    if not condition: raise AssertionError(message)

def sha(file):
    data=file.read_bytes()
    if file.suffix.lower() in TEXT or file.name in ['.gitignore','.gitattributes']:
        data=data.replace(b'\r\n',b'\n')
    return hashlib.sha256(data).hexdigest()

def read_json(rel): return json.loads((HW/rel).read_text(encoding='utf-8-sig'))
def rows(rel):
    with (HW/rel).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def voltages_ok(expected,voltages):
    return all(math.isfinite(v) and (-0.02<=v<=0.2 if not ((expected>>i)&1) else 1.6<=v<=1.82) for i,v in enumerate(voltages))

def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf-8-sig'))
    for name,digest in manifest['artifact_sha256'].items():
        require(sha(ROOT/name)==digest,f'Changed artifact: {name}')
    prompts=read_json('PROMPTS.json')
    require(prompts['assignments']==31 and prompts['pdf_files']==len(prompts['prompts'])==32,'Public assignment question coverage')
    require(prompts['pages']==sum(p['pages']for p in prompts['prompts'])==37,'Public assignment question pages')
    contexts=set();paths=set()
    for prompt in prompts['prompts']:
        name=prompt['path'];match=re.fullmatch(r'homework/(\d{4})/assignments/homework([1-4])(?:_version2)?\.pdf',name)
        require(match is not None and name not in paths,'Question PDF path or duplicate')
        paths.add(name);contexts.add((prompt['year'],prompt['homework']))
        require((int(match[1]),int(match[2]))==(prompt['year'],prompt['homework']),'Question PDF context')
        require(sha(ROOT/prompt['path'])==prompt['sha256'],'Public prompt hash')
        require(prompt['all_question_and_figure_pixels_identical'] and prompt['non_author_content_operators_unchanged'] and prompt['figure_image_bytes_unchanged'] and prompt['all_pages_visually_checked'] and not prompt['contains_handwriting'],'Public prompt preservation QA')
    require(len(contexts)==31,'Question PDF assignment contexts')
    covered=set()
    for year in read_json('COVERAGE.json')['years']:
        for assignment in year['homeworks']:
            if assignment['status']=='complete':
                require(assignment.get('prompt_storage')=='public' and sha(HW/assignment['prompt'])==assignment['prompt_sha256'],'Missing complete public assignment question')
                covered.add((year['year'],assignment['homework']))
    require(covered==contexts,'Completed homework question coverage')
    require(manifest['completed_assignments']==31 and manifest['completed_exams']==20,'Published archive counts')
    full_name=re.compile(r'(?:Jin[\s_\-\u2010-\u2014]*Fu\s+Li|Li\s*,?\s*Jin[\s_\-\u2010-\u2014]*Fu|J\s*\.\s*[-\u2010-\u2014]?\s*F\s*\.\s*Li)|'+chr(26446)+'['+chr(36914)+chr(36827)+']'+chr(31119),re.I)
    for name in manifest['artifact_sha256']:
        file=ROOT/name
        if file.suffix.lower() in TEXT:
            content=file.read_text(encoding='utf-8-sig')
            if file.suffix=='.json':content=json.dumps(json.loads(content),ensure_ascii=False)
            require(not full_name.search(content),f'Instructor full name in public text: {name}')
    hw1=read_json('2024/HW1/verification.json')
    require(hw1['status']=='PASS','HW1 logic check status')
    require(len(rows('2024/HW1/truth_tables.csv'))==96,'HW1 truth-table row count')
    checks=rows('2024/HW2/validation_checks.csv')
    require(len(checks)==43 and all(r['passed']=='True' for r in checks),'HW2 numeric checks')
    exhaustive=rows('2024/HW3/results/exhaustive_512.csv')
    cases=set()
    for row in exhaustive:
        x,y,cin=(int(row[k]) for k in ['x','y','cin']);expected=x+y+cin
        case=(x,y,cin)
        require(case not in cases,'Duplicate exhaustive case');cases.add(case)
        require(int(row['expected'])==expected,'Wrong expected sum')
        volts=[float(row[k]) for k in ['s0_v','s1_v','s2_v','s3_v','cout_v']]
        require(voltages_ok(expected,volts),f'Electrical output mismatch: {case}')
        require(int(row['observed'])==expected and row['passed']=='True',f'Wrong digital output: {case}')
    require(cases==set(itertools.product(range(16),range(16),range(2))),'Incomplete exhaustive coverage')
    s=read_json('2024/HW3/results/summary.json')
    candidate=next(c for c in s['candidates'] if c['candidate']==s['selected_candidate'])
    require(math.isclose(candidate['energy_9ns_fJ'],candidate['pavg_total_uW']*9,rel_tol=1e-9),'Energy/power units')
    require(math.isclose(candidate['delay_power_fJ'],candidate['pavg_total_uW']*candidate['worst_delay_ps']*1e-3,rel_tol=1e-9),'PDP units')
    selected=(HW/'2024/HW3/four_bit_multbased_adder.sp').read_bytes().replace(b'\r\n',b'\n')
    hw4=(HW/'2024/HW4/four_bit_multbased_adder.sp').read_bytes().replace(b'\r\n',b'\n')
    require(selected==hw4,'HW4 netlist differs from verified HW3 netlist')
    h4=read_json('2024/HW4/statistics.json')
    require(sha(HW/'2024/HW4/four_bit_multbased_adder.sp')==h4['netlist_sha256'],'HW4 netlist hash mismatch')
    require(sha(HW/'2024/HW4/testbench.sp')==h4['testbench_sha256'],'HW4 testbench hash mismatch')
    v4=rows('2024/HW4/vectors.csv')
    require([(int(r['x']),int(r['y'])) for r in v4]==[(1,5),(15,13),(11,9),(4,8),(3,7),(12,14),(2,15),(6,10)],'HW4 vector order')
    for row in v4:
        expected=int(row['x'])+int(row['y'])
        require(voltages_ok(expected,[float(row[k]) for k in ['s0','s1','s2','s3','cout']]),'HW4 output voltage mismatch')
    for readme in ROOT.rglob('*.md'):
        if '.git' in readme.parts:continue
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',readme.read_text(encoding='utf-8-sig')):
            if '://' in target or target.startswith('#'):continue
            require((readme.parent/target.split('#')[0]).exists(),f'Broken link in {readme.relative_to(ROOT)}: {target}')
    verify_multi_year.main()
    verify_older_years.main()
    verify_exams.main()
    print(f'PASS: public archive; 2024 HW1 {hw1["total_asserted_cases"]} logic checks; HW2 43 checks; HW3 512 measured cases; HW4 8 measured vectors; hashes, privacy and README links.')
    print('Saved-data verification only. Reproduction commands in the homework READMEs rerun HSPICE.')

if __name__=='__main__':main()
