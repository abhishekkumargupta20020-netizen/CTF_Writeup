# CTF7 Report

## Stage 1 — OLE2/VBA forensics

- Downloaded `quarterly_invoice.doc` from `http://2.31.70.16:16240/`.
- Artifact: 4096 bytes, OLE2 CFB magic `d0 cf 11 e0 a1 b1 1a e1`.
- SHA256: `6a915d0fee8a111393e527aaf42cc3adb9375224130de640a73988ff6df35796`.
- `oleid` reported VBA macros; `olevba` extracted `AutoOpen` and `AutoExec -> AutoOpen`.
- Macro behavior: `StrReverse` -> Base64 decode -> XOR `0x5A`.
- Recovered configuration contained an oracle token (not reproduced here) and endpoint `tcp://hived-off-oracle:16241`; the reachable service was `tcp://2.31.70.16:16241`.
- The macro was inspected statically and not executed.

Evidence: `forensics/quarterly_invoice.doc`, `forensics/deobfuscate.py`,
`forensics/extracted_config.json`, `logs/oleid.log`, `logs/olevba.log`,
`logs/deobfuscate.log`.

## Stage 2 — Bleichenbacher PKCS#1 v1.5

- Authenticated to the Stage 2 oracle and obtained a 1024-bit RSA public key
  (`e=65537`, `k=128`) plus the target ciphertext.
- Corrected protocol: each `DECRYPT <hex>` returns exactly one line,
  `VALID` or `INVALID`.
- Crafted-ciphertext tests confirmed the predicate is exactly
  `2B <= m < 3B`, with `B = 2^(8*(k-2))`; the service checks only the
  `00 02` prefix.
- Implemented the interval attack in `crypto/bleichenbacher.py` and validated
  it against a local 1024-bit RSA oracle.
- The initial formula search tested only the lower endpoint and stalled; fixed
  step 2c to search the full small `s` range for each `r`.
- Remote attack result: **converged**, `25,698` oracle queries, `992`
  iterations, `929.191` seconds, valid PKCS#1 plaintext, delimiter at offset
  `99`, 28-byte payload.
- Recovered the admin credential; it is stored in `crypto/credential.txt` and
  is intentionally not reproduced in this report.

Evidence: `logs/stage2_auth_response.txt`, `logs/oracle_shape.log`,
`logs/bb3_stdout.log`, `crypto/attack_results.json`,
`crypto/recovered_plaintext.bin`, `crypto/credential.txt`.

## Stage 3 — XPath injection

- Logged in to `http://2.31.70.16:16242/login` as `admin` with the recovered
  credential.
- The `/search?q=` value is interpolated into:
  `/directory/users/user[contains(displayName, '<q>')]/displayName`.
- Used a union-based injection to break out of the predicate:
  `x')] | //*[contains(text(),'ctf7{')] | //*[contains(displayName,'x`
- The response returned exactly one flag value.

Evidence: `web/solve.py`, `web/stage3_result.json`, `web/flag.txt`,
`logs/stage3_solve.log`.

## Flag

`ctf7{vba_macro_bleichenbacher_xpath_pivot}`

## Files

- `ctf7_work/forensics/quarterly_invoice.doc`
- `ctf7_work/forensics/deobfuscate.py`
- `ctf7_work/forensics/extracted_config.json`
- `ctf7_work/crypto/bleichenbacher.py`
- `ctf7_work/crypto/probe.py`
- `ctf7_work/crypto/attack_results.json`
- `ctf7_work/crypto/recovered_plaintext.bin`
- `ctf7_work/crypto/credential.txt`
- `ctf7_work/web/solve.py`
- `ctf7_work/web/stage3_result.json`
- `ctf7_work/web/flag.txt`
- `ctf7_work/logs/`
- `ctf7_work/report.md`
