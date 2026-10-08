"""Independent classification of binary linear [16,7,>=6] codes (Agent B).

Every [16,7] code has an information set; move it to the first 7 coordinates
so G = [I_7 | A], A a 7x9 binary matrix.  Simultaneous row/first-7-column
permutations (S_7) and permutations of the last 9 coordinates (S_9) preserve
this shape.  The S_7 x S_9 orbit of A contains the matrix whose row-major
reading is minimal; that matrix has rows sorted ascending (row as 9-bit int,
column 0 = MSB) and columns sorted ascending (column as 7-bit int, row 0 =
MSB).  So enumerating all A with sorted rows and sorted columns and d>=6
reaches every equivalence class.  We then group by invariants and prove
equivalence inside each group with explicit permutations (networkx VF2 on the
coordinate / minimum-word incidence graph, then a direct check that the
permutation maps the whole code onto the other code).

usage: python classify16_7_6.py [even|all]
"""
import sys, itertools, time
import networkx as nx
from networkx.algorithms import isomorphism

MODE = sys.argv[1] if len(sys.argv) > 1 else "even"
GROUP = int(sys.argv[2]) if len(sys.argv) > 2 else -1
N, K, R = 16, 7, 9
D = 6

def pc(x):
    return x.bit_count()

cands = [r for r in range(1 << R) if pc(r) >= D - 1 and (MODE == "all" or pc(r) % 2 == 1)]
cands.sort()

sols = []
t0 = time.time()

def rec(rows, sums, colpref):
    # sums: list of (A-part xor, number of rows used)
    t = len(rows)
    if t == K:
        sols.append(tuple(rows))
        return
    start = rows[-1] + 1 if rows else 0
    for r in cands:
        if r < start:
            continue
        # column prefix sortedness
        newpref = [(colpref[j] << 1) | ((r >> (R - 1 - j)) & 1) for j in range(R)]
        if any(newpref[j] > newpref[j + 1] for j in range(R - 1)):
            continue
        ok = True
        newsums = []
        for s, c in sums:
            v = s ^ r
            if pc(v) + c + 1 < D:
                ok = False
                break
            newsums.append((v, c + 1))
        if not ok:
            continue
        rec(rows + [r], sums + newsums, newpref)

rec([], [(0, 0)], [0] * R)
print("mode", MODE, "solutions", len(sols), "time %.1fs" % (time.time() - t0), flush=True)

def codewords(rows):
    gens = [((1 << (N - 1 - i)) | r) for i, r in enumerate(rows)]  # identity bits on top 7 positions
    words = [0]
    for g in gens:
        words += [w ^ g for w in words]
    return words

def wd(words):
    out = [0] * (N + 1)
    for w in words:
        out[pc(w)] += 1
    return tuple(out)

def invariant(words):
    # weight distribution + multiset over coordinates of (number of min words through it)
    # + multiset over coordinate pairs of number of min words through both
    mw = [w for w in words if pc(w) == D]
    deg = sorted(sum((w >> i) & 1 for w in mw) for i in range(N))
    pair = sorted(sum(((w >> i) & 1) & ((w >> j) & 1) for w in mw) for i in range(N) for j in range(i + 1, N))
    return (wd(words), tuple(deg), tuple(pair))

def graph(words):
    mw = [w for w in words if pc(w) == D]
    G = nx.Graph()
    for i in range(N):
        G.add_node(("c", i), kind=0)
    for k, w in enumerate(mw):
        G.add_node(("w", k), kind=1)
        for i in range(N):
            if (w >> i) & 1:
                G.add_edge(("c", i), ("w", k))
    return G

def apply_perm(w, perm):
    out = 0
    for i in range(N):
        if (w >> i) & 1:
            out |= 1 << perm[i]
    return out

def equivalent(wa, wb, Ga, Gb):
    gm = isomorphism.GraphMatcher(Ga, Gb, node_match=lambda a, b: a["kind"] == b["kind"])
    sb = set(wb)
    for m in gm.isomorphisms_iter():
        perm = [m[("c", i)][1] for i in range(N)]
        if all(apply_perm(w, perm) in sb for w in wa):
            return perm
    return None

groups = {}
for s in sols:
    words = codewords(s)
    inv = invariant(words)
    groups.setdefault(inv, []).append(s)
print("invariant groups", len(groups), flush=True)

classes = []
for gi, (inv, members) in enumerate(sorted(groups.items())):
    if GROUP >= 0 and gi != GROUP:
        continue
    reps = []  # list of (rows, words, graph)
    for s in members:
        words = codewords(s)
        G = graph(words)
        found = False
        for (rs, rw, rg) in reps:
            if equivalent(words, rw, G, rg) is not None:
                found = True
                break
        if not found:
            reps.append((s, words, G))
    for (rs, rw, rg) in reps:
        classes.append((inv[0], rs))
    print("group wd", {i: c for i, c in enumerate(inv[0]) if c}, "members", len(members), "classes", len(reps), flush=True)

print("TOTAL classes", len(classes))
for wdist, rs in classes:
    print({i: c for i, c in enumerate(wdist) if c}, "A rows", [format(r, "09b") for r in rs])
print("elapsed %.1fs" % (time.time() - t0))
