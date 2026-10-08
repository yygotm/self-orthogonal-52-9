"""All weight-6 orthogonal transvections from one doubly-even kernel.
Grouped by weight distribution only, NOT by code equivalence.
"""
from reassess import *
from itertools import combinations

def main():
    start=time.monotonic();rows=[int(s[::-1],2) for s in (OUT/'fullsupport-D-2251816993685511.txt').read_text().splitlines()];words=span(rows);low=[w for w in words if w.bit_count()==24]
    inc=[sum(((w>>j)&1)<<i for i,w in enumerate(low)) for j in range(52)]
    types={};tested=0;valid=0
    for a,b,c in combinations(range(49),3):
        ia,ib,ic=inc[a],inc[b],inc[c];i3=ia&ib&ic;k3=((ia&ib)|(ia&ic)|(ib&ic))^i3
        for d in range(c+1,50):
            i4=i3&inc[d];k4=(k3&inc[d])|(i3&~inc[d])
            for e in range(d+1,51):
                i5=i4&inc[e];k5=(k4&inc[e])|(i4&~inc[e])
                for f in range(e+1,52):
                    tested+=1
                    if i5&~inc[f] or k5&inc[f]:continue
                    valid+=1;h=(1<<a)|(1<<b)|(1<<c)|(1<<d)|(1<<e)|(1<<f)
                    wd=Counter((w^h if (w&h).bit_count()%2 else w).bit_count() for w in words);key=tuple(sorted(wd.items()))
                    if key not in types:
                        out=[r^h if (r&h).bit_count()%2 else r for r in rows];info=inspect(out,52);info.pop('columns');assert info['so'] and info['d']>=24
                        idx=len(types);types[key]={'type_index':idx,'h':h,'count':0,'check':info}
                        (OUT/f'neighbor-D-{idx}.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in out)+'\n')
                        print(json.dumps({'new_weight_type':idx,'h':h,'check':info,'seconds':time.monotonic()-start}),flush=True)
                    types[key]['count']+=1
    result={'tested':tested,'expected':math.comb(52,6),'valid':valid,'weight_types':list(types.values()),'seconds':time.monotonic()-start}
    assert tested==math.comb(52,6)
    (OUT/'kernel-neighbors.json').write_text(json.dumps(result,indent=2));print(json.dumps({'tested':tested,'valid':valid,'weight_types':len(types),'seconds':result['seconds']}),flush=True)

if __name__=='__main__':main()
