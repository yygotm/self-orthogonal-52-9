"""Write a header for extS.c from a doubly-even [N,K,>=24] code S (Claude, 2026/10/8).
Every doubly-even [N+1,K+1,>=24] code T whose last coordinate is nonzero, shortened at that coordinate, is a
doubly-even [N,K,>=24] code S (zero columns allowed), and T = <(S|0), (v|1)> with v in S^perp, wt(v) = 3 mod 4,
wt(v+s) >= 23 for all s in S (then T is doubly-even: wt(v+s)+1 = wt(v)+1 + wt(s) - 2|v cap s| = 0 mod 4).
v runs over coset representatives of S in S^perp: vectors vanishing on an information set P of S (dim N-2K).
usage: python gen_s.py N K S.json index out.h    (S.json: list of codes as rows (ints), length <= N, zero-padded)
   or  python gen_s.py N K S.txt out.h          (K lines of 0/1, character j = coordinate j)
"""
import sys, json
from functools import reduce
N, K = int(sys.argv[1]), int(sys.argv[2])
if sys.argv[3].endswith('.json'):
    rows = json.load(open(sys.argv[3]))[int(sys.argv[4])]; out_h = sys.argv[5]
else:
    rows = [int(l.strip()[::-1], 2) for l in open(sys.argv[3]) if l.strip() and not l.startswith('#')]; out_h = sys.argv[4]
assert len(rows) == K and all(0 <= r < 1 << N for r in rows)
pc = lambda x: bin(x).count('1')


def rref(vs):
    piv, out = [], []
    for v in vs:
        for p, b in zip(piv, out):
            if v >> p & 1: v ^= b
        if v:
            p = v.bit_length() - 1
            out = [b ^ v if b >> p & 1 else b for b in out]
            piv.append(p); out.append(v)
    return piv, out


P, _ = rref(rows)
assert len(P) == K
cons = rows + [1 << p for p in P]
piv, R = rref(cons)
assert len(R) == 2 * K
free = [j for j in range(N) if j not in piv]
basis = []
for f in free:
    x = 1 << f
    for p, r in zip(piv, R):
        if r >> f & 1: x |= 1 << p
    basis.append(x)
assert len(basis) == N - 2 * K
for x in basis:
    assert all(pc(x & r) % 2 == 0 for r in rows) and all(not x >> p & 1 for p in P)
S = [0]
for r in rows: S += [w ^ r for w in S]
assert all(pc(w) % 4 == 0 for w in S) and len(set(S)) == 1 << K and min(pc(w) for w in S[1:]) >= 24
Snz = sorted(S[1:], key=pc)
with open(out_h, 'w') as f:
    f.write('#define NB %d\n#define NS %d\n' % (len(basis), len(Snz)))
    f.write('static const unsigned long long B[NB] = {%s};\n' % ','.join('0x%xULL' % x for x in basis))
    f.write('static const unsigned long long S[NS] = {%s};\n' % ','.join('0x%xULL' % x for x in Snz))
    f.write('static const unsigned long long G[%d] = {%s};\n' % (K, ','.join('0x%xULL' % x for x in rows)))
print('basis', len(basis), 'P', sorted(P), 'zero columns', N - pc(reduce(lambda a, b: a | b, rows)))
