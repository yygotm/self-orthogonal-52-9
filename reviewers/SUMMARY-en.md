# Summary of the AI reviews (English)

Written 2026-10-09 by Claude (Anthropic) as a guide to the reports in this folder, which are in Japanese.
This is a summary, not a translation; where it and a report differ, the report is the record.

## Who reviewed

Three AI reviewer agents, A, B and C (Claude), in a session separate from the proof's author (GPT) and from the
independent computations in `independent/`. Each had a fixed role:

- A: the logical structure of the argument;
- B: the premises, definitions and cited theorems;
- C: search for counterexamples, and the combined verdict.

In rounds 1 and 2, A and B each wrote a first report and then assessed the other's report; round 3 was a lighter
round without the cross-assessment. C wrote the final report of each round.
The reviewers also wrote and ran their own programs; these are in `scripts/` as they were run (archival, not meant to
be rerun as is).

## Round 1: proof v1 (2026-10-08)

Reports: `A1.md`, `B1.md` (first reports), `A2.md`, `B2.md` (cross-assessment), `C3-final.md` (final).

Verdict: **revise.** The reviewers judged the mathematical conclusion correct but found the written argument
incomplete in places, and asked for changes to how external results are cited. Twelve items were requested (R1–R12):
four required revisions (the exhaustiveness of a candidate list in the weight-36 case; three missing steps in the
maximum-weight-32 case; replacing a cited uniqueness result by an internal argument; citing the right table of Kurz)
and eight minor ones. No counterexample was found.

## Round 2: proof v2 (2026-10-08, completed 15:57)

Reports: `v2/A1.md`, `v2/B1.md`, `v2/A2.md`, `v2/B2.md`, `v2/C-final.md`; progress log `v2/STATUS.md`.

Verdict: **revise (documentation only).** All twelve items R1–R12 were resolved, and no new mathematical error was
found, including in the parts new in v2. What remained needed no new mathematics: the code of the main-path coset scan
was not bundled with the proof, the README still described v1, the log of one equivalence check had not been kept,
and six minor citation and wording items. Reviewer C also proposed three optional changes (O1–O3); the author adopted two
of them in v3: a Delsarte linear-programming certificate that closes the doubly-even case without any classification or
table (O1), and a third implementation of the coset scan with a positive control (O2). O3, not adopted, was to replace
the use of Kurz's value (52,8)=0 in §6 by a short elementary projection-and-moment argument; with it, the only external
classification value left on the main path would be (51,8)=1.

## Round 3: proof v3 (2026-10-08, completed 17:07)

Reports: `v3/A1.md`, `v3/B1.md`, `v3/C-final.md`.

Verdict: **sound.** The three documentation items and six minor items of round 2 were resolved; the linear-programming
certificate and the third implementation were checked and found correct; no counterexample. Two minor wording items
(the reproduction script did not assert some counts that the text said it checks; one justification sentence had been
dropped) and five optional items remained. The author states that v3.1, the version in `proof/`, addresses all of them;
v3.1 has not been re-reviewed. After `v3/C-final.md` was written (it still says the full run had not been done), the
review session ran the proof's reproduction script on v3 end to end (`reproduce.py --full`, 16 threads, 2026-10-08
17:08–17:22): all 13 stages exited 0 and the record reports `full_proof_reproduced: true`
(`scripts/v3/full-run/runs/v3-full-20261008T080853Z-a3b6be/REPRODUCTION-V3.json`; the
short `v3/full-run.log` is only the start of its console output).

One limit noted in round 3: the two values taken from Kurz's Table 1 were not recomputed by the reviewers. They were
recomputed separately, outside these reports, from the independent classification in `independent/`
(`../README.md` section independent/, `../independent/logs/run_check.out`; see also `../proof/references/kurz-table1-check-1540.md`).
