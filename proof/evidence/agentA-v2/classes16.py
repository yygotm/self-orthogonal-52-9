"""Agent A2: upper bound on the number of equivalence classes of [16,7,>=6] codes.
Enumeration of the 28,718 reduced systematic forms reuses the logic of Agent B's count_all16.py
(copied, row/column-sorted [I_7|A]); the equivalence part is my own: for each code, VF2 on the
(coordinates x weight-6 words) incidence graph against the first code of its weight distribution,
then the coordinate permutation found is applied to ALL 128 codewords and checked to give the rep code.
usage: python classes16.py START END"""
import sys, time
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
R, K, D = 9, 7, 6
cands = sorted(r for r in range(1 << R) if r.bit_count() >= D - 1)
sols = []
def rec(rows, sums, colpref):
    if len(rows) == K:
        sols.append(tuple(rows)); return
    start = rows[-1] + 1 if rows else 0
    for r in cands:
        if r < start: continue
        newpref = [(colpref[j] << 1) | ((r >> (R - 1 - j)) & 1) for j in range(R)]
        if any(newpref[j] > newpref[j + 1] for j in range(R - 1)): continue
        newsums = []
        for s, c in sums:
            v = s ^ r
            if v.bit_count() + c + 1 < D: break
            newsums.append((v, c + 1))
        else:
            rec(rows + [r], sums + newsums, newpref)
rec([], [(0, 0)], [0] * R)
print('solutions', len(sols)); sys.stdout.flush()
def code(rows):
    g = [(1 << (R + i)) | a for i, a in enumerate(rows)]   # 16-bit words
    W = [0]
    for x in g: W += [w ^ x for w in W]
    return frozenset(W)
def graph(Wset):
    G = nx.Graph()
    for c in range(16): G.add_node(('c', c), t=0)
    for w in Wset:
        if w.bit_count() == 6:
            G.add_node(('w', w), t=1)
            for c in range(16):
                if w >> c & 1: G.add_edge(('w', w), ('c', c))
    return G
def rank(ws):
    piv = {}; r = 0
    for v in ws:
        while v:
            h = v.bit_length() - 1
            if h in piv: v ^= piv[h]
            else: piv[h] = v; r += 1; break
    return r
reps = {}
def wkey(W):
    return tuple(sorted((k, sum(1 for w in W if w.bit_count() == k)) for k in set(w.bit_count() for w in W)))
for rows in sols:                      # global group representatives = first code of each weight distribution
    W = code(rows); k_ = wkey(W)
    if k_ not in reps: reps[k_] = (W, graph(W))
print('global groups', len(reps)); sys.stdout.flush()
a, b = int(sys.argv[1]), int(sys.argv[2])
lim = b - a
t0 = time.time(); bad = 0; nodd = 0
for idx, rows in enumerate(sols[a:b], start=a):
    W = code(rows)
    wd = tuple(sorted({w.bit_count() for w in W}))
    key = tuple(sorted((k, sum(1 for w in W if w.bit_count() == k)) for k in set(w.bit_count() for w in W)))
    if any(w.bit_count() % 2 for w in W): nodd += 1
    w6 = [w for w in W if w.bit_count() == 6]
    assert rank(w6) == 7          # weight-6 words span the code
    RW, RG = reps[key]
    GM = GraphMatcher(graph(W), RG, node_match=lambda a, b: a['t'] == b['t'])
    m = next(GM.isomorphisms_iter(), None)
    ok = False
    if m is not None:
        perm = {c: m[('c', c)][1] for c in range(16)}
        img = frozenset(sum(1 << perm[c] for c in range(16) if w >> c & 1) for w in W)
        ok = (img == RW)
    if not ok: bad += 1
    if idx % 2000 == 0: print(idx, 'classes so far', len(reps), 'bad', bad, '%.0fs' % (time.time() - t0)); sys.stdout.flush()
print('checked', lim, 'weight-distribution groups', len(reps), 'codes NOT mapped to their group rep', bad,
      'codes with odd words', nodd, 'time %.0fs' % (time.time() - t0))
for k in reps: print(k)
