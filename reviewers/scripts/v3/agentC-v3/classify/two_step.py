"""Enumerate two weight-4 isometries from the near-solution seed.
All second moves are covered for each processed first move. First moves are
ordered by resulting count of weight-20 words and bounded by wall time.
"""
from reassess import *
from itertools import combinations
import numpy as np,argparse

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=120);args=ap.parse_args()
    start=time.monotonic();rows=[int(s[::-1],2) for s in (OUT/'best-fixed-seed.txt').read_text().splitlines()];words=np.array(span(rows)[1:],dtype=np.uint64);weights=np.bitwise_count(words)
    allh=np.array([sum(1<<j for j in js) for js in combinations(range(52),4)],dtype=np.uint64)
    firsts=allh[np.bitwise_count(allh&words[weights==18][0])==1]
    costs=np.ones(len(firsts),dtype=np.int16)
    for w in words[weights==22]:costs+=(np.bitwise_count(firsts&w)==3)
    order=np.argsort(costs,kind='stable');hist=dict(Counter(map(int,costs)))
    print(json.dumps({'first_moves':len(firsts),'weight20_hist':hist}),flush=True)
    done=0;minbad=10000
    for ix in order:
        h1=firsts[ix];changed=np.bitwise_count(words&h1)%2;w1=words^(changed.astype(np.uint64)*h1);wt1=np.bitwise_count(w1)
        options=allh
        for w in w1[wt1==20]:
            options=options[np.bitwise_count(options&w)==1]
            if not len(options):break
        if len(options):
            for w in w1[wt1==22]:
                options=options[np.bitwise_count(options&w)!=3]
                if not len(options):break
        if len(options):
            h2=int(options[0]);h1=int(h1);r1=[r^h1 if (r&h1).bit_count()%2 else r for r in rows];out=[r^h2 if (r&h2).bit_count()%2 else r for r in r1];check=inspect(out,52);check.pop('columns');assert check['so'] and check['rank']==9 and check['d']>=22
            result={'FOUND':True,'h1':h1,'h2':h2,'check':check,'seconds':time.monotonic()-start}
            (OUT/'SOLUTION-52-9-22.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in out)+'\n');(OUT/'two-step-SOLUTION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);return
        done+=1
        if done%1000==0:print(json.dumps({'done':done,'current_bad20':int(costs[ix]),'seconds':time.monotonic()-start}),flush=True)
        if time.monotonic()-start>args.seconds:break
    result={'status':'NO_WITNESS_IN_PROCESSED_FIRST_MOVES','processed_first_moves':done,'total_first_moves':len(firsts),'last_bad20':int(costs[ix]),'hist':hist,'seconds':time.monotonic()-start}
    (OUT/'two-step-result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
