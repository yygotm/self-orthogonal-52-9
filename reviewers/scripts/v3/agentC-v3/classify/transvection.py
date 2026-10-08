"""Search isometries x -> x + <x,h>h, wt(h)=2 mod4, on D."""
from triple_search import setup
from reassess import *
from itertools import combinations

def main():
    start=time.monotonic();rows,_,_,_=setup();words=span(rows);low=[w for w in words if w.bit_count()==24]
    incidence=[sum(((w>>j)&1)<<i for i,w in enumerate(low)) for j in range(51)]
    total=0;found=[]
    for a,b,c,d in combinations(range(50),4):
        base=incidence[a]&incidence[b]&incidence[c]&incidence[d]
        for e in range(d+1,51):
            total+=1
            if not(base&incidence[e]):
                h=(1<<51)|(1<<a)|(1<<b)|(1<<c)|(1<<d)|(1<<e)
                out=[r^h if (r&h).bit_count()%2 else r for r in rows]
                check=inspect(out,52);check.pop('columns');assert check['so'] and check['d']>=24
                found.append({'h':h,'check':check})
                if check['zeros']==0 and not (OUT/'fullsupport-D-first.txt').exists():(OUT/'fullsupport-D-first.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in out)+'\n')
    result={'tested_h':total,'expected_h':math.comb(51,5),'found':len(found),'examples':found[:10],'seconds':time.monotonic()-start}
    (OUT/'transvection6.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
