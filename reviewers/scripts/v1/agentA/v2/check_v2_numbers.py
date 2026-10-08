"""Agent A (v2 review): recompute the numbers and small lemmas that PROOF.md v2 states.
Usage: python check_v2_numbers.py <so52-v2 folder>
Reads only the data files D-representative-*.txt, residual16-*.txt, LOWER-52-9-20.txt."""
import sys, itertools, random
from fractions import Fraction as Fr
from math import ceil
from collections import Counter

DIR = sys.argv[1]
pc = int.bit_count
ok_all = True
def check(name, cond, extra=''):
    global ok_all
    ok_all &= bool(cond)
    print(('OK   ' if cond else 'FAIL ') + name + (('  ' + str(extra)) if extra != '' else ''))

def load(name, n):
    rows = [int(s.strip()[::-1], 2) for s in open(f'{DIR}/{name}') if s.strip() and not s.startswith('#')]
    return rows
def span(rows):
    a = [0]
    for r in rows: a += [w ^ r for w in a]
    return a
def rank(rows):
    piv = {}
    for x in rows:
        while x:
            p = x.bit_length() - 1
            if p in piv: x ^= piv[p]
            else: piv[p] = x; break
    return len(piv)
def wd(words): return dict(sorted(Counter(pc(w) for w in words).items()))
def columns(rows, n): return [sum((r >> j & 1) << i for i, r in enumerate(rows)) for j in range(n)]
def griesmer(k, d): return sum(ceil(d / 2**i) for i in range(k))

# ---------------- D representatives (§3.1 table)
expect = {0: (1, {0: 1, 24: 204, 32: 51}, 0), 1: (0, {0: 1, 24: 172, 28: 32, 32: 51}, 0),
          2: (0, {0: 1, 24: 174, 28: 30, 32: 49, 36: 2}, 1)}
reps = {}
for i in range(3):
    R = load(f'D-representative-{i}.txt', 52); W = span(R); reps[i] = (R, W)
    cols = columns(R, 52); nz = [c for c in cols if c]
    z = cols.count(0); b = sum(v * (v - 1) // 2 for v in Counter(nz).values())
    so = all(pc(x & y) % 2 == 0 for x in R for y in R)
    check(f'D{i}: rank 8, SO, doubly even, zero cols {z}, b {b}, wd {wd(W)}',
          rank(R) == 8 and so and all(pc(w) % 4 == 0 for w in W) and (z, wd(W), b) == (expect[i][0], expect[i][1], expect[i][2]))
check('D0 on its 51 nonzero coords: projective (b=0) and 8-divisible', all(pc(w) % 8 == 0 for w in reps[0][1]))

# ---------------- §3.1: Griesmer 58, and the q=0 branch by double counting (new, independent of the 2^36 scan)
check('§3.1 Griesmer g(8,28)=58', griesmer(8, 28) == 58)
s = {i: expect[i][1].get(32, 0) + expect[i][1].get(36, 0) for i in range(3)}
check('A32+A36 = 51 for each of D0,D1,D2', set(s.values()) == {51}, s)
check('q=0 branch: 255*(A32+A36)(C) = 511*51 has no integer solution', (511 * 51) % 255 != 0, f'511*51/255 = {Fr(511*51,255)}')
# sanity of the double-counting identity on a real 9-dim doubly-even code (lower bound code)
L = load('LOWER-52-9-20.txt', 52); WL = span(L)
check('lower-bound code: rank 9, SO, wd', rank(L) == 9 and all(pc(x & y) % 2 == 0 for x in L for y in L), wd(WL))
check('lower-bound weight enumerator 1+51z20+204z24+204z28+51z32+z52', wd(WL) == {0: 1, 20: 51, 24: 204, 28: 204, 32: 51, 52: 1})
# hyperplanes of the 9-dim message space = kernels of nonzero functionals u
tot = Counter()
for u in range(1, 512):
    for m in range(1, 512):
        if pc(m & u) % 2 == 0:
            w = 0
            for i in range(9):
                if m >> i & 1: w ^= L[i]
            tot[pc(w)] += 1
check('double counting identity sum_H A_w(H) = 255 A_w(C) (checked on lower-bound code)',
      all(tot[w] == 255 * c for w, c in wd(WL).items() if w))

# ---------------- §3.2
check('§3.2 Griesmer g(8,24)=50, g(7,8)=18', griesmer(8, 24) == 50 and griesmer(7, 8) == 18)
for z in (1, 2):
    h40 = 2**7 * (1 + (11 - z)); h36 = 2**6 * (1 + (10 - z))
    check(f'§3.2 z={z}: Hamming [{11-z},7,3]: {h40} > 2^{11-z}={2**(11-z)};  [{10-z},6,3]: {h36} > 2^{10-z}={2**(10-z)}',
          h40 > 2**(11 - z) and h36 > 2**(10 - z))
    check(f'§3.2 z={z}: weight 44 even-image dim 7-z <= 6; weight 48 kernel dim >= 5+z, 48/2^(r-1) non-integer',
          7 - z <= 6 and all(48 % 2**(r - 1) for r in range(5 + z, 9)))
def solve_moments(n, b, A36=0):
    # unknowns A24, A28, A32 (weights 24..32 plus A36)
    import numpy as np
    M = [[1, 1, 1], [24, 28, 32], [576, 784, 1024]]
    rhs = [255 - A36, 128 * n - 36 * A36, 64 * (n * n + n + 2 * b) - 1296 * A36]
    # exact solve by Cramer
    def det(m): return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
    D = det(M); out = []
    for c in range(3):
        Mc = [row[:] for row in M]
        for r in range(3): Mc[r][c] = rhs[r]
        out.append(Fr(det(Mc), D))
    return out
for b in range(0, 4):
    a = solve_moments(51, b); c = solve_moments(50, b)
    check(f'§3.2 moments b={b}: n=51 A28={a[1]} (=-8b), n=50 A28={c[1]} (=-40-8b)', a[1] == -8 * b and c[1] == -40 - 8 * b)
a = solve_moments(51, 0); check('§3.2 n=51,b=0: (A24,A28,A32)=(204,0,51)', a == [204, 0, 51])
# §6 / §5 general moment formula with no zero column, n=52
for b in range(3):
    for A36 in range(0, 12):
        a = solve_moments(52, b, A36)
        assert a == [172 + 4*b - A36, 32 - 8*b + 3*A36, 51 + 4*b - 3*A36]
check('§5 moment formulas A24=172+4b-A36, A28=32-8b+3A36, A32=51+4b-3A36 (n=52)', True)
check('§6 f=0 would force A28=0 i.e. b=4 (8-divisible, non-projective): Kurz Table 1 must count non-projective codes',
      solve_moments(52, 4)[1] == 0)

# ---------------- §4
check('§4 weight 52: (52^2+127*16)/128 = 37 < 52', Fr(52**2 + 127 * 16, 128) == 37)
ev8 = Counter(pc(x) for x in range(1, 256) if pc(x) % 2 == 0)
check('§4 weight 44: even [8,7,2] counts j=2,4,6,8 = 28,70,28,1 and sum = 128*39',
      [ev8[j] for j in (2, 4, 6, 8)] == [28, 70, 28, 1] and 44**2 + sum(ev8[j] * (2*j - 4)**2 for j in ev8) == 128 * 39)
# weight 40: build both even [12,7,4] outer codes from AG(4,2) minus 4 points
pts = list(range(16))
def outer(deleted):
    P = [p for p in pts if p not in deleted]
    H = [sum(1 << j for j in range(12))] + [sum(((P[j] >> i) & 1) << j for j in range(12)) for i in range(4)]
    code = [x for x in range(1 << 12) if all(pc(x & h) % 2 == 0 for h in H)]
    dual = span(H)
    return code, dual
for name, dele in [('plane', [0, 1, 2, 3]), ('independent', [0, 1, 2, 4 | 8 ^ 0])]:
    # independent: 0,1,2,12 -> 1,2,12 linearly independent; check sum != 0 (not a plane)
    if name == 'independent':
        dele = [0, 1, 2, 12]
        assert 0 ^ 1 ^ 2 ^ 12 != 0
    code, dual = outer(dele)
    js = [pc(x) for x in code if x]
    check(f'§4 weight 40 outer ({name}): dim 7, d=4, even, dual min wt >= 4, sum j = 768, sum j^2 = 4992',
          len(code) == 128 and min(js) == 4 and all(j % 2 == 0 for j in js) and min(pc(x) for x in dual if x) >= 4
          and sum(js) == 768 and sum(j * j for j in js) == 4992)
    check(f'§4 weight 40 ({name}): 1600 + sum (2j-8)^2 = 5120 = 128*40', 1600 + sum((2*j - 8)**2 for j in js) == 5120)
check('§4 weight 40: Griesmer g(7,6)=15 > 12', griesmer(7, 6) == 15)
# 4 points of AG(4,2): exactly two affine types
def aff_type(S):
    a = S[0]; vs = [s ^ a for s in S[1:]]
    return rank(vs)
types = Counter(aff_type(list(S)) for S in itertools.combinations(range(16), 4))
check('§4: 4-subsets of AG(4,2) = 140 planes (rank 2) + 1680 independent (rank 3)', types == Counter({2: 140, 3: 1680}), dict(types))

# ---------------- §5
res = {}
for i in range(3):
    R = load(f'residual16-{i}.txt', 16); res[i] = wd(span(R))
check('§5 residual16 weight distributions (B=0, A=1, C=2)',
      res[0] == {0: 1, 6: 45, 8: 41, 10: 34, 12: 6, 14: 1} and res[1] == {0: 1, 6: 48, 8: 30, 10: 48, 16: 1}
      and res[2] == {0: 1, 6: 44, 8: 45, 10: 28, 12: 10}, res)
for i, tag, a36, nlow, nup in [(0, 'B', 8, 48, 64), (2, 'C', 11, 56, 76)]:
    A36max = 1 + sum(c for j, c in res[i].items() if j >= 12)
    Nlow = sum(c for j, c in res[i].items() if j % 4 == 0)          # derivative 1 iff j = 0 mod 4 (incl. the pair {0,c})
    check(f'§5 {tag}: A36 <= {A36max}, N >= {Nlow}, N <= 32+4*A36max = {32 + 4*A36max}', (A36max, Nlow, 32 + 4 * A36max) == (a36, nlow, nup))
check('§5 pair with both weight 36 needs j=18>16', (72 - 36) // 2 == 18)
check('§5 A: only outer word with j>=12 is all-ones (j=16)', [j for j in res[1] if j >= 12] == [16])
check('§5 A: N = 40-8b >= 32 -> b <= 1; A28 = 32-8+6 = 30 for b=1, A36=2', solve_moments(52, 1, 2)[1] == 30 and all(40 - 8 * b < 32 for b in (2, 3)))
# sigma_p values from coset weights 28 (x30) and 36 (x2)
def inv5(F):
    return [Fr(sum(F[u] * (-1) ** pc(u & p) for u in range(32)), 32) for p in range(32)]
u0 = 0b10000
F = [-20 if u in (0, u0) else -4 for u in range(32)]
sig = inv5(F)
check('§5 A: signed counts p=0:-5, p!=0 & u0.p=0: -1, u0.p=1: 0',
      sig[0] == -5 and all(sig[p] == (-1 if pc(p & u0) % 2 == 0 else 0) for p in range(1, 32)))
check('§5 A: Griesmer g(5,24)=47', griesmer(5, 24) == 47)
# K [47,5,24], weights 24 x30, 32 x1 -> multiplicities
F = [47] + [47 - 2 * (32 if u == u0 else 24) for u in range(1, 32)]
m = inv5(F)
check('§5 A: K column types: 15 singles on w1-hyperplane, 16 doubles off it, 0 zero (effective)',
      m[0] == 0 and all(m[p] == (1 if pc(p & u0) % 2 == 0 else 2) for p in range(1, 32)))
# Parseval 96 => t = +-1 (§5) and t = 0 (§6)
def parseval_sum(t):
    nT = 8 - 2 * t; nR = 8 + 2 * t
    if not (0 <= nT <= 32 and 0 <= nR <= 32): return None
    return Fr((32 - nT) * 16 + nT * 144 + (32 - nR) * 16 + nR * 144, 32)
check('§5/§6 Parseval sum = 96 independent of t', all(parseval_sum(t) == 96 for t in range(-4, 5)))
check('§5 A: 30 + 64 + 2t^2 = 96 -> t = +-1;  §6: 96 + 2t^2 = 96 -> t = 0',
      [t for t in range(-5, 6) if 94 + 2 * t * t == 96] == [-1, 1] and [t for t in range(-4, 5) if 96 + 2 * t * t == 96] == [0])
sols = set()
for S in range(-16, 17, 2):
    for Wa in range(-16, 17, 2):
        for Wb in range(-16, 17, 2):
            if all(v in (4, -12) for e in (1, -1) for v in (S + e * (Wa + Wb), -S + e * (Wa - Wb))):
                sols.add((S, Wa, Wb))
check('§5 A: (S,Wa,Wb) in {(4,4,-4),(4,-4,4),(-4,4,4),(-4,-4,-4)}', sols == {(4, 4, -4), (4, -4, 4), (-4, 4, 4), (-4, -4, -4)}, sorted(sols))
# 4-variable bent functions, duals, counts
def walsh(f, nv):
    return [sum((-1) ** ((f >> x & 1) ^ (pc(x & w) & 1)) for x in range(1 << nv)) for w in range(1 << nv)]
bent = {}
for f in range(1 << 16):
    W = walsh(f, 4)
    if all(abs(v) == 4 for v in W):
        bent[f] = sum((1 if v < 0 else 0) << w for w, v in enumerate(W))
check('§5 A: 896 bent functions', len(bent) == 896)
check('§5 A: for bent s, s(0)=0 <=> wt(dual)=6', all(((f & 1) == 0) == (pc(d) == 6) for f, d in bent.items()))
check('§5 A: 448 bent functions of weight 6', sum(1 for f in bent if pc(f) == 6) == 448)
def anf(f, nv):
    a = [f >> x & 1 for x in range(1 << nv)]
    for i in range(nv):
        for x in range(1 << nv):
            if x >> i & 1: a[x] ^= a[x ^ (1 << i)]
    return a
pureq = [f for f in bent if all((not c) or pc(x) == 2 for x, c in enumerate(anf(f, 4)))]
check('§5 A: 28 pure-quadratic bent L', len(pureq) == 28)
ALL1 = (1 << 16) - 1
per_L = []
for Lf in pureq:
    h = ALL1 ^ bent[Lf]
    per_L.append(sum(1 for B in bent if pc(B) == 6 and (B ^ h) in bent))
check('§5 A: 192 per L, total 5376', set(per_L) == {192} and sum(per_L) == 5376, sum(per_L))
# duality-sum condition equivalent to the sign pattern
good = True
for _ in range(2000):
    s, a, b = random.choice(list(bent)), random.choice(list(bent)), random.choice(list(bent))
    Ws, Wa, Wb = walsh(s, 4), walsh(a, 4), walsh(b, 4)
    lhs = all((Ws[w], Wa[w], Wb[w]) in sols for w in range(16))
    rhs = all(((bent[a] >> w) ^ (bent[b] >> w) ^ (bent[s] >> w)) & 1 for w in range(16))
    good &= (lhs == rhs)
check('§5 A: sign condition <=> dual(a)+dual(b)+dual(s)=1 (2000 random bent triples)', good)

# ---------------- §6
check('§6: Griesmer g(5,12)=24', griesmer(5, 12) == 24)
A16 = Fr(16 * 24 - 12 * 31, 4)
check('§6: halved [24,5,12] has A12=28, A16=3', A16 == 3)
def mult_halved(W16):
    F = [24] + [24 - 2 * (16 if u in W16 else 12) for u in range(1, 32)]
    return inv5(F)
mm = mult_halved({1, 2, 3})
check('§6: 3 weight-16 messages summing to 0 -> m in {0,1}, 24 points outside a 3-dim U',
      all(x in (0, 1) for x in mm) and sum(mm) == 24 and all(mm[p] == 0 for p in range(32) if pc(p & 1) % 2 == 0 and pc(p & 2) % 2 == 0))
bad = all(any(x.denominator != 1 for x in mult_halved({a, b, c})) for a, b, c in itertools.combinations(range(1, 32), 3) if a ^ b ^ c != 0)
check('§6: 3 independent weight-16 messages -> some non-integer multiplicity', bad)
# 3-variable: semi-bent <=> non-affine quadratic; cubic fails
semi = [f for f in range(256) if all(v in (0, 4, -4) for v in walsh(f, 3))]
deg = lambda f: max([pc(x) for x, c in enumerate(anf(f, 3)) if c] or [-1])
check('§6: 3-var functions with Walsh in {0,+-4} = 112 non-affine quadratics',
      len(semi) == 112 and all(deg(f) == 2 for f in semi) and sum(1 for f in range(256) if deg(f) == 2) == 112)
check('§6: every cubic 3-var function has odd weight', all(pc(f) % 2 == 1 for f in range(256) if deg(f) == 3))
pq = lambda f: sum(c << x for x, c in enumerate(anf(f, 3)) if pc(x) == 2)
supp = {f: frozenset(w for w, v in enumerate(walsh(f, 3)) if v) for f in semi}
check('§6: Walsh support of each non-affine quadratic is a 4-point affine plane',
      all(len(S) == 4 and (lambda L: L[0] ^ L[1] ^ L[2] ^ L[3])(sorted(S)) == 0 for S in supp.values()))
comp_ok = all((supp[f] | supp[g] == frozenset(range(8)) and not (supp[f] & supp[g])) <= (pq(f) == pq(g)) for f in semi for g in semi)
check('§6: complementary Walsh supports => same pure quadratic part (all 112x112 pairs)', comp_ok)
check('§6: 7*6*16^2 = 10752; 344064 = 10752*32', 7 * 6 * 16**2 == 10752 and 10752 * 32 == 344064)
check('§6: 8th-row zero-col patterns meeting a fixed 2-set in exactly 1 point: 4 (of 4 zeros), 6 (of 5 zeros, §5)',
      sum(1 for S in itertools.combinations(range(4), 2) if len(set(S) & {0, 1}) == 1) == 4 and
      sum(1 for S in itertools.combinations(range(5), 2) if len(set(S) & {0, 1}) == 1) == 6)

# ---------------- §7
check('§7.2: order of 2 mod 51 is 8', min(e for e in range(1, 60) if pow(2, e, 51) == 1) == 8)
gens = [tuple((j + 1) % 51 for j in range(51)), tuple((2 * j) % 51 for j in range(51))]
grp = {tuple(range(51))}; frontier = list(grp)
while frontier:
    nxt = []
    for g in frontier:
        for s in gens:
            h = tuple(s[g[j]] for j in range(51))
            if h not in grp: grp.add(h); nxt.append(h)
    frontier = nxt
def order(g):
    e, x = 1, g
    while x != tuple(range(51)): x = tuple(g[x[j]] for j in range(51)); e += 1
    return e
check('§7.2: <j->j+1, j->2j> has order 408 and is not cyclic (max element order < 408)',
      len(grp) == 408 and max(order(g) for g in grp) < 408, max(order(g) for g in grp))
h1, h2 = 2251816993685511, 2251834173685767
supp_of = lambda h: [j for j in range(52) if h >> j & 1]
check('§7.2: supports h1={0,1,2,17,34,51}, h2={0,1,2,18,35,51}', supp_of(h1) == [0, 1, 2, 17, 34, 51] and supp_of(h2) == [0, 1, 2, 18, 35, 51])
T = lambda x, h: x ^ h if pc(x & h) % 2 else x
for i, h in ((1, h1), (2, h2)):
    img = sorted(span([T(r, h) for r in reps[0][0]]))
    check(f'§7.2: T_h{i}(D0) equals D-representative-{i} as a code', img == sorted(reps[i][1]))
rng = random.Random(7)
good = True
for _ in range(3000):
    perm = list(range(52)); rng.shuffle(perm)
    g = lambda x: sum(1 << perm[j] for j in range(52) if x >> j & 1)
    h = sum(1 << j for j in rng.sample(range(52), 6)); x = rng.getrandbits(52)
    if pc(x) % 2: x ^= 1
    good &= g(T(x, h)) == T(g(x), g(h))
    d = pc(T(x, h)) - pc(x); good &= d in (-4, 0, 4)
check('§7.2: g T_h g^-1 = T_gh and weight change in {-4,0,4} for even x, wt(h)=6 (3000 random)', good)
# §7.1 complement / information-set representative arguments (dimension facts)
check('§7.1: dim D^perp = 44, dim D^perp/D = 36', 52 - 8 == 44 and 44 - 8 == 36)
print('ALL OK' if ok_all else 'SOME CHECK FAILED')
