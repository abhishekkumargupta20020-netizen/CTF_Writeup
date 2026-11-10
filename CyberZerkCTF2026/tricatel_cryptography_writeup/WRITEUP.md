# Tricatel — CTF Writeup

**Category: Cryptography**
**Event / Series: CyberZerk — Tricatel**
**Author: Siddart (solved with Pip)**
**Date: 10 November 2026**

These five challenges are about telling encoding apart from encryption — and about strong-looking cryptography collapsing when it is used carelessly. A CFO's "encrypted" memo, an analyst's note of hope overwritten by the voice in their head, a "triple-layer military-grade" password that is no encryption at all, the same CFO's safe protected by a repeating XOR key, and finally a real RSA key — 1023 bits, standard exponent — undone because its two primes were generated far too close together. In the first four, the flag format `CyberZerk{...}` is the known plaintext that cracks the cipher open; in the fifth, the mathematics does it.

| # | Challenge | File | Technique | Flag |
|---|-----------|------|-----------|------|
| 1 | The CFO's Encrypted Memo | `note_chiffree.txt` | Base64, then Vigenère (known-plaintext attack) | `CyberZerk{Pr1m3s_CODIR_P3nd4nt_L3s_R3fus_D3_C0ng3s}` |
| 2 | Analyst's Logbook — Day 43 | `analyst_logbook.txt` | Vigenère, key = the refrain "Je suis nul" | `CyberZerk{Tu_As_Ta_Place_Ici}` |
| 3 | The "Triple-Layer" Password | `triple_base64.txt` | Base64 applied 3 times (encoding, not encryption) | `CyberZerk{B4s364_N3st_P4s_Du_Ch1ffr3m3nt}` |
| 4 | The CFO's Safe | `coffre_chiffre.hex` | Repeating-key XOR, key `TRICATEL` recovered by known plaintext | `CyberZerk{X0R_R3p3t3_C_3st_P4s_S3cur1s3}` |
| 5 | The CFO's RSA Key | `cle_publique_et_message.txt` | RSA, Fermat factorisation of close primes | `CyberZerk{F3rm4t_C4ss3_L3s_Pr3m13rs_Tr0p_Pr0ch3s}` |

**Package contents**

```
tricatel_cryptography_writeup/
├── WRITEUP.md                  <- this file (also exported as PDF)
├── challenges/
│   ├── note_chiffree.txt       <- Challenge 1 (original file)
│   ├── analyst_logbook.txt     <- Challenge 2 (prompt as given; no file was supplied)
│   ├── triple_base64.txt       <- Challenge 3 (prompt as given; no file was supplied)
│   ├── coffre_chiffre.hex      <- Challenge 4 (original file)
│   └── cle_publique_et_message.txt <- Challenge 5 (original file)
└── solvers/
    ├── solve_01_cfo_vigenere.py
    ├── solve_02_logbook_vigenere.py
    ├── solve_03_triple_base64.py
    ├── solve_04_xor_safe.py
    ├── solve_05_rsa_fermat.py
    └── solve_all.py            <- runs all 5, verified: 5/5 flags
```

Run everything:

```bash
python3 solvers/solve_all.py
# or individually, e.g.
python3 solvers/solve_01_cfo_vigenere.py challenges/note_chiffree.txt
```

All solvers are Python standard-library only — no pip installs needed.

---

## Challenge 1 — The CFO's Encrypted Memo

**Category:** Cryptography / Vigenère
**File:** `challenges/note_chiffree.txt`
**Prompt:** *The CFO encrypts his expense reports "so nobody sticks their nose into them." A burned-out intern leaked this memo before resigning. It supposedly proves that the executive committee's (CODIR) bonuses skyrocketed while leave requests were being denied.*

### Intuition

One layer is visible at a glance — the file is a single Base64-looking line — but decoding it once does not give a flag, it gives flag-shaped gibberish. That shape is the clue: `{ }`, `_` and digits are untouched, only letters are scrambled, and the first letters line up with `CyberZerk`. A letter-only cipher with no single Caesar shift and a repeating pattern is a Vigenère, and the known flag format hands you the key.

### Analysis

The file is a single line:

```
SG1tZXREamZ2e1B0MXEzeF9RWkRLVl9VM2JvNG52X1AzeF9GM3F1dV9IM19IMGJyM3N9
```

**Layer 1 — Base64:**

```python
import base64
base64.b64decode("SG1tZXREamZ2e1B0MXEzeF9RWkRLVl9VM2JvNG52X1AzeF9GM3F1dV9IM19IMGJyM3N9")
# b'HmmetDjfv{Pt1q3x_QZDKV_U3bo4nv_P3x_F3quu_H3_H0br3s}'
```

Still flag-shaped — `HmmetDjfv{...}` has the same length and punctuation as `CyberZerk{...}` — but no single Caesar shift turns `HmmetDjfv` into `CyberZerk`, and the repetition pattern rules out a simple substitution. This is a polyalphabetic cipher: Vigenère.

**Layer 2 — Vigenère, known-plaintext attack:**

Use the known format `CyberZerk` to recover the keystream (cipher − plain, letter by letter):

```
C->H +5   y->m +14   b->m +11   e->e 0   r->t +2   Z->D +4
e->j +5   r->f +14   k->v +11
```

The keystream repeats with **period 6: `[5, 14, 11, 0, 2, 4]`**. Applying it — letters only, digits / `_` / `{ }` pass through and the key does not advance on them — to the whole string gives perfectly readable leetspeak French, which confirms the key:

```python
import base64
ct = base64.b64decode("SG1tZXREamZ2e1B0MXEzeF9RWkRLVl9VM2JvNG52X1AzeF9GM3F1dV9IM19IMGJyM3N9").decode()
key = [5, 14, 11, 0, 2, 4]
out, i = [], 0
for ch in ct:
    if ch.isalpha():
        base = 65 if ch.isupper() else 97
        out.append(chr((ord(ch) - base - key[i % 6]) % 26 + base)); i += 1
    else:
        out.append(ch)
print(''.join(out))
# CyberZerk{Pr1m3s_CODIR_P3nd4nt_L3s_R3fus_D3_C0ng3s}
```

### Solver

`solve_01_cfo_vigenere.py` — Base64-decodes the file, derives the keystream from the known plaintext `CyberZerk`, asserts it repeats with period 6 as `[5, 14, 11, 0, 2, 4]`, then Vigenère-decrypts the full string.

### Flag

```
CyberZerk{Pr1m3s_CODIR_P3nd4nt_L3s_R3fus_D3_C0ng3s}
```

Leetspeak: *Primes CODIR Pendant Les Refus De Congés* — "CODIR bonuses while leave requests were being refused", exactly what the intern claimed the memo proved.

### Lesson

Vigenère was unbreakable for 300 years — until the attacker knows (or guesses) a few letters of plaintext. A flag format, a greeting, or a file header is often all the known plaintext a cryptanalyst needs.

---

## Challenge 2 — Analyst's Logbook, Day 43

**Category:** Cryptography / Vigenère
**File:** `challenges/analyst_logbook.txt` (prompt as given; no file was supplied)
**Prompt:** *Analyst's Logbook — Day 43: "I can't push forward anymore. Every time I try to write this report, that voice in my head comes back. It blurs my thoughts, it encrypts my certainties. It repeats the same thing to me over and over in a loop, like an inevitability: I am worthless." I tried to write a note to reassure myself, to remind myself who I am. But the voice took over. My own message of hope was encrypted by its refrain, using a centuries-old substitution method attributed to a 16th-century French diplomat. Here is the note I found on my desk this morning: `LctyzRrlv{Cy_Sm_Bs_Cflli_Awq}`*

### Intuition

Every word of the story is a hint, and none of it is decoration. "Centuries-old substitution method attributed to a 16th-century French diplomat" is the Vigenère cipher (Blaise de Vigenère). "It repeats the same thing to me over and over in a loop" is a repeating Vigenère key. And the refrain itself — "I am worthless" — is the key, in French.

### Analysis

The refrain: *"I am worthless"* — in French: **« Je suis nul »**. Spaces removed, the key is:

```
JESUISNUL
```

You can confirm it without guessing, by the same known-plaintext attack as Challenge 1, on the flag format:

```
L-C = J   c-y = E   t-b = S   y-e = U   z-r = I
R-Z = S   r-e = N   l-r = U   v-k = L
        ->  J E S U I S N U L
```

Decrypt — letters only, key repeating, `_ { }` pass through:

```python
ct  = "LctyzRrlv{Cy_Sm_Bs_Cflli_Awq}"
key = "JESUISNUL"
out, i = [], 0
for ch in ct:
    if ch.isalpha():
        k = ord(key[i % len(key)]) - 65; i += 1
        base = 65 if ch.isupper() else 97
        out.append(chr((ord(ch) - base - k) % 26 + base))
    else:
        out.append(ch)
print(''.join(out))
# CyberZerk{Tu_As_Ta_Place_Ici}
```

### Solver

`solve_02_logbook_vigenere.py` — finds the `Word{...}` token in `analyst_logbook.txt` (or takes it as an argument), verifies the key `JESUISNUL` against the known plaintext `CyberZerk`, then Vigenère-decrypts it.

### Flag

```
CyberZerk{Tu_As_Ta_Place_Ici}
```

Plain reading: *Tu As Ta Place Ici* — "You do have a place here." The reassuring note the analyst meant to write, once the voice's encryption is removed.

### Lesson

In classical ciphers the key is often the weakest link — and here it is literally the attacker's own refrain. A key drawn from the story, a name, or a slogan is a key an analyst can guess; and a repeating key, however long, still leaks its period through known plaintext.

---

## Challenge 3 — The "Triple-Layer Military-Grade" Password

**Category:** Cryptography / Encoding vs. Encryption
**File:** `challenges/triple_base64.txt` (prompt as given; no file was supplied)
**Prompt:** *Tricatel's IT department reset your access following your sick leave. They claim to have used a "triple-layer military-grade encryption algorithm" to secure your temporary password. At a glance, it mostly looks like a standard encoding repeated for show... Here is your token: `VVROc2FWcFlTbUZhV0VweVpUQkpNR042VFRKT1JqbFBUVE5PTUZneFFUQmpNVGxGWkZZNVJHRkVSbTFhYmtsNllsUk9kV1JJTUQwPQ==`*

### Intuition

Trust the prompt's own doubt: "it mostly looks like a standard encoding repeated for show." Base64 has no key, no secret, and no security — repeating it three times is still just Base64. Peel the layers one at a time and watch for the flag format to appear.

### Analysis

Peel it layer by layer:

```python
import base64
s = "VVROc2FWcFlTbUZhV0VweVpUQkpNR042VFRKT1JqbFBUVE5PTUZneFFUQmpNVGxGWkZZNVJHRkVSbTFhYmtsNllsUk9kV1JJTUQwPQ=="

for i in range(3):
    s = base64.b64decode(s).decode()
    print(i+1, s)
```

```
1  UTNsaVpYSmFaWEpyZTBJMGN6TTJORjlPTTNOMFgxQTBjMTlFZFY5RGFERm1abkl6YlROdWRIMD0=
2  Q3liZXJaZXJre0I0czM2NF9OM3N0X1A0c19EdV9DaDFmZnIzbTNudH0=
3  CyberZerk{B4s364_N3st_P4s_Du_Ch1ffr3m3nt}
```

Layer 2 is recognisable on sight — `Q3liZXJaZXJr` is Base64 for `CyberZerk`, the same prefix seen across the whole Tricatel series. One more decode and the flag falls out.

### Solver

`solve_03_triple_base64.py` — finds the long Base64 token in `triple_base64.txt` (or takes it as an argument), decodes it three times, printing each layer, and returns the result starting with `CyberZerk{`.

Manual equivalent:

```bash
echo 'VVROc2FWcFlTbUZhV0VweVpUQkpNR042VFRKT1JqbFBUVE5PTUZneFFUQmpNVGxGWkZZNVJHRkVSbTFhYmtsNllsUk9kV1JJTUQwPQ==' | base64 -d | base64 -d | base64 -d
```

### Flag

```
CyberZerk{B4s364_N3st_P4s_Du_Ch1ffr3m3nt}
```

Leetspeak: *Base64 N'est Pas Du Chiffrement* — "Base64 is not encryption." Anyone can decode it, no key needed, however many times you repeat it.

### Lesson

Encoding is not encryption. Base64 exists to move binary data through text channels, not to keep a secret — it has no key to steal and no key to protect. Calling it "military-grade" because it was applied three times is security theatre; a password stored this way is a password stored in plain sight.

---

## Challenge 4 — The CFO's Safe

**Category:** Cryptography / XOR
**File:** `challenges/coffre_chiffre.hex`
**Prompt:** *The CFO "encrypted" the contents of his safe with a little custom script. We recovered the result in hexadecimal. It seems he always reuses the same key, over and over again.*

### Intuition

Hexadecimal is just the container — the real cipher is the "same key, over and over again": a repeating-key XOR. Repeating XOR has a fatal property: `cipher ^ plain = key`. If you know any stretch of plaintext as long as the key, you recover the key itself — and this series hands you that stretch for free, because every plaintext starts with `CyberZerk{`.

### Analysis

The file is 80 hex characters = **40 bytes**:

```python
ct = bytes.fromhex("172b2b26330e203e3f291173130b177f24613d701e171a7f2726161375271a1f67313c3170277631")
# 40 bytes, not readable - XOR-encrypted
```

**Recover the key from known plaintext:**

```python
known = b"CyberZerk{"
key_stream = bytes(c ^ p for c, p in zip(ct, known))
# b'TRICATELTR'
```

`TRICATEL` followed by `TR` again is the repetition confirming itself: the key is **`TRICATEL`, period 8**, reused over and over, exactly as the prompt said.

**Decrypt the whole 40 bytes:**

```python
key = b"TRICATEL"
pt = bytes(b ^ key[i % len(key)] for i, b in enumerate(ct))
print(pt.decode())
# CyberZerk{X0R_R3p3t3_C_3st_P4s_S3cur1s3}
```

### Solver

`solve_04_xor_safe.py` — hex-decodes the file, XORs the ciphertext against the known plaintext `CyberZerk{` to recover the key stream, asserts it is `TRICATEL` repeating with period 8, then XOR-decrypts all 40 bytes with that key.

### Flag

```
CyberZerk{X0R_R3p3t3_C_3st_P4s_S3cur1s3}
```

Leetspeak: *XOR Répété C'Est Pas Sécurisé* — "Repeating XOR is not secure."

### Lesson

XOR is a perfectly good operation — inside real ciphers, with a key as long as the message and used once (a one-time pad), it is even unbreakable. An 8-byte key repeated over a 40-byte message, against a plaintext with a known header, is none of that: the key falls out of the first 10 bytes, and the company name was the worst key choice of all.

---

## Challenge 5 — The CFO's RSA Key

**Category:** Cryptography / RSA
**File:** `challenges/cle_publique_et_message.txt`
**Prompt:** *We intercepted the CFO's RSA public key and an encrypted message. The home-brewed key generator was cobbled together in a rush on a production night... the two prime factors look strangely similar.*

### Intuition

RSA's security is the belief that factoring `n` is infeasible. That belief assumes `p` and `q` are large, independent, random primes. "The two prime factors look strangely similar" breaks the assumption directly: if `p` and `q` are close together, Fermat factorisation finds them almost instantly, whatever the size of `n` — and here `n` is 1023 bits, a size that would be respectable if the primes had been chosen properly.

### Analysis

The interception gives the complete public material:

```
n = 80212772058200318331300079496309046404407863541893990823458017701424496169728020886315708954946247456549467636228289508051504043657362562710963459898059618322307640646997491893098662379623269687517308992271177299514157669726203684540391560112332919658354699766234227531947934780484232345671991558901521674857   (1023 bits, 308 digits)
e = 65537
c = 37349549515090945417450122795335580990902750723340185050711772061916623126113099880177602219381069951334085720404628406456724149937589057117852268813232105608362675774617868234377809159128266125490782550531069542420297187328167250214392422812890728320489416372899423467921565710232771608025776495955836994422
```

**Fermat factorisation.** For `n = p * q` with `p` close to `q`, write `n = a^2 - b^2 = (a - b)(a + b)`, where `a = (p + q) / 2` and `b = (q - p) / 2`. If `p` and `q` are close, `a` is barely above the square root of `n`, so trying `a = ceil(sqrt(n))`, then `a + 1`, `a + 2`, ... until `a^2 - n` is a perfect square finds them fast.

Here it succeeds on the **very first try** — `a = ceil(sqrt(n))` already works:

```python
import math
a = math.isqrt(n)
if a * a < n: a += 1
b = math.isqrt(a * a - n)   # b*b == a*a - n, perfect square immediately
p, q = a - b, a + b
```

```
p = 8956158331461113597193699151162992842511926079913161674307075322407112742407580991516755976831685819784496449586972839527644177119922983875200034813617119
q = 8956158331461113597193699151162992842511926079913161674307075322407112742407580991516755976831685819784496449586972839527644177119922983875200034814456503
q - p = 839384
p * q == n  (verified)
```

Two 154-digit primes differing by only 839,384 — identical in their first ~148 digits. The "generator cobbled together on a production night" evidently took a prime and nudged it to find the second one.

**Decrypt.** With `p` and `q` known, RSA is over: rebuild the private exponent and decrypt exactly as the owner would.

```python
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)          # e = 65537
m = pow(c, d, n)
print(m.to_bytes((m.bit_length() + 7) // 8, 'big').decode())
# CyberZerk{F3rm4t_C4ss3_L3s_Pr3m13rs_Tr0p_Pr0ch3s}
```

### Solver

`solve_05_rsa_fermat.py` — parses `n`, `e`, `c` from the file, Fermat-factors `n` (first iteration), asserts `p * q == n`, derives `d` from `phi = (p - 1)(q - 1)`, decrypts `c`, and converts the result from a big integer back to bytes.

### Flag

```
CyberZerk{F3rm4t_C4ss3_L3s_Pr3m13rs_Tr0p_Pr0ch3s}
```

Leetspeak: *Fermat Casse Les Premiers Trop Proches* — "Fermat breaks primes that are too close." (`Pr3m13rs` = *premiers*, primes / firsts.)

### Lesson

Key length is not security by itself. A 1023-bit modulus with two near-identical primes is weaker than a much smaller key with honestly random ones, because close primes hand Fermat's method — a 17th-century technique — a factorisation in one step. Generate each prime independently, at random, and far apart; and never home-brew a key generator on a production night.

---

## Summary — Cryptography Takeaways

| # | What looked like security | What it actually was |
|---|---------------------------|----------------------|
| 1 | A CFO's "encrypted" memo | Base64 wrapping a Vigenère — broken by known plaintext (`CyberZerk`) giving a period-6 keystream |
| 2 | A note of hope "encrypted by the voice" | Vigenère keyed by the refrain itself — `JESUISNUL` ("Je suis nul") |
| 3 | "Triple-layer military-grade encryption" | Base64, three times — encoding with no key at all |
| 4 | A CFO's safe "encrypted" with a custom script | Repeating-key XOR — key `TRICATEL` (period 8) recovered from the known plaintext `CyberZerk{` |
| 5 | A real 1023-bit RSA public key | Primes generated too close together — Fermat factorisation succeeds on the first iteration (`q - p = 839384`), then standard RSA decryption |

Every flag in this category is itself the lesson, in leetspeak French:

1. `Pr1m3s_CODIR_P3nd4nt_L3s_R3fus_D3_C0ng3s` — CODIR bonuses while leave requests were refused
2. `Tu_As_Ta_Place_Ici` — You do have a place here
3. `B4s364_N3st_P4s_Du_Ch1ffr3m3nt` — Base64 is not encryption
4. `X0R_R3p3t3_C_3st_P4s_S3cur1s3` — Repeating XOR is not secure
5. `F3rm4t_C4ss3_L3s_Pr3m13rs_Tr0p_Pr0ch3s` — Fermat breaks primes that are too close

**All 5 flags verified with `solvers/solve_all.py`: 5/5 extracted.**
