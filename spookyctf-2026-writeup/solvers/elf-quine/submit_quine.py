#!/usr/bin/env python3
"""Submit the 105-byte ELF quine to 3.129.162.36:31903.
Protocol: connect, read banner, send 'SIZE <n>\n', then exactly n raw bytes.
"""
import socket, sys
HOST, PORT = "3.129.162.36", 31903
data = open(sys.argv[1] if len(sys.argv) > 1 else "quine105", "rb").read()
print(f"quine: {len(data)} bytes")
s = socket.create_connection((HOST, PORT), timeout=10)
s.settimeout(5)
banner = b""
try:
    while b"\n" not in banner or len(banner) < 20:
        chunk = s.recv(4096)
        if not chunk:
            break
        banner += chunk
        if len(banner) > 4096:
            break
except socket.timeout:
    pass
print("banner:", banner)
s.sendall(f"SIZE {len(data)}\n".encode() + data)
resp = b""
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        resp += chunk
except socket.timeout:
    pass
print("reply:", resp.decode(errors="replace"))
