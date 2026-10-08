# Agent A2 independent generator: N = {x in D^perp : x_p = 0 for p in P}, P = pivot set of RREF(D).
# Each coset of D in D^perp meets N exactly once. Writes rows of D and 36 basis vectors of N.
import sys
rows = [l.strip() for l in open(sys.argv[1]) if l.strip()]
n = 52
D = [int(r[::-1], 2) for r in rows]          # bit j = char j
# RREF of D over low-bit pivots
R = list(D); piv = []
for r_i in range(len(R)):
    # choose pivot = lowest set bit not already used
    pass
M = list(D); pivots = []
row = 0
for col in range(n):
    sel = next((i for i in range(row, len(M)) if M[i] >> col & 1), None)
    if sel is None: continue
    M[row], M[sel] = M[sel], M[row]
    for i in range(len(M)):
        if i != row and M[i] >> col & 1: M[i] ^= M[row]
    pivots.append(col); row += 1
assert row == 8
# constraints: x.d = 0 for D rows, x_p = 0 for p in P  -> nullspace
cons = D + [1 << p for p in pivots]
# nullspace via RREF of constraint matrix
C = list(cons); cp = []; r = 0
for col in range(n):
    sel = next((i for i in range(r, len(C)) if C[i] >> col & 1), None)
    if sel is None: continue
    C[r], C[sel] = C[sel], C[r]
    for i in range(len(C)):
        if i != r and C[i] >> col & 1: C[i] ^= C[r]
    cp.append(col); r += 1
assert r == 16, r
free = [c for c in range(n) if c not in cp]
basis = []
for f in free:
    x = 1 << f
    for i, pc in enumerate(cp):
        if C[i] >> f & 1: x |= 1 << pc
    basis.append(x)
assert len(basis) == 36
pc_ = lambda x: bin(x).count('1')
assert all(pc_(x & d) % 2 == 0 for x in basis for d in D)
assert all((x >> p & 1) == 0 for x in basis for p in pivots)
with open(sys.argv[2], 'w') as fo:
    fo.write('static const unsigned long long DR[8]={%s};\n' % ','.join('0x%xULL' % d for d in D))
    fo.write('static const unsigned long long NB_[36]={%s};\n' % ','.join('0x%xULL' % x for x in basis))
print('pivots', pivots)
