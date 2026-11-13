#!/usr/bin/env python3
"""
Solver: Ending.exe (TVX reversing) - "What has beginnings has endings".

The binary is a tiny .NET program with three layers:

  1. A string literal `package` holds Base64 -> GZip data. Unpack() opens it
     and then transforms every byte i:
         b = ROR8(b, (i % 5) + 1) XOR ((199 + 91*i) & 0xFF)
     The result is bytecode for a small virtual machine.
  2. Run() is that VM: 4 x UInt16 registers, 128 x UInt16 memory cells, a
     31-byte output buffer (the flag length), and these opcodes:
         0x10 R[a] = imm16        0x11 R[a] ^= imm16     0x12 R[a] += imm16
         0x13 R[a] = ROL16(R[a], b)
         0x14 R[a] = M[b]         0x15 M[a] = R[b]
         0x16 R[a] ^= R[b]        0x17 R[a] += R[b]      0x18 R[a] -= R[b]
         0x19 R[a] = ~R[a]        0x1A R[a] = M[R[b]]
         0x30 JNZ R[a], rel8      0x31 JMP rel8
         0x40 OUT (byte) R[a]     0xFF HALT
     (rel8 for 0x30 is added to ip *after* the offset byte is fetched;
      for 0x31 it is added to the offset byte's own position - an off-by-one
      here derails the whole program.)
  3. Main() compares your input with the VM's 31-byte output string and
     prints "accepted" / "rejected".

This solver re-implements Unpack() + the VM in pure stdlib Python and
prints the string the VM produces, i.e. the flag. Verified against the
real binary under Mono: the printed string is "accepted", the obvious
de-leeted variant is "rejected".

Usage: python3 solve_01_ending.py [path/to/Ending.exe]
"""
import base64
import gzip
import os
import struct
import sys


def extract_package(exe_bytes):
    """Pull the first #US user string (the `package` literal) out of the PE."""
    i = exe_bytes.find(b"BSJB")
    if i < 0:
        raise ValueError("no .NET metadata signature")
    ver_len = struct.unpack_from("<I", exe_bytes, i + 12)[0]
    p = i + 16 + ver_len
    _, nstreams = struct.unpack_from("<HH", exe_bytes, p)
    p += 4
    streams = {}
    for _ in range(nstreams):
        off, size = struct.unpack_from("<II", exe_bytes, p)
        p += 8
        name = b""
        while exe_bytes[p] != 0:
            name += exe_bytes[p:p + 1]
            p += 1
        p += 1
        p = (p + 3) & ~3
        streams[name.decode()] = (i + off, size)
    us_off, us_size = streams["#US"]
    us = exe_bytes[us_off:us_off + us_size]
    b0 = us[1]  # first entry, offset 1
    if b0 & 0x80 == 0:
        ln, j = b0, 2
    else:
        ln, j = ((b0 & 0x3F) << 8) | us[2], 3
    return us[j:j + ln - 1].decode("utf-16le")


def ror8(v, c):
    c &= 31
    return ((v >> c) | (v << ((8 - c) & 31))) & 0xFF


def unpack(exe_bytes):
    blob = gzip.decompress(base64.b64decode(extract_package(exe_bytes)))
    return bytes(ror8(b, (i % 5) + 1) ^ ((199 + 91 * i) & 0xFF)
                 for i, b in enumerate(blob))


def run(prog):
    R = [0] * 4
    M = [0] * 128
    out = bytearray()
    ip = 0
    for _ in range(10_000_000):
        op = prog[ip]
        ip += 1
        if op == 0xFF:
            return bytes(out)

        def rdbyte():
            nonlocal ip
            b = prog[ip]
            ip += 1
            return b

        def rdword():
            nonlocal ip
            w = prog[ip] | (prog[ip + 1] << 8)
            ip += 2
            return w

        def s8(b):
            return b - 256 if b >= 128 else b

        if op == 0x10:
            a = rdbyte(); R[a] = rdword()
        elif op == 0x11:
            a = rdbyte(); R[a] = (R[a] ^ rdword()) & 0xFFFF
        elif op == 0x12:
            a = rdbyte(); R[a] = (R[a] + rdword()) & 0xFFFF
        elif op == 0x13:
            a = rdbyte(); b = rdbyte(); v = R[a]
            R[a] = ((v << (b & 0x1F)) | (v >> ((16 - b) & 0x1F))) & 0xFFFF
        elif op == 0x14:
            a = rdbyte(); b = rdbyte(); R[a] = M[b]
        elif op == 0x15:
            a = rdbyte(); b = rdbyte(); M[a] = R[b]
        elif op == 0x16:
            a = rdbyte(); b = rdbyte(); R[a] = (R[a] ^ R[b]) & 0xFFFF
        elif op == 0x17:
            a = rdbyte(); b = rdbyte(); R[a] = (R[a] + R[b]) & 0xFFFF
        elif op == 0x18:
            a = rdbyte(); b = rdbyte(); R[a] = (R[a] - R[b]) & 0xFFFF
        elif op == 0x19:
            a = rdbyte(); R[a] = (~R[a]) & 0xFFFF
        elif op == 0x1A:
            a = rdbyte(); b = rdbyte(); R[a] = M[R[b]]
        elif op == 0x30:            # JNZ: ip already past offset byte
            a = rdbyte(); off = s8(rdbyte())
            if R[a] != 0:
                ip += off
        elif op == 0x31:            # JMP: relative to the offset byte itself
            pos = ip
            ip += 1
            ip = pos + s8(prog[pos])
        elif op == 0x40:
            a = rdbyte(); out.append(R[a] & 0xFF)
        else:
            raise RuntimeError(f"bad opcode {op:#04x} at {ip - 1:#x}")
    raise RuntimeError("runaway VM")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "challenges", "Ending.exe")
    prog = unpack(open(path, "rb").read())
    print(run(prog).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
