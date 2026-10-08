/* Enumerate lifts for classify.py (Claude, 2026/10/8).
   stdin: k1 n0 m lo mode  then k1 base rows (hex, length n0 <= 63).  mode: 0 any, 1 even, 2 doubly-even.
   Finds all multisets of m points p in F_2^k1 (p = 0 allowed) such that for every nonzero u:
     s_u = #{chosen p : u.p = 1},  wr(u) + s_u >= lo,  wr(u) + m - s_u >= lo,
     even: wr+s_u even;  de: wr+s_u = 0 mod 4 and wr+m-s_u = 0 mod 4.
   Prints each solution as m point indices (nondecreasing). */
#include <stdio.h>
#include <stdlib.h>
int k1, n0, m, lo, mode, P;
int wr[1 << 8], a[1 << 8], b[1 << 8], s[1 << 8], sel[64];
unsigned char dot[1 << 8][1 << 8];
long long nsol = 0;
static void out(void) {
    for (int u = 1; u < P; u++) {
        int t = wr[u] + s[u];
        if (mode == 1 && (t & 1)) return;
        if (mode == 2 && ((t & 3) || ((wr[u] + m - s[u]) & 3))) return;
    }
    nsol++;
    for (int i = 0; i < m; i++) printf("%d%c", sel[i], i + 1 < m ? ' ' : '\n');
}
static void dfs(int depth, int minp) {
    int r = m - depth;
    if (r == 0) { out(); return; }
    for (int p = minp; p < P; p++) {
        int ok = 1;
        for (int u = 1; u < P; u++) {
            int v = s[u] + dot[u][p];
            if (v > b[u] || v + (r - 1) < a[u]) { ok = 0; break; }
        }
        if (!ok) continue;
        for (int u = 1; u < P; u++) s[u] += dot[u][p];
        sel[depth] = p;
        dfs(depth + 1, p);
        for (int u = 1; u < P; u++) s[u] -= dot[u][p];
    }
}
int main(void) {
    unsigned long long base[8];
    if (scanf("%d %d %d %d %d", &k1, &n0, &m, &lo, &mode) != 5) return 1;
    for (int i = 0; i < k1; i++) scanf("%llx", &base[i]);
    P = 1 << k1;
    for (int u = 0; u < P; u++) {
        unsigned long long r = 0;
        for (int i = 0; i < k1; i++) if (u >> i & 1) r ^= base[i];
        wr[u] = __builtin_popcountll(r);
        a[u] = lo - wr[u]; if (a[u] < 0) a[u] = 0;
        b[u] = m - (lo - wr[u]); if (b[u] > m) b[u] = m;
        for (int p = 0; p < P; p++) dot[u][p] = __builtin_popcount(u & p) & 1;
    }
    for (int u = 1; u < P; u++) if (a[u] > b[u]) return 0;
    dfs(0, 0);
    fprintf(stderr, "%lld\n", nsol);
    return 0;
}
