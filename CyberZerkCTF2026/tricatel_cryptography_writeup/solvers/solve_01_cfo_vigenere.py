#!/usr/bin/env python3
"""Challenge 1 - CFO's encrypted memo: Base64, then Vigenere.
Base64-decodes note_chiffree.txt, then recovers the Vigenere keystream
by a known-plaintext attack on the flag format CyberZerk{...} and
decrypts the rest. Letters only; digits / _ / { } pass through and
the key does not advance on them. Stdlib only.
Usage: python3 solve_01_cfo_vigenere.py [path/to/note_chiffree.txt]
"""
import base64
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / "challenges" / "note_chiffree.txt"
KNOWN_PLAIN = "CyberZerk"


def vigenere_decrypt(ciphertext: str, keystream: list[int]) -> str:
    out, i = [], 0
    for ch in ciphertext:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            out.append(chr((ord(ch) - base - keystream[i % len(keystream)]) % 26 + base))
            i += 1
        else:
            out.append(ch)
    return "".join(out)


def solve(path: Path) -> str:
    raw = path.read_text(encoding="utf-8").strip()
    ciphertext = base64.b64decode(raw).decode()
    # Known-plaintext attack: cipher - plain over "CyberZerk" gives the
    # keystream, which repeats with period 6: [5, 14, 11, 0, 2, 4].
    keystream = [(ord(c) - ord(p)) % 26 for c, p in zip(ciphertext, KNOWN_PLAIN)]
    assert keystream[:6] == [5, 14, 11, 0, 2, 4], keystream
    assert keystream[6:9] == keystream[:3], "keystream does not repeat with period 6"
    flag = vigenere_decrypt(ciphertext, keystream[:6])
    if not flag.startswith("CyberZerk{"):
        raise SystemExit("flag not found")
    print(f"Base64 layer: {ciphertext}")
    print(f"Keystream (period 6): {keystream[:6]}")
    return flag


if __name__ == "__main__":
    p = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    print(solve(p))
