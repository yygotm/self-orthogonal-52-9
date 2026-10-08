"""Agent B (step 2): independent check of the "one orbit" claims in PROOF.md
sec.5 (A type: 5,376 seventh rows -> 1 orbit, 36 eighth rows -> 1 class = D2)
and sec.6 (10,752 seventh rows -> 1 orbit, 24 eighth rows -> 1 class = D1).

Candidate generation is copied from the author's normalized36_orbits.py /
normalized32_orbits.py (Agent A reproduced those counts independently).
Equivalence is tested WITHOUT the author's permutation group: two binary codes
of equal length are permutation-equivalent iff some bases a, b satisfy
wt(sum_S a_i) = wt(sum_S b_i) for all S (the weight function determines the
column multiset by Walsh inversion).  Backtracking over b, rarest weights first.

usage: python verify_orbits.py 36|32 [step]   (step: test every step-th 7th row)
"""
import sys, os, time, json
from collections import defaultdict

SO52 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "so52")

def span(rows):
    a = [0]
    for r in rows:
        a += [w ^ r for w in a]
    return a

def echelon(rows):
    b = {}
    for x in rows:
        while x:
            p = x.bit_length() - 1
            if p in b: x ^= b[p]
            else: b[p] = x; break
    return b

def reduce_by(x, b):
    for p in sorted(b, reverse=True):
        if x >> p & 1: x ^= b[p]
    return x

def load(name):
    rows = [l.strip() for l in open(os.path.join(SO52, name)) if l.strip()]
    return [sum(1 << j for j, ch in enumerate(r) if ch == "1") for r in rows]

def walsh(f):
    return [sum((-1) ** (((f >> x) & 1) + ((a & x).bit_count() % 2)) for x in range(16)) for a in range(16)]

def equiv(WA, WB):
    """WA, WB: full word lists. Returns True iff permutation-equivalent."""
    from collections import Counter
    ca = Counter(x.bit_count() for x in WA); cb = Counter(x.bit_count() for x in WB)
    if ca != cb:
        return False
    # choose basis of A from rarest weights first
    order = sorted((x for x in WA if x), key=lambda x: (ca[x.bit_count()], x))
    piv = {}; a = []
    for x in order:
        v = x
        while v:
            p = v.bit_length() - 1
            if p in piv: v ^= piv[p]
            else: piv[p] = v; a.append(x); break
    k = len(a)
    byw = defaultdict(list)
    for y in WB:
        if y: byw[y.bit_count()].append(y)
    def rec(t, sA, sB):
        if t == k:
            return True
        at = a[t]
        for y in byw[at.bit_count()]:
            nb = []
            ok = True
            for x, z in zip(sA, sB):
                if (x ^ at).bit_count() != (z ^ y).bit_count():
                    ok = False; break
                nb.append(z ^ y)
            if ok and rec(t + 1, sA + [x ^ at for x in sA], sB + nb):
                return True
        return False
    return rec(0, [0], [0])

def gen36():
    cols = list(range(1, 16)) + [p for p in range(16, 32) for _ in range(2)] + [0] * 5
    K = [sum((p >> i & 1) << j for j, p in enumerate(cols)) for i in range(5)]
    g = (1 << 15) - 1 | sum(1 << (16 + 2 * x) for x in range(16)) | 31 << 47
    cw = span(K + [g])
    monos = [3, 5, 6, 9, 10, 12]; qs = []; bents = []
    for q in range(64):
        f = sum((sum((q >> i & 1) * ((x & m) == m) for i, m in enumerate(monos)) % 2) << x for x in range(16)); W = walsh(f)
        if any(abs(w) != 4 for w in W): continue
        qs.append((f, W))
        for a in range(16):
            ff = f ^ sum(((x & a).bit_count() % 2) << x for x in range(16))
            if ff.bit_count() != 6: ff ^= 65535
            bents.append((ff, walsh(ff)))
    cand = set()
    for L, WL in qs:
        h = sum((w > 0) << a for a, w in enumerate(WL))
        for B, WB in bents:
            WBH = walsh(B ^ h)
            if any(abs(w) != 4 for w in WBH): continue
            r = sum((WB[x] < 0) << (x - 1) for x in range(1, 16)) | sum(((L >> x & 1) << (15 + 2 * x)) | ((WBH[x] < 0) << (16 + 2 * x)) for x in range(16)) | 3 << 47
            assert all((r ^ w).bit_count() in (24, 32) for w in cw)
            cand.add(r)
    root = min(cand)
    rows7 = K + [g, root]; b7 = echelon(rows7); coset = [root ^ w for w in cw]; ks = set()
    for outer in [5, 9, 17, 6, 10, 18]:
        for r0 in cand:
            r = r0 ^ 3 << 47 ^ outer << 47
            if all((r ^ w).bit_count() in (24, 32) for w in coset): ks.add(reduce_by(r, b7))
    return K, g, cand, root, ks, "D-representative-2.txt"

def spread(x):
    z = 0
    while x:
        b = x & -x; z |= 1 << (2 * (b.bit_length() - 1)); x -= b
    return z

def gen32():
    cols = [p for p in range(8, 32) for _ in range(2)] + [0] * 4
    K = [sum((p >> i & 1) << j for j, p in enumerate(cols)) for i in range(5)]
    g = sum(1 << (2 * i + 1) for i in range(24)) | 15 << 48
    kb = echelon(K); all24 = (1 << 24) - 1; qmono = [3, 5, 6]
    buckets = defaultdict(list)
    for qa in range(1, 8):
        for qb in range(1, 8):
            if qa == qb: continue
            for af in range(16):
                for bf in range(16):
                    S = []
                    for x in range(8):
                        yy = []
                        for q, a in [(qa, af), (qb, bf)]:
                            z = ((x & (a & 7)).bit_count() + (a >> 3) + sum((q >> i & 1) * ((x & m) == m) for i, m in enumerate(qmono))) % 2; yy.append(z)
                        S.append(x | (yy[0] << 3) | (yy[1] << 4))
                    f = [-sum((-1) ** ((u & p).bit_count() % 2) for u in S) // 4 for p in range(8, 32)]
                    pos = sum((z == 1) << i for i, z in enumerate(f)); neg = sum((z == -1) << i for i, z in enumerate(f))
                    buckets[(qa, qb, pos | neg)].append((spread(pos), spread(neg)))
    cand = set()
    for (qa, qb, supp), items in buckets.items():
        other = buckets[(qa, qb, all24 ^ supp)]
        for p0, n0 in items:
            for p1, n1 in other:
                r = 3 * n0 | 2 * p1 | n1 | 3 << 48; cand.add(reduce_by(r, kb))
    root = min(cand)
    rows7 = K + [g, root]; b7 = echelon(rows7); coset = [root ^ w for w in span(K + [g])]; ks = set()
    for outer in [5, 6, 9, 10]:
        for r0 in sorted(cand):
            r = r0 ^ (3 << 48) ^ (outer << 48)
            if all((r ^ w).bit_count() in (24, 32) for w in coset): ks.add(reduce_by(r, b7))
    return K, g, cand, root, ks, "D-representative-1.txt"

def main():
    which = sys.argv[1]; step = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    t0 = time.time()
    K, g, cand, root, ks, repname = gen36() if which == "36" else gen32()
    print(json.dumps({"case": which, "seventh_rows": len(cand), "eighth_rows": len(ks), "gen_s": round(time.time() - t0, 1)}), flush=True)
    W7root = span(K + [g, root])
    # eighth rows: each 8-dim code must be equivalent to the representative D
    Wrep = span(load(repname))
    bad8 = [r for r in sorted(ks) if not equiv(span(K + [g, root, r]), Wrep)]
    print(json.dumps({"eighth_rows_equiv_to_rep": len(ks) - len(bad8), "bad": len(bad8), "t": round(time.time() - t0, 1)}), flush=True)
    # seventh rows: each 7-dim code must be equivalent to the root's
    tested = 0; bad7 = 0
    for i, r in enumerate(sorted(cand)):
        if i % step: continue
        tested += 1
        if not equiv(span(K + [g, r]), W7root): bad7 += 1
        if tested % 500 == 0:
            print(json.dumps({"tested": tested, "bad": bad7, "t": round(time.time() - t0, 1)}), flush=True)
    print(json.dumps({"seventh_tested": tested, "seventh_not_equiv": bad7, "t": round(time.time() - t0, 1)}), flush=True)

if __name__ == "__main__":
    main()
