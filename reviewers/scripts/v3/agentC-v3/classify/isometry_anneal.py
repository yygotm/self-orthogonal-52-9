"""Explore SO codes without fixing their doubly-even subcode.
Moves T_h(x)=x+<x,h>h, wt(h) even, preserve the Gram form exactly.
Heuristic construction only; failure has no nonexistence implication.
"""
from reassess import *
from triple_search import setup
import numpy as np,random,argparse

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=int,default=120);ap.add_argument('--seed',type=int,default=52);args=ap.parse_args()
    rng=random.Random(args.seed);rows,basis,masks,_=setup()
    # Nontrivial even coset, excluding the all-ones extension.
    a=sum(basis[j] for j in [])
    v=0
    for m in masks:
        if rng.getrandbits(1):v^=m|(1<<51)
    rows.append(v)
    if (OUT/'best-fixed-seed.txt').exists():rows=[int(s[::-1],2) for s in (OUT/'best-fixed-seed.txt').read_text().splitlines()]
    words=np.array(span(rows),dtype=np.uint64)
    assert len(set(map(int,words)))==512 and ((1<<52)-1) not in words
    words=words[1:];weights=np.bitwise_count(words).astype(np.int16)
    def cost(w):return np.maximum(22-w,0).astype(np.int32)**2
    c=int(cost(weights).sum());best=c;bestwords=words.copy();saved_best=best;iterations=0;start=time.monotonic();lastlog=start
    while time.monotonic()-start<args.seconds:
        phase=iterations%30000;temp=12*(0.08/12)**(phase/30000)
        if phase==0 and iterations:
            words=bestwords.copy();weights=np.bitwise_count(words).astype(np.int16);c=best
        js=rng.sample(range(52),6 if rng.random()<0.12 else 4);h=sum(1<<j for j in js)
        inter=np.bitwise_count(words&np.uint64(h)).astype(np.int16);changed=(inter%2)==1
        newweights=weights+(len(js)-2*inter)*changed
        nc=int(cost(newweights).sum());delta=nc-c
        if delta<=0 or rng.random()<math.exp(-delta/temp):
            words^=changed.astype(np.uint64)*np.uint64(h);weights=newweights;c=nc
            if c<best:
                best=c;bestwords=words.copy();print(json.dumps({'best_cost':best,'distance':int(weights.min()),'iteration':iterations,'seconds':time.monotonic()-start}),flush=True)
                out=[int(words[(1<<i)-1]) for i in range(9)]
                (OUT/f'anneal-best-{args.seed}.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in out)+'\n')
                if c==0:
                    check=inspect(out,52);check.pop('columns');assert check['so'] and check['rank']==9 and check['d']>=22
                    (OUT/'SOLUTION-52-9-22.txt').write_text((OUT/f'anneal-best-{args.seed}.txt').read_text());print(json.dumps({'FOUND':check}),flush=True);return
        iterations+=1
        if time.monotonic()-lastlog>30:
            print(json.dumps({'best':best,'current':c,'iterations':iterations,'seconds':time.monotonic()-start}),flush=True);lastlog=time.monotonic()
    result={'status':'TIME_LIMIT_NO_WITNESS','best_cost':best,'iterations':iterations,'seconds':time.monotonic()-start,'seed':args.seed}
    (OUT/f'anneal-{args.seed}.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
