from pathlib import Path
import runpy,json
base=Path(__file__).resolve().parent
for name in ["verify_register_layout.py","verify_numerical.py"]:
 runpy.run_path(str(base/name),run_name="__main__")
report={"all_checks_passed":True,"reports":["register-layout-verification.json","numerical-verification.json"],"scope":"source-derived analytical checks only"}
(base/"verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report))
