# Chest — SOLVED

Flag: TVX{never_dig_straight_down}

## Method (different from the spaced-quadgram annealers)
1. Space test: no independent set of symbols sums to ~270 with English
   word-length gaps (best annealing set: total 194, mean loglik -3.22, gaps
   to 23). Conclusion: the plaintext has NO spaces — it is spaceless English.
2. Built a spaceless quadgram model (log10, +1 smoothing) from 10 Gutenberg
   books, spaces stripped (7.42M chars): ~/workspace/chest/quadgram_nospace_logp.bin
   Calibration: real spaceless English of 1437 chars scores ~-6000 to -6120.
3. Plain quadgram annealing collapsed to a degenerate 6-letter decode
   (e 37%, score -5937, "better" than real English) — the +1-smoothed
   quadgram model rewards using only common quadgrams and does not punish
   missing letters. Diagnosis: same flaw as the earlier solvers.
4. Fix: added a chi-square letter-frequency penalty (weight 1.0) to the
   objective in solve_nospace2 (C annealer, 39 symbols -> 26 letters).
   Seed 1 converged to total -6252.3, chi2 98 — readable English.
5. Two rare letters were misassigned by the annealer (quadgram-neutral,
   semantically forced):
   - coal (3x) -> x, not s: "pickaxe", "next", "tvx"
   - emerald (1x) -> j, not p: "joined"
   Corrected quadgram score -6166.9; segmentation 346 words, 97% in-vocab.

## Plaintext (spaceless, 1437 chars)
"It began the way every world begins with a single tree and a growing
sense of dread. I punched the oak until my knuckles ached, crafted a table
and carved a crude pickaxe before the sun slid behind the hills. By
nightfall I had dug into the side of a hill and sealed the entrance with
dirt, listening to the zombies groan outside while a skeleton rattled
somewhere above me. Morning brought coal, iron and a cave that breathed
cold air against my face. I followed the tunnel down, placing torches
behind me like breadcrumbs, until the walls glittered with redstone and
the floor gave way to a lake of lava. I bridged across with cobblestone,
one careful block at a time, and found a strange stone doorway half
buried in the gravel. The frame was missing three eyes of ender, so I
turned back and spent the next week hunting endermen across the plains,
never looking them in the eye. When I finally lit the portal, the Nether
swallowed me whole. Fortress walls rose from a sea of fire, blazes
drifted between the towers, and every bridge seemed to lead nowhere. I
lost my sword to a ghast fireball and my patience to a piglin who wanted
nothing but gold. Somewhere in that red haze I found a chest hidden
beneath the netherrack, and inside lay a book written in the old
enchanting table script. The last page held a single warning that I have
carried ever since. The old miners left their rule carved into the bedrock
beneath the first village: whoever reads this must remember the vault
phrase, because it has saved more lives than any diamond armor ever will.
The phrase is NEVER DIG STRAIGHT DOWN. Wrap it in the usual braces
behind the tag TVX, all lowercase, joined with underscores, and the vault
will open for you. Now go build something wonderful — and watch out for
the creeper behind you."

## Mapping (item -> letter)
arrow k, bedrock f, blaze_rod d, bone t, bookshelf c, cactus u,
clay_ball u, coal x, cobblestone p, diamond w, dirt o, emerald j,
end_stone e, ender_pearl n, feather v, flint m, ghast_tear g,
glowstone l, gold_ingot t, gravel h, gunpowder n, iron_ingot a,
lapis_lazuli c, melon_slice i, nether_wart r, netherrack i, oak_log c,
obsidian d, pumpkin o, redstone a, rotten_flesh e, sand e, slime_ball h,
soul_sand y, spider_eye r, stick s, string l, sugar_cane s, torch b

## Files
- solve_nospace.c / solve_nospace2 (C annealer, quadgram + chi2 penalty)
- quadgram_nospace_logp.bin (spaceless model)
- build_model_nospace.py, segment.py (word-segmentation verifier)
- decode_final.txt (corrected spaceless plaintext)
