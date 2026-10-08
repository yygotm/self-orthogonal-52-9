"""Agent A: independent arithmetic checks for PROOF.md sections 3-6."""
from fractions import Fraction as Fr
from itertools import combinations
import math

# ---- moments (section 5): D doubly even [52,8], no zero column, b equal-column pairs,
# weights in {24,28,32,36}.  Solve 3 linear equations with A36 and b as parameters.
def solve_moments(A36, b):
    # unknowns A24,A28,A32
    n = 52
    S0 = 255 - A36
    S1 = 128 * n - 36 * A36
    S2 = 128 * n + 64 * (n * (n - 1) - 2 * b) + 128 * 2 * b - 1296 * A36
    # solve [1 1 1; 24 28 32; 576 784 1024] x = [S0,S1,S2]

    M = [[1, 1, 1], [24, 28, 32], [576, 784, 1024]]
    rhs = [S0, S1, S2]
    # Cramer with fractions
    def det(m):
        return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
                + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
    D = det(M)
    out = []
    for c in range(3):
        mm = [row[:] for row in M]
        for r in range(3):
            mm[r][c] = rhs[r]
        out.append(Fr(det(mm), D))
    return out

for A36 in range(0, 4):
    for b in range(0, 3):
        A24, A28, A32 = solve_moments(A36, b)
        assert A24 == 172 + 4*b - A36 and A28 == 32 - 8*b + 3*A36 and A32 == 51 + 4*b - 3*A36, (A36, b)
print('moments: A24=172+4b-A36, A28=32-8b+3A36, A32=51+4b-3A36 confirmed; N=A28+A36=32-8b+4A36')

# ---- weight 52
print('w52 sum m^2 =', Fr(52**2 + 127*16, 128))
# ---- weight 44: even [8,7] distribution
cnt = {j: math.comb(8, j) for j in (2, 4, 6, 8)}
s = 44**2 + sum(cnt[j] * (2*j - 4)**2 for j in cnt)
print('w44 bound sum =', s, '=128*', Fr(s, 128), ' need >=', 128*44)
# check bound |F|<=2j-4 from 24<=i+j, 24<=44-i+j, i+j=0 mod 4
for j in (2, 4, 6, 8):
    Fs = [44-2*i for i in range(45) if i+j >= 24 and 44-i+j >= 24 and (i+j) % 4 == 0]
    assert max(abs(f) for f in Fs) <= 2*j-4

# ---- weight 48 Walsh/Parseval on 16 triples
# f(t) odd in {-3..3}, |W(a)|=4 for all a -> sum f^2 = 16 -> all |f|=1
print('w48: sum f^2 = 16*16/16 =', 16*16//16)
# inner weight of coset with outer 1111: multiple of 3 and 4, in [20,28]
print('w48 1111 coset inner options:', [i for i in range(20, 29) if i % 12 == 0])

# ---- weight 40: both outer types
def span(rows):
    a = [0]
    for r in rows:
        a += [w ^ r for w in a]
    return a

def nullspace(rows, n):
    # basis of {x in F2^n : r.x=0 for all r}
    piv = {}
    for x in rows:
        while x:
            p = x.bit_length()-1
            if p in piv: x ^= piv[p]
            else: piv[p] = x; break
    # full reduce
    for p in sorted(piv):
        for q in sorted(piv):
            if q != p and piv[q] >> p & 1:
                piv[q] ^= piv[p]
    free = [p for p in range(n) if p not in piv]
    out = []
    for f in free:
        x = 1 << f
        for p, r in piv.items():
            if r >> f & 1:
                x |= 1 << p
        assert all(bin(r & x).count('1') % 2 == 0 for r in rows)
        out.append(x)
    return out

for deleted in ([0, 1, 2, 3], [0, 1, 2, 4]):
    pts = [p for p in range(16) if p not in deleted]
    H = [4095] + [sum((p >> j & 1) << i for i, p in enumerate(pts)) for j in range(4)]
    G = nullspace(H, 12)
    W = span(G)
    wd = {}
    for w in W:
        wd[bin(w).count('1')] = wd.get(bin(w).count('1'), 0) + 1
    tot = 40**2 + sum(c * (2*j - 8)**2 for j, c in wd.items() if j)
    # j-range check
    for j in wd:
        if j == 0: continue
        Fs = [40-2*i for i in range(41) if i+j >= 24 and 40-i+j >= 24]
        assert max(abs(f) for f in Fs) == 2*j - 8
    print('w40 type', deleted, 'dim', len(G), 'wd', dict(sorted(wd.items())), 'Parseval sum', tot, '=128*', Fr(tot, 128))

# a(u) forced 0 at j=4,8,12 and the two-choice structure for j=8,12
for j in (4, 6, 8, 10, 12):
    opts = [(i, (i+j)//4 % 2) for i in (24-j, 16+j) if (i+j) % 4 == 0]
    print('w40 j=%d inner options (i, f):' % j, sorted(set(opts)))

# ---- weight 36: residual codes
import pathlib
base = pathlib.Path(__file__).resolve().parent.parent / 'so52'
for name, idx in (('B', 0), ('A', 1), ('C', 2)):
    rows = [int(s[::-1], 2) for s in (base / f'residual16-{idx}.txt').read_text().splitlines()]
    W = span(rows)
    assert len(set(W)) == 128
    wd = {}
    for w in W:
        wd[bin(w).count('1')] = wd.get(bin(w).count('1'), 0) + 1
    cols = [sum((r >> j & 1) << i for i, r in enumerate(rows)) for j in range(16)]
    rep = len(cols) - len(set(cols))
    nbig = sum(c for j, c in wd.items() if j >= 12)
    nder = sum(c for j, c in wd.items() if j % 4 == 0)  # pairs with derivative 1 (incl u=0)
    # Parseval bound with full constraints 24<=i+j<=36, 24<=36-i+j<=36, i+j=0 mod 4
    tot = 36**2
    for j, c in wd.items():
        if j == 0: continue
        Fs = [36-2*i for i in range(37) if 24 <= i+j <= 36 and 24 <= 36-i+j <= 36 and (i+j) % 4 == 0]
        tot += c * max(f*f for f in Fs)
    # choices per (j, a): number of i with i+j = 4a mod 8
    ch = {}
    for j in wd:
        if j == 0: continue
        for a in (0, 1):
            L = [i for i in range(37) if 24 <= i+j <= 36 and 24 <= 36-i+j <= 36 and (i+j) % 8 == 4*a]
            ch[(j, a)] = L
    print(name, 'wd', dict(sorted(wd.items())), 'repeated cols', rep, 'A36<=', 1+nbig,
          'N>=', nder, 'Parseval sum/128', Fr(tot, 128), 'choices', ch)
