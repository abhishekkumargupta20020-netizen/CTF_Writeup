#!/usr/bin/env python3
"""
cryptoone (TVXCTFCRYPTO1) -- "ender chest"

chall.py (paraphrased):
    Q = d * G                                  on y^2 = x^3 + a*x + b (mod p)
    ender_chest = AES-256-CBC(SHA256(str(d)),    FLAG)
    shulker_box = AES-256-CBC(SHA256(str(Q[0])), REALFLAG)

Traps / weakness:
  1. shulker_box needs only Q[0], which is published in output.txt.
     It decrypts immediately -- to a decoy:  TVX{tNt_g035_B00m_C0ngr4t5}
  2. The curve order is smooth.  Counting points (Schoof / PARI ellcard)
     gives #E = ord(G) = 4724861355973759917094976238449899
              = 11 * 367 * 13399 * 58453 * 484079 * 40128631 * 76927309
     Every prime factor is < 2^27, so Pohlig-Hellman reduces the ECDLP
     Q = d*G to tiny discrete logs (largest BSGS is sqrt(76927309) ~ 8772
     steps), CRT reassembles d, and ender_chest opens.

This solver is standard-library only: the AES-256 decryption below is a
small pure-Python implementation, and the curve order N is verified
in-code (N*G = O, and (N/q)*G != O for every prime q | N, so ord(G) = N
exactly, not merely a multiple/divisor claim).

Run:  python3 solve_01_cryptoone.py [path/to/output.txt]
"""
import ast
import hashlib
import math
import os
import sys
from math import gcd

# --------------------------------------------------------------------------
# Pure-Python AES-256 decryption (FIPS-197)
# --------------------------------------------------------------------------

def _gf_mul(x, y):
    r = 0
    while y:
        if y & 1:
            r ^= x
        x = ((x << 1) ^ 0x11B) & 0xFF if x & 0x80 else (x << 1) & 0xFF
        y >>= 1
    return r

def _gf_pow(x, e):
    r = 1
    while e:
        if e & 1:
            r = _gf_mul(r, x)
        x = _gf_mul(x, x)
        e >>= 1
    return r

def _build_sboxes():
    sbox = []
    for i in range(256):
        inv = 0 if i == 0 else _gf_pow(i, 254)          # multiplicative inverse
        s = inv
        for rot in (1, 2, 3, 4):
            s ^= ((inv << rot) | (inv >> (8 - rot))) & 0xFF
        sbox.append((s ^ 0x63) & 0xFF)
    inv_sbox = [0] * 256
    for i, s in enumerate(sbox):
        inv_sbox[s] = i
    return sbox, inv_sbox

_SBOX, _INV_SBOX = _build_sboxes()
_RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40]

def _key_expansion(key):
    """AES-256: Nk=8, Nr=14 -> 60 words of 4 bytes."""
    w = [list(key[4 * i:4 * i + 4]) for i in range(8)]
    for i in range(8, 60):
        temp = list(w[i - 1])
        if i % 8 == 0:
            temp = [_SBOX[temp[1]] ^ _RCON[i // 8 - 1],
                    _SBOX[temp[2]], _SBOX[temp[3]], _SBOX[temp[0]]]
        elif i % 8 == 4:
            temp = [_SBOX[b] for b in temp]
        w.append([w[i - 8][j] ^ temp[j] for j in range(4)])
    return w

def _aes_decrypt_block(block, w):
    # state[r][c] = block[4*c + r]
    s = [[block[4 * c + r] for c in range(4)] for r in range(4)]

    def add_round_key(rnd):
        for c in range(4):
            for r in range(4):
                s[r][c] ^= w[4 * rnd + c][r]

    def inv_shift_rows():
        for r in range(1, 4):
            s[r] = s[r][-r:] + s[r][:-r]

    def inv_sub_bytes():
        for r in range(4):
            for c in range(4):
                s[r][c] = _INV_SBOX[s[r][c]]

    def inv_mix_columns():
        for c in range(4):
            col = [s[r][c] for r in range(4)]
            s[0][c] = _gf_mul(col[0], 14) ^ _gf_mul(col[1], 11) ^ _gf_mul(col[2], 13) ^ _gf_mul(col[3], 9)
            s[1][c] = _gf_mul(col[0], 9) ^ _gf_mul(col[1], 14) ^ _gf_mul(col[2], 11) ^ _gf_mul(col[3], 13)
            s[2][c] = _gf_mul(col[0], 13) ^ _gf_mul(col[1], 9) ^ _gf_mul(col[2], 14) ^ _gf_mul(col[3], 11)
            s[3][c] = _gf_mul(col[0], 11) ^ _gf_mul(col[1], 13) ^ _gf_mul(col[2], 9) ^ _gf_mul(col[3], 14)

    add_round_key(14)
    for rnd in range(13, 0, -1):
        inv_shift_rows()
        inv_sub_bytes()
        add_round_key(rnd)
        inv_mix_columns()
    inv_shift_rows()
    inv_sub_bytes()
    add_round_key(0)
    return bytes(s[r][c] for c in range(4) for r in range(4))

def aes_cbc_decrypt(key, data):
    """data = iv || ciphertext, PKCS#7 padded."""
    w = _key_expansion(key)
    iv, ct = data[:16], data[16:]
    out, prev = [], iv
    for i in range(0, len(ct), 16):
        blk = ct[i:i + 16]
        dec = _aes_decrypt_block(blk, w)
        out.append(bytes(x ^ y for x, y in zip(dec, prev)))
        prev = blk
    pt = b"".join(out)
    return pt[:-pt[-1]]

def chest_open(hex_ct, key_src):
    key = hashlib.sha256(key_src).digest()
    return aes_cbc_decrypt(key, bytes.fromhex(hex_ct)).decode()

# --------------------------------------------------------------------------
# Elliptic curve arithmetic (short Weierstrass, prime field)
# --------------------------------------------------------------------------

class Curve:
    def __init__(self, p, a):
        self.p, self.a = p, a

    def add(self, P, R):
        p, a = self.p, self.a
        if P is None:
            return R
        if R is None:
            return P
        (x1, y1), (x2, y2) = P, R
        if x1 == x2 and (y1 + y2) % p == 0:
            return None
        if P == R:
            lam = (3 * x1 * x1 + a) * pow(2 * y1, -1, p) % p
        else:
            lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
        x3 = (lam * lam - x1 - x2) % p
        return x3, (lam * (x1 - x3) - y1) % p

    def mul(self, k, P):
        R = None
        while k:
            if k & 1:
                R = self.add(R, P)
            P = self.add(P, P)
            k >>= 1
        return R

    def neg(self, P):
        return None if P is None else (P[0], (-P[1]) % self.p)

# --------------------------------------------------------------------------
# Factoring (deterministic Miller-Rabin + Pollard rho -- plenty here,
# because every factor of N turns out to be < 2^27)
# --------------------------------------------------------------------------

def is_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a_ in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):  # deterministic < 2^64, ample here
        if a_ % n == 0:
            continue
        x = pow(a_, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def pollard_rho(n):
    if n % 2 == 0:
        return 2
    import random
    random.seed(n)
    while True:
        x = random.randrange(n)
        c = random.randrange(1, n)
        y, d = x, 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d

def factor(n, out=None):
    out = {} if out is None else out
    if n == 1:
        return out
    if is_prime(n):
        out[n] = out.get(n, 0) + 1
        return out
    d = pollard_rho(n)
    factor(d, out)
    factor(n // d, out)
    return out

# --------------------------------------------------------------------------
# Pohlig-Hellman
# --------------------------------------------------------------------------

def bsgs(curve, g, h, order):
    m = math.isqrt(order) + 1
    table, cur = {}, None
    for j in range(m):
        table.setdefault(cur, j)
        cur = curve.add(cur, g)
    inv_gm = curve.neg(curve.mul(m, g))
    cur = h
    for i in range(m + 1):
        if cur in table:
            x = i * m + table[cur]
            if x < order and curve.mul(x, g) == h:
                return x
        cur = curve.add(cur, inv_gm)
    raise ValueError("BSGS failed")

def pohlig_hellman(curve, G, Q, N, prime_factors):
    residues = []
    for q in prime_factors:
        Ni = N // q
        Gi, Qi = curve.mul(Ni, G), curve.mul(Ni, Q)
        assert curve.mul(q, Gi) is None          # Gi really has order q
        residues.append((bsgs(curve, Gi, Qi, q), q))
    # CRT (moduli are coprime primes)
    x, M = 0, 1
    for r, mod in residues:
        x += M * (((r - x) * pow(M, -1, mod)) % mod)
        M *= mod
        x %= M
    return x

# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

# Curve order, from point counting (Schoof's algorithm, PARI/GP ellcard).
# Verified below, so the solver does not have to trust it.
CURVE_ORDER = 4724861355973759917094976238449899

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "challenges", "output.txt")
    env = {}
    for line in open(path):
        line = line.strip()
        if line and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = ast.literal_eval(v.strip())
    p, a, G, Q = env["p"], env["a"], tuple(env["G"]), tuple(env["Q"])
    curve = Curve(p, a)
    for P in (G, Q):                              # both points are on the curve
        assert (P[1] * P[1] - (P[0] ** 3 + a * P[0] + env["b"])) % p == 0

    # --- trap first: the shulker box opens with the public Q[0] -----------
    decoy = chest_open(env["shulker_box"], str(Q[0]).encode())
    print(f"[*] shulker_box (key = Q[0], public) -> {decoy}   <-- decoy, not the flag")

    # --- verify the claimed order of G ------------------------------------
    N = CURVE_ORDER
    assert curve.mul(N, G) is None, "N*G != O"
    factors = factor(N)
    print(f"[*] #E = ord(G) = {N}")
    print(f"[*] factorisation = {factors}  (all prime factors < 2^27: smooth)")
    for q in factors:
        assert factors[q] == 1 and is_prime(q)
        assert curve.mul(N // q, G) is not None, "ord(G) would be a proper divisor"
    print("[*] verified: N*G = O and (N/q)*G != O for every q | N, so ord(G) = N")

    # --- Pohlig-Hellman ECDLP ---------------------------------------------
    d = pohlig_hellman(curve, G, Q, N, sorted(factors))
    assert curve.mul(d, G) == Q
    print(f"[*] recovered d = {d}")
    print(f"[*] check: d*G == Q -> True")

    # --- open the ender chest ---------------------------------------------
    flag = chest_open(env["ender_chest"], str(d).encode())
    print(f"Flag: {flag}")
    return flag

if __name__ == "__main__":
    main()
