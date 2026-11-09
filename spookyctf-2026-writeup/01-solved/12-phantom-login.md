# Phantom Login — Windows log forensics

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Flag recovered

## Flag

```
spooky{the_ghost_left_a_trace}
```

## Challenge

A `Phantom_Login.zip` containing `njit_security.csv`, `njit_web.log`, `case_notes.txt`, and `PLAYER_README.md`. A phantom account logged in and accessed the archives. Trace it and find the flag.

## Files

- `challenge-files/Phantom_Login.zip` — the log bundle
- `evidence/phantom_case_notes.txt` — the case notes

## Solution

**1. Find the phantom account.**
In the security log, the account `evelyn.graves` stands out: it is the only user ever seen from external IP `203.0.113.77`. Its timeline (in-file timestamps, 2026-10-31):

| Time (UTC) | Event |
|---|---|
| 03:10–03:12 | 9 failed logons, event 4625 |
| 03:14 | Successful logon, event 4624 |
| 03:15 | Special privileges, event 4672 |
| 03:17 | Access to `\\BW-FS01\Archives$`, event 5140 |

All with LogonID `0xB130`. The `administrator` failures from `198.51.100.66` are a decoy — a different source IP and a different account.

**2. Follow the web log.**
The web log shows the same user and IP accessing `/archives/` and `/archives/export?note=...`.

**3. Decode the note.**
Base64-decoding the `note` parameter gives the flag.

## Flag

```
spooky{the_ghost_left_a_trace}
```

Flag recovered during the event.
