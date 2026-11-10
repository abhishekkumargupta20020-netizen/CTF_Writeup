#!/usr/bin/env python3
"""
Challenge 04 - Crisis management poster (two-part challenge)
File: challenges/affiche_crise.png (320x200 PNG)
Category: Steganography + Crypto (tEXt chunk key / appended XOR)

Part 1 - the KEY, inside the image structure:
  A tEXt chunk 'cle\\x00Y3IxczMtdGMyNg=='  -> Base64 -> b'cr1s3-tc26'
Part 2 - the MESSAGE, appended after the image:
  35 bytes of binary after the IEND chunk (IEND ends at 13056,
  file is 13091 bytes).
Part 3 - one reads the other: repeating-key XOR.
No dependencies beyond the standard library.
"""
import base64, re, struct, sys

path = sys.argv[1] if len(sys.argv) > 1 else "challenges/affiche_crise.png"
d = open(path, "rb").read()
print(f"Total size: {len(d)}")

off, key_b64, iend_end = 8, None, None
while off + 8 <= len(d):
    length, typ = struct.unpack(">I4s", d[off:off+8])
    chunk = d[off+8:off+8+length]
    print(f"chunk @{off}: {typ.decode()} len={length}" + (f" -> {chunk!r}" if typ == b"tEXt" else ""))
    if typ == b"tEXt":
        keyword, _, value = chunk.partition(b"\x00")
        print(f"    keyword={keyword.decode()!r} value={value.decode()!r}")
        key_b64 = value
    off += 8 + length + 4
    if typ == b"IEND":
        iend_end = off
        break

key = base64.b64decode(key_b64)
print(f"Key: Base64 {key_b64.decode()} -> {key!r} ({len(key)} bytes)")

cipher = d[iend_end:]
print(f"Appended after IEND @{iend_end}: {len(cipher)} bytes: {cipher.hex()}")

plain = bytes(b ^ key[i % len(key)] for i, b in enumerate(cipher))
print(f"XOR decrypted: {plain!r}")
m = re.search(rb"CyberZerk\{[^}]+\}", plain)
if m:
    print(f"[+] FLAG: {m.group().decode()}")
