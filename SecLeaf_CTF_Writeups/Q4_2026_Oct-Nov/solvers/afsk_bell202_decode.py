#!/usr/bin/env python3
"""
Reference Bell 202 AFSK / UART 8N1 decoder.

This is a configurable reproduction helper. It was not validated against the
original WAV because that recording was not present in the recovered files.
Assumptions from the solve notes:
  mark=1200 Hz -> bit 1
  space=2200 Hz -> bit 0
  baud=1200
  UART 8N1, LSB-first
"""
import argparse
import numpy as np
from scipy.io import wavfile

def mono_float(data):
    if data.ndim == 2:
        data = data.astype(np.float64).mean(axis=1)
    else:
        data = data.astype(np.float64)
    peak = np.max(np.abs(data)) or 1.0
    return data / peak

def tone_score(x, fs, freq):
    n = np.arange(len(x), dtype=np.float64)
    w = np.hanning(len(x))
    y = x * w
    phase = 2.0 * np.pi * freq * n / fs
    c = np.dot(y, np.cos(phase))
    s = np.dot(y, np.sin(phase))
    return c*c + s*s

def classify_bits(x, fs, start, baud, mark, space, count):
    spb = fs / baud
    bits = []
    for i in range(count):
        a = int(round(start + i * spb))
        b = int(round(start + (i + 1) * spb))
        if b > len(x) or b - a < 8:
            break
        cell = x[a:b]
        bits.append(1 if tone_score(cell, fs, mark) >= tone_score(cell, fs, space) else 0)
    return bits

def parse_uart(bits, max_frames=None):
    out = []
    i = 0
    while i + 10 <= len(bits):
        if bits[i] != 0:  # start bit
            i += 1
            continue
        frame = bits[i:i+10]
        if frame[9] != 1:  # stop bit
            i += 1
            continue
        value = sum(frame[1+j] << j for j in range(8))
        out.append(value)
        i += 10
        if max_frames and len(out) >= max_frames:
            break
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--start", type=float, default=30.0, help="burst start in seconds")
    ap.add_argument("--duration", type=float, default=0.178)
    ap.add_argument("--baud", type=float, default=1200)
    ap.add_argument("--mark", type=float, default=1200)
    ap.add_argument("--space", type=float, default=2200)
    ap.add_argument("--count", type=int, default=21)
    ap.add_argument("--offset-scan-ms", type=float, default=0.8,
                    help="scan start offset from 0 to this many milliseconds")
    ap.add_argument("--offset-steps", type=int, default=17)
    args = ap.parse_args()

    fs, raw = wavfile.read(args.wav)
    x = mono_float(raw)
    begin = int(args.start * fs)
    end = min(len(x), int((args.start + args.duration) * fs))
    segment = x[begin:end]
    if len(segment) == 0:
        raise SystemExit("Selected segment is empty; check --start and --duration")

    best = None
    offsets = np.linspace(0, args.offset_scan_ms / 1000.0, args.offset_steps)
    for off in offsets:
        bits = classify_bits(segment, fs, off * fs, args.baud, args.mark, args.space,
                             int(args.duration * args.baud) + 4)
        data = parse_uart(bits, args.count)
        printable = sum(32 <= b < 127 for b in data)
        valid = len(data)
        score = (valid, printable)
        if best is None or score > best[0]:
            best = (score, off, bits, data)

    (_, _), off, bits, data = best
    raw_bytes = bytes(data)
    print(f"sample_rate={fs} Hz")
    print(f"decoded_frames={len(data)} / {args.count}")
    print(f"sample_offset={off*1000:.4f} ms")
    print("hex:", raw_bytes.hex())
    print("ascii:", raw_bytes.decode("ascii", "replace"))
    print("bytes:", repr(raw_bytes))

if __name__ == "__main__":
    main()
