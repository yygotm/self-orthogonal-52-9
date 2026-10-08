import pickle, sys
from collections import Counter
def info(rows):
    k=len(rows); ws=Counter(); sup=0
    for r in rows: sup|=r
    for m in range(1,1<<k):
        v=0
        for i in range(k):
            if m>>i&1: v^=rows[i]
        ws[bin(v).count('1')]+=1
    return bin(sup).count('1'), min(ws), all(w%8==0 for w in ws)
for p,k in [('D52.pkl',8),('T51.pkl',7)]+[(f'class-{n}-6-24-de.pkl',6) for n in (48,49,50)]:
    codes=pickle.load(open(sys.argv[1]+'/'+p,'rb'))
    c=Counter()
    for rows in codes:
        rows=list(rows); assert len(rows)==k
        neff,d,e8=info(rows)
        if e8: c[(neff,d)]+=1
    print(p,len(codes),'8-div by (neff,d):',dict(sorted(c.items())))
