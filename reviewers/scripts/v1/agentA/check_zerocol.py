"""Agent A step2: doubly-even [52,8,>=24] with z zero columns (effective length n=52-z).
Moments (weights 24,28,32,36 only) -> A28 as function of A36 and b; plus Hamming-bound facts."""
from fractions import Fraction as Fr
import sympy as sp
A24,A28,A32,A36,b=sp.symbols('A24 A28 A32 A36 b')
for n in (52,51,50):
    eqs=[sp.Eq(A24+A28+A32+A36,255),
         sp.Eq(24*A24+28*A28+32*A32+36*A36,128*n),
         sp.Eq(576*A24+784*A28+1024*A32+1296*A36,128*n+64*(n*(n-1)-2*b)+256*b)]
    s=sp.solve(eqs,[A24,A28,A32])
    print('n_eff',n,{k:sp.expand(v) for k,v in s.items()},' N=A28+A36=',sp.expand(s[A28]+A36))
# Hamming bound facts used to kill weight-36/40 words when zero columns exist
from math import comb
for (n,k,t) in [(9,6,1),(10,7,1),(8,6,1),(9,7,1)]:
    print(f'[{n},{k},3] sphere-packing: 2^{k}*(1+{n})={2**k*(1+n)} vs 2^{n}={2**n} ->', 'impossible' if 2**k*(1+n)>2**n else 'not excluded')
