"""Lift each explicit even [16,7,6] residual across a weight-36 word."""
from reassess import *
from ortools.sat.python import cp_model

def run(idx):
    e=[int(s[::-1],2) for s in (OUT/f'residual16-{idx}.txt').read_text().splitlines()];ew=span(e)
    m=cp_model.CpModel();x=[m.new_int_var(0,2,f'x{v}') for v in range(128)];dup=[m.new_bool_var(f'b{v}') for v in range(128)]
    m.add(sum(x)==36);m.add(x[0]>=1)
    for xx,bb in zip(x,dup):m.add(xx<=1+bb);m.add(xx>=2*bb)
    m.add(sum(dup)<=2)
    for u in range(1,128):
        j=ew[u].bit_count();allowed=[i for i in range(37) if (i+j)%4==0 and 24<=i+j<=36 and 24<=36-i+j<=36]
        y=m.new_int_var_from_domain(cp_model.Domain.from_values(allowed),f'w{u}');m.add(sum(x[v] for v in range(128) if (u&v).bit_count()%2)==y)
    sol=cp_model.CpSolver();sol.parameters.max_time_in_seconds=60;sol.parameters.num_workers=4
    st=sol.solve(m);res={'residual_index':idx,'status':sol.status_name(st),'seconds':sol.wall_time}
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        cols=[v for v in range(128) for _ in range(sol.value(x[v]))];rows=[(1<<36)-1]+[sum(((v>>i)&1)<<j for j,v in enumerate(cols))|(e[i]<<36) for i in range(7)]
        check=inspect(rows,52);check.pop('columns');assert check['rank']==8 and check['d']>=24 and all(w%4==0 for w in check['weights'])
        res['check']=check;(OUT/f'kernel36-{idx}.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in rows)+'\n')
    (OUT/f'kernel36-{idx}.json').write_text(json.dumps(res,indent=2));print(json.dumps(res),flush=True)

if __name__=='__main__':
    for idx in [0,2,1]:run(idx)
