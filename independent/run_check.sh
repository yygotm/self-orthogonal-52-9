#!/bin/sh
# Quick checks of the independent classification (Claude, 2026/10/8). Minutes, not hours.
# usage (from independent/):
#   docker build -t so52-indep class52
#   docker run --rm -v "$PWD:/w" -w /w so52-indep sh run_check.sh
# Writes nothing into the bundle: every run happens in a scratch copy under /tmp.
set -e
export PYTHONDONTWRITEBYTECODE=1   # keep the bundle unchanged
W=$(pwd)
T=$(mktemp -d)
cp -r class52 ext52x "$T"/   # shorten.py finds ../ext52x/extS.c
NPROC=${NPROC:-$(nproc)}; export NPROC

echo '== 1. the bundled data: dimension, doubly-even, d >= 24, pairwise inequivalent, counts, weight distributions'
python check_data.py

echo "== 2. which of these codes are 8-divisible (input to the Kurz Table 1 cross-check, see README)"
python kurz/kurzcheck.py data

echo '== 3. classify.py against brute force on small parameters'
(cd "$T/class52" && python brute_check.py 2>/dev/null)

echo '== 4. shorten.py on a case with a known answer: doubly-even [16,5,8] -> 1 class (RM(1,4)), [17,6,8] -> 0'
(cd "$T/class52" && cp "$W"/data/class-14-4-8-de.json "$W"/data/class-15-4-8-de.json . \
  && DMIN=8 python shorten.py 15 4 t16.json class-15-4-8-de.json class-14-4-8-de.json >/dev/null \
  && DMIN=8 python shorten.py 16 5 t17.json t16.json >/dev/null \
  && python -c "import json; a=len(json.load(open('t16.json'))); b=len(json.load(open('t17.json'))); print('[16,5,8]:', a, ' [17,6,8]:', b); assert (a, b) == (1, 0)")

echo '== 5. S for n = 48, 49 recomputed from scratch and compared with data/'
(cd "$T/class52" && rm -f class-*.json && python classify.py 48 6 24 de 2>/dev/null && python classify.py 49 6 24 de 2>/dev/null \
  && python - "$W"/data <<'EOF'
import json, sys
from classify import canon
for n in (48, 49):
    a = {canon(r, n) for r in json.load(open(f'class-{n}-6-24-de.json'))}
    b = {canon(r, n) for r in json.load(open(f'{sys.argv[1]}/class-{n}-6-24-de.json'))}
    assert a == b, n
    print(f'n={n}: recomputed {len(a)} classes = data')
EOF
)

echo '== 6. ext52x: headers regenerate byte-equal from D-gpt*.txt, and the scanner compiles'
(cd "$T/ext52x" && for t in 0 1 2; do python gen.py D-gpt$t.txt chk$t.h >/dev/null; tr -d '\r' < basis-gpt$t.h | cmp chk$t.h - || exit 1; done \
  && gcc -O3 -fopenmp -DBASIS='"basis-gpt0.h"' ext52x.c -o ext52x && echo 'headers equal, ext52x compiled')

rm -rf "$T"
echo 'run_check: OK'
