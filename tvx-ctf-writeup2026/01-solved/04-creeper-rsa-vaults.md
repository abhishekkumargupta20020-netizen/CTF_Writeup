# Creeper RSA Vaults — Shared Prime

**Author:** Abhishek Kr Gupta
**Event:** TVXCTF, 2026-11-13
**Status:** Solved by derivation, NOT platform-confirmed

## Flag

```
TVXCTF{the_creeper_reused_a_prime}
```

## Challenge

"A Creeper built two RSA vaults with parts stolen from the same crafting
table. The message was encrypted for Vault A. Recover it."
Files: `public_keys.txt`, `ciphertext.txt`

## Method

The two vaults are two 281-bit RSA moduli that share a prime. The whole
attack is one gcd:

```
p = gcd(nA, nB) = 1393796574908163946345982392040522705234977
qA = nA / p    = 1393796574908163946345982392040523594123793
d  = e^-1 mod (p - 1)(qA - 1)        # e = 65537
m  = c^d mod nA
```

Decrypting the Vault A ciphertext with `d` gives the flag as plaintext.
No factoring was needed — the shared prime falls out of the gcd directly.

## Solver

`solvers/04-creeper-rsa-solve.py`

```bash
python3 solvers/04-creeper-rsa-solve.py
```

## Flag

```
TVXCTF{the_creeper_reused_a_prime}
```
