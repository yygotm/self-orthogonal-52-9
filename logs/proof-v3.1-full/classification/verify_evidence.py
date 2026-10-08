"""Fast integrity and historical-completion checks; does not rerun scans."""
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent


def verify():
    records=json.loads((ROOT/'SOURCE-MANIFEST.json').read_text(encoding='utf-8'))['copies']
    for rec in records:
        path=ROOT/rec['path']
        assert path.is_file(),path
        assert hashlib.sha256(path.read_bytes()).hexdigest()==rec['sha256'],path
    coverage=[]
    for start,end in [(0,7200),(7200,14400),(14400,21600),(21600,28718)]:
        path=ROOT/f'evidence/agentA-v2/classes16-{start}.log'
        text=path.read_text()
        assert 'solutions 28718' in text and 'global groups 3' in text
        m=re.search(r'checked (\d+) weight-distribution groups 3 codes NOT mapped to their group rep (\d+) codes with odd words (\d+)',text)
        assert m and tuple(map(int,m.groups()))==(end-start,0,0),path
        coverage.append([start,end])
    assert sum(b-a for a,b in coverage)==28718
    for i in range(3):
        p=ROOT/f'evidence/agentA-v2/scanA{i}-22.out'
        text=p.read_text()
        assert '0mod4 17179738112, 2mod4 17180000256 (sum 34359738368' in text,p
        assert 'min>=T: 0mod4 0, 2mod4 0' in text,p
        assert 'accepted 0 of 2^36' in (ROOT/f'evidence/ext52x/d22-gpt{i}.out').read_text()
        assert (ROOT/f'D-representative-{i}.txt').read_text().splitlines()==(ROOT/f'evidence/ext52x/D-gpt{i}.txt').read_text().splitlines()
    positive=(ROOT/'evidence/agentC-v2/scanA0-20.out').read_text()
    assert 'min>=T: 0mod4 1138092541, 2mod4 0' in positive
    return {'copied_files_hash_verified':len(records),'classes16_ranges':coverage,
            'classes16_unmapped':0,'historical_named_full_scan_logs_verified':True,
            'historical_positive_control':1138092541,'scans_rerun':False}


if __name__=='__main__': print(json.dumps(verify(),sort_keys=True))
