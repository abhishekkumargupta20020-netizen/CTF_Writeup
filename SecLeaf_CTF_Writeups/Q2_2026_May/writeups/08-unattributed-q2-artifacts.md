# Q2 May Artifacts — Attribution Uncertain

This note prevents loose files from being incorrectly promoted into solved SecLeaf challenges.

## `protected.zip`

Recovered file properties:

```text
Size: 220 bytes
ZIP entries: 1
Entry: flag.txt
Encrypted: yes
Compression: stored
Uncompressed size: 26 bytes
```

The archive metadata showed a CRC32 value of `7b499f13`.

Inspection:

```bash
file protected.zip
zipinfo -v protected.zip
unzip -l protected.zip
```

The archive is encrypted, but the preserved conversation does not establish its challenge title, password, or accepted flag. It is therefore listed as an unattributed artifact.

## `art.txt`

The file is a 442-byte ASCII pattern consisting largely of `@` and `%` characters. It forms a gradually changing shape:

```text
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@%%%%@@@@@@@@@@@@
@@@@@@@@@@%%%%%%%%%%@@@@@@@@@@
...
%%%%%%%%%@@@@@@@@@@@%%%%%%%%%%%
```

No challenge prompt, decoding rule, or verified result is preserved.

## `Chall.rar`

A 47,060-byte RAR artifact was uploaded on 24 May 2026. The recovered records do not establish whether it is the same Gerber task as `Files.rar` or a separate challenge. Do not merge its contents into the Q2 Gerber write-up without checking the archive manifest.

## Status

These artifacts are preserved as evidence, but they are not counted as solved SecLeaf challenges.
