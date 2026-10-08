"""Jointly search v and every distance-preserving weight-6 transvection h.
This is exhaustive for the one-transvection family when all 23 certified
larger-group orbits finish (the smaller cyclic group gives 695 orbits).
"""
from triple_search import *
import numpy as np

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--start',type=int,default=0);ap.add_argument('--count',type=int,default=695);args=ap.parse_args()
    start=time.monotonic();rows,basis,masks,orbits=setup(full=True);words=span(rows); low=[w for w in words if w.bit_count()==24]
    incidence=[sum(((w>>j)&1)<<i for i,w in enumerate(low)) for j in range(51)];hs=[]
    for a,b,c,d in combinations(range(50),4):
        base=incidence[a]&incidence[b]&incidence[c]&incidence[d]
        for e in range(d+1,51):
            if not(base&incidence[e]):hs.append((1<<51)|(1<<a)|(1<<b)|(1<<c)|(1<<d)|(1<<e))
    hs=np.array(hs,dtype=np.uint64)
    odd=np.zeros(1<<17,dtype=np.uint64)
    for j,msk in enumerate(masks):odd[1<<j:1<<(j+1)]=odd[:1<<j]^np.uint64(msk|(1<<51))
    words.sort(key=lambda w:(w.bit_count()!=24,w));wa=np.array(words,dtype=np.uint64)
    log=(OUT/f'joint-switch-full-{args.start}.jsonl').open('w');done=0;candidates=0
    print(json.dumps({'h_count':len(hs),'orbits':len(orbits),'setup_seconds':time.monotonic()-start}),flush=True)
    for idx,(x,size) in enumerate(orbits):
        if idx<args.start or idx>=args.start+args.count:continue
        a=0
        for j,v in enumerate(basis):
            if x>>j&1:a^=v
        cand=odd^np.uint64(a);cand=cand[np.bitwise_count(cand)%4==2]
        for w in words:
            cand=cand[np.bitwise_count(cand^np.uint64(w))>=18]
            if not len(cand):break
        candidates+=len(cand)
        for vn in cand:
            coset=wa^vn;weights=np.bitwise_count(coset)
            options=hs
            for w in coset[weights==18]:
                options=options[np.bitwise_count(options&w)==1]
                if not len(options):break
            if not len(options):continue
            for w in coset[weights==22]:
                options=options[np.bitwise_count(options&w)!=5]
                if not len(options):break
            if len(options):
                h=int(options[0]);v=int(vn);out=[r^h if (r&h).bit_count()%2 else r for r in rows+[v]]
                check=inspect(out,52);check.pop('columns');assert check['so'] and check['rank']==9 and check['d']>=22
                (OUT/'SOLUTION-52-9-22.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in out)+'\n')
                result={'FOUND':True,'orbit':idx,'a':a,'v':v,'h':h,'check':check,'seconds':time.monotonic()-start}
                (OUT/'joint-switch-SOLUTION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);return
        done+=1;r={'orbit':idx,'surviving_d18':len(cand),'orbits_done':done,'candidates_total':candidates,'seconds':time.monotonic()-start}
        log.write(json.dumps(r)+'\n');log.flush()
        if done%10==0 or done==1:print(json.dumps(r),flush=True)
    result={'status':'EXHAUSTED_ALL_ORBITS' if done==len(orbits) else 'EXHAUSTED_SELECTED_ORBITS','orbits_done':done,'orbits_total':len(orbits),'h_count':len(hs),'candidates_total':candidates,'seconds':time.monotonic()-start}
    (OUT/'joint-switch-summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
