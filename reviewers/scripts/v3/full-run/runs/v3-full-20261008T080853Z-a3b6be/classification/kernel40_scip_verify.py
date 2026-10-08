"""Independent SCIP MIP encodings of the two weight-40 branches.
Solver status is evidence, not an exported formal infeasibility certificate.
"""
from reassess import *
from triple_search import nullspace,echelon
from ortools.linear_solver import pywraplp

def solve_bent():
    A=json.loads((OUT/'bent-kernel40.json').read_text())['A'];s=pywraplp.Solver.CreateSolver('SCIP');s.SetTimeLimit(60000);s.SetNumThreads(2)
    c=[s.BoolVar(f'c{j}') for j in range(64)];b=[s.BoolVar(f'b{j}') for j in range(64)];s.Add(sum(c)==28);s.Add(sum(b)==12);s.Add(b[0]==1)
    for u in range(1,64):
        z=s.BoolVar(f'z{u}');s.Add(sum((1 if (u&v).bit_count()%2==0 else -1)*c[v] for v in range(64))==8*z-4)
    for v in range(64):s.Add(sum(c[v^a] for a in A)==6-4*b[v])
    (OUT/'kernel40-bent-model.lp').write_text(s.ExportModelAsLpFormat(False))
    st=s.Solve();return {'branch':'plane','solver':s.SolverVersion(),'status':st,'INFEASIBLE':st==s.INFEASIBLE,'wall_ms':s.WallTime()}

def solve_refined():
    pts=[x for x in range(16) if x not in [0,1,2,4]];hr=[4095]+[sum(((v>>j)&1)<<i for i,v in enumerate(pts)) for j in range(4)];base=nullspace(hr,12);e=[w for w in span(base) if w.bit_count()==10]
    for r in base:
        if len(echelon(e+[r]))>len(e):e.append(r)
    ew=span(e);cases=json.loads((OUT/'kernel40-small.json').read_text())['survivors'];out=[]
    for idx,case in enumerate(cases):
        s=pywraplp.Solver.CreateSolver('SCIP');s.SetTimeLimit(60000);s.SetNumThreads(2);x=[s.BoolVar(f'x{v}') for v in range(128)];s.Add(sum(x)==40)
        for u in range(1,128):
            j=ew[u].bit_count();lo=24-j;hi=16+j;expr=sum(x[v] for v in range(128) if (u&v).bit_count()%2)
            if lo==hi:s.Add(expr==lo)
            else:
                z=s.BoolVar(f'z{u}');s.Add(expr==lo+(hi-lo)*z)
        for p in range(16):s.Add(sum(x[p+16*q] for q in range(8))==case['multiplicities'][16+p])
        first=next(p for p in range(16) if case['multiplicities'][16+p]);s.Add(x[first]==1)
        (OUT/f'kernel40-independent-{idx}.lp').write_text(s.ExportModelAsLpFormat(False))
        st=s.Solve();r={'branch':'independent','case':idx,'status':st,'INFEASIBLE':st==s.INFEASIBLE,'wall_ms':s.WallTime()};out.append(r);print(json.dumps(r),flush=True)
    return out

if __name__=='__main__':
    r=solve_bent();print(json.dumps(r),flush=True);out=[r]+solve_refined();(OUT/'kernel40-scip-verification.json').write_text(json.dumps(out,indent=2))
