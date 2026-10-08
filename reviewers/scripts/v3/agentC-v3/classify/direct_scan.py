"""Build and run PROOF 7.1. Default: bounded checks. Full scan needs --full.

Portable Python >=3.10 + GCC/OpenMP, or an already installed Docker gcc:14
image. Docker mode never pulls an image and disables container networking.
Outputs go to a new run directory, never to the historical evidence files.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid

ROOT=Path(__file__).resolve().parent
EXPECTED_SEEN={"seen0":2**34-2**17,"seen2":2**34+2**17}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def words(rows):
    out=[0]
    for r in rows:
        out += [w^r for w in out]
    return out


def rref(rows,n):
    rows=list(rows); pivots=[]; rank=0
    for col in range(n):
        found=next((j for j in range(rank,len(rows)) if rows[j]>>col&1),None)
        if found is None: continue
        rows[rank],rows[found]=rows[found],rows[rank]
        for j in range(len(rows)):
            if j!=rank and rows[j]>>col&1: rows[j]^=rows[rank]
        pivots.append(col); rank+=1
    return rows[:rank],pivots


def basis(rows,n):
    """D-perp vectors zero on an information set; each D-coset once."""
    k=len(rows)
    reduced,pivots=rref(rows,n)
    if len(reduced)!=k: raise ValueError('Dependent generator rows')
    dw=words(rows)
    if any(w.bit_count()%4 for w in dw): raise ValueError('Not doubly even')
    cons,cp=rref(rows+[1<<p for p in pivots],n)
    if len(cons)!=2*k: raise ValueError('Constraints are not independent')
    bs=[]
    for f in range(n):
        if f in cp: continue
        x=1<<f
        for row,p in zip(cons,cp):
            if row>>f&1: x|=1<<p
        bs.append(x)
    assert len(bs)==n-2*k
    assert all((x&r).bit_count()%2==0 for x in bs for r in rows)
    assert all(not(x>>p&1) for x in bs for p in pivots)
    assert len(rref(rows+bs,n)[0])==n-k
    return bs


def read_matrix(path):
    lines=[x.strip() for x in Path(path).read_text().splitlines() if x.strip()]
    if not lines or len({len(x) for x in lines})!=1 or any(set(x)-{'0','1'} for x in lines):
        raise ValueError('Invalid binary matrix')
    n=len(lines[0]); rows=[int(x[::-1],2) for x in lines]
    if not 1<=n<=62 or not 1<=len(rows)<=12 or n-2*len(rows)<0:
        raise ValueError('Unsupported dimensions')
    return n,rows


def header(path,n,rows):
    bs=basis(rows,n)
    def array(name,items):
        return f'static const unsigned long long {name}[{max(1,len(items))}]={{'+','.join(hex(x)+'ULL' for x in (items or [0]))+'};\n'
    text=f'#define CODE_N {n}\n#define CODE_K {len(rows)}\n#define QUOTIENT_DIM {len(bs)}\n'
    Path(path).write_text(text+array('DR',rows)+array('NB_',bs),encoding='ascii')
    return bs


def representative(bs,index):
    gray=index^(index>>1); x=0
    for i,b in enumerate(bs):
        if gray>>i&1: x^=b
    return x


def expected_range(rows,bs,threshold,start,count):
    ans=dict(seen0=0,seen2=0,hit0=0,hit2=0)
    dw=words(rows)
    for i in range(start,start+count):
        x=representative(bs,i); w=x.bit_count()
        if w%2: continue
        cls=str(w%4); ans['seen'+cls]+=1
        if min((x^d).bit_count() for d in dw)>=threshold: ans['hit'+cls]+=1
    return ans


def independent_small(rows,n,threshold):
    """Enumerate every ambient vector, quotient by actual sets, no nullspace."""
    dw=words(rows); cosets={}
    for v in range(1<<n):
        if any((v&r).bit_count()%2 for r in rows): continue
        coset=frozenset(v^d for d in dw)
        cosets[coset]=min(coset)
    ans=dict(seen0=0,seen2=0,hit0=0,hit2=0)
    for coset,v in cosets.items():
        if v.bit_count()%2: continue
        cls=str(v.bit_count()%4); ans['seen'+cls]+=1
        if min(x.bit_count() for x in coset)>=threshold: ans['hit'+cls]+=1
    assert len(cosets)==2**(n-2*len(rows))
    return ans


def gray_index(vector,bs):
    piv={}
    for i,b in enumerate(bs):
        c=1<<i
        while b:
            p=b.bit_length()-1
            if p in piv: b^=piv[p][0]; c^=piv[p][1]
            else: piv[p]=(b,c); break
    mask=0
    while vector:
        p=vector.bit_length()-1
        if p not in piv: raise ValueError('Not in complement')
        vector^=piv[p][0]; mask^=piv[p][1]
    index=0
    while mask: index^=mask; mask>>=1
    return index


class Engine:
    def __init__(self,backend,compiler,out,threads,timeout):
        self.backend=backend; self.compiler=compiler; self.out=out
        self.threads=threads; self.timeout=timeout; self.commands=[]

    def command(self,cmd):
        env=os.environ.copy(); env['OMP_NUM_THREADS']=str(self.threads)
        begin=time.monotonic()
        p=subprocess.run(cmd,cwd=self.out,env=env,text=True,encoding='utf-8',
                         stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=self.timeout)
        rec={'argv':cmd,'exit_code':p.returncode,'seconds':time.monotonic()-begin,'output':p.stdout}
        self.commands.append(rec)
        (self.out/'commands.json').write_text(json.dumps(self.commands,indent=2),encoding='utf-8')
        if p.returncode: raise RuntimeError(p.stdout or str(cmd))
        return p.stdout

    def docker(self,args):
        return ['docker','run','--rm','--pull=never','--network=none',
                '--cpus',str(self.threads),'-e',f'OMP_NUM_THREADS={self.threads}',
                '-v',f'{ROOT}:/src:ro','-v',f'{self.out}:/work','-w','/work','gcc:14']+args

    def build(self,label,n,rows):
        hp=self.out/(label+'.h'); bs=header(hp,n,rows)
        if self.backend=='docker':
            cmd=self.docker(['gcc','-std=c11','-O3','-march=native','-fopenmp','-I/work',
                             f'-DHDR="{hp.name}"','/src/scan_direct.c','-o',label])
        else:
            exe=label+('.exe' if os.name=='nt' else '')
            cmd=[self.compiler,'-std=c11','-O3','-march=native','-fopenmp','-I',str(self.out),
                 f'-DHDR="{hp.name}"',str(ROOT/'scan_direct.c'),'-o',str(self.out/exe)]
        self.command(cmd)
        return bs

    def scan(self,label,threshold,start,count,expected):
        args=[str(threshold),str(start),str(count)]
        if self.backend=='docker': cmd=self.docker(['./'+label]+args)
        else: cmd=[str(self.out/(label+('.exe' if os.name=='nt' else '')))]+args
        text=self.command(cmd); result=json.loads(text)
        assert result['threshold']==threshold and result['start']==start and result['count']==count
        assert result['visited']==count
        for name,value in expected.items():
            assert result[name]==value,(label,name,result[name],value)
        result['label']=label; result['expected_counts_matched']=True
        print(json.dumps(result),flush=True)
        return result


def run(mode,backend,compiler,threads,out):
    out=Path(out).resolve(); out.mkdir(parents=True,exist_ok=False)
    engine=Engine(backend,compiler,out,threads,30 if mode=='check' else None)
    meta={'mode':mode,'full_scan_completed':False,'backend':backend,'threads':threads,
          'source_sha256':sha(ROOT/'scan_direct.c'),'inputs':{},'runs':[]}
    target=out/'DIRECT-REPRODUCTION.json'
    def save(): target.write_text(json.dumps(meta,indent=2),encoding='utf-8')
    save()
    try:
        matrices=[]
        for i in range(3):
            fp=ROOT/f'D-representative-{i}.txt'; n,rows=read_matrix(fp)
            assert n==52 and len(rows)==8 and min(w.bit_count() for w in words(rows) if w)==24
            meta['inputs'][fp.name]=sha(fp)
            bs=engine.build(f'D{i}',n,rows); matrices.append((rows,bs))
            for threshold in ([22,20] if i==0 and mode=='full' else [22]):
                if mode=='full':
                    expect=EXPECTED_SEEN|{'hit0':1138092541 if threshold==20 else 0,'hit2':0}
                    r=engine.scan(f'D{i}',threshold,0,2**36,expect)
                else:
                    # Cross a Gray block boundary; only 4,096 representatives per D.
                    start=2**16-2048; count=4096
                    expect=expected_range(rows,bs,threshold,start,count)
                    r=engine.scan(f'D{i}',threshold,start,count,expect)
                meta['runs'].append(r); save()
        if mode=='check':
            for label,n,rows in [('small1',8,[15]),('small2',8,[15,240]),('small3',4,[15])]:
                bs=engine.build(label,n,rows)
                for threshold in [0,2,4]:
                    expect=independent_small(rows,n,threshold)
                    meta['runs'].append(engine.scan(label,threshold,0,2**len(bs),expect))
            # Positive control at the actual length: all-ones + D0 has min 20.
            rows,bs=matrices[0]; _,pivots=rref(rows,52); allones=2**52-1
            x=next(allones^d for d in words(rows) if all(not((allones^d)>>p&1) for p in pivots))
            ix=gray_index(x,bs)
            assert representative(bs,ix)==x
            for threshold in [20,22]:
                expect=expected_range(rows,bs,threshold,ix,1)
                assert expect['hit0']==(1 if threshold==20 else 0)
                meta['runs'].append(engine.scan('D0',threshold,ix,1,expect))
            meta['check_passed']=True
            meta['scope']='Small ambient-space exhaustive comparisons, 4096 reps per D, and one known D0 coset; NOT a full length-52 scan.'
        else:
            assert len(meta['runs'])==4 and all(r['visited']==2**36 for r in meta['runs'])
            meta['full_scan_completed']=True
            meta['scope']='3 kernels at T=22 and D0 at T=20, all 2^36 quotient representatives each.'
        save(); return meta
    except BaseException as exc:
        meta['error']=str(exc); save(); raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(); g.add_argument('--full',action='store_true'); g.add_argument('--check',action='store_true')
    p.add_argument('--backend',choices=['native','docker'],default='native')
    p.add_argument('--compiler',default='gcc'); p.add_argument('--threads',type=int,default=1)
    p.add_argument('--out',type=Path)
    a=p.parse_args()
    if a.threads<1: p.error('--threads must be positive')
    if a.backend=='native' and shutil.which(a.compiler) is None: p.error('GCC not found; use --backend docker with an existing gcc:14 image')
    mode='full' if a.full else 'check'
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]
    out=a.out or ROOT/'runs'/f'direct-{mode}-{stamp}'
    result=run(mode,a.backend,a.compiler,a.threads,out)
    print(json.dumps({'result_file':str(out/'DIRECT-REPRODUCTION.json'),
                      'full_scan_completed':result['full_scan_completed'],
                      'check_passed':result.get('check_passed')}))


if __name__=='__main__': main()
