#!/usr/bin/env python3
"""SummerIsOver.exe solver.
Reveal():
  blob 26 bytes, schedule 8 bytes (static arrays)
  for i in range(26):
    j=(5*i+1)%26
    v=blob[j]
    v ^= (51+11*i) & 0xFF
    v ^= schedule[i % 8]
    v = (v - ((i*i*3+25) & 0xFF)) & 0xFF
    v = ROR(v, i%5+1)
    out[i] = v ^ ((33+7*i) & 0xFF)
  final = out with each 4-byte block reversed
  return ASCII(final)
"""
blob = bytes([233,147,146,170,148,228,241,180,70,143,4,16,157,84,163,89,78,57,138,62,119,57,99,250,2,251])
schedule = bytes([109,18,169,64,243,39,136,91])
def ror(x,n):
    return ((x >> (n & 31)) | (x << ((8-n) & 31))) & 0xFF
out = bytearray(len(blob))
for i in range(len(blob)):
    j = (5*i+1) % len(blob)
    v = blob[j]
    v ^= (51+11*i) & 0xFF
    v ^= schedule[i % len(schedule)]
    v = (v - ((i*i*3+25) & 0xFF)) & 0xFF
    v = ror(v, i%5+1)
    out[i] = (v ^ ((33+7*i) & 0xFF)) & 0xFF
final = bytearray(len(out))
for i in range(len(out)):
    bs = (i//4)*4
    bl = min(4, len(out)-bs)
    final[bs+bl-1-(i-bs)] = out[i]
print(bytes(final).decode('ascii'))
print("intermediate out:", bytes(out).decode('ascii', errors='replace'))
