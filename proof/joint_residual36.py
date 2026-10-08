"""Search C directly over a prescribed residual of its doubly-even kernel.
This searches all kernel lifts and their extensions in one model, without
first classifying the [52,8,24] kernels. High kernel weights >=40 excluded
using the separate reductions/checks; see RESEARCH.md for proof status.
"""
from reassess import *
from triple_search import echelon, nullspace
from ortools.sat.python import cp_model

def run(idx):
    erows=[int(s[::-1],2) for s in (OUT/f'residual16-{idx}.txt').read_text().splitlines()];ew=span(erows)
    m=cp_model.CpModel();x=[[m.new_int_var(0,2,f'x{p}_{b}') for b in range(2)] for p in range(128)];t=[m.new_bool_var(f't{j}') for j in range(16)]
    m.add(sum(xx for pair in x for xx in pair)==36);m.add(x[0][0]>=1)
    for p in range(128):m.add(sum(x[p])<=2)
    for j in echelon(erows):m.add(t[j]==0)
    monos=[z for z in range(1,128) if z.bit_count()<=3]
    ev=[sum(((z&u)==z)<<i for i,z in enumerate(monos)) for u in range(128)]
    base=nullspace([ev[u] for u in range(128) if ew[u].bit_count()==6],len(monos))
    coeff=[m.new_bool_var(f'cf{i}') for i in range(len(base))]
    aval=[]
    for u in range(128):
        a=m.new_bool_var(f'a{u}');aval.append(a)
        terms=[coeff[i] for i,r in enumerate(base) if (r&ev[u]).bit_count()%2]
        if terms:m.add_bool_xor(terms+[a.Not()])
        else:m.add(a==0)
    print(json.dumps({'residual':idx,'cubic_dimension':len(base)}),flush=True)
    odd=[]
    for u in range(128):
        for alpha in range(2):
            w=ew[u];jw=w.bit_count()
            if u or alpha:
                z=m.new_int_var(6,9,f'd{u}_{alpha}')
                m.add(sum(sum(x[p]) for p in range(128) if ((p&u).bit_count()+alpha)%2)+jw==4*z)
                flip=alpha*((1+jw//2)%2)
                aa=aval[u] if not flip else 1-aval[u]
                m.add_allowed_assignments([z,aval[u]],[(zz,(zz%2)^flip) for zz in range(6,10)])
                odd.append(aa)
            z=m.new_int_var(5,12,f'c{u}_{alpha}')
            inner=sum(x[p][b] for p in range(128) for b in range(2) if ((p&u).bit_count()+alpha+b)%2)
            outer=sum(1-t[j] if w>>j&1 else t[j] for j in range(16))
            m.add(inner+outer==4*z+2)
    n_odd=m.new_int_var_from_domain(cp_model.Domain.from_values([32,48,56,60,64,68,72,76,80,84,88,92,96,100,104,108,112,116,120,124,128]),'Nodd')
    m.add(sum(odd)==n_odd)
    s=cp_model.CpSolver();s.parameters.max_time_in_seconds=120;s.parameters.num_workers=4
    st=s.solve(m);res={'residual_index':idx,'status':s.status_name(st),'seconds':s.wall_time}
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        cols=[1|(p<<1)|(b<<8) for p in range(128) for b in range(2) for _ in range(s.value(x[p][b]))]
        cols+=[sum(((erows[i]>>j)&1)<<(i+1) for i in range(7))|(s.value(t[j])<<8) for j in range(16)]
        rows=[sum(((v>>i)&1)<<j for j,v in enumerate(cols)) for i in range(9)];check=inspect(rows,52);check.pop('columns');assert check['rank']==9 and check['so'] and check['d']>=22
        res['check']=check;(OUT/'SOLUTION-52-9-22.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in rows)+'\n')
    (OUT/f'joint-residual36-cubic-{idx}.json').write_text(json.dumps(res,indent=2));print(json.dumps(res),flush=True)

if __name__=='__main__':
    for idx in [0,2,1]:run(idx)
