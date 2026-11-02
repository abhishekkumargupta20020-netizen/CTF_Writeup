# SecLeaf CTF — Q2 + Q4 Consolidated Write-up Archive

This archive separates the user's SecLeaf investigations into two event periods:

- **Q2 2026 — May 2026**
- **Q4 2026 — 31 October to 1 November 2026**

It contains individual Markdown write-ups, reproduction scripts where a defensible script can be supplied, and a small subset of source artifacts recovered from the user's Library. The 2 November update adds two confirmed reverse-engineering solves to Q4.

## Accuracy and scope

The archive is a reconstruction from previous conversation records and available files. It does **not** claim to contain every official challenge from either event. It includes the challenges and investigations that could be attributed to SecLeaf from the recovered records.

Statuses are deliberately conservative:

- **Solved / verified:** the user supplied or received a confirmed accepted flag.
- **Candidate / unverified:** a plausible value was recovered, but no acceptance response is preserved.
- **Incomplete:** investigation stopped before a flag was confirmed.
- **Attribution uncertain:** an artifact or session existed, but available evidence does not prove it belonged to SecLeaf.

### Q2 index

| Write-up | Subject | Status |
|---|---|---|
| `01-memghost.md` | Memory-dump triage and flag decoys | Candidate; not verified |
| `02-emergency-transmission.md` | Classical/Vigenère cipher attempt | Incomplete |
| `03-printable-ciphertext.md` | Repeating-key XOR / printable ciphertext | Incomplete |
| `04-jpeg-zip-polyglot.md` | JPEG with appended ZIP data | Incomplete |
| `05-svg-corrupted-vector.md` | Corrupted SVG/vector investigation | Incomplete |
| `06-backup-leak.md` | Secure Notes Portal / web enumeration | Incomplete |
| `07-gerber-archive.md` | Gerber PCB archive extraction and layer inspection | Incomplete |
| `08-unattributed-q2-artifacts.md` | `protected.zip`, `art.txt`, `Chall.rar` attribution notes | Uncertain |

### Q4 index

| Write-up | Subject | Status |
|---|---|---|
| `01-afsk-radio-burst.md` | AFSK/Bell 202 decoding | **Solved** |
| `02-gerber-view.md` | Gerber View | **Solved** |
| `03-coordinate-recovery.md` | Saleae logic capture / coordinate extraction | Candidate; not verified |
| `04-reflected-storm-pcap.md` | DNS ANY reflection PCAP | Incomplete; candidate rejected |
| `05-null-choir-reverse-engineering.md` | Custom 64-bit state machine / trace reversal | **Solved** |
| `06-reverse-engineering-udp-evidence.md` | 290 UDP packets / 52-round transform reversal | **Solved**; title not preserved |

### Attribution-uncertain appendix

`Attribution_Uncertain/archive-7z.md` records a separate encrypted-archive investigation whose SecLeaf attribution could not be confirmed. It is not counted as a SecLeaf challenge.

## Verified flags

These four Q4 flags are preserved as confirmed SecLeaf solves:

```text
SecLeaf{R4d10_W4v35}
SecLeaf{NH3_g3rB3r_v13w_}
SecLeaf{th3_ch01r_s1ng5_1n_5h4d0w_m4ch1n35!!!!!}
SecLeaf{n01s3_1n_th3_w1r35_4nd_4ft3r1m4g3s!!!!!}
```

The following are **not verified** and must not be submitted as confirmed flags:

```text
SecLeaf{1m_R3@ll_Fla9}
SecLeaf{-34.6037,-58.3816}
SecLeaf{10.0.55.200_5_reflectors}
```

The coordinate candidate was revised after the earlier `-34.6038` answer was rejected; no acceptance confirmation is preserved for the revised value. The reflected-storm candidate was rejected.

## Included solvers

- `Q2_2026_May/solvers/memghost_triage.py` — lists flag-like strings and offsets in `memory.bin`; it does not decide which candidate is accepted.
- `Q2_2026_May/solvers/extract_jpeg_zip.py` — extracts an appended ZIP from a JPEG at the recovered offset.
- `Q2_2026_May/solvers/vigenere_probe.py` — reproduces the recorded ROT13/Vigenère test, including its non-plaintext output.
- `Q4_2026_Oct-Nov/solvers/afsk_bell202_decode.py` — reference Bell 202 / UART decoder. The original WAV was not available in the recovered Library, so this is a configurable reproduction helper, not a claim that the script was re-run against the original audio.
- `Q4_2026_Oct-Nov/solvers/pcap_dns_reflection.py` — Scapy-based DNS reflection summary script for the original PCAP.

The two reverse-engineering write-ups were added from prior-session evidence. Their exact original binaries, trace/packet evidence, and solver source were not present in the recovered file set, so the write-ups distinguish confirmed findings from missing reproduction details.

## Source artifacts included

The archive includes source artifacts that were available and materialized:

- Q2: `memory.bin`, `art.txt`, `protected.zip`, `Files.rar`, `Chall.rar`
- Q4: `reflected-storm.pcap`

Other original files referenced in the investigations (for example, the JPEG carrier, SVG/vector file, AFSK WAV, Saleae `.sr` capture, and Gerber View challenge bundle) were not available in the recovered file set and are not fabricated.

## Reproduction environment

General tools used or recommended:

```bash
python3 --version
file --version
strings --version
xxd -h
binwalk --help
exiftool -ver
steghide --version
7z
tshark --version
```

Python dependencies for the included scripts:

```bash
python3 -m pip install numpy scipy scapy
```

For the Q4 coordinate capture, use Saleae Logic 2 to open the original `.sr` file and export the digital channel or decode UART. The captured sample rate was 1 GHz; the UART baud rate was not preserved in the available notes and must be inferred from the waveform rather than assumed.

## Competition separation

Do not merge unrelated HI Cyber Con / `hiCTF{...}` work into this SecLeaf archive. In particular, the `ground-station.zip` / GSC-7 offline audit and Overgrowth GraphQL investigation were identified as HI Cyber Con material, not SecLeaf Q4.
