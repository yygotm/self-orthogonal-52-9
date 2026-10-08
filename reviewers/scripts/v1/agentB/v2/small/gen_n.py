"""Write basis.h (or argv[2], for the D in file argv[1]) for ext52x.c (Claude, 2026/10/8).
D = cyclic [51,8,24] (codetables generator polynomial, as in ../ext52.py) + one zero column, doubly-even.
Coset representatives of D in D^perp: vectors of D^perp that vanish on an information set P of D (dim 52-8-8 = 36).
Every coset v+D (v in D^perp) contains exactly one such vector, so these 2^36 vectors cover all extensions <D,v>.
"""
N, K = 51, 8
EXP = [43, 42, 41, 37, 36, 33, 30, 29, 27, 26, 25, 22, 21, 20, 19, 17, 16, 13, 12, 10, 7, 5, 4, 0]
import sys
n = int(sys.argv[3])
g = sum(1 << e for e in EXP)
rows = [sum(((g >> ((j - s) % N)) & 1) << j for j in range(N)) for s in range(K)]
import sys
out_h = 'basis.h'
if len(sys.argv) > 1:  # D from a file: K lines of 0/1 strings of length 52 (character j = coordinate j)
    rows = [int(l.strip()[::-1], 2) for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
    out_h = sys.argv[2]
    assert len(rows) == K

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
# solve linear system: x in F_2^52 with x.r = 0 for r in rows and x_p = 0 for p in P
cons = rows + [1 << p for p in P]
# nullspace of cons (as rows of a 16 x 52 matrix)
piv, R = rref(cons)
assert len(R) == 16
free = [j for j in range(n) if j not in piv]
basis = []
for f in free:
    x = 1 << f
    for p, r in zip(piv, R):
        if r >> f & 1: x |= 1 << p
    basis.append(x)
for x in basis:
    assert all(bin(x & r).count('1') % 2 == 0 for r in rows) and all(not x >> p & 1 for p in P)
D = [0]
for r in rows: D += [w ^ r for w in D]
assert all(bin(w).count('1') % 4 == 0 for w in D) and len(set(D)) == 256
Dnz = sorted(D[1:], key=lambda w: bin(w).count('1'))
with open(out_h, 'w') as f:
    f.write('#define NB %d\n' % len(basis))
    f.write('static const unsigned long long B[NB] = {%s};\n' % ','.join('0x%xULL' % x for x in basis))
    f.write('static const unsigned long long D[255] = {%s};\n' % ','.join('0x%xULL' % x for x in Dnz))
    f.write('static const unsigned long long G[8] = {%s};\n' % ','.join('0x%xULL' % x for x in rows))
print('basis', len(basis), 'P', sorted(P))
