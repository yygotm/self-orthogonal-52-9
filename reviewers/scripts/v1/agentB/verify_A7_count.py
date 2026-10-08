"""Agent B (step 2): exhaustive count of seventh rows in PROOF.md sec.5 A-type
WITHOUT using bent duality / quadratic-ness of the double-column part.

Setup (author's normal form): K=[47,5,24] with column labels p in F2^5:
 singles p=(x,0), x in F2^4\\0 (15 cols); doubles p=(x,1), x in F2^4 (2 cols each);
 zero label p=0 (5 cols).  v = 1 on singles, (0,1) on each double, 1 on zeros.
A seventh row y gives per label p the numbers s_p = wt(y_p), t_p = wt((y+v)_p);
sigma_p = n_p - 2 s_p, tau_p = n_p - 2 t_p.  wt(y+k_u) = 26 - S^(u)/2 with
S^(u)=sum_p sigma_p (-1)^{u.p}; all 64 words of y+<K,v> must weigh 24 or 32,
i.e. S^(u), T^(u) in {4,-12}.  Parseval forces sigma_0=+-1; take sigma_0=+1
(zero-column bits = weight 2, positions fixed as the author does).
Singles: sigma=+-1 free (2^15) -- we enumerate ALL of them (no bentness assumed,
we just filter).  Doubles: state (a,b) -> (sigma,tau) in {(2,0),(1,0)->...}.
For fixed singles, the double part F(x)=sigma_x + i tau_x is recovered from its
Fourier transform; we enumerate all admissible transforms and invert.
Output: number of y (zero bits fixed), and that number / 32 (mod K)."""
import itertools, time
import numpy as np

t0 = time.time()
X = 16
chi = np.array([[(-1) ** ((u & x).bit_count() % 2) for x in range(X)] for u in range(X)])  # chi[u,x]
allowed_vals = {4, -12}
import sys
sig0 = int(sys.argv[1]) if len(sys.argv) > 1 else 1
tau0 = -sig0
total = 0
n_single_ok = 0
for sv in range(1 << 15):
    sigma_s = np.array([0] + [1 - 2 * ((sv >> (x - 1)) & 1) for x in range(1, 16)])  # x=0 has no single
    A = chi @ sigma_s  # A(u') for u' in F2^4
    # per u', allowed (Bd, Bt): need sig0 + A +- Bd in allowed, tau0 - A +- Bt in allowed (tau_single=-sigma)
    opts = []
    ok = True
    for u in range(X):
        bd = [b for b in range(-32, 33, 2) if (sig0 + A[u] + b) in allowed_vals and (sig0 + A[u] - b) in allowed_vals]
        bt = [b for b in range(-32, 33, 2) if (tau0 - A[u] + b) in allowed_vals and (tau0 - A[u] - b) in allowed_vals]
        if not bd or not bt:
            ok = False; break
        opts.append([complex(a, b) for a in bd for b in bt])
    if not ok:
        continue
    n_single_ok += 1
    sizes = [len(o) for o in opts]
    # enumerate all transforms: product of options (expected 2^16)
    prod = int(np.prod(sizes))
    assert prod <= 1 << 20, sizes
    grids = np.array(list(itertools.product(*opts)))  # (prod,16) complex
    F = grids @ chi / 16.0  # F[x] = (1/16) sum_u Fhat(u) chi(u,x)  (chi symmetric)
    good = np.all((np.abs(F.real) < 1e-9) & (np.abs(np.abs(F.imag) - 2) < 1e-9) |
                  (np.abs(F.imag) < 1e-9) & (np.abs(np.abs(F.real) - 2) < 1e-9), axis=1)
    total += int(good.sum())
print({"singles_patterns_passing": n_single_ok, "rows_with_fixed_zero_bits": total,
       "mod_K": total / 32, "author_claim": 5376, "seconds": round(time.time() - t0, 1)})
