"""Reproduce both questions with real HSPICE. Pass flags through to both drivers."""
from pathlib import Path
import subprocess,sys
H=Path(__file__).resolve().parent
for script in ['simulate_and.py','simulate_power.py']:
 subprocess.run([sys.executable,str(H/script),*sys.argv[1:]],check=True)
