from triple_search import *
import numpy as np
start=time.monotonic();rows,basis,masks,orbits=setup(True);words=span(rows)
odd=np.zeros(1<<17,dtype=np.uint64)
for j,msk in enumerate(masks):odd[1<<j:1<<(j+1)]=odd[:1<<j]^np.uint64(msk|(1<<51))
best=10**9;winner=None
for idx,(x,size) in enumerate(orbits):
    a=0
    for j,v in enumerate(basis):
        if x>>j&1:a^=v
    cand=odd^np.uint64(a);cand=cand[np.bitwise_count(cand)%4==2]
    for w in words:
        cand=cand[np.bitwise_count(cand^np.uint64(w))>=18]
        if not len(cand):break
    costs=np.zeros(len(cand),dtype=np.int16)
    for w in words:costs+=(np.bitwise_count(cand^np.uint64(w))==18)
    if len(cand) and int(costs.min())<best:
        best=int(costs.min());v=int(cand[int(costs.argmin())]);winner=rows+[v]
        print(json.dumps({'orbit':idx,'weight18_count':best,'v':v}),flush=True)
        (OUT/'best-fixed-seed.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in winner)+'\n')
result=inspect(winner,52);result.pop('columns');result['seconds']=time.monotonic()-start
(OUT/'best-fixed-seed.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
