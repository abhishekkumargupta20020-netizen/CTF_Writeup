# SpookyTrust — a wrapped key and a small private exponent

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Platform-confirmed

## Flag

```
spooky{4T_L345T_1T_15NT_F0UR}
```

## Challenge

A certificate-authority ceremony: four P-384 intermediate CAs, a root certificate, CSRs, a `ceremony.log`, a `key-inventory.csv`, and a `client.py`. An audit server (`http://3.149.129.229:8000/`) checks a signature. One intermediate's private key is recoverable — find it, sign, and submit.

## Files

- `challenge-files/spookytrust/` — the four intermediate certs (`ST-ISS-01.pem` … `ST-ISS-04.pem`), their CSRs, `ceremony.log`, `key-inventory.csv`, `client.py`
- `solvers/spookytrust/bsgs2.py` — the baby-step giant-step search
- `solvers/spookytrust/sign_and_submit.py` — sign and submit to the audit server
- `evidence/bsgs2.log` — the search log

## The anomaly

Reading `ceremony.log` and `key-inventory.csv` against the certificates, one event stands out: object `OBJ-0003` was wrapped (AES-256-GCM) and then unwrapped through a `compat-restore` step into `OBJ-0003-R`, which was used for intermediate `ST-ISS-03`. That wrap/unwrap round-trip is the weak point.

## Recovering the key

`ST-ISS-03` is a P-384 key, but its private exponent `d` turns out to be small (under 2^40). A baby-step giant-step (BSGS) search over the P-384 curve finds it:

```
d = 1963
```

The search is `solvers/spookytrust/bsgs2.py`; the successful run is recorded in `evidence/bsgs2.log`.

## Signing and submitting

With `d = 1963`, `solvers/spookytrust/sign_and_submit.py` builds the signature and submits it to the audit server. The server returned:

```json
{"result": "VALID", "flag": "spooky{4T_L345T_1T_15NT_F0UR}"}
```

## Flag

```
spooky{4T_L345T_1T_15NT_F0UR}
```

("at least it isnt four" — a joke about the small exponent.) Submitted on the platform and accepted.
