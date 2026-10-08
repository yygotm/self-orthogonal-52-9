"""Agent B v2: small analogue for the coset scans cosets.c (Agent C) and ext52x.c.

1. Make a random doubly-even [n,8] code D (optionally with the last coordinate a zero column),
   keeping the best minimum distance among several random tries. Write it as 8 lines of 0/1
   (character j = coordinate j), the format both header generators read.
2. Brute force, independent of any basis of D^perp: run over ALL x in F_2^n, keep x with x.r = 0 for
   every row r (that is D^perp itself), and for each such x compute the coset minimum
   m(x) = min_{d in D} wt(x+d) over all 256 words. Every coset has 256 elements with the same m and
   the same wt mod 4, so (#x with a property)/256 = #cosets with that property.
3. Print, for each threshold T, the six numbers cosets.c prints
   (wt = 0 / 2 mod 4, m >= T, T+2, T+4; even weight only) and the number ext52x.c prints
   (even weight, m >= T, both classes).

usage: python small_test.py n seed zerocol(0/1) out_prefix T1 T2 ...
"""
import sys, json, random
import numpy as np

n, seed, zc, pre = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
Ts = [int(a) for a in sys.argv[5:]]
rng = random.Random(seed)
m_eff = n - zc
pc = lambda x: bin(x).count('1')


def span(rows):
    w = [0]
    for r in rows:
        w += [x ^ r for x in w]
    return w


def rand_de():
    rows = []
    while len(rows) < 8:
        x = rng.getrandbits(m_eff)
        if x == 0 or pc(x) % 4:
            continue
        if any(pc(x & r) % 2 for r in rows):
            continue
        if x in set(span(rows)):
            continue
        rows.append(x)
    return rows


best = None
for _ in range(3000):
    rows = rand_de()
    d = min(pc(w) for w in span(rows)[1:])
    if best is None or d > best[0]:
        best = (d, rows)
d, rows = best
W = span(rows)
assert len(set(W)) == 256 and all(pc(w) % 4 == 0 for w in W)
with open(pre + '.txt', 'w') as f:
    for r in rows:
        f.write(''.join('1' if r >> j & 1 else '0' for j in range(n)) + '\n')

# D^perp by brute force over F_2^n
R = np.array(rows, dtype=np.uint64)
dual = []
CH = 1 << 24
for base in range(0, 1 << n, CH):
    x = np.arange(base, min(base + CH, 1 << n), dtype=np.uint64)
    ok = np.ones(len(x), dtype=bool)
    for r in R:
        ok &= (np.bitwise_count(x & r) & 1) == 0
    dual.append(x[ok])
dual = np.concatenate(dual)
assert len(dual) == 1 << (n - 8)
Wn = np.array(W, dtype=np.uint64)
m = np.full(len(dual), 99, dtype=np.int64)
for w in Wn:
    m = np.minimum(m, np.bitwise_count(dual ^ w).astype(np.int64))
wt = np.bitwise_count(dual).astype(np.int64)
ev = (wt % 2) == 0
out = {'n': n, 'seed': seed, 'zero_col': zc, 'd(D)': d, 'wd': {}, 'T': {}}
for w in W:
    out['wd'][pc(w)] = out['wd'].get(pc(w), 0) + 1
for T in Ts:
    res = []
    for cls in (0, 2):
        sel = ev & ((wt % 4) == cls)
        res.append([int(np.count_nonzero(sel & (m >= T + k))) // 256 for k in (0, 2, 4)])
    acc = int(np.count_nonzero(ev & (m >= T))) // 256
    out['T'][T] = {'cosets_c_0mod4': res[0], 'cosets_c_2mod4': res[1], 'ext52x_accepted': acc}
    # sanity: counts divisible by 256
    assert int(np.count_nonzero(ev & (m >= T))) % 256 == 0
print(json.dumps(out))
json.dump(out, open(pre + '.json', 'w'))
