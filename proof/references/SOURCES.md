# Included external reference

- Author: Sascha Kurz.
- Title: *Classification of 8-divisible binary linear codes with minimum distance 24*.
- Local copy: [kurz.pdf](kurz.pdf).
- Source URL: <https://d-nb.info/1223982076/34>.
- Original review acquisition date: 2026-10-08, as documented in the review materials.
- Copied into this package: 2026-10-08, from the reviewer's preserved download.
- SHA-256: `12a3ff326167fc2db86c80c3006d5f070cfd56b425796784ce37f2f0efdaf734`.
- Used result: Section 2, Table 1, PDF page 4; k=8 at n=51 and n=52.

The original caption and surrounding text say "minimum distance 24".
The k=1 entries at lengths 32, 40 and 48 suggest a reading that includes
minimum distances at least 24; this is an interpretation of the table, not a
verbatim definition. For the entries used here (k=8, n<=54), either reading
gives the same count: an 8-divisible code with minimum distance above 24
would have distance at least 32, whose Griesmer bound is 65.

The published values remain the classification input to the main proof.
There is also an [independent recomputation report by Claude, 2026-10-08](kurz-table1-check-1540.md),
recorded at 15:40, and the [aggregation code](../evidence/kurz/kurzcheck.py).
It reports agreement of stage1/stage2 classifications with (51,8)=1 and
(52,8)=0, as well as the stated k=6,7 entries. This revises the scope of
the v3 integrated review's statement that nobody had recomputed those values.
The review itself is preserved unchanged. The underlying classification
pickle inputs are not included, and stage1/stage2 were not rerun or audited
for completeness during the v3.1 revision; no external dependency is silently
removed on the strength of that report.
