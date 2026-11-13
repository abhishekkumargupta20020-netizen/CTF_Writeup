# ASK ME — Unsolved (7z Password)

**Author:** Abhishek Kr Gupta
**Event:** TVX CTF, 2026-11-13
**Status:** UNSOLVED — no flag obtained

## Challenge

A batch of Minecraft screenshots from a friend. The flag is trapped
inside a password-protected file, but the key was left in plain sight.
Hint: 'ASK ME' — check the rest of the screenshots to unlock the flag.
File: `ASK_ME.zip` — 8 screenshots (`1.png`–`8.png`) plus `FLAG.7z`
(7zAES, containing `FLAG.png`, 527,515 bytes; CRC B875E91B).

## What is verified

The diamond code is real. Sword + two diamond stacks rotate right one
slot per screenshot, wrapping in shot 8. First stack is 64 throughout;
second-stack counts are:

```
6, 9, 15, 53, 14, 36, 9, 20
```

Shot 2's second stack is a single diamond BLOCK (no count overlay) =
9 diamonds. `64 + count` as ASCII gives **"FIOuNdIT"** exactly
(70=F, 73=I, 79=O, 117=u, 78=N, 100=d, 73=I, 84=T).

## What is ruled out — do NOT retry these

"FIOuNdIT" is the message the screenshots spell, but it is **NOT** the
7z password in any straightforward form:

- All 128 case variants of "foundit", "found_it" variants,
  "iFoundIt" / "youfoundit" families
- Raw count strings ("6915531436920", "6 9 15 53 14 36 9 20",
  "6-9-15-53-14-36-9-20"), "FIOANJIT" (A1Z26 mod-26)
- A full anagram brute-force: all 20,160 permutations of "fioundit"
  and all 40,320 of "faoundit" (60,480 total) — zero hits
- ~2,700 other candidates: reversals, rotations, Morse parses of the
  case pattern, base64/hex/rot13 forms, numeric affixes, Minecraft
  vocabulary, question phrases, themed phrases
  (askme / ASK ME / please / diamond / creeper / TNT / minecraft /
  plain sight / query / question, etc.)
- LSB stego in the PNGs (whole-image RGB/RGBA, no printable hidden
  text), PNG text chunks (empty), trailing data after IEND, zip comment

The harness was validated: a test 7z with password "FIOuNdIT" extracts
fine, while the same password genuinely fails on `FLAG.7z`.

Other verified observations: "Diamond Sword" tooltip label appears only
in screenshots 6 and 7; a bright-pixel row scan found no other text,
signs, or name tags; clouds are procedural noise; the img8 TNT jump
(slot 2 → slot 7) is the only break in the hotbar rotation pattern.

## Next step — Shikhu's call

Untried angles: held/selected item per shot (sword, sword, sword, TNT,
TNT, sword, sword, TNT), scene/biome sequence (day forest → ocean
forest → swamp → lava at dusk → snowy night → night forest → cave →
creeper by the river), or a word only the friend would use.

Either ask the friend who sent the screenshots (the hint literally says
'ASK ME' — likely the intended move now the plain-sight reading is
exhausted as a password), or supply the friend's name / any word the
friend uses for one more targeted guess.

Full notes: `evidence/ask-me-subagent-notes.md`.

## Flag

None obtained. Do not fabricate one.
