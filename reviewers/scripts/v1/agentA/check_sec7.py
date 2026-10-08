"""Agent A: independent checks for PROOF.md section 7 (and D0..D2 facts)."""
import sys, time, random, json, pathlib
from itertools import combinations
import numpy as np

pc = lambda x: bin(x).count('1')
N51 = (1 << 51) - 1

def span(rows):
    a = [0]
    for r in rows:
        a += [w ^ r for w in a]
    return a

def rref(vecs):
    piv = {}
    for x in vecs:
        while x:
            p = x.bit_length() - 1
            if p in piv: x ^= piv[p]
            else: piv[p] = x; break
    return piv

def red(x, piv):
    for p in sorted(piv, reverse=True):
        if x >> p & 1: x ^= piv[p]
    return x

def wd(words):
    d = {}
    for w in words: d[pc(w)] = d.get(pc(w), 0) + 1
    return dict(sorted(d.items()))

# D0: cyclic [51,8,24] from the generator polynomial quoted in triple_search.py (data only)
poly = sum(1 << j for j in [43,42,41,37,36,33,30,29,27,26,25,22,21,20,19,17,16,13,12,10,7,5,4,0])
D0 = [poly << s for s in range(8)]
W0 = span(D0)
assert len(set(W0)) == 256
print('D0 weight distribution', wd(W0), 'support', pc(sum(W0) and (lambda: (lambda o: o)(0))() or 0) if False else '')
union = 0
for w in W0: union |= w
print('D0 nonzero coordinates', pc(union), '(coordinate 51 is the zero column)')
# cyclic shift invariance
rot = lambda x, k=1: ((x << k) | (x >> (51 - k))) & N51
piv0 = rref(D0)
assert all(red(rot(r), piv0) == 0 for r in D0)
# triples
cols = [sum((r >> j & 1) << i for i, r in enumerate(D0)) for j in range(51)]
assert len(set(cols)) == 51 and 0 not in cols
look = {c: j for j, c in enumerate(cols)}
tri = sorted({tuple(sorted((i, j, look[cols[i] ^ cols[j]]))) for i, j in combinations(range(51), 2) if (cols[i] ^ cols[j]) in look})
cover = sorted(x for t in tri for x in t)
print('triples', len(tri), 'partition', cover == list(range(51)))
masks = [sum(1 << j for j in t) for t in tri]

# ---------- T_h properties
rng = random.Random(1)
for _ in range(20000):
    h = sum(1 << j for j in rng.sample(range(52), 6))
    x = rng.getrandbits(52); y = rng.getrandbits(52)
    T = lambda z: z ^ h if pc(z & h) % 2 else z
    assert pc(T(x) & T(y)) % 2 == pc(x & y) % 2 and T(T(x)) == x
    if pc(x) % 2 == 0:
        d = pc(T(x)) - pc(x)
        assert d in (-4, 0, 4) and (pc(T(x)) - pc(x)) % 4 == 0
print('T_h: inner product, involution, weight change in {-4,0,4} for even words: OK (random 20000)')

# ---------- h1, h2
for name, h in (('h1', 2251816993685511), ('h2', 2251834173685767)):
    T = lambda z: z ^ h if pc(z & h) % 2 else z
    Dh = [T(r) for r in D0]
    Wh = span(Dh)
    colsh = [sum((r >> j & 1) << i for i, r in enumerate(Dh)) for j in range(52)]
    pairs = sum(1 for i, j in combinations(range(52), 2) if colsh[i] == colsh[j])
    so = all(pc(a & b) % 2 == 0 for a in Dh for b in Dh)
    print(name, 'weight', pc(h), 'contains coord 51', bool(h >> 51 & 1), 'support', [j for j in range(52) if h >> j & 1],
          'T_h(D0) wd', wd(Wh), 'zero cols', colsh.count(0), 'equal-col pairs b', pairs, 'SO', so,
          'rank', len(rref(Dh)))

# ---------- count of admissible h (weight 6, contains 51, T_h(D0) keeps d>=24)
low = [w for w in W0 if pc(w) == 24]
bad = set()
for w in low:
    sup = [j for j in range(51) if w >> j & 1]
    for c in combinations(sup, 5):
        bad.add(c)
print('admissible h count', 2349060 - len(bad), '(C(51,5)=2349060)')

# ---------- independent exhaustive D0 extension with the cyclic shift group only
# quotient space: vectors on 51 coords, orthogonal to D0, even on each triple, modulo D0
cons = D0 + masks
# nullspace of cons in F2^51
piv = rref(cons)
for p in sorted(piv):
    for q in list(piv):
        if q != p and piv[q] >> p & 1: piv[q] ^= piv[p]
free = [p for p in range(51) if p not in piv]
null = []
for f in free:
    x = 1 << f
    for p, r in piv.items():
        if r >> f & 1: x |= 1 << p
    null.append(x)
assert all(pc(x & c) % 2 == 0 for x in null for c in cons)
print('dim(E cap D0perp)=', len(null))
# complement of D0 inside: extend D0 echelon
pivD = rref(D0)
comp = []
pv = dict(pivD)
for x in null:
    y = red(x, pv)
    if y:
        pv[y.bit_length() - 1] = y; comp.append(y)
        # re-reduce not needed for rref() semantics since red handles order
print('quotient dim', len(comp))
k = len(comp)
# coordinate map: reduce vector mod D0 + comp echelon, and read labels
lab = {}
for i, c in enumerate(comp):
    x = c; l = 1 << i
    # reduce against D0 and previous labelled
    while x:
        p = x.bit_length() - 1
        if p in pivD: x ^= pivD[p]
        elif p in lab: x ^= lab[p][0]; l ^= lab[p][1]
        else: lab[p] = (x, l); break
def coords(x):
    l = 0
    while x:
        p = x.bit_length() - 1
        if p in pivD: x ^= pivD[p]
        elif p in lab: x ^= lab[p][0]; l ^= lab[p][1]
        else: raise ValueError('not in space')
    return l
gimg = [coords(rot(c)) for c in comp]
act = np.zeros(1 << k, dtype=np.int64)
for x in range(1, 1 << k):
    lb = x & -x
    act[x] = act[x ^ lb] ^ gimg[lb.bit_length() - 1]
assert len(np.unique(act)) == 1 << k
seen = np.zeros(1 << k, dtype=bool); reps = []
for x in range(1 << k):
    if seen[x]: continue
    orb = [x]; seen[x] = True; y = int(act[x])
    while not seen[y]:
        seen[y] = True; orb.append(y); y = int(act[y])
    reps.append((x, len(orb)))
print('orbits under cyclic shift', len(reps))
# masks ^ coordinate 51 table
odd = np.zeros(1 << 17, dtype=np.uint64)
for j, m in enumerate(masks):
    odd[1 << j:1 << (j + 1)] = odd[:1 << j] ^ np.uint64(m | (1 << 51))
Wsorted = sorted(W0, key=lambda w: (pc(w) != 24, w))
Warr = [np.uint64(w) for w in Wsorted]
t0 = time.time(); cov2 = 0; cov18 = 0; found22 = 0
for x, size in reps:
    a = 0
    for i in range(k):
        if x >> i & 1: a ^= comp[i]
    cand = odd ^ np.uint64(a)
    cand = cand[np.bitwise_count(cand) % 4 == 2]
    cov2 += len(cand) * size
    for w in Warr:
        cand = cand[np.bitwise_count(cand ^ w) >= 18]
        if not len(cand): break
    cov18 += len(cand) * size
    c22 = cand
    for w in Warr:
        c22 = c22[np.bitwise_count(c22 ^ w) >= 22]
        if not len(c22): break
    found22 += len(c22)
print('covered 2mod4 cosets', cov2, '== 2^34+2^17?', cov2 == 2**34 + 2**17)
print('cosets with min weight >=18 (all, unreduced count)', cov18)
print('cosets with min weight >=22 found', found22, 'sec', round(time.time() - t0, 1))
