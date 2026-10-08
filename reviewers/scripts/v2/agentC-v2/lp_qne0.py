# Delsarte LP for q!=0: C = D + coset, D fixed to D0/D1/D2 enumerator, coset weights 2 mod 4 >= 22 (sum 256).
# exact phase-1 via lp_exact.phase1
src = open('lp_exact.py').read().split('W = list(range(24, 53, 4))')[0]
ns = {}; exec(src, ns); K = ns['K']; phase1 = ns['phase1']
Ds = {'D0': {24: 204, 32: 51}, 'D1': {24: 172, 28: 32, 32: 51}, 'D2': {24: 174, 28: 30, 32: 49, 36: 2}}
V = list(range(22, 52, 4))
for name, D in Ds.items():
    rows = [([1]*len(V), '==', 256)]
    for j in range(1, 53):
        const = K(j, 0) + sum(a*K(j, w) for w, a in D.items()) - 512*D.get(j, 0)
        a = [K(j, w) - (512 if w == j else 0) for w in V]
        rows.append((a, '>=', -const))
    val, sol = phase1(rows)
    print(name, 'phase-1 optimum', val, 'INFEASIBLE' if val > 0 else 'feasible', {V[i]: v for i, v in sol.items()} if val == 0 else '')
# control: threshold 18 for D0 (LOWER-type extension with coset weights 20? those are 0 mod 4) -> use 2 mod 4 >=18
V = list(range(18, 52, 4)); D = Ds['D0']
rows = [([1]*len(V), '==', 256)]
for j in range(1, 53):
    const = K(j, 0) + sum(a*K(j, w) for w, a in D.items()) - 512*D.get(j, 0)
    rows.append(([K(j, w) - (512 if w == j else 0) for w in V], '>=', -const))
val, sol = phase1(rows); print('control D0 coset 2mod4 >=18:', val, 'feasible' if val == 0 else 'INFEASIBLE')
