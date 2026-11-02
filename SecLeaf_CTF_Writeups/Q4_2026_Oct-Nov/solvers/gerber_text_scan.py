#!/usr/bin/env python3
"""Quick text/metadata scan across extracted Gerber and drill files."""
import argparse
from pathlib import Path
import re

PAT = re.compile(rb"SecLeaf|flag|G04|EasyEDA|Gerber", re.I)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("directory", type=Path)
    args = ap.parse_args()
    for path in sorted(args.directory.rglob("*")):
        if not path.is_file():
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        hits = list(PAT.finditer(data))
        if hits:
            print(f"\n[{path}] {len(hits)} metadata/text matches")
            for m in hits[:30]:
                lo, hi = max(0, m.start()-40), min(len(data), m.end()+100)
                print(f"  offset=0x{m.start():x}: {data[lo:hi]!r}")

if __name__ == "__main__":
    main()
