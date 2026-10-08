# SO [52,9,22] proof package — v3 (2026-10-08)

[PROOF.md](PROOF.md) gives the Japanese computer-assisted proof draft of
`d_SO(52,9)=20`, including a [52,9,20] generator matrix. The
[v2 integrated AI review](review/v2/C-final.md) resolved R1–R12 and requested
documentation and packaging fixes. This v3 addresses those fixes; v3 itself
has not been independently re-reviewed or formally verified.

The [16,7,6] classification is supported by the bundled systematic enumeration
and explicit permutation checks, **not by an assumption about Simonis's paper**.
The remaining external classification data are Kurz Table 1, `(51,8)=1` and
`(52,8)=0`; the [PDF](references/kurz.pdf) and [source record](references/SOURCES.md)
are included. The table has not been recomputed here.

## What was run for v3

Only [bounded checks](runs/v3-bounded-check/REPRODUCTION-V3.json) were run:
three small ambient-space exhaustive comparisons, 4,096 representatives for
each length-52 kernel, the known distance-20 coset of D0, the fixed q=0
certificate, and integrity checks of the archived evidence. The record says
`bounded_checks_passed: true` and `full_proof_reproduced: false`.
**No long scan or full [16,7,6] equivalence classification was rerun for v3.**
The historical complete scans remain the evidence for the length-52 result.

## Requirements and commands

Python >=3.10 is required. Full classification also needs NumPy >=2 and
NetworkX >=3 (see [requirements-v3.txt](requirements-v3.txt)). The direct scan
needs GCC with OpenMP, either installed locally or in an existing Docker
`gcc:14` image. Docker execution uses `--pull=never`, `--network=none`, and an
explicit CPU limit. The scripts do not install packages or download an image.

Run from this directory. This is the default, bounded mode:

```text
python reproduce.py --check --backend docker --threads 2
```

With native GCC, replace `--backend docker` by `--backend native`; use
`--compiler /path/to/gcc` if it is not on PATH. For a future **full** reproduction:

```text
python reproduce.py --full --backend docker --threads 16
```

The full mode can take many minutes. Historical original C runs with
`gcc:14` and 16 OpenMP threads took roughly 1–5 minutes per T=22 scan and
3–8 minutes for the D0 T=20 control; these are machine-dependent observations,
not timings of the new wrapper. The [16,7,6] equivalence stage also takes
minutes. Do not confuse the bounded mode with a proof reproduction.

To rerun only Section 7.1:

```text
python direct_scan.py --full --backend docker --threads 16
```

Every run creates a new directory under `runs/` (or a nonexistent directory
specified by `--out`). It preserves all historical results. Generated headers,
commands, input and source hashes, counts, and status are recorded there.
The new C wrapper requires `THRESHOLD START COUNT`; it never assumes a full
range when arguments are omitted. Full success is recorded only after all
expected counts match.

## Main proof and reproduction stages

1. [verify_q0_certificate.py](verify_q0_certificate.py) checks the fixed
   MacWilliams/Delsarte certificate `23 K1 + 4 K2 + K3 <= -72` on the eight
   possible nonzero weights. It performs no coefficient search or LP solve.
2. [classes16.py](evidence/agentA-v2/classes16.py) enumerates 28,718 sorted
   systematic forms and checks coordinate permutations to three representatives.
   `reproduce.py --full` runs the disjoint ranges `[0,7200)`, `[7200,14400)`,
   `[14400,21600)`, `[21600,28718)` and checks all completion lines. Its
   enumeration reuses B's method; the permutation check is independently written.
3. `residual36_cubics.py`, `exact36.py`, `exact40.py`,
   `normalized32_orbits.py`, and `normalized36_orbits.py` classify the kernels.
4. `audit_exact.py` checks their representatives and the lower-bound witness.
   It also reads preserved Section 7.2 results; those are not called freshly
   rerun unless `--legacy-cross-checks` was requested.
5. [direct_scan.py](direct_scan.py) regenerates quotient-basis headers from
   the three matrix files, compiles [scan_direct.c](scan_direct.c), and runs
   **D0, D1, D2 at T=22, plus D0 at T=20**. This is the Section 7.1 main path.
   The C wrapper is an adaptation with range bounds and small-code support;
   only its bounded tests were run during v3 preparation.

Expected full results (all `2^36` representatives per scan):

| Input | T | visited | even, 0 mod 4 | even, 2 mod 4 | accepted 0 mod 4 | accepted 2 mod 4 |
|---|---:|---:|---:|---:|---:|---:|
| D0 | 22 | 68,719,476,736 | 17,179,738,112 | 17,180,000,256 | 0 | 0 |
| D1 | 22 | 68,719,476,736 | 17,179,738,112 | 17,180,000,256 | 0 | 0 |
| D2 | 22 | 68,719,476,736 | 17,179,738,112 | 17,180,000,256 | 0 | 0 |
| D0 | 20 | 68,719,476,736 | 17,179,738,112 | 17,180,000,256 | 1,138,092,541 | 0 |

The even coverage counts are `2^34 - 2^17` and `2^34 + 2^17`, summing to
`2^35`. The 0 mod 4 T=22 cases are a cross-check of the q=0 certificate.

Section 7.2 (`triple_exhaustive.py`, `joint_switch_search.py`) is an optional
reflection/orbit cross-check, not the main final scan. To add it to a full run:

```text
python reproduce.py --full --backend docker --threads 16 --legacy-cross-checks
```

## Evidence and file conventions

- [evidence/INDEX.md](evidence/INDEX.md): complete source/log index and historical
  replay instructions, including the missing header-generation and T=20 steps.
- [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json): byte-identical archived sources,
  original locations and SHA-256 values. [verify_evidence.py](verify_evidence.py)
  verifies copies and named historical completion records without rerunning scans.
- [AUDIT.json](AUDIT.json): prior exact checks of representatives and lower bound.
- [REPRODUCTION.json](REPRODUCTION.json): **v1** full-run record, not a v3 run.
- [PROOF-v1-20261008.md](PROOF-v1-20261008.md) and
  [PROOF-v2-20261008.md](PROOF-v2-20261008.md): preserved previous documents.
- [V3-CHANGES.md](V3-CHANGES.md): added/changed file paths and disposition table.
- [MANIFEST.json](MANIFEST.json): current distributable files, SHA-256 and MD5.
  The old manifest, README and entry point are in [history/v2](history/v2/).

Matrix coordinates are numbered from zero, left to right; coordinate j is
integer bit j. Original reviewer files are preserved unchanged, so historical
`/w` paths, comments and incomplete logs retain their original meaning.
The portable entry points above do not require the old H: drive or temporary
scratchpad. `evidence/so52/` contains the three matrices needed by historical
`evidence/agentB/verify_orbits.py`'s `../so52` reference.

OR-Tools and pynauty are needed only for alternative historical experiments
(the bundled class52 Dockerfile specifies its environment). Historical UNKNOWN
results and incomplete classification logs are not nonexistence evidence.
The existing v1 ZIP is unchanged; this directory contains v3.
