"""Agent B (v2 review): independent check of the coset-scan headers used for PROOF v2 §7.1.

For each D in D-representative-{0,1,2}.txt (8 lines of 0/1, character j = coordinate j):
  * D has rank 8, is doubly-even (hence D in D^perp), dim D^perp = 52 - 8 = 44.
  * cosets.c header h{i}.h (Agent C, gen_hdr.py): the 36 vectors B are in D^perp and rank(D + B) = 44,
    so the 2^36 combinations of B meet every coset v + D (v in D^perp) exactly once.
    W[255] is exactly the set of nonzero words of D.
  * ext52x.c header basis-gpt{i}.h (gen.py): the same, plus every B vector vanishes on the information
    set P, which is checked to be an information set (D restricted to P has rank 8).
  * coset weights mod 4: for v in D^perp, wt(v+d) = wt(v) mod 4 for all d in D (checked on random v).
Own linear algebra (row echelon on Python ints), not the code of gen_hdr.py / gen.py.
usage: python verify_headers.py DIR_WITH_D_FILES DIR_WITH_HEADERS
"""
import sys, re, random

ddir, hdir = sys.argv[1], sys.argv[2]
N = 52
pc = lambda x: x.bit_count()


def read_D(fn):
    return [sum(1 << j for j, ch in enumerate(l.strip()) if ch == '1')
            for l in open(fn) if l.strip() and l.strip()[0] in '01']


def rank(vs):
    basis = []  # list of (lowbit, vec), kept so that each lowbit is unique
    for v in vs:
        for lb, b in basis:
            if v >> lb & 1:
                v ^= b
        if v:
            lb = (v & -v).bit_length() - 1
            basis = [(l, b ^ v if b >> lb & 1 else b) for l, b in basis]
            basis.append((lb, v))
    return len(basis)


def arr(text, name):
    m = re.search(r'%s\[[^\]]*\]\s*=\s*\{([^}]*)\}' % name, text)
    return [int(x.strip().rstrip('ULL').rstrip('ull'), 16) for x in m.group(1).split(',') if x.strip()]


def span(rows):
    w = [0]
    for r in rows:
        w += [x ^ r for x in w]
    return w


ok_all = True
rng = random.Random(2026)
for i in range(3):
    D = read_D(f'{ddir}/D-representative-{i}.txt')
    assert len(D) == 8 and rank(D) == 8
    words = span(D)
    assert len(set(words)) == 256
    de = all(pc(w) % 4 == 0 for w in words)
    selforth = all(pc(a & b) % 2 == 0 for a in D for b in D)
    res = {'rank8': True, 'doubly_even': de, 'self_orth': selforth}
    for hname, wname in ((f'h{i}.h', 'W'), (f'basis-gpt{i}.h', 'D')):
        t = open(f'{hdir}/{hname}').read()
        B = arr(t, 'B')
        Wl = arr(t, wname)
        r = {}
        r['nB'] = len(B)
        r['B_in_Dperp'] = all(pc(b & d) % 2 == 0 for b in B for d in D)
        r['rank_D_plus_B'] = rank(D + B)
        r['W_is_D_minus_0'] = (sorted(Wl) == sorted(words[1:]))
        if hname.startswith('basis'):
            G = arr(t, 'G')
            r['G_equals_D_rows_span'] = (set(span(G)) == set(words))
            used = 0
            for b in B:
                used |= b
            # information set P: coordinates where every B vector vanishes and D|P has rank 8
            P = [j for j in range(N) if not used >> j & 1]
            r['P'] = P
            maskP = sum(1 << j for j in P)
            r['D_on_P_rank'] = rank([d & maskP for d in D])
        res[hname] = r
        good = (r['nB'] == 36 and r['B_in_Dperp'] and r['rank_D_plus_B'] == 44 and r['W_is_D_minus_0'])
        if hname.startswith('basis'):
            good = good and r['G_equals_D_rows_span'] and len(r['P']) == 8 and r['D_on_P_rank'] == 8
        ok_all &= good
    # mod-4 invariance of coset weights on random v in D^perp (v = random combination of B of h{i}.h)
    B = arr(open(f'{hdir}/h{i}.h').read(), 'B')
    inv = True
    for _ in range(2000):
        v = 0
        for b in B:
            if rng.random() < 0.5:
                v ^= b
        inv &= all((pc(v ^ w) - pc(v)) % 4 == 0 for w in words)
    res['coset_wt_mod4_invariant(2000 random v)'] = inv
    ok_all &= de and selforth and inv
    print(f'D{i}', res)
print('ALL OK' if ok_all else 'PROBLEM')
