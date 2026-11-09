# Philophobia — Sonnet 18 and an XOR key

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Platform-confirmed

## Flag

```
spooky{m4yb3_1_n33d_t0_10v3_mys31f}
```

## Challenge

An ELF binary (`philophobia.bin`, x86-64, 16,512 bytes, not stripped) prints a love poem and a heart, asks for `<start end>`, then asks for a line about "a certain famous summer day". Find the flag.

## Files

- `challenge-files/philophobia.bin` — the binary

## Solution

**1. The famous summer day.**
"A certain famous summer day" is Shakespeare's Sonnet 18, which opens:

```
Shall I compare thee to a summer's day?
```

**2. How the binary checks the input.**
The program takes `start` and `end`, then `strncmp`s 20 bytes of the input starting at offset `start` against `"Shall I compare thee"`. On a match, `print_flag` XORs a 35-byte embedded blob with a key:

```
key = (end - start) + 71
```

**3. Derive the key from the known plaintext.**
Every flag starts with `spooky{`. XORing the known plaintext `spooky{` against the start of the blob gives the key: **90**. So:

```
end - start = 90 - 71 = 19
```

**4. Run it.**
Run with `start=0`, `end=19` and the Sonnet 18 line as input:

```
Shall I compare thee to a summer's day?
```

The binary prints the flag.

## Flag

```
spooky{m4yb3_1_n33d_t0_10v3_mys31f}
```

("maybe i need to love myself".) Confirmed by running the binary.
