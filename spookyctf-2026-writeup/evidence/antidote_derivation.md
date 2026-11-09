# "I D0n't Feel S0 G00d" — derivation (2026-11-07, ~14:00 IST)

Challenge card (image-9.png): "I D0n't Feel S0 G00d", 458 pts, 47 solves, author inferno.
Description: arm numbers "84 53 16 8 28 16 11 6 7"; two lists (chemicals.txt, antidotes.txt);
note "Don't forget to move the neon!". Flag format spooky{antidote_here}.

## Verified facts
- Arm numbers as atomic numbers: 84 Po, 53 I, 16 S, 8 O, 28 Ni, 16 S, 11 Na, 6 C, 7 N
  -> "POISON IS NaCN" -> poison is sodium cyanide.
- chemicals.txt: 60 lines, alphabetical except Periodic Acid (#43, sorted #40).
  Sodium Cyanide is line 52 (1-based), sorted position also 52.
- antidotes.txt: 61 lines. Decode rule (verified on "4xd1n0d3" -> "antidote"):
  leet digits map directly (4=a, 3=e, 0=o, 7=t, 5=s, 6=g, 1=i/l by readability);
  letters shift back 10 (neon = element 10). All 61 lines decode to English phrases.
  Full corrected decode in workspace/antidote/fresh_eyes.txt.
- No decoded line names a real cyanide antidote. User already tried and got rejected:
  spooky{hydroxocobalamin}, spooky{sodium_thiosulfate}, spooky{sodium_nitrite},
  spooky{amyl_nitrite}.

## New checks run this session (all negative — see script output in research run)
- Arm numbers as character indices into concatenated decoded text (with/without
  underscores), raw text, and chemicals text, 0- and 1-based: gibberish
  ("lteetetot", "b_teatnot", "vd33d3d0d", ...).
- All 26 Caesar re-shifts of every decoded line and every raw line, searched for
  hydroxocobalamin / hydroxycobalamin / thiosulfate / thiosulphate / nitrite /
  cyanokit / edetate / cobalamin / vitamin / dmap / methylene / dicobalt / amyl /
  atropine / pralidoxime / kelocyanor / sulfate / cyanide / antidote: only hit is
  "antidote" itself at shift 0. No antidote name is Caesar-hidden anywhere.
- First-letter and last-letter acrostics of decoded lines under all 26 shifts:
  no keyword hits. Typo-letter strings ("rtiztie", "acclsu", etc.) under all shifts: nothing.
- image-9.png: no trailing data after IEND, no tEXt/iTXt/zTXt chunks — just the card screenshot.

## Derivation (the "don't forget" step)
- Direct index lookup fails by design: line 52 = "poison_is_bag_for_you" and
  lines 51-61 are an explicit decoy block ("flag_is_not_here",
  "this_is_not_the_flag", "nice_try_buddy", "try_harder", "barium_is_not_here",
  "you_are_not_cured"). The author blocked the naive index and its neighbourhood.
- The note "Don't forget to move the neon!" is the only instruction in the
  challenge besides the arm numbers, and "don't forget" implies a step solvers
  skip. It does double duty: the letters move back 10 to decode, AND the
  poison's position moves back 10: 52 - 10 = 42 (same direction as the letter shift).
- Line 42 = "an_apple_a_day". It is the first half of the proverb whose second
  half is line 19, "a_day_keeps_the_doctor_away" — the author split the proverb
  across the file. A joke "antidote" fits a file in which every line is a joke
  and no line is a real antidote.
- Counting check: poison is chemical #52 (1-based); 52-10=42; antidote line 42
  (1-based) = "an_apple_a_day". 0-based gives the same line (index 51-10=41 -> line 42).

## Ranked shortlist to submit, in order
1. spooky{an_apple_a_day} — the derivation above.
2. spooky{ask_your_doctor_not_me} — line 43; only if the solver counts line 1
   ("antidote") as a title/header, making entry #42 = line 43.
3. spooky{antidote_acquired} — line 2; only if the shift is +10 with wraparound (52+10=62 -> 2).
4. Real-world spelling variants, only if 1-3 all bounce (no derivation supports them):
   spooky{sodium_thiosulphate}, spooky{cyanokit}, spooky{dicobalt_edetate},
   spooky{vitamin_b12}, spooky{4_dmap}, spooky{hydroxycobalamin}.

## What would settle it
User submits #1 and reports the result. If #1 bounces, #2 is the immediate next
try (same derivation, different counting convention) — no further guessing needed
before that. If #1 and #2 both bounce, the index-shift theory is wrong and the
answer is a real-world antidote name outside the files.
