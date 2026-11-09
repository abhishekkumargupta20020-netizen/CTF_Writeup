# Fear-of-math / non-associative DH challenge
# Key insight: Ma = conj(a,g), Mb = conj(b,g) hide a,b, but the associator
# shared key K = assoc(a,g,Mb) * mu^{-a0} simplifies, after expressing
# a's b,c (and b's b,c) via Ma/Mb, to a public-only formula:
#   P = Cg*Ma_b - Bg*Ma_c
#   Q = Cg*Mb_b - Bg*Mb_c
#   R = Ma_c*Mb_b - Ma_b*Mb_c
#   K = mu^{2*G} * (P + R - Q) / (mu - 1)  mod q
# Verified on random a,b: formula matches shared_key(a,g,Mb) exactly.
import hashlib
p  = 1099511640127
q  = 340282370743387819766807672197819448083
mu = 145131588818725534535896278189401302887
inv_mu = pow(mu - 1, -1, q)
g = (739614761553, 87671554642066775345573935247301052006, 85147831812679793672994902968842668105, 71719252422814786229685092573269912498)
Ma = (739614761553, 312134278234991743315140578529310805510, 126369916264124511285906038626254340804, 134610391672392132751140546119763556201)
Mb = (739614761553, 244699321175961590059239024660541174646, 335110553885376877685776857080059519613, 55552870219389410159628089275413443533)
ct = bytes.fromhex("9915497c4929fceea2ab3cfd06a744ac9ff6d8de290c8911d18b746d885fb3f5508282d2da0adff5fa15")
Bg, Cg = g[1], g[2]
P = (Cg*Ma[1] - Bg*Ma[2]) % q
Q = (Cg*Mb[1] - Bg*Mb[2]) % q
R = (Ma[2]*Mb[1] - Ma[1]*Mb[2]) % q
K = pow(mu, 2*g[0], q) * (P + R - Q) % q * inv_mu % q
print("K =", K)
mask = hashlib.shake_256(b"loop|" + K.to_bytes(32, "big")).digest(len(ct))
print("flag =", bytes(x ^ y for x, y in zip(ct, mask)))
