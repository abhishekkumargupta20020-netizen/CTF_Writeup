#!/usr/bin/env python3
"""
Solver: Windows 10 memory-dump challenge ("true persistent secret").

Idea
----
The dump contains exactly two distinct TVX{...} strings:

  * TVX{dont_use_ai_for_solving}      -- decoy. It sits in the command line of
    two hidden, sleeping PowerShell processes (Start-Sleep -Seconds 86400),
    i.e. plain sight for any strings/automated scan.
  * one value stored as the SESSION_AUTH_TOKEN variable inside a process
    environment block (PEB) in RAM -- the real secret. It belongs to a
    short-lived svchost.exe (child of the interactive PowerShell) whose
    address space was already torn down when the dump was taken, so
    Volatility's windows.envars no longer lists it; the environment block
    itself survives in freed physical pages.

This solver streams the raw dump, finds every UTF-16LE environment block
that contains SESSION_AUTH_TOKEN=, parses the NAME=value list around it,
checks the block looks like a genuine Windows environment block
(SystemRoot / windir / ComSpec present), and prints the token value.

Usage:  python3 solve_01_memdump.py [path/to/memory.raw]
Stdlib only.
"""
import re
import sys

NEEDLE = "SESSION_AUTH_TOKEN=".encode("utf-16le")
CHUNK = 32 * 1024 * 1024
OVERLAP = 8192


def iter_hits(path):
    """Yield file offsets of NEEDLE in the UTF-16LE stream."""
    with open(path, "rb") as f:
        prev, base = b"", 0
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                return
            buf = prev + chunk
            start = 0
            while True:
                j = buf.find(NEEDLE, start)
                if j < 0:
                    break
                yield base - len(prev) + j
                start = j + 2
            prev = buf[-OVERLAP:]
            base += len(chunk)


def read_at(path, off, size):
    with open(path, "rb") as f:
        f.seek(off)
        return f.read(size)


def parse_env_block(path, hit):
    """Decode the environment block around `hit` and return its variables."""
    raw = read_at(path, max(0, hit - 4096), 8192 + 4096)
    text = raw.decode("utf-16le", errors="ignore")
    entries = {}
    for part in text.split("\x00"):
        if "=" in part:
            name, _, value = part.partition("=")
            name = name.strip("\x00\r\n ")
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_()]{0,40}", name or ""):
                entries[name] = value.strip()
    return entries


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "memory.raw"
    values = {}
    blocks = 0
    for hit in iter_hits(path):
        entries = parse_env_block(path, hit)
        token = entries.get("SESSION_AUTH_TOKEN", "")
        # A genuine environment block carries the standard system variables.
        if not re.fullmatch(r"TVX\{[^}\s]+\}", token or ""):
            continue
        if not {"SystemRoot", "windir", "ComSpec"} <= set(entries):
            continue
        blocks += 1
        values.setdefault(token, []).append(hex(hit))
    if not values:
        print("No SESSION_AUTH_TOKEN environment block found", file=sys.stderr)
        return 1
    for token, offs in values.items():
        print(f"SESSION_AUTH_TOKEN environment blocks: {len(offs)} "
              f"(e.g. physical offset {offs[0]})")
        print(token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
