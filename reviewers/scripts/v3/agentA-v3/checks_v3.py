"""Agent A (v3): independent recheck of O1 certificate and M4 representative conditions."""
import sys
from math import comb
from fractions import Fraction
from collections import Counter
from itertools import combinations
N=52
def K(j,w,n=N):
    return sum((-1)**s*comb(w,s)*comb(n-w,j-s) for s in range(0,j+1))
F=lambda w: 23*K(1,w)+4*K(2,w)+K(3,w)
print('F(0)',F(0), '=', 23*52+4*1326+22100)
print('F on 24..52:',{w:F(w) for w in range(24,53,4)})
print('max F on 24..52', max(F(w) for w in range(24,53,4)))
print('F(20)',F(20))
# check also F for all even w>=22 (not needed but shows sharpness)
print('F even 20..52', {w:F(w) for w in range(20,53,2)})
# closed forms: K1=52-2w; K2, K3 standard
for w in range(0,53):
    assert K(1,w)==52-2*w
    assert K(2,w)==((52-2*w)**2-52)//2
# lower-bound code (d=20) must NOT be excluded by the certificate
low={0:1,20:51,24:204,28:204,32:51,52:1}
print('lower code 512*(23B1+4B2+B3)=',sum(a*F(w) for w,a in low.items()))
# MacWilliams sanity on lower code: B_j integer >=0, B_0=1
Bs=[Fraction(sum(a*K(j,w) for w,a in low.items()),512) for j in range(53)]
print('lower code B0..B4',Bs[:5],'all int>=0',all(b.denominator==1 and b>=0 for b in Bs))
# worst case bound: 28600-72*511
print('bound',28600-72*511)
# ---- M4: representatives
base=sys.argv[1]
def load(p):
    rows=[l.strip() for l in open(p) if l.strip()]
    return [int(r[::-1],2) for r in rows], len(rows[0])   # bit i = column i
for i in range(3):
    G,n=load(f'{base}/D-representative-{i}.txt')
    G2,_=load(f'{base}/evidence/so52/D-representative-{i}.txt')
    W=[0]
    for g in G: W+= [w^g for w in W]
    rank=len(set(W))==256
    wd=Counter(bin(w).count('1') for w in W)
    so=all(bin(a&b).count('1')%2==0 for a in G for b in G)
    de=all(bin(g).count('1')%4==0 for g in G)
    cols=[sum(((G[r]>>c)&1)<<r for r in range(8)) for c in range(n)]
    z=cols.count(0)
    cc=Counter(c for c in cols if c)
    b=sum(comb(m,2) for m in cc.values())
    allones=(1<<n)-1
    print(f'D{i}: n={n} same_as_evidence={G==G2} rank8={rank} SO={so} gens_doubly_even={de} wd={dict(sorted(wd.items()))} z={z} b={b} ones_in_D={allones in set(W)}')
