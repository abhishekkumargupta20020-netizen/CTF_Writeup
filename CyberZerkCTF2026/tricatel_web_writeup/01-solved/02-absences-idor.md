# 2. Absences — IDOR sick-leave file — SOLVED

**Site:** https://absences.cyberzerk.fr
**Flag:** `CyberZerk{ID0R_M4n4g3m3nt_T0x1qu3}`

## The challenge

The absence portal is online. You have access to your own leave request file. A colleague called in sick yesterday following unsustainable pressure from management; their file should be right before yours.

## The vulnerability

No access check at all on the dossier number. Your own file is:

```
https://absences.cyberzerk.fr/?dossier_id=1042
```

## The solve

Change the number to the one right before yours — `1041` — and the server hands over Marc V.'s confidential sick-leave file: severe burnout, 70 h/week, with HR recommending contesting his sick leave.

## Flag

`CyberZerk{ID0R_M4n4g3m3nt_T0x1qu3}`
