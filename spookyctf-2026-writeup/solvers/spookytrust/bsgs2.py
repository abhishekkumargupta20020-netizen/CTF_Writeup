import sys
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import utils
from fastecdsa.curve import P384
from fastecdsa.point import Point

G = P384.G; n = P384.q; p = P384.p; a = P384.a; b = P384.b
M = 1 << 20
def load_cert(f): return x509.load_pem_x509_certificate(open(f,'rb').read())
def load_csr(f): return x509.load_pem_x509_csr(open(f,'rb').read())

# sanity: known d
T = 12345 * G
print('sanity: 12345*G built', flush=True)

print('building baby-step table (2^20)...', flush=True)
table = {}
cur = 0*G
for j in range(M):
    table[(cur.x, cur.y)] = j
    cur = cur + G
step = M*G
neg_step = Point(step.x, (-step.y) % p, curve=P384)
print('table built', flush=True)

def bsgs(T):
    cur = T
    for i in range(M):
        j = table.get((cur.x, cur.y))
        if j is not None:
            d = i*M + j
            if d*G == T:
                return d
        cur = cur + neg_step
    return None

print('sanity bsgs(12345*G) =', bsgs(T), flush=True)

Qs = {}
for i in range(1,5):
    pub = load_cert(f'ST-ISS-0{i}.pem').public_key().public_numbers()
    Qs[f'ISS-0{i}'] = Point(pub.x, pub.y, curve=P384)
rp = load_cert('root.pem').public_key().public_numbers()
Qs['root'] = Point(rp.x, rp.y, curve=P384)
print('--- d-search (d < 2^40) ---', flush=True)
for label, Q in Qs.items():
    print(f'{label}: d = {bsgs(Q)}', flush=True)

def R_candidates(r):
    out = []
    for x in (r, r+n):
        if x >= p: continue
        rhs = (pow(x,3,p) + a*x + b) % p
        y = pow(rhs, (p+1)//4, p)
        if (y*y) % p == rhs:
            out.append(Point(x, y, curve=P384))
            if y != 0:
                out.append(Point(x, (-y) % p, curve=P384))
    return out

sigs = []
r, s = utils.decode_dss_signature(load_cert('root.pem').signature)
sigs.append(('root self', r))
for i in range(1,5):
    r, s = utils.decode_dss_signature(load_cert(f'ST-ISS-0{i}.pem').signature)
    sigs.append((f'cert-0{i}', r))
    r, s = utils.decode_dss_signature(load_csr(f'ST-ISS-0{i}.csr.pem').signature)
    sigs.append((f'csr-0{i}', r))
print('--- k-search (k < 2^40) ---', flush=True)
for label, r in sigs:
    found = None
    for R in R_candidates(r):
        k = bsgs(R)
        if k is not None:
            found = k; break
    print(f'{label}: k = {found}', flush=True)
print('BSGS2 DONE', flush=True)
