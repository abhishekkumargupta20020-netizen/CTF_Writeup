# Gerber View

- **Competition:** SecLeaf Q4 2026
- **Date solved:** 1 November 2026
- **Category:** Hardware / PCB design forensics
- **Status:** **Solved**
- **Verified flag:** `SecLeaf{NH3_g3rB3r_v13w_}`

## Objective

Inspect the challenge's Gerber/PCB view and recover the hidden text/flag from the board design.

## Result

The accepted flag was recorded as:

```text
SecLeaf{NH3_g3rB3r_v13w_}
```

The challenge was explicitly distinguished from the earlier May Q2 `Files.rar` Gerber archive investigation. Do not combine their evidence or claim that the Q2 archive yielded this Q4 flag.

## Reproduction workflow

The precise Q4 Gerber bundle filename and complete command transcript were not preserved in the recovered context. The confirmed result came from examining the Gerber View challenge rather than from guessing a flag from a filename.

For a fresh copy of the original challenge bundle:

1. Preserve the original archive and calculate its hash.
2. List and extract all Gerber layers.
3. Open the complete layer set in a Gerber viewer.
4. Toggle copper, silkscreen, solder-mask, outline, and document layers individually.
5. Inspect text and vector geometry at different zoom levels.
6. Check for text placed on a non-obvious layer or hidden by default visibility.
7. Submit the exact recovered string and retain the platform's acceptance response.

Suggested commands:

```bash
file challenge_bundle.zip
sha256sum challenge_bundle.zip
unzip -l challenge_bundle.zip
mkdir gerber && unzip challenge_bundle.zip -d gerber
find gerber -type f -maxdepth 2 -print
grep -aRniE 'SecLeaf|flag|Gerber|G04' gerber/
```

Open the Gerber files in `gerbv` or KiCad Gerber Viewer:

```bash
gerbv gerber/*
```

## Important evidence boundary

The flag is preserved as confirmed. The exact layer name, file hash, and final visual extraction steps are not present in the recovered records, so they are not fabricated here.

## Lessons

- Inspect all PCB layers, not only top copper.
- Silkscreen and document layers can carry visible or hidden text.
- Keep the May Q2 Gerber archive investigation separate from this Q4 solved challenge.
