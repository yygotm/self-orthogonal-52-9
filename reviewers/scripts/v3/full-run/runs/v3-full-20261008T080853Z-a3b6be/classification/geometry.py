"""Construct and explicitly certify coordinate symmetries of the elliptic ovoid.
No precomputed group order or classification is needed for their validity.
"""
import itertools

def mul(a,b):
    p=0
    while b:
        if b&1:p^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return p

def inv(a):
    assert a;return mul(a,a)

def symmetries(cols):
    loc={x:j for j,x in enumerate(cols)}
    # Scalar multiplication by omega, via the cyclic shift by 17 coordinates.
    labels={}
    def insert(v,label):
        while v:
            p=v.bit_length()-1
            if p in labels:v^=labels[p][0];label^=labels[p][1]
            else:labels[p]=(v,label);return True
        return False
    chosen=[]
    for j,x in enumerate(cols):
        if insert(x,1<<j):chosen.append(j)
        if len(chosen)==8:break
    def lin(v):
        z=0
        while v:
            p=v.bit_length()-1;w,lab=labels[p];v^=w
            for j in chosen:
                if lab>>j&1:z^=cols[(j+17)%51]
        return z
    assert all(lin(x)==cols[(j+17)%51] for j,x in enumerate(cols))
    # Four GF(4) basis vectors, expanded to eight GF(2) basis vectors.
    bb=[];span={0}
    for x in range(1,256):
        if x in span:continue
        y=lin(x);assert y not in span and (x^y) not in span
        bb.extend([x,y]);span|={v^x for v in list(span)};span|={v^y for v in list(span)}
        if len(bb)==8:break
    to_binary=[]
    for u in range(256):
        x=0
        for j,b in enumerate(bb):
            if u>>j&1:x^=b
        to_binary.append(x)
    assert len(set(to_binary))==256
    to_gf={x:u for u,x in enumerate(to_binary)}
    def vec(u):return [(u>>(2*j))&3 for j in range(4)]
    def terms(u):
        x=vec(u);return [mul(t,t) for t in x]+[mul(x[i],x[j]) for i in range(4) for j in range(i+1,4)]
    # Find homogeneous quadratic form vanishing on the 51 column vectors.
    rref={}
    for col in cols:
        row=terms(to_gf[col])
        for p,r in sorted(rref.items()):
            if row[p]:
                z=row[p];row=[a^mul(z,b) for a,b in zip(row,r)]
        p=next((i for i,t in enumerate(row) if t),None)
        if p is not None:
            z=inv(row[p]);rref[p]=[mul(z,t) for t in row]
    free=[i for i in range(10) if i not in rref];assert len(free)==1
    q=[0]*10;q[free[0]]=1
    for p,row in sorted(rref.items(),reverse=True):
        v=0
        for j in range(p+1,10):v^=mul(row[j],q[j])
        q[p]=v
    def Q(u):
        v=0
        for a,b in zip(q,terms(u)):v^=mul(a,b)
        return v
    assert {to_binary[u] for u in range(1,256) if Q(u)==0}==set(cols)
    def scale(c,u):return sum(mul(c,t)<<(2*j) for j,t in enumerate(vec(u)))
    perms=[]
    # Reflections in all nonsingular vectors; scalar multiples repeat, so dedup.
    seen=set()
    for a in range(1,256):
        qa=Q(a)
        if not qa:continue
        perm=[]
        for col in cols:
            x=to_gf[col];b=Q(x^a)^Q(x)^qa
            y=x^scale(mul(b,inv(qa)),a);perm.append(loc[to_binary[y]])
        perm=tuple(perm)
        if perm not in seen:seen.add(perm);perms.append(list(perm))
    # A handful plus the order-51 cycle normally suffice; every one is verified.
    return perms[:8],{'quadratic_coefficients':q,'reflections':len(perms),'used':min(8,len(perms))}
