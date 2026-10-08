/* Exhaustive search: doubly-even [N+1,K+1,>=24] codes T = <(S|0),(v|1)> for a fixed doubly-even [N,K,>=24] code S
   (Claude, 2026/10/8). v runs over the 2^(N-2K) coset representatives of S in S^perp (header from gen_s.py).
   Accept v iff wt(v) = 3 mod 4 and wt(v+s) >= 23 for all s in S (then T is doubly-even with d >= 24, see gen_s.py).
   Prints every accepted v (hex, coordinates 0..N-1) and the total count.
   usage: extS      build: gcc -O3 -march=native -fopenmp -DBASIS='"basis-S.h"' extS.c -o extS */
#include <stdio.h>
#include <stdlib.h>
#ifndef BASIS
#define BASIS "basis-S.h"
#endif
#ifndef DMIN
#define DMIN 24   /* minimum distance of S and T (a multiple of 4); accept wt(v) = 3 mod 4, wt(v+s) >= DMIN-1 */
#endif
#include BASIS
#define TOP (NB < 12 ? 2 : 10)
int main(int argc, char **argv) {
    int low = NB - TOP; long long total = 0, done = 0;
    #pragma omp parallel for schedule(dynamic) reduction(+:total)
    for (long t = 0; t < (1L << TOP); t++) {
        unsigned long long v = 0;
        for (int i = 0; i < TOP; i++) if (t >> i & 1) v ^= B[low + i];
        for (unsigned long long s = 0; s < (1ULL << low); s++) {
            if (s) v ^= B[__builtin_ctzll(s)];
            int w = __builtin_popcountll(v);
            if ((w & 3) != 3 || w < DMIN - 1) continue;
            int ok = 1;
            for (int j = 0; j < NS; j++) if (__builtin_popcountll(v ^ S[j]) < DMIN - 1) { ok = 0; break; }
            if (ok) {
                #pragma omp critical
                printf("v %llx\n", v);
                total++;
            }
        }
        #pragma omp critical
        { done++; if (done % 64 == 0) { fprintf(stderr, "chunks %lld/%d\n", done, 1 << TOP); fflush(stderr); } }
    }
    printf("accepted %lld of 2^%d coset representatives\n", total, NB);
    return 0;
}
