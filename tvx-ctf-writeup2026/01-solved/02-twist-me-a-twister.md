# TwistMeATwister — .NET Twisted Reveal

**Author:** Abhishek Kr Gupta
**Event:** TVX CTF, 2026-11-13
**Status:** Solved by derivation, NOT platform-confirmed

## Flag

```
TVX{Fl4ggy_fl4g_fl4g_tw15ty_tw15t_tw15t}
```

## Challenge

"Ever heard of tongue twisters? programs can twist your tongue too!!"
File: `TwistMeATwister.exe` (.NET)
SHA-256: `3b624579593b6284ce6e9c64fda59ea608a34b577df028d66b47f325fa54a966`

## Method

The checker holds a 40-byte static array at RVA `0x2130`. `Reveal()`
twists it: for each output position `i`, it takes source index
`j = (7 * i + 3) % 40`, then

```
out[i] = ROR(data[j], j % 5 + 1) ^ ((55 + 11 * j) & 0xFF)
```

Reversing that in Python — inverting the rotation and the xor, reading
the bytes in the twisted order — gives clean ASCII in `TVX{...}` form.

## Solver

`solvers/02-twist-me-solve.py`

```bash
python3 solvers/02-twist-me-solve.py
```

## Flag

```
TVX{Fl4ggy_fl4g_fl4g_tw15ty_tw15t_tw15t}
```
