# Mission: Broken Trust — Shadow Cloud, 6/6

**Author:** Abhishek Kr Gupta
**Event:** TVX CTF, 2026-11-13
**Status:** Solved 6/6 stages in the challenge app —
NOT platform-submission-confirmed by Shikhu

## Flag

```
TVX{ROLE_HANDOFF_LAMBDA_TRUST_PUBLIC_POLICY_SECRET_READ_ROLE_SESSION_KMS_DECRYPT}
```

## Challenge

"Shadow Cloud — Advanced Investigation", a simulated (no real AWS)
6-stage quiz at https://ctf-tke5.onrender.com/. Each correct answer
reveals one flag fragment.

## Method

Each stage's answer was derived from the on-page evidence, then entered
in the app. Every one was accepted, progress 0/6 -> 6/6:

| Stage | Answer | Fragment |
|---|---|---|
| 01 | `iam:PassRole` | ROLE_HANDOFF |
| 02 | `lambda.amazonaws.com` | LAMBDA_TRUST |
| 03 | `BlockPublicPolicy` | PUBLIC_POLICY |
| 04 | `GetSecretValue` | SECRET_READ |
| 05 | `FinanceReadOnly` | ROLE_SESSION |
| 06 | `kms:Decrypt` | KMS_DECRYPT |

The app assembled and displayed the flag from the six fragments, joined
with underscores inside `TVX{...}`.

## Flag

```
TVX{ROLE_HANDOFF_LAMBDA_TRUST_PUBLIC_POLICY_SECRET_READ_ROLE_SESSION_KMS_DECRYPT}
```

Shikhu submits flags himself; this flag was displayed by the challenge
app, not submitted to the platform by Muse.
