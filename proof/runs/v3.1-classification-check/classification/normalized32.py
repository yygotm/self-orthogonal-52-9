"""Complete normal-form search for a full-support kernel with max weight 32.
Uses the minimum-weight classification of RM(3,8); derivation in RESEARCH.md.
--kernel searches only the doubly-even kernel, otherwise the target C.
"""
from reassess import *
from ortools.sat.python import cp_model

def run(kernel=False):
    m=cp_model.CpModel();opts=[];xs=[]
    # K has each point outside a fixed 3-space twice, plus four zero columns.
    for p in range(8,32):
        for parity in range(2):
            oo=[p|(g<<5)|(b<<8) for g in range(8) if g.bit_count()%2==parity for b in range(1 if kernel else 2)]
            xx=[m.new_bool_var(f'x{len(xs)}_{v}') for v in oo]
            m.add_exactly_one(xx);opts.append(oo);xs.append(xx)
    for g in [1,2,4,7]:
        oo=[g<<5|b<<8 for b in range(1 if kernel else 2)];xx=[m.new_bool_var(f'x{len(xs)}_{v}') for v in oo]
        m.add_exactly_one(xx);opts.append(oo);xs.append(xx)
    # Add K rows to the 3 new rows and (optionally) to the extension row.
    m.add(xs[0][0]==1)
    for u in range(1,256 if kernel else 512):
        expr=sum(x for oo,xx in zip(opts,xs) for v,x in zip(oo,xx) if (u&v).bit_count()%2)
        if u<256:
            g=u>>5
            if g==7:m.add(expr==28)
            elif g:
                b=m.new_bool_var(f'w{u}');m.add(expr==24+8*b)
            # K weights are already 24 or 32.
        else:
            z=m.new_int_var(5,12,f'w{u}');m.add(expr==4*z+2)
    s=cp_model.CpSolver();s.parameters.max_time_in_seconds=120;s.parameters.num_workers=4
    st=s.solve(m);res={'kernel_only':kernel,'status':s.status_name(st),'seconds':s.wall_time}
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        cols=[next(v for v,x in zip(oo,xx) if s.value(x)) for oo,xx in zip(opts,xs)]
        rows=[sum((v>>i&1)<<j for j,v in enumerate(cols)) for i in range(8 if kernel else 9)]
        chk=inspect(rows,52);chk.pop('columns');assert chk['rank']==len(rows) and chk['so'] and chk['d']>= (24 if kernel else 22)
        res['check']=chk;fname='normalized32-kernel.txt' if kernel else 'SOLUTION-52-9-22.txt'
        (OUT/fname).write_text('\n'.join(''.join(str(r>>j&1) for j in range(52)) for r in rows)+'\n')
    (OUT/f'normalized32-{kernel}.json').write_text(json.dumps(res,indent=2));print(json.dumps(res),flush=True)

if __name__=='__main__':run('--kernel' in sys.argv)
