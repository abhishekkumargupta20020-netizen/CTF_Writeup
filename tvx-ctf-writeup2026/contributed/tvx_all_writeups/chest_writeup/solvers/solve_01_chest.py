#!/usr/bin/env python3
"""
chest ("DO NOT SORT") -- homophonic substitution over Minecraft items.

chest.txt holds 1,437 item tokens, nine per line (160 lines, the last
one has six).  Each distinct item (39 of them) stands for one letter,
and common letters have several items: a homophonic substitution of a
letters-only (no spaces, no punctuation) English text over 25 letters
-- every letter except 'q' occurs.

How the mapping was recovered (see WRITEUP.md for the full story):
  * pattern mining, e.g. the trigram family
        {bone, gold_ingot} {gravel, slime_ball} {sand, end_stone}
    occurs 30 times and is "the";
  * simulated annealing against a tetragram language model of real
    English prose (a corpus built from the local man pages -- an
    earlier model trained on code/documentation text failed outright,
    which is itself a useful warning about language models);
  * two symbols the annealer swapped were fixed from context:
    cactus = 'u' (punched, until, sun, dug, tunnel, careful, found,
    must, vault, usual, you, wonderful) and coal = 'x' (pickaxe,
    next, and the "tag tvx" in the text itself).

The decoded text ends with its own instructions:

    "... whoever reads this must remember the vault phrase because it
     has saved more lives than any diamond armor ever will the phrase
     is NEVERDIGSTRAIGHTDOWN wrap it in the usual braces behind the
     tag TVX all lowercase joined with underscores and the vault will
     open for you ..."

    ->  TVX{never_dig_straight_down}

Run:  python3 solve_01_chest.py [path/to/chest.txt]
"""
import os
import re
import sys

ITEM_TO_LETTER = {
    "arrow": "k",        "bedrock": "f",     "blaze_rod": "d",
    "bone": "t",         "bookshelf": "z",   "cactus": "u",
    "clay_ball": "u",    "coal": "x",        "cobblestone": "p",
    "diamond": "w",      "dirt": "o",        "emerald": "j",
    "end_stone": "e",    "ender_pearl": "n", "feather": "v",
    "flint": "m",        "ghast_tear": "g",  "glowstone": "l",
    "gold_ingot": "t",   "gravel": "h",      "gunpowder": "n",
    "iron_ingot": "a",   "lapis_lazuli": "c", "melon_slice": "i",
    "nether_wart": "r",  "netherrack": "i",  "oak_log": "c",
    "obsidian": "d",     "pumpkin": "o",     "redstone": "a",
    "rotten_flesh": "e", "sand": "e",        "slime_ball": "h",
    "soul_sand": "y",    "spider_eye": "r",  "stick": "s",
    "string": "l",       "sugar_cane": "s",  "torch": "b",
}

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "challenges", "chest.txt")
    toks = open(path).read().split()
    assert len(toks) == 1437, len(toks)
    assert set(toks) == set(ITEM_TO_LETTER), set(toks) ^ set(ITEM_TO_LETTER)

    text = "".join(ITEM_TO_LETTER[t] for t in toks)
    print(f"[*] decoded {len(text)} letters (no spaces in the original):")
    print(text)

    m = re.search(r"thephraseis([a-z]+)wrapitintheusualbracesbehindthetagtvx"
                  r"alllowercasejoinedwithunderscores", text)
    assert m, "vault-phrase instructions not found"
    phrase = m.group(1)
    print(f"\n[*] vault phrase in the text: {phrase}")
    assert phrase == "neverdigstraightdown"

    # The phrase is written as continuous words in the story; the text says
    # to join it "with underscores".  Word boundaries are the ones in the
    # sentence itself: NEVER DIG STRAIGHT DOWN.
    words = ["never", "dig", "straight", "down"]
    assert "".join(words) == phrase
    flag = "TVX{" + "_".join(words) + "}"
    print(f"Flag: {flag}")
    return flag

if __name__ == "__main__":
    main()
