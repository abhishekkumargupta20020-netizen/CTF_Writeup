#!/usr/bin/env python3
"""Challenge 3 - "Triple-layer military-grade encryption": Base64 x3.
Peels three layers of Base64 off the token in triple_base64.txt.
Layer 2 is recognisable on sight: Q3liZXJaZXJr is Base64 for CyberZerk.
Stdlib only.
Usage: python3 solve_03_triple_base64.py [path/to/triple_base64.txt]
       python3 solve_03_triple_base64.py VVROc2FWcFlT...  (raw token)
"""
import base64
import re
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / "challenges" / "triple_base64.txt"
RAW = "VVROc2FWcFlTbUZhV0VweVpUQkpNR042VFRKT1JqbFBUVE5PTUZneFFUQmpNVGxGWkZZNVJHRkVSbTFhYmtsNllsUk9kV1JJTUQwPQ=="


def solve(arg: str | None) -> str:
    token = None
    if arg:
        m = re.search(r"[A-Za-z0-9+/=]{20,}", arg)
        token = m.group(0) if m else None
        if token is None:
            path = Path(arg)
            if not path.exists():
                token = RAW
    if token is None:
        path = Path(arg) if arg else DEFAULT
        text = path.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"[A-Za-z0-9+/=]{40,}", text)
        if not m:
            raise SystemExit("flag not found")
        token = m.group(0)
    s = token
    for layer in range(1, 4):
        s = base64.b64decode(s).decode()
        print(f"Layer {layer}: {s}")
    if not s.startswith("CyberZerk{"):
        raise SystemExit("flag not found")
    return s


if __name__ == "__main__":
    print(solve(sys.argv[1] if len(sys.argv) > 1 else None))
