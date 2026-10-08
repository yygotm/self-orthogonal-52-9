"""Independent exploration of binary self-orthogonal [52,9,22]."""
import sys, math, json, time, re, urllib.request
from pathlib import Path
from collections import Counter
from functools import reduce
# Use the selected Python environment; no author-specific package directory.
OUT=Path(__file__).resolve().parent

def kw(n,j,w):
    return sum((-1)**s*math.comb(w,s)*math.comb(n-w,j-s) for s in range(max(0,j-n+w),min(w,j)+1))

def enumerator(no_d_zero=False, not_eight=False, cubic_bound=False, maximize_odd=False, ones=False, objective=None, fixed_d=None):
    from ortools.sat.python import cp_model
    n=52; size=512; weights=list(range(22,53,2))
    m=cp_model.CpModel()
    a={0:1}|{w:m.new_int_var(0,511,f'A{w}') for w in weights}
    m.add(sum(a.values())==512)
    m.add(sum(x for w,x in a.items() if w%4==0)==256)
    if fixed_d is not None:
        for w,x in a.items():
            if w%4==0:m.add(x==fixed_d.get(w,0))
    bs=[];ss=[]
    for j in range(53):
        b=m.new_int_var(0,min(math.comb(52,j),2**43),f'B{j}')
        s=m.new_int_var(0,min(math.comb(52,j),2**43),f'S{j}')
        for var,sgn in [(b,False),(s,True)]:
            co={w:kw(n,j,w)*((-1)**(w//2) if sgn else 1) for w in a}
            g=reduce(math.gcd,[512]+list(co.values()))
            m.add(sum(co[w]//g*x for w,x in a.items())==512//g*var)
        m.add(b>=a.get(j,0));bs.append(b);ss.append(s)
    # D has dimension 8 and distance >=24. Its effective length is >=51.
    m.add(bs[1]+ss[1]<=1)
    if no_d_zero:m.add(bs[1]+ss[1]==0)
    odd=sum(x for w,x in a.items() if w%8==4)
    if not_eight:m.add(odd>=1)
    if cubic_bound:m.add(odd>=32)
    if ones:m.add(a[52]==1)
    if objective and objective.startswith('A'):m.maximize(a[int(objective[1:])])
    elif objective=='B2':m.maximize(bs[2])
    elif objective=='Ddual2':m.maximize(bs[2]+ss[2])
    elif maximize_odd:m.maximize(odd)
    else:m.minimize(ss[1]+bs[1])
    error=m.validate()
    if error:return {'error':error}
    sol=cp_model.CpSolver();sol.parameters.max_time_in_seconds=40;sol.parameters.num_workers=4
    start=time.monotonic(); st=sol.solve(m)
    result={'no_D_zero':no_d_zero,'not_eight':not_eight,'status':sol.status_name(st),'seconds':time.monotonic()-start}
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        A={w:(x if isinstance(x,int) else sol.value(x)) for w,x in a.items()}
        B=[sum(kw(n,j,w)*x for w,x in A.items())//size for j in range(53)]
        S=[sum((-1)**(w//2)*kw(n,j,w)*x for w,x in A.items())//size for j in range(53)]
        for j in range(53):
            assert sum(kw(n,j,w)*x for w,x in A.items())==size*B[j]
            assert sum((-1)**(w//2)*kw(n,j,w)*x for w,x in A.items())==size*S[j]
            assert B[j]>=A.get(j,0) and S[j]>=0
        result.update(A={w:x for w,x in A.items() if x},B=B,S=S,D_zero=B[1]+S[1])
    return result

def span(rows):
    a=[0]
    for r in rows:a += [w^r for w in a]
    return a

def inspect(rows,n):
    words=span(rows); wd=Counter(x.bit_count() for x in words)
    cols=[sum((r>>j&1)<<i for i,r in enumerate(rows)) for j in range(n)]
    return dict(n=n,k=len(rows),rank=int(math.log2(len(set(words)))),d=min(w for w in wd if w),
                weights=dict(sorted(wd.items())),so=all((a&b).bit_count()%2==0 for a in rows for b in rows),
                zeros=cols.count(0),repeats={c:q for c,q in Counter(cols).items() if q>1},columns=cols)

def parent(n,k):
    url=f'https://www.codetables.de/BKLC/BKLC.php?q=2&n={n}&k={k}'
    path=OUT/f'codetables-{n}-{k}.html'
    if not path.exists():
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        path.write_bytes(urllib.request.urlopen(req,timeout=25).read())
    raw=path.read_text(errors='replace'); rows=[]
    for row in re.findall(r'\[([01,\s]+)\]',raw):
        vals=re.findall(r'[01]',row)
        if len(vals)==n:rows.append(sum(int(x)<<j for j,x in enumerate(vals)))
    if len(rows)!=k:return {'n':n,'k':k,'matrix_rows':len(rows),'source':url}
    result=inspect(rows,n);result['source']=url
    (OUT/f'parent-{n}-{k}.txt').write_text('\n'.join(''.join(str(r>>j&1) for j in range(n)) for r in rows)+'\n')
    result.pop('columns')
    return result

if __name__=='__main__':
    if '--parents' in sys.argv:
        for n,k in [(54,9),(53,9),(55,9),(56,9),(54,10),(56,10)]:
            try:r=parent(n,k)
            except Exception as e:r={'n':n,'k':k,'error':str(e)}
            print(json.dumps(r),flush=True)
            (OUT/f'parent-{n}-{k}.json').write_text(json.dumps(r,indent=2))
    else:
        results=[]
        for nozero,not_eight in [(False,False),(True,True)]:
            r=enumerator(nozero,not_eight);results.append(r);print(json.dumps({k:v for k,v in r.items() if k not in ('B','S')}),flush=True)
        (OUT/'enumerators.json').write_text(json.dumps(results,indent=2))
