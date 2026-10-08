"""Exact integer enumeration after modular row reduction, no optimizer."""
from reassess import *
from triple_search import echelon,nullspace

def binary_affine(A,b):
    A=[r[:] for r in A];b=b[:];n=len(A);k=len(A[0]);used=set();t=0
    while t<n and len(used)<k:
        p,i,j=min(((A[i][j]&-A[i][j]) if A[i][j] else 8,i,j) for i in range(t,n) for j in range(k) if j not in used)
        if p==8:break
        A[t],A[i]=A[i],A[t];b[t],b[i]=b[i],b[t];used.add(j)
        inv=pow(A[t][j]//p,-1,8//p);A[t]=[(z*inv)%8 for z in A[t]];b[t]=b[t]*inv%8
        for i in range(t+1,n):
            assert A[i][j]%p==0
            mul=A[i][j]//p;A[i]=[(x-mul*y)%8 for x,y in zip(A[i],A[t])];b[i]=(b[i]-mul*b[t])%8
        t+=1
    eq=[]
    for row,rhs in zip(A,b):
        d=math.gcd(8,*row)
        if rhs%d:return None
        if d<8:eq.append(sum(((v//d)%2)<<i for i,v in enumerate(row))|((rhs//d%2)<<k))
    eb={}
    for w in eq:
        while w&((1<<k)-1):
            p=(w&((1<<k)-1)).bit_length()-1
            if p in eb:w^=eb[p]
            else:eb[p]=w;break
        else:
            if w:return None
    particular=0
    for p,w in sorted(eb.items()):
        if ((w>>k)&1)^((w&particular).bit_count()%2):particular|=1<<p
    return particular,nullspace([w&((1<<k)-1) for w in eb.values()],k)

def main():
    out=[]
    for idx in [0,2]:
        erows=[int(s[::-1],2) for s in (OUT/f'residual16-{idx}.txt').read_text().splitlines()];ew=span(erows)
        for oi,o in enumerate(json.loads((OUT/f'residual36-cubics-{idx}.json').read_text())['orbits']):
            if idx==0 and o['weight']>64:continue
            cs={u:[i for i in range(37) if 24<=i+ew[u].bit_count()<=36 and 24<=36-i+ew[u].bit_count()<=36 and (i+ew[u].bit_count())%8==4*(o['a']>>u&1)] for u in range(1,128)}
            F=[36]+[36-2*cs[u][0] for u in range(1,128)];free=[u for u in range(1,128) if len(cs[u])==2]
            numer=[sum(F[u]*(-1)**((u&v).bit_count()%2) for u in range(128)) for v in range(128)]
            if any(t%16 for t in numer):out.append({'index':idx,'orbit':oi,'status':'MOD16_CONTRADICTION'});continue
            A=[[(-1)**((u&v).bit_count()%2)%8 for u in free] for v in range(128)];b=[t//16%8 for t in numer];sol=binary_affine(A,b)
            if sol is None:out.append({'index':idx,'orbit':oi,'status':'MODULAR_CONTRADICTION'});continue
            p,bs=sol;assert len(bs)<=20
            neg=[sum(((u&v).bit_count()%2)<<i for i,u in enumerate(free)) for v in range(128)]
            const=[t//16 for t in numer];z=p;valid=0;bad=Counter()
            for t in range(1<<len(bs)):
                if t:z^=bs[(t&-t).bit_length()-1]
                nz=z.bit_count();mult=[]
                for v in range(128):
                    q=const[v]-nz+2*(z&neg[v]).bit_count()
                    if q%8:bad['nonintegral']+=1;break
                    if q<0:bad['negative']+=1;break
                    mult.append(q//8)
                else:
                    valid+=1;assert sum(mult)==36
            res={'index':idx,'orbit':oi,'free_signs':len(free),'binary_dimension':len(bs),'enumerated':1<<len(bs),'valid_nonnegative_integer':valid,'rejected':dict(bad),'status':'EXHAUSTED'};out.append(res);print(json.dumps(res),flush=True)
    (OUT/'exact36-results.json').write_text(json.dumps(out,indent=2));assert all(r.get('valid_nonnegative_integer',0)==0 for r in out)
    print(json.dumps({'models':len(out),'exhaustive_candidates':sum(r.get('enumerated',0) for r in out),'nonnegative_integer_solutions':0}),flush=True)

if __name__=='__main__':main()
