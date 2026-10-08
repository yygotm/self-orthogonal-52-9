"""Construct residual [16,7,6] examples by one-dimensional neighbor search.
No completeness claim beyond the explicitly enumerated neighborhoods.
"""
from reassess import *
from triple_search import nullspace,echelon
import numpy as np

def main():
    r=[65535]+[sum(((x>>j)&1)<<x for x in range(16)) for j in range(4)]
    r+=[sum((((x&1)*((x>>1)&1))^(((x>>2)&1)*((x>>3)&1)))<<x for x in range(16)),sum((((x&1)*((x>>1)&1))^(((x>>1)&1)*((x>>3)&1))^((x&1)*((x>>2)&1)))<<x for x in range(16))]
    if '--second' in sys.argv:r=[int(s[::-1],2) for s in (OUT/'residual16-0.txt').read_text().splitlines()]
    assert inspect(r,16)['d']==6
    allvec=np.arange(1<<16,dtype=np.uint64);allvec=allvec[np.bitwise_count(allvec)%2==0]
    found={};start=time.monotonic();count=0
    for path in sorted(OUT.glob('residual16-*.txt')):
        info=inspect([int(s[::-1],2) for s in path.read_text().splitlines()],16);info.pop('columns');found[tuple(sorted(info['weights'].items()))]=info
    for u in range(1,128):
        mb=nullspace([u],7);sub=[]
        for x in mb:
            y=0
            for j,rr in enumerate(r):
                if x>>j&1:y^=rr
            sub.append(y)
        words=span(sub);cand=allvec
        for w in words:
            cand=cand[np.bitwise_count(cand^np.uint64(w))>=6]
        for v in cand:
            rows=sub+[int(v)];info=inspect(rows,16);info.pop('columns');key=tuple(sorted(info['weights'].items()))
            if key not in found:
                idx=len(found);found[key]=info;(OUT/f'residual16-{idx}.txt').write_text('\n'.join(''.join(str(rr>>j&1) for j in range(16)) for rr in rows)+'\n');print(json.dumps({'index':idx,'check':info}),flush=True)
            if len(found)==3:break
        count+=1
        if len(found)==3:break
    (OUT/'residual16.json').write_text(json.dumps({'hyperplanes_processed':count,'examples':list(found.values()),'seconds':time.monotonic()-start},indent=2))

if __name__=='__main__':main()
