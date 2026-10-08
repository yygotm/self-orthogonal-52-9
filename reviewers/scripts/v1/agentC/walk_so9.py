"""Agent C, (b): annealed random walk over self-orthogonal [52,9] codes looking for d >= 22.
Moves: T_h(x) = x + (x.h)h with h of even weight 4..10 (inner-product preserving, so SO is preserved;
these transvections generate the isometry group of the even-weight space, so the walk is not confined to
a small family).  Cost = sum over nonzero words of max(0, 22 - wt).  Cost 0 would be an SO [52,9,22].
usage: python walk_so9.py start.txt seed steps temp
"""
import sys, random, time
from collections import Counter
fn, seed, STEPS, TEMP = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
random.seed(seed)
N = 52
rows = [sum(1 << j for j, ch in enumerate(l.strip()) if ch == '1') for l in open(fn) if l.strip() and l.strip()[0] in '01']
assert len(rows) == 9

def words(rs):
    w = [0]
    for r in rs: w += [x ^ r for x in w]
    return w

def cost(rs):
    c = 0
    for x in words(rs)[1:]:
        k = x.bit_count()
        if k < 22: c += 22 - k
    return c

ws = words(rows)
assert len(set(ws)) == 512 and all((a & b).bit_count() % 2 == 0 for a in rows for b in rows)
c = cost(rows); best = c; hist = Counter()
t0 = time.time()
for step in range(STEPS):
    k = random.choice((4, 6, 6, 8, 10))
    h = sum(1 << j for j in random.sample(range(N), k))
    r2 = [r ^ h if (r & h).bit_count() & 1 else r for r in rows]
    c2 = cost(r2)
    if c2 <= c or random.random() < pow(2.718281828, -(c2 - c) / TEMP):
        rows, c = r2, c2
        hist[min(x.bit_count() for x in words(rows)[1:])] += 1 if step % 50 == 0 else 0
        if c < best: best = c
        if c == 0:
            print('FOUND SO [52,9,>=22]:', [format(r, '052b')[::-1] for r in rows]); break
assert all((a & b).bit_count() % 2 == 0 for a in rows for b in rows)
print(fn.split('/')[-1], 'seed', seed, 'T', TEMP, 'best cost', best, 'final cost', c,
      'min-distance histogram (sampled)', dict(sorted(hist.items())), 'time %.0fs' % (time.time() - t0))
