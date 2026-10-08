# SO [52,9,22] investigation and proof package

The main document is **PROOF.md** (Japanese). It presents a computer-assisted
proof draft of nonexistence of binary Euclidean self-orthogonal [52,9,22]
codes, with an explicit [52,9,20] lower-bound witness.

The draft has not received independent external review. The mathematical
reductions are written out in PROOF.md; they are not machine-formalized.
The three-class [16,7,6] classification is cited from Simonis (1991), whose
publisher abstract was checked; its full proof was not accessed.

## Reproduction

Use Python 3.10 or newer and NumPy 2 or newer:

```text
python reproduce.py
```

The original run used Python 3.13 and NumPy 2.5.3. The final reproduction
pipeline does not call an optimization solver. `reassess.py` also adds the
original local package directory to Python's search path; on another machine
this nonexistent directory is harmless and installed NumPy is used normally.

Results are recorded in REPRODUCTION.json and reproduction-*.log.
AUDIT.json contains the witness checks and enumeration counts.

## Read first

- PROOF.md: coherent final argument and references.
- REPRODUCTION.json: completion and exit status of each final computation.
- AUDIT.json: exact checks, representatives, lower bound.
- D-representative-0.txt, -1.txt, -2.txt: the three kernel representatives.
- LOWER-52-9-20.txt: the nine-row lower-bound generator matrix.

All matrix files contain one binary row per line; coordinates are numbered
from zero from left to right. Scripts store coordinate j as integer bit j.

## Historical material

RESEARCH.md and the remaining files record unsuccessful searches and alternate
solver encodings. They include historical UNKNOWN results; those are not
used as nonexistence evidence. OR-Tools 9.15.6755 (including SCIP 10.0.0) is
only needed to rerun those alternative optimization experiments.

The final exact path is:

1. residual36_cubics.py + exact36.py: exclude the B/C residuals.
2. exact40.py: exclude both possible weight-40 residuals.
3. normalized32_orbits.py: classify the maximum-weight-32 kernel.
4. normalized36_orbits.py: classify the surviving weight-36 kernel.
5. triple_exhaustive.py: exclude extensions of the zero-coordinate kernel.
6. joint_switch_search.py: exclude extensions of both nonzero-coordinate kernels.
7. audit_exact.py: check representatives and the lower-bound witness.

MANIFEST.json records SHA-256 and MD5 for the packaged files. Archive hashes
are supplied in a separate text file beside the ZIP.
