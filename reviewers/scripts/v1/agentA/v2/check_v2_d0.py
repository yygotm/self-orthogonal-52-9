"""Agent A (v2 review): own exhaustive D0 coset scan, both residues mod 4, under <shift, x->2x>."""
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
mul2 = lambda x: sum(1 << (2 * j % 51) for j in range(51) if x >> j & 1)
assert all(red(mul2(r), piv0) == 0 for r in D0) and sorted(mul2(m) for m in masks) == sorted(masks)
acts = []
for g in (rot, mul2):
    gimg = [coords(g(c)) for c in comp]
    act = np.zeros(1 << k, dtype=np.int64)
    for x in range(1, 1 << k):
        lb = x & -x
        act[x] = act[x ^ lb] ^ gimg[lb.bit_length() - 1]
    assert len(np.unique(act)) == 1 << k
    acts.append(act)
seen = np.zeros(1 << k, dtype=bool); reps = []
for x in range(1 << k):
    if seen[x]: continue
    q = [x]; seen[x] = True
    for y in q:
        for act in acts:
            z = int(act[y])
            if not seen[z]: seen[z] = True; q.append(z)
    reps.append((x, len(q)))
print('orbits under <shift, x->2x>', len(reps))
# masks ^ coordinate 51 table
odd = np.zeros(1 << 17, dtype=np.uint64)
for j, m in enumerate(masks):
    odd[1 << j:1 << (j + 1)] = odd[:1 << j] ^ np.uint64(m | (1 << 51))
# D-representative-0.txt must span the same code as this D0
rep0 = [int(s.strip()[::-1], 2) for s in open(sys.argv[1]) if s.strip()]
assert len(rep0) == 8 and sorted(span(rep0)) == sorted(W0), 'D-representative-0 differs from cyclic D0'
print('D-representative-0.txt spans the same code as cyclic D0: True')
Wsorted = sorted(W0, key=lambda w: (pc(w) != 24, w))
Warr = [np.uint64(w) for w in Wsorted]
def survive(cand, T):
    for w in Warr:
        cand = cand[np.bitwise_count(cand ^ w) >= T]
        if not len(cand): break
    return cand
t0 = time.time(); cnt = {}
for x, size in reps:
    a = 0
    for i in range(k):
        if x >> i & 1: a ^= comp[i]
    allc = odd ^ np.uint64(a)
    r4 = np.bitwise_count(allc) % 4
    c0 = allc[r4 == 0]; c2 = allc[r4 == 2]
    assert len(c0) + len(c2) == len(allc)
    cnt['cover0'] = cnt.get('cover0', 0) + len(c0) * size
    cnt['cover2'] = cnt.get('cover2', 0) + len(c2) * size
    s = survive(c0, 20); cnt['0mod4_ge20'] = cnt.get('0mod4_ge20', 0) + len(s) * size
    s = survive(s, 24); cnt['0mod4_ge24'] = cnt.get('0mod4_ge24', 0) + len(s) * size
    s = survive(c2, 18); cnt['2mod4_ge18'] = cnt.get('2mod4_ge18', 0) + len(s) * size
    s = survive(s, 22); cnt['2mod4_ge22'] = cnt.get('2mod4_ge22', 0) + len(s) * size
print('even cosets covered: 0 mod 4', cnt['cover0'], '== 2^34-2^17 ?', cnt['cover0'] == 2**34 - 2**17,
      '; 2 mod 4', cnt['cover2'], '== 2^34+2^17 ?', cnt['cover2'] == 2**34 + 2**17)
for key in ['0mod4_ge20', '0mod4_ge24', '2mod4_ge18', '2mod4_ge22']:
    print(key, cnt[key])
print('match C/ext52x control 1138092541:', cnt['0mod4_ge20'] == 1138092541)
print('match step-1 / author 10997819424:', cnt['2mod4_ge18'] == 10997819424)
print('sec', round(time.time() - t0, 1))
