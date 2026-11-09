# Eberhardt Hall — Phasmophobia (haunted music)

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026

`FLAG`

`spooky{OOOGABOOGABOOGABOOspoopedBOOgotyou}`

## Challenge

Eberhardt Hall (NJIT) feels haunted near Halloween: eerie haunted-house music, whispering, a portrait that seems to shift, a ghost wearing a laurel. The evidence is a portrait (`ebersecret__1.jpg`) and an audio file (`PhasmophobiaChallenge__1.wav`).

## Files

- `challenge-files/ebersecret__1.jpg` — the portrait
- `challenge-files/PhasmophobiaChallenge__1.wav` — the audio
- `solvers/phasmo/make_clips.py`, `solvers/phasmo/run_whisper.py` — analysis scripts

## The reported solve

The audio’s spectrogram text is part 1, and the PNG’s hidden message (which is even labeled “(2)”) is part 2. Joining them in that order inside `spooky{}` gives:

**`spooky{OOOGABOOGABOOGABOOspoopedBOOgotyou}`**

- **Part 1 (audio):** `WWWOIJWWOIJWWOIJWWaxwwxml` decoded with Caesar shift 18 is `OOOGABOOGABOOGABOOspooped`.
- **Part 2 (PNG):** the LSB message `JWWowbgwc` decoded with the same shift is `BOOgotyou`.

The decoded spelling and capitalization are preserved as-is. If the platform rejects it, the likeliest tweaks are:

- With an underscore between the parts: `spooky{OOOGABOOGABOOGABOOspooped_BOOgotyou}`
- All lowercase: `spooky{ooogaboogaboogaboospoopedboogotyou}`

## What the author tried first (and why it missed)

The audio was analysed as a melody, not as a picture:

- The audio is a 32-note melody, all naturals — fast section A4–E4–E3–B4 repeated ×4, slow section A4–B4–D5–C5 repeated ×2.
- **Speech:** three speech engines agree — there is no spoken message in the audio, forward or reversed.
- **LSB / stego in the audio:** no hidden data found.
- **Für Elise:** edit distance 22/32 — not a match. **Phasmophobia's "Adrift":** wrong key.
- **Melody identification:** no match in a 1,861-file classical corpus or in \~30 known tunes.
- **Note-letter encodings:** all gibberish.
- **Steghide on the portrait:** passwords `adrift`, `Adrift`, `musicbox`, `lavender`, and others all failed.

The miss was looking at the audio as sound (notes, speech, melody) instead of looking at it as an image: the text was drawn in the spectrogram's upper frequencies, and the second half was in the portrait's least-significant bit plane, not under a steghide password.

## 