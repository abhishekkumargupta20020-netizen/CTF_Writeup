import subprocess, urllib.parse, re, sys
def fetch(u):
    q=urllib.parse.urlencode({'url':u})
    url=f'https://restructuration.cyberzerk.fr/?{q}'
    try:
        out=subprocess.check_output(['curl','-s','--max-time','15',url], timeout=20).decode('utf-8','ignore')
    except Exception as e:
        return f"ERR {e}"
    pre=re.findall(r'<pre[^>]*>(.*?)</pre>', out, flags=re.S)
    err=re.findall(r'class="err"[^>]*>(.*?)</', out, flags=re.S)
    # strip html for pre
    pre_clean=[re.sub(r'<[^>]+>',' ',p) for p in pre]
    return f"PRE={pre_clean} ERR={err}"

tests=sys.argv[1:]
for c in tests:
    print(f"\n=== {c} ===")
    print(fetch(c))
