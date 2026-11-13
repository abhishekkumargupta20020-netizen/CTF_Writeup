# chest — "DO NOT SORT" — Cryptography Writeup

## Prompt

> Deep under the first village I found a chest with a sign on it: DO NOT SORT.
> Inside, 1,437 items sit in one long row, nine slots per line. A scribbled
> note says "every item stands for a letter, but not every letter has just
> one item."
> Somebody wrote a warning in here. Find it.
> Flag format: `TVX{...}`

Supplied: `chest.txt`.

## Flag

```
TVX{never_dig_straight_down}
```

## The cipher

`chest.txt` is exactly 1,437 whitespace-separated Minecraft item names,
nine per line over 160 lines (the last line has six), with **39 distinct
items**. That is a **homophonic substitution cipher**:

- every item always stands for the same letter;
- common letters get several items (homophones), rare letters one —
  exactly what the note says;
- the plaintext is **letters only** — no spaces, no punctuation — over
  25 letters. `q` never occurs in the message, which fits a story with
  no *quick/quiet/queen* in it.

Item counts run from 70 (`sand`) down to a single occurrence
(`emerald`), tracking the frequencies of the letters they stand for
once each letter's total is summed over its items:

| Letter | Items | Letter | Items |
|---|---|---|---|
| a | iron_ingot, redstone | n | ender_pearl, gunpowder |
| b | torch | o | dirt, pumpkin |
| c | lapis_lazuli, oak_log | p | cobblestone |
| d | blaze_rod, obsidian | r | nether_wart, spider_eye |
| e | end_stone, rotten_flesh, sand | s | stick, sugar_cane |
| f | bedrock | t | bone, gold_ingot |
| g | ghast_tear | u | cactus, clay_ball |
| h | gravel, slime_ball | v | feather |
| i | melon_slice, netherrack | w | diamond |
| j | emerald | x | coal |
| k | arrow | y | soul_sand |
| l | glowstone, string | z | bookshelf |
| m | flint | | |

## How the mapping was recovered

### 1. Pattern mining

Some repeated symbol patterns are unmistakable. The trigram family

```
{bone, gold_ingot} · {gravel, slime_ball} · {sand, end_stone}
```

occurs **30 times** in all 2×2×2 = 8 combinations (5, 5, 4, 4, 4, 4, 3, 1) —
three letters, each with two homophones, spelling the commonest English
trigram: **the**, so `bone/gold_ingot = t`, `gravel/slime_ball = h`,
`sand/end_stone = e`. A second family,
`{netherrack, melon_slice, redstone} · gunpowder · ghast_tear` (9 times),
is a different common trigram whose last two letters have one item each.
And `glowstone` is followed by itself 7 times out of 43 occurrences —
a letter that doubles often, i.e. `l` ("ll").

### 2. Tetragram simulated annealing — and a lesson about the corpus

The full key was recovered by simulated annealing over item→letter
assignments, scored with English tetragram (4-gram) log-probabilities,
using incremental rescoring around the positions of the item being
changed.

The first attempt **failed completely** (best score −6.3 per tetragram,
pure gibberish), with a language model trained on local documentation
and code text. Its statistics are not English prose statistics at all —
in that corpus the commonest letter trigram is `san` (from "sandbox").
A control test confirmed the solver itself was sound: it recovered a
synthetic homophonic cipher made from that same corpus perfectly.

Rebuilding the corpus from genuine prose only — the system's man pages,
~43 MB of real sentences, where `the` is correctly the top trigram at
1.56 % and `e`/`t` the top letters — the same annealer reached
**−4.73 per tetragram** and the text simply read itself out.

### 3. Two swaps fixed by context

The annealer swapped two rare, statistically similar letters. Every
occurrence's context decides them unambiguously:

- `cactus` = **u**, not x — p**u**nched, **u**ntil, s**u**n, d**u**g,
  t**u**nnel, caref**u**l, fo**u**nd, h**u**nting, m**u**st, va**u**lt,
  **u**sual, yo**u**, wonderf**u**l.
- `coal` = **x**, not q — picka**x**e, ne**x**t, and the text's own
  "the tag t**vx**".

The singletons fall out the same way: `emerald` = **j** ("**j**oined",
its only occurrence), `bookshelf` = **z** ("**z**ombies", "bla**z**es",
"ha**z**e").

## The decoded warning

Spaces and capitals below are editorial — the original is one unspaced
string of 1,437 letters. It reads perfectly, start to finish:

> It began the way every world begins, with a single tree and a growing
> sense of dread. I punched the oak until my knuckles ached, crafted a
> table and carved a crude pickaxe, before the sun slid behind the
> hills. By nightfall I had dug into the side of a hill and sealed the
> entrance with dirt, listening to the zombies groan outside while a
> skeleton rattled somewhere above me. Morning brought coal, iron and a
> cave that breathed cold air against my face. I followed the tunnel
> down, placing torches behind me like breadcrumbs, until the walls
> glittered with redstone and the floor gave way to a lake of lava. I
> bridged across with cobblestone, one careful block at a time, and
> found a strange stone doorway half buried in the gravel. The frame
> was missing three eyes of ender, so I turned back and spent the next
> week hunting endermen across the plains, never looking them in the
> eye. When I finally lit the portal, the nether swallowed me whole.
> Fortress walls rose from a sea of fire, blazes drifted between the
> towers and every bridge seemed to lead nowhere. I lost my sword to a
> ghast fireball and my patience to a piglin who wanted nothing but
> gold. Somewhere in that red haze I found a chest hidden beneath the
> netherrack, and inside lay a book written in the old enchanting table
> script. The last page held a single warning that I have carried ever
> since. The old miners left their rule carved into the bedrock beneath
> the first village: whoever reads this must remember the vault phrase,
> because it has saved more lives than any diamond armor ever will.
> **The phrase is NEVER DIG STRAIGHT DOWN. Wrap it in the usual braces
> behind the tag TVX, all lowercase, joined with underscores, and the
> vault will open for you.** Now go build something wonderful, and
> watch out for the creeper behind you.

The message names its own flag format: the vault phrase
`neverdigstraightdown`, in braces behind the tag `TVX`, all lowercase,
joined with underscores:

```
TVX{never_dig_straight_down}
```

It is also, not coincidentally, the first rule of Minecraft.

## Solver

```
solvers/solve_01_chest.py   # this challenge, standard library only
solvers/solve_all.py        # runs every solver in the package
```

The solver carries the recovered mapping, checks it against the file
(1,437 tokens, exactly the 39 expected items), decodes the message,
extracts the vault phrase using the instructions embedded in the text
itself, and builds the flag:

```
$ python3 solvers/solve_all.py
=== solve_01_chest.py ===
[*] decoded 1437 letters (no spaces in the original):
itbeganthewayeveryworldbeginswithasingletree ... watchoutforthecreeperbehindyou

[*] vault phrase in the text: neverdigstraightdown
Flag: TVX{never_dig_straight_down}
[+] solve_01_chest.py: flag verified

1/1 challenges solved
```

Fresh-unzip test: `solve_all.py` passes **1/1**.

## Lessons

- Homophones flatten unigram frequencies, not patterns: repeated
  n-gram families (the 2×2×2 "the" block) and double letters still
  fingerprint the common letters, and 1,437 characters is far more
  than a tetragram annealer needs.
- A language model is only as good as its corpus. Trained on code and
  schema documentation, the identical solver produced confident
  gibberish; trained on real prose, it solved the cipher in seconds.
  Check your model's own statistics (`the` should be the top trigram)
  before trusting its verdicts.
- And the sign was right: sorting the chest groups the items, destroys
  the order, and the warning is gone. **Do not sort. Never dig straight
  down.**
