#!/usr/bin/env python3
"""Run every solver in this package and report how many flags were extracted."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOLVERS = ["solve_01_chest.py"]
EXPECTED = ["TVX{never_dig_straight_down}"]

def main():
    ok = 0
    for solver, flag in zip(SOLVERS, EXPECTED):
        print(f"=== {solver} ===")
        r = subprocess.run([sys.executable, os.path.join(HERE, solver)],
                           capture_output=True, text=True)
        print(r.stdout, end="")
        if r.stderr:
            print(r.stderr, end="", file=sys.stderr)
        if r.returncode == 0 and f"Flag: {flag}" in r.stdout:
            ok += 1
            print(f"[+] {solver}: flag verified")
        else:
            print(f"[-] {solver}: FAILED")
    print(f"\n{ok}/{len(SOLVERS)} challenges solved")
    return 0 if ok == len(SOLVERS) else 1

if __name__ == "__main__":
    sys.exit(main())
