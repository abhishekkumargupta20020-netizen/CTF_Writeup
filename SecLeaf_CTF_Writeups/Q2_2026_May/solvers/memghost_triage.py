#!/usr/bin/env python3
"""Read-only MemGhost triage helper. Lists flag-shaped strings and offsets."""
import argparse
import re
from pathlib import Path

FLAG_RE = re.compile(rb"SecLeaf\{[^}\r\n]{1,100}\}")
DECOYS = {
    b"SecLeaf{y0u_f0und_m3_haha_n0pe}",
    b"SecLeaf{alm0st_th3r3_just_k1dd1ng}",
    b"SecLeaf{wr0ng_flag_ag41n}",
    b"SecLeaf{r3ally_th1s_t1me_nope}",
    b"SecLeaf{n1c3_try_th1s_1snt_1t}",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dump", type=Path)
    args = ap.parse_args()
    data = args.dump.read_bytes()
    print(f"[+] File: {args.dump} ({len(data)} bytes)")
    print("[+] Flag-shaped strings:")
    seen = set()
    for m in FLAG_RE.finditer(data):
        value = m.group()
        seen.add(value)
        label = "known decoy" if value in DECOYS else "candidate / inspect context"
        print(f"0x{m.start():06x}  {label:26s}  {value.decode('ascii', 'replace')}")
    print("\n[+] Context marker:")
    marker = b"NOTE: The flag you need is hidden in plain sight."
    off = data.find(marker)
    if off >= 0:
        print(f"0x{off:06x}  {marker.decode()}")
    else:
        print("not found")
    print("\n[!] This script enumerates strings; it does not prove which candidate is accepted.")

if __name__ == "__main__":
    main()
