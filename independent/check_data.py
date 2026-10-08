"""Check the bundled classification data (Claude, 2026/10/8).

For every list of codes in data/: dimension, doubly-even, minimum weight >= 24, pairwise inequivalence (nauty
canonical form from class52/classify.py). Then the counts and weight distributions stated in the README.
usage: python check_data.py            (from independent/)
"""
import json, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'class52'))
from classify import canon, span, pc

D = os.path.join(HERE, 'data')


def wd(rows):
    return dict(sorted(Counter(pc(w) for w in span(rows)).items()))


def check(name, n, k, d, expected):
    codes = json.load(open(os.path.join(D, name)))
    assert len(codes) == expected, (name, len(codes), expected)
    seen = set()
    for rows in codes:
        assert len(rows) == k and all(r < 1 << n for r in rows), name
        ws = [pc(w) for w in span(rows)]
        assert len(ws) == 1 << k and ws.count(0) == 1, (name, 'not of full rank')
        assert all(w % 4 == 0 and (w == 0 or w >= d) for w in ws), (name, 'not doubly-even with d >= %d' % d)
        c = canon(rows, n)
        assert c not in seen, (name, 'two equivalent codes')
        seen.add(c)
    print(f'{name}: {len(codes)} pairwise inequivalent doubly-even [{n},{k},>={d}] codes')
    return codes


def support(rows):
    s = 0
    for r in rows: s |= r
    return pc(s)


S48 = check('class-48-6-24-de.json', 48, 6, 24, 1)
S49 = check('class-49-6-24-de.json', 49, 6, 24, 4)
S50 = check('class-50-6-24-de.json', 50, 6, 24, 117)
for n, cs in ((48, S48), (49, S49), (50, S50)):
    assert all(support(r) == n for r in cs), 'class-%d is not full support' % n
T = check('T51.json', 51, 7, 24, 59)
Dc = check('D52.json', 52, 8, 24, 3)
got = sorted(tuple(sorted(wd(r).items())) for r in Dc)
want = sorted(tuple(sorted(w.items())) for w in [
    {0: 1, 24: 204, 32: 51}, {0: 1, 24: 172, 28: 32, 32: 51}, {0: 1, 24: 174, 28: 30, 32: 49, 36: 2}])
assert got == want, got
print('D52.json weight distributions: D0, D1, D2 as stated')

# the author's representatives are equivalent to the three classes
mine = {canon(r, 52) for r in Dc}
for t in range(3):
    rows = [int(l.strip()[::-1], 2) for l in open(os.path.join(HERE, 'ext52x', f'D-gpt{t}.txt')) if l.strip()]
    assert canon(rows, 52) in mine, t
print('author representatives D-gpt0..2: each equivalent to one class of D52.json')
print('check_data: OK')
