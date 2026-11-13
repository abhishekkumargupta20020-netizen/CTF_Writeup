#!/usr/bin/env python3
"""Run every solver for this challenge and print the flag."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAL = HERE.parent / 'challenges' / 'last.txt'

if __name__ == '__main__':
    out = subprocess.run(
        [sys.executable, str(HERE / 'solve_01_last.py'), str(CHAL)],
        capture_output=True, text=True, check=True)
    print(out.stdout.strip())
