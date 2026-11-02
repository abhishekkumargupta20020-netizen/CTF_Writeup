#!/usr/bin/env python3
"""Summarize DNS ANY request/response patterns in reflected-storm.pcap."""
import argparse
from collections import Counter, defaultdict
from scapy.all import PcapReader, IP, UDP, DNS, DNSQR, DNSRR

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pcap")
    args = ap.parse_args()

    any_queries = []
    responses = []
    other_dns = 0
    with PcapReader(args.pcap) as packets:
        for p in packets:
            if not (p.haslayer(IP) and p.haslayer(UDP) and p.haslayer(DNS)):
                continue
            d = p[DNS]
            ip = p[IP]
            udp = p[UDP]
            if d.qr == 0 and d.qd and getattr(d.qd, "qtype", None) == 255:
                any_queries.append((ip.src, ip.dst, len(bytes(p)), udp.sport, udp.dport))
            elif d.qr == 1:
                responses.append((ip.src, ip.dst, len(bytes(p))))
            else:
                other_dns += 1

    src_counts = Counter(x[0] for x in any_queries)
    dst_counts = Counter(x[1] for x in any_queries)
    response_src_counts = Counter(x[0] for x in responses)
    response_dst_counts = Counter(x[1] for x in responses)

    print(f"DNS ANY requests: {len(any_queries)}")
    print(f"DNS responses:    {len(responses)}")
    print(f"Other DNS:        {other_dns}")
    print("\nANY query sources:")
    for ip, n in src_counts.most_common():
        print(f"  {ip:16s} {n}")
    print("\nANY query destinations:")
    for ip, n in dst_counts.most_common():
        print(f"  {ip:16s} {n}")
    if any_queries and responses:
        qavg = sum(x[2] for x in any_queries) / len(any_queries)
        ravg = sum(x[2] for x in responses) / len(responses)
        print(f"\nAverage packet size: query={qavg:.2f}, response={ravg:.2f}")
        if qavg:
            print(f"Size ratio: {ravg/qavg:.2f}x")
    print("\nResponse sources:")
    for ip, n in response_src_counts.most_common():
        print(f"  {ip:16s} {n}")
    print("\nResponse destinations:")
    for ip, n in response_dst_counts.most_common():
        print(f"  {ip:16s} {n}")

if __name__ == "__main__":
    main()
