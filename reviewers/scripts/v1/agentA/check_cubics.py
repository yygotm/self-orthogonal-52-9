"""Agent A: independent re-check of the cubic-function steps (sections 4 w40, 5 B/C/A).
No automorphism reduction; only the lift gauge a -> a + l(u)*deriv(u).
Integrality of inverse Walsh is tested by meet-in-the-middle over Z/8 (no F2 elimination).
"""
import sys, time, json, pathlib
import numpy as np

BASE = pathlib.Path(__file__).resolve().parent.parent / 'so52'
pc = lambda x: bin(x).count('1')

def span(rows):
    a = [0]
    for r in rows:
        a += [w ^ r for w in a]
    return a

def rref_basis(vecs):
    piv = {}
    for x in vecs:
        while x:
            p = x.bit_length() - 1
            if p in piv: x ^= piv[p]
            else: piv[p] = x; break
    return piv

def reduce(x, piv):
    for p in sorted(piv, reverse=True):
        if x >> p & 1: x ^= piv[p]
    return x

def cubic_space(zero_set):
    """truth tables (bit u) of all f on F2^7 with deg<=3, f(0)=0, f(u)=0 for u in zero_set."""
    monos = [m for m in range(1, 128) if pc(m) <= 3]
    tts = [sum(1 << u for u in range(128) if (u & m) == m) for m in monos]
    # linear map coefficient-vector -> truth table restricted to zero_set; find kernel
    # do Gaussian elimination on augmented [restricted tt | coefficient id]
    mask = sum(1 << u for u in zero_set)
    rows = [((tt & mask), tt) for tt in tts]
    piv = {}
    kernel = []
    for r, tt in rows:
        while r:
            p = r.bit_length() - 1
            if p in piv:
                r ^= piv[p][0]; tt ^= piv[p][1]
            else:
                piv[p] = (r, tt); break
        if not r:
            kernel.append(tt)
    kb = rref_basis(kernel)
    return list(kb.values())

def enum_span(basis):
    a = 0
    yield 0
    for z in range(1, 1 << len(basis)):
        a ^= basis[(z & -z).bit_length() - 1]
        yield a

CH = np.array([[(-1) ** pc(u & v) for u in range(128)] for v in range(128)], dtype=np.int64)  # CH[v,u]

def mitm(F0, free, delta, binary01):
    """count z in {0,1}^free with m = (F0 - sum z_u delta_u e_u) inverse-Walsh nonneg integer (and <=1 if binary01)."""
    num = CH @ np.array(F0, dtype=np.int64)  # 128*m when z=0
    if np.any(num % 16):
        return 0, 'mod16'
    t = (num // 16) % 8
    k = len(free)
    cols = [((delta[i] // 16) * CH[:, free[i]]) % 8 for i in range(k)]
    h1 = k // 2
    def table(idx):
        T = np.zeros((1, 128), dtype=np.uint8)
        for i in idx:
            T = np.concatenate([T, (T + cols[i].astype(np.uint8)) % 8])
        return T
    T1 = table(range(h1)); T2 = table(range(h1, k))
    rng = np.random.default_rng(1)
    R = rng.integers(0, 2**63, size=128, dtype=np.uint64)
    def keys(X):
        out = np.zeros(len(X), dtype=np.uint64)
        for s in range(0, len(X), 1 << 16):
            out[s:s+(1<<16)] = (X[s:s+(1<<16)].astype(np.uint64) * R).sum(axis=1)
        return out
    tt = t.astype(np.uint8)
    K1 = keys(((tt + np.uint8(8) - T1) % 8).astype(np.uint8))
    K2 = keys(T2)
    common = np.intersect1d(K1, K2)
    sols = 0
    if len(common):
        idx1 = np.nonzero(np.isin(K1, common))[0]; idx2 = np.nonzero(np.isin(K2, common))[0]
        d1 = {}
        for i in idx1.tolist():
            d1.setdefault(int(K1[i]), []).append(i)
        for j in idx2.tolist():
            for i in d1.get(int(K2[j]), []):
                z = [(i >> b) & 1 for b in range(h1)] + [(j >> b) & 1 for b in range(k - h1)]
                Fz = np.array(F0, dtype=np.int64)
                for b, u in enumerate(free):
                    if z[b]: Fz[u] -= delta[b]
                m = CH @ Fz
                if np.any(m % 128): continue
                m //= 128
                if np.any(m < 0): continue
                if binary01 and np.any(m > 1): continue
                sols += 1
    return sols, 'enumerated %d+%d bits, key matches %d' % (h1, k - h1, len(common))

def residual(idx):
    rows = [int(s[::-1], 2) for s in (BASE / f'residual16-{idx}.txt').read_text().splitlines()]
    return span(rows)

def w36(idx, lo, hi, label):
    ew = residual(idx); J = [pc(w) for w in ew]
    basis = cubic_space([u for u in range(128) if J[u] == 6])
    deriv = sum(((1 + J[u] // 2) % 2) << u for u in range(128))
    gauge = [sum((u >> i & 1) * (deriv >> u & 1) << u for u in range(128)) for i in range(7)]
    spaceb = rref_basis(basis)
    assert all(reduce(g, spaceb) == 0 for g in gauge)
    gb = rref_basis(gauge)
    hist = {}; reps = set()
    for a in enum_span(basis):
        N = pc(a) + pc(a ^ deriv)
        hist[N] = hist.get(N, 0) + 1
        if lo <= N <= hi:
            reps.add(reduce(a, gb))
    print(label, 'cubic dim', len(basis), 'gauge rank', len(gb), 'reps in [%d,%d]' % (lo, hi), len(reps), flush=True)
    if label == 'A':
        print('A weight histogram', dict(sorted(hist.items())), flush=True)
        return
    tot = 0; maxk = 0; t0 = time.time()
    SH = int(sys.argv[2]) if len(sys.argv) > 2 else 0; NS = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    for ai, a in enumerate(sorted(reps)):
        if ai % NS != SH: continue
        F0 = [36]; free = []; delta = []
        for u in range(1, 128):
            j = J[u]; au = a >> u & 1
            L = [i for i in range(37) if 24 <= i + j <= 36 and 24 <= 36 - i + j <= 36 and (i + j) % 8 == 4 * au]
            assert 1 <= len(L) <= 2 and (len(L) == 1 or L[1] - L[0] == 8), (u, j, au, L)
            F0.append(36 - 2 * L[0])
            if len(L) == 2:
                free.append(u); delta.append(16)
        maxk = max(maxk, len(free))
        s, info = mitm(F0, free, delta, False)
        assert s == 0, (label, a, s)
        tot += 1
    print(label, 'all', tot, 'gauge reps exhausted, 0 solutions; max free', maxk, 'sec', round(time.time() - t0, 1), flush=True)

def w40():
    for deleted in ([0, 1, 2, 3], [0, 1, 2, 4]):
        pts = [p for p in range(16) if p not in deleted]
        # independent construction of outer code: all x in F2^12 orthogonal to H
        H = [4095] + [sum((p >> j & 1) << i for i, p in enumerate(pts)) for j in range(4)]
        code = [x for x in range(1 << 12) if all(pc(x & h) % 2 == 0 for h in H)]
        assert len(code) == 128
        # choose a basis and message indexing
        piv = rref_basis(code); G = list(piv.values()); ew = span(G); J = [pc(w) for w in ew]
        basis = cubic_space([u for u in range(128) if J[u] in (4, 8, 12)])
        deriv = sum(((J[u] // 2) % 2) << u for u in range(128))
        gauge = [sum((u >> i & 1) * (deriv >> u & 1) << u for u in range(128)) for i in range(7)]
        spaceb = rref_basis(basis); assert all(reduce(g, spaceb) == 0 for g in gauge)
        gb = rref_basis(gauge)
        reps = sorted({reduce(a, gb) for a in enum_span(basis)})
        print('w40', deleted, 'cubic dim', len(basis), 'gauge rank', len(gb), 'reps', len(reps), flush=True)
        for a in reps:
            F0 = [40]; free = []; delta = []
            for u in range(1, 128):
                j = J[u]; au = a >> u & 1
                L = sorted({i for i in (24 - j, 16 + j) if (i + j) % 8 == 4 * au})
                assert L
                F0.append(40 - 2 * L[0])
                if len(L) == 2:
                    free.append(u); delta.append(2 * (L[1] - L[0]))
            s, info = mitm(F0, free, delta, True)
            print('   rep free', len(free), 'solutions', s, info, flush=True)
            assert s == 0

def selftest():
    rng = np.random.default_rng(7)
    for trial in range(3):
        m = np.zeros(128, dtype=np.int64)
        for v in rng.integers(0, 128, size=36): m[v] += 1
        F = CH.T @ m  # F(u)=sum_v m(v)(-1)^{uv}
        free = sorted(rng.choice(np.arange(1, 128), size=30, replace=False).tolist())
        zs = rng.integers(0, 2, size=30)
        F0 = F.copy()
        for b, u in enumerate(free): F0[u] += 16 * zs[b]
        s, info = mitm(F0.tolist(), free, [16] * 30, False)
        print('selftest solutions found', s, info)
        assert s >= 1


if __name__ == '__main__':
    t = time.time()
    selftest()
    if 'C' in sys.argv:
        w36(2, 56, 76, 'C'); print('total sec', round(time.time() - t, 1)); sys.exit()
    w40()
    w36(1, 0, 10**9, 'A')
    w36(0, 48, 64, 'B')
    print('total sec', round(time.time() - t, 1))
