import json, hashlib, os, sys
root = sys.argv[1]
SEP = os.sep
def h(p, alg):
    m = hashlib.new(alg)
    with open(p, 'rb') as f:
        m.update(f.read())
    return m.hexdigest()
def norm(r):
    return r.replace(SEP, '/')
d = json.load(open(os.path.join(root, 'MANIFEST.json'), encoding='utf-8'))
print('== MANIFEST entries', len(d))
ok = bad = miss = 0
for rel, info in d.items():
    p = os.path.join(root, rel)
    if not os.path.exists(p):
        miss += 1; print('MISSING', rel); continue
    s = h(p, 'sha256'); m = h(p, 'md5'); b = os.path.getsize(p)
    if s == info.get('sha256') and m == info.get('md5') and b == info.get('bytes'):
        ok += 1
    else:
        bad += 1; print('MISMATCH', rel, b, info.get('bytes'))
print('ok', ok, 'bad', bad, 'missing', miss)
listed = set(norm(k) for k in d)
extra = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        r = norm(os.path.relpath(os.path.join(dp, f), root))
        if r not in listed:
            extra.append(r)
print('on-disk files not in MANIFEST:', len(extra))
for r in sorted(extra):
    print('  ', r)
print('PROOF-v2 sha256', h(os.path.join(root, 'PROOF-v2-20261008.md'), 'sha256'))
sm = json.load(open(os.path.join(root, 'SOURCE-MANIFEST.json'), encoding='utf-8'))
print('== SOURCE-MANIFEST type', type(sm).__name__)
if isinstance(sm, dict):
    print(list(sm.keys())[:10])
    items = sm.get('files', sm)
else:
    items = sm
if isinstance(items, dict):
    items = [dict(v, _key=k) if isinstance(v, dict) else {'_key': k, 'v': v} for k, v in items.items()]
print('first item', items[0] if items else None)
ok = bad = miss = 0
for it in items:
    rel = it.get('path') or it.get('package_path') or it.get('copy') or it.get('_key')
    sha = it.get('sha256')
    if rel is None or sha is None:
        continue
    p = os.path.join(root, rel)
    if not os.path.exists(p):
        miss += 1; print('SM MISSING', rel); continue
    if h(p, 'sha256') == sha:
        ok += 1
    else:
        bad += 1; print('SM MISMATCH', rel)
print('SOURCE-MANIFEST ok', ok, 'bad', bad, 'missing', miss)
