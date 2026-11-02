# Gerber PCB Archive — Layer Inspection

- **Competition:** SecLeaf Q2 2026
- **Date investigated:** 24 May 2026
- **Category:** Hardware / file-format forensics
- **Artifacts:** `Files.rar`, `Chall.rar`
- **Status:** Partial; no accepted flag recovered

## 1. Archive identification

The recovered archive was a RAR5 file. The 7-Zip 25.01 extraction log reported:

```text
Type = Rar5
Physical Size = 13143
Method = v6:128K:m3
```

Extraction failed for 15 sub-items with:

```text
ERROR: Unsupported Method
```

The failures affected drill and Gerber files, including:

```text
Drill_NPTH_Through.DRL
Drill_PTH_Through.DRL
Drill_PTH_Through_Via.DRL
Gerber_BoardOutlineLayer.GKO
Gerber_BottomLayer.GBL
Gerber_BottomSolderMaskLayer.GBS
Gerber_DocumentLayer.GDL
Gerber_InnerLayer1.G1
Gerber_InnerLayer2.G2
Gerber_InnerLayer3.G3
Gerber_InnerLayer4.G4
Gerber_TopLayer.GTL
Gerber_TopPasteMaskLayer.GTP
Gerber_TopSilkscreenLayer.GTO
Gerber_TopSolderMaskLayer.GTS
```

## 2. Layer metadata

The extracted/available Gerber text showed:

```text
EasyEDA v6.5.54
2026-05-23 11:51:41
Gerber Generator version 0.2
Dimensions in millimeters
```

A common layer identifier was:

```text
d68cf33dacbd4a0ca005459ec500320f
```

`Gerber_InnerLayer2.G2` contained vector draw commands and a large amount of line geometry. `Gerber_DocumentLayer.GDL` contained filled vector paths.

## 3. Reproduction workflow

List the archive first:

```bash
7z l Files.rar
file Files.rar
```

The recorded 7-Zip build could not extract the archive's compression method. Try a RAR5-compatible extractor that supports the archive's method, preserving the original file:

```bash
unar Files.rar
```

or use a current WinRAR/compatible implementation.

Once extracted, inspect the layer set:

```bash
file Gerber_*
grep -aE 'G04|SecLeaf|flag|[A-Za-z]{4,}' Gerber_*
```

Open the full layer set together in a Gerber viewer such as `gerbv` or KiCad Gerber Viewer. Do not inspect only one copper layer: text may be on the document or silkscreen layer.

## 4. Important separation from Q4

This is the May 2026 Gerber archive investigation. It is **not** the Q4 `Gerber View` challenge that later produced the verified flag:

```text
SecLeaf{NH3_g3rB3r_v13w_}
```

The Q2 `Files.rar` work did not preserve an accepted flag.

## 5. Status

Archive contents and layer metadata were identified, but the unsupported compression prevented a complete extraction in the recorded session. No Q2 flag was confirmed.
