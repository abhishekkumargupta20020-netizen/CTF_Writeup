#!/usr/bin/env python3
"""
Challenge 01 - Spoofed HR email
File: challenges/note_du_drh.eml
Category: Forensics / Email Forensics

Proof: From is spoofed. Return-Path / Reply-To / Message-ID / Received
all point to attaquant@mail-cheap-relay.ru (45.83.12.207).
SPF=fail, DKIM=none, DMARC=fail.
Hidden content: Base64 attachment note_interne_rh.txt contains the flag.
"""
import base64, email, re, sys
from email import policy
from email.parser import BytesParser

path = sys.argv[1] if len(sys.argv) > 1 else "challenges/note_du_drh.eml"

with open(path, "rb") as f:
    msg = BytesParser(policy=policy.default).parse(f)

print(f"From:        {msg['From']}")
print(f"Return-Path: {msg['Return-Path']}")
print(f"Reply-To:    {msg['Reply-To']}")
print(f"Message-ID:  {msg['Message-ID']}")
print(f"Received:    {msg['Received']}")
print(f"SPF/DMARC:   {msg['Authentication-Results']}")
print(f"Subject:     {msg['Subject']}")
print()

for part in msg.iter_attachments():
    print(f"Attachment: {part.get_filename()} ({part.get_content_type()})")
    payload = part.get_payload(decode=True)  # auto-decodes Base64
    text = payload.decode(errors="replace")
    print("--- Decoded attachment ---")
    print(text)
    m = re.search(r"CyberZerk\{[^}]+\}", text)
    if m:
        print(f"[+] FLAG: {m.group(0)}")
