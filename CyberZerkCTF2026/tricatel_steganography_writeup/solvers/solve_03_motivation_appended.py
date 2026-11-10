#!/usr/bin/env python3
"""
Challenge 03 - Motivational poster
File: challenges/motivation.webp (960x1438 WebP, VP8L)
Category: Steganography / Appended data (polyglot)

The RIFF header declares 27196 bytes (+8 header = file should end
at 27204), but the file is 27533 bytes. The extra 329 bytes after
the WebP are a ZIP archive (PK\\x03\\x04) containing journal_intime.txt.
No dependencies beyond the standard library.
"""
import io, re, sys, zipfile

path = sys.argv[1] if len(sys.argv) > 1 else "challenges/motivation.webp"
d = open(path, "rb").read()
declared = int.from_bytes(d[4:8], "little") + 8
print(f"RIFF declared end: {declared}, actual size: {len(d)}, appended: {len(d)-declared} bytes")

start = d.find(b"PK\x03\x04")
print(f"ZIP signature PK\\x03\\x04 at offset: {start}")
z = zipfile.ZipFile(io.BytesIO(d[start:]))
print(f"ZIP contents: {z.namelist()}")
for name in z.namelist():
    text = z.read(name).decode(errors="replace")
    print(f"--- {name} ---\n{text}")
    m = re.search(r"CyberZerk\{[^}]+\}", text)
    if m:
        print(f"[+] FLAG: {m.group()}")
