"""Doubly-even [52,8,24] with a weight-40 word.
The residual is an even [12,7,4] code, obtained by deleting four affine
points from the parity-check matrix of the extended Hamming [16,11,4].
The two affine types of four deleted points are both included.
Parseval forces the 40 inner columns to be distinct and every nontrivial
Fourier coefficient to attain its distance bound in absolute value.
"""
from reassess import *
from triple_search import nullspace
from ortools.sat.python import cp_model
import argparse

def run(missing,seconds):
    points=[v for v in range(16) if v not in missing]
    checkrows=[(1<<12)-1]+[sum(((v>>j)&1)<<i for i,v in enumerate(points)) for j in range(4)]
    e=nullspace(checkrows,12);assert len(e)==7
    ew=span(e);ewd=Counter(w.bit_count() for w in ew);assert min(w for w in ewd if w)==4
    m=cp_model.CpModel();x=[m.new_bool_var(f'x{j}') for j in range(128)];m.add(sum(x)==40)
    for u in range(1,128):
        j=ew[u].bit_count();lo=24-j;hi=16+j
        weight=sum(x[v] for v in range(128) if (u&v).bit_count()%2)
        if lo==hi:m.add(weight==lo)
        else:
            s=m.new_bool_var(f's{u}');m.add(weight==lo+(hi-lo)*s)
    # Translations of the inner column set are row additions of the weight-40 word.
    m.add(x[0]==1)
    sol=cp_model.CpSolver();sol.parameters.max_time_in_seconds=seconds;sol.parameters.num_workers=4
    st=sol.solve(m);result={'missing':missing,'residual_weights':dict(ewd),'status':sol.status_name(st),'seconds':sol.wall_time}
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        cols=[v for v in range(128) if sol.value(x[v])];rows=[(1<<40)-1]+[sum(((v>>i)&1)<<j for j,v in enumerate(cols))|(e[i]<<40) for i in range(7)]
        check=inspect(rows,52);check.pop('columns');assert check['rank']==8 and check['d']>=24 and all(w%4==0 for w in check['weights'])
        result['check']=check;(OUT/f'kernel40-{missing[-1]}.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in rows)+'\n')
    (OUT/f'kernel40-{missing[-1]}.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=60);args=ap.parse_args()
    for missing in [[0,1,2,3],[0,1,2,4]]:run(missing,args.seconds)
