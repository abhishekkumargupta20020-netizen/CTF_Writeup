#!/usr/bin/env python3
import subprocess, sys, pathlib
here = pathlib.Path(__file__).resolve().parent
r = subprocess.run([sys.executable, str(here / "solve_01_ghostnote.py")])
sys.exit(r.returncode)
