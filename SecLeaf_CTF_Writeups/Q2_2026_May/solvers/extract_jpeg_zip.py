#!/usr/bin/env python3
"""Extract the appended ZIP from the JPEG/ZIP polyglot at known offset 9179."""
import argparse
from pathlib import Path
import zipfile

ZIP_OFFSET = 9179

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jpeg", type=Path)
    ap.add_argument("output", nargs="?", type=Path, default=Path("embedded.zip"))
    ap.add_argument("--offset", type=lambda x: int(x, 0), default=ZIP_OFFSET)
    args = ap.parse_args()

    data = args.jpeg.read_bytes()
    sig = data.find(b"PK\x03\x04")
    print(f"[+] First local ZIP header at: {sig}")
    if sig != args.offset:
        print(f"[!] Recorded offset is {args.offset}; using explicitly selected offset {args.offset}")
    if args.offset < 0 or args.offset >= len(data):
        raise SystemExit("offset outside input file")

    tail = data[args.offset:]
    args.output.write_bytes(tail)
    print(f"[+] Wrote {len(tail)} bytes to {args.output}")

    if zipfile.is_zipfile(args.output):
        with zipfile.ZipFile(args.output) as zf:
            print("[+] ZIP entries:")
            for info in zf.infolist():
                print(f"  {info.filename}  {info.file_size} bytes  encrypted={bool(info.flag_bits & 1)}")
    else:
        print("[!] Tail is not recognized as a complete ZIP archive")

if __name__ == "__main__":
    main()
