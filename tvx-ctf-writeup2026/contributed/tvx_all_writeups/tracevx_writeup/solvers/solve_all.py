#!/usr/bin/env python3
import subprocess, sys, pathlib
here = pathlib.Path(__file__).parent
r = subprocess.run([sys.executable, str(here/"solve_01_tracevx.py")], capture_output=True, text=True)
print(r.stdout.strip()); print(r.stderr.strip(), file=sys.stderr)
ok = 1 if "TVX{" in r.stdout else 0
print(f"{ok}/1 challenges solved")
sys.exit(0 if ok else 1)
