# The Logical Way — a message in Vulcan

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Platform-confirmed

## Flag

```
spooky{vtosh_katur_nirak}
```

## Challenge

A file `My_Message_to_you.7z` (7zAES-encrypted; password `LOGIC`) contains `My Message to you.zip`, which holds `LOGIC.pdf` — a 2-page Google Docs PDF with no extractable text, only 177 glyphs in the Vulcan script. Decode the message and find the flag.

## Files

- `challenge-files/My_Message_to_you.7z` — the encrypted archive
- `evidence/decoded_message.txt` — the decoded English text

## Solution

**1. Unpack.**
Decrypt the 7z with password `LOGIC`, unzip the inner zip, and open `LOGIC.pdf`.

**2. Read the Vulcan glyphs.**
The PDF contains 177 Vulcan-script glyphs. Each glyph matches dCode's Vulcan alphabet images exactly (diff 0.0), and the PDF's Alt text independently gives the identical 177-letter string. Two independent reads agree, so the transcription is solid.

**3. Translate.**
Decoded, the message reads:

> Those who do not follow the principles of Vulcan logic will fail. V'tosh ka'tur, Nirak, do not pity those who do not follow logic. Help them see reason.

With the meta instruction: "Turn the Vulcan into English and wrap it with underscores to see reason."

**4. Pick the flag.**
`Nirak` is Vulcan for "fool"; `V'tosh ka'tur` means "Vulcans without logic". Those are the only non-English (Vulcan) words in the decoded text. Wrapping them with underscores gives the flag.

## Flag

```
spooky{vtosh_katur_nirak}
```

Submitted on the platform and accepted.

## Rejected before the solve

Several whole-message and whole-text variants, `spooky{help_them_see_reason}`, and `spooky{see_reason}` were all rejected before the Vulcan-words reading landed.
