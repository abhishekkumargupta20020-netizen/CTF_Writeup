#!/usr/bin/env python3
"""SpookyTrust: sign the audit-server challenge with the recovered key.

Recovered private key for ST-ISS-03: d = 1963  (verified: 1963*G == Q_03).
Run on a machine that can reach the audit server:
    python3 sign_and_submit.py http://3.149.129.229:8000
Pure standard library, no pip packages needed.
"""
import base64
import hashlib
import json
import secrets
import sys
from urllib.request import Request, urlopen

# --- P-384 parameters (SECG) ---
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFF
a = p - 3
b = 0xB3312FA7E23EE7E4988E056BE3F82D19181D9C6EFE8141120314088F5013875AC656398D8A2ED19D2A85C8EDD3EC2AEF
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52973
Gx = 0xAA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A385502F25DBF55296C3A545E3872760AB7
Gy = 0x3617DE4A96262C6F5D9E98BF9292DC29F8F41DBD289A147CE9DA3113B5F0B8C00A60B1CE1D7E819D7A431D7C90EA0E5F
G = (Gx, Gy)


def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        lam = (3 * x1 * x1 + a) * pow(2 * y1, -1, p) % p
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)


def scalar_mult(k, P):
    R = None
    while k:
        if k & 1:
            R = point_add(R, P)
        P = point_add(P, P)
        k >>= 1
    return R


def sign(msg_bytes, d):
    z = int.from_bytes(hashlib.sha384(msg_bytes).digest(), "big") % n
    while True:
        k = secrets.randbelow(n - 1) + 1
        R = scalar_mult(k, G)
        r = R[0] % n
        if r == 0:
            continue
        s = (pow(k, -1, n) * (z + r * d)) % n
        if s == 0:
            continue
        if s > n // 2:  # low-s normalization
            s = n - s
        return r, s


def der_encode(r, s):
    def enc_int(x):
        b = x.to_bytes((x.bit_length() + 7) // 8, "big")
        if b[0] & 0x80:
            b = b"\x00" + b
        return b"\x02" + bytes([len(b)]) + b
    body = enc_int(r) + enc_int(s)
    return b"\x30" + bytes([len(body)]) + body


def main():
    server = sys.argv[1] if len(sys.argv) > 1 else "http://3.149.129.229:8000"
    server = server.rstrip("/")
    d = 1963

    with urlopen(Request(server + "/challenge"), timeout=10) as resp:
        chal = json.loads(resp.read().decode())
    print("challenge:", json.dumps(chal))

    session_id = chal.get("session_id") or chal.get("sessionId") or chal.get("id")
    message = chal.get("message") or chal.get("msg") or chal.get("challenge")
    if session_id is None or message is None:
        print("Unexpected challenge format; cannot proceed.")
        sys.exit(1)

    r, s = sign(message.encode("utf-8"), d)
    sig_b64 = base64.b64encode(der_encode(r, s)).decode()
    print("signature (Base64 DER):", sig_b64)

    body = json.dumps({"session_id": session_id, "signature": sig_b64}).encode()
    req = Request(server + "/verify", data=body, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=10) as resp:
        print("verify response:", resp.read().decode())


if __name__ == "__main__":
    main()
