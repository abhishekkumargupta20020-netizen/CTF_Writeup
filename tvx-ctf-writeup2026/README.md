# TVX CTF — Writeup

**Author:** Abhishek Kr Gupta
**Event:** TVX CTF, 2026-11-13
**Status:** 17 solved, 2 still open. Nothing in this bundle was submitted
by an AI — every flag was submitted by the author (or, where noted, has
not been submitted yet).

This is the merged bundle: the 14 challenges worked in this session
plus the 7 writeups Shikhu uploaded as `tvx_all_writeups.zip` (kept
verbatim under `contributed/tvx_all_writeups/`). One of those — the
memory dump — is the same challenge as the one that was open here, so
the merged total is **19 distinct challenges**.

## Status tiers — read these before the flags

- **Confirmed by Shikhu:** Evidence.zip — he confirmed the flag himself
  in chat ("this is correct").
- **Solved in the challenge app / retrieved live:** Forgotten Tenant
  (flag read from `evidence.json` after a live AWS role chain) and
  Mission: Broken Trust (6/6 stages accepted in the app). Neither was
  submitted to the platform by Muse; Shikhu submits himself.
- **Verified live by the contributed writeup's author:** TraceVX — all
  10 answers confirmed twice against the analyst service.
- **Derived, solver re-run here:** SteelAndFeathers, TwistMeATwister,
  SummerIsOver, Creeper RSA, Steve's Lost Book, Chest, The Fourth
  Portal, and the contributed cryptoone, Ending, WHAT A WASTE OF
  TOKENS... (3), and GhostNote — each solver was re-run in this session
  from its own folder and reproduced its flag. None has a platform
  acceptance on record yet.
- **Solved per contributed writeup, not re-run here:** the memory dump —
  its solver needs the 6.4 GB `memory.raw`, which was never downloaded
  here (Google Drive quota exceeded). The writeup matches the challenge
  exactly (same Drive file ID, same sizes) and its internal checks are
  recorded in the file.
- **Solved per uploaded writeup, Q5 independently verified here:**
  malwareX — Q1–Q4 match the earlier static analysis exactly, and the
  C2 was confirmed by decrypting the two `.cctor` Base64 blobs from the
  sample's own IL with the derived key (hosts and port reproduced
  byte-for-byte).
- **Open:** WHAT A WASTE OF TOKENS... (the `flag.txt` one) and ASK ME.

## The board

| # | Challenge | Category | Status | Flag |
|---|---|---|---|---|
| 1 | SteelAndFeathers | .NET / VM | Solved (derived) | `TVX{Congratulations_You_Know_Some_ball}` |
| 2 | TwistMeATwister | .NET | Solved (derived) | `TVX{Fl4ggy_fl4g_fl4g_tw15ty_tw15t_tw15t}` |
| 3 | SummerIsOver | .NET | Solved (derived) | `TVX{4nd_S0_7h3_5un_Sh1n35}` |
| 4 | Creeper RSA vaults | Crypto / RSA | Solved (derived) | `TVXCTF{the_creeper_reused_a_prime}` |
| 5 | Steve's Lost Book | Encoding | Solved (derived) | `TVXCTF{steve_found_the_hidden_chest}` |
| 6 | Chest / DO NOT SORT | Crypto / substitution | Solved (derived) | `TVX{never_dig_straight_down}` |
| 7 | Forgotten Tenant | Cloud / AWS | Solved (live) | `TVX{6N8at90xLFvdgyma648o}` |
| 8 | Mission: Broken Trust | Cloud | Solved 6/6 in app | `TVX{ROLE_HANDOFF_LAMBDA_TRUST_PUBLIC_POLICY_SECRET_READ_ROLE_SESSION_KMS_DECRYPT}` |
| 9 | The Fourth Portal | Crypto / poly + AES-GCM | Solved (derived) | `TVX{th3_3ch0_b1nds_th3_f0ur_w0rlds}` |
| 10 | Chrome History / Evidence.zip | Forensics | **Confirmed by Shikhu** | `TVX{2,http://127.0.0.1:8000/review.html,completed,2026-10-10_22-16-02}` |
| 11 | cryptoone | Crypto / ECDLP | Solved (contributed, solver re-run) | `TVX{D1dn5_F4lL_4_7h3_7r4p_7h15_t1me}` |
| 12 | Ending | .NET / VM | Solved (contributed, solver re-run) | `TVX{S0me_1nt2r2st1ng_t2xt_h2r2}` |
| 13 | WHAT A WASTE OF TOKENS... (3) | Crypto | Solved (contributed, solver re-run) | `TVX{Wh47_4_$4xv3efss_d39j97k}` |
| 14 | Memory dump | Forensics | Solved (contributed, not re-run) | `TVX{m3m0ry_4rt_n0t_pr0mpt_2026}` |
| 15 | GhostNote | Forensics | Solved (contributed, solver re-run) | `Tvx{7312f376b0786df4db8a8950057228fb246e5013}` |
| 16 | TraceVX | Forensics | Solved (contributed, live-verified) | `TVX{Ahmed@WIN-TRACE-01_TraceTelemetry-185.192.48.239_8MiB_411ff385}` |
| 17 | malwareX | Malware RE | Solved (uploaded writeup, Q5 verified) | `TVX{103.118.252.177:168}` |
| 18 | WHAT A WASTE OF TOKENS... | Crypto | Open | — |
| 19 | ASK ME | Stego / 7z | Open | — |

Not in this bundle: the contributed package's INDEX notes two more
challenges with no completed writeup — **phantom-trace** (objective 3
still pending the investigation-tool uid) and **malwareX** (not
delivered there; our full writeup is #17 above).

## How this bundle is organised

- `01-solved/` — one file per solved challenge: the vulnerability or
  trick, the exact steps, and the flag. Files 11–16 are summaries of
  the contributed writeups, with their provenance and verification
  status stated at the top of each file.
- `02-open/` — one file per open challenge: what was tried, what failed,
  and the next concrete check. No flag is guessed in these files.
- `solvers/` — the 6 Python solvers that reproduce the session's
  derived flags (Fourth Portal needs `pip install cryptography`).
  The contributed challenges' solvers stay in their own folders under
  `contributed/` — they read their challenge files by relative path,
  so run each from its own folder (`python3 solvers/solve_all.py`).
  Forgotten Tenant, Broken Trust and Evidence.zip have no offline
  solver — see their files.
- `evidence/` — the Chest full writeup, the Evidence.zip solve notes,
  the Forgotten Tenant `evidence.json`, the ASK ME subagent notes, and
  the malwareX writeup (verbatim, as uploaded).
- `contributed/tvx_all_writeups/` — Shikhu's uploaded package, verbatim:
  its INDEX.md plus all 7 writeup folders (WRITEUP.md + WRITEUP.pdf,
  solvers, and original challenge files).

## Notes and limits

- The three .NET reverses (SteelAndFeathers, TwistMeATwister,
  SummerIsOver) are all the same shape — an obfuscated `Reveal()` /
  `Unpack()` that unscrambles a static blob — solved by inverting the
  transform in Python rather than by running the checker. Ending is the
  same family with a full VM instead of a straight reveal.
- The Chest solve only worked once the plaintext was treated as
  **spaceless** English; every spaced model collapsed to a degenerate
  decode.
- cryptoone's lesson, twice over: never key anything from a public
  value (the shulker box decoy `TVX{tNt_g035_B00m_C0ngr4t5}`), and a
  curve is only as safe as the largest prime factor of its order
  (Pohlig–Hellman, all factors < 2²⁷).
- ASK ME: "FIOuNdIT" is verified as the message in the screenshots and
  definitively NOT the 7z password — do not retry foundit variants or
  anagrams (60,480 permutations tried, zero hits).
- Memory dump: the decoy `TVX{dont_use_ai_for_solving}` lives only in a
  `Start-Sleep` comment; the real secret is a `SESSION_AUTH_TOKEN`
  environment variable in freed RAM.
- GhostNote's flag tag is lowercase `Tvx{...}` — don't "correct" it to
  `TVX{...}`.
- malwareX is a **live malware sample** — static analysis only, never
  executed outside a sandbox. All five questions are now answered; the
  uploaded writeup is kept verbatim at `evidence/malwarex-writeup.md`.
  One correction to it: its MD5 line for the config password ends
  `...db14`, but recomputing `MD5("WTvF178FT4EyjFcV")` gives `...dbac`
  — its own derived key is built from `...dbac`, so the key is right
  and the MD5 line has a one-byte typo.
- WHAT A WASTE OF TOKENS... (the `flag.txt` one) is still open, but its
  series sibling part 3 is solved (#13) — read that file first before
  trying new ciphers on it.
