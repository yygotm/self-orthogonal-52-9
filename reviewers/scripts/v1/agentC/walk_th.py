"""Agent C, (a): annealed random walk over doubly-even [52,8] codes using orthogonal reflections
T_h(x) = x + (x.h)h with wt(h) = 2 mod 4 (6 or 10).  These preserve inner products and wt mod 4 of
even words, so doubly-evenness is preserved; reflections in nonsingular vectors generate the orthogonal
group of (even vectors / <1>, wt/2 mod 2), so the walk can in principle reach every doubly-even [52,8] code
not containing the all-ones word (up to the start's Witt class).
Cost = sum over nonzero words of max(0, 24 - wt).  Every visited state with cost 0 is a doubly-even
[52,8,>=24] code; we record its invariants (zero columns, equal-column pairs b, weight distribution) and
keep one generator per new invariant.
usage: python walk_th.py start.txt seed steps temp
"""
import sys, random, time, json
from collections import Counter
fn, seed, STEPS, TEMP = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
random.seed(seed)
N = 52
rows = []
for l in open(fn):
    l = l.strip()
    if l and l[0] in '01': rows.append(sum(1 << j for j, ch in enumerate(l) if ch == '1'))
assert len(rows) == 8

def words(rs):
    w = [0]
    for r in rs: w += [x ^ r for x in w]
    return w

def cost(rs):
    c = 0
    for x in words(rs)[1:]:
        k = x.bit_count()
        if k < 24: c += 24 - k
    return c

def inv(rs):
    ws = words(rs)
    wd = tuple(sorted(Counter(x.bit_count() for x in ws).items()))
    cols = [sum(((r >> j) & 1) << i for i, r in enumerate(rs)) for j in range(N)]
    cc = Counter(cols)
    z = cc.get(0, 0)
    b = sum(m * (m - 1) // 2 for c, m in cc.items() if c)
    mult = tuple(sorted(m for c, m in cc.items() if c))
    return (z, b, wd, mult)

def refl(rs, h):
    return [r ^ h if (r & h).bit_count() & 1 else r for r in rs]

c = cost(rows)
seen = {}
nzero = 0
allg = []
t0 = time.time()
for step in range(STEPS):
    k = 6 if random.random() < 0.7 else 10
    h = sum(1 << j for j in random.sample(range(N), k))
    r2 = refl(rows, h)
    c2 = cost(r2)
    if c2 <= c or random.random() < pow(2.718281828, -(c2 - c) / TEMP):
        rows, c = r2, c2
        if c == 0:
            nzero += 1
            key = inv(rows)
            if key not in seen:
                seen[key] = [format(r, '052b')[::-1] for r in rows]
            if len(allg) < 400 and nzero % 5 == 1:
                allg.append([format(r, '052b')[::-1] for r in rows])
out = {'start': fn, 'seed': seed, 'steps': STEPS, 'temp': TEMP, 'cost0_states': nzero,
       'classes': [{'zero': k[0], 'b': k[1], 'wd': k[2], 'mult': k[3], 'gen': g} for k, g in seen.items()], 'samples': allg}
json.dump(out, open('walk_%s_%d.json' % (fn.split('/')[-1].split('.')[0], seed), 'w'))
print(fn, 'seed', seed, 'cost0 states', nzero, 'distinct invariants', len(seen), 'time %.0fs' % (time.time() - t0))
for k in seen: print('  zero', k[0], 'b', k[1], 'wd', k[2], 'mult', Counter(k[3]))
