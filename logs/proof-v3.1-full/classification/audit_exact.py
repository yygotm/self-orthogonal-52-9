"""Bounded independent checks of the exact arithmetic and final artifacts."""
from reassess import *
from triple_search import span as _unused, setup, echelon, reduce_by, nullspace
from exact36 import binary_affine
import random

def main():
    rng=random.Random(520922);tests=0
    for k in range(1,9):
        for trial in range(40):
            A=[[rng.randrange(8) for _ in range(k)] for _ in range(rng.randrange(1,13))];b=[rng.randrange(8) for _ in A]
            actual={z for z in range(1<<k) if all(sum(r[j]*(z>>j&1) for j in range(k))%8==v for r,v in zip(A,b))}
            sol=binary_affine(A,b)
            if sol is None:assert not actual
            else:
                p,bs=sol;sup={p^v for v in span(bs)};assert actual<=sup and len(sup)==1<<len(bs)
            tests+=1
    # Exhaustive truth-table check: all 4-variable bent functions are quadratic.
    import numpy as np
    f=np.arange(65536,dtype=np.uint32);W=np.ones((65536,16),dtype=np.int16)
    for x in range(16):W[:,x]=1-2*((f>>x)&1).astype(np.int16)
    for step in [1,2,4,8]:
        for i in range(0,16,2*step):
            a=W[:,i:i+step].copy();b=W[:,i+step:i+2*step].copy();W[:,i:i+step]=a+b;W[:,i+step:i+2*step]=a-b
    bent=f[np.all(np.abs(W)==4,axis=1)];assert len(bent)==896
    for ff in bent:
        an=[int(ff)>>x&1 for x in range(16)]
        for i in range(4):
            for x in range(16):
                if x>>i&1:an[x]^=an[x^(1<<i)]
        assert all(not c or x.bit_count()<=2 for x,c in enumerate(an))
    # Check the all-ones residual's cubic spectrum directly, avoiding a
    # dependence on the second-weight theorem of Reed--Muller codes.
    er=[int(s[::-1],2) for s in (OUT/'residual16-1.txt').read_text().splitlines()];ew=span(er)
    mono=[z for z in range(1,128) if z.bit_count()<=3];ev=[sum(((z&u)==z)<<i for i,z in enumerate(mono)) for u in range(128)]
    bs=nullspace([ev[u] for u in range(128) if ew[u].bit_count()==6],len(mono));tv=[sum(((z&v).bit_count()%2)<<u for u,v in enumerate(ev)) for z in bs]
    dd=sum(((1+w.bit_count()//2)%2)<<u for u,w in enumerate(ew));a=0;wc=Counter()
    for z in range(1<<len(tv)):
        if z:a^=tv[(z&-z).bit_length()-1]
        wc[a.bit_count()+(a^dd).bit_count()]+=1
    assert len(tv)==16 and wc[40]==0 and wc[32]>0
    counts={}
    for tag,corefile,resfile,rowkey in [('32','normalized32-core7-0.txt','normalized32-classification.json','second_rows'),('36','normalized36-core7-0.txt','normalized36-second-rows-0.json',None)]:
        rr=[int(s[::-1],2) for s in (OUT/corefile).read_text().splitlines()];data=json.loads((OUT/resfile).read_text());extra=data[rowkey] if rowkey else data
        for v in extra:
            c=inspect(rr+[v],52);assert c['rank']==8 and c['so'] and c['d']==24 and max(c['weights'])==int(tag)
        counts[tag]=len(extra)
    # Explicit lower-bound witness and representative kernels.
    D,_,_,_=setup();info=inspect(D+[(1<<52)-1],52);info.pop('columns');assert info['rank']==9 and info['so'] and info['d']==20
    (OUT/'LOWER-52-9-20.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in D+[(1<<52)-1])+'\n')
    hlist=[0,2251816993685511,2251834173685767];reps=[]
    for i,h in enumerate(hlist):
        rr=[r^h if (r&h).bit_count()%2 else r for r in D];ch=inspect(rr,52);ch.pop('columns');assert ch['so'] and ch['rank']==8 and ch['d']==24
        if h:assert h.bit_count()==6 and h>>51&1
        reps.append(ch);(OUT/f'D-representative-{i}.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in rr)+'\n')
    assert [r['weights'] for r in reps]==[{0:1,24:204,32:51},{0:1,24:172,28:32,32:51},{0:1,24:174,28:30,32:49,36:2}]
    log=[json.loads(s) for s in (OUT/'joint-switch-full-0.jsonl').read_text().splitlines()];assert len(log)==23 and {r['orbit'] for r in log}==set(range(23)) and log[-1]['candidates_total']==985908
    e36=json.loads((OUT/'exact36-results.json').read_text());assert len(e36)==49 and all(r.get('valid_nonnegative_integer',0)==0 for r in e36)
    e40=json.loads((OUT/'exact40-results.json').read_text());assert len(e40)==2 and all(r.get('valid',0)==0 for br in e40 for r in br['cases'])
    res={'modular_reduction_tests':tests,'all_four_variable_truth_tables':65536,'bent_functions':896,'all_bent_quadratic':True,'all_ones_residual_cubics':65536,'all_ones_residual_cubic_weights':dict(wc),'normalized_kernels_checked':counts,'lower_bound':info,'representatives':reps,'exact36_models':49,'exact36_candidates':sum(r.get('enumerated',0) for r in e36),'exact40_candidates':sum(r.get('enumerated',0) for br in e40 for r in br['cases']),'extension_orbits_finished':23,'extension_candidates':985908}
    (OUT/'AUDIT.json').write_text(json.dumps(res,indent=2));print(json.dumps(res),flush=True)

if __name__=='__main__':main()
