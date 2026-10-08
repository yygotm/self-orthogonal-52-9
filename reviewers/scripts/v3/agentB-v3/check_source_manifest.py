import json, hashlib, os, sys
root=sys.argv[1]
def h(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()
sm=json.load(open(os.path.join(root,'SOURCE-MANIFEST.json'),encoding='utf-8'))
print('note:',sm.get('note'))
c=sm['copies']; print('copies',len(c))
ok=bad=miss=0; so=sb=sm_=0
for it in c:
    p=os.path.join(root,it['path'])
    if not os.path.exists(p): miss+=1; print('MISSING',it['path']); continue
    if h(p)==it['sha256']: ok+=1
    else: bad+=1; print('BAD',it['path'])
    s=it.get('source')
    if s and os.path.exists(s):
        if h(s)==it['sha256']: so+=1
        else: sb+=1; print('SOURCE CHANGED',it['path'],s)
    else: sm_+=1
print('copy ok',ok,'bad',bad,'missing',miss)
print('original source still present & equal',so,'differs',sb,'source not found',sm_)
