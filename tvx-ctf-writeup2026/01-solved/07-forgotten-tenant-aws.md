# Forgotten Tenant — AWS Role-Chain Pivot

**Author:** Abhishek Kr Gupta
**Event:** TVX CTF, 2026-11-13
**Status:** Solved via live AWS, flag retrieved from evidence.json —
NOT platform-submission-confirmed by Shikhu

## Flag

```
TVX{6N8at90xLFvdgyma648o}
```

## Challenge

"A Q4 2024 cloud migration left a forgotten AWS environment never fully
decommissioned." Investigate the archived environment, analyse the
forensic evidence, and reconstruct the intended access path to retrieve
the final evidence.

Given: AWS IAM credentials (player), region `us-east-1`, migration
archive bucket `tvx-forgotten-tenant-migration-archive-pro0hid4`,
forensic bundle `forgotten-tenant-stage3-bundle.zip`.

## Method

Player identity (confirmed live):

```
user: tvx-forgotten-tenant-player
account: 400875701859
```

The migration archive bucket held the ExternalId clues: the role tag
`audit-ext-id-prefix` in the IAM snapshot gave `fthK52`, and ticket
`TVX-4471` gave the last-6 suffix `ycGCAX`, so:

```
ExternalId = fthK52ycGCAX
```

The live chain, executed with the player credentials:

```
player
  -> AssumeRole tvx-forgotten-tenant-legacy-migration-role (with ExternalId)
  -> AssumeRole tvx-forgotten-tenant-incident-response-role
  -> GetObject s3://tvx-forgotten-tenant-forensics-pro0hid4/case-ab5396cd/handoff-RYII91T48V/evidence.json
```

The case folder came from the 2026-03-14 manifest upload; the handoff
sub-path from 2026-03-15. `ListBucket` on the forensics bucket was denied,
but `GetObject` on the exact key succeeded — the classic excessive-trust
pattern the case documents: the legacy role's inline policy allowed
`sts:AssumeRole` into the incident-response role.

`evidence.json` (saved as `evidence/forgotten-tenant-evidence.json`):

```json
{
  "case_id": "case-ab5396cd",
  "handoff_code": "RYII91T48V",
  "classification": "internal-forensics",
  "final_flag": "TVX{6N8at90xLFvdgyma648o}"
}
```

Note: `TVX{Cl0ud_s3cur1ty}` in the challenge description was NOT the
flag — it is a generic example in the text.

## Flag

```
TVX{6N8at90xLFvdgyma648o}
```

Shikhu submits flags himself; this one was retrieved live, not submitted
to the platform by Muse.
