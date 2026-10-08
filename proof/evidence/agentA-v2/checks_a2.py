# Agent A2: (1) Kurz Table 1 rows k=1..3 from scratch (multisets of points, 8-divisible, d>=24, eff. length n)
#           (2) weight distributions of D-representative-0/1/2 and A1's double-counting for q=0
#           (3) f=0 in Sec.6 forces b=4 (moments), Griesmer values
import itertools, sys
from fractions import Fraction
from collections import Counter
DREP = sys.argv[1]
def dot(a,b): return bin(a&b).count('1')&1
def kurz_row(k, nmax=54):
    pts = list(range(1, 2**k))
    # GL(k,2) as list of column-images of basis
    mats = []
    for cols in itertools.product(pts, repeat=k):
        # check invertible
        sp = {0}
        for c in cols: sp |= {x^c for x in sp}
        if len(sp) == 2**k: mats.append(cols)
    def app(M, p):
        r = 0
        for i in range(k):
            if p>>i & 1: r ^= M[i]
        return r
    perms = [tuple(app(M,p) for p in pts) for M in mats]
    res = Counter()
    wts = [w for w in range(24, nmax+1, 8)]
    seen = set()
    for wv in itertools.product(wts, repeat=len(pts)):
        # sum_u w(u) = 2^(k-1) n
        s = sum(wv)
        if s % 2**(k-1): continue
        n = s // 2**(k-1)
        if n > nmax: continue
        # m(p) = (1/2^k) sum_u F(u)(-1)^{u.p}, F(0)=n, F(u)=n-2w(u)
        m = []
        ok = True
        for p in [0]+pts:
            t = n + sum((n-2*w)*(-1)**dot(u,p) for u,w in zip(pts,wv))
            if t % 2**k or t < 0: ok=False; break
            m.append(t//2**k)
        if not ok or m[0] != 0: continue
        mm = tuple(m[1:])
        # dimension exactly k: support spans F2^k
        sp = {0}
        for p,c in zip(pts,mm):
            if c: sp |= {x^p for x in sp}
        if len(sp) != 2**k: continue
        canon = min(tuple(mm[pts.index(q)-0] if False else 0 for q in pts) for _ in [0]) # placeholder
        # canonical form under GL: multiset as sorted (point->mult) images
        best = None
        for P in perms:
            img = [0]*len(pts)
            for i,p in enumerate(pts): img[P[i]-1] = mm[i]
            img = tuple(img)
            if best is None or img < best: best = img
        if best in seen: continue
        seen.add(best)
        res[n] += 1
    return dict(sorted(res.items()))
for k in (1,2,3):
    print('Kurz row k=%d (multisets, d>=24):' % k, kurz_row(k))
# (2)
def load(i):
    rows = [l.strip() for l in open(f'{DREP}/D-representative-{i}.txt') if l.strip()]
    return [int(r[::-1],2) for r in rows]
def span(rows):
    out=[0]
    for r in rows: out += [x^r for x in out]
    return out
wd = {}
for i in range(3):
    W = Counter(bin(x).count('1') for x in span(load(i)))
    rows = [l.strip() for l in open(f'{DREP}/D-representative-{i}.txt') if l.strip()]
    cols = Counter(''.join(r[j] for r in rows) for j in range(52))
    z = cols.get('0'*len(rows),0)
    b = sum(c*(c-1)//2 for col,c in cols.items() if col != '0'*len(rows))
    wd[i] = W
    print(f'D{i}: weights {dict(sorted(W.items()))} zerocols={z} b={b} A32+A36={W[32]+W[36]}')
print('q=0 double count: 511*51 =', 511*51, ' /255 =', Fraction(511*51,255))
# also with A24: sum_H A24(H) must be divisible by 255 -> 204x0+172x1+174x2, x0+x1+x2=511
sols = [(x0,x1,511-x0-x1) for x0 in range(512) for x1 in range(512-x0) if (204*x0+172*x1+174*(511-x0-x1))%255==0]
print('A24-only constraint solutions count:', len(sols))
# (3) Sec 6 f=0: n=52, no zero col, weights 24,32 only
A32 = Fraction(128*52 - 24*255, 8); A24 = 255 - A32
b = Fraction(576*A24 + 1024*A32, 64) - (52*52+52)
print('f=0: A24=%s A32=%s 2b=%s b=%s' % (A24, A32, b, b/2))
g = lambda k,d: sum(-(-d//2**i) for i in range(k))
print('Griesmer g(8,28)=%d g(8,24)=%d g(9,24)=%d g(8,32)=%d' % (g(8,28), g(8,24), g(9,24), g(8,32)))
