"""Agent B (step 2): exhaustive count of seventh rows in PROOF.md sec.6
(max weight 32, f != 0) WITHOUT semi-bent / quadratic / radical arguments.

Author's normal form: K columns = each p in F2^5 \\ U (U = {p<8}, 3-dim) twice,
plus 4 zero columns; v = (0,1) on each pair, 1 on zeros.  For a seventh row y,
per label p: sigma_p = n_p - 2 wt(y_p), tau_p = n_p - 2 wt((y+v)_p).
Pairs: (sigma,tau) in {(2,0),(0,2),(0,-2),(-2,0)} (bijective with the 2 bits).
All 64 words of y + <K,v> weigh 24/32  <=>  S^(u), T^(u) in {4,-12} for all u.
Parseval gives sigma_0 = 0 (zero bits weight 2; positions fixed).
Since sigma vanishes on U, sum_{z in U^perp} S^(w+z) = 0, so in each U^perp-coset
exactly one of the four values is -12.  We enumerate all 4^8 placements of
the -12's (no other assumption), invert, keep sigma with values in {0,+-2}
vanishing on U, do the same for tau, and pair sigma, tau with complementary
supports.  Expected (author / Agent A): 344,064 raw, 10,752 mod K."""
import itertools, time
import numpy as np
from collections import Counter

t0 = time.time()
P = 32
chi = np.array([[(-1) ** ((u & p).bit_count() % 2) for p in range(P)] for u in range(P)])
outside = [p for p in range(P) if p >= 8]
valid = []
for pos in itertools.product(range(4), repeat=8):
    Fh = np.full(P, 4)
    for w in range(8):
        z = [0, 8, 16, 24][pos[w]]
        Fh[w | z] = -12
    s = chi @ Fh  # = 32 * sigma
    if np.any(s % 32):
        continue
    s //= 32
    if np.any(s[:8] != 0):
        continue
    if not np.all(np.isin(s[8:], (-2, 0, 2))):
        continue
    valid.append(tuple(int(v) for v in s[8:]))
print({"valid_sigma_vectors": len(valid), "t": round(time.time() - t0, 1)}, flush=True)
bysupp = Counter()
for v in valid:
    bysupp[sum((x != 0) << i for i, x in enumerate(v))] += 1
full = (1 << 24) - 1
raw = sum(c * bysupp.get(full ^ m, 0) for m, c in bysupp.items())
print({"raw_pairs": raw, "mod_K": raw / 32, "author_raw": 344064, "author_mod_K": 10752,
       "t": round(time.time() - t0, 1)})
