"""Try every weight-six orthogonal transvection of the public [54,9,24]."""
from reassess import *
from itertools import combinations

def main():
    start=time.monotonic();rows=[int(s[::-1],2) for s in (OUT/'parent-54-9.txt').read_text().splitlines()]
    words=span(rows);assert min(w.bit_count() for w in words if w)==24
    low=[w for w in words if w.bit_count()==24]
    inc=[sum((w>>j&1)<<i for i,w in enumerate(low)) for j in range(54)]
    oldcols=inspect(rows,54)['columns'];valid=0;types=Counter();tested=0;witness=None
    for a,b,c in combinations(range(51),3):
        ia,ib,ic=inc[a],inc[b],inc[c];i3=ia&ib&ic;k3=((ia&ib)|(ia&ic)|(ib&ic))^i3
        for d in range(c+1,52):
            i4=i3&inc[d];k4=(k3&inc[d])|(i3&~inc[d])
            for e in range(d+1,53):
                i5=i4&inc[e];k5=(k4&inc[e])|(i4&~inc[e])
                for f in range(e+1,54):
                    tested+=1
                    if i5&~inc[f] or k5&inc[f]:continue
                    valid+=1;coords=[a,b,c,d,e,f];syn=reduce(int.__xor__,(oldcols[j] for j in coords),0)
                    cols=[v^syn if j in coords else v for j,v in enumerate(oldcols)]
                    repeated=[v for v,count in Counter(cols).items() if v and count>1]
                    if repeated:
                        pair=[j for j,v in enumerate(cols) if v==repeated[0]][:2]
                        punct=[v for j,v in enumerate(cols) if j not in pair]
                        sol=[sum((v>>i&1)<<j for j,v in enumerate(punct)) for i in range(9)]
                        chk=inspect(sol,52);chk.pop('columns');assert chk['rank']==9 and chk['so'] and chk['d']>=22
                        witness={'hcoords':coords,'pair':pair,'check':chk}
                        (OUT/'SOLUTION-52-9-22.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in sol)+'\n')
                        print(json.dumps(witness),flush=True);break
                if witness:break
            if witness:break
        if witness:break
    res={'tested':tested,'total':math.comb(54,6),'valid_distance24':valid,'witness':witness,'seconds':time.monotonic()-start}
    (OUT/'parent54-neighbors.json').write_text(json.dumps(res,indent=2));print(json.dumps(res),flush=True)

if __name__=='__main__':main()
