#!/usr/bin/env python3
"""TraceVX solver: submits the 10 evidence-derived answers to the analyst
service (nc 169.58.174.26 1337) and prints the flag.
Answers were derived offline from traceVX.ad1 - see WRITEUP.md for the
step-by-step derivation of each one. 'hint' does not consume an attempt.
"""
import re, socket, sys

HOST, PORT = "169.58.174.26", 1337
ANSWERS = [
    "Ahmed",                                              # Q1 account (SRU/prefetch/MFT/task all line up 14:3x)
    "login-microsoftonline.secure-verify.cc",             # Q2 XOR 0x98 url_reputation.bin (key=sum(C2 octets)&0xff=152)
    "2026-09-17T14:31:51Z",                               # Q3 Edge History jsonl, load just before 14:32:18 PS run
    "powershell.exe",                                     # Q4 Prefetch POWERSHELL.EXE-9A3B.pf FirstRun 14:32:18, Ahmed
    "stage.cmdline",                                      # Q5 $MFT/USN: Temp\k29x8 CREATE 14:32:20, DELETE 14:32:27
    "Navigator.exe",                                      # Q6 dropped in ProgramData\Microsoft\UpdateCache 14:32:36; carved PE OriginalFilename=NavigatorCore.dll
    "411ff3850c2ed96028e4f39184fed07c3fdacf56936e03581ce479c6ed7ab8cd",  # Q7 sha256 of carved, gunzipped PE at disk.img 0x4D000
    "TraceTelemetry",                                     # Q8 logon task, Author Ahmed, 14:32:40, runs Navigator.exe
    "185.192.48.239:443",                                 # Q9 C2 in carved PE + SRUDB for Navigator.exe
    "8388608",                                            # Q10 SRU SUM outbound to C2: Navigator 5242880 + AdaptConductor 3145728
]

def recv_until(sock, needle=b"answer>", timeout=15):
    sock.settimeout(timeout); data = b""
    while needle not in data:
        chunk = sock.recv(4096)
        if not chunk: break
        data += chunk
    return data

def main():
    s = socket.create_connection((HOST, PORT), timeout=20)
    banner = recv_until(s).decode(errors="ignore")
    transcript = banner
    for ans in ANSWERS:
        s.sendall(b"hint\n"); transcript += recv_until(s).decode(errors="ignore")
        s.sendall((ans + "\n").encode())
        resp = recv_until(s, timeout=15).decode(errors="ignore"); transcript += resp
        if "CONFIRMED" not in resp:
            # one attempt may remain; report and stop rather than guess blindly
            print(f"[-] answer not confirmed: {ans}\n{resp}"); s.close(); return 1
    # final message may arrive with the last CONFIRMED or after
    try:
        s.settimeout(5); tail = s.recv(8192).decode(errors="ignore"); transcript += tail
    except Exception: pass
    s.close()
    m = re.search(r"(?:FLAG:\s*)?(TVX\{[^}]+\})", transcript)
    if not m:
        print("[-] no flag in transcript\n" + transcript); return 1
    print(m.group(1)); return 0

if __name__ == "__main__":
    sys.exit(main())
