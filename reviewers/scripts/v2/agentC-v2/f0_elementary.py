"""Agent C v2: elementary exclusion of the sec.6 f=0 case without Kurz Table 1.
Claim: no binary [52,8] code D without zero columns whose nonzero weights all lie in {24,32}.
Moments (k=8): A24=188, A32=67, b=sum_p C(m(p),2)=4.
Project from a repeated column p0 of multiplicity mu: H0={u: u.p0=0} is a [52-mu,7] code
(columns = images of the other columns in F2^8/<p0>, all nonzero), weights in {24,32}.
Moments for k=7 give b' (number of equal column pairs of H0):
  mu=3 -> n'=49 -> 2b'=-10 (impossible);  mu=2 -> n'=50 -> b'=1.
mu<=2 everywhere means 4 doubled points p0,q1,q2,q3; in H0 the images of q1,q2,q3 are doubled,
so b'>=3 != 1.  Contradiction.
Also: a numerical control of the projection/moment bookkeeping on the real code D2 (b=1)."""
from fractions import Fraction as Fr
import sys

def moments(k, n, weights):
    """solve A_w (two weights) from sum A = 2^k-1, sum wA = 2^(k-1) n; return A and b from 2nd moment."""
    w1, w2 = weights
    N = 2**k - 1
    A2 = Fr(2**(k-1) * n - w1 * N, w2 - w1); A1 = N - A2
    S2 = w1*w1*A1 + w2*w2*A2
    b = (S2 / 2**(k-2) - n*n - n) / 2
    return A1, A2, b

print('k=8 n=52 {24,32}: A24,A32,b =', moments(8, 52, (24, 32)))
for mu in (2, 3):
    print(f'project from point of multiplicity {mu}: k=7 n={52-mu}: A24,A32,b\' =', moments(7, 52-mu, (24, 32)))

# control on D2: project from its doubled column, compare b' from formula (using actual weights) with direct count
path = sys.argv[1]
rows = [l.strip() for l in open(path) if l.strip()]
k, n = len(rows), len(rows[0])
cols = [sum(int(rows[i][j]) << i for i in range(k)) for j in range(n)]
from collections import Counter
cnt = Counter(c for c in cols if c)
dbl = [c for c, m in cnt.items() if m >= 2]
print('D2: zero cols', cols.count(0), 'repeated columns', {c: m for c, m in cnt.items() if m >= 2})
p0 = dbl[0]
# H0 = {u : u.p0 = 0}; weights of its words
par = lambda x: bin(x).count('1') & 1
H0w = [sum(cnt[c] for c in cnt if c != p0 and par(u & c)) for u in range(1, 256) if not par(u & p0)]
# quotient columns: images of c != p0 in F2^8/<p0>; identify c ~ c^p0
img = Counter()
for c, m in cnt.items():
    if c == p0: continue
    img[min(c, c ^ p0)] += m
nq = sum(img.values())
b_direct = sum(m*(m-1)//2 for m in img.values())
S1 = sum(H0w); S2 = sum(w*w for w in H0w)
b_formula = Fr(S2, 2**5) - nq*nq - nq
print(f'D2 projected: n\'={nq}, sum w = {S1} (expect {2**6*nq}), b\' direct={b_direct}, b\' from 2nd moment={b_formula/2}')
