/* Exhaustive search: SO [52,9,>=d] codes <D,v>, D = cyclic [51,8,24] + zero column (Claude, 2026/10/8).
   v runs over the 2^36 coset representatives of D in D^perp (basis.h from gen.py). <D,v> is SO iff wt(v) even.
   Accept v iff wt(v+c) >= d for all c in D. Prints every accepted v (up to a cap) and the total count.
   usage: ext52x d [cap]      build: gcc -O3 -march=native -fopenmp ext52x.c -o ext52x */
#include <stdio.h>
#include <stdlib.h>
#ifndef BASIS
#define BASIS "basis.h"
#endif
#include BASIS
#define TOP 2
int main(int argc, char **argv) {
    int d = atoi(argv[1]); long cap = argc > 2 ? atol(argv[2]) : 100;
    int low = NB - TOP; long long total = 0, done = 0;
    #pragma omp parallel for schedule(dynamic) reduction(+:total)
    for (long t = 0; t < (1L << TOP); t++) {
        unsigned long long v = 0;
        for (int i = 0; i < TOP; i++) if (t >> i & 1) v ^= B[low + i];
        for (unsigned long long s = 0; s < (1ULL << low); s++) {
            if (s) v ^= B[__builtin_ctzll(s)];
            int w = __builtin_popcountll(v);
            if ((w & 1) || w < d) continue;
            int ok = 1;
            for (int j = 0; j < 255; j++) if (__builtin_popcountll(v ^ D[j]) < d) { ok = 0; break; }
            if (ok) {
                #pragma omp critical
                { static long shown = 0; if (shown++ < cap) printf("v %llx wt %d\n", v, w); }
                total++;
            }
        }
        #pragma omp critical
        { done++; if (done % 64 == 0) { fprintf(stderr, "chunks %lld/%d\n", done, 1 << TOP); fflush(stderr); } }
    }
    printf("d=%d accepted %lld of 2^%d coset representatives\n", d, total, NB);
    return 0;
}
