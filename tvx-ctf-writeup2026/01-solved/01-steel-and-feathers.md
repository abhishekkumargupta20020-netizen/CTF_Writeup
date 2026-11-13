# SteelAndFeathers — .NET Stack VM

**Author:** Abhishek Kr Gupta
**Event:** TVX CTF, 2026-11-13
**Status:** Solved by derivation, NOT platform-confirmed

## Flag

```
TVX{Congratulations_You_Know_Some_ball}
```

## Challenge

"What's Heavier A kilogram of steel Or a Kilogram of feathers?, Or A Flag?"
File: `SteelAndFeathers.exe` (.NET)
SHA-256: `5c6d5092ec8421c18fa73ec4ac21783d547520579bd08fe4b8f6835eab99ee98`
Flag format: `TVX{...}`

## Method

The exe is a .NET checker. `Unpack()` base64 + gzip-decodes an embedded
blob, then unscrambles it per byte:

```
byte[i] = ROR(byte[i], i % 7 + 1) ^ (23 + i * 41)
```

That gives a stack-VM program. `Run()` executes it — instructions are
push / xor / add / rol / store / load / output, halt `0xFF` — and its
output is the string `Main()` compares the input against. Running the VM
in the solver consumes all 1288 VM bytes and prints the flag.

## Solver

`solvers/01-steel-and-feathers-solve.py`

```bash
python3 solvers/01-steel-and-feathers-solve.py
```

## Flag

```
TVX{Congratulations_You_Know_Some_ball}
```

(Both weigh the same, by the way.)
