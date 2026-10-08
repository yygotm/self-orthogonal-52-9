"""Run the complete final computation. No optimization solver is called.
Requires Python >=3.10 and NumPy >=2 (numpy.bitwise_count).
Run: python reproduce.py
Outputs detailed logs in reproduction-*.log and completed-run metadata.
"""
import subprocess,sys,json,time,hashlib
from pathlib import Path
OUT=Path(__file__).resolve().parent
SCRIPTS=['residual36_cubics.py','exact36.py','exact40.py','normalized32_orbits.py','normalized36_orbits.py','triple_exhaustive.py','joint_switch_search.py','audit_exact.py']

def main():
    runs=[];start=time.monotonic()
    for name in SCRIPTS:
        begin=time.monotonic();print('START '+name,flush=True)
        with (OUT/('reproduction-'+name+'.log')).open('w',encoding='utf-8') as log:
            p=subprocess.Popen([sys.executable,str(OUT/name)],cwd=OUT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8')
            for line in p.stdout:log.write(line);log.flush()
            rc=p.wait()
        run={'script':name,'exit_code':rc,'seconds':time.monotonic()-begin,'sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest()};runs.append(run)
        (OUT/'REPRODUCTION.json').write_text(json.dumps({'runs':runs,'complete':False},indent=2))
        print(json.dumps(run),flush=True)
        if rc:raise SystemExit(rc)
    js=json.loads((OUT/'joint-switch-summary.json').read_text());assert js['status']=='EXHAUSTED_ALL_ORBITS' and js['orbits_done']==23 and js['h_count']==29376
    result={'complete':True,'optimizer_called':False,'python':sys.version,'runs':runs,'seconds':time.monotonic()-start,'scope':'All final enumerations; mathematical reductions and cited classification theorems are described in PROOF.md, not machine-formalized.'}
    (OUT/'REPRODUCTION.json').write_text(json.dumps(result,indent=2));print(json.dumps({'COMPLETE':True,'seconds':result['seconds']}),flush=True)

if __name__=='__main__':main()
