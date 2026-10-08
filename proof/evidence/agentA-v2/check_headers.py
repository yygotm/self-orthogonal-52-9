# Agent A2 (v2 step 2): independent check of the headers actually compiled by predecessor B's run_all.sh
import re, sys, itertools
RUN = sys.argv[1]; DREP = sys.argv[2]
def arr(txt, name):
    m = re.search(r'%s\[[^\]]*\]\s*=\s*\{([^}]*)\}' % name, txt)
    return [int(x.replace('ULL',''),16) for x in m.group(1).split(',') if x.strip()]
def rank(vs):
    piv = {}
    r = 0
    for v in vs:
        while v:
            h = v.bit_length()-1
            if h in piv: v ^= piv[h]
            else: piv[h] = v; r += 1; break
    return r
def span(rows):
    out = {0}
    for r in rows:
        out |= {x ^ r for x in out}
    return out
pc = lambda x: bin(x).count('1')
for i in range(3):
    rows = [l.strip() for l in open(f'{DREP}/D-representative-{i}.txt') if l.strip()]
    assert all(len(r)==52 for r in rows)
    fw = [int(r[::-1],2) for r in rows]   # char j -> bit j
    bw = [int(r,2) for r in rows]          # char j -> bit 51-j
    for hname, arrname in ((f'h{i}.h','W'), (f'basis-gpt{i}.h','D')):
        txt = open(f'{RUN}/{hname}').read()
        B = arr(txt,'B'); W = arr(txt, arrname)
        Ws = set(W)
        orient = None
        for nm, g in (('char j=bit j', fw), ('char j=bit 51-j', bw)):
            if Ws == span(g) - {0}: orient = nm
        Dsp = span(W[:]) ; 
        rD = rank(W)
        dual_ok = all(pc(b & w) % 2 == 0 for b in B for w in W)
        r_all = rank(W + B)
        de = all(pc(w) % 4 == 0 for w in W)
        print(f'D{i} {hname}: |B|={len(B)} |W|={len(W)} distinct={len(Ws)} rankD={rD} doublyeven={de} '
              f'W==D-rep({orient}) B_in_Dperp={dual_ok} rank(D+B)={r_all} maxbit={max(x.bit_length() for x in B+W)}')
