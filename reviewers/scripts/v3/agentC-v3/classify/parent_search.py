from reassess import *
from itertools import combinations

def run():
    rows=[int(s[::-1],2) for s in (OUT/'parent-56-10.txt').read_text().splitlines()]
    words=span(rows); cols=inspect(rows,56)['columns']
    pairs={}
    for i,j in combinations(range(56),2):pairs.setdefault(cols[i]^cols[j],[]).append((i,j))
    tested=0;best=0;hist=Counter();winner=None
    for u,ps in pairs.items():
        msgs=[m for m in range(1024) if (m&u).bit_count()%2==0]
        lows=[words[m] for m in msgs if words[m].bit_count()==24]
        for p,q in combinations(ps,2):
            # Four distinct coordinates; equality pairs after restricting to ker(u).
            js=sorted(p+q)
            if len(set(js))!=4:continue
            mask=sum(1<<j for j in js)
            bad=sum((w&mask)==mask for w in lows)
            tested+=1;hist[bad]+=1
            if bad==0:
                winner={'u':u,'deleted':js,'messages':msgs};break
        if winner:break
    result={'tested_pair_pair_choices':tested,'bad_weight24_words_hist':dict(sorted(hist.items())), 'winner':winner}
    (OUT/'parent56-search.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result),flush=True)

if __name__=='__main__':run()
