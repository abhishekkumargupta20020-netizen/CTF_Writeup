# Tricatel — CTF Writeup

**Category: Forensics**
**Event / Series: CyberZerk — Tricatel**
**Author: Siddart (solved with Pip)**
**Date: 10 November 2026**

A single storyline links all four challenges: Tricatel, night of **13 November 2026**, a confidential HR file, burnout / sick-leave surveillance, and one external attacker IP that keeps coming back — `45.83.12.207` (`mail-cheap-relay.ru`).

| # | Challenge | File | Technique | Flag |
|---|-----------|------|-----------|------|
| 1 | The HR Director's Note | `note_du_drh.eml` | Email forensics, SPF/DKIM/DMARC, Base64 | `CyberZerk{M4il_Sp00f3_P0ur_Surv31ll3r_L3s_Arr3ts}` |
| 2 | Night Exfiltration — Intranet Log | `access.log` | Log analysis, anomaly hunting, URL decoding | `CyberZerk{L0g_4n4lys3_Exf1l_C0nf1rm33}` |
| 3 | Calls for Help / Farewell Message | `appels_a_l_aide.pcap` | Network forensics, PCAP / TCP stream | `CyberZerk{Exf1ltr4t10n_HTTP_D3s3sp01r}` |
| 4 | Removed Secret | `depot_intranet.tgz` | Git forensics, history archaeology | `CyberZerk{G1t_N0ubl13_J4m41s_R13n_Du_P4ss3}` |

**Package contents**

```
tricatel_forensic_writeup/
├── WRITEUP.md                  <- this file (also exported as PDF)
├── challenges/
│   ├── note_du_drh.eml         <- Challenge 1 (1.9 KB)
│   ├── access.log              <- Challenge 2 (13 KB, 121 lines)
│   ├── appels_a_l_aide.pcap    <- Challenge 3 (1.5 KB, 12 packets)
│   └── depot_intranet.tgz      <- Challenge 4 (14 KB, Git repo)
└── solvers/
    ├── solve_01_email.py
    ├── solve_02_access_log.py
    ├── solve_03_pcap.py
    ├── solve_04_git.py
    └── solve_all.py            <- runs all 4, verified: 4/4 flags
```

Run everything:

```bash
python3 solvers/solve_all.py
# or individually, e.g.
python3 solvers/solve_01_email.py challenges/note_du_drh.eml
```

---

## Challenge 1 — The HR Director's Note

**Category:** Forensics / Email Forensics
**File:** `challenges/note_du_drh.eml`
**Prompt:** *An internal email from the HR Director is being forwarded, which he claims is "authentic." The employees swear they never sent it. Prove where it really comes from and what it is hiding.*

### Intuition

Never trust the `From:` display header. In email forensics you trust, in order: `Received:` (added by servers), `Return-Path`, authentication results (SPF / DKIM / DMARC), `Reply-To`, and `Message-ID` — and you decode every encoded body part.

### Analysis

Claimed identity:

```
From: "Direction des Ressources Humaines" <drh@tricatel-cyber.fr>
To:   <equipe@tricatel-cyber.fr>
Subject: =?UTF-8?B?Tm90ZSBpbnRlcm5lIC0g4oCcYmllbnZlaWxsYW5jZeKAnQ==?=
```

Subject is RFC 2047 Base64. Decoded: `Note interne - "bienveillance"` — ironic.

Real origin — every server-controlled header disagrees with `From:`:

```
Return-Path: <attaquant@mail-cheap-relay.ru>
Reply-To:    <attaquant@mail-cheap-relay.ru>
Message-ID:  <20261113031449.9F2A1@mail-cheap-relay.ru>
Received:    from vps-unknown.mail-cheap-relay.ru [45.83.12.207]
             by mx.tricatel-cyber.fr (Postfix) with ESMTP id 9F2A1;
             Fri, 13 Nov 2026 03:14:52 +0100 (CET)

Received-SPF: fail (domain of drh@tricatel-cyber.fr does not
              designate 45.83.12.207 as permitted sender)
Authentication-Results: mx.tricatel-cyber.fr;
    spf=fail smtp.mailfrom=attaquant@mail-cheap-relay.ru;
    dkim=none; dmarc=fail (p=quarantine) header.from=tricatel-cyber.fr
```

Verdict table:

| Check | Result | Meaning |
|-------|--------|---------|
| SPF | **fail** | `45.83.12.207` is not authorised to send for `tricatel-cyber.fr` |
| DKIM | **none** | No signature from the claimed domain |
| DMARC | **fail** | Alignment fails, policy = quarantine |
| Return-Path / Reply-To | attacker domain | Replies and bounces go to the attacker, not HR |

This is textbook **email spoofing**: the attacker forged the `From:` header and sent via his own cheap relay.

What it hides: the message is `multipart/mixed`. Part 2 is an attachment `note_interne_rh.txt`, `Content-Transfer-Encoding: base64`. Decoding it (any MIME parser does it automatically):

```
NOTE INTERNE - CONFIDENTIEL RH
Objet : surveillance des arrets maladie

Consigne de la Direction : contester systematiquement les arrets
de plus de 3 jours et bloquer les acces informatiques du salarie.
Ne pas laisser de trace ecrite cote salarie.

Preuve de l'ordre : CyberZerk{M4il_Sp00f3_P0ur_Surv31ll3r_L3s_Arr3ts}
```

In English: systematically contest sick leave over 3 days, block the employee's IT access, leave no written trace on the employee's side.

### Solver

`solve_01_email.py` — stdlib only. Parses with `email.BytesParser`, prints all authentication headers, iterates attachments with `iter_attachments()` (which Base64-decodes), regex-extracts `CyberZerk{...}`.

Manual equivalent:

```bash
grep -A20 "note_interne" note_du_drh.eml   # extract Base64 block
echo '<base64>' | base64 -d
```

### Flag

```
CyberZerk{M4il_Sp00f3_P0ur_Surv31ll3r_L3s_Arr3ts}
```
*Leetspeak: "Mail Spoofé Pour Surveiller Les Arrêts" — spoofed mail to surveil sick leave.*

### Lesson

`From:` is a claim, not proof. SPF + DKIM + DMARC exist precisely for this, and a `fail` on all three from an unrelated external relay settles authenticity — regardless of what the sender asserts.

---

## Challenge 2 — Night Exfiltration (Intranet Log)

**Category:** Forensics / Log Analysis
**File:** `challenges/access.log` (Apache/Nginx combined log format, 121 lines)
**Prompt:** *During the night of November 13, a confidential file left Tricatel's intranet. Find the successful exfiltration request.*

### Intuition

Don't read 121 lines one by one. Establish the baseline, then hunt for the line that breaks it on several axes at once: source, path, status, and size.

### Analysis

Baseline (120 lines): internal sources only (`10.0.0.2`–`10.0.0.39`), ordinary paths (`/`, `/login`, `/logout`, `/intranet`, `/css/app.css`, `/favicon.ico`, `/api/absences`, `/rh/dossier?id=1042`), mixed `200/302/304/404`, response sizes roughly 150–4,000 bytes.

The anomaly — line 94:

```
45.83.12.207 - - [13/Nov/2026:02:47:03 +0100] "GET /export.php?file=rapport_confidentiel_rh.zip&token=CyberZerk%7BL0g_4n4lys3_Exf1l_C0nf1rm33%7D HTTP/1.1" 200 184320 "-" "curl/8.2.1"
```

Why this is *the* successful exfiltration, and not a failed probe:

| Signal | Normal traffic | This line |
|--------|---------------|-----------|
| Source IP | `10.0.0.x` internal | **`45.83.12.207` external** — same attacker IP as Challenge 1 |
| Path | browsing / API | **`/export.php?file=rapport_confidentiel_rh.zip`** — only export in the log |
| Status | often 302/304/404 | **`200`** — success |
| Size | < ~4 KB | **`184320` bytes (180 KB)** — the actual file left |
| User-Agent | mixed browsers | `curl/8.2.1` — scripted download |
| Position | chronological | **Out of order**: `02:47:03` inserted between `02:26:04` and `02:26:21` lines |

Failed attempts would be `401/403/404` with a small error body. A `200` + a large body on a confidential archive is a completed download.

The flag is not in plaintext — it is the `token=` parameter, URL-encoded: `%7B` → `{`, `%7D` → `}`.

```
token=CyberZerk%7BL0g_4n4lys3_Exf1l_C0nf1rm33%7D
  URL-decode ↓
CyberZerk{L0g_4n4lys3_Exf1l_C0nf1rm33}
```

### Solver

`solve_02_access_log.py` — filters for non-`10.0.0.` sources / `/export.php`, `urllib.parse.unquote()`s the line, regex-extracts the flag.

Manual equivalent:

```bash
grep -v '^10\.0\.0\.' access.log
awk '$9==200 && $10>10000' access.log
grep export access.log
```

### Flag

```
CyberZerk{L0g_4n4lys3_Exf1l_C0nf1rm33}
```
*"Log Analyse Exfil Confirmée".*

### Lesson

One line can prove exfiltration if you read status + bytes together: a request is an attempt, a `200` with the file's size is a theft. Also watch log *ordering* — an out-of-sequence entry often betrays later insertion / tampering.

---

## Challenge 3 — Calls for Help (Farewell Message)

**Category:** Forensics / Network Forensics
**File:** `challenges/appels_a_l_aide.pcap` (1.5 KB, 12 packets)
**Prompt:** *A Tricatel SOC analyst abruptly resigned. Before returning their equipment, the network team noticed one last suspicious request leaving their workstation toward an unidentified server. We have recovered a capture of their local network traffic. Analyze this capture to find their farewell message.*
*Title pun: "appels à l'aide" = calls for help, and also HTTP calls.*

### Intuition

Small PCAP = read it all. Find the TCP stream with an actual payload; handshakes are noise. If traffic is HTTP (not HTTPS), the message is in clear text — follow the stream.

### Analysis

Packet inventory (parsed manually — no tshark/scapy was needed, and the solver does the same):

| Packet | Flow | Content |
|--------|------|---------|
| 1–2 | IPv6 `::1` | Noise / parallel stack, no payload |
| 3–5 | TCP `127.0.0.1:52058 → 127.0.0.1:9999` | SYN, SYN-ACK, ACK handshake |
| **6** | **TCP, 405 bytes payload** | **HTTP POST — the message** |
| 7 | ACK | — |
| 8–12 | FIN / ACK | Clean teardown |

Packet 6, reassembled:

```http
POST /adieu.php HTTP/1.1
Host: localhost:9999
Accept: */*
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) BurnoutBrowser/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 198

employe=Marc_V&statut=epuisement_total&message=Je quitte Tricatel. Le management me détruit la santé mentale. Je n'ai plus dormi depuis 3 jours. Adieu. Flag: CyberZerk{Exf1ltr4t10n_HTTP_D3s3sp01r}
```

The employee is **Marc_V**, status `epuisement_total` (total exhaustion):

> "Je quitte Tricatel. Le management me détruit la santé mentale. Je n'ai plus dormi depuis 3 jours. Adieu."
> *"I quit Tricatel. Management is destroying my mental health. I haven't slept in 3 days. Goodbye."*

Note the "unidentified server" is in fact `localhost:9999` in the capture (`/adieu.php`) — a local listener / test endpoint for the exfiltration channel, which is why the capture is on loopback.

### Solver

`solve_03_pcap.py` — dependency-free PCAP parser: reads the 24-byte global header, iterates packet records, strips Ethernet (14 B) / IPv4 (IHL) / TCP (data offset), collects non-empty payloads, regex-extracts the flag.

With standard tools, the same result in one line:

```bash
tshark -r appels_a_l_aide.pcap -Y http -T fields -e http.file_data
# Wireshark: right-click packet 6 -> Follow -> TCP Stream
strings appels_a_l_aide.pcap | grep -i cyberzerk
```

### Flag

```
CyberZerk{Exf1ltr4t10n_HTTP_D3s3sp01r}
```
*"Exfiltration HTTP Désespoir" — HTTP exfiltration of despair.*

### Lesson

Encryption is what protects content, not the network. Unencrypted HTTP exposes method, path, headers, and body to anyone with a capture — always follow the TCP stream first in a PCAP challenge before assuming encoding or steganography.

---

## Challenge 4 — The Removed Secret (Git Depot)

**Category:** Forensics / Git Forensics
**File:** `challenges/depot_intranet.tgz` → `depot/` (a `.git` repository + `config.py` + `deploy.sh`)
**Prompt:** *Here is a copy of Tricatel's intranet Git repository, retrieved before a developer left. They swear they "removed the secret from the code." A secret removed from the code hasn't necessarily left the history.*

### Intuition

In Git, "delete" means "add a new commit without it." Every previous version remains an object in `.git/objects`, reachable from history forever — until history itself is rewritten *and* unreachable objects are garbage-collected. Check `git log -p`, not just the working tree.

### Analysis

Working tree at HEAD looks clean — and that is the trap:

```python
# config.py
DEBUG = False
DB_HOST = "10.0.0.5"
```
```sh
# deploy.sh (HEAD)
API_KEY="${DEPLOY_API_KEY}"   # lu depuis l'environnement maintenant
```

History (`git log --oneline --all`):

```
db83693 (HEAD -> master) MAJ config
b3fc794 Securisation: cle sortie du code (lue depuis env)
36e1d6e Ajout script de deploiement
e04f057 Init config intranet
```

Commit `b3fc794` ("Sécurisation") is the removal. Its parent `36e1d6e` is the leak. `git log -p --all` (or `git show 36e1d6e:deploy.sh`) shows:

```diff
commit 36e1d6e4796269f32a1aae755305771818af9ca3
    Ajout script de deploiement

+#!/bin/sh
+# Script de déploiement - NE PAS COMMITER LES SECRETS
+API_KEY="CyberZerk{G1t_N0ubl13_J4m41s_R13n_Du_P4ss3}"
+echo "Déploiement avec $API_KEY"
```

```diff
commit b3fc79460448563cdfdc3440aff06d6ea8fffc6d
    Securisation: cle sortie du code (lue depuis env)

-API_KEY="CyberZerk{G1t_N0ubl13_J4m41s_R13n_Du_P4ss3}"
-echo "Déploiement avec $API_KEY"
+API_KEY="${DEPLOY_API_KEY}"   # lu depuis l'environnement maintenant
+echo "Déploiement"
```

The developer did the right fix in the wrong order: the secret must be **rotated / revoked first**, because the old value stays readable in blob `d21eace` for anyone who clones the repo. Proper remediation: revoke the key, then rewrite history (`git filter-repo`) and force-push, and purge clones/forks.

### Solver

`solve_04_git.py` — safely extracts the tarball to a temp dir, runs `git log --oneline --all` and `git log -p --all`, regex-extracts the flag from the full history (not HEAD).

Manual equivalent:

```bash
tar -xzf depot_intranet.tgz && cd depot
git log -p --all | grep -i cyberzerk
git show 36e1d6e:deploy.sh
# thorough version: git rev-list --all --objects + git cat-file, git fsck --lost-found (dangling objects)
```

### Flag

```
CyberZerk{G1t_N0ubl13_J4m41s_R13n_Du_P4ss3}
```
*"Git N'oublie Jamais Rien Du Passé" — Git never forgets anything from the past. Literally the lesson of the challenge.*

### Lesson

A committed secret is a compromised secret, forever, in every clone. Removing it from HEAD is cosmetic. Rotate it, then rewrite history.

---

## Timeline — How the 4 Challenges Connect

```
Oct 24        Dev commits API_KEY to Git, then "removes" it        [Ch. 4]
              -> key still in history, repo later retrieved

13 Nov 02:47  External 45.83.12.207 downloads                      [Ch. 2]
              /export.php?file=rapport_confidentiel_rh.zip
              200 OK, 184320 bytes — intranet log

13 Nov 03:14  Same attacker (45.83.12.207 / mail-cheap-relay.ru)   [Ch. 1]
              spoofs drh@tricatel-cyber.fr, SPF/DKIM/DMARC all fail
              Hidden note: contest sick leave > 3 days, block IT
              access, leave no trace

(undated)     Marc_V, SOC analyst, total exhaustion, no sleep      [Ch. 3]
              for 3 days, POSTs his farewell to /adieu.php
              in clear-text HTTP
```

Same attacker IP in Challenges 1 and 2 links the spoofed email to the exfiltration. Challenges 1 and 3 give the human story behind the data: surveillance of sick leave, and an analyst burned out by it.

## Summary of Flags

```
1. CyberZerk{M4il_Sp00f3_P0ur_Surv31ll3r_L3s_Arr3ts}
2. CyberZerk{L0g_4n4lys3_Exf1l_C0nf1rm33}
3. CyberZerk{Exf1ltr4t10n_HTTP_D3s3sp01r}
4. CyberZerk{G1t_N0ubl13_J4m41s_R13n_Du_P4ss3}
```

## Tools Used

- Python 3 standard library only for all solvers (`email`, `base64`, `re`, `urllib.parse`, `struct`, `subprocess`, `tarfile`) — no external dependencies
- `git log -p --all` / `git show` for Git archaeology
- Manual PCAP parsing (Wireshark / `tshark -Y http` / `strings` give identical results)
- `grep` / `awk` log triage for the access log

*All four solvers were executed against the original challenge files and produce the four flags above (4/4).*
