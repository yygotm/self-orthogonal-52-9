/* Agent C: exhaustive scan of all 2^36 cosets v+D of a doubly-even [52,8] code D inside D^perp.
   For each coset with wt(v) even (=> <D,v> self-orthogonal), compute min weight of v+D, exiting early
   once it drops below T. Counts cosets with min >= T, >= T+2, >= T+4 separately for wt(v)=0 / 2 mod 4.
   build: gcc -O3 -march=native -fopenmp -DHDR='"h1.h"' cosets.c -o c1 ; run: ./c1 T */
#include <stdio.h>
#include <stdlib.h>
#include HDR
#define TOP 12
int main(int argc, char **argv) {
    int T = atoi(argv[1]);
    int low = NB - TOP;
    long long cnt[2][3] = {{0}};
    long long c00=0,c01=0,c02=0,c20=0,c21=0,c22=0;
    #pragma omp parallel for schedule(dynamic) reduction(+:c00,c01,c02,c20,c21,c22)
    for (long t = 0; t < (1L << TOP); t++) {
        unsigned long long v = 0;
        for (int i = 0; i < TOP; i++) if (t >> i & 1) v ^= B[low + i];
        for (unsigned long long s = 0; s < (1ULL << low); s++) {
            if (s) v ^= B[__builtin_ctzll(s)];
            int w = __builtin_popcountll(v);
            if ((w & 1) || w < T) continue;
            int m = w;
            for (int j = 0; j < 255; j++) {
                int x = __builtin_popcountll(v ^ W[j]);
                if (x < m) { m = x; if (m < T) break; }
            }
            if (m < T) continue;
            if ((w & 3) == 0) { c00++; if (m >= T + 2) c01++; if (m >= T + 4) c02++; }
            else              { c20++; if (m >= T + 2) c21++; if (m >= T + 4) c22++; }
            if (m >= 22) {
                #pragma omp critical
                printf("FOUND v=%llx min=%d\n", v, m);
            }
        }
    }
    printf("T=%d  wt(v)=0 mod 4: >=T %lld, >=T+2 %lld, >=T+4 %lld\n", T, c00, c01, c02);
    printf("T=%d  wt(v)=2 mod 4: >=T %lld, >=T+2 %lld, >=T+4 %lld\n", T, c20, c21, c22);
    return 0;
}
