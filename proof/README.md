# SO [52,9,22] proof package — v3.1 (2026-10-08)

[PROOF.en.md](PROOF.en.md) is the authoritative English text; [PROOF.md](PROOF.md) is the Japanese source text; version 3 was reviewed, and version 3.1 incorporates the responses but has not been re-reviewed.
If the two versions differ, verify the mathematical content against the Japanese source text.

[PROOF.md](PROOF.md) gives the Japanese computer-assisted proof draft of
`d_SO(52,9)=20`, including a [52,9,20] generator matrix. The
[v3 integrated AI review](review/v3/C-final.md) judged the proof complete,
with no counterexample or new mathematical error, and resolved D1–D3/M1–M6.
This revision addresses its C-1–C-7 comments. That is an AI review outcome;
v3.1 has not itself been re-reviewed, and the complete proof has not been formally verified.
The [Lean supplement](lean/README.md) contains the lower-bound construction and selected lemmas,
with pinned versions, build instructions, and historical successful build records.

The [16,7,6] classification is supported by the bundled systematic enumeration
and explicit permutation checks, **not by an assumption about Simonis's paper**.
The remaining external classification data are Kurz Table 1, `(51,8)=1` and
`(52,8)=0`; the [PDF](references/kurz.pdf) and [source record](references/SOURCES.md)
are included. An [independent recomputation reported by Claude on 2026-10-08](references/kurz-table1-check-1540.md)
agrees with both values. Its stage1/stage2 classification was not rerun or
audited for completeness during this revision; the main proof retains the
published-table citation. The aggregation code is included, but its input
classification pickle files are not.

## Execution records and their scope

During v3 preparation, only [bounded checks](runs/v3-bounded-check/REPRODUCTION-V3.json) were run:
three small ambient-space exhaustive comparisons, 4,096 representatives for
each length-52 kernel, the known distance-20 coset of D0, the fixed q=0
certificate, and integrity checks of the archived evidence. The record says
`bounded_checks_passed: true` and `full_proof_reproduced: false`.
During the v3 review, [reviewer B](review/v3/B1.md) ran the generated C
binaries over the full `2^36` range for all four expected cases, with exact
agreement: [D0 T=20](evidence/agentB-v3/full-d0-t20.log),
[D0/D1/D2 T=22](evidence/agentB-v3/full-t22.log). These were direct C binary
invocations, not an end-to-end `reproduce.py --full` run or a recorded
`direct_scan.py --full` run. Reviewer C separately reran the classification
and audit stages, as described in the integrated review.

For v3.1, [fresh classification and gate checks](runs/v3.1-classification-check/CHECK-V3.1.json)
passed: the five classification scripts and audit completed in a fresh work
directory, with one orbit and one class in each branch; all three matrices
and the lower-bound witness were byte-identical. Regression checks reject
extra orbits/classes, missing outputs/members, duplicate members, wrong counts,
UNKNOWN status, and unexpected solutions. These checks took about 10 seconds
and disabled OR-Tools imports during classification.
The [bounded scan checks](runs/v3.1-bounded-check/REPRODUCTION-V3.1.json) also
passed with `full_proof_reproduced: false`.
**No length-52 full scan, full [16,7,6] equivalence classification, or legacy
reflection search was run during the v3.1 revision.**

## Requirements and commands

Python >=3.10 is required. Full classification also needs NumPy >=2 and
NetworkX >=3 (see [requirements-v3.txt](requirements-v3.txt), unchanged for v3.1).
`reassess.py` now uses the selected Python environment without injecting an
author-specific package path; the original is in [history/v3](history/v3/).
The direct scan
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
3–8 minutes for the D0 T=20 control. Reviewer B measured the new range-capable
C binary on 2026-10-08 at about 55–57 seconds per T=22 scan and 133 seconds
for D0 T=20, also with `gcc:14` and 16 threads. These are machine-dependent
reviewer observations, not measurements from v3.1 preparation. The [16,7,6]
equivalence stage takes about 18–19 minutes for four sequential shards in
the historical environment. As of the v3.1 revision, no end-to-end `reproduce.py --full` run was claimed.
Subsequent successful v3 and v3.1 full runs are recorded in the execution-update footnote in
[PROOF.en.md §9](PROOF.en.md#9-scope-and-limitations-of-reproduction-and-verification).
Do not confuse the bounded mode with a proof reproduction.

To rerun only Section 7.1:

```text
python direct_scan.py --full --backend docker --threads 16
```

Every run creates a new directory under `runs/` (or a nonexistent directory
specified by `--out`). It preserves all historical results. Generated headers,
commands, input and source hashes, counts, and status are recorded there.
The new C wrapper requires `THRESHOLD START COUNT`; it never assumes a full
range when arguments are omitted. Full success is recorded only after the
four classes16 completion checks, the explicit classification checks below,
the audit and regenerated-matrix checks, and all direct-scan coverage/accepted
counts pass. This does not claim automatic verification of every number
appearing in the mathematical narrative.

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
   The work directory starts with Python code and the three `residual16-*.txt`
   inputs only; existing classification JSON and generated matrices are not copied.
   The entry point then requires one first-row orbit and one second-row class
   in each normalized branch, first/second candidate counts 5,376/36 and
   10,752/24 (raw 344,064 in the latter), and complete class membership without
   duplicates. It also requires 49 models / 5,318 candidates / no solution for
   `exact36`, and two branches / four cases / 8,448 candidates / no solution
   for `exact40`. Missing data or mismatches fail before full success is recorded.
4. `audit_exact.py` checks their representatives and the lower-bound witness.
   Its archived Section 7.2 input `joint-switch-full-0.jsonl` is copied separately;
   it is not called freshly rerun unless `--legacy-cross-checks` was requested.
5. [direct_scan.py](direct_scan.py) regenerates quotient-basis headers from
   the three matrix files, compiles [scan_direct.c](scan_direct.c), and runs
   **D0, D1, D2 at T=22, plus D0 at T=20**. This is the Section 7.1 main path.
   The C wrapper is an adaptation with range bounds and small-code support;
   only its bounded tests were run during v3 and v3.1 preparation; reviewer B's
   full runs are separately identified above.

Expected full results (all `2^36` representatives per scan):

| Input | T | visited | even, 0 mod 4 | even, 2 mod 4 | accepted 0 mod 4 | accepted 2 mod 4 |
|---|---:|---:|---:|---:|---:|---:|
| D0 | 22 | 68,719,476,736 | 17,179,738,112 | 17,180,000,256 | 0 | 0 |
| D1 | 22 | 68,719,476,736 | 17,179,738,112 | 17,180,000,256 | 0 | 0 |
| D2 | 22 | 68,719,476,736 | 17,179,738,112 | 17,180,000,256 | 0 | 0 |
| D0 | 20 | 68,719,476,736 | 17,179,738,112 | 17,180,000,256 | 1,138,092,541 | 0 |

The even coverage counts are `2^34 - 2^17` and `2^34 + 2^17`, summing to
`2^35`. Every coset has constant weight modulo 4, so the two counts can be
derived independently from the dual weight distribution by the MacWilliams
identity and division by 256; see PROOF Section 7.1 and the
[integer calculation](evidence/agentC-v3/coverage_macwilliams.py).
The 0 mod 4 T=22 cases are a cross-check of the q=0 certificate: for a
hypothetical doubly-even [52,9,>=24] code C, any eight-dimensional subcode D
has minimum distance 24 by Griesmer, and C minus D is a coset with all weights
0 mod 4 and at least 24. It therefore appears in that column (PROOF Section 3.1).

To test the v3.1 classification success gate without scans or NumPy:

```text
python -B test_reproduction_checks.py
```

Section 7.2 (`triple_exhaustive.py`, `joint_switch_search.py`) is an optional
reflection/orbit cross-check, not the main final scan. To add it to a full run:

```text
python reproduce.py --full --backend docker --threads 16 --legacy-cross-checks
```

## Evidence and file conventions

- [evidence/INDEX.md](evidence/INDEX.md): complete source/log index and historical
  replay instructions, including the missing header-generation and T=20 steps.
- [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json): archived sources with distribution cleanup,
  anonymized provenance, current SHA-256 values, and preserved earlier hashes. [verify_evidence.py](verify_evidence.py)
  verifies copies and named historical completion records without rerunning scans.
- [AUDIT.json](AUDIT.json): prior exact checks of representatives and lower bound.
- [REPRODUCTION.json](REPRODUCTION.json): **v1** full-run record, not a v3 run.
- [PROOF-v1-20261008.md](PROOF-v1-20261008.md) and
  [PROOF-v2-20261008.md](PROOF-v2-20261008.md), plus
  [PROOF-v3-20261008.md](PROOF-v3-20261008.md): preserved previous documents.
- [V3-CHANGES.md](V3-CHANGES.md): added/changed file paths and disposition table.
- [V3.1-CHANGES.md](V3.1-CHANGES.md): this revision's C-1–C-7 dispositions,
  paths and bounded verification results.
- [MANIFEST.json](MANIFEST.json): current distributable files, SHA-256 and MD5.
  Previous snapshots are in [history/v2](history/v2/) and [history/v3](history/v3/).

Matrix coordinates are numbered from zero, left to right; coordinate j is
integer bit j. Included historical copies have conversational endings and internal
identifiers removed for distribution; external originals were not modified. Mathematical
content, executable proof and computation code, seeds, and recorded numerical results are
preserved. Historical `/w` paths and incomplete logs retain their original context.
The two historical package-check JSON reports use `relative_links_checked` and
`missing_relative_links` as descriptive field names; their values are unchanged.
See [PUBLICATION-CHECK.json](PUBLICATION-CHECK.json) for the cleanup and verification record.
The portable entry points above do not require the old H: drive or temporary
scratchpad. `evidence/so52/` contains the three matrices needed by historical
`evidence/agentB/verify_orbits.py`'s `../so52` reference.

OR-Tools and pynauty are needed only for alternative historical experiments
(the bundled class52 Dockerfile specifies its environment). Historical UNKNOWN
results and incomplete classification logs are not nonexistence evidence.
The existing v1 ZIP is unchanged; this directory contains v3.1.
