# CTF Write-up: Zone Transfer

## Challenge Overview

- **Challenge Name:** Zone Transfer
- **Category:** DNS / Network Security / Digital Forensics
- **Flag Format:** `CREST{...}`
- **Artifacts Provided:** `zone_dump.json`, `ops_changelog.json`
- **Difficulty:** Easy–Medium

## 1. Challenge Description

The challenge provides two JSON files: `zone_dump.json` and `ops_changelog.json`. The objective is to recover the flag by examining the DNS zone data and correlating its records with the operational change history.

The key observation is that the flag is split into five fragments. Each fragment is encoded using Base32 and associated with a `serial_ref` value. These references correspond to `change_serial` values in the operations changelog.

The fragments must be decoded and ordered correctly to reconstruct the complete flag.

## 2. Investigation Methodology

### Step 1: Inspect the Provided Artifacts

Start by examining the structure of both JSON files.

- `zone_dump.json` contains DNS-related records and encoded flag fragments.
- `ops_changelog.json` contains operational change records, including serial numbers and associated hosts.

The goal is to identify the encoded fragments and determine how they relate to the changelog.

### Step 2: Identify the Base32-Encoded Fragments

Inspect the records in `zone_dump.json` and locate the fields containing encoded data. The relevant records contain fragments associated with `serial_ref` values.

Base32 is an encoding scheme that represents binary data using a restricted alphabet. It is not encryption, so the original content can be recovered by decoding the encoded values.

The important task is to decode each fragment without losing its association with its serial reference.

### Step 3: Correlate the Serial References

For each fragment, match its `serial_ref` against the corresponding `change_serial` in `ops_changelog.json`.

This correlation provides the ordering information required to reconstruct the flag. The fragments should be sorted by their matching change serials in ascending order.

### Step 4: Decode and Order the Fragments

The recovered fragments, in changelog order, are:

| Change serial | Host | Decoded fragment |
|---:|---|---|
| `2024010209` | `stage.meridianlabs.ctf` | `CREST{z0n3` |
| `2024010268` | `portal.meridianlabs.ctf` | `_tr4nsf3rs` |
| `2024011069` | `mx2.meridianlabs.ctf` | `_ar3n7_sup` |
| `2024012279` | `git.meridianlabs.ctf` | `p0s3d_t0_b` |
| `2024012711` | `mail.meridianlabs.ctf` | `3_publ1c}` |

Concatenating the fragments in ascending serial order produces the complete flag.

## 3. Flag Reconstruction

The fragments can be represented as:

```text
CREST{z0n3
_tr4nsf3rs
_ar3n7_sup
p0s3d_t0_b
3_publ1c}
```

Combining them without inserting additional characters gives:

```text
CREST{z0n3_tr4nsf3rs_ar3n7_supp0s3d_t0_b3_publ1c}
```

## 4. Final Flag

```text
CREST{z0n3_tr4nsf3rs_ar3n7_supp0s3d_t0_b3_publ1c}
```

## 5. Why the Solution Works

The solution relies on two linked pieces of evidence:

1. **Encoding:** Base32 decoding reveals the individual flag fragments.
2. **Correlation and ordering:** The `serial_ref` values connect the fragments to the operations changelog, whose `change_serial` values establish their correct sequence.

Decoding alone would reveal only disconnected pieces. Correlating the records and sorting them by their matching serial numbers recovers the intended token.

The reconstructed message reads:

> “Zone transfers aren't supposed to be public.”

This wording is consistent with the challenge's DNS misconfiguration theme.

## 6. Security Lessons

The challenge illustrates several important security concepts:

- **DNS zone-transfer exposure:** Unrestricted DNS zone transfers can disclose hostnames and other DNS records to unauthorized parties.
- **Information disclosure:** Internal naming conventions and infrastructure relationships can help an attacker map an organization's environment.
- **Metadata correlation:** Serial numbers and references can expose relationships between otherwise separate data sources.
- **Encoding is not encryption:** Base32 provides a representation of data, not confidentiality.
- **Defensive DNS configuration:** Restrict zone transfers to authorized secondary DNS servers and monitor unexpected transfer attempts.

## 7. Conclusion

The challenge was solved by decoding five Base32 fragments from `zone_dump.json`, matching each fragment's `serial_ref` to the corresponding `change_serial` in `ops_changelog.json`, and concatenating the fragments in ascending serial order.

The final flag is:

`CREST{z0n3_tr4nsf3rs_ar3n7_supp0s3d_t0_b3_publ1c}`

The central lesson is that exposed DNS zone data can reveal infrastructure information, while careful correlation of structured artifacts can recover information hidden across multiple records.
