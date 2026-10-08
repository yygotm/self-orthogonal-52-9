"""Agent B v2: small checks of numbers newly stated in PROOF v2."""
import sys
from collections import Counter
from math import ceil
d = sys.argv[1]
def read(fn):
    return [sum(1 << j for j, ch in enumerate(l.strip()) if ch == '1') for l in open(fn) if l.strip() and l.strip()[0] in '01']
def span(rows):
    w = [0]
    for r in rows: w += [x ^ r for x in w]
    return w
pc = lambda x: x.bit_count()
D0 = read(d + '/D-representative-0.txt'); W0 = set(span(D0))
def perm(x, f):
    return sum(1 << f(j) for j in range(52) if x >> j & 1)
sh = lambda j: j if j == 51 else (j + 1) % 51
fr = lambda j: j if j == 51 else (2 * j) % 51
print('D0 invariant under j->j+1 mod 51:', all(perm(x, sh) in W0 for x in D0))
print('D0 invariant under j->2j mod 51:', all(perm(x, fr) in W0 for x in D0))
print('order of 2 mod 51:', next(k for k in range(1, 60) if pow(2, k, 51) == 1))
for name, h in [('h1', 2251816993685511), ('h2', 2251834173685767)]:
    print(name, 'support', [j for j in range(52) if h >> j & 1])
for i in range(3):
    R = read(d + f'/residual16-{i}.txt'); W = span(R)
    wd = sorted(Counter(pc(x) for x in W).items())
    print(f'residual16-{i}', len(R), 'wd', wd, ' #(j>=12)=', sum(1 for x in W if pc(x) >= 12))
g = lambda k, dd: sum(ceil(dd / 2**i) for i in range(k))
print('Griesmer g(8,28)', g(8, 28), 'g(8,24)', g(8, 24), 'g(9,24)', g(9, 24), 'g(7,8)', g(7, 8), 'g(7,6)', g(7, 6), 'g(5,24)', g(5, 24))
print('Hamming', 2**7*11, 2**10, 2**7*10, 2**9, 2**6*10, 2**9, 2**6*9, 2**8)
# moments with weights 24,28,32 only: solve A28 as function of n,b
for n in (51, 50):
    for b in (0, 1, 2):
        s0, s1, s2 = 255, 128*n, 64*(n*n + n + 2*b)
        A28 = -(s2 - 56*s1 + 768*s0) / 16
        print('n', n, 'b', b, 'A28', A28)
print('weight-40 Parseval', 1600 + 4*4992 - 32*768 + 64*127, 128*40, ' moments', 12*64, 12*64 + 12*11*32)
