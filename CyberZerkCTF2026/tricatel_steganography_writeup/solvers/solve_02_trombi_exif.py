#!/usr/bin/env python3
"""
Challenge 02 - Marc V.'s staff directory photo
File: challenges/trombi_marc_v.jpg (400x300 JPEG)
Category: Steganography / Metadata (EXIF)

The image carries one APP1 Exif segment. Ordinary tags
(270 ImageDescription, 315 Artist) are decoys/context; the flag is
in the Exif sub-IFD, tag 37510 (0x9286) UserComment, after its
standard 8-byte 'ASCII\\0\\0\\0' character-code prefix.
No trailing data after the JPEG EOI marker.
Requires: Pillow
"""
import re, sys
from PIL import Image

path = sys.argv[1] if len(sys.argv) > 1 else "challenges/trombi_marc_v.jpg"
im = Image.open(path)
print(f"{im.format} {im.size} {im.mode}")
exif = im.getexif()
for tag, val in exif.items():
    print(f"EXIF {tag}: {val!r}")

exif_ifd = exif.get_ifd(0x8769)          # Exif sub-IFD via ExifOffset 34665
print(f"Exif IFD: {exif_ifd}")
comment = exif_ifd.get(37510, b"")       # 0x9286 UserComment
print(f"UserComment raw: {comment!r}")
m = re.search(rb"CyberZerk\{[^}]+\}", comment)
if m:
    print(f"[+] FLAG: {m.group().decode()}")
else:  # fallback: scan whole file
    m = re.search(rb"CyberZerk\{[^}]+\}", open(path, "rb").read())
    print(f"[+] FLAG (file scan): {m.group().decode()}" if m else "[-] not found")
