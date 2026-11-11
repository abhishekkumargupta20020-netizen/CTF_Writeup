# 4. Manager — JWT alg:none — SOLVED

**Site:** https://manager.cyberzerk.fr
**Flag:** `CyberZerk{JWT_4lg_N0n3_C_3st_N0n}`

## The challenge

Tricatel's manager area is protected by a JWT token. Your account is only an "employee" account. An exhausted developer botched the token verification on a production night. Forge yourself an admin access and retrieve the CODIR (Executive Committee) bonus table.

## The vulnerability

The session JWT is HS256, and the site accepts unsigned tokens. The site itself hints at it: the token check was botched and "it even accepts tokens without a signature".

Original token (session cookie):

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZW1wbG95ZTg0NzIiLCJyb2xlIjoiZW1wbG95ZSJ9.s9ip1QaEfGwDjSo2VMn4p3fQ1PEGp8GixtSX-jeg6sM
```

Decoded: header `{"alg":"HS256","typ":"JWT"}`, payload `{"user":"employe8472","role":"employe"}`.

## The solve

Forge a token with `alg:none`, role `admin`, and an empty signature:

```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiZW1wbG95ZTg0NzIiLCJyb2xlIjoiYWRtaW4ifQ.
```

Send it as `Cookie: session=<token>`. Verified live 2026-11-10 ~07:18 UTC: the page replies "rôle admin" with the CODIR bonus table and the flag.

One detail that matters: the same payload with an HS256 header and an empty signature does **not** work — the role falls back to "invité". `alg:none` is the key.

## Flag

`CyberZerk{JWT_4lg_N0n3_C_3st_N0n}`
