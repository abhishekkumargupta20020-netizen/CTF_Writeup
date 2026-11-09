# StashTheHash — crack the hash, read the red channel

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Flag recovered

## Flag

```
spooky{dleeds_isa_devil}
```

## Challenge

A `StashTheHash.zip` containing `UserAccountInfo.txt` and an encrypted `secretKnowledgeFolder.7z`. Get into the archive and find the flag.

## Files

- `challenge-files/StashTheHash.zip` — the archive bundle

## Solution

**1. Crack the password hash.**
`UserAccountInfo.txt` gives the account `dleeds` (Daniel Leeds, display name DevilLeeds) with an MD5 password hash:

```
ad7bcd7ab3cc113f496e1840bc582bbd
```

Cracking it against `rockyou.txt` gives the password:

```
newjerseydevils
```

**2. Open the 7z.**
That password unlocks `secretKnowledgeFolder.7z`, which contains `secretKnowledge.png` (700×700).

**3. Read the red-channel LSB plane.**
Plotting the red channel's least-significant-bit plane reveals the flag.

## Flag

```
spooky{dleeds_isa_devil}
```

Flag recovered during the event.
