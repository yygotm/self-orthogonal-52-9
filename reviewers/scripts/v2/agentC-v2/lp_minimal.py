# greedy minimal set of Delsarte constraints B_j>=0 that already make doubly-even [52,9,>=24] infeasible (exact)
src = open('lp_exact.py').read().split('W = list(range(24, 53, 4))')[0]
ns = {}; exec(src, ns); K = ns['K']; phase1 = ns['phase1']
W = list(range(24, 53, 4))
def rows_for(J):
    rows = [([1]*len(W), '==', 511)]
    for j in J: rows.append(([K(j, w) for w in W], '>=', -K(j, 0)))
    return rows
J = list(range(1, 53))
assert phase1(rows_for(J))[0] > 0
for j in list(J):
    T = [x for x in J if x != j]
    if phase1(rows_for(T))[0] > 0: J = T
print('minimal infeasible set of j (B_j>=0 only, A_w>=0 on w in 24..52 step 4):', J)
print('phase-1 optimum:', phase1(rows_for(J))[0])
