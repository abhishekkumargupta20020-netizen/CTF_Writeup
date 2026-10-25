# CTF Writeup: Frequency-Domain Audio Steganography

## Challenge Information

- **Category:** Audio Forensics / Steganography
- **Artifact:** `recording.wav`
- **Flag format:** `ctf7{...}`
- **Candidate flag:** `ctf7{fr3qu3ncy_d0m41n_s3cr3ts}`

## 1. Challenge Description

The challenge provides an audio recording that sounds like an ordinary ambient tone. The description warns that examining the amplitude waveform or using a default spectrogram will not be sufficient.

This suggests that the hidden information may be encoded in the recording's frequency content rather than in its audible amplitude pattern.

The objective is to inspect the signal precisely, identify any structured frequency patterns, and reconstruct the hidden message.

## 2. Initial File Inspection

The recording is a mono, uncompressed PCM WAV file with these properties:

| Property | Value |
|---|---|
| Duration | 9 seconds |
| Sample rate | 44,100 Hz |
| Channels | 1 |
| Sample format | 16-bit PCM |

These properties can be verified with Python:

```python
import wave

with wave.open("recording.wav", "rb") as audio:
    print("Channels:", audio.getnchannels())
    print("Sample rate:", audio.getframerate())
    print("Sample width:", audio.getsampwidth())
    print("Frames:", audio.getnframes())
    print("Duration:", audio.getnframes() / audio.getframerate())
```

## 3. Why a Waveform Is Not Enough

An amplitude waveform displays how the signal's amplitude changes over time. It is useful for identifying silence, pulses, clipping, and changes in loudness, but it does not directly reveal which frequencies are present.

For this challenge, frequency-domain analysis is more informative.

The Fast Fourier Transform (FFT) converts a signal segment into its frequency components. A spectrogram then shows how those components vary over time.

## 4. Frequency Analysis

The recording can be analyzed using Python and SciPy:

```python
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

audio, sample_rate = sf.read("recording.wav")

frequencies, times, power = spectrogram(
    audio,
    fs=sample_rate,
    nperseg=8192,
    noverlap=6144
)

plt.figure(figsize=(14, 6))
plt.pcolormesh(
    times,
    frequencies,
    10 * np.log10(power + 1e-12),
    shading="auto"
)
plt.ylim(1500, 5500)
plt.xlabel("Time (seconds)")
plt.ylabel("Frequency (Hz)")
plt.title("Frequency-Domain Analysis of recording.wav")
plt.colorbar(label="Power (dB)")
plt.tight_layout()
plt.show()
```

The frequency spectrum contains prominent components around 2–5 kHz. Several peaks are close to multiples of a 200 Hz spacing, which is a useful lead for further analysis.

However, these observations alone do not establish the encoding scheme. The next step is to determine whether the frequencies represent symbols, whether they change at consistent time boundaries, and how those symbols map to bytes.

## 5. Recovering the Encoded Message

A reproducible solution must establish the following:

1. Identify stable tone intervals and measure their dominant frequencies.
2. Determine the spacing between valid frequency symbols.
3. Establish the mapping from each frequency to a symbol or numeric value.
4. Recover the symbol sequence while preserving repetitions and ordering.
5. Group symbols into bytes if the evidence supports a hexadecimal or other byte-based encoding.
6. Decode the resulting bytes and check whether the output contains a valid flag.

Do not assume that every spectral peak represents a separate symbol. Harmonics, background tones, and transitions between symbols can produce additional peaks.

## 6. Flag

The candidate flag previously identified for this challenge is:

```text
ctf7{fr3qu3ncy_d0m41n_s3cr3ts}
```

**Verification status:** The candidate has not yet been independently reproduced from the audio with a complete, documented frequency-to-symbol mapping. It should be confirmed before being reported as a verified solution.

## 7. Key Takeaway

The central lesson is that audio steganography can encode information in properties other than amplitude. Frequency analysis can expose structured patterns that are difficult to notice by listening alone.

A reliable solution requires more than finding suspicious frequencies: it must also explain the symbol mapping, reconstruct the message deterministically, and validate the final flag against the original recording.
