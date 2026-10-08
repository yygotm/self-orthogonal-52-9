"""Agent C, (a): simulated annealing for doubly-even [52,8,>=24] codes from scratch, many chains in parallel.
State: 52 columns p_i in F_2^8 (zero allowed). Word u has weight W[u] = #{i : u.p_i = 1}.
Target: for all u != 0, W[u] = 0 mod 4 and W[u] >= 24. Found codes are written as column lists to sa_found.txt.
usage: python sa_de.py seed chains steps
"""
import sys, numpy as np, time
seed, CH, STEPS = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = np.random.default_rng(seed)
n = 52
u = np.arange(256)
T = np.array([[bin(a & b).count('1') & 1 for b in range(256)] for a in range(256)], dtype=np.int16)  # T[p][u]

def pen(W):
    r = W & 3
    p = np.minimum(r, 4 - r) + np.maximum(0, 24 - W)
    p[..., 0] = 0
    return p.sum(axis=-1)

cols = rng.integers(1, 256, size=(CH, n))
W = T[cols].sum(axis=1)                      # (CH,256)
cost = pen(W)
found = []
t0 = time.time()
ar = np.arange(CH)
for step in range(STEPS):
    temp = max(0.05, 2.0 * (1 - step / STEPS))
    i = rng.integers(0, n, size=CH)
    old = cols[ar, i]
    new = np.where(rng.random(CH) < 0.5, old ^ (1 << rng.integers(0, 8, size=CH)), rng.integers(0, 256, size=CH))
    W2 = W - T[old] + T[new]
    c2 = pen(W2)
    d = c2 - cost
    acc = (d <= 0) | (rng.random(CH) < np.exp(-np.maximum(d, 0) / temp))
    cols[ar[acc], i[acc]] = new[acc]
    W[acc] = W2[acc]; cost[acc] = c2[acc]
    hit = np.nonzero(cost == 0)[0]
    for h in hit:
        found.append(sorted(int(x) for x in cols[h]))
        cols[h] = rng.integers(1, 256, size=n); W[h] = T[cols[h]].sum(axis=0); cost[h] = pen(W[h])
with open('sa_found_%d.txt' % seed, 'w') as f:
    for c in found: f.write(' '.join(map(str, c)) + '\n')
print('seed', seed, 'found', len(found), 'min cost now', int(cost.min()), 'time %.0fs' % (time.time() - t0))
