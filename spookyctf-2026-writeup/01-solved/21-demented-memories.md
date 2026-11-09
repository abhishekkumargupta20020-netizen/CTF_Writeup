# Demented Memories — three fragments of the past

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Solved — flag confirmed correct by the author, 2026-11-06

## Flag (confirmed)

```
spooky{the_g00d_the_l0st_@nd_th3_void}
```

Challenge

750 points, author cyb3r\_s1lv@. "My memories are leaving me... help me recover my fragmented parts of the past." The file `forgotten-playground.7z` is a git repository. The flag is split into three numbered fragments.

## Files

- `challenge-files/forgotten-playground.7z` — the git repo
- `evidence/` — see the repo itself for the fragments

## Derivation

**Fragment 1 —&#32;`spooky{the_g00d_`**
A comment in `retrospective.c`, deleted in the final "MEMORY WIPE INITIALIZATION" commit. Recovered from the git history.

**Fragment 2 —&#32;`the_l0st_@nd`**
A hidden file `.fog61.fog`, hex-decoded. The "61" in `.git/errored_space.txt` points to it. The other 70 `.fog` files and the 80 hashes in `fog.fog` are random decoys — none decode to text, and none are MD5s of single characters.

**Fragment 3 —&#32;`th3_void}`**
In `.git/errored_space.txt` itself.

**The image is a red herring.**
`the_golden_age.jpg` is just a 2010s nostalgia collage (Nyan Cat, Minecraft, Bieber, Adventure Time, Angry Birds, PewDiePie) — no LSB, EXIF, or trailing data.

## Flag 

Direct concatenation of the three fragments gives `spooky{the_g00d_the_l0st_@ndth3_void}`, but the confirmed flag has an underscore inserted between `@nd` and `th3`:

```
spooky{the_g00d_the_l0st_@nd_th3_void}
```

("the good, the lost and the void".) Confirmed correct by the author on 2026-11-06, and independently given in this form by both external writeups that cover the challenge.