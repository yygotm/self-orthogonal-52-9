"""Agent B v3: full scans of scan_direct.c on medium doubly-even codes (k up to 8)
compared with an independent brute force that does not use direct_scan.basis.
Usage: python -I test_medium.py <so52-v3 dir> <work dir>
"""
import json, subprocess, sys, os, importlib.util
from pathlib import Path
from collections import Counter

PKG = Path(sys.argv[1]).resolve(); WORK = Path(sys.argv[2]).resolve(); WORK.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location('ds', PKG / 'direct_scan.py'); ds = importlib.util.module_from_spec(spec); spec.loader.exec_module(ds)

def golay_rows():
    g = [1,0,1,0,1,1,1,0,0,0,1,1]  # x^11+x^10+x^6+x^5+x^4+x^2+1, coeff of x^0..x^11
    rows = []
    for s in range(12):
        v = 0
        for i, c in enumerate(g):
            if c: v |= 1 << (i + s)
        if bin(v).count('1') % 2: v |= 1 << 23
        rows.append(v)
    return rows

def span(rows):
    out = [0]
    for r in rows: out += [w ^ r for w in out]
    return out

def my_dual(rows, n):
    """Independent: brute-force D-perp by Gaussian elimination on the check system."""
    # solve x . r = 0 ; build basis by elimination over columns (different from direct_scan)
    piv = {}
    basis = []
    # nullspace via standard: reduce row matrix, then free columns
    M = [r for r in rows]
    pivcols = []
    rank = 0
    for c in range(n - 1, -1, -1):  # different column order than direct_scan
        idx = next((i for i in range(rank, len(M)) if M[i] >> c & 1), None)
        if idx is None: continue
        M[rank], M[idx] = M[idx], M[rank]
        for i in range(len(M)):
            if i != rank and M[i] >> c & 1: M[i] ^= M[rank]
        pivcols.append(c); rank += 1
    for f in range(n):
        if f in pivcols: continue
        x = 1 << f
        for i, c in enumerate(pivcols):
            if M[i] >> f & 1: x |= 1 << c
        basis.append(x)
    for x in basis:
        assert all(bin(x & r).count('1') % 2 == 0 for r in rows)
    return basis

def brute(rows, n, thresholds):
    dw = span(rows); dual = span(my_dual(rows, n))
    seen = {}
    for v in dual:
        key = min(v ^ d for d in dw)
        if key not in seen:
            seen[key] = min(bin(v ^ d).count('1') for d in dw)
    res = {}
    wt = {k: bin(k).count('1') for k in seen}
    for T in thresholds:
        a = Counter()
        for k, mw in seen.items():
            w = wt[k]
            if w % 2: continue
            cls = str(w % 4); a['seen' + cls] += 1
            if mw >= T: a['hit' + cls] += 1
        res[T] = {x: a[x] for x in ['seen0', 'seen2', 'hit0', 'hit2']}
    return res, len(seen)

def run_c(label, n, rows, T):
    hp = WORK / (label + '.h'); bs = ds.header(hp, n, rows)
    exe = WORK / label
    if not exe.exists():
        subprocess.run(['docker', 'run', '--rm', '--pull=never', '--network=none', '-v', f'{PKG}:/src:ro', '-v', f'{WORK}:/work', '-w', '/work', 'gcc:14',
                        'gcc', '-std=c11', '-O3', '-fopenmp', '-I/work', f'-DHDR="{hp.name}"', '/src/scan_direct.c', '-o', label], check=True)
    p = subprocess.run(['docker', 'run', '--rm', '--pull=never', '--network=none', '-e', 'OMP_NUM_THREADS=4', '-v', f'{WORK}:/work', '-w', '/work', 'gcc:14',
                        './' + label, str(T), '0', str(2 ** len(bs))], check=True, capture_output=True, text=True)
    return json.loads(p.stdout)

G = golay_rows()
assert all(bin(w).count('1') % 4 == 0 for w in span(G))
cases = [('g6', 24, G[:6]), ('g8', 24, G[:8]), ('g8z', 26, G[:8]), ('g4', 24, G[:4])]
ok = True
for label, n, rows in cases:
    Ts = [4, 6, 8, 10]
    ref, ncos = brute(rows, n, Ts)
    for T in Ts:
        r = run_c(label, n, rows, T)
        got = {x: r[x] for x in ['seen0', 'seen2', 'hit0', 'hit2']}
        match = got == ref[T]
        ok &= match
        print(label, 'n', n, 'k', len(rows), 'cosets', ncos, 'T', T, 'C', got, 'brute', ref[T], 'MATCH' if match else 'DIFF', flush=True)
print('ALL MATCH' if ok else 'SOME DIFF')
