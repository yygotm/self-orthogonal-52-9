"""Agent B: every element of the sec.6 seventh-row candidate set is valid
(all 64 words of r + <K,v> weigh 24 or 32) and distinct mod K; with the
independent count 10,752 (verify_32_7_count.py) this shows completeness."""
from verify_orbits import gen32, span, echelon, reduce_by
K, g, cand, root, ks, rep = gen32()
cw = span(K + [g]); kb = echelon(K)
bad = sum(1 for r in cand if not all((r ^ w).bit_count() in (24, 32) for w in cw))
print({"cand": len(cand), "invalid": bad, "distinct_mod_K": len({reduce_by(r, kb) for r in cand})})
