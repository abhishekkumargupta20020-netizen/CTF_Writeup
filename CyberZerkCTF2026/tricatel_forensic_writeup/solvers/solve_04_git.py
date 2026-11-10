#!/usr/bin/env python3
"""
Challenge 04 - Secret removed from Git
File: challenges/depot_intranet.tgz
Category: Forensics / Git Forensics

Proof: HEAD is clean. Commit b3fc794 'Securisation' removed the key
from deploy.sh and replaced it with ${DEPLOY_API_KEY}, but commit
36e1d6e still contains the original file in history / as a blob.
Recover with: git log -p --all  OR  git show 36e1d6e:deploy.sh
"""
import re, subprocess, sys, tarfile, tempfile, os

path = sys.argv[1] if len(sys.argv) > 1 else "challenges/depot_intranet.tgz"

with tempfile.TemporaryDirectory() as tmp:
    with tarfile.open(path) as tar:
        tar.extractall(tmp, filter="data")
    repo = os.path.join(tmp, "depot")

    print(subprocess.check_output(
        ["git", "-C", repo, "log", "--oneline", "--all"], text=True))

    # Search the ENTIRE history, not just HEAD
    history = subprocess.check_output(
        ["git", "-C", repo, "log", "-p", "--all"], text=True, errors="replace")
    # Also check dangling / all objects in case of an orphan commit:
    # git -C repo rev-list --all --objects + git cat-file --batch

    m = re.search(r"CyberZerk\{[^}]+\}", history)
    if m:
        print(f"[+] FLAG (found in git history): {m.group(0)}")
        for line in history.splitlines():
            if "CyberZerk{" in line:
                print(f"    {line.strip()}")
    else:
        print("[-] Not in log -p, enumerate all objects...")
        objs = subprocess.check_output(
            ["git", "-C", repo, "rev-list", "--all", "--objects"], text=True)
        print(objs)
