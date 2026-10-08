"""Agent B v2: make length-parametrized copies of gen_hdr.py (Agent C) and gen.py (ext52x).
Only the hard-coded length 52 and the derived constants 44/36 are replaced; every replacement is asserted.
usage: python make_copies.py DIR_WITH_ORIGINAL_COPIES"""
import sys
src = sys.argv[1]
BS = chr(92)  # backslash


def rep(text, pairs):
    for a, b in pairs:
        assert text.count(a) == 1, a
        text = text.replace(a, b)
    return text


t = open(src + '/gen_hdr.py', newline='').read()
t = rep(t, [("D = read(sys.argv[1]); n = 52", "D = read(sys.argv[1]); n = int(sys.argv[3])"),
            ("assert len(dual) == 44", "assert len(dual) == n - 8"),
            ("assert len(comp) == 36", "assert len(comp) == n - 16"),
            ("f.write('#define NB 36" + BS + "n')", "f.write('#define NB %d" + BS + "n' % (n - 16))"),
            ("B[36] = {%s}", "B[NB] = {%s}")])
open('gen_hdr_n.py', 'w', newline='').write(t)
t = open(src + '/gen.py', newline='').read()
t = rep(t, [("n = N + 1", "import sys" + chr(10) + "n = int(sys.argv[3])")])
open('gen_n.py', 'w', newline='').write(t)
