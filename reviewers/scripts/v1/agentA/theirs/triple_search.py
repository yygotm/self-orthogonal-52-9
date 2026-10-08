"""Exact decomposition for the fixed cyclic [51,8,24] plus zero column.

Every v is uniquely a plus odd triple masks, with a even on every triple.
Orthogonality depends only on a. Quotient by D leaves 18 bits for a.
Certified coordinate automorphisms act on these 18 bits; each orbit needs
one 18-Boolean distance problem (17 triple bits and the extra coordinate).
"""
from reassess import *
from itertools import combinations
import argparse

def echelon(rows):
    b={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in b:x^=b[p]
            else:b[p]=x;break
    return b

def reduce_by(x,b):
    for p in sorted(b,reverse=True):
        if x>>p&1:x^=b[p]
    return x

def nullspace(rows,n):
    b=echelon(rows);free=[p for p in range(n) if p not in b]; out=[]
    for f in free:
        x=1<<f
        for p in sorted(b):
            if (b[p]&x).bit_count()%2:x^=1<<p
        assert all((r&x).bit_count()%2==0 for r in rows)
        out.append(x)
    return out

def setup(full=False):
    poly=sum(1<<j for j in [43,42,41,37,36,33,30,29,27,26,25,22,21,20,19,17,16,13,12,10,7,5,4,0])
    rows=[poly<<s for s in range(8)]; db=echelon(rows)
    cols=[sum((r>>j&1)<<i for i,r in enumerate(rows)) for j in range(51)]
    lookup={c:j for j,c in enumerate(cols)}; triples=set()
    for i,j in combinations(range(51),2):
        k=lookup.get(cols[i]^cols[j])
        if k is not None:triples.add(tuple(sorted((i,j,k))))
    triples=sorted(triples);masks=[sum(1<<j for j in t) for t in triples]
    assert len(triples)==17 and sum(masks)==(1<<51)-1
    constraints=rows+masks+[1<<p for p in db]
    basis=nullspace(constraints,51)
    assert len(basis)==18
    eb=echelon([v|(1<<(51+i)) for i,v in enumerate(basis)]) if False else None
    # Reduction with explicit labels; each label gives the quotient coordinate.
    labelled={}
    for i,v in enumerate(basis):
        lab=1<<i
        while v:
            p=v.bit_length()-1
            if p in labelled:v^=labelled[p][0];lab^=labelled[p][1]
            else:labelled[p]=(v,lab);break
    def encode(v):
        lab=0
        while v:
            p=v.bit_length()-1;w,t=labelled[p];v^=w;lab^=t
        return lab
    gens=[]
    permutations=[[(j+1)%51 for j in range(51)],[(2*j)%51 for j in range(51)]]
    if full:
        from geometry import symmetries
        extra,meta=symmetries(cols);permutations+=extra
        (OUT/'geometry.json').write_text(json.dumps(meta,indent=2))
    for perm in permutations:
        def apply(v):return sum(((v>>j)&1)<<perm[j] for j in range(51))
        assert all(reduce_by(apply(r),db)==0 for r in rows)
        assert set(apply(t) for t in masks)==set(masks)
        gb=[encode(reduce_by(apply(v),db)) for v in basis]
        mapping=[0]*(1<<18)
        for x in range(1,1<<18):
            lb=x&-x;mapping[x]=mapping[x^lb]^gb[lb.bit_length()-1]
        assert len(set(mapping))==1<<18
        gens.append(mapping)
    seen=bytearray(1<<18);orbits=[]
    for x in range(1<<18):
        if seen[x]:continue
        seen[x]=1;q=[x]
        for y in q:
            for g in gens:
                z=g[y]
                if not seen[z]:seen[z]=1;q.append(z)
        orbits.append((x,len(q)))
    return rows,basis,masks,orbits

def problem(a,words,masks,limit):
    from ortools.sat.python import cp_model
    m=cp_model.CpModel();t=[m.new_bool_var(f't{j}') for j in range(17)]; b=m.new_bool_var('last')
    expressions=[]
    for w in words:
        x=a^w
        expr=x.bit_count()+sum((3-2*(x&msk).bit_count())*tj for msk,tj in zip(masks,t))+b
        m.add(expr>=22);expressions.append(expr)
    z=m.new_int_var(5,12,'quarter');m.add(expressions[0]==4*z+2)
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=limit;solver.parameters.num_workers=1
    status=solver.solve(m)
    result={'status':solver.status_name(status),'seconds':solver.wall_time}
    if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
        v=a^(solver.value(b)<<51)
        for msk,tj in zip(masks,t):
            if solver.value(tj):v^=msk
        result['v']=v
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--limit',type=float,default=0.3);ap.add_argument('--start',type=int,default=0);ap.add_argument('--count',type=int,default=10000);args=ap.parse_args()
    start=time.monotonic();rows,basis,masks,orbits=setup();words=span(rows)
    meta={'quotient_dimension':len(basis),'orbit_count':len(orbits),'orbit_sizes':dict(Counter(s for _,s in orbits)),'total':sum(s for _,s in orbits),'setup_seconds':time.monotonic()-start}
    (OUT/'triple-orbits.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta),flush=True)
    results=[];counts=Counter();fn=OUT/f'triple-results-{args.start}-{args.limit}.jsonl'
    with fn.open('w') as fh:
        for idx,(x,size) in enumerate(orbits):
            if idx<args.start or idx>=args.start+args.count:continue
            a=0
            for j,v in enumerate(basis):
                if x>>j&1:a^=v
            r=problem(a,words,masks,args.limit);r.update(orbit=idx,representative=x,size=size);counts[r['status']]+=1
            fh.write(json.dumps(r)+'\n');fh.flush()
            if 'v' in r:
                matrix=rows+[r['v']]; check=inspect(matrix,52);check.pop('columns');assert check['so'] and check['rank']==9 and check['d']>=22
                (OUT/'SOLUTION-52-9-22.txt').write_text('\n'.join(''.join(str(v>>j&1) for j in range(52)) for v in matrix)+'\n')
                print(json.dumps({'FOUND':r,'check':check}),flush=True);break
            if idx%50==0:print(json.dumps({'processed':idx+1,'counts':dict(counts),'elapsed':time.monotonic()-start}),flush=True)
    print(json.dumps({'counts':dict(counts),'elapsed':time.monotonic()-start,'file':str(fn)}),flush=True)

if __name__=='__main__':main()
