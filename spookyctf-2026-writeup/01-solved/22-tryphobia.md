# Trypophobia — Java reverse engineering

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Challenge:** Trypophobia — 75 points, author Ryan, 214 solves. "Classic reverse engineering, right?"
**Status:** Solved — flag confirmed correct by the author, 2026-11-06

## Flag (confirmed)

```
spooky{ever_reversed_java?A67b_91}
```

Note the literal `?` at position 25 — it is forced by the arithmetic, not a guess.

## Challenge

A file `binary.bin` is a Java 8 class named `binary` (1,246 bytes, SHA-256 `a5ec0f5795a92247dab4ff26311d937a6447c290e368c4859a14170237e46406`). Its `main()` takes one argument and calls a static `check(String)`. Reverse it and find the accepted input.

## Files

- `challenge-files/binary.bin` — the Java class
- `solvers/java-re/solve.py` — the per-position brute-force solver
- `solvers/java-re/emulate.py` — the JVM-stack emulator
- `solvers/java-re/disasm.py` — the disassembler

## Derivation

`check(String)` requires the input to be exactly **34 characters** long, then checks each `charAt(i)` with a two-operation obfuscation that rotates through three forms:

- `(c ^ A) + B`
- `(A - c) ^ B`
- `(c + A) ^ B`

compared against a target, with duplicate/pop no-ops mixed in. Each operation is bijective, so brute-forcing the printable ASCII range for each position independently (in a JVM-stack emulator) gives a unique solution per position.

One position is forced in an interesting way: `(31 - c) ^ 34 == -62` gives `c = 63`, which is `?`. That is why the flag contains a literal `?` at position 25.

## Verify

With a JDK, run:

```bash
java binary 'spooky{ever_reversed_java?A67b_91}'
```

Expected output: `Correct!`

## Flag (confirmed)

```
spooky{ever_reversed_java?A67b_91}
```

A complete derivation from the bytecode, confirmed correct by the author on 2026-11-07 — the author's screenshot shows this exact flag entered in the Trypophobia challenge's submission field.