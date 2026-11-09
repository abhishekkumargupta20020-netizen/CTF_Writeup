# fsvchall2 — format string

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Unsolved — payload verified locally, remote secret never fetched

## Challenge

A format-string vulnerability. The binary prints user input with `printf(input, secret)`, where `secret` is read from `/opt/ctf/chall2/secret.txt`. The service is at `nc 18.226.103.146 9002`.

## Files

- `challenge-files/fsvchall2.c` — the vulnerable source
- `challenge-files/fsvchall2.bin` — the binary
- `solvers/fsvchall2/fsvchall2_exploit.py` — the exploit

## Vulnerability

`vuln()` does:

```c
printf(input, secret);
```

`secret` is the first vararg. So the format-string payload `%s` prints the secret.

## Exploit

The payload is simply:

```
%s
```

The full script is `solvers/fsvchall2/fsvchall2_exploit.py`. It was verified locally against a fake secret using `socat`, and it works.

## Why it stayed unsolved

The remote service (`18.226.103.146:9002`) could not be reached from the solving machine — direct TCP was off. The exploit was left as a one-command job for the author to run on their own machine:

```bash
python3 solvers/fsvchall2/fsvchall2_exploit.py
```

The output would be the secret, and the flag would be `spooky{<secret>}`. The remote secret was never fetched before the window closed.

## Status

Unsolved. The payload is verified locally, but the remote secret was never retrieved.
