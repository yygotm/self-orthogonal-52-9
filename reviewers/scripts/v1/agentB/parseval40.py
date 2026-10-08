"""Agent B: check the weight-40 Parseval equality for both even [12,7,4] types,
and that 4-subsets of AG(4,2) fall in exactly 2 AGL(4,2)-orbits (by brute force
over the affine group), and that every even [12,7,4] arises this way."""
import itertools

pts = list(range(16))  # AG(4,2) points as 4-bit ints

def code_from_removed(rem):
    keep = [p for p in pts if p not in rem]
    # parity-check matrix H: rows = all-ones + 4 coordinate rows; columns (1,p)
    H = [sum(1 << j for j in range(12))] + [sum(((keep[j] >> b) & 1) << j for j in range(12)) for b in range(4)]
    words = [x for x in range(1 << 12) if all(((x & h).bit_count() % 2) == 0 for h in H)]
    return words

for name, rem in [("plane", (0, 1, 2, 3)), ("indep", (0, 1, 2, 4))]:
    W = code_from_removed(rem)
    dims = len(W).bit_length() - 1
    wd = {}
    for x in W:
        wd[x.bit_count()] = wd.get(x.bit_count(), 0) + 1
    s40 = 40 ** 2 + sum((2 * x.bit_count() - 8) ** 2 for x in W if x)
    s36 = 36 ** 2  # placeholder not used
    print(name, "dim", dims, "wd", dict(sorted(wd.items())), "sum F^2 upper", s40, "128*40", 128 * 40)

# orbits of 4-subsets under AGL(4,2)
def matvec(M, v):
    out = 0
    for i in range(4):
        if (M[i] & v).bit_count() % 2:
            out |= 1 << i
    return out

GL = []
for rows in itertools.product(range(1, 16), repeat=4):
    # invertible?
    piv = {}
    ok = True
    for r in rows:
        v = r
        while v:
            p = v.bit_length() - 1
            if p in piv:
                v ^= piv[p]
            else:
                piv[p] = v; break
        if not v:
            ok = False; break
    if ok:
        GL.append(rows)
print("|GL(4,2)|", len(GL))
subsets = set(itertools.combinations(pts, 4))
orbits = 0
seen = set()
for s in sorted(subsets):
    if s in seen:
        continue
    orbits += 1
    orb = set()
    for M in GL:
        for t in range(16):
            orb.add(tuple(sorted(matvec(M, p) ^ t for p in s)))
    seen |= orb
    print("orbit rep", s, "size", len(orb), "xor-sum", s[0] ^ s[1] ^ s[2] ^ s[3])
print("orbits", orbits)

# every even [12,7,>=4] code: dual contains all-ones; H columns (1,p) distinct since d>=3
# (two equal columns -> weight-2 codeword). So 12 distinct points of AG(4,2). Check d>=4 automatically:
# three columns with first coordinate 1 sum to first coordinate 1, never zero. OK.
