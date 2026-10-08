"""v3.1 entry point. Default: bounded checks. Full scans require --full.

python reproduce.py --check --backend docker
python reproduce.py --full --backend docker --threads 16

The full path reruns [16,7,6] classification, kernel classification and
Section 7.1. --legacy-cross-checks adds the old reflection route.
Historical outputs are preserved. Each run uses a fresh output directory.
"""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid

ROOT=Path(__file__).resolve().parent
CLASSIFY=['residual36_cubics.py','exact36.py','exact40.py',
          'normalized32_orbits.py','normalized36_orbits.py']
LEGACY=['triple_exhaustive.py','joint_switch_search.py']
CLASSIFY_INPUTS=[f'residual16-{i}.txt' for i in range(3)]


def prepare_classification(work, root=ROOT):
    """Stage code and named inputs only; never seed generated classifications."""
    work.mkdir(parents=True,exist_ok=False)
    sources=sorted(root.glob('*.py'))+[root/name for name in CLASSIFY_INPUTS]
    for source in sources:
        shutil.copyfile(source,work/source.name)
    return [source.name for source in sources]


def verify_classification(work):
    """Fail closed on missing outputs, extra orbits/classes, or wrong counts."""
    def read(name):
        return json.loads((work/name).read_text(encoding='utf-8'))
    def require(condition,message):
        if not condition:
            raise ValueError('classification verification failed: '+message)
    def one_class(classes,rows,count,label):
        require(len(rows)==count and len(set(rows))==count,label+' candidate count')
        require(len(classes)==1,label+' must have one class')
        require(len(classes[0])==count and set(classes[0])==set(rows),
                label+' class must contain every candidate exactly once')

    c36=read('normalized36-classification.json')
    require(c36['first_rows']==5376,'weight-36 first_rows')
    require(len(c36['first_orbits'])==1,'weight-36 must have one first orbit')
    require(c36['first_orbits'][0]['size']==5376,'weight-36 orbit size')
    require(len(c36['kernels'])==1,'weight-36 must have one kernel branch')
    k36=c36['kernels'][0]
    require(k36['core_index']==0 and k36['second_rows']==36,'weight-36 second_rows')
    one_class(k36['classes'],read('normalized36-second-rows-0.json'),36,'weight-36')

    o32=read('normalized32-orbits.json')
    require(o32['raw']==344064 and o32['quotient']==10752,'weight-32 first_rows')
    require(len(o32['orbits'])==1,'weight-32 must have one first orbit')
    require(o32['orbits'][0]['size']==10752,'weight-32 orbit size')
    c32=read('normalized32-classification.json')
    one_class(c32['equivalence_classes'],c32['second_rows'],24,'weight-32')

    e36=read('exact36-results.json')
    e40=read('exact40-results.json')
    cases40=[row for branch in e40 for row in branch['cases']]
    allowed={'EXHAUSTED','MODULAR_CONTRADICTION'}
    require(len(e36)==49 and sum(r.get('enumerated',0) for r in e36)==5318,
            'exact36: 49 models and 5318 candidates')
    require(all(r['status'] in allowed and r.get('valid_nonnegative_integer',0)==0
                for r in e36),'exact36: completed with no solutions')
    require(len(e40)==2 and len(cases40)==4 and
            sum(r.get('enumerated',0) for r in cases40)==8448,
            'exact40: two branches, four cases and 8448 candidates')
    require(all(r['status'] in allowed and r.get('valid',0)==0 for r in cases40),
            'exact40: completed with no solutions')
    return {'normalized36':{'first_rows':5376,'first_orbits':1,'second_rows':36,'classes':1},
            'normalized32':{'raw':344064,'first_rows':10752,'first_orbits':1,'second_rows':24,'classes':1},
            'exact36':{'models':49,'candidates':5318,'solutions':0},
            'exact40':{'branches':2,'cases':4,'candidates':8448,'solutions':0}}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(); g.add_argument('--check',action='store_true'); g.add_argument('--full',action='store_true')
    p.add_argument('--backend',choices=['native','docker'],default='native')
    p.add_argument('--compiler',default='gcc'); p.add_argument('--threads',type=int,default=1)
    p.add_argument('--legacy-cross-checks',action='store_true'); p.add_argument('--out',type=Path)
    a=p.parse_args()
    if a.threads<1: p.error('--threads must be positive')
    if a.legacy_cross_checks and not a.full: p.error('--legacy-cross-checks requires --full')
    mode='full' if a.full else 'check'
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]
    out=(a.out or ROOT/'runs'/f'v3.1-{mode}-{stamp}').resolve()
    out.mkdir(parents=True,exist_ok=False)
    meta={'version':'3.1','mode':mode,'full_proof_reproduced':False,'runs':[],
          'python':sys.version,'started_utc':datetime.now(timezone.utc).isoformat()}
    result=out/'REPRODUCTION-V3.1.json'
    def save(): result.write_text(json.dumps(meta,indent=2),encoding='utf-8')
    def call(name,args,cwd):
        begin=time.monotonic(); print('START '+name,flush=True)
        with (out/(name+'.log')).open('w',encoding='utf-8') as log:
            proc=subprocess.run(args,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,
                                timeout=None if a.full else 180)
        meta['runs'].append({'name':name,'argv':args,'cwd':str(cwd),
                             'exit_code':proc.returncode,'seconds':time.monotonic()-begin})
        save()
        if proc.returncode: raise RuntimeError(f'{name} failed; see {out/(name+".log")}')
    save()
    try:
        call('evidence',[sys.executable,'-B',str(ROOT/'verify_evidence.py')],ROOT)
        call('q0-certificate',[sys.executable,'-B',str(ROOT/'verify_q0_certificate.py')],ROOT)
        if a.full:
            work=out/'classification'
            meta['classification_staged_files']=prepare_classification(work)
            script=ROOT/'evidence/agentA-v2/classes16.py'
            for lo,hi in [(0,7200),(7200,14400),(14400,21600),(21600,28718)]:
                call(f'classes16-{lo}',[sys.executable,'-B',str(script),str(lo),str(hi)],out)
                text=(out/f'classes16-{lo}.log').read_text(encoding='utf-8')
                expected=f'checked {hi-lo} weight-distribution groups 3 codes NOT mapped to their group rep 0 codes with odd words 0'
                assert 'solutions 28718' in text and expected in text
            for name in CLASSIFY: call(name,[sys.executable,'-B',str(work/name)],work)
            meta['classification_checks']=verify_classification(work)
            save()
            if a.legacy_cross_checks:
                for name in LEGACY: call(name,[sys.executable,'-B',str(work/name)],work)
            else:
                # Only this archived legacy log is input to audit_exact;
                # no generated classification JSON/TXT is pre-populated.
                shutil.copyfile(ROOT/'joint-switch-full-0.jsonl',work/'joint-switch-full-0.jsonl')
            # audit_exact also checks archived legacy outputs; do not call them rerun.
            call('audit_exact.py',[sys.executable,'-B',str(work/'audit_exact.py')],work)
            for i in range(3):
                name=f'D-representative-{i}.txt'
                assert (work/name).read_text().splitlines()==(ROOT/name).read_text().splitlines()
            meta['audit_legacy_results_rerun']=a.legacy_cross_checks
        cmd=[sys.executable,'-B',str(ROOT/'direct_scan.py'),'--'+mode,
             '--backend',a.backend,'--compiler',a.compiler,'--threads',str(a.threads),
             '--out',str(out/'direct')]
        call('direct-scan',cmd,ROOT)
        direct=json.loads((out/'direct/DIRECT-REPRODUCTION.json').read_text())
        if a.full:
            assert direct['full_scan_completed']; meta['full_proof_reproduced']=True
        else:
            assert direct['check_passed'] and not direct['full_scan_completed']
            meta['bounded_checks_passed']=True
        meta['completed']=True; save()
        print(json.dumps({'result_file':str(result),'full_proof_reproduced':meta['full_proof_reproduced'],
                          'bounded_checks_passed':meta.get('bounded_checks_passed')}),flush=True)
    except BaseException as exc:
        meta['completed']=False; meta['error']=str(exc); save(); raise


if __name__=='__main__': main()
