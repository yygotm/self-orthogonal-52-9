set -e
cd /w
for i in 0 1 2; do gcc -O2 -fopenmp -DHDR="\"hA$i.h\"" scanA.c -o sA$i; done
for i in 1 2 0; do s=$(date +%s); ./sA$i 22 > scanA$i-22.out; e=$(date +%s); echo "D$i T=22 $((e-s))s" >> scanA-times.txt; done
s=$(date +%s); ./sA0 20 > scanA0-20.out; e=$(date +%s); echo "D0 T=20 $((e-s))s" >> scanA-times.txt
echo DONE >> scanA-times.txt
