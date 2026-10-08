"""Exact replacement of both weight-40 MIP branches using cubic functions."""
from reassess import *
from triple_search import nullspace,echelon,reduce_by
from exact36 import binary_affine

def main():
    out=[]
    for deleted in [[0,1,2,3],[0,1,2,4]]:
        pts=[p for p in range(16) if p not in deleted];hr=[4095]+[sum((p>>j&1)<<i for i,p in enumerate(pts)) for j in range(4)];erows=nullspace(hr,12);ew=span(erows)
        mono=[z for z in range(1,128) if z.bit_count()<=3];ev=[sum(((z&u)==z)<<i for i,z in enumerate(mono)) for u in range(128)]
        base=nullspace([ev[u] for u in range(128) if ew[u].bit_count() in [4,8,12]],len(mono));truths=[sum(((r&ev[u]).bit_count()%2)<<u for u in range(128)) for r in base]
        deriv=sum((w.bit_count()//2%2)<<u for u,w in enumerate(ew));gauge=echelon([sum(((u>>i&1) and (deriv>>u&1))<<u for u in range(128)) for i in range(7)])
        assert len(truths)<=22
        reps=set();a=0
        for z in range(1<<len(truths)):
            if z:a^=truths[(z&-z).bit_length()-1]
            reps.add(reduce_by(a,gauge))
        print(json.dumps({'deleted':deleted,'cubic_dimension':len(truths),'gauge':len(gauge),'representatives':len(reps)}),flush=True)
        results=[]
        for ai,a in enumerate(sorted(reps)):
            cs={u:sorted(set(i for i in [24-ew[u].bit_count(),16+ew[u].bit_count()] if (i+ew[u].bit_count())%8==4*(a>>u&1))) for u in range(1,128)}
            assert all(cs.values());F=[40]+[40-2*cs[u][0] for u in range(1,128)];free=[u for u in range(1,128) if len(cs[u])==2];scales=[(cs[u][1]-cs[u][0])//8 for u in free]
            numer=[sum(F[u]*(-1)**((u&v).bit_count()%2) for u in range(128)) for v in range(128)]
            if any(t%16 for t in numer):results.append({'a':a,'status':'MOD16_CONTRADICTION'});continue
            A=[[s*(-1)**((u&v).bit_count()%2)%8 for u,s in zip(free,scales)] for v in range(128)];b=[t//16%8 for t in numer];sol=binary_affine(A,b)
            if sol is None:results.append({'a':a,'status':'MODULAR_CONTRADICTION'});continue
            p,bs=sol;assert len(bs)<=22
            masks=[sum(((u&v).bit_count()%2 and s==sv)<<i for i,(u,s) in enumerate(zip(free,scales))) for v in range(128) for sv in [1,2]];s1=sum((s==1)<<i for i,s in enumerate(scales));s2=sum((s==2)<<i for i,s in enumerate(scales))
            valid=0;bad=Counter();z=p
            for t in range(1<<len(bs)):
                if t:z^=bs[(t&-t).bit_length()-1]
                nz=(z&s1).bit_count()+2*(z&s2).bit_count()
                for v in range(128):
                    q=numer[v]//16-nz+2*(z&masks[2*v]).bit_count()+4*(z&masks[2*v+1]).bit_count()
                    if q%8:bad['nonintegral']+=1;break
                    if q not in (0,8):bad['not_binary']+=1;break
                else:valid+=1
            rr={'a':a,'status':'EXHAUSTED','binary_dimension':len(bs),'enumerated':1<<len(bs),'valid':valid,'rejected':dict(bad)};results.append(rr);print(json.dumps({'deleted':deleted,'case':ai,**rr}),flush=True)
        assert all(r.get('valid',0)==0 for r in results)
        out.append({'deleted':deleted,'cubic_dimension':len(truths),'gauge_dimension':len(gauge),'cases':results})
    (OUT/'exact40-results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'branches':2,'cases':sum(len(r['cases']) for r in out),'enumerated':sum(z.get('enumerated',0) for r in out for z in r['cases']),'valid':0}),flush=True)

if __name__=='__main__':main()
