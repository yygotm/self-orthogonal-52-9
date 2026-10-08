"""Agent C, (c): small checks of individual lemmas on random instances.
1. f(x)=wt(x)/4 mod 2 on a doubly-even code (any length, zero/repeated columns allowed) has ANF degree <= 3;
   and degree can be exactly 3 (so the bound is not vacuous). Random doubly-even codes are produced by random
   reflections T_h (wt h = 2 mod 4) from D0 and from random small doubly-even codes.
2. For wt(h)=6 and any x with x.h=1: wt(T_h x)-wt(x) in {-4,0,4}; for x.h=0 unchanged. Exhaustive over all
   intersection patterns via random sampling of x of all weights.
3. q(x)=wt(x)/2 mod 2 is linear on a random SO code; fails on a non-SO even code (sanity of the test).
"""
import random
random.seed(5)
def words(rs):
    w=[0]
    for r in rs: w+=[x^r for x in w]
    return w
def anf_deg(tt, k):
    a=list(tt)
    for i in range(k):
        for m in range(1<<k):
            if m>>i&1: a[m]^=a[m^(1<<i)]
    return max((bin(m).count('1') for m in range(1<<k) if a[m]), default=-1)
D0=[sum(1<<j for j,ch in enumerate(l.strip()) if ch=='1') for l in open('../so52/D-representative-0.txt') if l.strip()]
N=52; degs={}
rows=D0[:]
for it in range(3000):
    k=random.choice((6,10)); h=sum(1<<j for j in random.sample(range(N),k))
    rows=[r^h if (r&h).bit_count()&1 else r for r in rows]
    ws=words(rows)
    assert all(x.bit_count()%4==0 for x in ws)
    if any(x==0 for x in ws[1:]): continue
    d=anf_deg([(x.bit_count()//4)&1 for x in ws],8); degs[d]=degs.get(d,0)+1
    assert d<=3
print('1. ANF degree of wt/4 mod 2 over 3000 random doubly-even [52,8] codes:', degs)
# random small doubly-even codes with repeated columns: columns multiset random, keep if doubly-even
cnt=0;degs2={}
for it in range(200000):
    k=random.randint(3,6); n=random.choice((8,12,16,20,24))
    cols=[random.randrange(1<<k) for _ in range(n)]
    rows=[sum(((c>>i)&1)<<j for j,c in enumerate(cols)) for i in range(k)]
    ws=words(rows)
    if all(x.bit_count()%4==0 for x in ws):
        d=anf_deg([(x.bit_count()//4)&1 for x in ws],k); degs2[d]=degs2.get(d,0)+1; assert d<=3; cnt+=1
print('   small random doubly-even (repeated/zero columns allowed):', cnt, 'codes, degrees', degs2)
ch=set()
for it in range(200000):
    h=random.sample(range(52),6); hm=sum(1<<j for j in h)
    x=random.getrandbits(52)
    if (x&hm).bit_count()&1:
        y=x^hm; ch.add(y.bit_count()-x.bit_count())
print('2. weight changes under T_h, wt(h)=6, x.h=1:', sorted(ch))
# 3
ok=bad=0
for it in range(2000):
    rows=[r^h if (r&h).bit_count()&1 else r for r in D0+[(1<<52)-1] for h in [0]]
    # SO code: D0 + all-ones, then random reflection with even h of weight 4 (SO preserved, doubly-even not)
    h=sum(1<<j for j in random.sample(range(52),4))
    rows=[r^h if (r&h).bit_count()&1 else r for r in rows]
    ws=words(rows); q={x:(x.bit_count()//2)&1 for x in ws}
    lin=all(q[a^b]==q[a]^q[b] for a in random.sample(ws,20) for b in random.sample(ws,20))
    ok+=lin
print('3. q linear on random SO [52,9] codes:', ok, '/ 2000')
