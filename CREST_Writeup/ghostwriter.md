# Ghost Writer - CTF solve report

## Executive summary

The challenge is a two-stage firmware/backend problem:

1. **MIPS firmware (`gw-client`)** speaks a small big-endian binary protocol to
   the backend: a 16-byte header `(magic, opcode, index, length)` using magic
   `GWP1` (`0x47575031`) and opcodes `1=NEW, 2=EDIT, 3=DEL, 4=VIEW, 6=DIAG`.
2. **Backend (`noted`, x86-64, non-PIE, glibc 2.36)** has a use-after-free:
   `DEL` frees a note but leaves its pointer and size.  `EDIT`/`VIEW` operate on
   the stale pointer.  A UAF write to a freed large chunk's `bk_nextsize`
   poisons a subsequent large-bin insertion.  The unchecked
   "smaller than smallest" path writes the inserted victim chunk address to
   `bk_nextsize + 0x20`.  Pointing that at `g_diag` redirects the `DIAG`
   indirect call to attacker-controlled heap data, where we place the hidden
   `win()` function.

**Verified flag (exact bytes returned by the live service):**

```
ctf7{mips_re_largebin_attack_chain}
```

Raw terminal output:

```
[noted] diagnostic override engaged -- dumping master note:
ctf7{mips_re_largebin_attack_chain}
```

The live service was solved multiple times with identical output.  Note: the task text
says `ctf{...}`, but the actual service flag uses the `ctf7{...}` prefix; the
report preserves the observed bytes rather than altering them.

## Stage 1 - Firmware and protocol

### Artifacts

| File | SHA-256 | Type |
|------|---------|------|
| `artifacts/gw-client` | `CE3EF0E5E003090EEA2C0D3D14C4F3C5DD0CA34A745D14D4AA64279761603329` | ELF32, MSB, MIPS, ET_EXEC, static |
| `artifacts/noted` | `1F35E9C057FABD89184D5DE98DDB316632C93BB82E4C97DC7F844504D7A14259` | ELF64, x86-64, ET_EXEC, non-PIE |

`gw-client` header: `ELFCLASS32`, `ELFDATA2MSB`, `EM_MIPS`, entry `0x400580`,
statically linked (907,208 bytes).  Execution would require a big-endian MIPS
emulator (`qemu-mips`, not `qemu-mipsel`); the protocol was recovered
statically.  The reference backend was supplied by the challenge server, so
static analysis of `noted` was possible in addition to firmware analysis.

### Recovered protocol

Full byte-level specification is in `protocol/protocol.md`.

```
Header (16 bytes, four big-endian u32):
  +0x00 magic  = 0x47575031 ("GWP1")
  +0x04 opcode
  +0x08 index  (0..15)
  +0x0c length (payload bytes; 0 for DEL/VIEW/DIAG)
```

| Opcode | Operation | Payload |
|-------:|-----------|---------|
| 1 | NEW  | `length` bytes; malloc, store pointer/size, read payload |
| 2 | EDIT | `length` bytes; read into stored pointer |
| 3 | DEL  | none; `free`, pointer not cleared |
| 4 | VIEW | none; write `stored_size` raw bytes |
| 6 | DIAG | none; call `g_diag->fn` |

Key static evidence:

* `send_hdr @ 0x400710` builds `0x47575031` with `lui $v0,0x4757` /
  `ori $a0,$v0,0x5031`, applies `htonl` to all four fields, writes 16 bytes.
* `req_new @ 0x4007f8`, `req_edit @ 0x40088c`, `req_delete @ 0x400920`,
  `req_view @ 0x400984`, `req_diag @ 0x4009e8` pass opcodes 1, 2, 3, 4, 6.
* Backend `main @ 0x40137a` reads 16 bytes, applies `ntohl` four times,
  compares the first word with `0x47575031`, and jumps through the table at
  `0x4020c0`.
* Full client disassembly: `logs/gw-client.disasm.txt`.

### Dynamic validation

`protocol/test_protocol.py` against the live backend produced:

```
NEW   -> b'OK_NEW\n'
VIEW  -> b'AAAA'
EDIT  -> b'OK_EDIT\n'
VIEW  -> b'BBBB'
DIAG  -> b'[noted] diagnostics nominal.\nOK_DIAG\n'
DEL   -> b'OK_DEL\n'
OP5   -> b'ERR_OP\n'
```

The same exchange also succeeds against the supplied `noted` running under the
exact Debian 12 glibc 2.36 loader.

## Stage 2 - Backend analysis and exploitation

### Vulnerability

`DEL` at `0x40155a` calls `free(notes[index])` but does not null
`notes[index]` or clear `sizes[index]`.  `EDIT` at `0x4014fe` reads attacker
data into `notes[index]`, and `VIEW` at `0x40158b` writes from it.  This gives a
use-after-free read and write with lengths up to `0x2000`.

### Diagnostic target

* `g_diag` is a global function-table pointer at `0x4040c0`, initially
  `0x4040a0` (`default_diag`).
* `DIAG` (`0x4015c3`) executes `rax = g_diag; rax = [rax+0x18]; call rax`.
* `default_diag`'s slot `[0x4040a0+0x18] = 0x4012e7` (`diag_default`).
* `win @ 0x4011e6` opens `/flag.txt`, reads up to `0x100` bytes, writes them to
  stdout, and calls `_exit(0)`.  It falls back to the `FLAG` environment
  variable if `/flag.txt` is unavailable.

### Large-bin primitive (glibc 2.36)

In `_int_malloc`, when an unsorted large chunk is inserted below the smallest
chunk of its large bin, glibc 2.36 executes (no integrity check on
`bk_nextsize` in this branch):

```c
if (size < chunksize_nomask(bck->bk)) {
    fwd = bck;
    bck = bck->bk;
    victim->fd_nextsize = fwd->fd;
    victim->bk_nextsize = fwd->fd->bk_nextsize;
    fwd->fd->bk_nextsize = victim->bk_nextsize->fd_nextsize = victim;
}
```

The final statement writes the **victim chunk address** to
`(bk_nextsize + 0x20)`.

### Heap choreography

Chunk sizes (64-bit glibc, tcache max request `0x408`; both chunks bypass
tcache):

* `A`: request `0x420` -> chunk `0x430`, large-bin index 64.
* `B`: request `0x410` -> chunk `0x420`, large-bin index 64 (< `A`).
* Guards/triggers: requests `0x1000` and `0x2000` (chunks `0x1010`/`0x2010`),
  used to prevent top consolidation and to force unsorted-bin processing.

| Step | Operation | Allocator state / effect |
|-----:|-----------|--------------------------|
| 1 | `NEW A(0x420)`, `NEW G1(0x1000)`, `NEW B(0x410)`, `NEW G2(0x1000)` | all in use; B must exist before A is sorted |
| 2 | `DEL A` | A -> unsorted bin (G1 prevents top merge) |
| 3 | `NEW T1(0x2000)` | A sorted into large bin 64; `fd_nextsize=bk_nextsize=A`; T1 from top |
| 4 | `DEL B` | B -> unsorted bin (G2 prevents top merge) |
| 5 | `EDIT A` (UAF) | `A->bk_nextsize = g_diag - 0x20 = 0x4040a0` |
| 6 | `NEW T2(0x2000)` | B sorted; `B < A` -> first branch writes `B` to `0x4040c0`; thus `g_diag = B`; then `B->bk = A` |
| 7 | `EDIT B` (UAF) | `B->bk = 0x4011e6`; since `g_diag = B`, `[g_diag+0x18] = [B+0x18] = win` |
| 8 | `DIAG` | `call [g_diag+0x18]` -> `win()` -> dumps flag and `_exit(0)` |

Address/value table:

| Symbol / field | Address | Value used |
|----------------|---------|------------|
| `g_diag` | `0x4040c0` | overwritten with B chunk base |
| `g_diag - 0x20` (write destination base) | `0x4040a0` | stored in `A->bk_nextsize` |
| `g_diag[3]` / `[B+0x18]` | `0x4040c0+0x18` / `B+0x18` | `0x4011e6` (`win`) |
| `win` | `0x4011e6` | flag dumper |
| `diag_default` | `0x4012e7` | original callback |
| `DIAG` call site | `0x4015c3` | `call [g_diag+0x18]` |

Important verified detail: `B` must be allocated **before** `A` is sorted into
the large bin.  Allocating `B` afterwards makes `malloc(0x410)` carve `B` out of
`A` in the large bin, and the later UAF edit corrupts the unsorted-bin chunk's
`fd`/`bk`, tripping glibc's unlink check.  This was observed in the local lab
and corrected.

### Verification

The exploit was first reproduced locally against the supplied `noted` running
under the exact Debian 12 glibc loader (`Debian GLIBC 2.36-9+deb12u14`), with a
dummy `FLAG` environment value; it printed
`ctf{LOCAL_TEST_FLAG}`, proving the full chain (UAF -> large-bin write ->
`g_diag` redirect -> `win`).

It was then run repeatedly against the live endpoint `2.31.70.16:16251`.  Every
run completed every stage and produced the same 96-byte response:

```
5b6e6f7465645d20646961676e6f73746963206f7665727269646520656e6761676564202d2d
2064756d70696e67206d6173746572206e6f74653a0a637466377b6d6970735f72655f6c61
72676562696e5f61747461636b5f636861696e7d0a
```

which decodes to `[noted] diagnostic override engaged -- dumping master
note:\nctf7{mips_re_largebin_attack_chain}\n`.

## Reproducibility

Required tools:

* Python 3, `capstone`, `pyelftools` (analysis), `socket`/`struct` (exploit).
* A Linux environment (WSL is sufficient) for the local lab: `socat`,
  `dpkg-deb`, and the extracted Debian 12 glibc 2.36 loader.
* Windows/Linux `objdump` for the x86-64 backend; Capstone for MIPS.

Commands:

```bash
# fetch artifacts
curl -O http://2.31.70.16:16250/gw-client
curl -O http://2.31.70.16:16250/noted
sha256sum gw-client noted

# protocol check against the live backend
python protocol/test_protocol.py 2.31.70.16 16251

# full exploit against the live backend
python exploit/solve.py 2.31.70.16 16251
```

Local lab (optional):

```bash
# extract the exact glibc and run the supplied backend via socat
dpkg-deb -x libc6_2.36-9+deb12u14_amd64.deb glibc236
socat TCP-LISTEN:16261,reuseaddr,fork EXEC:/tmp/gwtest/run.sh
python exploit/solve.py 127.0.0.1 16261
```

Key files:

* `protocol/protocol.md` - byte-level protocol specification.
* `protocol/gwproto.py` - protocol client/serializer.
* `protocol/test_protocol.py` - benign live validation.
* `exploit/solve.py` - full exploit.
* `exploit/debug_heap.py` - UAF-based heap-state inspector (local lab).
* `exploit/gen_input.py` - emits the exploit byte stream for offline debugging.
* `logs/gw-client.disasm.txt`, `backend/noted.disasm.txt` - disassembly.
* `logs/remote_solve.log`, `logs/last_output.bin` - live run evidence.

## Limitations and uncertainty

* The remote server's exact libc patch level cannot be read directly.  The
  challenge states glibc 2.36; behavior matches Debian 12 glibc
  `2.36-9+deb12u14`, which was used for local reproduction.
* No heap address leak is required: the write value is the victim chunk address
  and the target is the fixed non-PIE `g_diag`.
* The observed flag prefix is `ctf7{`, not `ctf{` as stated in the task text.
  The exact server bytes are reported above and preserved in
  `logs/last_output.bin`.
* The local lab uses the `FLAG` environment fallback because `/flag.txt` does
  not exist locally; the remote run reads the real `/flag.txt` (the returned
  value differs from the local dummy).
