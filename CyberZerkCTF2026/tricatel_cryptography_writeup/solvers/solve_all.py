#!/usr/bin/env python3
"""Run all 5 Cryptography solvers and print the flags. Stdlib only."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOLVERS = [
    ("1 CFO Memo (Base64 + Vigenere)", "solve_01_cfo_vigenere.py"),
    ("2 Analyst's Logbook (Vigenere, key JESUISNUL)", "solve_02_logbook_vigenere.py"),
    ("3 Triple Base64 (Base64 x3)", "solve_03_triple_base64.py"),
    ("4 CFO's Safe (Repeating XOR, key TRICATEL)", "solve_04_xor_safe.py"),
    ("5 CFO's RSA (Fermat, close primes)", "solve_05_rsa_fermat.py"),
]

if __name__ == "__main__":
    ok = 0
    for label, script in SOLVERS:
        r = subprocess.run([sys.executable, str(HERE / script)],
                           capture_output=True, text=True)
        flag = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
        print(f"[{label}]")
        if r.stderr.strip():
            print(r.stderr.strip())
        print(r.stdout.strip())
        print()
        if flag.startswith("CyberZerk{"):
            ok += 1
    print(f"{ok}/5 flags extracted")
