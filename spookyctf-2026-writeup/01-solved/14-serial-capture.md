# Serial capture — the multi-language onion

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Flag recovered

## Flag

```
spooky{mu1tipl3_l@ngu@ges}
```

## Challenge

A serial log (`serial-capture.log`) with many languages and onion-like layers. Reassemble what was transferred and find the flag.

## Files

- `challenge-files/serial/image.jpg` — the reconstructed JPEG (2560×1440)
- `challenge-files/serial/file1_clean.bin` — the reconstructed Latin text
- `challenge-files/serial/communication.fun` — the extracted Steghide payload

## Solution

**1. Serial log → XMODEM.**
The log is a hex dump of XMODEM transfers: `SOH`, sequence and complement bytes, 128-byte blocks, checksum = sum mod 256 (verified on all 2,948 blocks), `EOT`, and `0x1A` padding. Reassembling the transfers yields two files:

- a 2560×1440 JPEG (377,221 bytes cleaned)
- a 133-byte Latin text file

**2. The Latin text gives the key.**
The Latin text says the key requires understanding what the image means, and that it is what they call a "supermercado". The image is a supermarket screenshot. `supermercado` (lowercase) works as the Steghide passphrase for the JPEG.

**3. Steghide → `communication.fun`.**
Extracting the embedded data gives `communication.fun` (598 bytes, rijndael-128 CBC, compressed).

**4. Hex-escaped Portuguese.**
That file is hex-escaped (`\x..`) Portuguese text. Decoding it gives the flag prefix `spooky{mu1tipl3_`, followed by decimal ASCII `108 64 110 103 117 64 103 101 115 125`, which decodes to `l@ngu@ges}`.

## Flag

```
spooky{mu1tipl3_l@ngu@ges}
```

("multiple languages".) Flag recovered during the event.
