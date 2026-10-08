"""Agent B: enumerate all (not only even) [16,7,>=6] codes in the reduced
systematic form of classify16_7_6.py and report whether any has an odd-weight word."""
import time
R, K, D = 9, 7, 6
cands = sorted(r for r in range(1 << R) if r.bit_count() >= D - 1)
n_sol = 0; n_odd = 0; wds = {}
def rec(rows, sums, colpref):
    global n_sol, n_odd
    if len(rows) == K:
        n_sol += 1
        wd = {}
        for s, c in sums:
            w = s.bit_count() + c
            wd[w] = wd.get(w, 0) + 1
        key = tuple(sorted(wd.items()))
        wds[key] = wds.get(key, 0) + 1
        if any(w % 2 for w in wd): n_odd += 1
        return
    start = rows[-1] + 1 if rows else 0
    for r in cands:
        if r < start: continue
        newpref = [(colpref[j] << 1) | ((r >> (R - 1 - j)) & 1) for j in range(R)]
        if any(newpref[j] > newpref[j + 1] for j in range(R - 1)): continue
        newsums = []
        for s, c in sums:
            v = s ^ r
            if v.bit_count() + c + 1 < D: break
            newsums.append((v, c + 1))
        else:
            rec(rows + [r], sums + newsums, newpref)
t = time.time(); rec([], [(0, 0)], [0] * R)
print("all-mode solutions", n_sol, "with odd words", n_odd, "time %.1f" % (time.time() - t))
for k, v in wds.items(): print(v, k)
