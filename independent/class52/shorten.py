"""Shortening step (Claude, 2026/10/8): from all doubly-even [N,K,>=24] codes S (rows as ints, zero columns allowed,
length N) to all doubly-even [N+1,K+1,>=24] codes T with a nonzero last coordinate, up to equivalence.

T = <(S|0),(v|1)> with v in S^perp, wt(v) = 3 mod 4, wt(v+s) >= 23 for all s in S (then T is doubly-even with d >= 24,
see ../ext52x/gen_s.py). For each S the 2^(N-2K) coset representatives v of S in S^perp are enumerated exhaustively by
../ext52x/extS.c (gcc, OpenMP), and the resulting T are reduced by classify.canon (nauty). Every doubly-even
[N+1,K+1,>=24] code of dimension K+1 with some nonzero coordinate arises this way (move that coordinate last and shorten:
the shortened code has dimension K, is doubly-even, d >= 24, and is equivalent to one of the input S), so the output is
the complete classification of doubly-even [N+1,K+1,>=24] codes (zero columns allowed), given a complete input.
usage: python shorten.py N K out.json in1.json [in2.json ...]      log: shorten-<N+1>-<K+1>.log
"""
import sys, os, json, subprocess, time
from functools import reduce
from multiprocessing import Pool
from classify import canon, span, pc

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, '..', 'ext52x')
N, K = int(sys.argv[1]), int(sys.argv[2])
OUT = sys.argv[3]
DMIN = int(os.environ.get('DMIN', '24'))  # minimum distance (multiple of 4); 24 for the [52,8,24] problem, smaller for tests
LOG = open(os.path.join(HERE, f'shorten-{N+1}-{K+1}-d{DMIN}.log'), 'a')


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True); print(s, file=LOG, flush=True)


def rref(vs):
    piv, out = [], []
    for v in vs:
        for p, b in zip(piv, out):
            if v >> p & 1: v ^= b
        if v:
            p = v.bit_length() - 1
            out = [b ^ v if b >> p & 1 else b for b in out]
            piv.append(p); out.append(v)
    return piv, out


def header(rows, path):
    """Basis of S^perp cap {x_P = 0} (P an information set of S), the nonzero words of S, and S itself."""
    assert len(rows) == K and all(0 <= r < 1 << N for r in rows)
    P, _ = rref(rows); assert len(P) == K
    piv, R = rref(rows + [1 << p for p in P]); assert len(R) == 2 * K
    free = [j for j in range(N) if j not in piv]
    basis = []
    for f in free:
        x = 1 << f
        for p, r in zip(piv, R):
            if r >> f & 1: x |= 1 << p
        basis.append(x)
    assert len(basis) == N - 2 * K
    for x in basis:
        assert all(pc(x & r) % 2 == 0 for r in rows) and all(not x >> p & 1 for p in P)
    S = span(rows)
    assert all(pc(w) % 4 == 0 for w in S) and len(set(S)) == 1 << K and min(pc(w) for w in S[1:]) >= DMIN
    Snz = sorted(S[1:], key=pc)
    with open(path, 'w') as f:
        f.write('#define NB %d\n#define NS %d\n' % (len(basis), len(Snz)))
        f.write('static const unsigned long long B[NB] = {%s};\n' % ','.join('0x%xULL' % x for x in basis))
        f.write('static const unsigned long long S[NS] = {%s};\n' % ','.join('0x%xULL' % x for x in Snz))
        f.write('static const unsigned long long G[%d] = {%s};\n' % (K, ','.join('0x%xULL' % x for x in rows)))
    return len(basis)


def _canon(rows):
    return canon(rows, N + 1), rows


def wd(rows):
    out = {}
    for x in span(rows): out[pc(x)] = out.get(pc(x), 0) + 1
    return dict(sorted(out.items()))


def main():
    codes = []
    for p in sys.argv[4:]: codes += json.load(open(p))
    log(f'== {time.strftime("%H:%M:%S")} shorten N={N} K={K} DMIN={DMIN}: {len(codes)} input codes S from {sys.argv[4:]}')
    for rows in codes: assert all(pc(w) % 4 == 0 and (w == 0 or pc(w) >= DMIN) for w in span(rows)) and len(rows) == K
    seen = {}
    pool = Pool(int(os.environ.get('NPROC', '16')))
    for i, rows in enumerate(codes):
        t0 = time.time()
        hdr = os.path.join(HERE, f'basis-S{N}-{i}.h'); exe = os.path.join(HERE, f'extS-{N}-{i}')
        nb = header(rows, hdr)
        subprocess.run(['gcc', '-O3', '-march=native', '-fopenmp', f'-DBASIS="{os.path.basename(hdr)}"', f'-DDMIN={DMIN}',
                        '-I', HERE, os.path.join(EXT, 'extS.c'), '-o', exe], check=True)
        res = subprocess.run([exe], capture_output=True, text=True, check=True)
        vs = [int(l.split()[1], 16) for l in res.stdout.splitlines() if l.startswith('v ')]
        tail = [l for l in res.stdout.splitlines() if l.startswith('accepted')]
        assert tail and int(tail[0].split()[1]) == len(vs), tail
        Ts = [list(rows) + [v | 1 << N] for v in vs]
        new = 0
        for c, T in pool.imap_unordered(_canon, Ts, chunksize=64):
            if c not in seen: seen[c] = T; new += 1
        zc = N - pc(reduce(lambda a, b: a | b, rows))
        log(f'S {i}/{len(codes)} (zero cols {zc}, 2^{nb} reps): accepted {len(vs)}, new classes {new}, total {len(seen)}, {time.time()-t0:.0f}s')
        os.remove(exe); os.remove(hdr)
    out = list(seen.values())
    json.dump(out, open(OUT, 'w'))
    log(f'== {time.strftime("%H:%M:%S")} doubly-even [{N+1},{K+1},>={DMIN}] (zero columns allowed): {len(out)} classes -> {OUT}')
    for T in out:
        log(f'   zero cols {N + 1 - pc(reduce(lambda a, b: a | b, T))}, weights {wd(T)}')
    if N + 1 == 52 and DMIN == 24:
        mine = {canon(T, 52): j for j, T in enumerate(out)}
        for t in range(3):
            p = os.path.join(EXT, f'D-gpt{t}.txt')
            rows = [int(l.strip()[::-1], 2) for l in open(p) if l.strip()]
            c = canon(rows, 52)
            log(f'GPT D{t}: weights {wd(rows)} -> {"class %d" % mine[c] if c in mine else "NOT IN MY LIST"}')


if __name__ == '__main__':
    main()
