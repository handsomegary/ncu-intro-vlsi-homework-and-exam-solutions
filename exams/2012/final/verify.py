from pathlib import Path
import runpy,json
base=Path(__file__).resolve().parent
for name in ["verify_numerical.py","verify_q5.py","verify_logic_layout.py"]:
    runpy.run_path(str(base/name),run_name="__main__")
report={"all_checks_passed":True,"scope":"source-defined analytical models, no SPICE claim","reports":["numerical-verification.json","q5-verification.json","logic-layout-verification.json"]}
(base/"verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report))
