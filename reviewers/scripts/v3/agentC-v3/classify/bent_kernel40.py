"""Construct the branch with two weight-40 words through a 6-variable bent set.
This is a construction/feasibility experiment; no global completeness claim.
"""
from reassess import *
from triple_search import nullspace,echelon
from ortools.sat.python import cp_model

def main():
    pts=list(range(4,16));hr=[4095]+[sum(((v>>j)&1)<<i for i,v in enumerate(pts)) for j in range(4)];basis=nullspace(hr,12)
    # Choose an information basis with all ones first.
    eb=echelon([4095]);e=[4095]
    for r in basis:
        if len(echelon(e+[r]))>len(e):e.append(r)
    assert len(e)==7
    A=[sum(((e[i+1]>>j)&1)<<i for i in range(6)) for j in range(12)];assert len(set(A))==12
    assert all(sum((-1)**((u&a).bit_count()%2) for a in A) in (-4,0,4) for u in range(1,64))
    m=cp_model.CpModel();c=[m.new_bool_var(f'c{j}') for j in range(64)];b=[m.new_bool_var(f'b{j}') for j in range(64)]
    m.add(sum(c)==28);m.add(sum(b)==12);m.add(b[0]==1)
    for u in range(1,64):
        s=m.new_bool_var(f's{u}');m.add(sum((1 if (u&v).bit_count()%2==0 else -1)*c[v] for v in range(64))==8*s-4)
    for v in range(64):m.add(sum(c[v^a] for a in A)==6-4*b[v])
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=120;solver.parameters.num_workers=4
    st=solver.solve(m);res={'status':solver.status_name(st),'seconds':solver.wall_time,'A':A}
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        B=[v for v in range(64) if solver.value(b[v])];C=[v for v in range(64) if solver.value(c[v])]
        cols=[(v<<2)|1 for v in A]+[(v<<2)|2 for v in B]+[(v<<2)|3 for v in C]
        rows=[sum(((v>>i)&1)<<j for j,v in enumerate(cols)) for i in range(8)]
        check=inspect(rows,52);check.pop('columns');assert check['rank']==8 and check['d']>=24 and all(w%4==0 for w in check['weights'])
        res.update(B=B,C=C,check=check);(OUT/'bent-kernel40.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in rows)+'\n')
    (OUT/'bent-kernel40.json').write_text(json.dumps(res,indent=2));print(json.dumps(res),flush=True)

if __name__=='__main__':main()
