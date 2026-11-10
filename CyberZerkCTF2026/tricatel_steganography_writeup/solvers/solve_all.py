#!/usr/bin/env python3
"""Run all 4 solvers. Usage: python3 solvers/solve_all.py [challenges_dir]"""
import subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__))
base = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(here), "challenges")
jobs = [
    ("01 Badge LSB", "solve_01_badge_lsb.py", os.path.join(base, "badge_marc_v.png")),
    ("02 Trombi EXIF", "solve_02_trombi_exif.py", os.path.join(base, "trombi_marc_v.jpg")),
    ("03 Motivation appended ZIP", "solve_03_motivation_appended.py", os.path.join(base, "motivation.webp")),
    ("04 Crise tEXt + XOR", "solve_04_crise_text_xor.py", os.path.join(base, "affiche_crise.png")),
]
for name, script, arg in jobs:
    print(f"\n{'='*70}\n{name}: {arg}\n{'='*70}")
    subprocess.run([sys.executable, os.path.join(here, script), arg])
