set -e
cd /w/agentC-v3/replay
export OMP_NUM_THREADS=16
E=/w/so52-v3/evidence
for i in 0 1 2; do
  gcc -O3 -march=native -fopenmp -I. -DHDR="\"h$i.h\"" $E/agentC/cosets.c -o cos$i
  gcc -O3 -march=native -fopenmp -I. -DBASIS="\"basis-gpt$i.h\"" $E/ext52x/ext52x.c -o ext$i
  gcc -O3 -march=native -fopenmp -I. -DHDR="\"hA$i.h\"" $E/agentA-v2/scanA.c -o scan$i
done
ls -la cos* ext* scan*
s=$(date +%s); echo "ext0 20 start $(date)"; ./ext0 20 3 > ext0-20.out 2>/dev/null; echo "ext0 20 $(( $(date +%s)-s ))s"
s=$(date +%s); ./cos1 22 > cos1-22.out; echo "cos1 22 $(( $(date +%s)-s ))s"
s=$(date +%s); ./scan2 22 > scan2-22.out; echo "scan2 22 $(( $(date +%s)-s ))s"
echo DONE $(date)
