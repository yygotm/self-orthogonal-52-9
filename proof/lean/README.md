# Lean supplement: lower bound and selected lemmas

This directory contains the existing So52 formalization: 21 Lean source files,
pinned dependencies, and historical build evidence. It does **not** formalize
the complete nonexistence proof or the equality `d_SO(52,9)=20`.
The main text is [PROOF.en.md](../PROOF.en.md); the Japanese
[PROOF.md](../PROOF.md) is the Japanese source text; version 3 was reviewed,
and version 3.1 incorporates the responses but has not been re-reviewed.

## Versions and build

- Lean: **4.34.1**, pinned by [lean-toolchain](lean-toolchain).
- Mathlib: **v4.34.1**, commit
  `d13f23b723b8a846827a245b89c10fc7d3f11612`.
- [lake-manifest.json](lake-manifest.json) locks Mathlib and its transitive
  dependencies. Keep it together with [lakefile.toml](lakefile.toml).

With Git and the Lean toolchain manager (elan) installed, run the following
from this directory:

```text
lake --version
lake exe cache get
lake build
```

The first setup needs network access to obtain the pinned dependencies and
Mathlib cache. `lake build` builds the default target **So52**, importing all
bundled modules through [So52.lean](So52.lean). The explicit equivalent is:

```text
lake build So52
```

For just the explicit lower-bound construction:

```text
lake build So52.LowerBound
```

`LowerBound.lean` imports `Std.Tactic`; the other modules also use Mathlib.
Do not substitute a newer Lean or Mathlib version or run an unpinned dependency
update when reproducing this snapshot. Compilation writes generated files
under `.lake/`; these files are not part of the distribution.

The original project also had an unrelated example target named `LeanMath`.
For this distribution, that target is omitted and the default target is
changed to `So52`. The Lean source files and dependency pins are unchanged.
No Lean build was run while preparing this distribution on 2026-10-09.

## What is formalized

| Files | Established statements and scope |
|---|---|
| [LowerBound.lean](So52/LowerBound.lean) | An explicit binary linear encoder from 9 message bits to 52 coordinates; injectivity, self-orthogonality, pairwise distance at least 20, and attainment of weight 20. The principal theorem is `So52.lower_bound_certificate`. Coordinate 0 is the leftmost character in the matrix [LOWER-52-9-20.txt](../LOWER-52-9-20.txt). |
| [Reductions.lean](So52/Reductions.lean) | Support/weight identities, half-weight arithmetic, residual-kernel obstruction, and weight-change tests for weight-6 transvections. These local lemmas do not certify the exhaustive extension scan. |
| [Kernel.lean](So52/Kernel.lean) | Linearity of `q = wt/2 mod 2` on a self-orthogonal code, its doubly-even kernel, dimension and coset-cardinality statements, and a **conditional** first reduction. `reduction52` takes `GeneralBound52_9` as an explicit argument. |
| [Residual.lean](So52/Residual.lean), [EvenSpace.lean](So52/EvenSpace.lean) | Residual projection, kernel and dimension statements, parity, and lower bounds on residual weights; identification of the weight-44 residual with the even-weight space. |
| [Fourier.lean](So52/Fourier.lean), [FourierCoefficients.lean](So52/FourierCoefficients.lean), [FourierBlocks.lean](So52/FourierBlocks.lean), [WeightDistribution.lean](So52/WeightDistribution.lean) | Character orthogonality, Parseval identities, column-multiplicity identities, and finite weight-distribution calculations used by the following exclusions. |
| [Weight44.lean](So52/Weight44.lean), [Weight52.lean](So52/Weight52.lean) | Exclusion of weights 44 and 52 in a doubly-even length-52, dimension-8 code with nonzero weights at least 24. |
| [Weight48.lean](So52/Weight48.lean), [Weight48Cosets.lean](So52/Weight48Cosets.lean), [Weight48Exclusion.lean](So52/Weight48Exclusion.lean), [TripleBits.lean](So52/TripleBits.lean) | Kernel/triple structure, coset constraints, and exclusion of weight 48 under the same code hypotheses. |
| [Weight40.lean](So52/Weight40.lean), [ResidualDual.lean](So52/ResidualDual.lean), [ResidualMoments.lean](So52/ResidualMoments.lean), [Weight40Equality.lean](So52/Weight40Equality.lean) | Assuming a weight-40 word exists: necessary integer Fourier constraints with actual witnesses, residual dual minimum weight at least 4, moments 768 and 4992, and inner Parseval equality 5120. Actual inner column multiplicities are 0/1 and the nonzero Fourier coefficients attain their endpoints. These are necessary conditions, **not an exclusion of weight 40**. |
| [Section4.lean](So52/Section4.lean) | `max_weight_le36_of_no_weight40` assembles the maximum-weight bound **with exclusion of weight 40 as an explicit hypothesis**. |

`GeneralBound52_9` is the proposition that every binary length-52,
dimension-9 linear code has a nonzero word of weight at most 22. The files
do not prove this proposition or declare it as an axiom. This conditional
Lean reduction must not be identified with the q=0 certificate in §3.1 of
the main proof, which is not formalized here.

The lower-bound file gives its certificate in terms of an explicit `BitVec`
encoder. The general lemmas use submodules over `ZMod 2`; the README does not
assert an additional formal bridge theorem between these two presentations.

## What is not formalized

- The fixed-coefficient q=0 certificate in the main text.
- The weight-40 residual classification, cubic reduction, and final integer
  enumeration, hence the unconditional exclusion of weight 40.
- The classification into the three doubly-even kernels in §§3.2–6,
  including the external classification-table dependencies.
- Exhaustive extension exclusion in §7 and completeness of its computation.
- Nonexistence of an SO [52,9,22] code and the complete upper bound needed
  for `d_SO(52,9)=20`.

The upper-bound computation remains the separate, computer-assisted argument
in the main text. Successful compilation of this supplement does not verify
that complete argument.

## Preserved build evidence and provenance

[lean-build-weight40-equality.log](logs/lean-build-weight40-equality.log)
ends with `Build completed successfully (1700 jobs).` The accompanying
[status record](logs/build-weight40-equality-status.json) records
`lake build So52`, exit code **0**, on **2026-10-08 16:10:25–16:11:04 JST**,
with elapsed time **39.6698637 seconds**. This is a historical build, not a
new build of the packaged directory. Some entries in the log are replayed
build results, as explicitly marked by Lake.

The printed theorem dependencies in that log are among `propext`,
`Classical.choice` (also printed as `choice`), and `Quot.sound`. The preserved
[source-scan record](logs/source-scan-weight40-equality.json) reports no
forbidden matches; it is a historical source check, not a replacement for
building the files.

The source report records comment-only changes to `So52.lean` and
`So52/Weight40Equality.lean` at **2026-10-08 16:44 JST**, after that successful
build, with no subsequent rebuild for those comments. The
[historical source hashes](logs/weight40-equality-source-sha256.json) retain
their original values and therefore do not describe every current file.
[SOURCE-RECORD.json](SOURCE-RECORD.json) records the distributed snapshot,
the unchanged source copies, log-path redactions, and the build-file adaptation.
The package [MANIFEST.json](../MANIFEST.json) records current distribution hashes.
