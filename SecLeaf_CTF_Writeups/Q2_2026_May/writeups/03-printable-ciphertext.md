# Printable Ciphertext — Repeating-Key XOR Investigation

- **Competition:** SecLeaf Q2 2026
- **Category:** Cryptography
- **Status:** Incomplete; no accepted flag recovered

## Objective

Decode a printable ciphertext using the clue `KEY: SecLeaf` / `SecLeaf` as a possible repeating key.

## Evidence preserved

The ciphertext was recorded as beginning:

```text
?:%oPo\...
```

The complete byte-for-byte ciphertext is not preserved in the recovered conversation record. Therefore, this write-up does not invent the missing characters or claim a successful decryption.

## Attempts recorded

The previous investigation tried:
- repeating-key XOR with `SecLeaf`,
- case variants,
- cyclic key shifts,
- reversed key,
- ROT47,
- Base85 / Ascii85 checks.

The outputs remained corrupted or non-readable. Shifts 0–6 of the `SecLeaf` key did not produce valid plaintext.

## Reproduction guidance

Once the original ciphertext file/text is recovered, preserve it exactly:

```bash
xxd -g 1 ciphertext.bin
```

Then test candidate repeating-key XOR keys while scoring printable output. A basic probe is:

```python
def xor_repeat(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

ciphertext = open("ciphertext.bin", "rb").read()
for key in (b"SecLeaf", b"secleaf", b"SECLEAF", b"faelceS"):
    plain = xor_repeat(ciphertext, key)
    print(key, repr(plain[:200]))
```

This is only a starting test. It must not be treated as a solution unless the output is coherent and the flag is accepted.

## Status

No readable plaintext or verified `SecLeaf{...}` flag was recovered. The complete ciphertext is required for exact reproduction.
