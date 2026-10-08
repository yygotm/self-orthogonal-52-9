# Bundled evidence and historical replay

All files listed below are byte-for-byte copies. Their original paths, sizes,
and SHA-256 values are in [SOURCE-MANIFEST.json](../SOURCE-MANIFEST.json).
The source locations were read, never edited. Past incomplete logs are retained
as historical records, not upgraded into successful computations.

## Proof roles

| Directory | Role |
|---|---|
| agentC | Original complement-basis generator, cosets.c, three headers, unnamed original logs |
| named-rerun | Input-named reruns of cosets.c and ext52x.c, all six headers, T=22 and T=20 outputs |
| ext52x | Second original implementation, input matrices and full-run output |
| agentA-v2 | Third implementation scanA.c, headers, named outputs, and classes16.py with four completed shards |
| agentC-v2 | scanA's positive control and the exact q=0 LP discovery scripts/logs |
| agentB | Systematic-form enumeration, independent row-count checks and orbit-equivalence checks |
| agentB-v2 | Repeated systematic-form count and an INCOMPLETE equivalence rerun |
| agentA | Row-count checks and modular-lifting checks |
| class52 | Alternative CP-SAT/pynauty classification and completion log |
| so52 | Three unmodified representatives for agentB scripts using ../so52 |

The [four classes16 logs](agentA-v2/) cover [0,7200), [7200,14400),
[14400,21600), [21600,28718). Enumeration reuses B's code; the equivalence
check is A2's independently written part. The incomplete
[classify16_7_6.rerun.log](agentB-v2/classify16_7_6.rerun.log) is NOT the
upper-bound proof of three classes.

The old C logs do not identify the two D inputs by name. Input attribution
is supported by the files in named-rerun and by scanA's named outputs, not
by an inference from regenerating a header alone.

## Replay the three original direct implementations

The portable v3.1 entry point is `python reproduce.py --full ...`; see
[README](../README.md). The following optional Bash commands replay the
**unchanged original implementations**, on a system with Python and GCC/OpenMP.
They include header generation and the T=20 control commands absent from some
historical shell scripts. These are reconstructed reproducible commands,
not claims that the incomplete historical shell scripts contained them.
They launch long scans; they were NOT run during v3 preparation.
Run from the package root, using a fresh output directory:

```bash
mkdir -p runs/original-replay
cd runs/original-replay
export OMP_NUM_THREADS=16
for i in 0 1 2; do
  python ../../evidence/agentC/gen_hdr.py ../../D-representative-$i.txt h$i.h
  python ../../evidence/ext52x/gen.py ../../D-representative-$i.txt basis-gpt$i.h
  python ../../evidence/agentA-v2/mkbasis.py ../../D-representative-$i.txt hA$i.h
  gcc -O3 -march=native -fopenmp -I. -DHDR="\"h$i.h\"" ../../evidence/agentC/cosets.c -o cos$i
  gcc -O3 -march=native -fopenmp -I. -DBASIS="\"basis-gpt$i.h\"" ../../evidence/ext52x/ext52x.c -o ext$i
  gcc -O3 -march=native -fopenmp -I. -DHDR="\"hA$i.h\"" ../../evidence/agentA-v2/scanA.c -o scan$i
  ./cos$i 22 > cos$i-22.out
  ./ext$i 22 > ext$i-22.out
  ./scan$i 22 > scan$i-22.out
done
./cos0 20 > cos0-20.out
./ext0 20 3 > ext0-20.out
./scan0 20 > scan0-20.out
```

All T=22 accepted counts must be zero. At T=20, `cosets.c` and `scanA.c`
report 1,138,092,541 on the 0 mod 4 side and zero on the 2 mod 4 side.
`ext52x.c` reports only the **combined accepted total 1,138,092,541**;
it does not print the two mod 4 counts separately. `scanA.c` additionally
reports coverage counts 17,179,738,112 and 17,180,000,256.

The archived LP scripts include coefficient searches; do not run lp_cert.py
as a quick test. [verify_q0_certificate.py](../verify_q0_certificate.py)
checks the fixed certificate without that search. The class52 alternative
uses its own [Dockerfile](class52/Dockerfile); it is not part of the solver-free
main reproduction pipeline.

## Copied source inventory

- [agentC/cosets.c](agentC/cosets.c) (1806 bytes)
- [agentC/gen_hdr.py](agentC/gen_hdr.py) (2607 bytes)
- [agentC/h0.h](agentC/h0.h) (5387 bytes)
- [agentC/h1.h](agentC/h1.h) (5402 bytes)
- [agentC/h2.h](agentC/h2.h) (5402 bytes)
- [agentC/run_d0_20.log](agentC/run_d0_20.log) (99 bytes)
- [agentC/run_d12_22.log](agentC/run_d12_22.log) (180 bytes)
- [named-rerun/basis-gpt0.h](named-rerun/basis-gpt0.h) (5719 bytes)
- [named-rerun/basis-gpt1.h](named-rerun/basis-gpt1.h) (5752 bytes)
- [named-rerun/basis-gpt2.h](named-rerun/basis-gpt2.h) (5738 bytes)
- [named-rerun/cos0-20.out](named-rerun/cos0-20.out) (99 bytes)
- [named-rerun/cos0-22.out](named-rerun/cos0-22.out) (90 bytes)
- [named-rerun/cos1-22.out](named-rerun/cos1-22.out) (90 bytes)
- [named-rerun/cos2-22.out](named-rerun/cos2-22.out) (90 bytes)
- [named-rerun/cosets.c](named-rerun/cosets.c) (1806 bytes)
- [named-rerun/D0.txt](named-rerun/D0.txt) (432 bytes)
- [named-rerun/D1.txt](named-rerun/D1.txt) (432 bytes)
- [named-rerun/D2.txt](named-rerun/D2.txt) (432 bytes)
- [named-rerun/ext0-20.out](named-rerun/ext0-20.out) (115 bytes)
- [named-rerun/ext0-22.out](named-rerun/ext0-22.out) (46 bytes)
- [named-rerun/ext1-22.out](named-rerun/ext1-22.out) (46 bytes)
- [named-rerun/ext2-22.out](named-rerun/ext2-22.out) (46 bytes)
- [named-rerun/ext52x.c](named-rerun/ext52x.c) (1708 bytes)
- [named-rerun/gen.py](named-rerun/gen.py) (2424 bytes)
- [named-rerun/gen_hdr.py](named-rerun/gen_hdr.py) (2607 bytes)
- [named-rerun/h0.h](named-rerun/h0.h) (5387 bytes)
- [named-rerun/h1.h](named-rerun/h1.h) (5402 bytes)
- [named-rerun/h2.h](named-rerun/h2.h) (5402 bytes)
- [named-rerun/run_all.sh](named-rerun/run_all.sh) (446 bytes)
- [named-rerun/times.txt](named-rerun/times.txt) (165 bytes)
- [ext52x/basis-gpt1.h](ext52x/basis-gpt1.h) (5752 bytes)
- [ext52x/D-gpt0.txt](ext52x/D-gpt0.txt) (432 bytes)
- [ext52x/D-gpt1.txt](ext52x/D-gpt1.txt) (432 bytes)
- [ext52x/D-gpt2.txt](ext52x/D-gpt2.txt) (432 bytes)
- [ext52x/d20-gpt0.out](ext52x/d20-gpt0.out) (119 bytes)
- [ext52x/d20.out](ext52x/d20.out) (115 bytes)
- [ext52x/d22-gpt0.out](ext52x/d22-gpt0.out) (47 bytes)
- [ext52x/d22-gpt1.out](ext52x/d22-gpt1.out) (47 bytes)
- [ext52x/d22-gpt2.out](ext52x/d22-gpt2.out) (47 bytes)
- [ext52x/ext52x.c](ext52x/ext52x.c) (1708 bytes)
- [ext52x/gen.py](ext52x/gen.py) (2424 bytes)
- [ext52x/run_gpt.sh](ext52x/run_gpt.sh) (226 bytes)
- [agentA-v2/check_headers.log](agentA-v2/check_headers.log) (768 bytes)
- [agentA-v2/check_headers.py](agentA-v2/check_headers.py) (1669 bytes)
- [agentA-v2/checks_a2.log](agentA-v2/checks_a2.log) (603 bytes)
- [agentA-v2/checks_a2.py](agentA-v2/checks_a2.py) (3686 bytes)
- [agentA-v2/classes16-0.log](agentA-v2/classes16-0.log) (429 bytes)
- [agentA-v2/classes16-14400.log](agentA-v2/classes16-14400.log) (403 bytes)
- [agentA-v2/classes16-21600.log](agentA-v2/classes16-21600.log) (438 bytes)
- [agentA-v2/classes16-7200.log](agentA-v2/classes16-7200.log) (437 bytes)
- [agentA-v2/classes16.py](agentA-v2/classes16.py) (3634 bytes)
- [agentA-v2/hA0.h](agentA-v2/hA0.h) (772 bytes)
- [agentA-v2/hA1.h](agentA-v2/hA1.h) (774 bytes)
- [agentA-v2/hA2.h](agentA-v2/hA2.h) (775 bytes)
- [agentA-v2/mkbasis.py](agentA-v2/mkbasis.py) (1871 bytes)
- [agentA-v2/run_scanA.sh](agentA-v2/run_scanA.sh) (347 bytes)
- [agentA-v2/scanA-times.txt](agentA-v2/scanA-times.txt) (93 bytes)
- [agentA-v2/scanA.c](agentA-v2/scanA.c) (1548 bytes)
- [agentA-v2/scanA0-22.out](agentA-v2/scanA0-22.out) (116 bytes)
- [agentA-v2/scanA1-22.out](agentA-v2/scanA1-22.out) (116 bytes)
- [agentA-v2/scanA2-22.out](agentA-v2/scanA2-22.out) (116 bytes)
- [agentC-v2/hA0.h](agentC-v2/hA0.h) (772 bytes)
- [agentC-v2/lp_cert.log](agentC-v2/lp_cert.log) (605 bytes)
- [agentC-v2/lp_cert.py](agentC-v2/lp_cert.py) (959 bytes)
- [agentC-v2/lp_exact.log](agentC-v2/lp_exact.log) (372 bytes)
- [agentC-v2/lp_exact.py](agentC-v2/lp_exact.py) (3017 bytes)
- [agentC-v2/lp_exact_ctrl.log](agentC-v2/lp_exact_ctrl.log) (174 bytes)
- [agentC-v2/lp_exact_ctrl.py](agentC-v2/lp_exact_ctrl.py) (813 bytes)
- [agentC-v2/lp_minimal.log](agentC-v2/lp_minimal.log) (112 bytes)
- [agentC-v2/lp_minimal.py](agentC-v2/lp_minimal.py) (693 bytes)
- [agentC-v2/pos-docker.log](agentC-v2/pos-docker.log) (223 bytes)
- [agentC-v2/pos-times.txt](agentC-v2/pos-times.txt) (18 bytes)
- [agentC-v2/run_pos.sh](agentC-v2/run_pos.sh) (179 bytes)
- [agentC-v2/scanA.c](agentC-v2/scanA.c) (1548 bytes)
- [agentC-v2/scanA0-20.out](agentC-v2/scanA0-20.out) (125 bytes)
- [agentB/a7_s3.log](agentB/a7_s3.log) (117 bytes)
- [agentB/a7_s5.log](agentB/a7_s5.log) (117 bytes)
- [agentB/check_cand32_valid.py](agentB/check_cand32_valid.py) (535 bytes)
- [agentB/classify16_7_6.py](agentB/classify16_7_6.py) (4952 bytes)
- [agentB/count_all16.py](agentB/count_all16.py) (1285 bytes)
- [agentB/cubic_check.py](agentB/cubic_check.py) (1131 bytes)
- [agentB/parseval40.py](agentB/parseval40.py) (2367 bytes)
- [agentB/th_equiv.py](agentB/th_equiv.py) (2211 bytes)
- [agentB/verify_32_7_count.py](agentB/verify_32_7_count.py) (2017 bytes)
- [agentB/verify_A7_count.py](agentB/verify_A7_count.py) (2884 bytes)
- [agentB/verify_orbits.py](agentB/verify_orbits.py) (7482 bytes)
- [agentB/vo32.log](agentB/vo32.log) (1032 bytes)
- [agentB/vo36.log](agentB/vo36.log) (576 bytes)
- [agentB-v2/classify16_7_6.rerun.log](agentB-v2/classify16_7_6.rerun.log) (118 bytes)
- [agentB-v2/count_all16.rerun.log](agentB-v2/count_all16.rerun.log) (217 bytes)
- [agentB-v2/verify_headers.log](agentB-v2/verify_headers.log) (1127 bytes)
- [agentB-v2/verify_headers.py](agentB-v2/verify_headers.py) (3907 bytes)
- [agentA/c_shard0.log](agentA/c_shard0.log) (327 bytes)
- [agentA/c_shard1.log](agentA/c_shard1.log) (327 bytes)
- [agentA/c_shard2.log](agentA/c_shard2.log) (327 bytes)
- [agentA/check_cubics.py](agentA/check_cubics.py) (8373 bytes)
- [agentA/check_rows.py](agentA/check_rows.py) (4967 bytes)
- [agentA/check_zerocol.py](agentA/check_zerocol.py) (902 bytes)
- [class52/classify.py](class52/classify.py) (5556 bytes)
- [class52/Dockerfile](class52/Dockerfile) (199 bytes)
- [class52/lift.c](class52/lift.c) (2146 bytes)
- [class52/log16-7.txt](class52/log16-7.txt) (1679 bytes)
- [so52/D-representative-0.txt](so52/D-representative-0.txt) (432 bytes)
- [so52/D-representative-1.txt](so52/D-representative-1.txt) (432 bytes)
- [so52/D-representative-2.txt](so52/D-representative-2.txt) (432 bytes)

## Evidence added for v3.1

- [v3 integrated review](../review/v3/C-final.md), [A1](../review/v3/A1.md),
  [B1](../review/v3/B1.md): unchanged review documents. The Kurz recalculation
  supplement below updates the scope of the integrated report without editing it.
- [B's D0 T=20 log](agentB-v3/full-d0-t20.log) and
  [B's three T=22 logs](agentB-v3/full-t22.log): full C binary runs on
  2026-10-08, with range counts and timings. B used binaries generated during
  [bounded reproduction](agentB-v3/repro-check/direct/DIRECT-REPRODUCTION.json);
  these are not logs of `reproduce.py --full` or `direct_scan.py --full`.
- [C's coverage derivation](agentC-v3/coverage_macwilliams.py) and
  [output](agentC-v3/coverage_macwilliams.log): exact MacWilliams computation,
  rerun in [v3.1 bounded checks](../runs/v3.1-classification-check/coverage.log).
- [C's classification replay summary](agentC-v3/classify-summary.log):
  successful component runs described in the v3 integrated review.
- [Claude's Kurz table check, 2026-10-08 15:40](../references/kurz-table1-check-1540.md)
  and [aggregation script](kurz/kurzcheck.py): independent stage1/stage2
  classification agreement, reported by Claude. The underlying classification
  pickle inputs are not bundled or rerun for v3.1; this is supporting evidence,
  not a replacement for the published table in the proof.

All copied files, including pre-edit snapshots in `history/v3/`, are recorded
with their original paths and hashes in SOURCE-MANIFEST.json. The replay
instructions above remain long-running commands and were not run for v3.1.
