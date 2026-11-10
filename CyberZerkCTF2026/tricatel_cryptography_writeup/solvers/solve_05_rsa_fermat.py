#!/usr/bin/env python3
"""Challenge 5 - CFO's RSA: Fermat factorisation of close primes.
Parses n, e, c from cle_publique_et_message.txt. Because p and q are
strangely close, a = ceil(sqrt(n)) already gives a^2 - n as a perfect
square: p = a - b, q = a + b, with q - p = 839384 for two 154-digit
primes. Then phi = (p-1)(q-1), d = e^-1 mod phi, m = c^d mod n.
Stdlib only.
Usage: python3 solve_05_rsa_fermat.py [path/to/cle_publique_et_message.txt]
"""
import math
import re
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / "challenges" / "cle_publique_et_message.txt"


def fermat(n: int) -> tuple[int, int]:
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    while True:
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            return a - b, a + b
        a += 1


def solve(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    values = {k: int(v) for k, v in re.findall(r"([nce])\s*=\s*(\d+)", text)}
    n, e, c = values["n"], values["e"], values["c"]
    p, q = fermat(n)
    assert p * q == n
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"q - p = {q - p}")
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, n)
    pt = m.to_bytes((m.bit_length() + 7) // 8, "big").decode()
    if not pt.startswith("CyberZerk{"):
        raise SystemExit("flag not found")
    return pt


if __name__ == "__main__":
    p = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    print(solve(p))
