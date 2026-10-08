set -e
cd /w
for i in 0 1 2; do
  gcc -O3 -march=native -fopenmp -DHDR="\"h$i.h\"" cosets.c -o c$i
  gcc -O3 -march=native -fopenmp -DBASIS="\"basis-gpt$i.h\"" ext52x.c -o x$i
done
for i in 0 1 2; do
  s=$(date +%s); ./c$i 22 > cos$i-22.out; e=$(date +%s); echo "cosets D$i T=22 $((e-s))s" >> times.txt
  s=$(date +%s); ./x$i 22 > ext$i-22.out 2>/dev/null; e=$(date +%s); echo "ext52x D$i d=22 $((e-s))s" >> times.txt
done
echo DONE >> times.txt
