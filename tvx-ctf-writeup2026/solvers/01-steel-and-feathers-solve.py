#!/usr/bin/env python3
"""SteelAndFeathers.exe solver.
.NET exe: Unpack() base64+gzip, then per-byte ROR(i%7+1) ^ (23+i*41)
Run() is a stack VM (opcodes 0x10 push imm, 0x20 xor, 0x30 add,
0x40 rol, 0x51 pop, 0x60 store mem, 0x61 load mem, 0x70 output, 0xFF halt)
whose output is the expected flag string checked by Main().
"""
import base64, gzip, pathlib, re
exe = pathlib.Path.home()/"workspace/user/files/SteelAndFeathers.exe"
data = exe.read_bytes()
strs = [m.group().decode('utf-16le') for m in re.finditer(rb'(?:[\x20-\x7e]\x00){4,}', data)]
b64 = [s for s in strs if s.startswith('H4sI')][0]
arr = bytearray(gzip.decompress(base64.b64decode(b64)))
def ror(x,n):
    return ((x >> (n & 31)) | (x << ((8-n) & 31))) & 0xFF
for i in range(len(arr)):
    arr[i] = (ror(arr[i], i%7+1) ^ ((23 + i*41) & 0xFF)) & 0xFF
mem = bytearray(256); mem[250] = 45  # '-'
stack, out, pc = [], [], 0
while True:
    op = arr[pc]; pc += 1
    if op == 0xFF: break
    elif op == 0x10: stack.append(arr[pc]); pc += 1
    elif op == 0x20: stack.append((stack.pop() ^ stack.pop()) & 0xFF)
    elif op == 0x30: stack.append((stack.pop() + stack.pop()) & 0xFF)
    elif op == 0x40:
        v = stack.pop(); sh = arr[pc]; pc += 1
        stack.append(((v << (sh & 31)) | (v >> ((8-sh) & 31))) & 0xFF)
    elif op == 0x51: stack.pop()
    elif op == 0x60: mem[arr[pc]] = stack.pop(); pc += 1
    elif op == 0x61: stack.append(mem[arr[pc]]); pc += 1
    elif op == 0x70: out.append(stack.pop())
    else: raise SystemExit(f"unknown opcode {op:#x} at {pc-1}")
print(bytes(out).decode('ascii'))
