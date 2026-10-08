"""Integer split MacWilliams/shadow conditions around a weight-22 word.
Necessary conditions only; any feasible answer is not a code construction.
"""
from reassess import *
from ortools.sat.python import cp_model
import argparse

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--weight',type=int,default=22);ap.add_argument('--seconds',type=float,default=90);args=ap.parse_args();cw=args.weight;rest=52-cw
    start=time.monotonic();m=cp_model.CpModel();a={}
    for i in range(0,cw//2+1,2):
        for j in range(0,rest+1,2):
            if (i,j)==(0,0):a[i,j]=1
            elif i+j>=22 and cw-i+j>=22 and i+j not in (44,48,52) and cw-i+j not in (44,48,52):a[i,j]=m.new_int_var(0,255,f'a{i}_{j}')
    m.add(sum(a.values())==256)
    m.add(sum((int((i+j)%4==0)+int((cw-i+j)%4==0))*x for (i,j),x in a.items())==256)
    def av(i,j):return a.get((min(i,cw-i),j),0)*(2 if i*2==cw else 1) if 0<=i<=cw and i%2==0 else 0
    b={};s={}
    for u,v,shadow in [(u,v,shadow) for u in range(cw+1) for v in range(rest+1) for shadow in [False,True] if u%2==(cw//2%2 if shadow else 0)]:
            dest=s if shadow else b
            upper=min(math.comb(cw,u)*math.comb(rest,v),2**43)
            var=m.new_int_var(0,upper,f'{"S" if shadow else "B"}{u}_{v}');dest[u,v]=var
            co={}
            for (i,j),x in a.items():
                val=kw(rest,v,j)*(kw(cw,u,i)*((-1)**((i+j)//2) if shadow else 1)+kw(cw,u,cw-i)*((-1)**((cw-i+j)//2) if shadow else 1))
                co[i,j]=val
            g=reduce(math.gcd,[512]+list(co.values()))
            m.add(sum(co[ij]//g*x for ij,x in a.items())==512//g*var)
            if not shadow:m.add(var>=av(u,v))
    m.add(b[0,1]==0)
    if (1,0) in s:m.add(s[1,0]==0)
    if (0,1) in s:m.add(s[0,1]==0)
    # The doubled-even kernel has at most five repeated-column pairs under
    # the previously computed necessary enumerator conditions; omitted here.
    error=m.validate()
    if error:print(json.dumps({'error':error}));return
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=args.seconds;solver.parameters.num_workers=4
    status=solver.solve(m);result={'chosen_weight':cw,'status':solver.status_name(status),'seconds':solver.wall_time,'A_variables':len(a)}
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        result['split_A']={str(ij):(x if isinstance(x,int) else solver.value(x)) for ij,x in a.items() if (x if isinstance(x,int) else solver.value(x))}
        ordinary=Counter()
        for (i,j),x in a.items():
            value=x if isinstance(x,int) else solver.value(x);ordinary[i+j]+=value;ordinary[cw-i+j]+=value
        result['ordinary_A']={w:x for w,x in sorted(ordinary.items()) if x}
    (OUT/f'split-enumerator-{cw}.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
