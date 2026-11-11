# CyberZerk — Tricatel Writeup

**Author:** Abhishek Kr Gupta
**Event:** CyberZerk Tricatel challenges, 2026-11-10
**Status:** 4 solved, 2 still open. Nothing in this bundle was submitted by an AI — every flag was submitted by the author.

## The board

| # | Challenge | Site | Status | Flag |
|---|---|---|---|---|
| 1 | Pointeuse — hidden overtime | https://pointeuse.cyberzerk.fr | Solved | `CyberZerk{P0int3us3_Qu1_0ubl13_L3s_H3ur3s_Sup}` |
| 2 | Absences — IDOR sick-leave file | https://absences.cyberzerk.fr | Solved | `CyberZerk{ID0R_M4n4g3m3nt_T0x1qu3}` |
| 3 | Email — spoofed HR mail | `note_du_drh.eml` (uploaded file) | Solved | `CyberZerk{M4il_Sp00f3_P0ur_Surv31ll3r_L3s_Arr3ts}` |
| 4 | Manager — JWT alg:none | https://manager.cyberzerk.fr | Solved | `CyberZerk{JWT_4lg_N0n3_C_3st_N0n}` |
| 5 | SQL — admin login, CEO memo | https://sql.cyberzerk.fr | Open | — |
| 6 | Restructuration — SSRF, internal vault | https://restructuration.cyberzerk.fr | Open | — |

## How this bundle is organised

- `01-solved/` — one file per solved challenge: the vulnerability, the exact steps, and the flag.
- `02-open/` — one file per open challenge: what was tried, what failed, and the next concrete check.
- `evidence/` — the solve notes and attempt logs written while solving.
- `solvers/` — the SSRF test script (`test_ssrf.py`).

## The common thread

All six challenges are one story: Tricatel's HR systems were built in a rush — a developer coding auth at 4:00 AM after sleepless nights — and every layer trusts the client: an unsigned cookie decides your role, a dossier number in the URL decides whose file you read, an email's `From:` header is taken at face value, a JWT is accepted with no signature, a login query is built from raw input, and a URL fetcher is trusted to stay outside the internal network.

## Notes and limits

- The SQL payloads in `02-open/05-sql-admin-login.md` were listed but never run live: the POST to sql.cyberzerk.fr was blocked during preparation, so they still need one live run (by the author, with any password such as `x`).
- The SSRF fetcher appears to have no usable external egress, and loopback is the fetcher's own, not the app's — see `02-open/06-ssrf-restructuration.md` for the full ~30-URL log.
- One mix-up to avoid: the SSRF challenge lives on **restructuration.cyberzerk.fr**, not manager.cyberzerk.fr. The manager site is the JWT challenge.
