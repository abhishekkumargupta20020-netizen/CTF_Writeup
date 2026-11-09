# Jokes website — "EXTREME JOKE ZONE"

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Platform-confirmed

## Flag

```
spooky{th4t_w4snt_funn3h}
```

## Challenge

A Doge-themed "EXTREME JOKE ZONE" website at `http://18.217.64.238` with a flashing rainbow background and a "Generate Joke" button. Each click loads a new joke. The flag was hidden in the joke-generation mechanism.

## Solution

**1. Observe the URL.**
Each "Generate Joke" click navigates to a Base64-encoded path. The path encodes a keyword.

**2. Decode the path.**
The decoding chain is:

```
Base64 path  →  E/e string  →  UTF-16BE keyword
```

where `E = 0` and `e = 1`. Decoding the paths from successive clicks gives ordinary keywords such as `chef`, `guitar`, and `singer`.

**3. Craft the keyword "flag".**
Instead of clicking at random, encode the keyword `flag` through the same chain (UTF-16BE → E/e bits → Base64) and request that URL directly. The page then returns the flag as the joke heading.

## Flag

```
spooky{th4t_w4snt_funn3h}
```

Submitted on the platform and accepted.
