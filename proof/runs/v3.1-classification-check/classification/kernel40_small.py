"""All 32 formal distributions on <c40,u1_36,...,u4_36>.
The four residual weight-10 words have disjoint zero pairs.
Check inverse Fourier column multiplicities with exact integers.
"""
from reassess import *
from itertools import product

survivors=[];rejected=Counter()
triples=[u for u in range(16) if u.bit_count()==3]
for choices in product([0,1],repeat=5):
    weights={0:0,16:40}
    for u in range(1,16):
        s=u.bit_count()
        if s==1:w=36;j=10
        elif s==2:w=24;j=4
        elif s==3:w=24+4*choices[triples.index(u)];j=6
        else:w=24+8*choices[4];j=8
        weights[u]=w;weights[u+16]=40+2*j-w
    sums=[sum((52-2*weights[u])*(-1)**((u&v).bit_count()%2) for u in range(32)) for v in range(32)]
    if any(z%32 for z in sums):rejected['nonintegral']+=1;continue
    mult=[z//32 for z in sums]
    if min(mult)<0:rejected['negative']+=1;continue
    survivors.append({'choices':choices,'multiplicities':mult,'weights':weights})
result={'tested':32,'rejected':dict(rejected),'survivors':survivors}
(OUT/'kernel40-small.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
