# Haunted portrait — blue-channel LSB

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Flag recovered

## Flag

```
spooky{portraits_keep_secrets}
```

## Challenge

A haunted portrait image (`haunted_portrait.png`). Find the hidden flag.

## Solution

**1. Rule out the easy hiding places.**
There is no trailing data after the PNG end and no useful metadata. The secret is in the pixels themselves.

**2. Check the LSB planes.**
The red and green channels' least-significant bits look random (about 50% ones). The blue channel is different: only about 3.6% ones, and the ones are confined to the portrait region. That is the signal.

**3. Read the blue-channel LSB plane.**
It reads:

```
THE PORTRAIT WHISPERS:
THE DEAD SPEAK IN ROT13
fcbbxl{cbegenvgf_xrrc_frpergf}
```

**4. ROT13.**
ROT13-decoding the last line:

```
fcbbxl{cbegenvgf_xrrc_frpergf}  →  spooky{portraits_keep_secrets}
```

## Flag

```
spooky{portraits_keep_secrets}
```

Flag recovered during the event.
