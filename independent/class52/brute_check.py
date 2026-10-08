"""Cross-check classify.py on small parameters by brute force (Claude, 2026/10/8):
all full-support [n,k,>=d] codes = all multisets of n nonzero columns in F_2^k spanning F_2^k with all
nonzero messages of weight >= d, reduced by the same canonical form."""
import sys, itertools
from classify import classify, canon, pc
def brute(n, k, d):
    pts = range(1, 1 << k); seen = set()
    for cols in itertools.combinations_with_replacement(pts, n):
        if any(sum(pc(u & p) & 1 for p in cols) < d for u in range(1, 1 << k)): continue
        rows = [sum(1 << j for j, p in enumerate(cols) if p >> i & 1) for i in range(k)]
        seen.add(canon(rows, n))
    return seen
for n, k, d in [(7, 4, 2), (8, 4, 3), (9, 4, 4), (10, 4, 4), (11, 4, 5)]:
    a = {canon(r, n) for r in classify(n, k, d, 'any')}; b = brute(n, k, d)
    print((n, k, d), len(a), len(b), 'OK' if a == b else 'MISMATCH', flush=True)
