"""Lift every orbit of residual-compatible cubic weight functions.
No x[0]>0 normalization: cubic gauge has already fixed column translations.
"""
from reassess import *
from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp

def run(idx,scip=False):
    e=[int(s[::-1],2) for s in (OUT/f'residual16-{idx}.txt').read_text().splitlines()];ew=span(e)
    data=json.loads((OUT/f'residual36-cubics-{idx}.json').read_text());results=[]
    for oi,orb in enumerate(data['orbits']):
        if idx==0 and orb['weight']>64:
            results.append({'orbit':oi,'weight':orb['weight'],'status':'EXCLUDED_MOMENT_BOUND'});continue
        a=orb['a'];allowed={}
        for u in range(1,128):
            j=ew[u].bit_count();allowed[u]=[i for i in range(37) if 24<=i+j<=36 and 24<=36-i+j<=36 and (i+j)%8==4*(a>>u&1) and (i+j)%4==0]
            assert allowed[u]
        if scip:
            m=pywraplp.Solver.CreateSolver('SCIP');m.SetTimeLimit(10000);m.SetNumThreads(2);x=[m.IntVar(0,2,f'x{v}') for v in range(128)];m.Add(sum(x)==36)
            for u,vals in allowed.items():
                expr=sum(x[v] for v in range(128) if (u&v).bit_count()%2)
                if len(vals)==1:m.Add(expr==vals[0])
                else:
                    assert len(vals)==2;z=m.BoolVar(f'z{u}');m.Add(expr==vals[0]+(vals[1]-vals[0])*z)
            st=m.Solve();status={m.OPTIMAL:'OPTIMAL',m.FEASIBLE:'FEASIBLE',m.INFEASIBLE:'INFEASIBLE'}.get(st,'UNKNOWN');secs=m.WallTime()/1000;value=lambda v:int(round(v.solution_value()))
        else:
            m=cp_model.CpModel();x=[m.new_int_var(0,2,f'x{v}') for v in range(128)];m.add(sum(x)==36)
            for u,vals in allowed.items():
                y=m.new_int_var_from_domain(cp_model.Domain.from_values(vals),f'w{u}');m.add(sum(x[v] for v in range(128) if (u&v).bit_count()%2)==y)
            s=cp_model.CpSolver();s.parameters.max_time_in_seconds=10;s.parameters.num_workers=4;st=s.solve(m);status=s.status_name(st);secs=s.wall_time;value=s.value
        res={'index':idx,'orbit':oi,'weight':orb['weight'],'solver':'SCIP' if scip else 'CP-SAT','status':status,'seconds':secs}
        if status in ['OPTIMAL','FEASIBLE']:
            cols=[v for v in range(128) for _ in range(value(x[v]))];rows=[(1<<36)-1]+[sum((v>>i&1)<<j for j,v in enumerate(cols))|(e[i]<<36) for i in range(7)]
            ch=inspect(rows,52);ch.pop('columns');assert ch['so'] and ch['rank']==8 and ch['d']>=24 and all(w%4==0 for w in ch['weights'])
            assert all(((span(rows[1:])[u].bit_count()//4)%2)==(a>>u&1) for u in range(128))
            res['check']=ch;(OUT/f'kernel36-cubic-{idx}-{oi}.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in rows)+'\n')
        results.append(res);print(json.dumps(res),flush=True)
        (OUT/f'lift36-fixed-cubic-{idx}-{scip}.json').write_text(json.dumps(results,indent=2))
    return results

if __name__=='__main__':
    for idx in [0,2]:run(idx,'--scip' in sys.argv)
