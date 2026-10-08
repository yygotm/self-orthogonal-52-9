"""Agent B (v2 review): small counts quoted in PROOF v2 §5 (A-type, row 7) and §6.
 * 4-variable bent functions: total, how many of weight 6, all of degree <= 2.
 * pure quadratic bent L (no linear/constant terms): 28.
 * for each L: #{B bent, wt(B)=6 : B + 1 + dual(L) bent}  (PROOF: 192 each, 5,376 in total).
 * 3 variables: 7 nonzero pure quadratic parts; functions with Walsh values in {0,+-4} have degree 2 and
   a nonzero quadratic part (semi-bent), affine ones have Walsh +-8.
usage: python bent_counts.py
"""
from itertools import product


def walsh(tt, m):
    return [sum((-1) ** (tt[x] ^ (bin(w & x).count('1') & 1)) for x in range(1 << m)) for w in range(1 << m)]


def anf_degree(tt, m):
    a = list(tt)
    for i in range(m):
        for x in range(1 << m):
            if x >> i & 1:
                a[x] ^= a[x ^ (1 << i)]
    return max((bin(x).count('1') for x in range(1 << m) if a[x]), default=-1)


m = 4
bent = []
for t in range(1 << 16):
    tt = [(t >> x) & 1 for x in range(16)]
    W = walsh(tt, m)
    if all(abs(v) == 4 for v in W):
        bent.append((t, tt, W))
print('4-var bent total', len(bent), ' weight-6:', sum(1 for t, tt, W in bent if sum(tt) == 6),
      ' max degree', max(anf_degree(tt, m) for t, tt, W in bent))
pairs = [(i, j) for i in range(4) for j in range(i + 1, 4)]
bent_set = {t for t, tt, W in bent}
dual = {t: sum(((1 if W[w] < 0 else 0) << w) for w in range(16)) for t, tt, W in bent}
Ls = []
for mask in range(1 << 6):
    tt = [0] * 16
    for x in range(16):
        v = 0
        for k, (i, j) in enumerate(pairs):
            if mask >> k & 1:
                v ^= (x >> i & 1) & (x >> j & 1)
        tt[x] = v
    t = sum(b << x for x, b in enumerate(tt))
    if t in bent_set:
        Ls.append(t)
print('pure quadratic bent L:', len(Ls))
B6 = [t for t, tt, W in bent if sum(tt) == 6]
per = []
for L in Ls:
    h = dual[L] ^ 0xFFFF
    per.append(sum(1 for B in B6 if (B ^ h) in bent_set))
print('per-L counts:', sorted(set(per)), ' total', sum(per))
# 3 variables
m = 3
semi = []
for t in range(1 << 8):
    tt = [(t >> x) & 1 for x in range(8)]
    W = walsh(tt, m)
    if all(v in (0, 4, -4) for v in W):
        semi.append(anf_degree(tt, m))
print('3-var Walsh in {0,+-4}:', len(semi), ' degrees', sorted(set(semi)))
print('3-var functions with |Walsh| = 8 somewhere and degree <= 1:',
      sum(1 for t in range(256) if anf_degree([(t >> x) & 1 for x in range(8)], 3) <= 1))
