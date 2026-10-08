"""Classify binary codes by residual lifting (Claude, 2026/10/8).

classify(n, k, d, mode): all inequivalent full-support binary [n,k,>=d] codes (no zero column), mode in
{'any', 'even', 'de'} (de = doubly-even). Every such code C with minimum weight m has a weight-m word c; with c as
the first row, the other rows restricted to the complement of supp(c) form a full-support [n-m, k-1, >=ceil(m/2)]
code (the residual). Conversely C is recovered from the residual by appending m columns (1,p), p in F_2^(k-1),
i.e. a multiset y of points p with |y| = m. For each nonzero message u with residual word r_u:
  wt(r_u) + s_u >= m  and  wt(r_u) + m - s_u >= m,  s_u = sum_{u.p=1} y_p
(so c is a minimum weight word), plus the parity conditions of the mode. All lifts of all residuals, for all
m >= d, are enumerated with CP-SAT (lift.c, a plain DFS, was far slower) and reduced by a canonical form (nauty on the codeword/coordinate incidence graph).
"""
import sys, time, json, os, subprocess
from ortools.sat.python import cp_model
from multiprocessing import Pool
from pynauty import Graph, certificate

pc = lambda x: bin(x).count('1')
MODES = {'any': 0, 'even': 1, 'de': 2}
LIFT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lift')
POOL = None


def span(rows):
    w = [0]
    for r in rows: w += [x ^ r for x in w]
    return w


def canon(rows, n):
    words = [x for x in span(rows) if x]
    N = n + len(words)
    adj = {i: [] for i in range(N)}
    for t, x in enumerate(words):
        adj[n + t] = [j for j in range(n) if x >> j & 1]
    g = Graph(N, directed=False, adjacency_dict=adj, vertex_coloring=[set(range(n)), set(range(n, N))])
    return (n, len(rows), certificate(g))


def ok_mode(rows, mode):
    ws = [pc(x) for x in span(rows)]
    return mode == 'any' or (mode == 'even' and all(w % 2 == 0 for w in ws)) or (mode == 'de' and all(w % 4 == 0 for w in ws))


def lift(base, n0, k1, m, d, mode):
    """All codes (k1+1 rows, length n0+m) from residual base (k1 rows, length n0): CP-SAT enumerates the
    multisets y of points p in F_2^k1 (|y| = m)."""
    if mode == 'even' and m % 2: return []
    if mode == 'de' and m % 4: return []
    lo = max(m, d); P = 1 << k1
    md = cp_model.CpModel()
    y = [md.NewIntVar(0, m, f'y{p}') for p in range(P)]
    md.Add(sum(y) == m)
    for u in range(1, P):
        r = 0
        for i in range(k1):
            if u >> i & 1: r ^= base[i]
        wr = pc(r)
        if wr + m < lo or wr < lo - m: return []
        s = sum(y[p] for p in range(P) if pc(u & p) & 1)
        md.Add(wr + s >= lo); md.Add(wr + m - s >= lo)
        if mode in ('even', 'de'):
            q = 2 if mode == 'even' else 4
            z = md.NewIntVar(0, n0 + m, f'z{u}'); md.Add(wr + s == q * z)
            if mode == 'de':
                z2 = md.NewIntVar(0, n0 + m, f'w{u}'); md.Add(wr + m - s == 4 * z2)
    out = []
    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self): out.append([self.Value(v) for v in y])
    sv = cp_model.CpSolver(); sv.parameters.enumerate_all_solutions = True; sv.parameters.num_workers = 1
    st = sv.Solve(md, CB())
    assert st in (cp_model.OPTIMAL, cp_model.INFEASIBLE), sv.StatusName(st)
    codes = []
    for sol in out:
        cols = [p for p in range(P) for _ in range(sol[p])]
        rows = [((1 << m) - 1) << n0]
        for i in range(k1):
            rows.append(base[i] | sum(1 << (n0 + t) for t, p in enumerate(cols) if p >> i & 1))
        codes.append(rows)
    return codes


def _job(args):
    base, n0, k1, m, d, mode, n = args
    out = {}
    for rows in lift(base, n0, k1, m, d, mode):
        c = canon(rows, n)
        if c not in out: out[c] = rows
    return out


CACHE = {}
LOG = sys.stderr


def classify(n, k, d, mode='any', top_m=None):
    key = (n, k, d, mode)
    if key in CACHE: return CACHE[key]
    pk = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'class-{n}-{k}-{d}-{mode}.json')
    if os.path.exists(pk):
        CACHE[key] = json.load(open(pk)); return CACHE[key]
    if k == 1:
        res = [[(1 << n) - 1]] if n >= d and ok_mode([(1 << n) - 1], mode) else []
        CACHE[key] = res; return res
    seen = {}
    ms = top_m if top_m else range(d, n + 1)
    for m in ms:
        n0 = n - m
        if n0 < k - 1: break
        bases = classify(n0, k - 1, (m + 1) // 2, 'even' if mode == 'de' else 'any')  # residual of a doubly-even code is even
        t0 = time.time(); nsol = 0
        jobs = [(b, n0, k - 1, m, d, mode, n) for b in bases]
        for part in (POOL.imap_unordered(_job, jobs) if POOL and len(jobs) > 1 else map(_job, jobs)):
            nsol += len(part)
            for c, rows in part.items():
                if c not in seen: seen[c] = rows
        if bases:
            print(f'  [{n},{k},>={d}] {mode}: m={m}, {len(bases)} residuals, {nsol} lift classes (per residual), {len(seen)} classes so far, {time.time()-t0:.1f}s', file=LOG, flush=True)
    res = list(seen.values())
    print(f'[{n},{k},>={d}] {mode}: {len(res)} classes', file=LOG, flush=True)
    CACHE[key] = res
    return res


if __name__ == '__main__':
    n, k, d, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    POOL = Pool(int(os.environ.get('NPROC', '16')))
    res = classify(n, k, d, mode)
    with open(f'class-{n}-{k}-{d}-{mode}.json', 'w') as f: json.dump(res, f)
    print(n, k, d, mode, len(res))
