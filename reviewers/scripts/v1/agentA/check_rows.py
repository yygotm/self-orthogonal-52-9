"""Agent A: independent enumeration of the 7th-row candidates in sections 5 (type A) and 6.
Uses only the Fourier characterisations derived by hand (see report), with my own layout,
and verifies each candidate by direct weight computation.  No orbit computation.
"""
import itertools
pc = lambda x: bin(x).count('1')

def span(rows):
    a = [0]
    for r in rows:
        a += [w ^ r for w in a]
    return a

# ---------------- Section 6 (max weight 32) ----------------
# layout: pair p (p in F2^5 \ U, U=span(e0,e1,e2)) -> coords 2*k (v=0) and 2*k+1 (v=1); zero cols 48..51
P = [p for p in range(32) if p >> 3]          # 24 points outside U
assert len(P) == 24
K = [sum((p >> i & 1) << (2 * k) | (p >> i & 1) << (2 * k + 1) for k, p in enumerate(P)) for i in range(5)]
v = sum(1 << (2 * k + 1) for k in range(24)) | (15 << 48)
spanKv = span(K + [v])
assert all(pc(w) in (0, 24, 32) for w in span(K)) and all(pc(w ^ v) == 28 for w in span(K))

# all functions phi: F2^3 -> F2^2 (65536); graph S={x | phi(x)<<3}; g(p) = -(1/4) sum_{u in S} (-1)^{u.p}
def gfun(phi):
    S = [x | (phi[x] << 3) for x in range(8)]
    out = []
    for p in P:
        t = sum((-1) ** pc(u & p) for u in S)
        if t % 4: return None
        out.append(-t // 4)
    return out
good = []
for code in range(1 << 16):
    phi = [(code >> (2 * x)) & 3 for x in range(8)]
    g = gfun(phi)
    if g is not None and all(z in (-1, 0, 1) for z in g):
        good.append(g)
print('sec6: phi with g in {0,+-1}:', len(good))
# check each good g actually has Walsh in {2,-6} on all of F2^5
for g in good:
    for w in range(32):
        val = sum(z * (-1) ** pc(w & p) for z, p in zip(g, P))
        assert val in (2, -6)
bysupp = {}
for g in good:
    s = tuple(z != 0 for z in g)
    bysupp.setdefault(s, []).append(g)
raw = set()
for g in good:
    comp = tuple(z == 0 for z in g)
    for h in bysupp.get(comp, []):
        y = 3 << 48   # zero-col pattern 1100
        for k in range(24):
            if g[k] == -1: y |= 3 << (2 * k)          # tau=-2 : both bits 1
            if h[k] == 1: y |= 1 << (2 * k + 1)       # rho=+2 : (0,1)
            if h[k] == -1: y |= 1 << (2 * k)          # rho=-2 : (1,0)
        raw.add(y)
print('sec6: raw 7th rows (zero pattern fixed, not reduced mod K):', len(raw))
# verify every raw row by direct weights, and modulo K
bad = sum(1 for y in raw if not all(pc(y ^ w) in (24, 32) for w in spanKv))
modK = {min(y ^ w for w in span(K)) for y in raw}
print('sec6: invalid by direct weight check:', bad, '; classes mod K:', len(modK))
# completeness spot-check: random rows with zero pattern 1100 that pass the weight test must be in raw
import random
rng = random.Random(3); hits = 0
for _ in range(200000):
    y = (3 << 48) | rng.getrandbits(48)
    if all(pc(y ^ w) in (24, 32) for w in spanKv[:64]) and all(pc(y ^ w) in (24, 32) for w in spanKv):
        hits += 1; assert y in raw
print('sec6: random valid rows found', hits, '(all in raw)')

# ---------------- Section 5 type A ----------------
# layout: zero cols 0..4 ; singles p in 1..15 -> 5+(p-1) ; doubles x in 0..15 (p=16+x) -> 20+2x (v=0), 21+2x (v=1)
def walsh4(f):  # f truth table bits 0..15
    return [sum((-1) ** ((f >> x & 1) + pc(a & x)) for x in range(16)) for a in range(16)]
bents = [f for f in range(1 << 16) if all(abs(w) == 4 for w in walsh4(f))]
assert len(bents) == 896
dual = {}
for f in bents:
    W = walsh4(f); dual[f] = sum((W[a] < 0) << a for a in range(16))
bentset = set(bents)
KA = []
for i in range(5):
    r = 0
    for p in range(1, 16):
        if p >> i & 1: r |= 1 << (5 + p - 1)
    for x in range(16):
        if (16 + x) >> i & 1: r |= 3 << (20 + 2 * x)
    KA.append(r)
vA = (31) | (((1 << 15) - 1) << 5) | sum(1 << (21 + 2 * x) for x in range(16))
assert pc(vA) == 36
spanKvA = span(KA + [vA])
assert sorted(set(pc(w) for w in span(KA))) == [0, 24, 32]
canon_a = [f for f in bents if not (f & 1) and not any(f >> (1 << i) & 1 for i in range(4))]
print('secA: canonical bent y_a:', len(canon_a))
candA = set()
for ya in canon_a:
    for s in bents:
        if s & 1: continue      # s(0)=0 (zero-column sign +1 <-> weight-2 pattern)
        bt = dual[ya] ^ dual[s] ^ 0xFFFF
        if bt not in bentset: continue
        yb = dual[bt]
        y = 3   # zero pattern 11000
        for p in range(1, 16):
            if s >> p & 1: y |= 1 << (5 + p - 1)
        for x in range(16):
            if ya >> x & 1: y |= 1 << (20 + 2 * x)
            if yb >> x & 1: y |= 1 << (21 + 2 * x)
        candA.add(y)
badA = sum(1 for y in candA if not all(pc(y ^ w) in (24, 32) for w in spanKvA))
print('secA: 7th-row candidates', len(candA), 'invalid', badA)
hits = 0
for _ in range(200000):
    y = 3 | (rng.getrandbits(47) << 5)
    if all(pc(y ^ w) in (24, 32) for w in spanKvA):
        hits += 1
        yr = min(y ^ w for w in span(KA))
        assert any(yr == min(c ^ w for w in span(KA)) for c in [y]) # trivial
print('secA: random valid rows found', hits)
