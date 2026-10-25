# CREST IR-17 Writeup

## Result

```text
CREST{FORENSIC_NONCE_ALIGNMENT_V3}
```

The ECDSA private scalar was recovered from quantized nonces using a
known-LSB Hidden Number Problem / lattice CVP attack.  The active quantum was
`2^18`, not the stale `LEGACY_QUANTUM = 2^24`.  The recovered scalar matches the
supplied secp256k1 public key and all 16 signatures.  AES-256-GCM
authentication of `sealed_flag.bin` succeeds.

## Artifacts

| File | Size | SHA-256 |
|------|-----:|---------|
| `signatures.json` | 6,189 | `e19ddbf3ab22192618b8b0f70ddf3a07196bc00c08d8524f7d169e98e3977599` |
| `pubkey.pem` | 7,034 | `c672fcca138c67bc68772cd94843202c932e6c86654fe4a9d5e2b16ff343f141` |
| `sign_service.py` | 547 | `023604353a4f4e67746567cf36ef00c5369d641430f2f5446846b3ba47ca7521` |
| `evidence/incident_17.log` | 73,601,363 | `2460f25146bcebffee0f2f34d1b432551420041496177abb54f6cb7fdcb034c4` |
| `evidence/calibration.note` | 456 | `e9a889b5be98c3a3d9fe329f0e1dbcc9bd363936579d179576271b599fa533e7` |
| `sealed_flag.bin` | 67 | `3de20a30701bf8a3c02d2f098592a8475ef222cba53e0462c291f9e61e14e934` |

`pubkey.pem` and `signatures.json` contain many decoy comments and decoy
`CREST{...}` markers.  Only the single real PEM block and the 16 objects in the
`signatures` array were used.

## The nonce weakness

The recovered signing fragment describes secp256k1 ECDSA and a
`quantized_counter` nonce source:

```python
CURVE_NAME = "secp256k1"
NONCE_SOURCE = "quantized_counter"
LEGACY_QUANTUM = 0x01000000  # 2^24, stale branch

def make_nonce(counter, quantum):
    return (counter // quantum) * quantum
```

Therefore every nonce is a multiple of a power-of-two quantum `q = 2^e`.

The clues conflict:

- `sign_service.py` contains `2^24`, but the value is explicitly from a stale
  branch and its production call site was lost.
- `calibration.note` says the archived profile covered exponents 18 through 31,
  and that the margin value `24` is ambiguous (exponent, byte count, or stale
  revision).  It requires inference from the signatures.
- `incident_17.log` is 800,014 lines, of which 800,000 are identical cache-audit
  cover traffic.  The 14 anomalies are seven rejected decoy tokens plus:

```text
IR-17: signing service recovered from retired audit node
cfg-cache: active profile unavailable; stale profile found
counter-normalizer: quantized mode enabled
operator note: do not trust LEGACY_QUANTUM without signature-level validation
signing records exported; per-request nonce values absent
evidence capsule sealed; export completed
```

So `2^24` is a hypothesis only.  All exponents in `18..31` must be tested, and
the winner must satisfy the public key and every signature.

## Signature validation

For each signature `(r, s)` with message hash `z`:

```text
w  = s^-1 mod n
u1 = z*w mod n
u2 = r*w mod n
R  = u1*G + u2*Q
valid iff R.x mod n == r
```

Results:

- All 16 stored hashes match SHA-256 of the corresponding `audit-entry-NNNN`
  message.
- All 16 signatures are valid against the PEM public key.
- All 16 `r` values are distinct; there is no exact nonce reuse.

## Hidden Number Problem

Write `q = 2^e` and `k_i = q a_i`, with `0 <= a_i < n/q`.  ECDSA gives:

```text
s_i k_i = z_i + r_i d  (mod n)
```

Multiplying by `(s_i q)^-1 mod n`:

```text
a_i = A_i d + C_i  (mod n)
A_i = r_i * (s_i q)^-1 mod n
C_i = z_i * (s_i q)^-1 mod n
```

Thus `A_i d + C_i - n t_i = a_i`, where `a_i` is small.  Build the lattice

```text
L = n Z^16 + Z A,   A = (A_1, ..., A_16)
```

and use CVP with target `(-C_1, ..., -C_16)`.  For the correct `d`, the lattice
vector `v` satisfies:

```text
v_i + C_i = a_i,   0 <= a_i < n/q.
```

A square basis is formed using a pivot coordinate `j` with
`gcd(A_j, n) = 1`:

```text
rows i != j : n * e_i
row j       : (A_1/A_j, ..., 1, ..., A_16/A_j) mod n
```

After LLL reduction, `fpylll.CVP.closest_vector` finds `v`.  The scalar is
recovered as `d = v_j * A_j^-1 mod n` and then verified independently.

For `e = 18`, the residual bound is about `n/2^18` (238 bits), and 16
signatures provide 16 x 18 = 288 known zero bits, more than the 256-bit scalar.
The LLL/CVP step succeeds in milliseconds.

## Exponent resolution

Every exponent in `18..31` was tested with the same lattice pipeline.  Only
**18** produced a candidate satisfying both `Q = dG` and all signatures.
Exponent 24, the stale constant, fails.

Independent confirmation from the recovered nonces:

```text
k_i = (z_i + r_i d) * s_i^-1 mod n
```

2-adic valuations:

```text
[20, 21, 18, 19, 18, 19, 19, 18, 18, 19, 19, 19, 18, 19, 26, 18]
```

All nonces are divisible by `2^18`, and six have exact valuation 18, so they are
not all divisible by `2^19`.  This uniquely confirms quantum `2^18`.

## Recovered scalar

```text
d = 0xf757acbadcb14f5fcf9ce5d80b54a633888ad75735dc594444517769e630d6a0
```

Verification:

- `1 <= d < n`: yes.
- `dG == Q` from `pubkey.pem`: yes.
- All 16 ECDSA signatures valid with this scalar: yes.
- All derived nonces multiples of `2^18`: yes.
- At least one nonce not a multiple of `2^19`: yes.

## AES-256-GCM decryption

Key derivation:

```python
scalar_bytes = d.to_bytes(32, "big")
aes_key = hashlib.sha256(scalar_bytes).digest()
```

```text
AES-256 key = d28fd4cbf28541036d9651c13cc9b35dfd85dd5abbc801147d237f481aaffd98
```

`sealed_flag.bin` layout:

```text
5-byte magic + 12-byte nonce + 34-byte ciphertext + 16-byte tag = 67 bytes
```

Important discrepancy: the actual magic is `WBSG1` (`57 42 53 47 31`), while
the task text says `UBS61`.  The actual file bytes were used.  With AAD exactly
`b"CRY-03"`, `decrypt_and_verify` returns **PASS**:

```text
nonce      = 1734dc2a5e93e5f20f7ab02d
plaintext  = CREST{FORENSIC_NONCE_ALIGNMENT_V3}
```

Authentication success proves the scalar, KDF, nonce, ciphertext/tag split, and
AAD are all correct.

## Reproduction

Recovery, from WSL Ubuntu with `fpylll`:

```bash
wsl -d Ubuntu -- python3 /mnt/d/shivam/player/output/solve_ecdsa.py
```

Decryption, from Windows Python with PyCryptodome:

```powershell
python D:\shivam\player\output\decrypt_evidence.py
```

The decryption script reads the recovered scalar from
`verification_results.json`, re-validates it against the PEM public key and all
signatures, derives the key, and authenticates the capsule.

## Deliverables

- `output/forensics_report.md` - full analysis.
- `output/solve_ecdsa.py` - signature parsing, verification, HNP/CVP recovery.
- `output/decrypt_evidence.py` - KDF and authenticated AES-GCM decryption.
- `output/verification_results.json` - per-signature checks, public-key
  comparison, exponent diagnostics, nonce valuations, AES-GCM status, flag.

## Final flag

```text
CREST{FORENSIC_NONCE_ALIGNMENT_V3}
```
