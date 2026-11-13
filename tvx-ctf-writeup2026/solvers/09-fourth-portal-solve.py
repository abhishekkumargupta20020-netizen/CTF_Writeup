import csv, itertools, json, pathlib, hashlib, hmac
base=pathlib.Path("/home/hatch/workspace/fourth-portal")
P=257
def load(name):
    pts=[]
    with open(base/name) as f:
        for row in csv.DictReader(f):
            pts.append((int(row['X'])%P, int(row['Z'])%P))
    return pts
def solve_poly(pts):
    n=len(pts)
    A=[[pow(x,i,P) for i in range(n)]+[z] for x,z in pts]
    for col in range(n):
        piv=next(r for r in range(col,n) if A[r][col]%P)
        A[col],A[piv]=A[piv],A[col]
        inv=pow(A[col][col],-1,P); A[col]=[(v*inv)%P for v in A[col]]
        for r in range(n):
            if r!=col and A[r][col]:
                f=A[r][col]; A[r]=[(A[r][j]-f*A[col][j])%P for j in range(n+1)]
    return [A[i][n] for i in range(n)]
def ev(c,x): return sum(ci*pow(x,i,P) for i,ci in enumerate(c))%P
coeffs={}
for world,fn in [("Overworld","overworld/beacons.csv"),("Nether","nether/beacons.csv"),("End","the_end/beacons.csv")]:
    pts=load(fn); best=None
    for combo in itertools.combinations(range(16),8):
        try: c=solve_poly([pts[i] for i in combo])
        except Exception: continue
        if any(v>255 for v in c): continue
        m=[i for i,(x,z) in enumerate(pts) if ev(c,x)==z]
        if best is None or len(m)>len(best[1]): best=(c,m)
    coeffs[world]=best[0]; print(world, best[0], "matches", len(best[1]))
O,N,E=coeffs["Overworld"],coeffs["Nether"],coeffs["End"]
H=list(bytes.fromhex(open(base/"the_echo/core.hex").read().replace(" ","").replace("\n","")))
frame=bytes([v for i in range(8) for v in (O[i],N[i],E[i],H[i])])
print("frame",frame.hex())
v=json.load(open(base/"the_echo/vault.json"))
prk=hmac.new(bytes.fromhex(v["salt_hex"]),frame,hashlib.sha256).digest()
t=b""; okm=b""; c=1
while len(okm)<32:
    t=hmac.new(prk,t+v["info_ascii"].encode()+bytes([c]),hashlib.sha256).digest(); okm+=t; c+=1
key=okm[:32]; print("hkdf key",key.hex())
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
pt=AESGCM(key).decrypt(bytes.fromhex(v["nonce_hex"]), bytes.fromhex(v["ciphertext_hex"])+bytes.fromhex(v["tag_hex"]), v["aad_ascii"].encode())
print(pt.decode())
