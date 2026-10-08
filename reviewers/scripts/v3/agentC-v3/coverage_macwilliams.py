# seen0/seen2 from MacWilliams: #{c in D^perp : wt = 0 / 2 mod 4} / |D|
from math import comb
n=52
def K(j,w): return sum((-1)**s*comb(w,s)*comb(n-w,j-s) for s in range(j+1))
dists={'D0':{0:1,24:204,32:51},'D1':{0:1,24:172,28:32,32:51},'D2':{0:1,24:174,28:30,32:49,36:2}}
for name,A in dists.items():
    B=[sum(a*K(j,w) for w,a in A.items()) for j in range(n+1)]
    assert all(b%256==0 and b>=0 for b in B); B=[b//256 for b in B]
    assert sum(B)==2**44
    m0=sum(B[j] for j in range(0,n+1,4)); m2=sum(B[j] for j in range(2,n+1,4)); odd=sum(B[j] for j in range(1,n+1,2))
    s0,s2=m0//256,m2//256
    print(name,'seen0',s0,'expected',2**34-2**17,s0==2**34-2**17,'seen2',s2,s2==2**34+2**17,'odd cosets',odd//256,odd//256==2**35, 'dual min wt',min(j for j in range(1,n+1) if B[j]))
