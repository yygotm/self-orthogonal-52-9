"""Enumerate the minimum-cubic-weight branch with two weight-36 words.
Core: [47,5,24] with 15 single columns and 16 double columns, five zeros.
The chosen weight-36 coset gives the sixth row. Bent 4-variable graphs
enumerate the remaining 7-dimensional steps. Completeness needs the
mathematical reduction recorded in RESEARCH.md; all matrices are checked.
"""
from reassess import *
from triple_search import echelon,reduce_by
from collections import defaultdict,deque

def walsh(f):return [sum((-1)**(((f>>x)&1)+((a&x).bit_count()%2)) for x in range(16)) for a in range(16)]
def apply(perm,w):return sum((w>>j&1)<<perm[j] for j in range(52))

def main():
    start=time.monotonic();cols=list(range(1,16))+[p for p in range(16,32) for _ in range(2)]+[0]*5
    K=[sum((p>>i&1)<<j for j,p in enumerate(cols)) for i in range(5)]
    g=(1<<15)-1|sum(1<<(16+2*x) for x in range(16))|31<<47
    cb=echelon(K+[g]);cw=span(K+[g]);assert g.bit_count()==36
    def canon(r):
        c=r>>15&1
        if c:r^=K[4]
        for i in range(4):
            if r>>(15+2*(1<<i))&1:r^=K[i]
        return r
    monos=[3,5,6,9,10,12];qs=[];bents=[]
    for q in range(64):
        f=sum((sum((q>>i&1)*((x&m)==m) for i,m in enumerate(monos))%2)<<x for x in range(16));W=walsh(f)
        if any(abs(w)!=4 for w in W):continue
        qs.append((f,W))
        for a in range(16):
            ff=f^sum(((x&a).bit_count()%2)<<x for x in range(16))
            if ff.bit_count()!=6:ff^=65535
            bents.append((ff,walsh(ff)))
    assert len(qs)==28 and len(bents)==448
    cand=set()
    for L,WL in qs:
        h=sum((w>0)<<a for a,w in enumerate(WL))
        for B,WB in bents:
            WBH=walsh(B^h)
            if any(abs(w)!=4 for w in WBH):continue
            r=sum((WB[x]<0)<<(x-1) for x in range(1,16))|sum(((L>>x&1)<<(15+2*x))|((WBH[x]<0)<<(16+2*x)) for x in range(16))|3<<47
            assert canon(r)==r and all((r^w).bit_count() in (24,32) for w in cw)
            cand.add(r)
    print(json.dumps({'first_rows':len(cand),'seconds':time.monotonic()-start}),flush=True)
    # AGL(4,2) on the pair labels, the corresponding GL action on singles.
    perms=[]
    for i,j in [(0,1),(1,2),(2,3),(0,0)]:
        mat=[1<<k for k in range(4)]
        if i==j:mat[1]^=1
        else:mat[i],mat[j]=mat[j],mat[i]
        pp=[]
        for x in range(1,16):pp.append(reduce(int.__xor__,(mat[i] for i in range(4) if x>>i&1),0)-1)
        for x in range(16):
            y=reduce(int.__xor__,(mat[i] for i in range(4) if x>>i&1),0);pp.extend([15+2*y,16+2*y])
        perms.append(pp+list(range(47,52)))
    for i in range(4):perms.append(list(range(15))+[15+(j^(2<<i)) for j in range(32)]+list(range(47,52)))
    perms.append(list(range(15))+[15+(j^1) for j in range(32)]+list(range(47,52)))
    for pp in perms:assert sorted(pp)==list(range(52)) and all(reduce_by(apply(pp,r),cb)==0 for r in K+[g])
    remain=set(cand);orbits=[];transport={}
    while remain:
        root=min(remain);remain.remove(root);qq=deque([root]);transport[root]=list(range(52));cnt=1
        while qq:
            r=qq.popleft()
            for pp in perms:
                v=canon(apply(pp,r));assert v in cand
                if v in remain:remain.remove(v);qq.append(v);cnt+=1;transport[v]=[pp[j] for j in transport[r]]
        orbits.append({'root':root,'size':cnt});print(json.dumps({'first_orbit':len(orbits)-1,'size':cnt}),flush=True)
    result={'first_rows':len(cand),'first_orbits':orbits,'kernels':[]}
    for idx,orb in enumerate(orbits):
        r1=orb['root'];rows7=K+[g,r1];b7=echelon(rows7);coset=[r1^w for w in cw];ks=set()
        for outer in [5,9,17,6,10,18]:
            for r0 in cand:
                r=r0^3<<47^outer<<47
                if all((r^w).bit_count() in (24,32) for w in coset):ks.add(reduce_by(r,b7))
        print(json.dumps({'first_orbit':idx,'second_rows':len(ks),'seconds':time.monotonic()-start}),flush=True)
        (OUT/f'normalized36-core7-{idx}.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in rows7)+'\n')
        (OUT/f'normalized36-second-rows-{idx}.json').write_text(json.dumps(sorted(ks)))
        result['kernels'].append({'core_index':idx,'second_rows':len(ks)})
        if len(orbits)!=1:continue
        dsu={r:r for r in ks};gens=[]
        def find(x):
            while dsu[x]!=x:dsu[x]=dsu[dsu[x]];x=dsu[x]
            return x
        def consume(h):
            assert sorted(h)==list(range(52)) and all(reduce_by(apply(h,w),b7)==0 for w in rows7)
            changed=False
            for r in ks:
                s=reduce_by(apply(h,r),b7);assert s in ks
                a,b=find(r),find(s)
                if a!=b:dsu[a]=b;changed=True
            if changed:gens.append(h)
            return len({find(r) for r in ks})
        for a,b in [(47,48),(49,50),(50,51)]:
            pp=list(range(52));pp[a],pp[b]=pp[b],pp[a];consume(pp)
        done=False
        for r,P in transport.items():
            for pp in perms:
                v=canon(apply(pp,r));Q=transport[v];inv=[0]*52
                for i,j in enumerate(Q):inv[j]=i
                hh=[inv[pp[P[i]]] for i in range(52)]
                if consume(hh)==1:done=True;break
            if done:break
        classes=defaultdict(list)
        for r in ks:classes[find(r)].append(r)
        checks=[]
        for group in classes.values():
            ch=inspect(rows7+[group[0]],52);ch.pop('columns');checks.append(ch)
        result['kernels'][-1].update(classes=list(classes.values()),certified_permutations=gens,checks=checks)
        print(json.dumps({'kernel_classes':len(classes),'sizes':[len(v) for v in classes.values()],'seconds':time.monotonic()-start}),flush=True)
    result['seconds']=time.monotonic()-start;(OUT/'normalized36-classification.json').write_text(json.dumps(result,indent=2))

if __name__=='__main__':main()
