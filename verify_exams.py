"""Verify published exam artifacts, declared question scope, printed points and analytical circuit evidence."""
from pathlib import Path
import csv,json,math
ROOT=Path(__file__).resolve().parent
P=ROOT/'exams'/'2024'/'midterm'
def need(ok,msg):
    if not ok:raise AssertionError(msg)
def js(name):return json.loads((P/name).read_text(encoding='utf-8-sig'))
def rows(name):
    with (P/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))





def verify_2024_midterm():
    for name in ['exam.pdf','solution.pdf']:
        need((P/name).read_bytes().startswith(b'%PDF-'),'Missing exam PDF')
    for name in ['exam.tex','solution.tex']:
        tex=(P/name).read_text(encoding='utf-8')
        need('\\begin{document}' in tex and '\\end{document}' in tex,'Standalone TeX')
        need('\\includegraphics' not in tex and '\\input{' not in tex,'Editable standalone reconstruction')
    s=js('sources.json')
    coverage=json.loads((ROOT/'exams'/'COVERAGE.json').read_text(encoding='utf-8-sig'))
    item=next(e for e in coverage['completed_exams'] if e['year']==2024 and e['exam']=='midterm')
    need(item['status']=='complete' and item['questions']==7,'Published midterm question scope')
    need(sum(s['question_points'])==100 and sum(s['question_1_part_points'])==30,'Printed point totals')
    q=js('q2_q7_verification.json');need(q['status']=='PASS','Logic status')
    a=rows('q2_mux_truth.csv');need(len(a)==16,'MUX coverage')
    seen=set()
    for r in a:
        s,x,y,z=(int(r[k]) for k in ['s','x','y','z']);seen.add((s,x,y,z))
        expected=int((y and (x or z)) if s else (x or y or z))
        need(int(r['expected'])==int(r['mux_output'])==expected and r['passed']=='True','MUX independent cofactor check')
    need(len(seen)==16,'Unique MUX cases')
    a=rows('q7_switch_checks.csv');need(len(a)==32,'CMOS coverage')
    counts={'a':0,'b':0,'c':0}
    for r in a:
        x,y,z=(int(r[k]) for k in ['X','Y','Z']);part=r['part'];counts[part]+=1
        underlying=(x and (y or z)) if part=='a' else ((x and y) or z) if part=='b' else (x or (y and (int(r['W']) or z)))
        expected=int(not underlying)
        need(int(r['expected'])==int(r['output'])==expected and r['rail_exclusive']=='True' and r['passed']=='True','CMOS independent polarity/rail check')
    need(counts=={'a':8,'b':8,'c':16},'CMOS part coverage')
    q=js('q3_q6_verification.json')
    need(len(rows('q3_stage_checks.csv'))==40 and len(rows('q4_regions.csv'))==15 and len(rows('q5_noise_scenarios.csv'))==4,'Analytical row counts')
    for case in q['Q3']['cases'][:2]:
        b=case['best'];h=case['input_cap_over_Cg']
        need(b['total_stages_including_A']==3 and b['inserted_inverters']==2 and b['inserted_buffer_noninverting'],'Chain polarity/count')
        need(math.isclose(b['delay_T_over_R_Cg'],3*h**(1/3),rel_tol=1e-12),'Chain delay')
    need(math.isclose(q['Q4']['rising_input_switch_onset_V'],.8),'Switch-R threshold')
    need(q['Q5']['source_quantitative_noise_margins'] is None,'No invented source margins')
    original=q['Q6']['student_design_recomputed'];fixed=q['Q6']['corrected_design']
    need(original['worst_delay_over_R_Cg']==10 and not original['strictly_below_8_R_Cg'],'Student capacitance error retained')
    need(fixed['inverter_input_cap_over_Cg']==3 and fixed['AND_output_rise_delay_over_R_Cg']==fixed['AND_output_fall_delay_over_R_Cg']==7 and fixed['strictly_below_8_R_Cg'],'Corrected strict delay bound')
    qa=js('pdf_qa.json')
    need(qa['all_final_pages_visually_checked'] and qa['exam_pages']==2 and qa['solution_pages']==6 and qa['overfull_boxes']==0 and qa['typeset_raster_image_count']==0,'PDF QA and editable vectors')
    print('PASS: 2024 midterm; 7 questions/100 points, 16 MUX +32 CMOS cases, conditional buffer sizing, corrected 7RCg bound, standalone vector PDFs.')
def main():
    import subprocess,sys
    coverage=json.loads((ROOT/'exams'/'COVERAGE.json').read_text(encoding='utf-8-sig'))
    need(len(coverage['completed_exams'])>=1,'Exam coverage count')
    for item in coverage['completed_exams']:
        p=ROOT/'exams'/str(item['year'])/item['exam']
        for key in ['exam_pdf','exam_tex','solution_pdf','solution_tex']:
            artifact=(ROOT/'exams'/item[key]).resolve()
            need(artifact.is_relative_to((ROOT/'exams').resolve()),'Public exam artifact must remain inside exams')
            need(artifact.is_file(),'Public coverage artifact missing')
        for name in ['exam.pdf','solution.pdf']:
            need((p/name).read_bytes().startswith(b'%PDF-'),'Missing exam PDF')
        for name in ['exam.tex','solution.tex']:
            tex=(p/name).read_text(encoding='utf-8')
            need('\\begin{document}' in tex and '\\end{document}' in tex,'Standalone TeX')
            need('\\includegraphics' not in tex and '\\input{' not in tex,'Editable standalone reconstruction')
        if item['status']!='complete':need('missing' in item,'Partial question scope must be labeled')
        for script in sorted(p.glob('verify*.py')):
            subprocess.run([sys.executable,str(script)],cwd=p,check=True)
    verify_2024_midterm()
    p=ROOT/'exams'/'2024'/'final'
    if p.exists():
        s=json.loads((p/'sources.json').read_text(encoding='utf-8'))
        need(sum(s['question_points'])==110,'Preserve printed final point total')
        need(any(e['year']==2024 and e['exam']=='final' and e['status']=='complete' and e['questions']==6 for e in coverage['completed_exams']),'Published final question scope')
        q=json.loads((p/'pdf_qa.json').read_text(encoding='utf-8'))
        need(q['all_final_pages_visually_checked'] and q['typeset_raster_image_count']==q['overfull_boxes']==0,'Final PDF QA')
    print('PASS:',len(coverage['completed_exams']),'public exam packets; declared scope, editable sources and all analytical evidence.')
    return {'status':'PASS','exam_packets':len(coverage['completed_exams'])}

if __name__=='__main__':main()
