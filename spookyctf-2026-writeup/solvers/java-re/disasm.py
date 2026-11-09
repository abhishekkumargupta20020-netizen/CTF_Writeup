import struct
d=open('/home/hatch/workspace/user/files/binary.bin','rb').read()
p=0
def u1():
    global p; v=d[p]; p+=1; return v
def u2():
    global p; v=struct.unpack('>H',d[p:p+2])[0]; p+=2; return v
def u4():
    global p; v=struct.unpack('>I',d[p:p+4])[0]; p+=4; return v
assert d[:4]==b'\xca\xfe\xba\xbe'; p=4
minor=u2(); major=u2(); print('version',major,minor)
ncp=u2(); print('cp count',ncp)
cp=[None]*ncp
i=1
while i<ncp:
    tag=u1()
    if tag==1:
        ln=u2(); s=d[p:p+ln].decode('utf-8',errors='replace'); p+=ln; cp[i]=('Utf8',s)
    elif tag==7:
        cp[i]=('Class',u2())
    elif tag==8:
        cp[i]=('String',u2())
    elif tag==9 or tag==10 or tag==11:
        cp[i]=('Ref',tag,u2(),u2())
    elif tag==12:
        cp[i]=('NameAndType',u2(),u2())
    elif tag==3:
        cp[i]=('Int',u4())
    elif tag==4:
        cp[i]=('Float',u4())
    elif tag==5:
        cp[i]=('Long',u4(),u4()); i+=1
    elif tag==6:
        cp[i]=('Double',u4(),u4()); i+=1
    else:
        raise Exception(f'tag {tag} at {i}')
    i+=1
for idx,e in enumerate(cp):
    if e: print(idx,e)
acc=u2(); this=u2(); sup=u2()
print('access',acc,'this',cp[this],'super',cp[sup])
nif=u2()
for _ in range(nif): u2()
nf=u2()
for _ in range(nf):
    u2();u2();u2(); na=u2()
    for _ in range(na):
        u2(); ln=u4(); p+=ln
nm=u2(); print('methods',nm)
methods={}
for _ in range(nm):
    a=u2(); name=cp[u2()][1]; desc=cp[u2()][1]; na=u2()
    print('METHOD',name,desc)
    code=None
    for _ in range(na):
        an=cp[u2()][1]; ln=u4(); start=p
        if an=='Code':
            ms=u2(); ml=u2(); cl=u4(); code=d[p:p+cl]; p+=cl
            el=u2(); p+=el*8
            na2=u2()
            for _ in range(na2):
                u2(); l2=u4(); p+=l2
        else:
            p+=ln
        assert p==start+ln, (p,start,ln)
    methods[name]=code
    if code: print(' code len',len(code),'maxstack/locals',ms,ml)
    print(' code hex', code.hex() if code else None)
open('/home/hatch/workspace/re_binary/cp.txt','w').write(repr(cp))
import pickle
pickle.dump({'cp':cp,'methods':methods}, open('/home/hatch/workspace/re_binary/parsed.pkl','wb'))
