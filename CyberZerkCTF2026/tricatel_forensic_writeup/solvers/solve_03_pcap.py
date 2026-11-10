#!/usr/bin/env python3
"""
Challenge 03 - Farewell message / Appels a l'aide
File: challenges/appels_a_l_aide.pcap
Category: Forensics / Network Forensics (PCAP)

No tshark/scapy required - parses the pcap + Ethernet/IP/TCP manually.
Only 12 packets, only packet 6 carries a payload: an HTTP POST
to /adieu.php on localhost:9999, in clear text.
Alternative with tshark: tshark -r file.pcap -Y http -T fields -e http.file_data
Alternative with Wireshark: Follow > TCP Stream
"""
import re, struct, sys

path = sys.argv[1] if len(sys.argv) > 1 else "challenges/appels_a_l_aide.pcap"
data = open(path, "rb").read()

# Skip 24-byte pcap global header
off, pkt_no = 24, 0
payloads = []
while off + 16 <= len(data):
    _, _, incl_len, _ = struct.unpack("<IIII", data[off:off+16])
    off += 16
    pkt = data[off:off+incl_len]; off += incl_len; pkt_no += 1
    if len(pkt) < 14: continue
    ethertype = struct.unpack("!H", pkt[12:14])[0]
    if ethertype != 0x0800: continue  # IPv4 only (packets 1-2 are IPv6 noise)
    ip = pkt[14:]
    ihl = (ip[0] & 0x0F) * 4
    if ip[9] != 6: continue  # TCP only
    tcp = ip[ihl:]
    doff = ((struct.unpack("!H", tcp[12:14])[0] >> 12) & 0xF) * 4
    payload = tcp[doff:]
    if payload:
        payloads.append(payload)
        print(f"Packet {pkt_no} payload:\n{payload.decode(errors='replace')}\n")

full = b"".join(payloads).decode(errors="replace")
m = re.search(r"CyberZerk\{[^}]+\}", full)
if m:
    print(f"[+] FLAG: {m.group(0)}")
