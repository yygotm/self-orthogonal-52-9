"""Agent A: consistency of the 23-orbit reduction and an own-code spot check of the joint T_h filter.
Imports the author's setup() (copied here) only to obtain the 23 orbit representatives and sizes.
"""
import sys, json, time
from itertools import combinations
import numpy as np
from triple_search import setup, span

pc = lambda x: bin(x).count('1')
rows, basis, masks, orbits = setup(full=True)
print('orbits', len(orbits), 'sum sizes', sum(s for _, s in orbits))
log = [json.loads(s) for s in open('joint-switch-full-0.jsonl')]
weighted = sum(size * r['surviving_d18'] for (x, size), r in zip(orbits, log))
print('weighted count of (2 mod 4, min>=18) cosets from author log x orbit sizes:', weighted)
print('orbit sizes', [s for _, s in orbits])

if len(sys.argv) > 1:
    W = span(rows)
    low = [w for w in W if pc(w) == 24]
    # own construction of admissible h
    hs = []
    lowsets = [w for w in low]
    for c in combinations(range(51), 5):
        m = sum(1 << j for j in c)
        if not any((w & m) == m for w in lowsets): hs.append(m | (1 << 51))
    hs = np.array(hs, dtype=np.uint64); print('h count', len(hs), flush=True)
    odd = np.zeros(1 << 17, dtype=np.uint64)
    for j, msk in enumerate(masks): odd[1 << j:1 << (j + 1)] = odd[:1 << j] ^ np.uint64(msk | (1 << 51))
    wa = np.array(W, dtype=np.uint64)
    for idx in map(int, sys.argv[1:]):
        t0 = time.time(); x, size = orbits[idx]
        a = 0
        for j, v in enumerate(basis):
            if x >> j & 1: a ^= v
        cand = odd ^ np.uint64(a); cand = cand[np.bitwise_count(cand) % 4 == 2]
        # min weight over coset >= 18 : compute all 256 distances in blocks
        keep = np.ones(len(cand), dtype=bool)
        for w in W:
            keep &= np.bitwise_count(cand ^ np.uint64(w)) >= 18
        cand = cand[keep]
        sols = 0
        for vn in cand:
            coset = wa ^ vn; wt = np.bitwise_count(coset)
            opt = hs
            for w in coset[wt == 18]:
                opt = opt[np.bitwise_count(opt & w) == 1]
                if not len(opt): break
            if len(opt):
                for w in coset[wt == 22]:
                    opt = opt[np.bitwise_count(opt & w) != 5]
                    if not len(opt): break
            ok = opt
            sols += int(len(ok))
        print(json.dumps({'orbit': idx, 'surviving_d18_mine': len(cand), 'author': log[idx]['surviving_d18'], 'h_solutions': sols, 'sec': round(time.time() - t0, 1)}), flush=True)
