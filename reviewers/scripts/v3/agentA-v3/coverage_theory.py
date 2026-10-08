"""Agent A (v3): derive expected 0/2 mod 4 coverage counts of even cosets in D^perp/D from the quadratic form (Arf invariant), independent of scans."""
import sys
base=sys.argv[1]
n=52
def load(p):
    rows=[l.strip() for l in open(p) if l.strip()]
    return [int(r[::-1],2) for r in rows]
pc=lambda x: bin(x).count('1')
def reduce(v,piv):
    for h in sorted(piv,reverse=True):
        if v>>h&1: v^=piv[h]
    return v
def add(v,piv):
    v=reduce(v,piv)
    if v: piv[v.bit_length()-1]=v; return True
    return False
def dual(G):
    # nullspace of G (rows) over F2, length n
    rows=[(g,1<<i) for i,g in enumerate(G)]
    # brute: gaussian elimination on columns
    M=[[ (g>>c)&1 for c in range(n)] for g in G]
    piv_cols=[];r=0
    for c in range(n):
        p=next((i for i in range(r,len(M)) if M[i][c]),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]
        for i in range(len(M)):
            if i!=r and M[i][c]: M[i]=[a^b for a,b in zip(M[i],M[r])]
        piv_cols.append(c); r+=1
    free=[c for c in range(n) if c not in piv_cols]
    basis=[]
    for f in free:
        v=1<<f
        for i,c in enumerate(piv_cols):
            if M[i][f]: v|=1<<c
        basis.append(v)
    return basis
for i in range(3):
    G=load(f'{base}/D-representative-{i}.txt')
    Dp=dual(G)
    assert all(pc(a&b)%2==0 for a in Dp for b in G)
    # even subspace E of D^perp
    E=[];piv={}
    odd=next((v for v in Dp if pc(v)%2),None)
    Ebasis=[v if pc(v)%2==0 else v^odd for v in Dp if v!=odd]
    pivD={}
    for g in G: add(g,pivD)
    comp=[];piv=dict(pivD)
    for v in Ebasis:
        if add(v,piv): comp.append(v)
    m=len(comp)
    B=lambda x,y: pc(x&y)&1
    Q=lambda x: (pc(x)//2)&1
    # symplectic reduction
    vecs=list(comp); arf=0; h=0; rad=[]
    while vecs:
        e=vecs.pop()
        j=next((k for k,f in enumerate(vecs) if B(e,f)),None)
        if j is None:
            rad.append(e); continue
        f=vecs.pop(j)
        arf^=Q(e)&Q(f); h+=1
        new=[]
        for x in vecs:
            # project out <e,f>
            x2=x
            if B(x,f): x2^=e
            if B(x,e): x2^=f
            new.append(x2)
        vecs=new
    # radical vectors may not be independent mod earlier projections; check Q on radical span
    radQ=[Q(r) for r in rad]
    print(f'D{i}: dim(E/D)={m} hyperbolic pairs={h} radical dim={len(rad)} Q on radical={radQ} Arf={arf}')
    if all(q==0 for q in radQ):
        z=2**len(rad)*(2**(2*h-1)+(-1)**arf*2**(h-1))
        print(f'   zeros(0 mod 4 incl. trivial)={z} = 2^34{"+" if z>2**34 else "-"}2^17? {z in (2**34-2**17,2**34+2**17)}; nonzeros(2 mod 4)={2**m-z}')
