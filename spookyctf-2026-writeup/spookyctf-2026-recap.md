# SpookyCTF 2026 — final board

Competition closed **2026-11-07 17:00 UTC / 22:30 IST**. This is a record of where
things stood at close. Nothing below was submitted by Muse — the platform needs
Shikhu's login, and the submission window is now shut.

## Confirmed by the platform (10)

| Challenge | Flag |
|---|---|
| Glass bottle / Denbigh asylum | `spooky{north_wales_hospital.1966}` |
| Jokes website ("EXTREME JOKE ZONE") | `spooky{th4t_w4snt_funn3h}` |
| Corn maze buffer overflow | `spooky{br4v3Se@O77er}` |
| Spooky Keystreams (AES-CTR reuse) | `spooky{cs351JKS}` |
| ELF quine | `spooky{phdr_in_ehdr_c2d021cc4fc5}` |
| SpookyTrust (P-384, d = 1963) | `spooky{4T_L345T_1T_15NT_F0UR}` |
| EYE memory forensics | `spooky{th3y_ar3_w2tch1ng}` |
| Philophobia (Sonnet 18) | `spooky{m4yb3_1_n33d_t0_10v3_mys31f}` |
| The Logical Way (Vulcan) | `spooky{vtosh_katur_nirak}` |
| Fear of math (non-associative DH) | `spooky{spooky_scary_nonassociative_diffie_hellman}` |

The fear-of-math flag was the last confirmed solve, reported by Shikhu at
2026-11-07 16:08 UTC — the bare 42-byte plaintext was rejected; the wrapped
form was accepted.

## Derived but never confirmed (unknown whether submitted before close)

These are clean derivations, not guesses, but no platform result was reported
for any of them. If Shikhu submitted any in the final half-hour before close,
that is the missing fact that settles them.

| Challenge | Derived flag |
|---|---|
| Numerophobia | `spooky{th3_4n5w3r_h45_4lw4y5_b33n_42}` |
| Demented Memories | `spooky{the_g00d_the_l0st_@ndth3_void}` (fallback with underscore before `th3`: `spooky{the_g00d_the_l0st_@nd_th3_void}`) |
| Java reverse engineering | `spooky{ever_reversed_java?A67b_91}` |
| Emilia / Bavarian hospital | `spooky{bezirkskrankenhaus_passau}` |
| NICC security dashboard | `spooky{Th3_fe3d_goe5_b07H_way$}` |
| I D0n't Feel S0 G00d | `spooky{an_apple_a_day}` (fallback `spooky{ask_your_doctor_not_me}`) |
| Graveyard letter | candidates `spooky{i_feel_like_someones_watching_me}` and `spooky{someone_is_watching_me}` — `spooky{eyes_are_watching_me}` and `spooky{the_one_you_left_behind}` were already rejected |
| Informant historical site | best guess `spooky{Wernigerode_Castle}` (fallback `spooky{Schloss_Wernigerode}`) |
| Hashphobia | only the tail is known: `...4nd_ch3ck_review5}`; six beginning guesses were given, none confirmed |

## Unsolved at close (no flag)

- Eberhardt Hall haunted music — 32-note melody, no match found
- SP00KY protocol server — flag never recovered (no solver script was provided)
- Visiobibliophobia livestream — no flag seen on any checked stream
- Hashphobia — magic word never found after 1,000,000+ probes
- fsvchall2 format string — payload verified locally, remote secret never fetched
  (`python3 ~/workspace/fsvchall2_exploit.py` was the one command left)

## Open question for Shikhu

Which of the "derived but never confirmed" flags did you actually submit before
22:30 IST, and which landed? That answer closes the record — and the tracking
items for those challenges, which are still marked active.
