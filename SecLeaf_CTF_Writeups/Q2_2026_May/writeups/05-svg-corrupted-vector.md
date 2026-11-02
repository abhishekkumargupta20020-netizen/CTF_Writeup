# Corrupted SVG / Vector Asset Investigation

- **Competition:** SecLeaf Q2 2026
- **Category:** File-format forensics / steganography
- **Status:** Incomplete; artifact attribution and final flag not preserved

## Objective

Investigate a corrupted vector asset. The prior session referred to an SVG/vector challenge, but the exact original filename, prompt, and full terminal output were not preserved.

## Known observations

- The supplied object was described as a corrupted vector asset.
- The investigation treated it as a file-format problem rather than assuming the visible rendering was the entire payload.
- No final flag or accepted submission was recorded.

## Reproduction workflow

First preserve and identify the original file:

```bash
file challenge.svg
sha256sum challenge.svg
head -c 512 challenge.svg
strings -a challenge.svg | head -n 100
```

Check XML validity and recoverable text:

```bash
xmllint --noout challenge.svg
grep -aE 'SecLeaf|flag|text|metadata|desc|title' challenge.svg
```

Inspect SVG structure:
- `<metadata>`, `<desc>`, and `<title>` elements,
- hidden or off-canvas groups,
- clipping paths and masks,
- CSS opacity / display properties,
- transforms and extreme coordinates,
- embedded raster data,
- malformed XML or truncated tags.

Render only after preserving the original:

```bash
rsvg-convert challenge.svg -o rendered.png
```

Compare the rendered result with the XML source. Hidden paths, masks, and off-canvas elements can be visible in source but not in the default rendering.

## Status and missing evidence

The original SVG itself and the exact successful/failed commands are not available in the recovered file set. No flag should be claimed. This entry is retained as an incomplete investigation rather than merged with the separate JPEG/ZIP polyglot challenge.
