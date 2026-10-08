"""Agent B: check T_h(D0) is permutation-equivalent to D1 / D2 (PROOF.md section 7).
Method: two [n,k] binary codes are permutation-equivalent iff there are bases
a (of A) and b (of B) such that wt(sum_{i in S} a_i) = wt(sum_{i in S} b_i) for
all nonempty S (the weight function on messages determines the column multiset
by Walsh inversion).  We fix a basis of A from weight-24 words and backtrack
over weight-24 words of B."""
import os, sys
sys.setrecursionlimit(10000)
SO52 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "so52")

def load(name):
    rows = [l.strip() for l in open(os.path.join(SO52, name)) if l.strip()]
    return [sum(1 << j for j, ch in enumerate(r) if ch == "1") for r in rows]

def span(g):
    w = [0]
    for x in g:
        w += [y ^ x for y in w]
    return w

def T(x, h):
    return x ^ h if (x & h).bit_count() % 2 else x

def basis_from(words):
    piv = {}; out = []
    for x in words:
        v = x
        while v:
            p = v.bit_length() - 1
            if p in piv: v ^= piv[p]
            else: piv[p] = v; out.append(x); break
    return out

def equiv(WA, WB, w=24):
    a = basis_from([x for x in WA if x.bit_count() == w])
    k = len(a)
    assert len(span(a)) == len(set(WA))
    # target weights for prefix sums
    cand = [x for x in WB if x.bit_count() == w]
    def rec(t, sumsA, sumsB):
        if t == k:
            return True
        for y in cand:
            ok = True
            newB = []
            for sa, sb in zip(sumsA, sumsB):
                if (sa ^ a[t]).bit_count() != (sb ^ y).bit_count():
                    ok = False; break
                newB.append(sb ^ y)
            if not ok:
                continue
            if rec(t + 1, sumsA + [sa ^ a[t] for sa in sumsA], sumsB + newB):
                return True
        return False
    return rec(0, [0], [0])

W0 = span(load("D-representative-0.txt"))
for h, nm in [(2251816993685511, "D-representative-1.txt"), (2251834173685767, "D-representative-2.txt")]:
    img = [T(x, h) for x in W0]
    WB = span(load(nm))
    print(nm, "h weight", h.bit_count(), "contains coord 51:", bool((h >> 51) & 1),
          "T_h(D0) ~ rep:", equiv(img, WB), flush=True)
