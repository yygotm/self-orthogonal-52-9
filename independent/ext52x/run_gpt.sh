set -e
for t in 2 0 1; do
  gcc -O3 -march=native -fopenmp -DBASIS="\"basis-gpt$t.h\"" ext52x.c -o ext52x-gpt$t
  ./ext52x-gpt$t 22 > d22-gpt$t.out 2> d22-gpt$t.err
done
./ext52x-gpt0 20 3 > d20-gpt0.out 2> d20-gpt0.err
