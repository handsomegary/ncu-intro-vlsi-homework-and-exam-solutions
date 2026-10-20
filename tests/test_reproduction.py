"""Check that fresh-download entry points work without private machine defaults."""
import hashlib
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from reproduce_saved import fresh_output

ROOT=Path(__file__).resolve().parents[1]
ENTRIES=json.loads((ROOT/'simulation_entries.json').read_text(encoding='utf-8'))['entries']


class ReproductionEnvironment(unittest.TestCase):
    def setUp(self):
        base=os.environ.get('VLSI_TEST_TEMP')
        if base:
            Path(base).mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(prefix='vlsi reproduction ',dir=base)
        self.work=Path(self.temp.name)
        self.model=self.work/'authorized model fixture.l'
        # This is a path fixture only. The checker must never execute/read it as a PDK.
        self.model.write_text('* environment-check path fixture, not a process model\n')
        self.environment=os.environ.copy()
        self.environment.pop('HSPICE',None)
        self.environment.pop('CIC018_MODEL',None)

    def tearDown(self):
        self.temp.cleanup()

    def invoke(self, script, flags=(), env=None, root=ROOT):
        return subprocess.run([sys.executable,'-B',str(root/script),*map(str,flags)],
                              cwd=self.work,env=env or self.environment,
                              capture_output=True,text=True,timeout=30)

    def test_every_driver_rejects_missing_model_before_simulation(self):
        for entry in ENTRIES:
            with self.subTest(entry=entry['path']):
                result=self.invoke(entry['path'],['--hspice',sys.executable,'--check-environment'])
                self.assertEqual(result.returncode,2,result.stdout+result.stderr)
                self.assertIn('Supply --model',result.stderr)

    def test_explicit_paths_with_spaces_reach_all_driver_preflights(self):
        initial_files={p.relative_to(self.work) for p in self.work.rglob('*')}
        for entry in ENTRIES:
            with self.subTest(entry=entry['path']):
                result=self.invoke(entry['path'],['--hspice',sys.executable,'--model',self.model,'--check-environment'])
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                answer=json.loads(result.stdout)
                self.assertEqual(Path(answer['model']),self.model.resolve())
                self.assertEqual(Path(answer['hspice']),Path(sys.executable).resolve())
                self.assertEqual(answer['license_and_model_compatibility'],'not probed')
                self.assertEqual({p.relative_to(self.work) for p in self.work.rglob('*')},initial_files)

    def test_invalid_executable_and_model_are_actionable(self):
        result=self.invoke('check_environment.py',['--hspice',self.work/'missing-executable','--model',self.model])
        self.assertEqual(result.returncode,2)
        self.assertIn('HSPICE executable not found',result.stderr)
        result=self.invoke('check_environment.py',['--hspice',sys.executable,'--model',self.work/'missing-model.l'])
        self.assertEqual(result.returncode,2)
        self.assertIn('Process model not found',result.stderr)

    def test_environment_variables_are_supported(self):
        env=self.environment.copy()
        env.update(HSPICE=sys.executable,CIC018_MODEL=str(self.model))
        result=self.invoke('check_environment.py',env=env)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_prepared_public_deck_preserves_source_and_has_resolved_includes(self):
        original=ROOT/'homework/2024/HW3/testbench.sp'
        before=hashlib.sha256(original.read_bytes()).hexdigest()
        target=self.work/'prepared circuit'
        result=self.invoke('prepare_instructor_testbench.py',['--model',self.model,'--outdir',target])
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(),before)
        deck=(target/'instructor_testbench.sp').read_text()
        self.assertIn(".lib '"+self.model.as_posix()+"'",deck)
        self.assertIn(".include '"+(target/'four_bit_multbased_adder.sp').as_posix()+"'",deck)
        self.assertEqual((target/'four_bit_multbased_adder.sp').read_bytes(),
                         (ROOT/'homework/2024/HW3/four_bit_multbased_adder.sp').read_bytes())
        self.assertIn('.tran 0.1ns 9n',deck.lower())
        def without_paths(text):
            return re.sub(r"(?im)^(\s*\.(?:lib|include)\s+)'[^']+'",r"\1'<PATH>'",text)
        self.assertEqual(without_paths(deck),without_paths(original.read_text(encoding='ascii')))

    def test_saved_demo_works_without_cad_and_protects_sources(self):
        output=self.work/'saved demo'
        result=self.invoke('reproduce_saved.py',['--outdir',output])
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        summary=json.loads((output/'summary.json').read_text())
        self.assertEqual(summary['completed_assignments'],31)
        self.assertEqual(summary['public_question_pdfs'],32)
        self.assertGreater(summary['delay_series'],0)
        self.assertTrue((output/'assignment_index.csv').is_file())
        self.assertTrue((output/'delay_summary.csv').is_file())
        result=self.invoke('reproduce_saved.py',['--outdir',ROOT/'homework/2024/HW3'])
        self.assertEqual(result.returncode,2)
        result=self.invoke('reproduce_saved.py',['--outdir',output])
        self.assertEqual(result.returncode,2)

    def test_output_guard_rejects_new_directories_inside_every_source_tree(self):
        # These targets do not need to exist: merely being empty/new must not
        # allow a generator to write inside a tracked source hierarchy.
        for relative in ['homework/2024/HW3/new-output','exams/2024/final/new-output',
                         'tests/new-output','.github/workflows/new-output',
                         '.git/new-output','new-root-output']:
            with self.subTest(relative=relative):
                target=ROOT/relative
                self.assertFalse(target.exists())
                with self.assertRaises(ValueError):fresh_output(target)
                self.assertFalse(target.exists())
        with self.assertRaises(ValueError):fresh_output(ROOT)
        self.assertEqual(fresh_output(ROOT/'reproduced/new-output'),
                         (ROOT/'reproduced/new-output').resolve())
        self.assertEqual(fresh_output(self.work/'external output'),
                         (self.work/'external output').resolve())

    def test_prepared_deck_keeps_unicode_output_path_and_rejects_apostrophe(self):
        output=self.work/('prepared '+chr(0x984c)+chr(0x76ee))
        result=self.invoke('prepare_instructor_testbench.py',
                           ['--model',self.model,'--outdir',output])
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        deck=(output/'instructor_testbench.sp').read_text(encoding='utf-8')
        self.assertIn((output/'four_bit_multbased_adder.sp').as_posix(),deck)
        forbidden=self.work/"can't quote this"
        result=self.invoke('prepare_instructor_testbench.py',
                           ['--model',self.model,'--outdir',forbidden])
        self.assertEqual(result.returncode,2)
        self.assertIn('apostrophe',result.stderr)
        self.assertFalse(forbidden.exists())

    def test_analytical_modes_need_no_model_or_simulator(self):
        copy=self.work/'disposable download'
        shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('.git','__pycache__','reproduced'))
        flags={'prepare_only':'--prepare-only','analytical_only':'--analytical-only',
               'skip_hspice':'--skip-hspice','logic_only':'--logic-only'}
        for entry in ENTRIES:
            if not entry['non_simulation_mode']:
                continue
            with self.subTest(entry=entry['path']):
                result=self.invoke(entry['path'],[flags[entry['non_simulation_mode']]],root=copy)
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_2024_hw2_model_override_only_changes_scratch_deck(self):
        copy=self.work/'hw2 disposable download'
        shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('.git','__pycache__','reproduced'))
        source=copy/'homework/2024/HW2/reproduce.py'
        before={p.name:p.read_bytes() for p in source.parent.glob('*.sp')}
        spec=importlib.util.spec_from_file_location('hw2_reproduction_fixture',source)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        raw=self.work/'selected model runtime'
        failed=subprocess.CompletedProcess([],1,stdout=b'',stderr=b'')
        # Stop at the CAD boundary while exercising real CLI/deck construction.
        with patch.object(sys,'argv',[str(source),'--hspice',sys.executable,
                                      '--model',str(self.model),'--raw-dir',str(raw)]), \
             patch.object(module.subprocess,'run',return_value=failed), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main(),1)
        deck=(raw/'q2_cic018_tt.sp').read_text()
        self.assertIn(".lib '"+self.model.as_posix()+"'",deck)
        self.assertNotIn(".lib 'D:/cic018.l'",deck)
        self.assertEqual(before,{p.name:p.read_bytes() for p in source.parent.glob('*.sp')})


if __name__=='__main__':
    unittest.main()
