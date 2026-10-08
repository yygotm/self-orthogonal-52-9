"""Agent B: f(u)=wt(uG)/4 mod 2 on F2^8 for D0,D1,D2: algebraic degree, weight, flat check."""
import os
SO52 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "so52")
def load(name):
    rows = [l.strip() for l in open(os.path.join(SO52, name)) if l.strip()]
    return [sum(1 << j for j, ch in enumerate(r) if ch == "1") for r in rows]
for nm in ["D-representative-0.txt", "D-representative-1.txt", "D-representative-2.txt"]:
    g = load(nm)
    f = []
    for u in range(256):
        x = 0
        for i in range(8):
            if (u >> i) & 1: x ^= g[i]
        assert x.bit_count() % 4 == 0
        f.append((x.bit_count() // 4) % 2)
    anf = f[:]
    for i in range(8):
        for u in range(256):
            if (u >> i) & 1: anf[u] ^= anf[u ^ (1 << i)]
    deg = max([bin(u).count("1") for u in range(256) if anf[u]], default=-1)
    supp = [u for u in range(256) if f[u]]
    flat = None
    if supp:
        v = supp[0]; S = {s ^ v for s in supp}
        flat = all((a ^ b) in S for a in S for b in S)  # S linear subspace?
    print(nm, "deg f", deg, "wt f", len(supp), "supp is affine flat:", flat)
