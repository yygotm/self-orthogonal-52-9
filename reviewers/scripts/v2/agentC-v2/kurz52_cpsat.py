"""Agent C v2: solver cross-check of the one Kurz Table 1 value used in sec.6 (f=0 case):
no binary [52,8] code without zero columns whose nonzero weights all lie in {24,32}.
Column multiset m: F2^8 minus 0 -> {0..3}; for every nonzero message u,
wt(u) = sum_{p: u.p=1} m(p) in {24,32}.  Moments force A32=67 and b=sum C(m,2)=4
(so m<=3).  WLOG (columns span F2^8, some column repeated): m(e1)>=2, m(e_i)>=1.
usage: kurz52_cpsat.py N TIME   (N=52 target; N=51 positive control, b=0, A32=51)"""
import sys
from ortools.sat.python import cp_model
N = int(sys.argv[1]); TL = float(sys.argv[2])
P = range(1, 256)
md = cp_model.CpModel()
mmax = 3 if N == 52 else 1
m = {p: md.NewIntVar(0, mmax, f'm{p}') for p in P}
y = {u: md.NewBoolVar(f'y{u}') for u in P}
for u in P:
    md.Add(sum(m[p] for p in P if bin(u & p).count('1') & 1) == 24 + 8 * y[u])
md.Add(sum(m.values()) == N)
A32 = (N * 128 - 24 * 255) // 8
md.Add(sum(y.values()) == A32)
if N == 52:
    d2 = {p: md.NewBoolVar(f'd2{p}') for p in P}
    d3 = {p: md.NewBoolVar(f'd3{p}') for p in P}
    for p in P:
        md.Add(m[p] >= 2).OnlyEnforceIf(d2[p]); md.Add(m[p] <= 1).OnlyEnforceIf(d2[p].Not())
        md.Add(m[p] == 3).OnlyEnforceIf(d3[p]); md.Add(m[p] <= 2).OnlyEnforceIf(d3[p].Not())
    md.Add(sum(d2[p] + 2 * d3[p] for p in P) == 4)   # b = sum C(m,2) = 4
    md.Add(m[1] >= 2)
for i in range(8):
    md.Add(m[1 << i] >= 1)
s = cp_model.CpSolver()
s.parameters.max_time_in_seconds = TL
s.parameters.num_workers = 16
st = s.Solve(md)
print(f'N={N} A32={A32} status={s.StatusName(st)} wall={s.WallTime():.1f}s')
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = {p: s.Value(m[p]) for p in P if s.Value(m[p])}
    # independent check of the found multiset
    ws = sorted(set(sum(c for p, c in sol.items() if bin(u & p).count('1') & 1) for u in P))
    print('weights', ws, 'sum m', sum(sol.values()))
