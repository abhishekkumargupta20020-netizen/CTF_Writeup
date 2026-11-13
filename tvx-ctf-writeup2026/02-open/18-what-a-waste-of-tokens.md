# WHAT A WASTE OF TOKENS... — Unsolved Crypto

**Author:** Abhishek Kr Gupta
**Event:** TVX CTF, 2026-11-13
**Status:** UNSOLVED — no flag obtained

## Challenge

TVX, Crypto, 500 pts, 0 solves, author GLITTERPUFFO.
File: `flag.txt` — hex (229 bytes) decoding to 191 uppercase letters in
5-letter groups plus a trailing `P`.

Statistics: flat IC 0.037, no repeated trigram, all 26 letters present.

## What was ruled out (all tested, do not re-run as first steps)

- Caesar / Atbash
- Vigenere / Beaufort, short key (IC scan to 60, annealer k=8, 12, 16,
  20, 24, 30, best -5.98)
- Autokey, both plaintext- and ciphertext-types, k=1–40
- Playfair (digraph doubles present)
- Bifid / Trifid, standard and keyword squares
- Hill 2x2 full brute force (best -6.24); Hill 3x3 annealer, 92M iters
  (best -6.10)
- Columnar transposition / rail fence
- Bacon (all binary partitions tested)
- Base32 / Base64 / Base26
- XOR and running-key with description / author / keyword keys
- Python random-seed keystream, seeds 0–20000
  (randint / randrange / choice / random)

Work in `~/workspace/waste-tokens/` (`analyze.py`, `hill2`, `hill3`,
`vig_anneal`, `bifid_try.py`, `cheap.py`).

## Next lead

The description hints the solve may depend on the author's OTHER crypto
challenges: "every single cryptography challenge we uploaded personally",
"these stages". Shikhu was asked 2026-11-13 whether other GLITTERPUFFO
challenges exist on the platform and for their descriptions/files — no
reply yet. That is the next step; do not keep re-running the ciphers
above.

Update: part 3 of the same series **is** now solved — see
`01-solved/13-what-a-waste-of-tokens-3-last.md`
(`TVX{Wh47_4_$4xv3efss_d39j97k}`, from `last.txt`, 38,312 tokens ->
floats -> decimal codes -> hex -> letter-pair nibbles). It is a
different file and a different flag, but it shows the series' style:
heavy layered encodings where each layer spends many symbols on few
bytes, with one plausible-looking reading that is a trap (there, the
little-endian float reading). Worth re-reading this challenge's
`flag.txt` with that lens — e.g. checking whether the 191 letters hide
a layered encoding rather than a classical cipher — before trying new
ciphers.

## Flag

None obtained. Do not fabricate one.
