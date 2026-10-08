"""Refine the affine-independent residual branch by its four weight-10 words."""
from reassess import *
from triple_search import nullspace,echelon
from ortools.sat.python import cp_model

def main():
    points=[v for v in range(16) if v not in [0,1,2,4]]
    hr=[4095]+[sum(((v>>j)&1)<<i for i,v in enumerate(points)) for j in range(4)]
    base=nullspace(hr,12);ew=span(base);e=[w for w in ew if w.bit_count()==10]
    assert len(e)==4 and len(echelon(e))==4
    for r in base:
        if len(echelon(e+[r]))>len(e):e.append(r)
    assert len(e)==7;ew=span(e)
    cases=json.loads((OUT/'kernel40-small.json').read_text())['survivors'];results=[]
    for idx,case in enumerate(cases):
        m=cp_model.CpModel();x=[m.new_bool_var(f'x{j}') for j in range(128)];m.add(sum(x)==40)
        for u in range(1,128):
            j=ew[u].bit_count();lo=24-j;hi=16+j
            weight=sum(x[v] for v in range(128) if (u&v).bit_count()%2)
            if lo==hi:m.add(weight==lo)
            else:
                s=m.new_bool_var(f's{u}');m.add(weight==lo+(hi-lo)*s)
        for p in range(16):m.add(sum(x[p+16*q] for q in range(8))==case['multiplicities'][16+p])
        first=next(p for p in range(16) if case['multiplicities'][16+p]);m.add(x[first]==1)
        sol=cp_model.CpSolver();sol.parameters.max_time_in_seconds=30;sol.parameters.num_workers=4
        st=sol.solve(m);result={'case':idx,'choices':case['choices'],'status':sol.status_name(st),'seconds':sol.wall_time}
        if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            cols=[v for v in range(128) if sol.value(x[v])];rows=[(1<<40)-1]+[sum(((v>>i)&1)<<j for j,v in enumerate(cols))|(e[i]<<40) for i in range(7)]
            check=inspect(rows,52);check.pop('columns');assert check['rank']==8 and check['d']>=24 and all(w%4==0 for w in check['weights'])
            result['check']=check;(OUT/f'kernel40-refined-{idx}.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in rows)+'\n')
        results.append(result);(OUT/'kernel40-refined.json').write_text(json.dumps(results,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
