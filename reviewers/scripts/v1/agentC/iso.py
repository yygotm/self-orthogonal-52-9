"""Agent C: equivalence test for binary linear [52,8] codes.
X ~ Y (permutation equivalent) iff there is a linear bijection X -> Y preserving every weight
(MacWilliams: a weight-preserving linear map between binary codes is induced by a monomial = permutation
map; concretely the column multisets are determined by all 255 subset-sum weights via Fourier inversion).
We search a basis image y_0..y_7 of X's generator g_0..g_7 with wt(sum_S y) = wt(sum_S g) for all S.
Also used as a library: iso(rowsX, rowsY) -> list of images or None.
"""
import numpy as np, json, sys

def words(rs):
    w = [0]
    for r in rs: w += [x ^ r for x in w]
    return w

def iso(gx, ry):
    Y = np.array(words(ry)[1:], dtype=np.uint64)
    wy = np.bitwise_count(Y)
    def rec(k, xs, ys, img):
        if k == len(gx): return img
        g = gx[k]
        xs_new = [x ^ g for x in xs]
        wt_new = np.array([x.bit_count() for x in xs_new])
        cand = Y[wy == g.bit_count()]
        ysa = np.array(ys, dtype=np.uint64)
        M = np.bitwise_count(ysa[:, None] ^ cand[None, :])  # (2^k, ncand)
        ok = np.all(M == wt_new[:, None], axis=0)
        for y in cand[ok]:
            y = int(y)
            r = rec(k + 1, xs + xs_new, ys + [y ^ z for z in ys], img + [y])
            if r is not None: return r
        return None
    return rec(0, [0], [0], [])

def read(fn):
    return [sum(1 << j for j, ch in enumerate(l.strip()) if ch == '1') for l in open(fn) if l.strip() and l.strip()[0] in '01']

def parse(gen):
    return [sum(1 << j for j, ch in enumerate(s) if ch == '1') for s in gen]

if __name__ == '__main__':
    base = sys.argv[1]
    reps = [read(base + '/D-representative-%d.txt' % t) for t in range(3)]
    # self tests
    assert iso(reps[1], reps[1]) is not None
    from collections import Counter as C_
    wdist = lambda rs: tuple(sorted(C_(x.bit_count() for x in words(rs)).items()))
    rwd = [wdist(r) for r in reps]
    assert len(set(rwd)) == 3   # the three reps are pairwise inequivalent (different weight distributions)
    from collections import Counter
    tally = Counter()
    for fn in sys.argv[2:]:
        d = json.load(open(fn))
        gens = [c['gen'] for c in d['classes']] + d.get('samples', [])[:int(__import__('os').environ.get('CAP','400'))]
        for g in gens:
            rows = parse(g)
            hit = [t for t in range(3) if wdist(rows) == rwd[t] and iso(rows, reps[t]) is not None]
            tally[tuple(hit)] += 1
            if not hit:
                print('NOT EQUIVALENT to D0/D1/D2:', fn, g)
    print('equivalence tally (which reps matched -> count):', dict(tally))
