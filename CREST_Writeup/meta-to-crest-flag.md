# CTF Write-Up: Metadata Too — CREST Flag Recovery

## 1. Challenge Overview

**Category:** Digital Forensics / Metadata Analysis  
**Difficulty:** Easy–Medium  
**Objective:** Recover the hidden `CREST{...}` flag from a collection of nine Microsoft Word documents and an accompanying cover memo.

### Challenge Description

The provided archive contains nine `.docx` files and a `cover_memo.txt` file. The memo indicates that a workstation belonging to R. Chen may have been compromised. However, only documents authored by the compromised account are relevant; the remaining documents are unrelated noise.

The task is to identify the relevant documents, recover the embedded data, reconstruct the hidden message, and decode the final flag.

## 2. Initial Investigation

The first step was to extract the archive and inspect its contents.

The archive contained:

- Nine Microsoft Word documents (`doc_01.docx` through `doc_09.docx`)
- One text file (`cover_memo.txt`)

The cover memo provided the critical clue:

> Only documents actually AUTHORED by the compromised account are relevant.

This suggests that document metadata, particularly the author field, is more important than the visible text in each document.

## 3. Analyzing Document Metadata

Microsoft Word documents use the Office Open XML format. A `.docx` file is essentially a ZIP archive containing XML files, including `docProps/core.xml`, which stores core properties such as the document author, title, and modification information.

The investigation focused on the **Author** field for all nine documents.

The metadata analysis revealed four documents authored by R. Chen:

| Document | Author | Internal Memo | Relevant Fragment |
|---|---|---|---|
| `doc_03.docx` | R. Chen | #1 | `Q1JFU1R7ZDBjeF9` |
| `doc_05.docx` | R. Chen | #2 | `jMHJlX3ByMHAzcn` |
| `doc_02.docx` | R. Chen | #3 | `QxZXNfYXIzX20zd` |
| `doc_04.docx` | R. Chen | #4 | `DRkNHQ0X3QwMH0=` |

The remaining five documents were authored by other accounts and were excluded from the reconstruction.

**Key finding:** The relevant data was embedded in the four documents authored by R. Chen.

## 4. Reconstructing the Hidden Message

The four relevant documents contained numbered internal memos. These numbers established the correct order for combining the fragments.

The fragments were therefore arranged as follows:

1. `doc_03.docx` — Memo #1
2. `doc_05.docx` — Memo #2
3. `doc_02.docx` — Memo #3
4. `doc_04.docx` — Memo #4

Concatenating the fragments in this order produced the following Base64-encoded string:

```text
Q1JFU1R7ZDBjeF9jMHJlX3ByMHAzcnQxZXNfYXIzX20zdDRkNHQ0X3QwMH0=
```

The result looked like Base64 because it used the expected character set and ended with padding (`=`).

## 5. Decoding the Base64 String

The reconstructed string was decoded using Python's standard `base64` module.

```python
import base64

encoded = (
    "Q1JFU1R7ZDBjeF9jMHJlX3ByMHAzcn"
    "QxZXNfYXIzX20zdDRkNHQ0X3QwMH0="
)

decoded = base64.b64decode(encoded).decode("utf-8")

print(decoded)
```

**Important:** The code above illustrates the decoding operation. When reproducing the solution, ensure the concatenated input matches the exact fragments extracted from the challenge files. The verified complete encoded string is:

```text
Q1JFU1R7ZDBjeF9jMHJlX3ByMHAzcnQxZXNfYXIzX20zdDRkNHQ0X3QwMH0=
```

Decoding the complete string reveals the flag.

## 6. Final Flag

```text
CREST{d0cx_c0re_pr0p3rt1es_ar3_m3t4d4t4_t00}
```

## 7. Why the Solution Works

The challenge combines three basic digital-forensics techniques:

- **Metadata inspection:** The author field identifies documents associated with the compromised account.
- **Evidence correlation:** The internal memo numbers establish the sequence in which the fragments must be combined.
- **Encoding recognition:** Base64 decoding converts the reconstructed fragments into the final flag.

The challenge also demonstrates why document metadata matters during incident response. Files may contain useful forensic evidence even when their visible contents appear unremarkable.

## 8. Lessons Learned

1. Never rely exclusively on visible document content when investigating a file collection.
2. Inspect document metadata, including authorship and core properties.
3. Follow explicit clues in accompanying notes before analyzing every file in depth.
4. Preserve fragment boundaries and ordering information during reconstruction.
5. Validate encoded data before attempting more complicated decoding techniques.
6. Distinguish relevant evidence from unrelated files in a forensic collection.

## 9. Conclusion

The flag was recovered by filtering the nine documents using their author metadata, selecting the four documents attributed to R. Chen, arranging their fragments according to the internal memo numbers, and decoding the reconstructed Base64 string.

The central lesson is that **metadata can reveal information that is not immediately visible in a document's contents**.

**Flag:** `CREST{d0cx_c0re_pr0p3rt1es_ar3_m3t4d4t4_t00}`
