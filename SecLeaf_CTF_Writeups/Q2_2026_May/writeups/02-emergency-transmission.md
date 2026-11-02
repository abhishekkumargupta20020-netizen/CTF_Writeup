# Emergency Transmission — Classical Cipher Investigation

- **Competition:** SecLeaf Q2 2026
- **Date investigated:** 24 May 2026
- **Category:** Cryptography
- **Status:** Incomplete; no plaintext or accepted flag recovered

## Challenge objective

The prompt asked for a hidden message in an emergency transmission. The displayed wrapper was:

```text
SecLeaf{}
```

## Recovered ciphertext and key hint

```text
Ciphertext: VYOTYELUZSJCPMXXYQWCU
Key hint:   FRPYRNS
```

## 1. Key-hint interpretation

Applying ROT13 to the key hint:

```text
FRPYRNS  --ROT13-->  SECLEAF
```

This strongly suggested that `SECLEAF` was intended to be used as a key or keyword, but that observation alone did not establish the cipher.

## 2. Recorded Vigenère attempt

The previous attempt repeated the keyword to the ciphertext length:

```text
SECLEAFSECLEAFSECLEA
```

Manual Vigenère decryption produced:

```text
DUMIUEGCVQYYPHFTWFSCP
```

This was not readable plaintext and was not accepted as the solution.

## 3. Reproduction helper

```bash
python3 ../solvers/vigenere_probe.py
```

The helper prints the ROT13 result and the recorded Vigenère output.

## 4. What remains

Do not assume the keyword is directly the Vigenère key. Revisit:
- whether the ciphertext is encrypted or encoded,
- whether the hint is a key, a plaintext crib, or a key transformation,
- whether the cipher uses a nonstandard alphabet,
- whether the ciphertext has been transposed or transformed before classical decryption.

## 5. Status

No verified plaintext or flag was recovered in the available records. The Vigenère result above is a failed intermediate result, not the answer.
