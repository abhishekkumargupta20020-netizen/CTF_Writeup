import mmap, os, hashlib

SRC = "/home/hatch/workspace/spooked2/spooked2.lime"
PNG_OUT = "/home/hatch/workspace/spooked2/carved_png"
JPG_OUT = "/home/hatch/workspace/spooked2/carved_jpg"
os.makedirs(PNG_OUT, exist_ok=True)
os.makedirs(JPG_OUT, exist_ok=True)

PNG_SIG = b"\x89PNG\r\n\x1a\n"
PNG_END = b"IEND\xaeB`\x82"
JPG_SIG = b"\xff\xd8\xff"
JPG_END = b"\xff\xd9"

def carve(sig, end, kind, minlen, maxlen, outdir):
    found = []
    seen = {}
    with open(SRC, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        pos = 0
        while True:
            i = mm.find(sig, pos)
            if i < 0:
                break
            j = mm.find(end, i + len(sig))
            if j < 0:
                pos = i + 1
                continue
            endpos = j + len(end)
            length = endpos - i
            if minlen <= length <= maxlen:
                data = mm[i:endpos]
                h = hashlib.md5(data).hexdigest()
                if h not in seen:
                    seen[h] = i
                    fn = os.path.join(outdir, f"{kind}_{i:012x}_{length}.{'png' if kind=='png' else 'jpg'}")
                    with open(fn, "wb") as g:
                        g.write(data)
                    found.append((i, length, h, fn))
            pos = i + 1
        mm.close()
    return found

pngs = carve(PNG_SIG, PNG_END, "png", 2000, 40_000_000, PNG_OUT)
jpgs = carve(JPG_SIG, JPG_END, "jpg", 2000, 40_000_000, JPG_OUT)
print(f"PNG carved: {len(pngs)}", flush=True)
print(f"JPEG carved: {len(jpgs)}", flush=True)
with open("/home/hatch/workspace/spooked2/carve_log.txt", "w") as g:
    g.write("PNG\n")
    for i, length, h, fn in sorted(pngs, key=lambda x: -x[1]):
        g.write(f"0x{i:x}\t{length}\t{h}\t{fn}\n")
    g.write("JPEG\n")
    for i, length, h, fn in sorted(jpgs, key=lambda x: -x[1]):
        g.write(f"0x{i:x}\t{length}\t{h}\t{fn}\n")
print("done", flush=True)
