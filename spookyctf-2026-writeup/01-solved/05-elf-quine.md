# ELF quine — a 112-byte self-printing ELF

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Platform-confirmed

## Flag

```
spooky{phdr_in_ehdr_c2d021cc4fc5}
```

## Challenge

A service at `3.129.162.36:31903` accepts a program of at most 112 bytes. The program must print itself (a quine) and exit with status 0. The catch: it must be a valid ELF executable.

## Files

- `solvers/elf-quine/submit_quine.py` — submission helper
- `solvers/elf-quine/quine_v3` — the accepted 112-byte ELF

## Solution

The trick is that an ELF file's program header can live *inside* the ELF header itself (`p_filesz = p_memsz = 112`), so the whole file is both header and program. The code then just writes its own bytes to stdout.

Three versions were tried:

- **v1** failed: it set `EI_CLASS = 254`, which is not a valid ELF class.
- **v2** (105 bytes) failed on the server with exit status −11 (SIGSEGV) — it relied on registers that the loader left as garbage.
- **v3** (112 bytes) sets every register explicitly before use and sets `p_filesz = p_memsz = 112`. It passed both a normal loader test and a garbage-register loader test, and the server accepted it.

## Flag

```
spooky{phdr_in_ehdr_c2d021cc4fc5}
```

Submitted on the platform and accepted.
