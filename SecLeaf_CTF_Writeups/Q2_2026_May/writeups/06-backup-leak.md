# Backup Leak — Secure Notes Portal

- **Competition:** SecLeaf Q2 2026
- **Date investigated:** 23 May 2026
- **Category:** Web reconnaissance / information disclosure
- **Target:** `https://backup-leak.secleaf.tech/`
- **Status:** Incomplete; no flag or backup disclosure recovered

## 1. Initial response

The target returned HTTP 200. Headers showed:

```text
HTTP/2 200
server: cloudflare
x-powered-by: PHP/8.2.31
content-type: text/html; charset=UTF-8
```

The page content was:

```html
<h1>Secure Notes Portal</h1>
<p>Nothing sensitive is stored here.</p>
```

Cloudflare challenge JavaScript was appended to the page.

## 2. Directory enumeration

The investigation used Gobuster:

```bash
gobuster dir \
  -u https://backup-leak.secleaf.tech/ \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -x zip,tar,gz,bak,old,sql,txt \
  -t 2 \
  --timeout 30s
```

The scan was interrupted after approximately 50 of 38,000 entries because many requests timed out. A `.cvs.bak` request returned HTTP 522. This was not a successful discovery.

## 3. Direct path checks

The following paths were checked:

```text
.git/config
.git/HEAD
backup.zip
backup.tar.gz
notes.zip
notes.tar.gz
db.sql
dump.sql
.env
.env.bak
backup/
old/
dev/
admin/
api/
test/
debug/
```

Most returned 404. Some returned Cloudflare 522 or 520 errors.

Example:

```bash
curl -I https://backup-leak.secleaf.tech/
curl -s https://backup-leak.secleaf.tech/ | tee index.html
curl -sk -I https://backup-leak.secleaf.tech/.git/config
```

## 4. Interpretation

The challenge name and page text suggested an exposed backup or note store, but the preserved probing did not locate it. Cloudflare edge errors and timeouts limited enumeration.

Do not report `.cvs.bak` as a discovered backup: the response was 522, not a valid file.

## 5. Next steps

With a live, authorized instance:
1. Re-check `robots.txt`, sitemap, source, JavaScript, and linked routes.
2. Use a smaller, curated wordlist before broad enumeration.
3. Distinguish origin responses from Cloudflare edge errors.
4. Check common backup suffixes only after identifying the application's naming conventions.
5. Save response bodies and status codes, not just headers.

## Status

No backup, sensitive note, or verified flag was recovered in the available session.
