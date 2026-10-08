/* Portable wrapper implementation of the direct quotient scan in PROOF 7.1.
 * Same weight test as review/agentA-v2's scanA.c, with explicit range bounds,
 * parameterized small codes for tests, and machine-readable coverage counts.
 * Original, independently run implementations are preserved under evidence/.
 * Header defines CODE_N, CODE_K, QUOTIENT_DIM, DR[], NB_[].
 * Usage: scan THRESHOLD START COUNT. No implicit full scan.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <errno.h>
#include HDR

static int number(const char *s, unsigned long long *v) {
    char *end;
    if (!s[0] || s[0] == '-') return 0;
    errno = 0;
    *v = strtoull(s, &end, 10);
    return !errno && !*end;
}

int main(int argc, char **argv) {
    unsigned long long threshold, start, count;
    if (argc != 4 || !number(argv[1], &threshold) ||
        !number(argv[2], &start) || !number(argv[3], &count)) {
        fprintf(stderr, "Usage: scan THRESHOLD START COUNT\n"); return 2;
    }
    const unsigned long long total = 1ULL << QUOTIENT_DIM;
    if (threshold > CODE_N || start >= total || !count || count > total-start) {
        fprintf(stderr, "Invalid threshold or range\n"); return 2;
    }
    static unsigned long long words[1U << CODE_K];
    for (unsigned m=1; m<(1U<<CODE_K); ++m) {
        unsigned i=__builtin_ctz(m);
        words[m]=words[m^(1U<<i)]^DR[i];
        if (!words[m] || (__builtin_popcountll(words[m])&3)) {
            fprintf(stderr, "Input is not independent and doubly even\n"); return 3;
        }
    }
    for (int i=0; i<QUOTIENT_DIM; ++i)
        for (int j=0; j<CODE_K; ++j)
            if (__builtin_popcountll(NB_[i]&DR[j])&1) {
                fprintf(stderr, "Quotient basis is not orthogonal\n"); return 3;
            }
    const unsigned long long block=1ULL<<16;
    long long blocks=(long long)((count+block-1)/block);
    unsigned long long seen0=0,seen2=0,hit0=0,hit2=0,visited=0;
    #pragma omp parallel for schedule(dynamic) reduction(+:seen0,seen2,hit0,hit2,visited)
    for (long long b=0; b<blocks; ++b) {
        unsigned long long first=start+(unsigned long long)b*block;
        unsigned long long end=first+block;
        if (end>start+count) end=start+count;
        unsigned long long gray=first^(first>>1), x=0;
        for (int i=0; i<QUOTIENT_DIM; ++i) if ((gray>>i)&1) x^=NB_[i];
        for (unsigned long long s=first; s<end; ++s) {
            if (s!=first) x^=NB_[__builtin_ctzll(s)];
            ++visited;
            int w=__builtin_popcountll(x);
            if (w&1) continue;
            if (w&2) ++seen2; else ++seen0;
            if ((unsigned)w<threshold) continue;
            int ok=1;
            for (unsigned m=1; m<(1U<<CODE_K); ++m)
                if ((unsigned)__builtin_popcountll(x^words[m])<threshold) {ok=0; break;}
            if (ok) {if (w&2) ++hit2; else ++hit0;}
        }
    }
    printf("{\"n\":%d,\"k\":%d,\"quotient_dimension\":%d,"
           "\"threshold\":%llu,\"start\":%llu,\"count\":%llu,"
           "\"total\":%llu,\"visited\":%llu,\"seen0\":%llu,"
           "\"seen2\":%llu,\"hit0\":%llu,\"hit2\":%llu}\n",
           CODE_N,CODE_K,QUOTIENT_DIM,threshold,start,count,total,visited,
           seen0,seen2,hit0,hit2);
    return visited==count ? 0 : 4;
}
