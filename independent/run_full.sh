#!/bin/sh
# Full recomputation of the independent classification (Claude, 2026/10/8). Hours; see README for times.
# usage (from independent/):
#   docker build -t so52-indep class52
#   docker run --rm -v "$PWD:/w" -w /w so52-indep sh run_full.sh [OUT]
# Results go to OUT (default /w/full-run); the bundled data/ is only read, for the final comparison.
set -e
export PYTHONDONTWRITEBYTECODE=1   # keep the bundle unchanged
W=$(pwd)
OUT=${1:-$W/full-run}
mkdir -p "$OUT"
cp -r class52 ext52x "$OUT"/          # shorten.py finds ../ext52x/extS.c
NPROC=${NPROC:-$(nproc)}; export NPROC
cd "$OUT/class52"
rm -f class-*.json T51.json D52.json

echo "== $(date +%T) 1. S: all doubly-even [n,6,>=24] codes of full support, n = 48, 49, 50"
for n in 48 49 50; do python classify.py $n 6 24 de 2> log$n.txt; done

echo "== $(date +%T) 2. T51: shorten S to doubly-even [51,7,>=24] (about 2.5 h with 16 threads)"
python shorten.py 50 6 T51.json class-50-6-24-de.json class-49-6-24-de.json class-48-6-24-de.json

echo "== $(date +%T) 3. D52: shorten T51 to doubly-even [52,8,>=24] (about 45 min)"
python shorten.py 51 7 D52.json T51.json

echo "== $(date +%T) 4. compare with the bundled data"
python - "$W"/data <<'EOF'
import json, sys
from classify import canon
for name, n in [('class-48-6-24-de.json', 48), ('class-49-6-24-de.json', 49), ('class-50-6-24-de.json', 50),
                ('T51.json', 51), ('D52.json', 52)]:
    a = {canon(r, n) for r in json.load(open(name))}
    b = {canon(r, n) for r in json.load(open(f'{sys.argv[1]}/{name}'))}
    assert a == b, name
    print(f'{name}: recomputed {len(a)} classes = data')
EOF

echo "== $(date +%T) 5. ext52x: no [52,9,>=22] extension of D0, D1, D2; the d=20 control finds words"
cd "$OUT/ext52x"
for t in 0 1 2; do
  gcc -O3 -march=native -fopenmp -DBASIS="\"basis-gpt$t.h\"" ext52x.c -o ext52x-gpt$t
  ./ext52x-gpt$t 22 > d22-gpt$t.out 2> d22-gpt$t.err
  grep -q 'accepted 0 of 2^36' d22-gpt$t.out
done
./ext52x-gpt0 20 3 > d20-gpt0.out 2> d20-gpt0.err
test -s d20-gpt0.out
echo "== $(date +%T) run_full: OK"
