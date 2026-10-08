"""Agent B (v2 review): spot checks on the n=52 coset scans of PROOF v2 §7.1, with own linear algebra.
 (1) The vectors v printed by ext52x for D0 at d=20 (trials/28-so-codes/ext52x/d20*.out and the re-run):
     v in D0^perp, wt(v) even, min weight of v+D0 >= 20, so <D0,v> is SO [52,9,>=20]; report the exact min.
 (2) For D0, D1, D2: 200,000 uniformly random even-weight v in D^perp (D^perp from my own null space,
     not from the scan headers): distribution of the coset minimum by wt(v) mod 4. Sampling cannot prove
     absence; it only checks that nothing contradicts the exhaustive counts (0 cosets with min >= 22, and for
     D0, 1,138,092,541 / 2^35 ~ 3.3% of even cosets with min >= 20, all in the 0 mod 4 class).
usage: python spot_cosets.py SO52_V2_DIR V_HEX...
"""
import sys, random
from collections import Counter

d = sys.argv[1]
vs = [int(x, 16) for x in sys.argv[2:]]
pc = lambda x: x.bit_count()


def read_D(fn):
    return [sum(1 << j for j, ch in enumerate(l.strip()) if ch == '1')
            for l in open(fn) if l.strip() and l.strip()[0] in '01']


def span(rows):
    w = [0]
    for r in rows:
        w += [x ^ r for x in w]
    return w


def nullspace(rows, n=52):
    # Gaussian elimination on the 8 x 52 matrix, pivots chosen from the highest bit
    piv = []
    for r in rows:
        for p, b in piv:
            if r >> p & 1:
                r ^= b
        if r:
            p = r.bit_length() - 1
            piv = [(q, b ^ r if b >> p & 1 else b) for q, b in piv]
            piv.append((p, r))
    pset = {p for p, _ in piv}
    out = []
    for f in range(n):
        if f in pset:
            continue
        x = 1 << f
        for p, b in piv:
            if b >> f & 1:
                x |= 1 << p
        out.append(x)
    return out


rng = random.Random(52)
for i in range(3):
    D = read_D(f'{d}/D-representative-{i}.txt')
    W = span(D)[1:]
    dual = nullspace(D)
    assert len(dual) == 44 and all(pc(x & r) % 2 == 0 for x in dual for r in D)
    if i == 0:
        for v in vs:
            m = min([pc(v)] + [pc(v ^ w) for w in W])
            print('D0 printed v %x: in D0^perp %s, wt %d, coset min %d' %
                  (v, all(pc(v & r) % 2 == 0 for r in D), pc(v), m))
    hist = {0: Counter(), 2: Counter()}
    n = 0
    while n < 200000:
        v = 0
        for x in dual:
            if rng.getrandbits(1):
                v ^= x
        w = pc(v)
        if w % 2:
            continue
        n += 1
        m = min([w] + [pc(v ^ x) for x in W])
        hist[w % 4][m] += 1
    print(f'D{i} random even cosets: 0 mod 4 ->', dict(sorted(hist[0].items())),
          ' 2 mod 4 ->', dict(sorted(hist[2].items())))
