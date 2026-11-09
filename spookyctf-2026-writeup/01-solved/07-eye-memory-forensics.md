# EYE — "someone is watching" memory forensics

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Platform-confirmed

## Flag

```
spooky{th3y_ar3_w2tch1ng}
```

## Challenge

A user is paranoid that someone is watching them and taking pictures through their computer. The evidence is a memory capture, `spooked2_working.lime`, from a Kali Linux 7.1.5 machine (LiME image). Find the flag.

## Files

- `spooked2.lime` — the memory image, 1,073,278,016 bytes (SHA-256 `cc89dd1b0799b1f4acde678d913e38e8c1f90e7575323d15c70d7ffe561b664e`). **Not included in this zip** because of its size; see the README.
- `solvers/eye-forensics/carve.py` — the carving script
- `evidence/carve_log.txt` — the carving log

## Solution

**1. Carve the webcam photos.**
Carving the image for embedded JPEG/PNG data recovers webcam photos. In one of them a person is holding a piece of paper that reads:

```
w2tch1ng}
```

That is the tail of the flag.

**2. Find the beginning in the spy program's strings.**
Searching the memory image's strings for the spy program — a program called "eye see you" that grabs webcam frames and screenshots (saving them to `screenshots/latest_screenshot_<timestamp>`) — finds the string constant:

```
spooky{th3y_ar3_
```

at offsets 578,695,889 and 578,695,960.

**3. Join the halves.**
The two halves never appear joined in memory; the tail exists only in the photos. Joining them gives the flag:

```
spooky{th3y_ar3_w2tch1ng}
```

("they are watching".)

## Dead ends

- The 1920×922 screenshot and other large PNGs were fragmented and unrecoverable by naive carving.
- Volatility `pslist` was blocked — there is no ISF profile for the Kali 7.1.5 kernel.

Neither was needed: the photos plus the program strings were enough.

## Flag

```
spooky{th3y_ar3_w2tch1ng}
```

Submitted on the platform and accepted. A 4-page PDF writeup of this solve was also produced during the event.
