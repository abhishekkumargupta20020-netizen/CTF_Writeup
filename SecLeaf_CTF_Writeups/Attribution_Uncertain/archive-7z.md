# Encrypted Archive.7z — Attribution Uncertain

- **Competition:** Not confirmed
- **Category:** Archive forensics / password recovery
- **Status:** Incomplete; excluded from the confirmed SecLeaf Q4 index

## Recovered investigation notes

A separate archive investigation referenced:
- `Archive.7z`,
- AES-256 encryption,
- a 2^19 KDF/work factor,
- approximately 131 candidate passwords tested,
- no successful extraction in the preserved session.

The exact challenge prompt, archive hash, source filename, and flag were not preserved in a way that proves this was a SecLeaf Q4 challenge.

## Safe reproduction workflow

```bash
file Archive.7z
7z l -slt Archive.7z
sha256sum Archive.7z
```

Preserve the archive and avoid repeatedly launching large password lists without confirming the challenge's intended password derivation.

## Attribution

This entry is included only so the investigation is not lost. It is not counted as a SecLeaf challenge or a solved result until the event attribution is confirmed.
