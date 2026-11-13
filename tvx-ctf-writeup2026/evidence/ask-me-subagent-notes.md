# ASK ME — subagent investigation notes (2026-11-13)

## Status: UNSOLVED — no password found yet; anagram brute-force still running

## Verified facts (re-checked this session)
- Diamond counts per screenshot (1-8): [6, 9(block), 15, 53, 14, 36, 9, 20]. All re-verified
  visually at high zoom (bar_big_4.png etc.). 64+count as ASCII = "FIOuNdIT"
  (block=1 gives "FAOuNdIT").
- Test harness validated: 7z with known password "FIOuNdIT" extracts a test archive
  fine, and the same password genuinely FAILS on FLAG.7z. No harness bug.
- Item-name label "Diamond Sword" appears ONLY in img6 and img7, identical text/
  position (2512 bright pixels in label band for both, 0 in all others) — verified
  pixel-wise, not just visually.
- Bright-pixel row scan of all 8 images: only text-like bands are the hotbar and
  the img6 label. No other text, signs, or name tags anywhere in the images.
- Clouds (img1/2 sky crops) are procedural rectangles — no letters/shapes.
- Zip ASK_ME.zip: no comment; extra fields are only Unix timestamps. Creator TZ
  appears to be UTC+3 (zip times 01:28 vs file times 22:28).
- No PNG text chunks, no trailing data after IEND, LSB stego negative (parent).
- Mob catalogue (brightened): 1 none; 2 none; 3 chickens x2-3, mushrooms; 4 lava pool,
  3 fires, sheep x1-2, mushroom tree; 5 sheep/cows, distant lava glow, zombie far
  right; 6 creeper left edge x2, zombie centre-left, mushroom centre; 7 cave, no mobs,
  no ore; 8 creeper at crosshair, zombie far right, pig far left.
- Hotbar triple rotation + img8 TNT anomaly (TNT jumps from slot 2 to slot 7)
  confirmed; cyclic order of non-triple items is otherwise preserved.

## New candidates tested this session — ALL FAILED (~2,500 new, ~10,000 total incl. parent)
- try8: item position sequences as digits/letters, permutation strings (71)
- try9: FIOuNdIT/FAOuNdIT/foundit + prefixes/suffixes (432)
- try10: Minecraft vocabulary + 2-word combos, leet (1,121)
- try11: counts + selected/hand/hotbar combos (152)
- try12: selected-slot as index into counts, time/biome strings (53)
- try13: sorted counts, insertions of A/I, anagrams outfind/findout (75)
- try14: ASKME/minecraft/FIOuNdIT + numbers 0-100, 123, 2026, etc. (3,080)
- try15: letters sorted by sel/sword/varslot/hand/label/counts/time (49)
- try16: slot numbers as A1Z26 letters, e.g. sel -> ABCAAFGG (42)
- try17: case-as-Morse on FIOuNdIT ("---.-.--" all parses, incl. OAM/MNNM) (600)
- try18: hand-as-Morse (Sword=dash, TNT=dot) + day/night Morse parses (774)
- try19: French phrases (jetrouve etc.) + file-size orderings (87)
- try20: question phrases (whatistheflag, helpme, rest, opensesame...) (148)
- try21: counts as hex/octal/binary, totals in hex (26)
- try22: ASKME anagrams (makes, mask, same...) (54)
- try23: biome last letters (ahpsyter), tree first letters, mob strings (96)
- try24: youfoundit/foundtheflag/hereitis/password123 etc. (149)
- try25: base64/base32/hex/rot13 of counts and FIOuNdIT (12)
- try26: FIOuNdIT + numeric suffixes/prefixes 0-30, 42, 69, 1337... (340)
- try27: cyclic rotations of FIOuNdIT/FAOuNdIT/foundit/ifoundit (78)
- try28: TVX-style underscore phrases (i_found_it, in_plain_sight...) (240)
- Transform search (offline): add/sub/xor/mul of counts with every per-image
  modifier (sel/sword/varslot/hand/label/index/ASKME) + constants — no English
  output except FIOuNdIT itself. Binary-feature nibbles (hand/label/cross/block/
  day/sel-parity/var-parity) — no English output.

## Running: full anagram brute-force (background, started ~11:47 UTC, relaunched
## with fixed distinct output dirs after first launch clashed on shared dirs)
- /tmp/anagram_brute2.py: all unique permutations of "fioundit" (20,160) split
  over 2 workers (f0, f1) and of "faoundit" (40,320) over 2 workers (a0, a1).
- Logs: /tmp/ana_f0.log, /tmp/ana_f1.log, /tmp/ana_a0.log, /tmp/ana_a1.log.
  Output dirs test_ana_f0/f1/a0/a1 in ~/workspace/ask-me/.
- NOTE: first anagram launch (shared test_ana0/1 dirs) was unreliable due to
  dir clashes and was killed; only the relaunched run counts.

## UPDATE ~12:25 UTC — anagram brute COMPLETED, no hit
- f0/f1: all 20,160 unique permutations of "fioundit" — none.
- a0/a1: all 40,320 unique permutations of "faoundit" — none.
- Total 60,480 permutations tested, zero hits. Password is definitively NOT
  any anagram of the found letters.
- Also tested after the notes were first written: try29 other TVX flags as
  passwords (24) — FAILED; try30 Chest-derived "never_dig_straight_down" +
  variants (59) — FAILED. (Chest was solved in parallel by parent:
  TVX{never_dig_straight_down}.)

## Best remaining leads (not proven)
1. Anagram brute result (pending) — if negative, password is NOT any anagram
   of the found letters.
2. "FIOuNdIT" is too deliberate to be coincidence (diamond totals spell it),
   yet no simple form unlocks the archive. The missing step is likely a
   transformation not yet tried, OR the password is that string plus a
   component from a second feature (e.g. a word from ASK ME / biome / mob).
3. The img8 TNT jump (slot 2 -> 7) is the only break in the hotbar pattern;
   its significance is unexplained — possibly marks img8 as special, or is
   just the author selecting TNT.
4. "ASK ME" as a pun/method hint is still unresolved: tested as literal,
   anagram (MAKES/MASK/SAME), Morse-from-case, question phrases, French.
   Possibly it points at a method like "ask the image" (vision Q&A) — the
   answers to "what biome/mob/time?" give first letters TBSP/SFCR etc.,
   all tested and failed.
5. A targeted wordlist brute (Minecraft words x foundit x numbers) is the
   next brute step if the anagram run fails; ~100k candidates would need
   parallel 7z workers and ~30-60 min.

## Do NOT re-report as answers
- FIOuNdIT / FAOuNdIT / foundit / ifoundit / I FOUND IT and all case
  permutations, reversals, rotations, Morse parses, and the ~10,000
  candidates above — all verified failures against the 7z.
