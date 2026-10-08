"""Agent B v2 step 2: check A's double-counting argument for q=0 (doubly-even [52,9,24]).
Recompute weight distributions of D-representative-0/1/2 and 511*(A32+A36)/255.
usage: python double_count.py SO52_V2_DIR"""
import sys
from fractions import Fraction
from collections import Counter
d=sys.argv[1]
for i in range(3):
    rows=[sum(1<<j for j,ch in enumerate(l.strip()) if ch=='1') for l in open(f'{d}/D-representative-{i}.txt') if l.strip() and l.strip()[0] in '01']
    w=[0]
    for r in rows: w+=[x^r for x in w]
    c=Counter(x.bit_count() for x in w)
    print(i,len(rows),dict(sorted(c.items())),'A32+A36=',c[32]+c[36])
print('511*51/255 =',Fraction(511*51,255))
# sanity of incidence: in F2^9 each nonzero vector lies in 255 of 511 hyperplanes
n=0
for h in range(1,512):
    if bin(h&1).count('1')%2==0: n+=1
print('hyperplanes containing e1:',n)
