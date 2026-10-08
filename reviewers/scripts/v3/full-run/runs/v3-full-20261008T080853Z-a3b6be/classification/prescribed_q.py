"""Prescribed automorphisms with the nonzero quadratic character normalized.
All columns, including multiplicities, are represented; columns 0 and e8 are
excluded because the doubly-even kernel would have a zero coordinate.
The fixed-zero-coordinate kernel case has been separately exhausted.
"""
from reassess import *
from ortools.sat.python import cp_model
import argparse

def mapping(images):
    out=[0]*512
    for x in range(1,512):
        b=x&-x;out[x]=out[x^b]^images[b.bit_length()-1]
    return out

def orbits(g):
    seen=set();out=[]
    for x in range(512):
        if x in seen:continue
        orb=[];y=x
        while y not in seen:seen.add(y);orb.append(y);y=g[y]
        out.append(orb)
    return out

def solve(kind,blocks,limit,tight=False):
    images=[1<<j for j in range(9)]
    for i in range(blocks):
        p=2*i
        images[p]=(2 if kind==3 else 1)<<p;images[p+1]=3<<p
    g=mapping(images);assert g[256]==256
    tr=[sum(((images[j]>>i)&1)<<j for j in range(9)) for i in range(9)]
    os=orbits(g);mos=orbits(mapping(tr));m=cp_model.CpModel()
    xs=[m.new_int_var(0,52//len(o),f'x{i}') if o[0] not in (0,256) else 0 for i,o in enumerate(os)]
    m.add(sum(len(o)*x for o,x in zip(os,xs))==52)
    if tight:
        ids={v:i for i,o in enumerate(os) for v in o};pairs=[]
        for o in os:
            p=o[0]
            if p==0 or p>=256:continue
            y=xs[ids[p]]+xs[ids[p+256]]
            b=m.new_bool_var(f'dup{p}');m.add(y<=1+b);m.add(y>=2*b)
            pairs.append(len(o)*b)
        m.add(sum(pairs)<=5)
    for orb in mos:
        u=orb[0]
        if not u:continue
        assert len({z>>8 for z in orb})==1
        q=(u>>8)&1
        z=m.new_int_var(5 if q else 6,12 if q else 13,f'z{u}')
        co=[sum((u&v).bit_count()%2 for v in o) for o in os]
        m.add(sum(c*x for c,x in zip(co,xs))==4*z+2*q)
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=limit;solver.parameters.num_workers=4;solver.parameters.random_seed=52
    status=solver.solve(m);r={'order':kind,'blocks':blocks,'tight_multiplicity':tight,'point_orbits':len(os),'message_orbits':len(mos),'status':solver.status_name(status),'seconds':solver.wall_time}
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        cols=[v for o,x in zip(os,xs) for v in o for _ in range(x if isinstance(x,int) else solver.value(x))]
        rows=[sum(((v>>i)&1)<<j for j,v in enumerate(cols)) for i in range(9)]
        check=inspect(rows,52);check.pop('columns');assert check['so'] and check['rank']==9 and check['d']>=22
        r['check']=check;(OUT/'SOLUTION-52-9-22.txt').write_text('\n'.join(''.join(str(v>>j&1) for j in range(52)) for v in rows)+'\n')
    (OUT/f'prescribed-q-{kind}-{blocks}-{tight}.json').write_text(json.dumps(r,indent=2));return r

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=30);ap.add_argument('--tight',action='store_true');args=ap.parse_args()
    for kind,blocks in [(3,3),(3,2),(2,4),(2,3),(2,2),(3,1),(2,1)]:
        r=solve(kind,blocks,args.seconds,args.tight);print(json.dumps(r),flush=True)
        if 'check' in r:break

if __name__=='__main__':main()
