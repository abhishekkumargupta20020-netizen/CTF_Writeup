# Hashphobia — the magic word

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Unsolved — only the flag tail is known; the beginning was never found

## Known flag tail

The flag ends with:

```
4nd_ch3ck_review5}
```

(Base64 `NG5kX2NoM2NrX3JldmlldzV9` decodes to `4nd_ch3ck_review5}`.)

The beginning is unknown, so there is no complete flag.

## Challenge

750 points, author Frank C, 0 solves. Only a SHA-256 hash is given, with the instruction "do some recon":

```
f854432d21db979021f45b85384b7f2d6500fa2f62981c87ebba79b3d46f1a7b
```

## Files

- `solvers/hashphobia/solver.py` — the probing solver (stdlib-only)

## Recon

**1. The hash is a file.**
VirusTotal knows the hash: the file is `case-telemetry.sh`, a 138-byte shell script, 0/61 detections. It is a plain GET to:

```
http://18.117.181.107/
```

which replies:

```
status=nah; message=what's the magic word?
```

**2. The flag tail.**
A VirusTotal comment by "thehackerguy" (profile name Frank C — the author) gives the flag tail as Base64: `NG5kX2NoM2NrX3JldmlldzV9` → `4nd_ch3ck_review5}`.

**3. The server.**
RDAP: `18.117.181.107` sits in `NET-18-32-0-0-1` (AT-88-Z, Amazon), registered 2019-10-07. That confirms AWS hosting only — no flag lead.

**4. Platform hint.**
Hint 1: the magic word is one of the finite set of English magical words.

## What was tried — all "nah"

Over 1,000,000 probes in total, all `nah`:

- A 370k-word dictionary against `?word=`
- Classic / pop-culture / Harry Potter magic words
- Manners words
- Parameter and path fuzzing
- The comment's own words, the hash prefixes, the server IP, phobia words, and more

The wordlist space is exhausted. A rockyou password attack was requested and declined.

## Solver

`solvers/hashphobia/solver.py` (stdlib-only) has a built-in magic-words list, `--wordlist`, `--download-lists`, and `--vt-api-key` modes. Tested: 525 requests in 8 seconds, no hit.

## Full-flag guesses given (unconfirmed, none reported as accepted)

```
spooky{do_some_recon_4nd_ch3ck_review5}
spooky{recon_4nd_ch3ck_review5}
spooky{check_the_hash_4nd_ch3ck_review5}
spooky{always_do_recon_4nd_ch3ck_review5}
spooky{trust_but_verify_4nd_ch3ck_review5}
spooky{do_your_recon_4nd_ch3ck_review5}
```

## Remaining leads (not pursued)

- Discord was suggested as the remaining unchecked avenue.
- VT Intelligence (paid) similarity search for the author's "earlier script" was the other option. The admin said the challenge can be solved freely with no paid VT needed — the free path was never found.

A later VirusTotal comment by "max5196767" posted a Discord webhook for a personal channel, not the author's. No solution was posted there, and the token URL is not included in this bundle.

## Status

Unsolved. Only the tail `...4nd_ch3ck_review5}` is known.
