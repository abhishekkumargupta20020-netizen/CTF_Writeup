# Steve's Lost Book — Base64 in Plain Sight

**Author:** Abhishek Kr Gupta
**Event:** TVX / TVXCTF, 2026-11-13
**Status:** Solved by derivation, NOT platform-confirmed

## Flag

```
TVXCTF{steve_found_the_hidden_chest}
```

## Challenge

File: `Steves_Lost_Book.txt`

The file contains a single string — the Enderman's "travel-safe alphabet",
which is just Base64:

```
VFZYQ1RGe3N0ZXZlX2ZvdW5kX3RoZV9oaWRkZW5fY2hlc3R9
```

## Method

Decode it:

```bash
echo 'VFZYQ1RGe3N0ZXZlX2ZvdW5kX3RoZV9oaWRkZW5fY2hlc3R9' | base64 -d
```

Output:

```
TVXCTF{steve_found_the_hidden_chest}
```

## Solver

`solvers/05-steves-lost-book-solve.py`

```bash
python3 solvers/05-steves-lost-book-solve.py
```

## Flag

```
TVXCTF{steve_found_the_hidden_chest}
```

The `TVX{steve_found_the_hidden_chest}` form is also accepted per the
user.
