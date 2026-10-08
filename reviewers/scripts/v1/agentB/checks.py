"""Agent B: small independent checks of premises used in PROOF.md.
Reads matrices from ../so52 (read only)."""
import itertools, os, sys
import networkx as nx
from networkx.algorithms import isomorphism

SO52 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "so52")

def load(name):
    rows = [l.strip() for l in open(os.path.join(SO52, name)) if l.strip()]
    n = len(rows[0])
    return n, [sum(1 << j for j, ch in enumerate(r) if ch == "1") for r in rows]

def span(gens):
    w = [0]
    for g in gens:
        w += [x ^ g for x in w]
    return w

def wd(words):
    d = {}
    for x in words:
        d[x.bit_count()] = d.get(x.bit_count(), 0) + 1
    return dict(sorted(d.items()))

def rank(gens):
    piv = {}
    r = 0
    for g in gens:
        v = g
        while v:
            p = v.bit_length() - 1
            if p in piv:
                v ^= piv[p]
            else:
                piv[p] = v; r += 1; break
    return r

def info(name):
    n, g = load(name)
    W = span(g)
    allc = 0
    for x in W:
        allc |= x
    zero = [j for j in range(n) if not (allc >> j) & 1]
    so = all((a & b).bit_count() % 2 == 0 for a in g for b in g)
    cols = [tuple((r >> j) & 1 for r in g) for j in range(n)]
    nz = [c for c in cols if any(c)]
    from collections import Counter
    cc = Counter(nz)
    b = sum(m * (m - 1) // 2 for m in cc.values())
    print(name, "n", n, "rank", rank(g), "SO", so, "wd", wd(W), "zero cols", zero, "equal-col pairs b", b)
    return n, g, W

print("== representatives")
n0, g0, W0 = info("D-representative-0.txt")
n1, g1, W1 = info("D-representative-1.txt")
n2, g2, W2 = info("D-representative-2.txt")
for nm in ["residual16-0.txt", "residual16-1.txt", "residual16-2.txt", "LOWER-52-9-20.txt"]:
    info(nm)

# T_h check
def T(x, h):
    return x ^ h if (x & h).bit_count() % 2 else x

def graph(words, n, w):
    G = nx.Graph()
    for i in range(n):
        G.add_node(("c", i), kind=0)
    for k, x in enumerate(v for v in words if v.bit_count() == w):
        G.add_node(("w", k), kind=1)
        for i in range(n):
            if (x >> i) & 1:
                G.add_edge(("c", i), ("w", k))
    return G

def equivalent(Wa, Wb, n, w):
    Ga, Gb = graph(Wa, n, w), graph(Wb, n, w)
    gm = isomorphism.GraphMatcher(Ga, Gb, node_match=lambda a, b: a["kind"] == b["kind"])
    sb = set(Wb)
    for m in gm.isomorphisms_iter():
        perm = [m[("c", i)][1] for i in range(n)]
        ok = True
        for x in Wa:
            y = 0
            for i in range(n):
                if (x >> i) & 1:
                    y |= 1 << perm[i]
            if y not in sb:
                ok = False; break
        if ok:
            return perm
    return None

print("== T_h")
for h, Wt, nm in [(2251816993685511, W1, "D1"), (2251834173685767, W2, "D2")]:
    print("h weight", h.bit_count(), "bits", [j for j in range(52) if (h >> j) & 1])
    img = [T(x, h) for x in W0]
    print(" T_h(D0) wd", wd(img), " closed under xor:", all((a ^ b) in set(img) for a in img[:20] for b in img))
    # min-weight-24 words may not span; use weight 32 words too if needed
    sp24 = rank([x for x in img if x.bit_count() == 24])
    print(" rank of weight-24 words of T_h(D0):", sp24)
    perm = equivalent(img, Wt, 52, 24)
    print(" T_h(D0) permutation-equivalent to", nm, ":", perm is not None)
