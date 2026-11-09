# Diagraphephobia — a redacted Klingon PDF

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Flag recovered

## Flag

```
spooky{qaStaH_nuq}
```

## Challenge

The Federation has found a redacted file from spying on the Klingons. A one-page PDF, `Diagraphephobia.pdf`, shows a heading `Ja'` (Klingon for "tell, report") under black redaction bars, plus a glitched image. Recover what was redacted.

## Files

- `challenge-files/Diagraphephobia.pdf` — the redacted PDF

## Solution

**1. The redaction is only visual.**
Extracting the PDF text layer still gives the text hidden under the black bars: a Base64 string. (Diagraphephobia is the fear of deleting files / losing computer data — fitting the redaction theme.)

**2. The key is in the metadata.**
The PDF's Subject / description field is `lojmIt yIpoSmoH!` — Klingon for "Open the door!". It is exactly 16 characters, which makes it a valid AES-128 key.

**3. Base64-decode, then AES-128-ECB decrypt.**
Base64-decoding the hidden string and decrypting it with AES-128-ECB using the key `lojmIt yIpoSmoH!` gives Klingon plaintext beginning `nuqneH` / `DaHjaj tlhIngan yotlh...`, and the flag.

## Flag

```
spooky{qaStaH_nuq}
```

Flag recovered during the event.
