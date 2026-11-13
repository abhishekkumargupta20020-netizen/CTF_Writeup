# The Fourth Portal — Forged Beacons, Degree-7 Poly, AES-GCM Vault

**Author:** Abhishek Kr Gupta
**Event:** TVX CTF, 2026-11-13
**Status:** Solved by derivation, NOT platform-confirmed

## Flag

```
TVX{th3_3ch0_b1nds_th3_f0ur_w0rlds}
```

## Challenge

"An abandoned portal links the Overworld, the Nether, and the End. Then
a fourth world answers: the Echo. Its vault is sealed, and someone has
forged beacon readings in each of the old dimensions. Rebuild what the
three worlds lost, bring the Echo's piece, and open the vault."
Flag format: `TVX{...}`

## Method

Each world has 16 beacons; coordinates are taken mod 257. The honest
readings in each world fit a degree-7 polynomial

```
Z = c0 + c1*X + ... + c7*X^7   (mod 257)
```

with 4 forged readings and 12 honest ones per world:

- Overworld: `[142, 244, 194, 72, 92, 128, 2, 138]`
- Nether:    `[147, 108, 179, 81, 164, 6, 234, 230]`
- End:       `[201, 58, 11, 177, 171, 157, 123, 10]`

The Echo's piece was intact in `core.hex`:

```
6e 11 c3 61 9f ee 00 c4
```

Interleaving Overworld, Nether, End, Echo per row gave the 32-byte frame:

```
8e93c96ef46c3a11c2b30bc34851b1615ca4ab9f80069dee02ea7b008ae60ac4
```

HKDF-SHA256 (salt `4a06df8e10e1cb1e5c5fd2373f125dda`,
info `"TVX:fourth-portal:v1"`) derived the key, and AES-256-GCM
decryption of `vault.json` verified by its GCM tag — so the decrypt is
solid, not a guess.

## Solver

`solvers/09-fourth-portal-solve.py` — needs `pip install cryptography`:

```bash
python3 solvers/09-fourth-portal-solve.py
```

## Flag

```
TVX{th3_3ch0_b1nds_th3_f0ur_w0rlds}
```
