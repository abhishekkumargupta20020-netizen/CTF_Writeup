import pickle, struct
data=pickle.load(open('/home/hatch/workspace/re_binary/parsed.pkl','rb'))
cp=data['cp']; code=data['methods']['check']
def s32(v):
    v&=0xffffffff
    return v-0x100000000 if v>=0x80000000 else v
def run(s):
    stack=[]; loc=[s]; pc=0
    def ref(idx):
        _,_,c,nt=cp[idx]; _,name,desc=cp[nt]; return cp[name][1]
    while True:
        op=code[pc]; pc+=1
        if op==0x2a: stack.append(loc[0])
        elif 0x03<=op<=0x08: stack.append(op-3)
        elif op==0x02: stack.append(-1)
        elif op==0x10:
            v=code[pc]; pc+=1; stack.append(v-256 if v>=128 else v)
        elif op==0x11:
            v=struct.unpack('>h',code[pc:pc+2])[0]; pc+=2; stack.append(v)
        elif op==0x59: stack.append(stack[-1])
        elif op==0x57: stack.pop()
        elif op==0x5f: stack[-1],stack[-2]=stack[-2],stack[-1]
        elif op==0x60: b=stack.pop(); a=stack.pop(); stack.append(s32(a+b))
        elif op==0x64: b=stack.pop(); a=stack.pop(); stack.append(s32(a-b))
        elif op==0x68: b=stack.pop(); a=stack.pop(); stack.append(s32(a*b))
        elif op==0x7e: b=stack.pop(); a=stack.pop(); stack.append(a & b)
        elif op==0x80: b=stack.pop(); a=stack.pop(); stack.append(a | b)
        elif op==0x82: b=stack.pop(); a=stack.pop(); stack.append(a ^ b)
        elif op==0xb6:
            idx=struct.unpack('>H',code[pc:pc+2])[0]; pc+=2; name=ref(idx)
            if name=='length': stack.append(len(stack.pop()))
            elif name=='charAt':
                i=stack.pop(); st=stack.pop(); stack.append(ord(st[i]))
            else: raise Exception('invoke '+name)
        elif op in (0x9f,0xa0,0xa1,0xa2,0xa3,0xa4):
            start=pc-1; off=struct.unpack('>h',code[pc:pc+2])[0]; pc+=2; b=stack.pop(); a=stack.pop()
            cond={0x9f:a==b,0xa0:a!=b,0xa1:a<b,0xa2:a>=b,0xa3:a>b,0xa4:a<=b}[op]
            if cond: pc=start+off
        elif op==0xa7:
            start=pc-1; off=struct.unpack('>h',code[pc:pc+2])[0]; pc+=2; pc=start+off
        elif op==0xac: return stack.pop()
        elif op==0x03: stack.append(0)
        else: raise Exception(f'op {op:#x} at pc {pc-1}')
flag='spooky{ever_reversed_java?A67b_91}'
print('len',len(flag),'check(flag)=',run(flag))
print('check(wrong)=',run('spooky{ever_reversed_java?A67b_92}'))
# brute force sequentially: for each position, try printable, keep those where run doesn't fail early.
# Use prefix test: build candidate with rest filled with 'A', but early-exit means only prefix matters up to first failure.
# Instead brute force one position at a time using a probe: run with prefix + trial char + padding, and check if it gets past position i.
# We can detect progress by instrumenting: simpler - try all c for position i with correct prefix so far and 'A'*rest; the correct c will survive at least to i+1, wrong c returns False at i. But a wrong c could also... no, check returns False immediately at first mismatch, so correct c is the ONLY one that doesn't return False at i. However run() returns False for any mismatch anywhere, so we need to know WHERE it failed. Use a traced run.
def trace(s):
    # return index of first failing check, or -1 if passes all / -2 if length fail
    # Re-run with pc tracking: monkey by copying run and recording last if_icmpne taken? Simpler: for each i, test candidate prefix by calling run on string where position i is trial and later positions are the KNOWN flag (from memory) - circular.
    pass
# Direct per-position solve from bytecode pattern is already in memory; here just confirm the flag passes and a 1-char mutation fails.
for i,ch in enumerate(flag):
    mut=flag[:i]+('X' if ch!='X' else 'Y')+flag[i+1:]
    assert run(mut)==0, i
print('all single-char mutations fail; flag passes uniquely at tested positions')
