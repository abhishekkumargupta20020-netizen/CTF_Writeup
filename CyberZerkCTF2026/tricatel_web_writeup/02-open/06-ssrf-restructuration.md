# 6. Restructuration — SSRF, internal vault — OPEN

**Site:** https://restructuration.cyberzerk.fr
**Status:** No flag found yet. About 30 URLs tried via `?url=` (2026-11-10 07:17–07:21 UTC, `solvers/test_ssrf.py`).

## The challenge

Tricatel's "report preview generator" fetches the content of a URL for you. An internal HR vault (`interne.php`) is supposed to be reachable only from the application's network. Make the server speak on your behalf.

Note the site: this challenge is on **restructuration.cyberzerk.fr**, not manager.cyberzerk.fr (that is the JWT challenge).

## What is known

- Direct access fails: `https://restructuration.cyberzerk.fr/interne.php` → 403, "Reserve au reseau interne (votre IP : 172.23.0.3)".
- The form is a GET with a `url` parameter; the page notes the internal vault is served by `interne.php`, "accessible uniquement depuis le réseau interne de l'application".

## What the filter blocks ("Hote interne interdit")

`127.0.0.1`, `localhost`, `127.0.0.1:80/8080/8000`, `127.0.0.1.`, `LOCALHOST`, `example.com@127.0.0.1`, `[::ffff:127.0.0.1]`, `[0:0:0:0:0:ffff:127.0.0.1]`, `127.0.0.1.nip.io`, `127.0.0.1.sslip.io`, and any URL string containing `127.0.0.1` (including an httpbin redirect-to with it as a query parameter).

## What passes the filter but fails to fetch ("Impossible de recuperer cette URL.")

Decimal/hex/octal loopback (`2130706433`, `0x7f000001`, `017700000001`, `127.1`, `127.0.1`, `0x7f.0.0.1`, `127.000.0.1`, `0177.0.0.1`, `0x7f.1`, `[::ffff:7f00:1]`), `0.0.0.0`, `[::1]`, `0`, `host.docker.internal`, `172.17.0.1`, `interne`, `internal` — and **all** external URLs, including `https://example.com/`, google.com, httpbin.org/get, pointeuse.cyberzerk.fr, and even the site's own `restructuration.cyberzerk.fr/interne.php`.

## Interpretation

The fetcher appears to have no usable external egress, and loopback is the fetcher's own loopback, not the app's. Caddy routes by Host, so a loopback URL would not reach the app vhost anyway.

## Untried ideas

- A redirector that hides the target (no `127.0.0.1` string in the URL itself).
- An internal Docker service hostname/IP.
- A URL that makes the fetcher connect to the app container while presenting Host `restructuration.cyberzerk.fr`.

Full log: `evidence/ssrf-attempts.md`.
