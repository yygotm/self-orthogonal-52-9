"""Agent B (v2 review): recompute the k=1,2,3 rows of Kurz, Table 1 (number of 8-divisible [n,k]_2 codes,
effective length n, 'minimum distance 24'), to settle two reading questions:
  (a) does the table count NON-projective codes (repeated columns)?
  (b) does 'minimum distance 24' mean d = 24 exactly or d >= 24?
A code of dimension k with effective length n is a multiset of nonzero points of F_2^k (column multiplicities
m(p) >= 0, sum n, spanning). Weight of message u: w(u) = sum_{p: u.p=1} m(p). Fourier: F(u) = n - 2 w(u) =
sum_p m(p) (-1)^{u.p} (m(0) = 0), so m(p) = 2^-k sum_u F(u) (-1)^{u.p}. We enumerate weight vectors
w(u) in {24,32,40,48,...} (8-divisible), invert, keep integral nonnegative m with m(0) = 0, and count orbits
under GL(k,2) (equivalence of binary codes = permutation equivalence = GL-equivalence of point multisets).
usage: python kurz_small_rows.py
"""
import itertools

NS = [24, 32, 36, 40, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]
# Table 1 as read from the PDF (pdftotext -table, page 4); None = blank on the right (not computed)
TABLE = {
    1: [1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    2: [0, 0, 1, 1, 0, 2, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0],
}


def dot(u, p):
    return bin(u & p).count('1') & 1


def gl(k):
    vecs = range(1, 1 << k)
    mats = []
    for cols in itertools.product(vecs, repeat=k):
        # columns images of unit vectors; invertible iff span has size 2^k
        span = {0}
        for c in cols:
            span |= {s ^ c for s in span}
        if len(span) == 1 << k:
            mats.append(cols)
    return mats


def apply(cols, p):
    r = 0
    for i, c in enumerate(cols):
        if p >> i & 1:
            r ^= c
    return r


def count(k, n, mode):
    """mode: 'ge24' (d>=24), 'eq24' (d==24), 'ge24proj' (d>=24 and projective)."""
    pts = list(range(1, 1 << k))
    ws = [w for w in range(24, n + 1, 8)]
    G = gl(k)
    seen = set()
    for wv in itertools.product(ws, repeat=len(pts)):
        if mode == 'eq24' and 24 not in wv:
            continue
        F = {0: n}
        for u, w in zip(pts, wv):
            F[u] = n - 2 * w
        m = {}
        okk = True
        for p in range(1 << k):
            s = sum(F[u] * (-1) ** dot(u, p) for u in range(1 << k))
            if s % (1 << k) or s < 0:
                okk = False
                break
            m[p] = s >> k
        if not okk or m[0] != 0:
            continue
        if mode == 'ge24proj' and max(m.values()) > 1:
            continue
        # canonical form of multiset under GL(k,2)
        key = min(tuple(m[apply(g, p)] for p in pts) for g in G)
        seen.add(key)
    return len(seen)


for k in (1, 2, 3):
    for mode in ('ge24', 'eq24', 'ge24proj'):
        row = [count(k, n, mode) for n in NS]
        print('k', k, mode.ljust(9), ' '.join(f'{n}:{c}' for n, c in zip(NS, row)))
    if k in TABLE:
        print('k', k, 'Table1   ', ' '.join(f'{n}:{c}' for n, c in zip(NS, TABLE[k])))
