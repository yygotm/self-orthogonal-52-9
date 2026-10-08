# positive controls for lp_exact.phase1 (must be feasible)
import importlib.util, sys
spec = importlib.util.spec_from_file_location('lpx', 'lp_exact.py')
src = open('lp_exact.py').read().split('for so in (True, False):')[0]
ns = {}; exec(src, ns)
for ws, label in [(list(range(20, 53, 4)), 'doubly-even [52,9,>=20] (LOWER exists)'),
                  (list(range(22, 53, 2)), 'SO [52,9,>=22] all even weights')]:
    val, sol = ns['phase1'](ns['build'](True, True, ws))
    print(label, 'phase-1 optimum =', val, 'feasible' if val == 0 else 'INFEASIBLE')
# check the LOWER enumerator satisfies all rows exactly
K = ns['K']; A = {20: 51, 24: 204, 28: 204, 32: 51, 52: 1}
ok = all((K(j,0) + sum(a*K(j,w) for w,a in A.items())) >= 512*A.get(j,0) for j in range(53))
print('LOWER enumerator satisfies B_j>=A_j:', ok)
