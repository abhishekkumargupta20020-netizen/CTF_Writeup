# Reflected Storm — DNS Reflection PCAP Analysis

- **Competition:** SecLeaf Q4 2026
- **Date investigated:** 31 October 2026
- **Category:** Network forensics / DDoS analysis
- **Artifact:** `reflected-storm.pcap` (685,604 bytes)
- **Status:** Analysis performed; candidate flag rejected; final flag not recovered

## Objective

Analyse a packet capture showing a DNS reflection/amplification pattern and identify the victim and reflector infrastructure.

## 1. Capture summary

Recovered analysis reported:

```text
Total packets: 1,340
DNS ANY requests: 600
DNS responses: 600
Normal DNS exchange packets: 70
Victim/source address: 10.0.55.200
Destination service: UDP/53
```

The 600 requests were DNS `ANY` queries with a 75-byte payload. The 600 corresponding responses were approximately 1,014 bytes.

Amplification ratio:

\[
\frac{1014}{75} \approx 13.52
\]

The request/response count was 1:1, while the response size was about 13.52 times the request size.

## 2. Reflector candidates and counts

| Reflector | Request count |
|---|---:|
| `192.0.2.17` | 119 |
| `198.51.100.10` | 118 |
| `198.51.100.22` | 133 |
| `203.0.113.5` | 120 |
| `203.0.113.88` | 110 |
| **Total** | **600** |

These IP ranges are documentation ranges (RFC 5737). In a synthetic CTF capture they function as illustrative reflector addresses, not real routable reflectors.

A separate normal DNS exchange involved:

```text
10.0.1.50 <-> 10.0.1.1
```

It accounted for 70 packets and should not be mixed with the 600-packet reflection stream.

## 3. Reproduction

Install Scapy:

```bash
python3 -m pip install scapy
```

Run:

```bash
python3 ../solvers/pcap_dns_reflection.py ../artifacts/reflected-storm.pcap
```

The script groups DNS ANY requests by source address, reports DNS response sizes, and summarizes candidate reflectors.

Useful Wireshark display filters:

```text
dns
dns.qry.type == 255
udp.port == 53
ip.addr == 10.0.55.200
```

Useful tshark commands:

```bash
capinfos reflected-storm.pcap
tshark -r reflected-storm.pcap -Y 'dns.qry.type == 255'
tshark -r reflected-storm.pcap -Y 'dns.flags.response == 1'
```

## 4. Candidate flag and rejection

An earlier candidate was:

```text
SecLeaf{10.0.55.200_5_reflectors}
```

It was rejected. The packet analysis alone did not establish the exact expected flag string.

## 5. Next steps

Revisit the challenge wording and determine whether the requested answer is:
- victim IP,
- number of reflectors,
- ordered reflector list,
- amplification factor,
- or a specific combination.

Do not concatenate values into a flag without matching the prompt's required semantics.

## 6. Status

The network pattern and IPs were recovered, but the candidate flag was rejected and no accepted flag is preserved.
