# Ending — .NET VM, the Flag Is Computed, Not Stored

**Author:** Abhishek Kr Gupta
**Event:** TVX CTF, 2026-11-13
**Status:** Solved — from the contributed writeup in
`contributed/tvx_all_writeups/ending_writeup/` (uploaded by Shikhu).
Solver re-run here and verified: flag reproduced. The binary was also
verified against the real checker under Mono (accepted; the
"corrected English" variant rejected).

## Flag

```
TVX{S0me_1nt2r2st1ng_t2xt_h2r2}
```

## Challenge

"What has beginnings has endings, and what has code, has flags" — a
single Windows executable, `Ending.exe` (10,752 bytes, SHA-256
`16686a047bb948a327139cb1d80fc2a62b8e1f85b551645a4b34073d4fa7f3e2`),
"find the flag". No flag format was stated; the binary itself defines
the expected string.

## Method

The tagline is the map: the program has a *beginning* layer you can see
(a Base64 string), an *ending* you have to compute (a virtual machine's
output), and the flag exists only as the VM's behaviour — it is never
stored anywhere in the file.

### Layer 1 — the package

PE32 console executable, a Mono/.NET assembly. One class, `Program`,
four methods — `Ror`, `Unpack`, `ReadWord`, `Run`, `Main` — and one
literal field, `package`: a 1,308-character Base64 string. `Unpack()`:

1. `Convert.FromBase64String(package)` → bytes starting `1F 8B` (gzip).
2. `GZipStream` decompress → 958 bytes of high-entropy data.
3. A hand-rolled transform on every byte `i`:
   `b[i] = ROR8(b[i], (i % 5) + 1) XOR ((199 + 91*i) & 0xFF)`

That output is not text — it is bytecode.

### Layer 2 — the virtual machine

`Run()` interprets the bytecode with 4 registers (`UInt16` each), 128
memory cells (`UInt16` each), a 31-byte output buffer (the flag is 31
characters), and opcode `0xFF` halting (the "ending"):

| Opcode | Meaning |
|---|---|
| 0x10 / 0x11 / 0x12 | `R[a] = imm16` / `R[a] ^= imm16` / `R[a] += imm16` |
| 0x13 | `R[a] = ROL16(R[a], b)` |
| 0x14 / 0x15 | `R[a] = M[b]` / `M[a] = R[b]` |
| 0x16 / 0x17 / 0x18 | `R[a] ^= R[b]` / `R[a] += R[b]` / `R[a] -= R[b]` |
| 0x19 | `R[a] = ~R[a]` |
| 0x1A | `R[a] = M[R[b]]` |
| 0x30 | jump if `R[a] != 0`, signed-byte offset |
| 0x31 | unconditional jump, signed-byte offset |
| 0x40 | output low byte of `R[a]` |
| 0xFF | halt |

The one trap in the VM semantics is the jump base. For `0x30` the IL
adds the offset to `ip` *after* the offset byte has been fetched; for
`0x31` it adds it to the offset byte's own position. Getting that single
byte wrong derails execution into a bad opcode (`0xBE` at `0x379`) within
a few hundred steps — a useful smoke signal that the semantics, not the
data, are off.

Re-implementing `Unpack()` plus the VM in Python and executing the
958-byte program produces 31 output bytes:
`TVX{S0me_1nt2r2st1ng_t2xt_h2r2}`.

Leet-decoded it reads "some interesting text here" (0=o, 1=i, 2=e) —
but the digits are load-bearing, not a typo.

### Verification against the real binary

`Main()` prompts `flag> ` and string-compares the input with the VM
output. Running the genuine binary under Mono:

- `TVX{S0me_1nt2r2st1ng_t2xt_h2r2}` → **accepted**
- the "corrected English" variant `TVX{S0me_1nterest1ng_text_here}` →
  rejected
- a random string → rejected

## Solver

The contributed solver lives in its own folder and must be run from
there (it reads `challenges/Ending.exe` by relative path):

```bash
cd contributed/tvx_all_writeups/ending_writeup
python3 solvers/solve_all.py
```

Parses the PE's #US heap to extract the `package` literal (no .NET
tooling needed), applies the Base64 → GZip → ROR/XOR unpacking,
emulates the VM exactly, and prints the flag. Re-run in this session:
`1/1`.

## Flag

```
TVX{S0me_1nt2r2st1ng_t2xt_h2r2}
```

Full writeup + PDF: `contributed/tvx_all_writeups/ending_writeup/`.
