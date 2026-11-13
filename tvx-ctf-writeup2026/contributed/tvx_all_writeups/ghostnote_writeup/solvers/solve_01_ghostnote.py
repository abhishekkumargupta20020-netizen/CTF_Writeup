#!/usr/bin/env python3
"""
GhostNote solver (stdlib only).

Chain, exactly as implemented by the exported functions in
NotionUpdate.exe:

 1. deviceSecret (identity table, vault.db) is Base64 for 32 raw bytes.
 2. GhostNote_getC2(i) returns one of three blobs in .rdata
    (RVA 0x2000 / 0x2030 / 0x2060). GhostNote_decodeServer XORs each
    byte with 0x37 and stops at a raw 0x37 terminator:
      0: wss://notion-assets-cdn.com:9443/update
      1: wss://SYNC-NOTES-SERVICE.CLOUD:8443/api/v2
      2: wss://notes-edge-cache.net:443/sync
 3. GhostNote_extractHostLower keeps the host after "://", stops at
    ':' or '/', and lower-cases it.
 4. GhostNote_deriveSession:   session = SHA256(secret || host)
    GhostNote_validationDigest: SHA256(session || "GHOSTNOTE")
    Only host sync-notes-service.cloud reproduces the config value
    serverValidation = 2be46ca73aacd65f76539df5d2157357d44bf060
                        736cc92e457642daad0be83c
    Its port, 8443, is also the DestinationPort in the Sysmon
    EventID 3 network event - the other two are decoys.
 5. Campaign: registry SessionInfo SyncProfile = "GNT-0926"
    (hint in company-root-ca.pem, Base64 comment:
     "THE IDENTITY OPENS THE DOOR, BUT THE PROFILE NAMES THE CAMPAIGN.")
 6. GhostNote_finalFlagDigest: SHA256(secret || host || campaign),
    flag = "Tvx{" + hexdigest[:40] + "}"
"""
import base64, hashlib, pathlib, re, sqlite3, sys, zipfile, tempfile, os

def extract_root() -> pathlib.Path:
    # When run inside the package, the challenge zip sits in ../challenges/
    here = pathlib.Path(__file__).resolve()
    for cand in [here.parent.parent / "challenges" / "GhostNote.zip",
                 pathlib.Path("challenges/GhostNote.zip"),
                 pathlib.Path("GhostNote.zip")]:
        if cand.exists():
            tmp = pathlib.Path(tempfile.mkdtemp(prefix="ghostnote_"))
            with zipfile.ZipFile(cand) as z:
                z.extractall(tmp)
            return tmp / "GhostNote"
    # Fall back to a GhostNote folder next to the solver / cwd
    for cand in [here.parent.parent / "GhostNote", pathlib.Path("GhostNote")]:
        if cand.exists():
            return cand
    raise SystemExit("GhostNote.zip / GhostNote folder not found")

def main():
    root = extract_root()
    db = root / "Users/john/AppData/Roaming/Notion/vault.db"
    con = sqlite3.connect(db)
    secret_b64 = con.execute(
        "SELECT secret FROM identity WHERE name='deviceSecret'").fetchone()[0]
    server_validation = con.execute(
        "SELECT value FROM config WHERE name='serverValidation'").fetchone()[0]
    secret = base64.b64decode(secret_b64)
    assert len(secret) == 32, len(secret)

    exe = (root / "Users/john/AppData/Local/NotionUpdate/NotionUpdate.exe").read_bytes()
    # .rdata: file offset 0xe00 == RVA 0x2000. Three 0x30-spaced blobs,
    # each terminated in the raw data by a single 0x37 byte.
    servers = []
    for off in (0x2000, 0x2030, 0x2060):
        raw = exe[0xe00 + (off - 0x2000): 0xe00 + (off - 0x2000) + 0x30]
        end = raw.index(0x37)
        servers.append(bytes(b ^ 0x37 for b in raw[:end]).decode())

    def host_lower(url: str) -> str:
        host = url.split("://", 1)[1]
        host = re.split(r"[:/]", host, maxsplit=1)[0]
        return host.lower()

    real_host, session = None, None
    for url in servers:
        host = host_lower(url)
        sess = hashlib.sha256(secret + host.encode()).digest()
        val = hashlib.sha256(sess + b"GHOSTNOTE").hexdigest()
        print(f"candidate {url}  host={host}  validation={val} "
              f"{'MATCH' if val == server_validation else ''}")
        if val == server_validation:
            real_host, session = host, sess
    assert real_host, "no C2 candidate validated"

    reg = (root / "Users/john/NTUSER.DAT.reg").read_bytes().decode("utf-16")
    campaign = re.search(r'"SyncProfile"="([^"]+)"', reg).group(1)

    flag_digest = hashlib.sha256(
        secret + real_host.encode() + campaign.encode()).hexdigest()
    flag = f"Tvx{{{flag_digest[:40]}}}"
    print(f"deviceSecret (raw hex) : {secret.hex()}")
    print(f"real C2 host           : {real_host}")
    print(f"deriveSession          : {session.hex()}")
    print(f"validation (recomputed): {hashlib.sha256(session + b'GHOSTNOTE').hexdigest()}")
    print(f"serverValidation (db)  : {server_validation}")
    print(f"campaign / SyncProfile : {campaign}")
    print(f"finalFlagDigest        : {flag_digest}")
    print(flag)
    return flag

if __name__ == "__main__":
    main()
