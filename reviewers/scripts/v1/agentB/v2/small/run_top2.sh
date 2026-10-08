set -e
cd /w/small
for f in s28a s30a s30z; do
  gcc -O3 -fopenmp -DHDR="\"h_$f.h\"" cosets_top2.c -o ct_$f
  gcc -O3 -fopenmp -DBASIS="\"b_$f.h\"" ext52x_top2.c -o xt_$f
  for T in 2 4 6 8 10; do ./ct_$f $T >> ct_$f.out; ./xt_$f $T 0 >> xt_$f.out 2>/dev/null; done
done
echo DONE3 > top2.done
