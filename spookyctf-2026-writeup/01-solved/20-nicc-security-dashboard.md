# NICC — the security-guard dashboard

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Solved — flag confirmed correct by the author, 2026-11-06

## Flag

```
spooky{Th3_fe3d_goe5_b07H_way$}
```

Note the capital `T` and `H`, and the `$` before the closing brace.

## Challenge

A security-guard dashboard, NICC (Network Imaging Control Center), at `http://18.189.35.130/`. Follow the camera feeds and read the flag.

## Files

- `challenge-files/nicc/flag_crop.png` — the cropped, zoomed flag frame

## Derivation

The chain is found by following one HTML comment / wall text into the next feed:

1. **Homepage** — comments point to a legacy camera still registered: CAM-07.
2. **`/feeds/legacy/cam-07`** (East Stairwell) — the wall reads "SERVICE CORRIDOR - SC-12" and a comment gives the service camera directory: `/feeds/service/`.
3. **`/feeds/service/sc-12`** (Service Corridor) — the wall reads "MIRROR DOWNLINK: CAM 19" and a comment gives the redundant imaging namespace: `/feeds/mirror/`.
4. **`/feeds/mirror/cam-19`** (Network Operations) — the wall reads "SUB LEVEL B - SLB-04" and a comment says sublevel imaging uses a three-letter directory alongside the other feeds.
5. **`/feeds/sub/slb-04`** (CAM 04 — Sublevel B) — a data-timed reveal: a first frame at 3.5 s, then a cryptid frame that holds.

The flag is painted on the floor in that final feed, verified by a cropped zoom (`challenge-files/nicc/flag_crop.png`).

## Flag (confirmed)

```
spooky{Th3_fe3d_goe5_b07H_way$}
```

("the feed goes both ways".) A complete derivation from the live feeds, and the author confirmed on 2026-11-09 that this flag is correct.