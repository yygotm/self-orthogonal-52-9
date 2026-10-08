"""Look for exact congruence contradictions in the 49 cubic lift models.
Rows of the inverse Walsh transform give A z = b (mod 8).
Certificates are integer linear combinations, independently checkable.
"""
from reassess import *

def contradiction(A,b,mod=8):
    orig=[r[:] for r in A];rhs=b[:];n=len(A);k=len(A[0]);T=[[int(i==j) for j in range(n)] for i in range(n)]
    def valuation(x):return (x&-x) if x else mod
    for t in range(min(n,k)):
        p,i,j=min((valuation(A[i][j]),i,j) for i in range(t,n) for j in range(t,k))
        if p==mod:break
        A[t],A[i]=A[i],A[t];b[t],b[i]=b[i],b[t];T[t],T[i]=T[i],T[t]
        for row in A:row[t],row[j]=row[j],row[t]
        inv=pow(A[t][t]//p,-1,mod//p)
        A[t]=[(x*inv)%mod for x in A[t]];b[t]=b[t]*inv%mod;T[t]=[(x*inv)%mod for x in T[t]]
        for i in range(n):
            if i==t or not A[i][t]:continue
            assert A[i][t]%p==0
            mul=A[i][t]//p;A[i]=[(x-mul*y)%mod for x,y in zip(A[i],A[t])];b[i]=(b[i]-mul*b[t])%mod;T[i]=[(x-mul*y)%mod for x,y in zip(T[i],T[t])]
        for j in range(k):
            if j==t or not A[t][j]:continue
            assert A[t][j]%p==0
            mul=A[t][j]//p
            for row in A:row[j]=(row[j]-mul*row[t])%mod
    for i in range(n):
        d=math.gcd(mod,*A[i])
        if b[i]%d:
            c=T[i];lhs=[sum(c[ii]*orig[ii][j] for ii in range(n))%d for j in range(k)];rb=sum(c[ii]*rhs[ii] for ii in range(n))%d
            assert not any(lhs) and rb
            return {'modulus':d,'combination':c,'rhs':rb}
    return None

def main():
    out=[]
    for idx in [0,2]:
        erows=[int(s[::-1],2) for s in (OUT/f'residual16-{idx}.txt').read_text().splitlines()];ew=span(erows)
        for oi,o in enumerate(json.loads((OUT/f'residual36-cubics-{idx}.json').read_text())['orbits']):
            if idx==0 and o['weight']>64:continue
            choices={u:[i for i in range(37) if 24<=i+ew[u].bit_count()<=36 and 24<=36-i+ew[u].bit_count()<=36 and (i+ew[u].bit_count())%8==4*(o['a']>>u&1)] for u in range(1,128)}
            F=[36]+[36-2*choices[u][0] for u in range(1,128)];free=[u for u in range(1,128) if len(choices[u])==2]
            assert all(choices[u][1]-choices[u][0]==8 for u in free)
            numer=[sum(F[u]*(-1)**((u&v).bit_count()%2) for u in range(128)) for v in range(128)]
            if any(t%16 for t in numer):cert={'modulus':16,'direct_numerator':next(t for t in numer if t%16)}
            else:
                A=[[(-1)**((u&v).bit_count()%2)%8 for u in free] for v in range(128)];b=[t//16%8 for t in numer];cert=contradiction(A,b)
            out.append({'index':idx,'orbit':oi,'free_signs':len(free),'certificate':cert})
    (OUT/'modular36-certificates.json').write_text(json.dumps(out,indent=2));print(json.dumps({'models':len(out),'certified':sum(r['certificate'] is not None for r in out),'uncertified':[(r['index'],r['orbit']) for r in out if r['certificate'] is None]}),flush=True)

if __name__=='__main__':main()
