#!/usr/bin/env python3
"""TwistMeATwister.exe solver.
Reveal(): for i in 0..39: j=(7*i+3)%40; out[i]=ROR(data[j], j%5+1) ^ ((55+11*j)&0xFF)
data is the 40-byte static array at RVA 0x2130.
"""
import pathlib
data = bytes([162,216,9,192,74,180,56,71,143,213,231,22,230,127,188,219,2,85,152,237,76,229,224,182,136,102,176,160,67,64,235,43,70,223,94,189,250,205,91,18])
def ror(x,n):
    return ((x >> (n & 31)) | (x << ((8-n) & 31))) & 0xFF
out = bytearray(len(data))
for i in range(len(data)):
    j = (i*7 + 3) % len(data)
    v = ror(data[j], j % 5 + 1)
    v ^= (55 + 11*j) & 0xFF
    out[i] = v & 0xFF
print(bytes(out).decode('ascii'))
print(bytes(out))
