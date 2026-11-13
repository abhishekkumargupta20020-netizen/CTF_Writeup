#!/usr/bin/env python3
"""Run every solver in this package and report the score."""
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SOLVERS = ["solve_01_ending.py"]


def main():
    ok = 0
    for name in SOLVERS:
        print(f"===== {name} =====")
        r = subprocess.run([sys.executable, os.path.join(HERE, name)] + sys.argv[1:])
        ok += (r.returncode == 0)
    print(f"\n{ok}/{len(SOLVERS)} solvers extracted the flag")
    return 0 if ok == len(SOLVERS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
