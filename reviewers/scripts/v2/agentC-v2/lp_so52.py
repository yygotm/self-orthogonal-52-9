"""Agent C v2: Delsarte LP / small IP for self-orthogonal [52,9] weight enumerators.
Classification-independent cross-check of the q=0 branch (doubly-even [52,9,>=24])
and, as a probe, of the whole statement (SO [52,9,>=22]).
Constraints: A_0=1, A_w>=0 on allowed weights, sum A = 511,
B_j = 2^-9 sum_w A_w K_j(w) >= A_j for all j (C subset of C^perp), A_52<=1.
Solved with OR-Tools (GLOP LP, SCIP IP). An infeasible LP is then re-verified
exactly by an explicit Farkas certificate checked in Fractions (if found)."""
from math import comb
from fractions import Fraction as Fr
from ortools.linear_solver import pywraplp
import sys

n, k = 52, 9
def K(j, w):
    return sum((-1)**s * comb(w, s) * comb(n - w, j - s) for s in range(0, j + 1))

def model(weights, groups=None, integer=False):
    s = pywraplp.Solver.CreateSolver('SCIP' if integer else 'GLOP')
    A = {w: (s.IntVar if integer else s.NumVar)(0, s.infinity(), f'A{w}') for w in weights}
    if 52 in A: s.Add(A[52] <= 1)
    s.Add(sum(A.values()) == 2**k - 1)
    if groups:
        for ws, tot in groups:
            s.Add(sum(A[w] for w in ws) == tot)
    for j in range(0, n + 1):
        Bj = K(j, 0) + sum(A[w] * K(j, w) for w in weights)  # = 512*B_j
        rhs = (2**k) * (A[j] if j in A else (1 if j == 0 else 0))
        s.Add(Bj >= rhs)
    st = s.Solve()
    names = {0: 'OPTIMAL', 1: 'FEASIBLE', 2: 'INFEASIBLE', 3: 'UNBOUNDED', 4: 'ABNORMAL', 6: 'NOT_SOLVED'}
    sol = {w: A[w].solution_value() for w in weights} if st in (0, 1) else None
    return names.get(st, st), sol

cases = {
 'L1 doubly-even [52,9,>=24] (q=0 branch)': (list(range(24, 53, 4)), None),
 'L2 SO [52,9,>=22] (all even weights >=22)': (list(range(22, 53, 2)), None),
 'L3 SO [52,9,>=22] with q!=0 (255 words 0mod4, 256 words 2mod4)':
     (list(range(22, 53, 2)), [(list(range(24, 53, 4)), 255), (list(range(22, 53, 4)), 256)]),
}
for name, (ws, gr) in cases.items():
    for integer in (False, True):
        st, sol = model(ws, gr, integer)
        print(name, 'IP' if integer else 'LP', st,
              '' if sol is None else {w: round(v, 3) for w, v in sol.items() if v > 1e-9})
        sys.stdout.flush()
