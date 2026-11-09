# SP00KY Server --- Remote-Access Protocol

**Category:** Binary Exploitation / ELF / Remote Access\
**Architecture:** Linux x86-64\
**Remote endpoint:** `3.129.162.36:31903`\
**Payload limit:** 112 bytes\
**Status:** Solved

## Flag

``` text
sp00ky{reused_k_no_nons3nse_89f3ae32316e}
```

## 1. Challenge overview

The service accepts a very small x86-64 Linux ELF executable. The
submitted program must:

1.  Be no larger than 112 bytes.
2.  Write its own exact bytes to standard output.
3.  Exit with status `0`.

The service protocol is:

1.  Connect to the host and port.
2.  Read the banner.
3.  Send `SIZE <length>` followed by a newline.
4.  Send exactly that many raw ELF bytes.
5.  Read the service response (`PASS`/`FLAG` or `FAIL`).

This is an ELF quine challenge: the executable must reproduce its own
binary representation.

## 2. ELF size constraint and header overlap

A conventional ELF64 executable uses a 64-byte ELF header and a 56-byte
program header. Placed consecutively, these structures require 120
bytes, exceeding the 112-byte limit.

The intended size optimization is to place the program-header table at
offset 56 by setting `e_phoff = 56`. This overlaps the final eight bytes
of the ELF header with the beginning of the program header:

``` text
File offset
0                 56       64                         112
|-----------------|--------|--------------------------|
| ELF header      | shared | rest of program header   |
|                 | 8 byte |                          |
|-----------------|--------|--------------------------|
                  ^ program header begins at offset 56
```

The overlap allows the two structures to occupy 112 bytes in total. The
loader still needs a valid ELF identification, architecture, entry
point, program-header description, and executable load segment. Segment
alignment and the entry-point location must also be valid.

## 3. Quine execution concept

The program needs to perform two Linux x86-64 system calls:

-   `write(1, binary_start, 112)` --- write the complete mapped ELF
    image to stdout.
-   `exit(0)` --- terminate successfully.

The relevant syscall numbers are:

  System call     Number
  ------------- --------
  `write`            `1`
  `exit`            `60`

The executable can write its mapped image directly from memory; it does
not need to open its own file. Compact machine-code encodings and
careful use of ELF header bytes are essential to meeting the size limit.

> **Reproducibility note:** The supplied screenshot documents the later
> restricted-shell enumeration and flag retrieval. It does not show the
> exact 112-byte payload or assembly source. Therefore, this writeup
> explains the ELF-quine construction strategy but does not claim to
> reproduce the exact submitted binary.

## 4. Remote submission protocol

Connect to the service:

``` bash
nc 3.129.162.36 31903
```

The expected framing is:

``` text
SIZE 112\n
<exactly 112 raw ELF bytes>
```

Do not send hexadecimal text, Base64, or an extra newline as part of the
binary payload.

A Python submission client can transmit a locally generated ELF without
corrupting binary bytes:

``` python
#!/usr/bin/env python3

import socket
import sys
from pathlib import Path

HOST = "3.129.162.36"
PORT = 31903
MAX_SIZE = 112

payload_path = sys.argv[1] if len(sys.argv) > 1 else "./quine"
payload = Path(payload_path).read_bytes()

if len(payload) > MAX_SIZE:
    raise SystemExit(f"Payload too large: {len(payload)} bytes")

with socket.create_connection((HOST, PORT), timeout=10) as sock:
    sock.settimeout(5)

    banner = sock.recv(4096)
    print(banner.decode(errors="replace"))

    sock.sendall(f"SIZE {len(payload)}\n".encode("ascii"))
    sock.sendall(payload)

    response = bytearray()
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response.extend(chunk)
    except socket.timeout:
        pass

    print(response.decode(errors="replace"))
```

Run it with:

``` bash
python3 submit.py ./quine
```

## 5. Local validation

Before submitting, validate the executable locally:

``` bash
chmod +x quine

# Confirm the file size
wc -c quine

# Inspect ELF metadata
readelf -h quine
readelf -l quine

# Execute and capture stdout
./quine > output.bin
status=$?

# Compare output byte-for-byte with the executable
cmp quine output.bin

# Check the exit status
echo "$status"
```

Expected properties:

-   The file is at most 112 bytes.
-   `cmp` reports no differences.
-   The exit status is `0`.

A successful size check alone is not enough: the output must be
byte-for-byte identical to the uploaded executable.

## 6. Restricted-shell enumeration

After obtaining access to the SP00KY shell, the initial attempts to use
ordinary Linux utilities showed that this was a restricted command
interpreter.

For example:

``` text
admin@spooky:~$ cat /home/admin/flag.txt
cat: command not found

admin@spooky:~$ nano flag.txt
nano: command not found
```

The shell's own `help` command exposed its supported built-ins:

``` text
SP00KY shell
  help
  whoami
  id
  pwd
  ls [path]
  cd [path]
  cat <path>
  stat <path>
  date
  uname
  exit
```

The important distinction is that `cat` is available as a shell built-in
even though the external `cat` executable is unavailable.

### 6.1 Check identity

``` text
admin@spooky:~$ id
uid=0(admin) gid=0(admin) groups=0(admin)
```

The environment reports UID 0 for the `admin` account. The shell remains
restricted to its exposed commands.

### 6.2 Identify the working directory

``` text
admin@spooky:~$ pwd
/home/admin
```

### 6.3 List the home directory

``` text
admin@spooky:~$ ls /home/admin
flag.txt
notes.txt
```

The listing identifies `flag.txt` as the target file.

### 6.4 Read the flag

``` text
admin@spooky:~$ cat flag.txt
sp00ky{reused_k_no_nons3nse_89f3ae32316e}
```

## 7. Screenshot evidence

The screenshot below records the restricted-shell help output, identity,
working directory, directory listing, and successful flag retrieval.

![SP00KY restricted shell showing flag
retrieval](sp00ky-remote-shell.png)

## 8. Full solve sequence

1.  Connect to `3.129.162.36:31903`.
2.  Read the service banner and its payload limit.
3.  Construct an ELF64 quine within 112 bytes.
4.  Use the ELF header/program-header overlap to fit the required
    structures.
5.  Ensure the executable writes its complete mapped bytes and exits
    with status `0`.
6.  Send `SIZE <length>\n`, followed by exactly the raw ELF payload.
7.  Use the exposed SP00KY shell commands to enumerate the environment.
8.  Run `pwd` and `ls /home/admin`.
9.  Read the flag with the shell's built-in `cat`.

## 9. Key takeaways

-   ELF headers and program headers are structured data interpreted by
    the Linux loader; their layout can be exploited for size-constrained
    binaries.
-   A quine must reproduce every byte, not merely equivalent source code
    or output text.
-   Direct Linux syscalls avoid the size overhead of a standard C
    runtime.
-   Binary network protocols require exact length framing and raw-byte
    transmission.
-   A restricted shell may implement commands internally, so
    `command not found` for an external utility does not prove the
    corresponding built-in is unavailable.
-   Enumerate the supported command set with `help` before assuming a
    full shell is present.

## 10. Final result

**Flag:**

``` text
sp00ky{reused_k_no_nons3nse_89f3ae32316e}
```

**Evidence:** The supplied terminal screenshot shows the flag being read
from `/home/admin/flag.txt`.
