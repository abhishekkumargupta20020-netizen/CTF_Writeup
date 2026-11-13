# cryptoone — ECDLP on a Smooth-Order Curve (Pohlig–Hellman)

**Author:** Abhishek Kr Gupta
**Event:** TVXCTFCRYPTO1, 2026-11-13
**Status:** Solved — from the contributed writeup in
`contributed/tvx_all_writeups/cryptoone_writeup/` (uploaded by Shikhu).
Solver re-run here and verified: flag reproduced, decoy reproduced.

## Flag

```
TVX{D1dn5_F4lL_4_7h3_7r4p_7h15_t1me}
```

## Challenge

"ender chest — You found a world seed nobody could guess and used it as
the key to his chests. Elliptic curves are unbreakable, so the curve the
server admin picked must be fine, right?... RIGHT???"

Supplied in `cryptoone.7z`: `TVXCTFCRYPTO1/chall.py` and
`TVXCTFCRYPTO1/output.txt`. `params.py` and the flag files are not
supplied.

`chall.py` encrypts two flags with AES-256-CBC, keys `SHA256(str(d))`
(ender chest, the real flag) and `SHA256(str(Q[0]))` (shulker box), on
the curve `y² = x³ + a·x + b (mod p)`:

```
p = 4724861355973759862466485852137759          (112-bit prime)
a = 927566916496059264792326746507264
b = 4715968330470840770745781630703560
G = (3675942204092047283238136253093045, 3544727085494657603430718404172845)
Q = (3869418175838450319054504785525959, 1429060253338888234770668216689896)
```

## Method

### 1. The shulker box is a trap — do NOT submit this

Its key source is `Q[0]`, the x-coordinate of the public key, printed in
plain text in `output.txt`. Anyone can open it:

```
key = SHA256(b"3869418175838450319054504785525959")
shulker_box -> TVX{tNt_g035_B00m_C0ngr4t5}
```

"TNT goes boom" is the joke — the exploding chest. The variable in
`chall.py` is even called `REALFLAG` to talk you into stopping here.
The real flag is in the ender chest, and that one needs the secret `d`.

### 2. The curve the admin picked is not fine — its order is smooth

`p` is only 112 bits, but generic ECDLP (Pollard rho, ~2⁵⁶ steps) would
still be out of reach, and `d` is not small (no match in the first
2,000,000 multiples of `G`). The actual flaw is the group order.
Counting points (Schoof's algorithm — PARI/GP `ellcard`) gives:

```
#E = 4724861355973759917094976238449899
   = 11 × 367 × 13399 × 58453 × 484079 × 40128631 × 76927309
```

`ellgroup` reports the group as cyclic with that order, and `G` has
order exactly `#E` — `G` is a generator. Every prime factor is below
2²⁷. Textbook Pohlig–Hellman: the ECDLP is only as hard as its largest
prime factor.

The solver does not trust the point count blindly: with
`N = 4724861355973759917094976238449899` it checks in pure Python that
`N·G = O` and `(N/q)·G ≠ O` for every prime `q | N`, which together
prove `ord(G) = N` exactly.

### 3. Pohlig–Hellman: recover `d`

For each prime factor `qᵢ` of `N`, project down to the subgroup of
order `qᵢ` (`Gᵢ = (N/qᵢ)·G`, `Qᵢ = (N/qᵢ)·Q = (d mod qᵢ)·Gᵢ`) and solve
each small discrete log by baby-step / giant-step:

| qᵢ | d mod qᵢ |
|---|---|
| 11 | 3 |
| 367 | 341 |
| 13,399 | 6,052 |
| 58,453 | 1,439 |
| 484,079 | 88,736 |
| 40,128,631 | 22,612,983 |
| 76,927,309 | 44,817,997 |

CRT over the seven residues gives:

```
d = 2327569722739447708246377569803395
```

Verified directly: `d·G == Q`, exactly, on the given curve.

### 4. Open the ender chest

```
key = SHA256(str(d)) = SHA256(b"2327569722739447708246377569803395")
AES-256-CBC decrypt, strip PKCS#7
    -> TVX{D1dn5_F4lL_4_7h3_7r4p_7h15_t1me}
```

"Didn't fall for the trap this time" — the flag text itself confirms
which of the two chests was the real one.

## Solver

The contributed solver lives in its own folder and must be run from
there (it reads `challenges/output.txt` by relative path):

```bash
cd contributed/tvx_all_writeups/cryptoone_writeup
python3 solvers/solve_all.py
```

Standard library only (own pure-Python AES-256, EC arithmetic, BSGS,
Pollard-rho factoring, CRT). Prints the decoy as well as the flag so
the trap stays visible. Re-run in this session: `1/1`, flag verified.

## Flag

```
TVX{D1dn5_F4lL_4_7h3_7r4p_7h15_t1me}
```

Full writeup + PDF: `contributed/tvx_all_writeups/cryptoone_writeup/`.
