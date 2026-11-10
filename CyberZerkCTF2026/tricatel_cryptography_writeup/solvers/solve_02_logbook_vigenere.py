#!/usr/bin/env python3
"""Challenge 2 - Analyst's logbook: Vigenere, keyed by the refrain itself.
The refrain is "I am worthless" - in French "Je suis nul" - so the key
is JESUISNUL, repeating. Letters only; _ / { } pass through.
The key is confirmed by a known-plaintext attack on CyberZerk{...}.
Stdlib only.
Usage: python3 solve_02_logbook_vigenere.py [path/to/analyst_logbook.txt]
       python3 solve_02_logbook_vigenere.py LctyzRrlv{Cy_Sm_Bs_Cflli_Awq}  (raw token)
"""
import re
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / "challenges" / "analyst_logbook.txt"
KEY = "JESUISNUL"
RAW = "LctyzRrlv{Cy_Sm_Bs_Cflli_Awq}"


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    out, i = [], 0
    for ch in ciphertext:
        if ch.isalpha():
            k = ord(key[i % len(key)]) - 65
            i += 1
            base = 65 if ch.isupper() else 97
            out.append(chr((ord(ch) - base - k) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)


def solve(arg: str | None) -> str:
    token = None
    if arg:
        m = re.search(r"[A-Za-z]+\{[A-Za-z0-9_]+\}", arg)
        token = m.group(0) if m else arg
        if not re.fullmatch(r"[A-Za-z]+\{[A-Za-z0-9_]+\}", token):
            path = Path(arg)
            if path.exists():
                token = None
            else:
                token = RAW
    if token is None:
        path = Path(arg) if arg else DEFAULT
        text = path.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"[A-Za-z]+\{[A-Za-z0-9_]+\}", text)
        if not m:
            raise SystemExit("flag not found")
        token = m.group(0)
    # Known-plaintext check: L-c=J, c-y=E, t-b=S, y-e=U, z-r=I, ...
    check = "".join(chr((ord(c) - ord(p)) % 26 + 65)
                    for c, p in zip(token, "CyberZerk"))
    assert check == KEY, f"key from known plaintext is {check}, expected {KEY}"
    flag = vigenere_decrypt(token, KEY)
    if not flag.startswith("CyberZerk{"):
        raise SystemExit("flag not found")
    return flag


if __name__ == "__main__":
    print(solve(sys.argv[1] if len(sys.argv) > 1 else None))
