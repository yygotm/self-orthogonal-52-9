"""Agent B v2: compare cosets.c / ext52x.c outputs on the small analogues with the brute force (small_test.py).
usage: python compare_small.py s28a s30a s30z   (run in the folder holding c_*.out, x_*.out, *.json)"""
import sys, json, re
allok = True
for f in sys.argv[1:]:
    ref = json.load(open(f + '.json'))
    c = {}
    for line in open('c_' + f + '.out'):
        mm = re.match(r'T=(\d+)\s+wt\(v\)=(\d) mod 4: >=T (\d+), >=T\+2 (\d+), >=T\+4 (\d+)', line)
        if mm:
            T, cls = int(mm.group(1)), int(mm.group(2))
            c[(T, cls)] = [int(mm.group(k)) for k in (3, 4, 5)]
    x = {}
    for line in open('x_' + f + '.out'):
        mm = re.match(r'd=(\d+) accepted (\d+) of', line)
        if mm:
            x[int(mm.group(1))] = int(mm.group(2))
    for T, r in ref['T'].items():
        T = int(T)
        ok = (c[(T, 0)] == r['cosets_c_0mod4'] and c[(T, 2)] == r['cosets_c_2mod4'] and x[T] == r['ext52x_accepted'])
        allok &= ok
        print(f, 'n', ref['n'], 'zero_col', ref['zero_col'], 'T', T, 'cosets.c', c[(T, 0)], c[(T, 2)], 'ext52x', x[T],
              'brute', r['cosets_c_0mod4'], r['cosets_c_2mod4'], r['ext52x_accepted'], 'OK' if ok else 'MISMATCH')
print('ALL MATCH' if allok else 'SOME MISMATCH')
