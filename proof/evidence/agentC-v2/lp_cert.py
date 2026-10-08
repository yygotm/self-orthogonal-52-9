# explicit exact certificate for q=0 branch. Since all weights are even, K_{52-j}(w)=K_j(w), so
# B_49,B_50,B_51>=0 are B_3,B_2,B_1>=0.  Find y>=0 with sum_j y_j C(52,j) + 511*max_w sum_j y_j K_j(w) < 0.
from math import comb
from itertools import product
n=52
def K(j,w): return sum((-1)**s*comb(w,s)*comb(n-w,j-s) for s in range(j+1))
W=list(range(24,53,4)); J=[1,2,3]
assert all(K(52-j,w)==K(j,w) for j in J for w in W)
Kt={(j,w):K(j,w) for j in J for w in W}
for j in J: print('K_%d:'%j, {w:Kt[j,w] for w in W}, 'C(52,j)=',comb(52,j))
best=None
for y in product(range(0,201),repeat=3):
    if not any(y): continue
    c=max(sum(yj*Kt[j,w] for yj,j in zip(y,J)) for w in W)
    val=sum(yj*comb(52,j) for yj,j in zip(y,J))+511*c
    if best is None or val<best[0]: best=(val,y,c)
v,y,c=best
print('y=',y,' max_w sum_j y_j K_j(w)=',c,' certificate value=',v,'(<0 => contradiction)')
print('per-w values:',{w:sum(yj*Kt[j,w] for yj,j in zip(y,J)) for w in W})
