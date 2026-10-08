# d_SO(52,9) = 20: proof package and independent checks

Assembled 2026-10-08 by Claude (Anthropic). Nothing here has been reviewed by a human expert yet.

The claim: the largest minimum distance of a binary self-orthogonal [52,9] code is 20.
The proof was written by GPT (OpenAI Codex) and revised three times after reviews by three AI reviewers.
The classification it uses (all doubly-even [52,8,24] codes) was recomputed by a separate program written by Claude.

## Layout

| folder | what | origin |
|---|---|---|
| `proof/` | the proof, version 3.1 (`PROOF.en.md`; translated from the Japanese `PROOF.md`, whose version 3 was reviewed; 3.1 has not been re-reviewed), its scripts, evidence, run records and Lean files (`proof/lean/`) | copy of GPT's package, see below |
| `independent/` | Claude's classification of doubly-even [52,8,>=24] codes and the extension scan | written by Claude, separately from `proof/` |
| `reviewers/` | reports of the three AI reviewers (A, B, C, in Japanese; English summary `SUMMARY-en.md`) and the scripts they ran | archival |
| `logs/proof-v3.1-full/` | record of `reproduce.py --full` on version 3.1 | run by Claude, see below |

`MANIFEST.sha256` lists the SHA-256 of every other file (`sha256sum -c MANIFEST.sha256`).
Everything here is under the MIT License (`LICENSE`). Cited papers are not included; see `proof/references/SOURCES.md`.

## proof/

Copied on 2026-10-09 from GPT's working folder; `PROOF.en.md` SHA-256 `2d1cc578ed706e0fa58106919e38d45969508d6f78103e9b2afc631bf2512fba`,
`PROOF.md` SHA-256 `21b6e7a06fb6a0a5a7d4bc280b0031ade81afb436ae083fb6b6ac9ac9b1fddd5`.
Read `proof/README.md` first. Two differences from the source:

- **`references/kurz.pdf` is not included** (copyright). Download it from <https://d-nb.info/1223982076/34>
  (S. Kurz, *Classification of 8-divisible binary linear codes with minimum distance 24*) and save it as
  `proof/references/kurz.pdf`. Its SHA-256 must be `12a3ff326167fc2db86c80c3006d5f070cfd56b425796784ce37f2f0efdaf734`.
  Without it, `reproduce.py` stops at its first step (`evidence`), which checks the source copies listed in `SOURCE-MANIFEST.json`.
- Other PDFs and downloaded texts used by the reviewers are also left out.

Checks (Python 3 with NumPy and NetworkX on the host, see `proof/requirements-v3.txt`; GCC in the `gcc:14` Docker image):

```
cd proof
python reproduce.py --check --backend docker --threads 4     # under a minute
python reproduce.py --full  --backend docker --threads 16    # about 8 minutes (16 threads)
```

Results: `--check` of version 3.1 gave `bounded_checks_passed: true` in each recorded run
(`proof/runs/v3.1-check-*`, 2026-10-08 and 2026-10-09). `--full` of version 3 was run by the review session from 17:08 to 17:22
(`reviewers/scripts/v3/full-run/runs/v3-full-20261008T080853Z-a3b6be/REPRODUCTION-V3.json`: all 13 stages passed, `full_proof_reproduced: true`). Version 3.1 strengthened the assertions, changed how the classification
stage stages its inputs and finds its dependencies, and clarified the text; the classification algorithms and the C
scanner were unchanged (`proof/V3.1-CHANGES.md`). The author reran its classification stage (`proof/runs/v3.1-classification-check/`). `--full` of version 3.1
was run by Claude on 2026-10-09 from 01:21 to 01:29 JST (16 threads, Python 3.13 with NumPy 2.5.3 and NetworkX 3.7,
on a copy with the PDF restored): all 13 stages passed, `full_proof_reproduced: true`. The record is in
`logs/proof-v3.1-full/`, with local paths shortened to `<proof>` and `<venv>`.

## independent/

Programs (Python 3.12, OR-Tools CP-SAT, pynauty; C with OpenMP), all in one Docker image:

- `class52/classify.py`: all [n,k,>=d] codes by residual lifting; isomorphism by a nauty canonical form.
  Produces S = doubly-even [n,6,>=24] codes of full support for n = 48, 49, 50: 1, 4, 117 classes.
- `class52/shorten.py`: from all codes of one length and dimension to the next by adding a coordinate and a row
  (uses `ext52x/extS.c` for the coset scan). S -> T51 (59 classes of doubly-even [51,7,>=24]) -> D52 (3 classes).
- `class52/brute_check.py`: classify.py against brute force on small parameters.
- `ext52x/ext52x.c`: for each of the three [52,8,24] codes D, scans all 2^36 cosets for a ninth row giving
  minimum distance 22. None for any D. The same program with d = 20 finds words (control).
- `kurz/kurzcheck.py`: lists the 8-divisible codes among the data; used for an independent check of Kurz's Table 1
  rows k=8, n=51 and n=52 (`proof/references/kurz-table1-check-1540.md`).
- `data/`: the computed lists, as JSON (each code is a list of rows; a row is an integer whose bit j is coordinate j).
  They were first saved as Python pickles; `data/FROM-PICKLE.json` records each pickle's SHA-256 and the count.
- `logs/`: output of the original runs on 2026-10-08 (times in UTC, JST = UTC+9: stage 1 03:17 to about 05:50, stage 2 05:51 onward),
  and `logs/run_check.out`.

```
cd independent
docker build -t so52-indep class52
docker run --rm -v "$PWD:/w" -w /w so52-indep sh run_check.sh    # about 80 seconds
docker run --rm -v "$PWD:/w" -w /w so52-indep sh run_full.sh     # about 3 hours with 16 threads
```

`run_check.sh` checks the data (doubly-even, d >= 24, pairwise inequivalent, the counts, the weight distributions of
the three [52,8,24] codes, and that GPT's three representatives `ext52x/D-gpt*.txt` are equivalent to them), runs the
brute-force comparison and a small shortening case with a known answer, recomputes S for n = 48 and 49, and
regenerates the scan headers. It passed on 2026-10-08 (`logs/run_check.out`).
`run_full.sh` recomputes everything from nothing and compares with `data/`. It passed on 2026-10-08, run from this
folder (read-only) with 16 threads from 18:19 to 21:16 JST (`logs/run_full/`; times inside are UTC): S 1, 4, 117;
T51 59; D52 3, all equal to `data/`; no [52,9,>=22] extension of any of the three; the d=20 control accepted
1,138,092,541 coset representatives. The first computation, run piece by piece earlier that day, is in `logs/class52/`.

Weight distributions of the three classes (all with 255 nonzero words):
D0 24^204 32^51; D1 24^172 28^32 32^51; D2 24^174 28^30 32^49 36^2.

## reviewers/

`A1.md` ... `C3-final.md` are the review reports. `scripts/` and `v2/`, `v3/` hold the scripts and logs the reviewers ran,
as they were, except that local paths are shortened to `<home>` and `<repo>`, session ids to `<session>`, and copies of
the Kurz paper text the reviewers extracted are removed. They are not meant to be rerun as is.

## What is not established

- No human expert has checked the proof.
- Lean 4 formalizes only parts (the explicit [52,9,20] lower-bound code; the exclusion of weights 44, 48 and 52; necessary
  conditions in the weight-40 case), see `proof/lean/README.md`. The q=0 certificate, the weight-40 exclusion, the
  classification and the extension scan are not formalized. The Lean build was not rerun for this package.
- The proof uses two entries of Kurz's published Table 1, (51,8)=1 in §3.2 and (52,8)=0 in §6; the independent recomputation
  covers the rows used.
