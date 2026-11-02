# MemGhost — Memory Dump Triage

- **Competition:** SecLeaf Q2 2026
- **Date investigated:** 23 May 2026
- **Category:** Forensics / memory-dump analysis
- **Artifact:** `memory.bin` (28,695 bytes)
- **Status:** Candidate flag recovered; acceptance not verified

## Challenge prompt

The remembered prompt began:

> “A beautiful mess of memory…”

The flag format was `SecLeaf{...}`.

## 1. Initial triage

Start by identifying the file and its structure:

```bash
file memory.bin
stat memory.bin
sha256sum memory.bin
xxd -l 256 memory.bin
strings -a -n 4 memory.bin | less
```

The artifact begins with the marker:

```text
MEMDUMP_V1.0
```

The dump contains fragments resembling shell history, SQL, authentication headers, `/etc/passwd`, SSH key markers, stack-like records, and many planted flag strings.

## 2. Flag-string enumeration

The first pass used:

```bash
strings -a memory.bin | grep -oE 'SecLeaf\{[^}]+\}'
strings -a -td memory.bin | grep 'SecLeaf{'
```

The following strings were found as decoys:

```text
SecLeaf{y0u_f0und_m3_haha_n0pe}
SecLeaf{alm0st_th3r3_just_k1dd1ng}
SecLeaf{wr0ng_flag_ag41n}
SecLeaf{r3ally_th1s_t1me_nope}
SecLeaf{n1c3_try_th1s_1snt_1t}
```

The strongest candidate recovered in the dump was:

```text
SecLeaf{1m_R3@ll_Fla9}
```

The dump also contains the text:

```text
NOTE: The flag you need is hidden in plain sight.
END_OF_DUMP
```

That note is a clue to inspect the entire memory layout and not accept the first printable flag-shaped string.

## 3. Additional inspection

The previous investigation used:

```bash
strings -td memory.bin
grep -aob 'SecLeaf{' memory.bin
xxd -g 1 memory.bin | less
binwalk memory.bin
hexdump -C memory.bin | less
```

Other interesting embedded strings included:

```text
SELECT * FROM users
DROP TABLE IF EXISTS
Authorization: Bearer
/etc/passwd
/bin/bash
BEGIN RSA PRIVATE KEY
HTTP/1.1 200 OK
```

These suggest that the dump is a synthetic mixture of process memory, request fragments, stack data, and planted clues. Their presence alone does not prove a particular exploit or process history.

## 4. Reproduction solver

From this directory:

```bash
python3 ../solvers/memghost_triage.py ../artifacts/memory.bin
```

The script reports candidate strings and file offsets. It intentionally does not label a candidate as accepted.

## 5. Result and verification

Candidate:

```text
SecLeaf{1m_R3@ll_Fla9}
```

**Verification status:** No accepted submission response or explicit rejection was preserved. Record this as a candidate, not a solved challenge.

## 6. Lessons

- Use offset-aware extraction (`strings -td`) rather than plain `strings`.
- Expect planted decoys in CTF memory dumps.
- Correlate flag-like strings with surrounding structures and the challenge's “hidden in plain sight” clue.
- A flag-shaped string is not a verified flag until the challenge platform accepts it.
