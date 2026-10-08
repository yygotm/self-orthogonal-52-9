"""Exact CP model for an isometry move of prescribed support weight."""
from reassess import *
from ortools.sat.python import cp_model
import argparse

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--weight',type=int,default=8);ap.add_argument('--seconds',type=float,default=60);args=ap.parse_args()
    rows=[int(s[::-1],2) for s in (OUT/'best-fixed-seed.txt').read_text().splitlines()]
    m=cp_model.CpModel();h=[m.new_bool_var(f'h{j}') for j in range(52)];m.add(sum(h)==args.weight)
    for w in span(rows)[1:]:
        weight=w.bit_count()
        allowed=[j for j in range(min(weight,args.weight)+1) if weight+(args.weight-2*j if j%2 else 0)>=22]
        inter=m.new_int_var_from_domain(cp_model.Domain.from_values(allowed),f's{w}')
        m.add(inter==sum(h[j] for j in range(52) if w>>j&1))
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=args.seconds;solver.parameters.num_workers=4
    status=solver.solve(m);result={'weight_h':args.weight,'status':solver.status_name(status),'seconds':solver.wall_time}
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        hv=sum(solver.value(h[j])<<j for j in range(52));out=[r^hv if (r&hv).bit_count()%2 else r for r in rows];check=inspect(out,52);check.pop('columns');assert check['so'] and check['rank']==9 and check['d']>=22
        result.update(h=hv,check=check);(OUT/'SOLUTION-52-9-22.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in out)+'\n')
    (OUT/f'target-transvection-{args.weight}.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
