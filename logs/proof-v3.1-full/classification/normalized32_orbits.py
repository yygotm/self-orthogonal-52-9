"""Classify first 7-dimensional steps over the normalized dimension-6 core.
Only the certified generated subgroup is used; full automorphism knowledge
is unnecessary. Quadratic graph enumeration is complete for 3 variables.
"""
from reassess import *
from triple_search import echelon,reduce_by
from collections import defaultdict,deque

def core():
    cols=[p for p in range(8,32) for _ in range(2)]+[0]*4
    K=[sum((p>>i&1)<<j for j,p in enumerate(cols)) for i in range(5)]
    g=sum(1<<(2*i+1) for i in range(24))|15<<48
    return K,g

def spread(x):
    z=0
    while x:
        b=x&-x;z|=1<<(2*(b.bit_length()-1));x-=b
    return z

def main():
    start=time.monotonic();K,g=core();kb=echelon(K);all24=(1<<24)-1
    qmono=[3,5,6]
    buckets=defaultdict(list)
    for qa in range(1,8):
        for qb in range(1,8):
            if qa==qb:continue
            for af in range(16):
                for bf in range(16):
                    S=[]
                    for x in range(8):
                        yy=[]
                        for q,a in [(qa,af),(qb,bf)]:
                            z=((x&(a&7)).bit_count()+(a>>3)+sum((q>>i&1)*((x&m)==m) for i,m in enumerate(qmono)))%2;yy.append(z)
                        S.append(x|(yy[0]<<3)|(yy[1]<<4))
                    f=[-sum((-1)**((u&p).bit_count()%2) for u in S)//4 for p in range(8,32)]
                    assert all(z in (-1,0,1) for z in f)
                    pos=sum((z==1)<<i for i,z in enumerate(f));neg=sum((z==-1)<<i for i,z in enumerate(f))
                    buckets[(qa,qb,pos|neg)].append((spread(pos),spread(neg)))
    cand=set();raw=0
    for (qa,qb,supp),items in buckets.items():
        other=buckets[(qa,qb,all24^supp)]
        for p0,n0 in items:
            for p1,n1 in other:
                r=3*n0|2*p1|n1|3<<48;cand.add(reduce_by(r,kb));raw+=1
    print(json.dumps({'raw':raw,'quotient':len(cand),'seconds':time.monotonic()-start}),flush=True)
    assert raw==344064 and len(cand)==10752
    # Explicit linear transformations of p preserving the excluded 3-space.
    mats=[]
    for i,j in [(0,1),(1,2),(0,2),(3,4)]:
        mat=[1<<k for k in range(5)];mat[i],mat[j]=mat[j],mat[i];mats.append(mat)
    for i,j in [(0,1),(3,4)]+[(i,j) for i in range(3) for j in [3,4]]:
        mat=[1<<k for k in range(5)];mat[j]^=1<<i;mats.append(mat)
    perms=[]
    for mat in mats:
        pp=[]
        for p in range(8,32):
            v=reduce(int.__xor__,(mat[i] for i in range(5) if p>>i&1),0)
            pp.extend([2*(v-8),2*(v-8)+1])
        perms.append(pp+list(range(48,52)))
    for i in range(5):
        perms.append([j^((8+j//2)>>i&1) if j<48 else j for j in range(52)])
    # Complement outer pair, then add g, so the fixed outer vector is restored.
    perms.append(list(range(48))+[50,51,48,49])
    cb=echelon(K+[g]);tables=[]
    for perm in perms:
        assert sorted(perm)==list(range(52))
        def tr(w):return sum((w>>j&1)<<perm[j] for j in range(52))
        assert all(reduce_by(tr(r),cb)==0 for r in K+[g])
        tb=[]
        for shift in range(0,56,8):
            tb.append([sum((x>>j&1)<<perm[shift+j] for j in range(min(8,52-shift))) for x in range(256)])
        tables.append(tb)
    remaining=set(cand);orbits=[];transport={}
    while remaining:
        root=min(remaining);remaining.remove(root);queue=deque([root]);cnt=1;transport[root]=list(range(52))
        while queue:
            r=queue.popleft()
            for ti,tb in enumerate(tables):
                v=0
                for i,t in enumerate(tb):v|=t[r>>(8*i)&255]
                if ti==len(tables)-1:v^=g
                v=reduce_by(v,kb);assert v in cand
                if v in remaining:
                    remaining.remove(v);queue.append(v);cnt+=1;transport[v]=[perms[ti][j] for j in transport[r]]
        rows=K+[g,root];ch=inspect(rows,52);ch.pop('columns');assert ch['so'] and ch['d']==24
        orbits.append({'root':root,'size':cnt,'check':ch})
        idx=len(orbits)-1;(OUT/f'normalized32-core7-{idx}.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in rows)+'\n')
        print(json.dumps({'orbit':idx,'size':cnt,'remaining':len(remaining),'seconds':time.monotonic()-start}),flush=True)
    res={'raw':raw,'quotient':len(cand),'orbits':orbits,'seconds':time.monotonic()-start}
    (OUT/'normalized32-orbits.json').write_text(json.dumps(res,indent=2))
    assert len(orbits)==1
    r1=orbits[0]['root'];rows7=K+[g,r1];basis7=echelon(rows7);coset=[r1^w for w in span(K+[g])]
    kernels=set();firstcand=sorted(cand)
    for outer in [5,6,9,10]:
        for r0 in firstcand:
            r=r0^(3<<48)^(outer<<48)
            if all((r^w).bit_count() in (24,32) for w in coset):kernels.add(reduce_by(r,basis7))
    print(json.dumps({'second_rows_quotient':len(kernels),'seconds':time.monotonic()-start}),flush=True)
    (OUT/'normalized32-second-rows.json').write_text(json.dumps(sorted(kernels)))
    # Schreier generators for the stabilizer of r1 modulo the core.
    vv=sorted(kernels);dsu={r:r for r in vv};gens=[]
    def find(x):
        while dsu[x]!=x:dsu[x]=dsu[dsu[x]];x=dsu[x]
        return x
    def apply(perm,w):return sum((w>>j&1)<<perm[j] for j in range(52))
    def consume(h):
        assert sorted(h)==list(range(52)) and all(reduce_by(apply(h,w),basis7)==0 for w in rows7)
        changed=False
        for r in vv:
            s=reduce_by(apply(h,r),basis7);assert s in kernels
            ra,rb=find(r),find(s)
            if ra!=rb:dsu[ra]=rb;changed=True
        if changed:gens.append(h)
        return len({find(r) for r in vv})
    for a,b in [(48,49),(50,51)]:
        h=list(range(52));h[a],h[b]=h[b],h[a];consume(h)
    finished=False
    for r,P in transport.items():
        for ti,pp in enumerate(perms):
            v=apply(pp,r)
            if ti==len(perms)-1:v^=g
            v=reduce_by(v,kb);Q=transport[v];inv=[0]*52
            for i,j in enumerate(Q):inv[j]=i
            h=[inv[pp[P[i]]] for i in range(52)]
            if consume(h)==1:finished=True;break
        if finished:break
    classes=defaultdict(list)
    for r in vv:classes[find(r)].append(r)
    res2={'second_rows':vv,'equivalence_classes':list(classes.values()),'certified_permutations':gens,'seconds':time.monotonic()-start}
    (OUT/'normalized32-classification.json').write_text(json.dumps(res2,indent=2))
    print(json.dumps({'kernel_classes':len(classes),'class_sizes':[len(v) for v in classes.values()],'certified_permutations':len(gens),'seconds':time.monotonic()-start}),flush=True)

if __name__=='__main__':main()
