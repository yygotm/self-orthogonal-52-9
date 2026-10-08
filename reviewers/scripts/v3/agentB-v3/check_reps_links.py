"""Agent B v3: (a) representatives' z, b, weights; (b) Krawtchouk certificate via generating
polynomials; (c) relative links in md files; (d) header identity."""
import sys, re, os, hashlib
from pathlib import Path
from collections import Counter
from math import comb
P = Path(sys.argv[1]).resolve()

def span(rows):
    out = [0]
    for r in rows: out += [w ^ r for w in out]
    return out

print('== (a) representatives')
for i in range(3):
    lines = [l.strip() for l in (P / f'D-representative-{i}.txt').read_text().splitlines() if l.strip()]
    n = len(lines[0]); k = len(lines)
    cols = [tuple(int(l[j]) for l in lines) for j in range(n)]
    z = sum(1 for c in cols if not any(c))
    cc = Counter(c for c in cols if any(c))
    b = sum(m * (m - 1) // 2 for m in cc.values())
    rows = [int(l[::-1], 2) for l in lines]
    ws = span(rows)
    rank_ok = len(set(ws)) == 2 ** k
    so = all(bin(x & y).count('1') % 2 == 0 for x in rows for y in rows)
    wd = Counter(bin(w).count('1') for w in ws)
    print(i, 'n', n, 'k', k, 'rank_ok', rank_ok, 'SO', so, 'z', z, 'b', b, 'mult', sorted(Counter(cc.values()).items()), 'wd', sorted(wd.items()))

print('== (b) certificate via (1-x)^w (1+x)^(52-w)')
def poly_mul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] += x * y
    return r
def kraw_gf(n, w):
    p = [1]
    for _ in range(w): p = poly_mul(p, [1, -1])
    for _ in range(n - w): p = poly_mul(p, [1, 1])
    return p
F = {}
for w in [0] + list(range(24, 53, 4)):
    K = kraw_gf(52, w)
    F[w] = 23 * K[1] + 4 * K[2] + K[3]
print(F)
print('28600-72*511 =', 28600 - 72 * 511)
# Sanity: K_j(0) = C(52,j), K_1(w)=52-2w
assert kraw_gf(52, 0)[3] == comb(52, 3)
assert all(kraw_gf(52, w)[1] == 52 - 2 * w for w in range(53))
# also check the bound actually uses w in {24..52}; what if weights 20 allowed (control)?
K20 = kraw_gf(52, 20); print('F(20)=', 23 * K20[1] + 4 * K20[2] + K20[3])

print('== (c) relative links')
for md in ['PROOF.md', 'README.md', 'V3-CHANGES.md', 'evidence/INDEX.md', 'references/SOURCES.md']:
    t = (P / md).read_text(encoding='utf-8')
    links = re.findall(r'\]\(([^)]+)\)', t)
    bad = []; abs_ = []
    for L in links:
        if L.startswith('http'): continue
        if re.match(r'^[A-Za-z]:', L) or L.startswith('/'):
            abs_.append(L); continue
        tgt = (P / md).parent / L.split('#')[0]
        if not tgt.exists(): bad.append(L)
    print(md, 'links', len(links), 'missing', bad, 'absolute', abs_)
# code-span file names in PROOF.md that are not links: do they exist at root?
t = (P / 'PROOF.md').read_text(encoding='utf-8')
names = sorted(set(re.findall(r'`([A-Za-z0-9_\-]+\.(?:py|json|txt|c|jsonl))`', t)))
print('PROOF backticked files missing at root:', [n for n in names if not (P / n).exists()])

print('== (d) headers')
def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for i in range(3):
    a = P / f'runs/v3-bounded-check/direct/D{i}.h'
    b = Path(sys.argv[2]) / f'D{i}.h'
    print(i, 'bundled==mine', h(a) == h(b))
