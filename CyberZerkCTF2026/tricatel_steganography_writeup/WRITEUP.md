# Tricatel — CTF Writeup

**Category: Steganography**
**Event / Series: CyberZerk — Tricatel**
**Author: Siddart (solved with Pip)**
**Date: 10 November 2026**

Four images, four different hiding places. The series is a complete tour of where data can hide in an image file — **in the pixels, in the metadata, after the file, and split in two (key inside + cipher outside)**. Same victim throughout: Marc V., and the same theme: hidden night work and burnout that the official picture does not show.

| # | Challenge | File | Hiding place | Flag |
|---|-----------|------|--------------|------|
| 1 | Marc V.'s Badge | `badge_marc_v.png` | LSB of the Blue channel | `CyberZerk{B4dg3_N0cturn3_H3ur3s_C4ch33s}` |
| 2 | Staff Directory Photo | `trombi_marc_v.jpg` | EXIF UserComment tag | `CyberZerk{M3t4d0nn33s_EXIF_B4v4rd3s}` |
| 3 | Motivational Poster | `motivation.webp` | ZIP appended after the WebP | `CyberZerk{S0ur1r3_P0ur_C4ch3r_L3_Burn0ut}` |
| 4 | Crisis Poster | `affiche_crise.png` | `tEXt` chunk key + XOR cipher after `IEND` | `CyberZerk{St3g0_Pu1s_X0R_B13n_J0u3}` |

**Package contents**

```
tricatel_steganography_writeup/
├── WRITEUP.md                  <- this file (also exported as PDF)
├── challenges/
│   ├── badge_marc_v.png        <- Challenge 1 (480x300, 12 KB)
│   ├── trombi_marc_v.jpg       <- Challenge 2 (400x300, 20 KB)
│   ├── motivation.webp         <- Challenge 3 (960x1438, 27 KB)
│   └── affiche_crise.png       <- Challenge 4 (320x200, 13 KB)
└── solvers/
    ├── solve_01_badge_lsb.py
    ├── solve_02_trombi_exif.py
    ├── solve_03_motivation_appended.py
    ├── solve_04_crise_text_xor.py
    └── solve_all.py            <- runs all 4, verified: 4/4 flags
```

Run everything (solvers 1–2 need Pillow: `pip install Pillow`; 3–4 are stdlib-only):

```bash
python3 solvers/solve_all.py
```

**A method that solves all four, in order:** (1) check metadata, (2) check file structure / chunks, (3) check for data after the logical end of file, (4) check the pixels (LSB per channel). Every challenge in this set falls to exactly one of these four checks — Challenge 4 needs two of them combined.

---

## Challenge 1 — Marc V.'s Badge (LSB)

**Category:** Steganography / LSB Steganography
**File:** `challenges/badge_marc_v.png` — PNG, 480x300, RGB, 11,908 bytes
**Prompt:** *Marc V.'s badge photo is circulating on the intranet. HR uses it to claim that he "was present." What is this image actually hiding?*

### Intuition

First, notice it is not a photo at all: it is a synthetic badge card ("TRICATEL — BADGE D'ACCÈS, Marc V., Développeur Senior, Accès: open-space / nuit, ID #8471, Zone: R&D — Bât. B") with a generic silhouette instead of a portrait. A synthetic image with no metadata is a classic LSB carrier: check the file structure first to eliminate the easy hiding places, then go to the pixels.

### Analysis

Elimination:

- PNG chunks: only `IHDR`, `IDAT`, `IEND` — no `tEXt` / `iTXt` / `zTXt`
- No EXIF / metadata (`PIL.Image.info` is empty)
- No trailing data: `IEND` ends exactly at EOF (11,908 bytes)

So the secret must be in the pixel data itself. LSB extraction — take the least significant bit of one channel, in row-major order, pack bits MSB-first into bytes — tried per channel:

| Channel | LSB stream |
|---------|-----------|
| Red | all zero / blank |
| Green | all `0xFF` / blank |
| **Blue** | **`CyberZerk{B4dg3_N0cturn3_H3ur3s_C4ch33s}`** |

The flag is the *only* printable string in the entire Blue-LSB stream. It starts at byte **2580** of that stream — bit 20640, which is pixel **row 43, column 0**: immediately below the 43-pixel blue header band. Everything before it encodes the solid header colours, which is why the Red/Green streams look constant.

Why it is invisible: flipping the last bit of a blue value changes it by at most 1 out of 255 — imperceptible, especially in the dark blue/grey palette of this badge (846 distinct colours).

### Solver

`solve_01_badge_lsb.py` — iterates all three channels so the empty ones are proven empty, extracts the Blue LSB stream, regex-extracts the flag and reports its offset.

Tools that find the same: `zsteg badge_marc_v.png` (look at the `b1,b,lsb,bY` / blue-plane lines), StegOnline, Aperi'Solve.

### Flag

```
CyberZerk{B4dg3_N0cturn3_H3ur3s_C4ch33s}
```
*"Badge Nocturne, Heures Cachées" — a night badge, hidden hours. The badge HR circulates as proof of presence is itself the carrier for the concealed night-work record.*

### Lesson

A badge graphic proves presence of a *file*, not of a *person*. And always split LSB analysis per channel and per bit plane — a combined RGB extraction of this image yields only noise (`m\xb6\xdb...` from the header), which would have missed it.

---

## Challenge 2 — Staff Directory Photo (EXIF)

**Category:** Steganography / Metadata Steganography
**File:** `challenges/trombi_marc_v.jpg` — JPEG, 400x300, RGB, 19,615 bytes
**Prompt:** *Marc V.'s photo in the HR staff directory looks ordinary. But a photo is never just an image: look at what it carries along with it.*

### Intuition

The prompt points away from the pixels: "what it carries along with it" = metadata. For JPEG that means the `APP1` Exif segment. The direct contrast with Challenge 1 is intentional — there metadata was empty and the pixels held the secret; here it is the reverse.

### Analysis

The image is a staff-directory card: Marc V., *Développeur Senior, Service: R&D / Infra, Matricule: TC-8471, Site: Tricatel — Siège, "Badge valide"*, plus a decorative barcode strip.

The file starts with a 160-byte `APP1` segment: `FFD8 FFE1 00A0 "Exif\0\0"`. Parsing it:

| EXIF tag | Value |
|----------|-------|
| `270` ImageDescription | `Trombinoscope Tricatel - Marc V.` |
| `315` Artist | `Service RH` |
| `34665` ExifOffset → Exif sub-IFD | tag `37510` below |
| **`37510` (`0x9286`) UserComment** | **`ASCII\0\0\0CyberZerk{M3t4d0nn33s_EXIF_B4v4rd3s}`** |

`UserComment` is the standard place cameras/phones store free-text notes. Its value always begins with an 8-byte character-code prefix — here `ASCII\x00\x00\x00` — and the rest is the comment, stored in **plain text**. No decoding, no encryption.

Checks that confirm nothing else is hidden: the JPEG EOI marker `FFD9` is the final byte of the file (0 trailing bytes), and a raw `strings` scan finds the flag as the only interesting string, at offset 128.

### Solver

`solve_02_trombi_exif.py` — opens the Exif IFD with Pillow, then the Exif sub-IFD via `get_ifd(0x8769)`, reads tag 37510, regex-extracts the flag. Fallback: a plain file scan, which works equally well here.

Manual equivalents:

```bash
exiftool trombi_marc_v.jpg        # look at User Comment
strings trombi_marc_v.jpg | grep CyberZerk
```

### Flag

```
CyberZerk{M3t4d0nn33s_EXIF_B4v4rd3s}
```
*"Métadonnées EXIF Bavardes" — talkative EXIF metadata.*

### Lesson

Strip metadata before publishing staff photos. Descriptions, authors, camera serials, GPS coordinates and comments travel with the image to every recipient, forever, invisibly — `exiftool -all=` before publication is a one-line fix.

---

## Challenge 3 — Motivational Poster (Appended ZIP)

**Category:** Steganography / Appended Data (file polyglot)
**File:** `challenges/motivation.webp` — WebP (VP8L lossless), 960x1438, RGBA, 27,533 bytes
**Prompt:** *HR published this motivational poster to "boost" developers before the big release. But the graphic designer, on the verge of a breakdown, discreetly concealed their true feelings in it. Look beyond appearances.*

### Intuition

"Look beyond appearances" is literal: beyond the *end* of the image. Image decoders stop at the size the format declares. Anything after that is invisible to viewers, editors and thumbnails — but trivially present in the file. Compare declared size vs. actual size.

### Analysis

The poster is the famous "KEEP CALM AND CARRY ON" in Tricatel red. Its WebP structure is one chunk:

```
RIFF header:  declared size 27,196 bytes (+8 header) = image ends at 27,204
VP8L chunk:   @12, len=27,184
Actual file:                                   27,533 bytes
Unexplained:                                      329 bytes
```

At offset **27204** — exactly where the WebP should have ended:

```
50 4B 03 04  =  "PK\x03\x04" — ZIP local file header signature
```

Extracting from that offset (a ZIP reader tolerates the prefix, so plain `unzip motivation.webp` also works):

```
journal_intime.txt  (161 bytes)
```

Contents — the designer's diary, not a bare flag:

> Je n'en peux plus. Ils nous font travailler tous les week-ends sans compensation. Voici la preuve de mon épuisement : CyberZerk{S0ur1r3_P0ur_C4ch3r_L3_Burn0ut}

*"I can't take it anymore. They make us work every weekend with no compensation. Here is the proof of my exhaustion."*

### Solver

`solve_03_motivation_appended.py` — stdlib only. Reads the RIFF size field, locates `PK\x03\x04`, opens the trailing bytes with `zipfile`, prints the contained file and extracts the flag.

Manual equivalents: `binwalk -e motivation.webp`, `dd if=motivation.webp bs=1 skip=27204 of=out.zip`, or just `unzip`.

### Flag

```
CyberZerk{S0ur1r3_P0ur_C4ch3r_L3_Burn0ut}
```
*"Sourire Pour Cacher Le Burnout" — smiling to hide burnout, which is exactly what a motivational poster is doing here.*

### Lesson

A file's *format* size and its *file system* size are two different numbers, and their difference is a hiding place. Polyglots (image+ZIP is valid for both parsers) defeat any review that only opens the file in a viewer.

---

## Challenge 4 — Crisis Poster (tEXt Key + Appended XOR)

**Category:** Steganography + Cryptography
**File:** `challenges/affiche_crise.png` — PNG, 320x200, RGB, 13,091 bytes
**Prompt:** *A "crisis management" poster is circulating. It hides two things: a key, neatly tucked inside the image, and a message, appended right after. One is used to read the other.*

### Intuition

The prompt gives the architecture away: find (a) a key *inside* the image structure — for PNG, that means a chunk, most likely `tEXt` — and (b) a message *after* the image — bytes after `IEND`. Then figure out the cipher that combines them. A short key + a binary blob of exactly flag length points to repeating-key XOR, the CTF default.

### Analysis

The poster: "PLAN DE GESTION DE CRISE — TRICATEL, Procédure interne: 1. Isoler le périmètre concerné, 2. Prévenir la cellule de crise, 3. Ne communiquer qu'après validation, 4. Journaliser chaque décision, 5. Debrief dans les 48h — Confidentiel, diffusion interne uniquement."

PNG chunk walk:

```
@ 8     IHDR  len=13
@ 33    tEXt  len=20        <- the key, inside
@ 65    IDAT  len=12,967
@ 13044 IEND  len=0         <- image ends at 13,056
file size                   <- 13,091 bytes: 35 bytes appended
```

**Part 1 — the key (inside).** A `tEXt` chunk is `keyword + \x00 + text`, stored in clear:

```
cle \x00 Y3IxczMtdGMyNg==
```

`cle` is French for "key". Its value is Base64:

```python
base64.b64decode("Y3IxczMtdGMyNg==")   # -> b'cr1s3-tc26'  (10 bytes)
```

**Part 2 — the message (appended).** 35 bytes of raw binary after `IEND`, not a file (no signature), visibly non-printable:

```
200b531641771111594d3006021403722416
03453c2a01216c6f45505c69294244404e
```

**Part 3 — one reads the other.** Repeating-key XOR:

```python
key    = b'cr1s3-tc26'
cipher = <35 appended bytes>
plain  = bytes(b ^ key[i % len(key)] for i, b in enumerate(cipher))
# -> b'CyberZerk{St3g0_Pu1s_X0R_B13n_J0u3}'
```

Verification is instant and does not need a guess-check loop: `0x20 ^ 'c' = 'C'`, `0x0B ^ 'r' = 'y'`, `0x53 ^ '1' = 'b'`… it spells `CyberZerk{` from byte 0. Lengths corroborate: 35 cipher bytes = 35 flag characters, key cycles 3.5 times.

### Solver

`solve_04_crise_text_xor.py` — stdlib only. Walks the PNG chunks, extracts and Base64-decodes the `tEXt` value, slices everything after `IEND`, XOR-decrypts and extracts the flag, printing each intermediate so both halves are auditable.

### Flag

```
CyberZerk{St3g0_Pu1s_X0R_B13n_J0u3}
```
*"Stego Puis XOR Bien Joué" — stego then XOR, well played. It names its own construction.*

### Lesson

Splitting a secret into two hiding places does not make it safe if both travel in the same file. And repeating-key XOR with a 10-byte key recovered from the same container is obfuscation, not encryption — a known plaintext (`CyberZerk{`) alone would have recovered the key even without the `tEXt` chunk.

---

## Synthesis — One Image, Four Hiding Places

```
                    ┌── PIXELS ............ LSB (Blue) ......... Ch. 1
  an image file ────┼── METADATA .......... EXIF UserComment ... Ch. 2
                    ├── FILE STRUCTURE .... PNG tEXt chunk ..... Ch. 4 (key)
                    └── AFTER THE FILE .... appended ZIP / XOR . Ch. 3, Ch. 4 (message)
```

Checklist used for every challenge, and reusable on any image:

1. `file`, size, dimensions; open it — note what it *claims* to be (here: often not even a real photo)
2. Metadata: `exiftool`, `strings`
3. Structure: PNG chunks / JPEG segments / RIFF size vs. actual size
4. Trailing data: bytes after `IEND` / EOI / declared RIFF end
5. Pixels: LSB per channel, per bit plane (`zsteg`, manual extraction)
6. If two artefacts appear (key + blob), try XOR first, then Base64 / common ciphers

## Summary of Flags

```
1. CyberZerk{B4dg3_N0cturn3_H3ur3s_C4ch33s}
2. CyberZerk{M3t4d0nn33s_EXIF_B4v4rd3s}
3. CyberZerk{S0ur1r3_P0ur_C4ch3r_L3_Burn0ut}
4. CyberZerk{St3g0_Pu1s_X0R_B13n_J0u3}
```

## Tools Used

- Python 3 + Pillow for pixel/EXIF work; standard library only (`struct`, `base64`, `zipfile`, `re`) for structure, appended-data and XOR work
- Equivalent CLI tools noted per challenge: `zsteg`, `exiftool`, `strings`, `binwalk`, `unzip`

*All four solvers were executed against the original challenge files and produce the four flags above (4/4).*
