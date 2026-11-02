#!/usr/bin/env python3
"""Reproduce the recorded emergency-transmission Vigenere test."""
import codecs

ciphertext = "VYOTYELUZSJCPMXXYQWCU"
hint = "FRPYRNS"

key = codecs.decode(hint, "rot_13")
print("ROT13(key hint):", key)

def vigenere_decrypt(ct, k):
    out = []
    k = k.upper()
    j = 0
    for ch in ct.upper():
        if "A" <= ch <= "Z":
            c = ord(ch) - 65
            s = ord(k[j % len(k)]) - 65
            out.append(chr((c - s) % 26 + 65))
            j += 1
        else:
            out.append(ch)
    return "".join(out)

repeated = (key * ((len(ciphertext) + len(key) - 1) // len(key)))[:len(ciphertext)]
print("Repeated key:", repeated)
print("Recorded Vigenere result:", vigenere_decrypt(ciphertext, repeated))
print("This output was not readable plaintext and was not accepted as a solution.")
