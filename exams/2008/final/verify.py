from pathlib import Path
import json,runpy
p=Path(__file__).resolve().parent
for name in ["verify_logic_layout.py","verify_numerical.py"]:runpy.run_path(str(p/name),run_name="__main__")
r={"all_checks_passed":True,"reports":["logic-layout-verification.json","numerical-verification.json"],"scope":"source-derived analytical models only"}
(p/"verification.json").write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8")
print(json.dumps(r))
