# Coordinate Recovery — Saleae Logic Capture

- **Competition:** SecLeaf Q4 2026
- **Category:** Hardware / digital-signal forensics / geolocation
- **Status:** Candidate revised after rejection; final acceptance not preserved

## Objective

Recover a geographic coordinate from a digital signal capture. The required format was:

```text
SecLeaf{latitude,longitude}
```

with four decimal places.

## Artifact notes

The challenge bundle included a Saleae Logic capture:

```text
Chall-0.sr
```

Recovered context described:
- one digital channel,
- sample rate: 1 GHz,
- likely UART/NMEA-style serial data,
- coordinate extraction as the intended direction.

The exact `.sr` file was not present in the recovered Library, so the raw waveform cannot be re-decoded from this archive.

## 1. Open and export the capture

Open `Chall-0.sr` in Saleae Logic 2. Inspect the digital channel and identify:
- idle polarity,
- bit timing,
- start/stop bits,
- repeated frame boundaries,
- ASCII-like serial payload.

If the capture is UART, use the Logic 2 Async Serial analyzer. Do not assume the baud rate; estimate it from the shortest stable bit width and validate against frame structure.

Export the digital channel or decoded analyzer data for independent parsing.

## 2. NMEA possibility

The prior analysis considered GPS/NMEA as a likely format. If the decoded payload contains NMEA sentences, inspect common coordinate-bearing messages such as `$GPRMC` and `$GPGGA`.

For NMEA degrees/minutes conversion:

\[
\text{decimal degrees} = \text{degrees} + \frac{\text{minutes}}{60}
\]

Apply the N/S and E/W hemisphere signs after conversion.

## 3. Candidate history

The first coordinate submitted was rejected:

```text
SecLeaf{-34.6038,-58.3816}
```

The answer was then revised to:

```text
SecLeaf{-34.6037,-58.3816}
```

No successful acceptance response for the revised candidate is preserved. Therefore, the revised coordinate remains **unverified** in this archive.

## 4. Reproduction checklist

- Recover the original `Chall-0.sr`.
- Open it in Logic 2.
- Determine UART baud and polarity from the waveform.
- Decode the complete serial stream.
- Validate any NMEA checksums if present.
- Convert coordinates to decimal degrees.
- Round to exactly four decimal places.
- Submit and retain the acceptance response.

## 5. Status

Do not mark this challenge solved based only on the revised coordinate. The exact `.sr` artifact and final platform confirmation are required.
