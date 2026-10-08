"""Agent C: header for cosets.c (independent of the author's code and of trials/28-so-codes/ext52x/gen.py).
D: 8 x 52 generator (file: 8 lines of 0/1, char j = coordinate j).
Coset representatives of D in D^perp: span of a complement of D inside D^perp, built by
(1) computing a basis of D^perp as the null space of the generator (Gaussian elimination on columns),
(2) greedily extending a basis of D by D^perp basis vectors (rank test), keeping the 36 added vectors.
Every coset v+D (v in D^perp) is hit exactly once by the 2^36 combinations of the added vectors.
usage: python gen_hdr.py D.txt out.h
"""
import sys

def read(fn):
    rows = []
    for l in open(fn):
        l = l.strip()
        if l and l[0] in '01':
            rows.append(sum(1 << j for j, ch in enumerate(l) if ch == '1'))
    return rows

def nullspace(rows, n):
    # rows: ints (bit j = coordinate j). returns basis of {x : x.r = 0 for all r}
    piv = {}  # pivot col -> row
    red = []
    for r in rows:
        for c, pr in piv.items():
            if r >> c & 1: r ^= pr
        if r:
            c = (r & -r).bit_length() - 1
            for c2 in list(piv):
                if piv[c2] >> c & 1: piv[c2] ^= r
            piv[c] = r
    free = [j for j in range(n) if j not in piv]
    out = []
    for f in free:
        x = 1 << f
        for c, pr in piv.items():
            if pr >> f & 1: x |= 1 << c
        out.append(x)
    return out

class Span:
    def __init__(self): self.b = {}
    def add(self, v):
        for c in sorted(self.b, reverse=True):
            if v >> c & 1: v ^= self.b[c]
        if v == 0: return False
        self.b[v.bit_length() - 1] = v
        # keep reduced so the high-bit pass works
        return True

pc = lambda x: bin(x).count('1')
D = read(sys.argv[1]); n = int(sys.argv[3])
assert len(D) == 8
dual = nullspace(D, n)
assert len(dual) == n - 8
assert all(pc(x & r) % 2 == 0 for x in dual for r in D)
S = Span()
for r in D: assert S.add(r)
comp = [x for x in dual if S.add(x)]
assert len(comp) == n - 16
words = [0]
for r in D: words += [w ^ r for w in words]
assert len(set(words)) == 256 and all(pc(w) % 4 == 0 for w in words)
nz = sorted(words[1:], key=pc)
zc = n - pc(eval('|'.join(str(r) for r in D)))
with open(sys.argv[2], 'w') as f:
    f.write('#define NB %d\n' % (n - 16))
    f.write('static const unsigned long long B[NB] = {%s};\n' % ','.join('0x%xULL' % x for x in comp))
    f.write('static const unsigned long long W[255] = {%s};\n' % ','.join('0x%xULL' % x for x in nz))
from collections import Counter
print(sys.argv[1], 'zero cols', zc, 'wd', sorted(Counter(pc(w) for w in words).items()))
