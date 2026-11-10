#!/usr/bin/env python3
"""Run all 4 solvers. Usage: python3 solvers/solve_all.py [challenges_dir]"""
import subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__))
base = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(here), "challenges")
jobs = [
    ("01 Email", "solve_01_email.py", os.path.join(base, "note_du_drh.eml")),
    ("02 Log", "solve_02_access_log.py", os.path.join(base, "access.log")),
    ("03 PCAP", "solve_03_pcap.py", os.path.join(base, "appels_a_l_aide.pcap")),
    ("04 Git", "solve_04_git.py", os.path.join(base, "depot_intranet.tgz")),
]
for name, script, arg in jobs:
    print(f"\n{'='*70}\n{name}: {arg}\n{'='*70}")
    subprocess.run([sys.executable, os.path.join(here, script), arg])
