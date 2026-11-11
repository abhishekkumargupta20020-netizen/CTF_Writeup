# 3. Email — spoofed HR mail — SOLVED

**Source file:** `note_du_drh.eml` (uploaded by the author, 2026-11-10)
**Flag:** `CyberZerk{M4il_Sp00f3_P0ur_Surv31ll3r_L3s_Arr3ts}`

## The challenge

An internal email from the HR Director is being forwarded, which he claims is "authentic". The employees swear they never sent it. Prove where it really comes from and what it is hiding.

## The evidence (headers, verbatim from the file)

- `From: "Direction des Ressources Humaines" <drh@tricatel-cyber.fr>`
- `Return-Path: <attaquant@mail-cheap-relay.ru>`
- `Reply-To: <attaquant@mail-cheap-relay.ru>`
- `Received: from vps-unknown.mail-cheap-relay.ru (vps-unknown.mail-cheap-relay.ru [45.83.12.207]) by mx.tricatel-cyber.fr`
- `Received-SPF: fail` (domain of drh@tricatel-cyber.fr does not designate 45.83.12.207 as permitted sender)
- `Authentication-Results: spf=fail smtp.mailfrom=attaquant@mail-cheap-relay.ru; dkim=none; dmarc=fail (p=quarantine) header.from=tricatel-cyber.fr`
- `Message-ID: <20261113031449.9F2A1@mail-cheap-relay.ru>`

The `From:` header claims Tricatel; every authentication signal and the actual sending host say otherwise — a cheap relay in Russia (`mail-cheap-relay.ru`, 45.83.12.207). SPF fails, DKIM is absent, DMARC fails.

## What it is hiding

The attachment `note_interne_rh.txt` (Base64, decoded with a Python email parser) reads:

> NOTE INTERNE - CONFIDENTIEL RH / Objet : surveillance des arrets maladie
> Consigne: contester systematiquement les arrets de plus de 3 jours et bloquer les acces informatiques du salarie.

An internal order to systematically contest sick leave over 3 days and block the employee's IT access — the same pattern as Marc V.'s file in the absences challenge.

## Flag

`CyberZerk{M4il_Sp00f3_P0ur_Surv31ll3r_L3s_Arr3ts}`
