#!/usr/bin/env python3
"""
Challenge 02 - Intranet exfiltration
File: challenges/access.log
Category: Forensics / Log Analysis

Proof: 120/121 lines are internal 10.0.0.x, small responses.
1 line is external 45.83.12.207, GET /export.php, 200, 184320 bytes,
timestamp out-of-order (02:47 inserted between 02:26 lines).
Flag is URL-encoded in the token= query parameter.
"""
import re, sys
from urllib.parse import unquote

path = sys.argv[1] if len(sys.argv) > 1 else "challenges/access.log"

with open(path) as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines, 1):
    # Successful (200), large, external, or export.php = interesting
    if "/export.php" in line or not line.startswith("10.0.0."):
        print(f"Line {i}: {line.strip()}")
        decoded = unquote(line)  # %7B -> { , %7D -> }
        m = re.search(r"CyberZerk\{[^}]+\}", decoded)
        if m:
            print(f"[+] FLAG (URL-decoded token): {m.group(0)}")
