#!/usr/bin/env python3
"""
Hashphobia solver — SpookyCTF 2026 (author: Frank C, 750 pts).

Attack chain
------------
1. SHA-256 hash -> VirusTotal file report -> case-telemetry.sh (138 B shell
   script, 0 detections). The script does exactly one thing:
       curl http://18.117.181.107/
2. The server (18.117.181.107:80, nginx) answers every plain GET with:
       status=nah; message=what's the magic word?
   Only GET works (other methods -> 405); every path except / -> 404.
3. The flag tail comes from the author's VirusTotal comment ("thehackerguy"):
   base64 NG5kX2NoM2NrX3JldmlldzV9 -> "4nd_ch3ck_review5}"
   so the flag is:  spooky{<unknown beginning>4nd_ch3ck_review5}
4. Platform Hint 1 (5 pts): "what is the magic word? the english language
   only has so many magical words used that could the message."
   -> the magic word is one of the finite set of English magical words.
5. This script brute-forces the magic word against the server. Any response
   that is NOT "status=nah..." is a hit — the server should then return
   the flag (or its beginning).

What has already been tried (all "nah", ~1,000,000 probes as of 2026-11-07):
  * the 118 magical words below, in every form, vs word/magic/magic_word,
    as URL paths, and as bare parameters
  * 10k most-common passwords, 20k English words, 100k passwords vs
    word/magic/magic_word, a 370k-word dictionary vs word
  * 6,453 parameter names x 30 magic words (cross-product)
  * 4,751 paths, 6,453 param names, headers, methods, ports, encodings
So the magic word is NOT in any of those lists. This solver automates the
attack so you can run it yourself, extend the wordlists, or re-run it if
the server changes. If you have a free VirusTotal API key, --vt-api-key
resolves the server from the hash first (full chain, no hard-coding).

Usage
-----
  python3 hashphobia_solver.py                      # built-in magic words
  python3 hashphobia_solver.py --wordlist words.txt # your own list
  python3 hashphobia_solver.py --download-lists     # fetch 10k+20k+100k, run them
  python3 hashphobia_solver.py --params word magic magic_word --workers 25
  python3 hashphobia_solver.py --vt-api-key YOUR_KEY
  python3 hashphobia_solver.py --server http://18.117.181.107/

Requires only the Python 3 standard library. No rockyou (deliberately
not used here).
"""

import argparse
import concurrent.futures
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_HASH = "f854432d21db979021f45b85384b7f2d6500fa2f62981c87ebba79b3d46f1a7b"
DEFAULT_SERVER = "http://18.117.181.107/"
DEFAULT_PARAMS = ["word", "magic", "magic_word"]
FLAG_TAIL = "4nd_ch3ck_review5}"
NAH = "status=nah"

# The finite set of English magical words (classic, stage magic, Harry
# Potter, Colossal Cave / Zork, pop culture), each in the forms the server
# might expect: space, underscore, hyphen, and joined-up.
MAGIC_WORDS = [
    "abracadabra", "accio", "aguamenti", "alakazam", "alohomora", "avada",
    "avada kedavra", "avada-kedavra", "avada_kedavra", "avadakedavra",
    "bibbidi bobbidi boo", "bibbidi-bobbidi-boo", "bibbidi_bobbidi_boo",
    "bibbidibobbidiboo", "bippity boppity boo", "bippity-boppity-boo",
    "bippity_boppity_boo", "bippityboppityboo", "blorple", "colloportus",
    "confringo", "crucio", "depulso", "diffindo", "episkey", "expecto",
    "expecto patronum", "expecto-patronum", "expecto_patronum",
    "expectopatronum", "expelliarmus", "expulso", "ferula", "finite",
    "finite incantatem", "finite-incantatem", "finite_incantatem",
    "finiteincantatem", "frotz", "gemino", "girgol", "hocus", "hocus pocus",
    "hocus-pocus", "hocus_pocus", "hocuspocus", "impedimenta", "imperio",
    "incantatem", "incantato", "incendio", "jumbo", "kazam", "kedavra",
    "levicorpus", "leviosa", "locomotor", "lumos", "mellon", "morsmordre",
    "muffliato", "mumbo", "mumbo jumbo", "mumbo-jumbo", "mumbo_jumbo",
    "mumbojumbo", "nitfol", "nox", "obliviate", "open sesame", "open-sesame",
    "open_sesame", "opensesame", "patronum", "petrificus",
    "petrificus totalus", "petrificus-totalus", "petrificus_totalus",
    "petrificustotalus", "plover", "plugh", "pocus", "presto",
    "presto chango", "presto-chango", "presto_chango", "prestochango",
    "prior", "prior incantato", "prior-incantato", "prior_incantato",
    "priorincantato", "protego", "quietus", "reducto", "rezrov",
    "riddikulus", "sectumsempra", "sesame", "shazam", "sim sala bim",
    "sim-sala-bim", "sim_sala_bim", "simsalabim", "sonorus", "stupefy",
    "tarantallegra", "throck", "totalus", "vaxum", "waddiwasi",
    "wingardium", "wingardium leviosa", "wingardium-leviosa",
    "wingardium_leviosa", "wingardiumleviosa", "xyzzy", "zifmia",
]

# Extra magical words tried separately (pop culture / obscure). Kept here so
# they are part of the solver too; they are appended to MAGIC_WORDS at runtime.
EXTRA_MAGIC_WORDS = [
    "supercalifragilisticexpialidocious", "supercalifragilistic",
    "higitus", "higitus figitus", "higitus_figitus", "ni", "treguna",
    "treguna mekoides", "treguna_mekoides", "pedo mellon a minno",
    "pedo_mellon_a_minno", "flower gleam and glow", "flower_gleam_and_glow",
    "as you wish", "as_you_wish", "no place like home", "no_place_like_home",
    "amok", "hey presto", "hey_presto", "abra cadabra", "abra-cadabra",
    "ala-kazam", "kazaam", "Abracadabra", "Alakazam", "Kazam", "Kazaam",
    "Shazam", "Presto", "Hocus Pocus", "Open Sesame", "Sim Sala Bim",
    "Bibbidi Bobbidi Boo", "thank you", "thank_you", "thanks", "sorry",
    "excuse me", "excuse_me", "spell", "incantation", "enchantment",
    "conjure", "sorcery", "wizardry", "witchcraft", "magic word",
    "magicword", "the magic word", "the_magic_word",
    "speak friend and enter", "speak_friend_and_enter",
    "friend and enter", "friend_and_enter", "speak friend", "speak_friend",
]

WORDLIST_URLS = {
    "10k_passwords.txt":
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/"
        "Passwords/Common-Credentials/10k-most-common.txt",
    "20k_english.txt":
        "https://raw.githubusercontent.com/first20hours/google-10000-english/"
        "master/20k.txt",
    "100k_passwords.txt":
        "https://raw.githubusercontent.com/danielmiessler/SecLists/master/"
        "Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt",
}


def probe(server, param, value, timeout=8):
    """GET server?param=value. Returns the response body ('' on empty/error).

    An empty body is retried once: under load the server occasionally
    drops a connection, and an empty reply is NOT a hit.
    """
    url = server.rstrip("/") + "/?" + urllib.parse.urlencode({param: value})
    req = urllib.request.Request(url, headers={"User-Agent": "hashphobia-solver/1.0"})
    for _attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", "replace")
            if body.strip():
                return body
        except Exception:
            pass
    return ""


def is_hit(body):
    """A hit is a non-empty reply that is not the standard rejection."""
    return bool(body and body.strip() and NAH not in body)


def vt_resolve_server(api_key, sha256):
    """Resolve the server URL from VirusTotal (free API key) via the file's
    contacted URLs. Returns None on any failure (caller falls back)."""
    try:
        url = ("https://www.virustotal.com/api/v3/files/%s/contacted_urls"
               % sha256)
        req = urllib.request.Request(url, headers={"x-apikey": api_key})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        for item in data.get("data", []):
            u = item.get("attributes", {}).get("url", "")
            if u.startswith("http://") or u.startswith("https://"):
                return u
    except Exception as exc:  # noqa: BLE001 - any VT failure -> fall back
        print("[vt] lookup failed (%s); using default server" % exc)
    return None


def download_lists(dest_dir="wordlists"):
    """Download the public wordlists used in the recon. Returns [paths]."""
    os.makedirs(dest_dir, exist_ok=True)
    paths = []
    for name, url in WORDLIST_URLS.items():
        path = os.path.join(dest_dir, name)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            print("[dl] %s already present" % path)
        else:
            print("[dl] fetching %s ..." % url)
            urllib.request.urlretrieve(url, path)
            print("[dl] saved %s (%d lines)" % (path, sum(1 for _ in open(path))))
        paths.append(path)
    return paths


def load_values(path):
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return [line.strip() for line in fh if line.strip()]


def run(server, params, values, workers=25):
    """Brute-force every (param, value). Returns a list of hits."""
    jobs = [(p, v) for p in params for v in values]
    total = len(jobs)
    print("[*] server: %s" % server)
    print("[*] params: %s" % ", ".join(params))
    print("[*] values: %d  (total requests: %d, workers: %d)"
          % (len(values), total, workers))
    print("[*] a hit is any reply that is not '%s...'" % NAH)

    hits = []
    done = 0
    stop = threading.Event()
    started = time.time()

    def work(job):
        p, v = job
        if stop.is_set():
            return None
        body = probe(server, p, v)
        if is_hit(body):
            stop.set()
            return (p, v, body)
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(work, job): job for job in jobs}
        for fut in concurrent.futures.as_completed(futs):
            done += 1
            if done % 1000 == 0 or done == total:
                el = time.time() - started
                print("[*] %d/%d (%.0f%%) in %.0fs"
                      % (done, total, 100.0 * done / total, el), flush=True)
            try:
                res = fut.result()
            except Exception:
                res = None
            if res:
                hits.append(res)
                print("\n[!] HIT %s=%s -> %r\n" % res, flush=True)
                break

    if hits:
        with open("hashphobia_hit.txt", "w", encoding="utf-8") as fh:
            for p, v, body in hits:
                fh.write("%s=%s -> %s\n" % (p, v, body))
        print("[!] hit saved to hashphobia_hit.txt")
        for _p, _v, body in hits:
            if "spooky{" in body:
                print("[!] FLAG? %s" % body.strip())
        print("[!] known flag tail is %s, so a full flag looks like "
              "spooky{<beginning>%s}" % (FLAG_TAIL, FLAG_TAIL))
    else:
        print("[*] done: no hit in %d requests (%.0fs) — all '%s'"
              % (done, time.time() - started, NAH))
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description="Hashphobia magic-word solver")
    ap.add_argument("--server", default=DEFAULT_SERVER,
                    help="challenge server base URL")
    ap.add_argument("--hash", default=DEFAULT_HASH,
                    help="SHA-256 of case-telemetry.sh (for --vt-api-key)")
    ap.add_argument("--params", nargs="+", default=DEFAULT_PARAMS,
                    help="GET parameter names to try")
    ap.add_argument("--workers", type=int, default=25)
    ap.add_argument("--wordlist", action="append", default=[],
                    help="extra wordlist file (can repeat)")
    ap.add_argument("--download-lists", action="store_true",
                    help="download 10k + 20k + 100k lists and run them")
    ap.add_argument("--no-magic-words", action="store_true",
                    help="skip the built-in magical-words list")
    ap.add_argument("--vt-api-key", default=None,
                    help="free VirusTotal API key: resolve server from hash")
    args = ap.parse_args(argv)

    server = args.server
    if args.vt_api_key:
        resolved = vt_resolve_server(args.vt_api_key, args.hash)
        if resolved:
            print("[vt] server resolved from hash: %s" % resolved)
            server = resolved

    values = []
    if not args.no_magic_words:
        values.extend(MAGIC_WORDS)
        values.extend(EXTRA_MAGIC_WORDS)
    for path in args.wordlist:
        values.extend(load_values(path))
    if args.download_lists:
        for path in download_lists():
            values.extend(load_values(path))

    # De-duplicate, preserving order.
    seen = set()
    values = [v for v in values if not (v in seen or seen.add(v))]

    if not values:
        print("no values to try (give --wordlist or drop --no-magic-words)")
        return 2

    hits = run(server, args.params, values, workers=args.workers)
    return 0 if hits else 1


if __name__ == "__main__":
    sys.exit(main())
