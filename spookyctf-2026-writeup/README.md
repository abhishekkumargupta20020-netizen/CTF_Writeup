# SpookyCTF 2026 — Full Writeup

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026 (NJIT Cyber Security Network), 6–7 November 2026
**Competition window:** 2026-11-06 17:00 UTC → 2026-11-07 17:00 UTC (22:30 IST)
**Status of this writeup:** The competition is closed. Nothing in this bundle was submitted by an AI — every flag was submitted by the author on the platform (spooky.ctfd.io), which requires the author's login.

## How this bundle is organised

Each challenge has its own writeup file, grouped by outcome:

| Folder | Meaning | Count |
|---|---|---|
| `01-solved/` | Flag recovered. The 10 marked **Platform-confirmed** were accepted by the platform. The 6 marked **Flag recovered** were solved and the flag recovered during the event (their platform-confirmation is not recorded in the recap). | 16 |
| `02-derived-unconfirmed/` | A clean, complete derivation exists, but no platform result was reported before the window closed. Presented as record only — do not treat as confirmed. | 9 |
| `03-unsolved/` | No flag was found before close. Each file records what was tried and where it stopped. | 4 |
| `solvers/` | The runnable solver / exploit scripts, one folder per challenge. | — |
| `challenge-files/` | The original challenge inputs that are small enough to ship (binaries, pcaps, archives, text files). | — |
| `evidence/` | Derivation notes, decoded dumps and logs produced while solving. | — |
| `spookyctf-2026-recap.md` | The one-page final board compiled at close. | — |

## Status key

- **Platform-confirmed** — the flag was submitted on the platform and accepted.
- **Flag recovered** — the flag was recovered and delivered; platform confirmation is not recorded in the recap for these six.
- **Derived (unconfirmed)** — a complete derivation from the challenge files, but no platform result was reported before close.
- **Unsolved** — no flag was found.

## The board at close

**Platform-confirmed (10):** Glass bottle, Jokes website, Corn maze, Spooky Keystreams, ELF quine, SpookyTrust, EYE memory forensics, Philophobia, The Logical Way (Vulcan), Fear of math.

**Flag recovered (6):** Haunted portrait, Phantom Login, Cleithrophobia, Serial capture, StashTheHash, Diagraphephobia.

**Derived, unconfirmed (9):** Numerophobia, Demented Memories, Java reverse engineering, Emilia / Bavarian hospital, NICC security dashboard, I D0n't Feel S0 G00d, Graveyard letter, Informant historical site, Hashphobia (tail only).

**Unsolved (4):** Eberhardt Hall, SP00KY server, Visiobibliophobia, fsvchall2.

## Notes and limits

- **SP00KY server:** this challenge is recorded as unsolved with no solver script and no attack details. The participant material is not included in this bundle.
- **EYE memory forensics:** the memory image `spooked2.lime` is 1.0 GB (SHA-256 `cc89dd1b0799b1f4acde678d913e38e8c1f90e7575323d15c70d7ffe561b664e`) and is **not** included in this zip. The carving script is in `solvers/eye-forensics/carve.py` and the carve log is in `evidence/carve_log.txt`.
- **Hashphobia:** the Discord webhook that appeared in a VirusTotal comment is a fellow solver's personal channel. It is not included here and no solution was posted to it.
- **Remote services:** several challenge servers could not be reached from the solving machine (direct TCP was off), so some exploits were run by the author on their own machine and the output pasted back. Where that happened the writeup says so.

## Reproducing a solve

Each writeup names the solver script and the challenge files it uses. In most cases:

```bash
python3 solvers/<challenge>/solve.py        # or the named exploit script
```

Challenge files live in `challenge-files/`; evidence and derivation notes live in `evidence/`.
