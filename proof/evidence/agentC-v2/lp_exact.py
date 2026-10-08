"""Exact (Fraction) phase-1 simplex, Bland's rule, for the Delsarte LP of a
doubly-even [52,9,>=24] code (q=0 branch).  Infeasible <=> phase-1 optimum > 0.
Variants: with/without B_j >= A_j (self-orthogonality), with/without A_52<=1."""
from fractions import Fraction as Fr
from math import comb
n, k = 52, 9
def K(j, w):
    return sum((-1)**s * comb(w, s) * comb(n - w, j - s) for s in range(j + 1))

def phase1(rows):
    """rows: list of (coeffs(list), sense in {'>=','<=','=='}, rhs). vars x>=0.
    returns exact phase-1 optimum (sum of artificials)."""
    nv = len(rows[0][0])
    # standard form: a x (+/- s) + art = b with b>=0
    cons = []
    nslack = sum(1 for r in rows if r[1] != '==')
    m = len(rows)
    N = nv + nslack + m
    T = []
    si = nv
    basis = []
    for i, (a, sense, b) in enumerate(rows):
        row = [Fr(0)] * (N + 1)
        for j, c in enumerate(a): row[j] = Fr(c)
        if sense == '>=': row[si] = Fr(-1); si += 1
        elif sense == '<=': row[si] = Fr(1); si += 1
        row[N] = Fr(b)
        if row[N] < 0: row = [-x for x in row]
        row[nv + nslack + i] = Fr(1)
        T.append(row); basis.append(nv + nslack + i)
    art = set(range(nv + nslack, N))
    # objective: minimize sum art -> reduced costs
    z = [Fr(0)] * (N + 1)
    for row in T:
        for j in range(N + 1): z[j] += row[j]
    for j in art: z[j] = Fr(0)
    # z[j] = sum over rows of coefficient; entering if z[j] > 0 (for j not art)
    while True:
        ent = next((j for j in range(N) if j not in art and z[j] > 0), None)
        if ent is None: break
        best = None
        for i, row in enumerate(T):
            if row[ent] > 0:
                r = row[N] / row[ent]
                if best is None or r < best[0] or (r == best[0] and basis[i] < basis[best[1]]):
                    best = (r, i)
        if best is None: raise RuntimeError('unbounded phase1?')
        i = best[1]; piv = T[i][ent]
        T[i] = [x / piv for x in T[i]]
        for r in range(len(T)):
            if r != i and T[r][ent] != 0:
                f = T[r][ent]; T[r] = [a - f * b for a, b in zip(T[r], T[i])]
        f = z[ent]; z = [a - f * b for a, b in zip(z, T[i])]
        basis[i] = ent
    return z[N], {basis[i]: T[i][N] for i in range(len(T)) if basis[i] < nv}

W = list(range(24, 53, 4))
def build(so=True, a52=True, weights=W):
    rows = [([1] * len(weights), '==', 2**k - 1)]
    if a52 and 52 in weights: rows.append(([1 if w == 52 else 0 for w in weights], '<=', 1))
    for j in range(1, n + 1):
        a = [K(j, w) for w in weights]
        b = -K(j, 0)
        if so and j in weights:
            a = [c - (2**k if w == j else 0) for c, w in zip(a, weights)]
        rows.append((a, '>=', b))
    return rows
for so in (True, False):
    for a52 in (True, False):
        val, sol = phase1(build(so, a52))
        print(f'doubly-even [52,9,>=24]: B_j>=A_j={so}, A52<=1={a52}: phase-1 optimum = {val} '
              f'({"INFEASIBLE" if val > 0 else "feasible"})', flush=True)
