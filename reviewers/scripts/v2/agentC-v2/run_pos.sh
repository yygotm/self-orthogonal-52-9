set -e
cd /w
gcc -O2 -fopenmp -DHDR="\"hA0.h\"" scanA.c -o sA0
s=$(date +%s); timeout 570 ./sA0 20 > scanA0-20.out; e=$(date +%s); echo "D0 T=20 $((e-s))s rc=$?" >> pos-times.txt
