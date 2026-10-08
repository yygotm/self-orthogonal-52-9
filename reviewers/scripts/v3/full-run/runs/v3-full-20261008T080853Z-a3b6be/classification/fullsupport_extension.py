from triple_search import setup,echelon
from reassess import *
from ortools.sat.python import cp_model
import argparse

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--h',type=int,default=2251816993685511);ap.add_argument('--seconds',type=float,default=60);args=ap.parse_args()
    rows,_,_,_=setup();h=args.h
    rows=[r^h if (r&h).bit_count()%2 else r for r in rows]
    info=inspect(rows,52);info.pop('columns');assert info['d']>=24 and info['zeros']==0
    (OUT/f'fullsupport-D-{h}.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in rows)+'\n')
    m=cp_model.CpModel();v=[m.new_bool_var(f'v{j}') for j in range(52)]
    for p in echelon(rows):m.add(v[p]==0)
    for w in span(rows):
        q=m.new_int_var(5,12,f'q{w}')
        m.add(sum((1-v[j]) if w>>j&1 else v[j] for j in range(52))==4*q+2)
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=args.seconds;solver.parameters.num_workers=4;solver.parameters.random_seed=52
    st=solver.solve(m);result={'D':info,'h':h,'status':solver.status_name(st),'seconds':solver.wall_time,'stats':solver.response_stats()}
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        last=sum(solver.value(v[j])<<j for j in range(52));matrix=rows+[last];check=inspect(matrix,52);check.pop('columns');assert check['rank']==9 and check['so'] and check['d']>=22
        result['check']=check;(OUT/'SOLUTION-52-9-22.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in matrix)+'\n')
    (OUT/f'fullsupport-extension-{h}.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
