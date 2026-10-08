/* Agent A2 independent scan: all 2^36 coset reps x in N (D^perp vanishing on pivot set P).
   D words are generated here from the 8 rows. For even wt(x): coset min weight = min_{d in D} wt(x+d).
   Reports, per wt(x) mod 4 class: number of even reps seen (coverage), and #cosets with min >= T.
   usage: scanA T */
#include <stdio.h>
#include <stdlib.h>
#include HDR
int main(int argc,char**argv){
  int T=atoi(argv[1]);
  static unsigned long long DW[256];
  for(int m=0;m<256;m++){unsigned long long w=0;for(int i=0;i<8;i++) if(m>>i&1) w^=DR[i]; DW[m]=w;}
  for(int m=1;m<256;m++){int w=__builtin_popcountll(DW[m]); if(w%4||w<24){printf("BAD D word\n");return 1;}}
  const int HI=14, LO=36-HI;
  long long seen0=0,seen2=0,hit0=0,hit2=0;
  #pragma omp parallel for schedule(dynamic,4) reduction(+:seen0,seen2,hit0,hit2)
  for(long h=0;h<(1L<<HI);h++){
    unsigned long long base=0;
    for(int i=0;i<HI;i++) if(h>>i&1) base^=NB_[LO+i];
    unsigned long long x=base, g=0;
    for(unsigned long long s=0;s<(1ULL<<LO);s++){
      if(s){int b=__builtin_ctzll(s); x^=NB_[b];}
      int w=__builtin_popcountll(x);
      if(w&1) continue;
      int cls=w&3;
      if(cls==0) seen0++; else seen2++;
      if(w<T) continue;
      int ok=1;
      for(int m=1;m<256;m++) if(__builtin_popcountll(x^DW[m])<T){ok=0;break;}
      if(ok){ if(cls==0) hit0++; else hit2++; }
    }
  }
  printf("T=%d even reps: 0mod4 %lld, 2mod4 %lld (sum %lld, 2^35=%lld) | min>=T: 0mod4 %lld, 2mod4 %lld\n",
         T,seen0,seen2,seen0+seen2,1LL<<35,hit0,hit2);
  return 0;
}
