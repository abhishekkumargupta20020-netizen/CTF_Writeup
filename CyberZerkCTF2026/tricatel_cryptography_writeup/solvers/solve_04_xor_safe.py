#!/usr/bin/env python3
"""Challenge 4 - CFO's safe: repeating-key XOR.
Hex-decodes coffre_chiffre.hex (40 bytes), recovers the repeating XOR
key by a known-plaintext attack on the flag format CyberZerk{...}:
cipher ^ plain over the first 10 bytes gives TRICATELTR, i.e. key
TRICATEL with period 8, repeating. Stdlib only.
Usage: python3 solve_04_xor_safe.py [path/to/coffre_chiffre.hex]
"""
import re
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / "challenges" / "coffre_chiffre.hex"
KNOWN_PLAIN = b"CyberZerk{"


def solve(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    hex_token = re.search(r"[0-9a-fA-F]{40,}", text).group(0)
    ct = bytes.fromhex(hex_token)
    key_stream = bytes(c ^ p for c, p in zip(ct, KNOWN_PLAIN))
    print(f"Key stream from known plaintext: {key_stream}")
    # TRICATELTR -> key repeats with period 8
    key = key_stream[:8]
    assert key == b"TRICATEL", key
    assert key_stream[8:] == key[:2], "key does not repeat with period 8"
    pt = bytes(b ^ key[i % len(key)] for i, b in enumerate(ct)).decode()
    print(f"Key (period {len(key)}): {key.decode()}")
    if not pt.startswith("CyberZerk{"):
        raise SystemExit("flag not found")
    return pt


if __name__ == "__main__":
    p = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    print(solve(p))
