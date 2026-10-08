"""Enumerate residual-compatible cubic functions and certified symmetries."""
from reassess import *
from triple_search import nullspace,echelon,reduce_by
from collections import defaultdict,deque

def run(idx):
    start=time.monotonic();erows=[int(s[::-1],2) for s in (OUT/f'residual16-{idx}.txt').read_text().splitlines()];ew=span(erows)
    cols=inspect(erows,16)['columns'];cset=set(cols);lookup={v:i for i,v in enumerate(cols)}
    # Vertex/edge invariants from all weight classes; always necessary for automorphisms.
    wts=sorted(set(w.bit_count() for w in ew));point=[];edge={}
    for i in range(16):point.append(tuple(sum(w.bit_count()==z and (w>>i&1) for w in ew) for z in wts))
    for i in range(16):
        for j in range(16):edge[i,j]=tuple(sum(w.bit_count()==z and (w>>i&1) and (w>>j&1) for w in ew) for z in wts)
    autos=[];nodes=0
    def visit(mp):
        nonlocal nodes
        nodes+=1
        if len(mp)==128:
            autos.append([lookup[mp[v]] for v in cols]);return
        old=[v for v in cols if v in mp]
        candidates=[]
        for a in cols:
            if a in mp:continue
            ia=lookup[a]
            choices=[b for b in cols if b not in mp.values() and point[lookup[b]]==point[ia] and all(edge[ia,lookup[c]]==edge[lookup[b],lookup[mp[c]]] for c in old)]
            candidates.append((len(choices),a,choices))
        _,a,choices=min(candidates)
        for b in choices:
            new={v^a:w^b for v,w in mp.items()}
            if any((v in cset)!=(w in cset) for v,w in new.items()):continue
            if any(v in cset and point[lookup[v]]!=point[lookup[w]] for v,w in new.items()):continue
            visit(mp|new)
    visit({0:0})
    wlookup={w:i for i,w in enumerate(ew)};umaps=[]
    for pp in autos:
        newrows=[sum((r>>j&1)<<pp[j] for j in range(16)) for r in erows]
        assert all(r in wlookup for r in newrows)
        umaps.append(span([wlookup[r] for r in newrows]))
    print(json.dumps({'index':idx,'automorphisms':len(autos),'nodes':nodes,'seconds':time.monotonic()-start}),flush=True)
    monos=[z for z in range(1,128) if z.bit_count()<=3]
    ev=[sum(((z&u)==z)<<i for i,z in enumerate(monos)) for u in range(128)]
    base=nullspace([ev[u] for u in range(128) if ew[u].bit_count()==6],len(monos))
    truths=[sum(((r&ev[u]).bit_count()%2)<<u for u in range(128)) for r in base]
    deriv=sum(((1+w.bit_count()//2)%2)<<u for u,w in enumerate(ew))
    gauges=[sum(((u>>i&1) and (deriv>>u&1))<<u for u in range(128)) for i in range(7)]
    gb=echelon(gauges);representatives=set();a=0;counts=Counter()
    for z in range(1<<len(truths)):
        if z:a^=truths[(z&-z).bit_length()-1]
        weight=a.bit_count()+(a^deriv).bit_count();counts[weight]+=1
        # Keep every weight in the required range; no weight-spectrum theorem.
        if not 48<=weight<=76:continue
        representatives.add(reduce_by(a,gb))
    def act(a,uu):return sum((a>>u&1)<<i for i,u in enumerate(uu))
    remain=set(representatives);orbits=[]
    while remain:
        root=min(remain);orb={reduce_by(act(root,uu),gb) for uu in umaps}
        assert orb<=representatives
        remain.difference_update(orb);orbits.append({'a':root,'weight':root.bit_count()+(root^deriv).bit_count(),'size':len(orb)})
    result={'index':idx,'automorphisms':autos,'cubic_dimension':len(truths),'gauge_dimension':len(gb),'weight_counts':dict(counts),'representatives':len(representatives),'orbits':orbits,'seconds':time.monotonic()-start}
    (OUT/f'residual36-cubics-{idx}.json').write_text(json.dumps(result,indent=2));print(json.dumps({'index':idx,'cubics':len(truths),'quotient':len(representatives),'orbits':len(orbits),'sizes':{str(k):v for k,v in Counter((o['weight'],o['size']) for o in orbits).items()},'seconds':result['seconds']}),flush=True)

if __name__=='__main__':
    for idx in [0,2]:run(idx)
