#!/usr/bin/env python3
# Challenge Author: gl1tt3rpuff0
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
# ender chest 
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
#  You found a world seed nobody could guess and used it as
#  the key to his chests. Elliptic curves are unbreakable, so
#  the curve the server admin picked must be fine, right?... RIGHT??? 
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
import os, hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from params import p, a, b, G, d

FLAG  = open("flag.txt").read().strip()
REALFLAG = open("realflag.txt").read().strip()


def chest(msg: str, key_src: bytes) -> str:
    key = hashlib.sha256(key_src).digest()
    iv  = os.urandom(16)
    return (iv + AES.new(key, AES.MODE_CBC, iv).encrypt(pad(msg.encode(), 16))).hex()


Q = d * G 
ender_chest = chest(FLAG,  str(d).encode())    # opens with the world seed
shulker_box = chest(REALFLAG, str(Q[0]).encode()) # opens with the x coordinate

