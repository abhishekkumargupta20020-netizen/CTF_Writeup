# 1. Pointeuse — hidden overtime — SOLVED

**Site:** https://pointeuse.cyberzerk.fr
**Flag:** `CyberZerk{P0int3us3_Qu1_0ubl13_L3s_H3ur3s_Sup}`

## The challenge

Tricatel's new time-tracking software quietly "forgets" overtime hours. You only have access to your own profile — but someone surely has the right to see the real hours of the entire team.

## The vulnerability

The `profil` cookie is unsigned Base64 JSON. It decides your role, and the server trusts it:

```
{"employe":"Vous (#8472)","role":"employe"}
```

Encoded: `eyJlbXBsb3llIjoiVm91cyAoIzg0NzIpIiwicm9sZSI6ImVtcGxveWUifQ==`

As an employee you see only your own sheet — weeks S.45 and S.46, 35 h normal, 0 h overtime — with the note that overtime is "automatically brought back to 0 h, in accordance with company policy" and that only a manager profile can see the real register.

## The solve

Change `role` to `manager` in the cookie (re-encode the JSON as Base64, no signature to forge — there is none) and reload. The real register appears:

| Employee | Real hours | Declared |
|---|---|---|
| Marc V. | 58 h | 0 h |
| Stagiaire RH | 31 h | 0 h |
| Vous (#8472) | 44 h | 0 h |

## Flag

`CyberZerk{P0int3us3_Qu1_0ubl13_L3s_H3ur3s_Sup}`
