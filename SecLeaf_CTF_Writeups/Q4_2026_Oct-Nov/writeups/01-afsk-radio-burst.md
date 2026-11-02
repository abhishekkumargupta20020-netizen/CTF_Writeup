# AFSK Radio Burst — Bell 202 / UART Decode

- **Competition:** SecLeaf Q4 2026
- **Date solved:** 31 October 2026
- **Category:** Signal processing / audio forensics
- **Status:** **Solved**
- **Verified flag:** `SecLeaf{R4d10_W4v35}`

## Objective

Decode a short AFSK burst embedded near the end of an audio recording.

## Recovered signal parameters

| Parameter | Value |
|---|---|
| Relevant segment | Final ~178 ms |
| Approximate start | 30.000 s |
| Symbol rate | 1200 baud |
| Mark frequency | 1200 Hz |
| Space frequency | 2200 Hz |
| Framing | UART 8N1 |
| Bit order | LSB first |
| Valid frames | 21 / 21 |

The 21 frames correspond to 21 decoded bytes. The final flag was:

```text
SecLeaf{R4d10_W4v35}
```

## 1. Signal isolation

The useful signal was not distributed evenly through the recording. The repeating high-frequency patterns near the end were the key. The final approximately 178 ms contained the burst.

Load the WAV and inspect:
- the last 200–250 ms,
- spectrogram around 1.2 kHz and 2.2 kHz,
- stable tone duration,
- bit-cell transitions.

Audacity can be used for initial visual confirmation. A Python decoder can then classify each bit cell.

## 2. AFSK interpretation

This is a Bell 202-style mark/space mapping:

- mark (1200 Hz) represents binary `1`,
- space (2200 Hz) represents binary `0`.

The decoded stream uses asynchronous serial framing:
- start bit = 0,
- 8 data bits,
- least-significant bit first,
- stop bit = 1.

The 1200-baud bit period is:

\[
T_b = \frac{1}{1200} \approx 833.33\ \mu s
\]

A frame is 10 bits, approximately 8.333 ms. Twenty-one frames occupy approximately 175 ms, consistent with the recovered burst duration.

## 3. Reproduction

Install dependencies:

```bash
python3 -m pip install numpy scipy
```

Run the included reference decoder:

```bash
python3 ../solvers/afsk_bell202_decode.py recording.wav \
  --start 30.000 \
  --duration 0.178 \
  --baud 1200 \
  --mark 1200 \
  --space 2200 \
  --count 21
```

The original WAV was not available in the recovered Library, so the included script is a configurable reference implementation and has not been independently re-run against the source recording in this archive.

## 4. Verification record

The previous solve recorded:

```text
1200 baud
1200/2200 Hz
UART 8N1
LSB-first
21/21 valid frames
```

Flag:

```text
SecLeaf{R4d10_W4v35}
```

This flag is preserved as a confirmed solve.

## 5. Lessons

- Inspect the end of the recording rather than assuming the whole audio contains the same information.
- AFSK is a frequency-to-bit mapping; it is not ordinary speech recognition.
- UART framing and LSB-first order matter.
- Validate every frame's start and stop bits before trusting decoded bytes.
