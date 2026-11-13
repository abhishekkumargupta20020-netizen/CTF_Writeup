#!/usr/bin/env python3
"""WHAT A WASTE OF TOKENS... (3) - full decode of last.txt (stdlib only).

Layer 0: last.txt holds 38,312 space-separated tokens with values in
         {60, 61, 40}. 40 is a separator occurring every 9th token; each
         group of eight 60/61 tokens is one byte, MSB first (60=0, 61=1).
         Result: ASCII text of 193 decimal float32 values.
Layer 1: each value is an exact float32. Its 4 BIG-ENDIAN bytes are ASCII
         characters, giving a text of 257 space-separated decimal codes.
         (The little-endian reading also yields digits/spaces - it is a
         false trail; only the big-endian stream continues coherently.)
Layer 2: each decimal code -> one character: a hex string
         (e.g. '67 66 20 ...').
Layer 3: hex -> bytes: 29 space-separated two-letter pairs
         (gf gh gj in gi hj ef ei gv ...).
Layer 4: each pair is a byte written as two nibbles, nibbles mapped to
         letters by the table below (an alphabetical run d..n with 'm'
         dropped, extended by t=13, u=14, v=15):
             byte = 16 * TABLE[a] + TABLE[b]
         The table is forced by the known wrapper TVX{...}: T,V,X fix
         f=4,g=5,h=6,j=8; '{' and '}' fix i=7,n=11,t=13; the repeated
         pair 'ee' forces e=3 (17*e must be a flag character), 'df'
         then forces d=2 ('$'), and the alphabetical run fixes
         k=9,l=10,v=15. The solver verifies the wrapper, the flag
         charset, and an exact re-encoding of all 29 pairs.

Usage: python3 solve_01_last.py [path/to/last.txt]
"""
import struct
import sys
from pathlib import Path

TABLE = {'d': 2, 'e': 3, 'f': 4, 'g': 5, 'h': 6, 'i': 7, 'j': 8,
         'k': 9, 'l': 10, 'n': 11, 't': 13, 'v': 15}
INV = {v: k for k, v in TABLE.items()}
CHARSET = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_${}")


def solve(path):
    toks = Path(path).read_text().split()
    assert set(toks) <= {'40', '60', '61'}, set(toks)
    groups, cur = [], []
    for t in toks:
        if t == '40':
            groups.append(cur)
            cur = []
        else:
            cur.append(t)
    if cur:
        groups.append(cur)
    assert all(len(g) == 8 for g in groups)

    float_text = bytes(
        int(''.join('0' if b == '60' else '1' for b in g), 2) for g in groups
    ).decode()
    vals = [float(x) for x in float_text.split()]
    assert len(vals) == 193

    be = b''.join(struct.pack('>f', v) for v in vals)
    codes = be.decode().split()
    assert len(codes) == 257
    hex_text = ''.join(chr(int(c)) for c in codes)
    pairs = bytes.fromhex(hex_text).decode().split()
    assert len(pairs) == 29

    flag = ''.join(chr(16 * TABLE[a] + TABLE[b]) for a, b in pairs)
    assert flag.startswith('TVX{') and flag.endswith('}')
    assert set(flag) <= CHARSET
    re_encoded = ' '.join(INV[b >> 4] + INV[b & 15] for b in flag.encode())
    assert re_encoded == ' '.join(pairs), "re-encoding mismatch"
    return flag


if __name__ == '__main__':
    p = sys.argv[1] if len(sys.argv) > 1 else 'challenges/last.txt'
    print(solve(p))
