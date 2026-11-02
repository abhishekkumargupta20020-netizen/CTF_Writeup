# JPEG / ZIP Polyglot — Appended Archive Investigation

- **Competition:** SecLeaf Q2 2026
- **Date investigated:** 23 May 2026
- **Category:** Steganography / file-format forensics
- **Status:** Partial; no accepted flag recovered

## Objective

Inspect a JPEG carrier that also contains an appended ZIP archive, then continue the investigation using the extracted note and steganographic clues.

## Key finding

The ZIP local-header signature was found at byte offset:

```text
9179
```

The embedded archive was extracted from the JPEG carrier. The extracted `note.txt` contained the clues:

```text
XOR reuse
ECB leak
```

The notes from the investigation also recorded the phrase:

```text
entropy != randomness
```

Treat these as hints for subsequent cryptographic/steganographic work, not as a recovered flag.

## 1. Identify the polyglot

```bash
file challenge.jpg
xxd -l 64 challenge.jpg
binwalk challenge.jpg
grep -aob $'PK\x03\x04' challenge.jpg
```

The ZIP begins at offset `9179`.

## 2. Extract the ZIP tail

```bash
python3 ../solvers/extract_jpeg_zip.py challenge.jpg embedded.zip
unzip -l embedded.zip
unzip embedded.zip
```

Expected extracted file:

```text
note.txt
```

## 3. Steghide follow-up

The prior investigation examined the JPEG's Steghide capacity. The recorded available capacity was:

```text
446 bytes
```

Several passphrase attempts were made, but no successful hidden payload extraction or accepted flag was preserved.

Suggested inspection:

```bash
steghide info challenge.jpg
steghide extract -sf challenge.jpg
```

Do not invent a passphrase; use only one recovered from the original challenge evidence.

## 4. Interpretation

The note's references to XOR reuse and ECB leakage point toward cryptographic misuse:
- repeated XOR keystreams can expose relationships between plaintexts,
- ECB leaks repeated block structure,
- entropy is not equivalent to cryptographic unpredictability.

The precise downstream ciphertext, key material, and successful plaintext are not present in the recovered record.

## 5. Status

The JPEG/ZIP polyglot and embedded note were recovered. The final flag was not.
