"""Package completed evidence without altering source-project files."""
from pathlib import Path
import hashlib,json,zipfile
OUT=Path(__file__).resolve().parent

def main():
    completed=json.loads((OUT/'REPRODUCTION.json').read_text());assert completed['complete']
    files=sorted(p for p in OUT.iterdir() if p.is_file() and p.name!='MANIFEST.json' and p.suffix in {'.py','.md','.json','.jsonl','.txt','.lp','.log'})
    for p in files:
        if p.suffix=='.md':assert '\ufffd' not in p.read_text(encoding='utf-8')
    manifest={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'md5':hashlib.md5(p.read_bytes()).hexdigest()} for p in files}
    (OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    archive=OUT.parent/'so52-proof-draft-20261008.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files+[OUT/'MANIFEST.json']:z.write(p,'so52/'+p.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name,item in manifest.items():assert hashlib.sha256(z.read('so52/'+name)).hexdigest()==item['sha256']
    raw=archive.read_bytes();sha=hashlib.sha256(raw).hexdigest();md5=hashlib.md5(raw).hexdigest()
    hashes=archive.with_suffix('.hashes.txt');hashes.write_text(f'File: {archive.name}\nBytes: {len(raw)}\nSHA256: {sha}\nMD5: {md5}\n',encoding='utf-8')
    print(json.dumps({'archive':str(archive),'files':len(files)+1,'bytes':len(raw),'sha256':sha,'md5':md5,'hash_file':str(hashes)}))

if __name__=='__main__':main()
