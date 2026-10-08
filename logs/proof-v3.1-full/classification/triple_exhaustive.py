"""Exhaustive vectorized search of all quotient representatives, no SAT limit."""
from triple_search import *
import numpy as np

def main():
    start=time.monotonic();rows,basis,masks,orbits=setup();words=span(rows)
    odd=np.zeros(1<<17,dtype=np.uint64)
    for j,msk in enumerate(masks):odd[1<<j:1<<(j+1)]=odd[:1<<j]^np.uint64(msk|(1<<51))
    assert np.all(np.bitwise_count(odd)%2==0)
    total=0;represented=0;max_survived=0
    # All 256 distances, in fixed independently reproducible order.
    words.sort(key=lambda w:(w.bit_count()!=24,w))
    fh=(OUT/'triple-exhaustive.jsonl').open('w')
    for idx,(x,size) in enumerate(orbits):
        a=0
        for j,v in enumerate(basis):
            if x>>j&1:a^=v
        cand=odd^np.uint64(a)
        cand=cand[np.bitwise_count(cand)%4==2]
        before=len(cand);total+=before;represented+=before*size
        remaining=[]
        for w in words:
            cand=cand[np.bitwise_count(cand^np.uint64(w))>=22]
            remaining.append(len(cand))
            if not len(cand):break
        max_survived=max(max_survived,len(remaining))
        record={'orbit':idx,'representative':x,'size':size,'q2_count':before,'remaining':remaining}
        fh.write(json.dumps(record)+'\n');fh.flush()
        if len(cand):
            v=int(cand[0]);matrix=rows+[v];check=inspect(matrix,52);check.pop('columns');assert check['so'] and check['rank']==9 and check['d']>=22
            (OUT/'SOLUTION-52-9-22.txt').write_text('\n'.join(''.join(str(v>>j&1) for j in range(52)) for v in matrix)+'\n')
            print(json.dumps({'FOUND':v,'check':check}),flush=True);return
        if idx%50==0:print(json.dumps({'orbits_done':idx+1,'tested_q2_representatives':total,'covered_q2_cosets':represented,'seconds':time.monotonic()-start}),flush=True)
    result={'status':'EXHAUSTED_NO_EXTENSION_FOR_FIXED_D','orbits':len(orbits),'tested_q2_representatives':total,'covered_q2_cosets':represented,'expected_cosets':2**34+2**17,'maximum_distance_constraints_until_empty':max_survived,'seconds':time.monotonic()-start,'numpy_version':np.__version__}
    assert represented==2**34+2**17
    (OUT/'triple-exhaustive-summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
