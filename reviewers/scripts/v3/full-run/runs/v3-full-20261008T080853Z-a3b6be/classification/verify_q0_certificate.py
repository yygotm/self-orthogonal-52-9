"""Verify the fixed O1 certificate exactly; no LP search or solver is run."""
import json
from math import comb


def krawtchouk(n, j, w):
    return sum((-1)**s * comb(w, s) * comb(n-w, j-s)
               for s in range(max(0, j-n+w), min(w, j)+1))


def verify():
    n=52
    weights=range(24,53,4)
    def f(w):
        return sum(a*krawtchouk(n,j,w) for a,j in [(23,1),(4,2),(1,3)])
    values={w:f(w) for w in weights}
    assert all(v<=-72 for v in values.values())
    assert f(0)==28600 and f(0)-72*511==-8192
    lower={0:1,20:51,24:204,28:204,32:51,52:1}
    assert sum(lower.values())==512
    dual_numerators=[sum(a*krawtchouk(n,j,w) for w,a in lower.items())
                     for j in range(n+1)]
    assert all(v>=0 and v%512==0 for v in dual_numerators)
    return {'certificate_verified':True,'coefficients':[23,4,1],
            'nonzero_weight_values':values,'value_at_zero':28600,
            'upper_bound':-8192,'lower_bound_code_positive_control':True,
            'solver_called':False}


if __name__=='__main__':
    print(json.dumps(verify(),sort_keys=True))
