# Glass bottle — Denbigh asylum

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Platform-confirmed

## Flag

```
spooky{north_wales_hospital.1966}
```

## Challenge

A glass bottle containing a Morse-code audio clip and a photograph of a building. The task was to identify the place and the year.

## Files

- `challenge-files/glassbottle.zip` — the bottle contents (audio + photograph)
- `evidence/glassbottle_morse.txt` — the decoded Morse text

## Solution

**1. Decode the Morse audio.**
The audio is Morse code at roughly 550 Hz, with a dot of about 28 ms. Decoding it gives a message about a patient in an asylum.

**2. Identify the building.**
The photograph is Denbigh, Wales, circa 1885 — the North Wales Hospital, also known as Denbigh Asylum.

**3. Pin down the year.**
The clue "educational film in Room Male 2" matches the North Wales Hospital (Denbigh Asylum) Weekly Bulletin for 21–27 May 1966, which lists for Thursday at 2 pm: "Educational Film in Male 2".

That fixes the place and the year:

- Place: North Wales Hospital (Denbigh Asylum)
- Year: 1966

## Flag

```
spooky{north_wales_hospital.1966}
```

Submitted on the platform and accepted.
