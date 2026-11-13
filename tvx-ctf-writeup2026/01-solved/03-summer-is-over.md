# SummerIsOver — .NET Reveal with Schedule

**Author:** Abhishek Kr Gupta
**Event:** TVX CTF, 2026-11-13
**Status:** Solved by derivation, NOT platform-confirmed

## Flag

```
TVX{4nd_S0_7h3_5un_Sh1n35}
```

## Challenge

"When something fades away, something else comes to light."
File: `SummerIsOver.exe` (.NET)
SHA-256: `58672e593c4c216d368750552faddd243a3c98c26e45ac5e70ad365bbe560e62`

## Method

`Reveal()` works over a 26-byte blob plus an 8-byte schedule. For each
output position `i`, with `j = (5 * i + 1) % 26`:

```
v = blob[j] ^ (51 + 11 * i) ^ schedule[i % 8]
v -= (i * i * 3 + 25)
v = ROR(v, i % 5 + 1)
out[i] = v ^ (33 + 7 * i)
```

Then each 4-byte block of the output is reversed. Inverting every step
in Python unscrambles the flag — "and so the sun shines".

## Solver

`solvers/03-summer-is-over-solve.py`

```bash
python3 solvers/03-summer-is-over-solve.py
```

## Flag

```
TVX{4nd_S0_7h3_5un_Sh1n35}
```
