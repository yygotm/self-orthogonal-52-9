# Notes on the English translation

Source: [PROOF.md](PROOF.md), v3.1. Translation: [PROOF.en.md](PROOF.en.md).
The English text is authoritative. PROOF.md is the Japanese source text;
version 3 was reviewed, and version 3.1 incorporates the responses but has not been re-reviewed.
If they differ, verify the mathematical content against the Japanese source text.
The following 9 notes record notation, terminology, and documentary-scope
observations and editorial exceptions. They do not strengthen or weaken the
mathematical content of the translated proof and are not findings of a counterexample.

- **TN-1 — §5, “Structure of type A”: effective length versus ambient length.**
  The source calls K a [47,5,24] code, while describing its generator columns
  as 15 single columns, 16 pairs, and 5 zero columns, totaling 52 coordinates.
  The English text now explicitly states that K has length 52 and effective
  length 47, and that deletion of the 5 zero columns gives a [47,5,24] code.
  The subsequent calculations continue to keep K in ambient length 52.
  This is a **clarification, not a change of the argument**.
- **TN-2 — §5, “Structure of type A”: the two roles of k0.**
  The source first writes the second weight-36 codeword as v+k0, so k0 is
  a codeword of K, and then uses k0·p with a column type p in F2^5 and
  identifies k0=w1, where w1 is explicitly a message. Before the first use
  of k0·p, the English text now fixes a basis and explicitly identifies
  codewords with their 5-bit messages relative to that basis, retaining k0
  for both. This is a **clarification, not a change of the argument**.
- **TN-3 — §7.2 and related references: “reflection” is correct.**
  For wt(h)=6, q(h)=wt(h)/2 mod 2=1, so h is nonsingular for the quadratic
  form q=wt/2 mod 2 on the even-weight space. The map T_h(x)=x+(x·h)h is
  precisely a reflection in the orthogonal group of q (an orthogonal
  transvection). The source and translation correctly use “reflection”; no
  terminology correction is needed in the proof.
- **TN-4 — opening paragraphs, §2.3, §9, §11 M6, and the final paragraph:
  preservation claims versus subsequent privacy redaction.**
  The source says that imported source materials and included review copies
  were left unchanged and records identity with originals. The current
  [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json) explicitly records later privacy
  redactions and retains pre-redaction hashes. The preservation statements
  therefore need to be read in their revision-time context; they are not
  literal byte-identity claims for every file in the redacted distribution.
  The translation preserves those statements as written instead of silently
  updating the Japanese proof's historical account. The distribution cleanup of
  2026-10-09 also removes conversational endings and internal identifiers from
  included historical copies, with earlier hashes retained for provenance.
- **TN-5 — §3.2, weight 48: an implicit lower-bound inequality.**
  The source says that the outside image has dimension at most 3−z and then
  that the kernel dimension r “is 5+z≥6.” Rank–nullity gives a lower bound
  r≥5+z≥6 from the stated premise, rather than equality r=5+z. The English
  text now says “the kernel dimension satisfies r ≥ 5+z ≥ 6.” The subsequent
  contradiction uses only this lower bound. This is a **clarification, not
  a change of the argument**.

- **TN-6 — §2.1: external PDF omitted from the public distribution.**
  For copyright reasons, the public package does not include the Kurz PDF.
  The English text therefore replaces the “Included PDF” link with a notice
  of omission and a reference to the download URL and SHA-256 in
  [references/SOURCES.md](references/SOURCES.md). The Japanese source text
  retains its original local PDF link. As with TN-4, this is a distribution
  and documentary-scope difference, not a change to the cited mathematical
  result or the proof.

- **TN-7 — §6: the set on which the Fourier transform equals −6.**
  The source's phrase “its support S” is ambiguous because ĝ is nonzero at
  every point: its values are 2 and −6. The English text now explicitly
  defines S = {w : ĝ(w) = −6}, the set whose graph structure is used in the
  next step. This is a **clarification, not a change of the argument**.

- **TN-8 — §9: revision-time scope and subsequent full runs.**
  The statements that no end-to-end run had been performed are now limited
  by “as of this revision.” An execution-update footnote records subsequent
  successful full runs reported by Claude: v3 on 2026-10-08 at 17:08–17:22
  JST in a review session, and v3.1 on 2026-10-09 at 01:21–01:29 JST by
  Claude, with all 13 stages passing and full_proof_reproduced: true.
  The execution records are maintained in the public repository; no path
  is reproduced here. These runs were not independently rerun during this
  edit. This is a **clarification, not a change of the argument**.

- **TN-9 — current guides: the scope of review of the Japanese source.**
  The opening of these notes, the package README, and lean/README now call
  PROOF.md the Japanese source text: version 3 was reviewed, and version 3.1
  incorporates the responses but has not been re-reviewed. This replaces
  the unqualified description “the reviewed version.” Discrepancies are to
  be checked against the Japanese source text. This is a **clarification,
  not a change of the argument**.
