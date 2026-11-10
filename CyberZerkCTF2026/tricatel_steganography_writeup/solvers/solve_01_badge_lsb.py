#!/usr/bin/env python3
"""
Challenge 01 - Marc V.'s badge
File: challenges/badge_marc_v.png (480x300 PNG)
Category: Steganography / LSB

No metadata, no text chunks, no trailing data (IHDR/IDAT/IEND only).
The secret is in the pixels: LSB of the BLUE channel only, row-major,
MSB-first packing. Starts at byte 2580 of the B-LSB stream
(bit 20640 = pixel row 43, col 0, just below the blue header band).
Requires: Pillow  (pip install Pillow)
"""
import re, sys
from PIL import Image

path = sys.argv[1] if len(sys.argv) > 1 else "challenges/badge_marc_v.png"
im = Image.open(path).convert("RGB")
print(f"{im.format} {im.size} {im.mode}")

for channel, name in [(0, "Red"), (1, "Green"), (2, "Blue")]:
    bits = [px[channel] & 1 for px in im.getdata()]
    data = bytearray()
    for i in range(0, len(bits) - 7, 8):
        b = 0
        for bit in bits[i:i+8]:
            b = (b << 1) | bit
        data.append(b)
    m = re.search(rb"CyberZerk\{[^}]+\}", bytes(data))
    print(f"{name} LSB: {'[+] FLAG: ' + m.group().decode() if m else 'nothing'}")
    if m and channel == 2:
        print(f"    offset in B-LSB stream: byte {m.start()}, bit {m.start()*8}")
