# Fear of math — non-associative Diffie-Hellman

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Platform-confirmed

## Flag

```
spooky{spooky_scary_nonassociative_diffie_hellman}
```

## Challenge

"There is no good name for the fear of math." 734 points, author Eli S. File `chal.py` implements a non-associative loop Diffie-Hellman: `p = 1099511640127` (prime), `q` prime, `mu^p = 1 mod q`, public conjugates `g`, `Ma`, `Mb`, and a 42-byte ciphertext XORed with `SHAKE-256("loop|" + K)`. Recover the shared key `K` and decrypt.

## Files

- `challenge-files/chal.py` — the challenge
- `solvers/fear-of-math/solve.py` — the solver (also includes `chal.py` for reference)

## Solution

The associator shared key looks like it needs the secret exponents `a` and `b`, but it simplifies to a formula using only public values. With `Cg` and `Bg` from `g`, and `Ma`/`Mb` the public conjugates:

```
P = Cg*Ma_b - Bg*Ma_c
Q = Cg*Mb_b - Bg*Mb_c
R = Ma_c*Mb_b - Ma_b*Mb_c
K = mu^(2G) * (P + R - Q) / (mu - 1)  mod q
```

The formula was verified on random `a, b` before use — it matches the real shared key exactly. Computing it gives:

```
K = 286324188360977795495506529564082791425
```

Decrypting the 42-byte ciphertext with `SHAKE-256("loop|" + K)` gives the plaintext:

```
spooky_scary_nonassociative_diffie_hellman
```

## The wrapper matters

The bare 42-byte plaintext was submitted first and **rejected**. The correct platform flag is the whole decrypted string wrapped in `spooky{...}`.

## Flag

```
spooky{spooky_scary_nonassociative_diffie_hellman}
```

Submitted on the platform and accepted.

## Reproduce

```bash
python3 solvers/fear-of-math/solve.py
```

It prints `K` and the flag.
