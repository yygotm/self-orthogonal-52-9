set -e
cd /w/small
for f in s28a s30a s30z; do
  gcc -O3 -fopenmp -DHDR="\"h_$f.h\"" cosets.c -o c_$f
  gcc -O3 -fopenmp -DBASIS="\"b_$f.h\"" ext52x.c -o x_$f
  for T in 2 4 6 8 10; do ./c_$f $T >> c_$f.out; ./x_$f $T 0 >> x_$f.out 2>/dev/null; done
done
cd /w/run
s=$(date +%s); ./c0 20 > cos0-20.out; e=$(date +%s); echo "cosets D0 T=20 $((e-s))s" >> times.txt
s=$(date +%s); ./x0 20 3 > ext0-20.out 2>/dev/null; e=$(date +%s); echo "ext52x D0 d=20 $((e-s))s" >> times.txt
echo DONE2 >> times.txt
