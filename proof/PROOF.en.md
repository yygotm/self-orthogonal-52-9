# Nonexistence of a binary self-orthogonal [52,9,22] code: a computer-assisted proof candidate

Created: 2026/10/8. **v3.1: 2026/10/8, incorporating C-1–C-7 from the re-review of v3.** The codes considered are binary linear codes, and the inner product is the usual Euclidean inner product. Zero columns and repeated columns are not excluded at the outset; equivalence means equivalence under coordinate permutations.

**The conclusion obtained is d_SO(52,9)=20.** The mathematical reductions, finite enumerations, and a generator matrix attaining the lower bound are set out below. The overall verdict of the re-review of v3 was “sound”: D1–D3 and M1–M6 were all resolved, O1 and O2 were correct, and no counterexample or new mathematical error was found. This version addresses the remaining minor comments C-1 and C-2 and the optional comments C-3–C-7. This is an AI review verdict; human review, formalization, a check of novelty, and a re-review of v3.1 itself have not been performed. [v3 integrated report](review/v3/C-final.md)

The sources for the v1 review are the [review request](review/v1/revision-request.md), [A1](review/v1/A1.md), [A2](review/v1/A2.md), [B1](review/v1/B1.md), [B2](review/v1/B2.md), and [C integrated report](review/v1/C3-final.md). The v2 and v3 reports are included in [review/v2](review/v2/) and [review/v3](review/v3/). Preserved versions of the text are [v1](PROOF-v1-20261008.md), [v2](PROOF-v2-20261008.md), and [v3](PROOF-v3-20261008.md). The v3.1 revision corrected the checks in the entry point and the environment dependence, but did not rewrite past computation results or the imported source materials. Long full scans were not run during the revision; they are distinguished from the runs recorded by the reviewers.

The final exclusion computations are finite enumerations using integer and bit operations. The infeasibility results from OR-Tools and SCIP are retained as separate cross-checks, but are not used in the final proof route.

## 1. What changed through the three perspectives

| Perspective | Work performed | Contribution to the resolution |
|---|---|---|
| Extend the existing approach | Enumerated all extensions of the fixed [51,8,24]+0 code using its triple structure, and extended the method to examples without zero columns obtained by orthogonal transformations | Replaced UNKNOWN for the fixed example with complete exclusion. |
| Question the existing assumptions | Examined the premise that a large general classification had to come first, and narrowed the cases using maximum weight and the cubic function wt/4 mod 2 | Obtained a classification reducing all doubly-even [52,8,24] codes to 3 types. |
| Seek a different method | Combined Fourier/Walsh transforms, minimum-weight Reed–Muller codewords, bent functions in few variables, and elimination via congruences | Excluded 49 lifting problems by integer enumeration of 5,318 candidates, and weight 40 by enumeration of 8,448 candidates. |

For q≠0, another equivalent problem was obtained: the existence of a doubly-even [54,9,24] code with 2 identical nonzero columns. All weight-6 transformations of a publicly available [54,9,24] code were also tried, but this route is not needed for the final proof.

## 2. Known results used and the scope of verification

### 2.1. The classification table retained in the final route

We use Sascha Kurz, *Classification of 8-divisible binary linear codes with minimum distance 24*, **Section 2, Table 1 (PDF p.4)**. The table counts 8-divisible binary linear codes by effective length n, after removal of zero columns, and dimension k; the wording of the caption and text in the source is “minimum distance 24.” For k=8 and n≤54, g_2(8,32)=65>54, so minimum distance at least 24 and minimum distance exactly 24 count the same 8-divisible codes. The entries in the k=8 row at n=51,52,53,54 are, respectively, **1,0,0,1**; only uniqueness at n=51 and nonexistence at n=52 are used. Immediately before the table, the source explicitly states that blank entries on the left of each row mean 0. The table does not restrict the set of weights to {24,32}, and repeated columns are allowed. The PDF is not included in the public distribution; its download URL and SHA-256 are recorded in [references/SOURCES.md](references/SOURCES.md). [Source](https://d-nb.info/1223982076/34)

Table 1 and the definition of effective length were checked in the original text. In addition, **(51,8)=1 and (52,8)=0, the entries used in the proof, are reported as “agreement by independent recomputation (Claude, 2026/10/8).”** The [record dated 2026/10/8 15:40](references/kurz-table1-check-1540.md) counts the 8-divisible codes by effective length within the stage1/stage2 classification of doubly-even codes; the [aggregation code](evidence/kurz/kurzcheck.py) is also included. The statement “nobody has recomputed them” in the v3 integrated report did not cover this record, so this version adds that information. During this revision, stage1/stage2 themselves were neither rerun nor audited for completeness, and their full set of input pkl files is not included; the main proof therefore continues to cite Kurz Table 1. The earlier references to Proposition 1(1) or Table 4 as the direct source of these 2 entries are corrected here.

### 2.2. Classical results and facts checked computationally

We use the Griesmer bound, the Hamming bound, Fourier inversion and Parseval's identity on finite groups, and the following classical results on Reed–Muller codes. The minimum weight of RM(r,m) is 2^(m−r), and the supports of minimum-weight codewords are affine subspaces of codimension r. The source for the latter statement is Carlet (2024), *Identifying codewords in general Reed-Muller codes and determining their weights*, **Section 2, p.10613**. [Original PDF](https://www.aimspress.com/aimspress-data/math/2024/5/PDF/math-09-05-518.pdf)

The fact that bent functions in 4 variables have degree at most two was also checked by examining all 65,536 truth tables in `audit_exact.py`. Independent exhaustive enumerations by reviewers A and B were added as cross-checks of the counts and completeness of the seventh-row candidates in §5 and §6. The statement “the only external dependencies are the 2 entries of Kurz's table” refers to **dependence on external classification tables and code upper-bound data**; it does not mean that these classical theorems or the finite computations explicitly described in the text are unnecessary.

### 2.3. Where external classifications were replaced

Bouyukliev–Bouyuklieva's Table 8, previously used to reduce a D with zero columns to D0, has been replaced by the internal argument in §3.2 and Kurz Table 1. Thus we do not assume that the former table also counts nonprojective or non-8-divisible codes.

The classification in Simonis (1991), *A description of the [16,7,6] codes*, has been replaced by reviewer B's independent exhaustive classification. Put any [16,7,≥6] code in systematic form [I_7|A], and choose A lexicographically minimal in row-major order under permutations of its 7 rows and 9 columns. Then both rows and columns are in ascending order. A row permutation of A is accompanied by a coordinate permutation on the I_7 side, preserving code equivalence. Two equal rows would give a weight-2 codeword, so the rows are strictly ascending. Ordering the column prefixes and pruning by the necessary condition that every nonzero word generated so far has weight at least 6 permits an exhaustive scan of all A of this form.

Reviewer B's [count_all16.py](evidence/agentB/count_all16.py), without imposing an even-weight condition, produced **28,718 candidates, of which 0 have odd-weight words**. The counts by weight distribution in the [preserved rerun log](evidence/agentB-v2/count_all16.rerun.log) are 21,752, 6,910, and 56. No completion log was preserved for B's within-group equivalence checks in v1, and [B's v2 rerun log](evidence/agentB-v2/classify16_7_6.rerun.log) is also from an interrupted run; neither is used to establish the upper bound of 3 classes.

The evidence for “exactly 3 classes” is replaced by **v2 reviewer A2's [classes16.py](evidence/agentA-v2/classes16.py)** and the 4 completed logs for [0–7199](evidence/agentA-v2/classes16-0.log), [7200–14399](evidence/agentA-v2/classes16-7200.log), [14400–21599](evidence/agentA-v2/classes16-14400.log), and [21600–28717](evidence/agentA-v2/classes16-21600.log). For each candidate, this code constructs the incidence graph of weight-6 words and coordinates, then **applies the coordinate permutation returned by VF2 to all 128 words and checks equality with the representative code as a set**. There are 0 candidates that cannot be mapped to the representative of their weight-distribution group. The logs cover all 28,718 candidates without overlap, and the 3 distinct weight distributions give a lower bound of 3 classes. **The candidate enumeration reuses the logic of B's code; the independently written part is the isomorphism check.** Numerical reproduction is distinguished from independence of implementation. [v2 A2 §1.6](review/v2/A2.md), [v2 C §4 D3](review/v2/C-final.md)

An alternative classification by lifting from residual codes also gives 3 classes of [16,7,≥6] codes. The [classify.py](evidence/class52/classify.py), [Dockerfile](evidence/class52/Dockerfile), and [classification log](evidence/class52/log16-7.txt) are included. This alternative is a cross-check using CP-SAT and pynauty, distinguished from the systematic-form exhaustive enumeration and A2's explicit permutation checks in the main route. The review code and logs are listed in [evidence/INDEX.md](evidence/INDEX.md), and their identity in content with the original files is recorded in [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json).

### 2.4. Removing bounds for general codes from the main route

The only general upper bound needed in v1 to establish q≠0 first was **d(52,9)≤23**. In v3, the fixed-coefficient certificate in §3.1 excludes q=0, removing dependence on that upper-bound table. No upper bound for [52,8] codes is used either: the Griesmer bound shows that a doubly-even subcode of dimension 8 has minimum distance 24.

## 3. First reduce to a doubly-even subcode

### 3.1. Reduction covering both cases of q

On an SO code C, q(c)=wt(c)/2 mod 2 is linear. Indeed,

\[
\operatorname{wt}(x+y)=\operatorname{wt}(x)+\operatorname{wt}(y)-2|\operatorname{supp}(x)\cap\operatorname{supp}(y)|
\]

and self-orthogonality makes the intersection cardinality in the last term even.

Suppose that an SO [52,9] code C of minimum distance at least 22 exists. First, if q=0, it is a doubly-even [52,9,≥24] code, so its nonzero weights are restricted to 24,28,…,52. Let A_w be its weight distribution and B_j the weight distribution of its dual, and define the length-52 Krawtchouk polynomials by

\[
K_j(w)=\sum_s(-1)^s\binom ws\binom{52-w}{j-s}
\]

The MacWilliams identity gives 512B_j=Σ_w A_w K_j(w). Set F(w)=23K_1(w)+4K_2(w)+K_3(w). Then F(0)=28600 and

| w | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 52 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F(w) | −72 | −72 | −72 | −584 | −2120 | −5192 | −10312 | −17992 |

Since Σ_{w>0}A_w=511, A_w≥0, and B_j≥0,

\[
0\le512(23B_1+4B_2+B_3)
=28600+\sum_{w>0}A_wF(w)
\le28600-72\cdot511=-8192<0
\]

a contradiction. This **excludes q=0 without classification, a full coset scan, or a code upper-bound table**. [verify_q0_certificate.py](verify_q0_certificate.py) checks these 8 values and the inequality using integer arithmetic, with the existing distance-20 lower-bound code as a positive control. The original coefficient-search materials [lp_exact.py](evidence/agentC-v2/lp_exact.py), [lp_cert.py](evidence/agentC-v2/lp_cert.py), and their logs are also included, but verification requires neither a coefficient search nor the simplex method.

Consequently q≠0, and D=ker q is a doubly-even subcode of dimension 8 whose nonzero words have weight at least 24. If its minimum distance were at least 28, the Griesmer bound would require effective length at least

\[
\sum_{i=0}^{7}\left\lceil\frac{28}{2^i}\right\rceil
=28+14+7+4+2+1+1+1=58>52
\]

so D is a **doubly-even [52,8,24] code**. The 256 words of the nontrivial coset C\D all have weight at least 22, congruent to 2 mod 4; they are excluded by the direct scan in §7.1. The 0 mod 4 side, scanned at the same time in §7.1, is a cross-check of the exclusion of q=0; the main route excludes q=0 by the certificate above. §7.2 is retained as a cross-check route for q≠0.

Also, in the case q=0, any subcode D of dimension 8 in the hypothesized C is doubly-even [52,8,24] by the same Griesmer argument, and C\D is a coset whose words all have weight 0 mod 4 and minimum weight at least 24. It therefore belongs in the right-hand column of §7.1. This is the justification for calling that column a “cross-check of q=0.”

Below, we show that D has only the following 3 types, and exclude all of their extensions.

| Representative | Zero columns | Weight distribution |
|---|---:|---|
| D0 | 1 | 1+204z^24+51z^32 |
| D1 | 0 | 1+172z^24+32z^28+51z^32 |
| D2 | 0 | 1+174z^24+30z^28+49z^32+2z^36 |

The representative matrices are `D-representative-0.txt`, `D-representative-1.txt`, and `D-representative-2.txt`.

### 3.2. An internal reduction of the case with zero columns to D0

Let z≥1 be the number of zero columns, and n=52−z the effective length. The Griesmer bound is g_2(8,24)=50, so z≤2. Since the zero columns lie outside the support of every word, weights at least 36 can be excluded as follows.

1. **Weight 52:** Impossible because there is a zero column.
2. **Weight 44:** The kernel of projection onto the coordinates outside the support is {0,c}. Any other kernel word x would contradict wt(x)+wt(x+c)=44<48. The image must have dimension 7, but the even-weight space on the 8−z effective outside coordinates has dimension 7−z≤6, a contradiction.
3. **Weight 48:** The dimension of the outside image is at most 3−z, so the kernel dimension satisfies r ≥ 5+z ≥ 6. All kernel words other than 0,c have weight 24; Fourier inversion on the 48 coordinates in the support of c gives column multiplicity 48/2^(r−1). This is not an integer for r≥6, a contradiction.
4. **Weight 40:** The projection kernel is {0,c}, and the image is an even [12−z,7,≥4] code. For outside weight j, wt(x)+wt(x+c)=40+2j≥48, so j≥4. Puncturing one further coordinate gives a [11−z,7,≥3] code. The Hamming bound gives 2^7(1+10)=1408>2^10 for z=1 and 2^7(1+9)=1280>2^9 for z=2, excluding both cases.
5. **Weight 36:** Similarly, the outside code is even [16−z,7,≥6]. An even code of minimum distance at least 8 would contradict g_2(7,8)=18>16−z, so a weight-6 word must exist. The residual code obtained by deleting the support of that word is [10−z,6,≥3]. That the projection kernel is exactly the one-dimensional space spanned by that word, and that the outside weights are at least 3, follows from the fact that the sum of the weights of a pair of nonzero words is at least 12. The Hamming bound gives 2^6(1+9)=640>2^9 for z=1 and 2^6(1+8)=576>2^8 for z=2, a contradiction.

Thus the only nonzero weights are 24,28,32. In a generator matrix after removing the zero columns, let b be the number of unordered pairs of equal columns. For a binary code of dimension 8,

\[
\sum_{w>0}A_w=255,\qquad
\sum_w wA_w=128n,\qquad
\sum_w w^2A_w=64(n^2+n+2b)
\]

The term b in the second moment follows because the two bits corresponding to distinct nonzero columns are independent, whereas those corresponding to equal columns agree. For n=51, A28=−8b, hence b=0, A28=0, A24=204, and A32=51. For n=50, A28=−40−8b<0, which is impossible.

Therefore z=1, and removing the zero column from D gives a projective, 8-divisible [51,8,24] code. The **entry 1 at (n,k)=(51,8) in Kurz Table 1**, together with verification that D0 has the same parameters and weight distribution, implies that D is equivalent to D0. §4–§6 consider only D without zero columns.

## 4. Reducing the maximum weight to at most 36

Since the code is doubly-even, the candidate weights at least 24 are 24,28,32,36,40,44,48,52.

### Weight 52

Choose the all-one word as a basis vector. The Fourier coefficients of the multiplicities m of the 52 columns, expressed in the remaining 7 bits, are F(0)=52 and F(u)=±4 (u≠0). Parseval gives Σm²=(52²+127·16)/128=37, whereas nonnegative integrality gives Σm²≥Σm=52, a contradiction.

### Weight 44

Projection onto the 8 coordinates outside a weight-44 word c has kernel {0,c} and image dimension 7. Any other kernel word x would contradict wt(x)+wt(x+c)=44<48. The outside weights are even, so the image is the entire even [8,7,2] code.

Writing j for the outside weight, the Fourier coefficients of the 44 inside columns satisfy |F(u)|≤2j−4. The numbers of nonzero messages with j=2,4,6,8 are 28,70,28,1, respectively, so

\[
128\sum m^2\le44^2+70\cdot16+28\cdot64+144=128\cdot39<128\cdot44,
\]

a contradiction.

### Weight 48

Projection onto the 4 coordinates outside a weight-48 word c has an even image, so the dimension r of its kernel K is at least 5. All words of K other than 0,c have weight 24. Taking c as the all-one row and applying the Fourier transform gives column multiplicity 48/2^(r−1), so r=5. The code K is obtained by repeating each coordinate of RM(1,4) three times.

For a word x of outside weight 2, the inside weights in its K-coset are 22 or 26. Let r_t be the weight on each triple and put f(t)=3−2r_t. All 16 Walsh coefficients have absolute value 4. Parseval implies that each r_t is 1 or 2.

Let x,y,z be lifts of the outside basis 1100,1010,1001. Each individual word and each sum of two of them has outside weight 2, so on each triple the images of x,y,z are the 3 distinct nonzero elements of F2^3/〈111〉. Thus x+y+z is 000 or 111 on each triple.

Its outside part is 1111, and the inside weights of its K-coset lie in the range 20–28 and are divisible by both 4 and 3. Hence they are all 24. This requires a 16-bit truth table to have distance 8 from every affine function, making all Walsh coefficients 0, a contradiction.

### Weight 40: exhaustive integer enumeration

The kernel of projection onto the outside coordinates is {0,c}, and the image has dimension 7. If i is the inside weight and j the outside weight, i+j≥24 and 40−i+j≥24 imply j≥4. The image is even, and minimum distance at least 6 would contradict g_2(7,6)=15>12, so it is even [12,7,4]. An all-one row can be chosen in a parity-check matrix, so its 12 columns are obtained by deleting 4 points from the 16 affine points of F2^4. The deleted 4-point sets have 2 types: an affine plane or an affinely independent set.

The dual words of this outside code are the intersections of supports of affine functions with the 12-point set. The support of a nonzero affine function has 8 or 16 points, so the dual minimum distance is at least 4. Consequently a generator matrix of the outside code has neither zero nor repeated columns, and the first and second moments of its weight j are 768 and 4992, respectively.

For outside weight j, |F(u)|≤2j−8. Using these moments, over the nonzero messages we obtain

\[
40^2+\sum_{u\ne0}(2j(u)-8)^2
=1600+4\cdot4992-32\cdot768+64\cdot127
=5120=128\cdot40
\]

The upper bound from Parseval equals the lower bound Σm²≥Σm=40. Thus the multiplicities of the 40 inside columns are 0/1, and every nontrivial coefficient attains the bound ±(2j−8).

For a doubly-even code, the function f(x)=wt(x)/4 mod 2 has degree at most three. This follows from the inclusion–exclusion expansion of weight: the weights in the linear terms are divisible by 4, the intersection cardinalities in the quadratic terms are even, and the coefficients of terms of degree at least four are divisible by 8.

Choose c and lifts x(u) as a basis, and put a(u)=f(x(u)). Then

\[
f(x(u)+c)+f(x(u))=j(u)/2\pmod2.
\]

For j=4,8,12, we must have a(u)=0. For both residual types, the cubic functions in 7 variables satisfying these conditions form a linear space of dimension 8. The 7-dimensional equivalence operation of changing basis lifts by c reduces each type to 2 candidates.

For each candidate, enumerate all permitted choices of signs of F(u) and test whether the inverse Walsh transform gives m with values 0/1. After elimination by congruences, the enumeration count is 4,096+4,096+256=8,448; the remaining 1 candidate is immediately contradictory modulo the congruences, and there are 0 solutions.

**Code:** `exact40.py`, `exact40-results.json`. In the bent model and the 8-branch integer programming model used for cross-checking, both OR-Tools and SCIP also returned infeasibility, providing a cross-check through different reductions.

## 5. The case containing weight 36

Outside a weight-36 word c, the code is even [16,7,6]. The kernel is {0,c}; an outside weight at most 4 would make the sum of the weights of two words less than 48. Even minimum distance at least 8 contradicts g_2(7,8)=18>16, so the minimum distance is 6. We use the 3 representatives verified by the independent exhaustive classification in §2.3.

| Type | File | Weight distribution |
|---|---|---|
| B | `residual16-0.txt` | 1+45z^6+41z^8+34z^10+6z^12+z^14 |
| A | `residual16-1.txt` | 1+48z^6+30z^8+48z^10+z^16 |
| C | `residual16-2.txt` | 1+44z^6+45z^8+28z^10+10z^12 |

### Excluding types B and C

The function a(u)=wt(x(u))/4 mod 2 has degree at most three in 7 variables, and

\[
f(x(u)+c)=a(u)+1+j(u)/2\pmod2.
\]

For j=6, a=0. The dimensions of the spaces of cubic functions satisfying these linear conditions are 18 for type B and 19 for type C. Enumerate all functions and reduce by changes of lifts a↦a+ℓ(u)(1+j(u)/2) and verified coordinate permutations of the residual code.

Let b be the number of pairs of equal columns in D, which has no zero columns, and A36 the number of weight-36 words. The first 2 moments give

\[
A24=172+4b-A36,\quad A28=32-8b+3A36,\quad A32=51+4b-3A36
\]

so the weight of f is N=32−8b+4A36. Let x be a weight-36 word other than c, and j its outside weight. Since wt(x+c)=2j≥24, we have j≥12. If both words of a pair x,x+c with the same outside word had weight 36, then 36+2j=72, so j=18>16. Thus at most one has weight 36. Hence

\[
A36\le1+\#\{\text{outside words of weight }j\ge12\}
\]

giving 1+6+1=8 for type B and 1+10=11 for type C. In each pair where the derivative is 1, exactly one value of f is 1, giving N≥48 for type B and N≥56 for type C. Thus 48≤N≤64 for type B and 56≤N≤76 for type C.

In the implementation, `residual36_cubics.py` generates both types over the common wider range 48≤N≤76; the type-B upper bound 64 is applied as a pre-lifting condition in `exact36.py`. The type-C lower bound 56 is automatically satisfied by the derivative condition. The actual lifting problems comprise 3 orbits for type B and 46 for type C. For each a, the inside weight i satisfies

\[
24\le i+j\le36,\quad24\le36-i+j\le36,\quad i+j\equiv4a(u)\pmod8
\]

There is either 1 choice or 2 choices differing by 8. Put F(u)=36−2i and encode each binary choice by z_u∈{0,1}. The inside column multiplicities are recovered uniquely by the inverse Walsh transform

\[
m(v)=\frac{1}{128}\sum_u F(u)(-1)^{u\cdot v}
\]

Reduce integrality to linear congruences mod 8 and enumerate every solution of the necessary F2 equations obtained by row elimination. At most 12 binary degrees of freedom remain. Among the total of 5,318 candidates, 0 yield nonnegative integer multiplicities. The count is 0 even without assuming an upper bound of 2 on the multiplicities.

**Code:** `residual36_cubics.py`, `exact36.py`, `exact36-results.json`. All 49 OR-Tools/SCIP models also returned INFEASIBLE, in agreement.

### Structure of type A

A lift of the outside all-one word and its difference with c have weights 32 and 36. No other outside word yields weight 36, so D has exactly 2 weight-36 words.

The Parseval upper bound for the 36 inside columns is Σm²≤38. To bound b, the number of pairs of equal columns among all 52 columns, directly, it suffices to use f≠0 and the minimum weight of RM(3,8). The moment equation gives N=wt(f)=40−8b≥32, hence b≤1 and N is 32 or 40. This avoids applying the inside multiplicities to the outside part without justification. All 65,536 cubic functions compatible with type A can be enumerated; 0 have weight 40 (`audit_exact.py`). Therefore b=1 and f has weight 32.

The support of a minimum-weight word of RM(3,8) is an affine space of dimension 5, so its direction subspace K has code dimension 5; K is 8-divisible, with weights 24 or 32. The coset on which f=1 contains 30 words of weight 28 and 2 of weight 36.

Choose one weight-36 word v and write the other as v+k0. Fix a basis of K and identify its codewords with their 5-bit messages in F2^5 relative to that basis; in particular, k0 also denotes the message of the codeword k0. For a column type p of K, the signed difference in column counts, with signs given by the bits of v, is −5 for p=0, −1 for p≠0 with k0·p=0, and 0 for k0·p=1. Thus K has at least 5 zero columns. The Griesmer bound gives effective length at least 47 for K, so there are exactly 5 zero columns.

K has length 52 and effective length 47. After deleting its 5 zero columns, it is a [47,5,24] code, with weight distribution 1+30z^24+z^32. Let w1 be the message corresponding to the unique weight-32 word. Fourier inversion shows that the column types are the 15 nonzero points of the hyperplane w1·p=0, each once, the 16 points outside it, each twice, and 5 zero columns. The signed column count for v in the preceding paragraph is 0 whenever k0·p=1. For a single column, however, the signed count is ±1 and cannot be 0. Thus k0·p=0 at all 15 points with w1·p=0. It follows that k0=w1, and v can be normalized to have bit 1 on the 15 single columns and the zero columns, and bits 0,1 on each pair of equal columns. This equality is established before using the normal form.

#### Completeness of the seventh-row enumeration: from Parseval to bent functions

Represent the column types p in F2^5, with the hyperplane given by p=(u,0) and the repeated columns by p=(u,1), where u∈F2^4. For the seventh row y, define the signed sums for each column type by

\[
\tau_p=\sum_{j:\,p_j=p}(-1)^{y_j},\qquad
\rho_p=\sum_{j:\,p_j=p}(-1)^{y_j+v_j}
\]

Write T=\widehat\tau and R=\widehat\rho for the Fourier transforms on K. Since y+K and y+v+K belong to the part where f=0, all their words have weight 24 or 32, so T,R∈{4,−12}. Let r be the weight of y on the 5 zero columns, and t=τ_0=5−2r; then ρ_0=−t. The mean of T is t, so −12 occurs 8−2t times in T, and 8+2t times in R. Parseval gives

\[
\sum_p(\tau_p^2+\rho_p^2)
=\frac{1}{32}\sum_w(T(w)^2+R(w)^2)=96
\]

The 15 single columns contribute a total of 30 to the left-hand side, the 16 pairs of equal columns contribute a total of 64, and the zero columns contribute 2t². Thus 94+2t²=96 and t=±1. Replacing y by y+v changes the sign of t, so we can normalize to t=1 and weight r=2 on the zero columns; by permuting the zero columns we may take these to be 2 fixed positions.

Let s(u) (u≠0) be the bits on the single columns, extend by s(0)=0, and let a(u),b(u) be the bits on each pair. Write the Walsh transforms in 4 variables as

\[
W_a(w')=\sum_u(-1)^{a(u)+w'\cdot u},\qquad
S=W_s(w')
\]

and similarly for the others. For w=(w',ε), we have

\[
T(w)=S+(-1)^\varepsilon(W_a+W_b),\qquad
R(w)=-S+(-1)^\varepsilon(W_a-W_b)
\]

Requiring T,R∈{4,−12} for both ε=0,1 leaves only

\[
(S,W_a,W_b)=(4,\,\pm4,\,\mp4)
\quad\text{or}\quad
(-4,\,\pm4,\,\pm4)
\]

Thus s,a,b are all bent. Defining their duals by W_a=4(−1)^ã and similarly, the condition is equivalent to **ã+b̃+s̃=1**. Conversely, bent functions satisfying this relation make all the above values of T,R equal to 4 or −12, satisfying every required weight condition.

All bent functions in 4 variables have degree at most two; this was also checked over all 65,536 truth tables. Adding words of K can add any affine function to a, so its linear and constant terms can be eliminated to choose a purely quadratic bent function L. There are 28 such L. Put B=s̃ and h=1+L̃. Then b̃=B+h, and s(0)=0 is equivalent to wt(B)=6. Thus `normalized36_orbits.py` need only enumerate the 28 choices of L and the 448 bent functions B of weight 6, retaining all those for which B+h is also bent. There are 192 for each L, for a total of **5,376**. The preceding derivation works in both directions, so this enumeration covers every candidate.

As an independent check, reviewer B used [verify_A7_count.py](evidence/agentB/verify_A7_count.py) to enumerate the 2^15 sign patterns on the single columns and all permitted Fourier values, followed by inverse transformation. With the zero-column pattern fixed, this gave **172,032=5,376×32**, or 5,376 modulo addition of K. This count does not rely on bent functions being quadratic. All original 5,376 candidates were also checked to be valid and distinct modulo K; together with the equality of counts, this gives an independent cross-check of completeness. [B2 §1(1)](review/v1/B2.md)

#### The eighth row and equivalence classes

The 5,376 seventh-row candidates form 1 orbit under coordinate permutations verified to preserve the code. The eighth row can be normalized in the same way. For its weight-2 pattern on the 5 zero columns, it suffices to examine the 6 patterns intersecting the seventh row's 2-point set in exactly 1 point. Intersection size 0 would make the sum of the rows have zero-column weight 4, and intersection size 2 would make it 0, contradicting the necessary condition of weight 2 or 3 from the same Parseval argument. Modulo addition of the existing 7 rows, there are 36 eighth-row candidates, all in 1 orbit. Without using the author's permutation group, reviewer B independently verified the single orbit of seventh rows and the single class of eighth rows by checking that a correspondence between bases preserves the weights of all words. Hence this type of D consists of the single type D2. [B2 §2](review/v1/B2.md)

**Code:** `normalized36_orbits.py`, `normalized36-classification.json`.

## 6. The case of maximum weight 32

If f=wt/4 mod 2 is zero, the code is 8-divisible. In this case, the moment equation A28=32−8b and A28=0 give **b=4**, so D is nonprojective and has repeated columns. Kurz Table 1 classifies codes allowing repeated columns (§2.1), so it applies to this D, which has no zero columns, effective length 52, dimension 8, and minimum distance 24. The **entry 0 at (n,k)=(52,8)** excludes it. If f≠0, the minimum weight of RM(3,8) gives wt(f)≥32.

Substituting A36=0 into the moment equation above gives wt(f)=32−8b, hence b=0 and wt(f)=32. The support of f=1 is an affine space of dimension 5; its direction K has dimension 5 and weights 24 or 32, and all 32 words of the coset have weight 28.

The Fourier transform of the constant-weight coset shows that the multiplicities of the nonzero columns of K are even, and that there are at least 4 zero columns. Halving the nonzero multiplicities and applying the Griesmer bound gives at most 4 zero columns, so there are exactly 4. The code obtained by halving is [24,5,12], with weight distribution 1+28z^12+3z^16.

Integrality of its column multiplicities implies that the sum of the 3 messages of weight 16 is zero. Thus the 24 columns are all points outside a fixed subspace U of dimension 3 in F2^5. The code K has a unique normalization consisting of two copies of each of these columns and 4 zero columns.

A representative v with f=1 has bits 0,1 on each pair of equal columns and all ones on the 4 zero columns. Below, we also derive the weights of the remaining rows on the zero columns.

### Completeness of the seventh-row enumeration: zero columns and Fourier support

Let y be the seventh row, and define τ_p,ρ_p as in §5, the signed sums for y and y+v at each column type. The repeated columns of K correspond to the 24 points of P=F2^5\U. If r is the weight of y on the 4 zero columns, then τ_0=4−2r=t and ρ_0=−t. All words of y+K and y+v+K have weight 24 or 32, so the same Parseval calculation as in §5 gives Σ_p(τ_p²+ρ_p²)=96. The 24 pairs alone contribute 24×4=96, while the zero columns contribute 2t². Hence t=0 and **r=2**.

Let a(p),b(p) be the bits of y on each pair, and define

\[
g(p)=\frac{(-1)^{a(p)}+(-1)^{b(p)}}2,\qquad
h(p)=\frac{(-1)^{a(p)}-(-1)^{b(p)}}2
\]

on P, extending both by zero on U. Then g,h∈{0,±1}, and their supports are complementary in P. Since τ=2g and ρ=2h, the weight-24/32 condition is equivalent to **ĝ,ĥ∈{2,−6}**. Conversely, g,h satisfying this condition and the complementary-support condition uniquely determine a,b on each pair.

Put W=U^⊥, so dim W=2. Since g vanishes on U, for any α,

\[
\sum_{w\in W}\widehat g(\alpha+w)
=4\sum_{p\in U}g(p)(-1)^{\alpha\cdot p}=0
\]

Each coset of W has 4 points, and ĝ takes only the values 2 and −6, so **−6 occurs at exactly 1 point of each coset**. Let S = {w : ĝ(w) = −6}. This set is therefore the graph of a function φ from the quotient F2^5/W≅F2^3 to W≅F2^2. The graph form is a consequence of the Fourier conditions, not an assumption used in the reduction.

Choose coordinates so that S={(u,φ(u)):u∈F2^3}. For p=(α,β) with β≠0, the inverse transform is

\[
g(\alpha,\beta)=-\frac14
\sum_{u\in\mathbb F_2^3}(-1)^{\alpha\cdot u+\beta\cdot\varphi(u)}
\]

Since g∈{0,±1}, the Walsh values of the 2 components of φ and of their sum belong to {0,±4}; all are semi-bent functions in 3 variables. A degree-three Boolean function in 3 variables has a truth table of odd weight, which remains odd after adding an affine function. Its Walsh coefficients are therefore 2 mod 4, so it cannot satisfy this condition. The degree is consequently at most two. Affine functions are also excluded because they have a Walsh coefficient ±8; the purely quadratic parts qa,qb of the 2 components must therefore be nonzero and distinct.

### Why h is paired with the same pair of quadratic parts

On each slice with fixed β≠0, the support of g is the Walsh support of a nonzero quadratic form in 3 variables, an affine plane of 4 points. The direction of this plane is determined by the one-dimensional radical of the polar alternating form of the quadratic form. For the support of h to be its complement, the plane on the h side must have the same direction, so the radicals coincide. Over F2^3, the 7 nonzero alternating forms and the 7 one-dimensional subspaces correspond bijectively through the radical, so the purely quadratic parts also coincide. Applying this to β=(1,0),(0,1) shows that the h side has the same pair **(qa,qb)**. The linear and constant terms are separately enumerated; this equality does not assert that those terms are equal as well.

Choosing an ordered pair of distinct nonzero purely quadratic parts from the 7 possibilities, and adding one of 16 affine parts to each component, gives 7×6×16²=10,752 functions g. Pairing each with every h having the same quadratic parts and complementary support gives **344,064 seventh-row candidates**, or **10,752 candidates** modulo the 32 additions from K. Each candidate is directly checked against all weight conditions, and duplicates modulo K are removed.

As an independent completeness check, reviewers A and B did not use quadraticity, but instead took the inverse transform for **all 4^8=65,536 functions φ**, choosing the position of −6 in each of the 8 cosets of W. They retained every {0,±1}-valued function and every pair with complementary supports, obtaining the same 344,064 candidates and 10,752 quotient candidates. The validity and distinctness modulo K of the original candidates were also checked separately. [A1 §(2)](review/v1/A1.md), [B2 §1(2)](review/v1/B2.md)

### The eighth row and equivalence classes

All 10,752 seventh-row candidates form 1 orbit under verified coordinate permutations. The eighth row also has weight 2 on the zero columns, and the same condition is required of the sum of the two rows, so its intersection with the seventh row's 2-point set has size 1. Examining the 4 such outside patterns and quotienting by addition of the 7 existing rows gives 24 candidates, all in 1 orbit. Reviewer B's independent equivalence check by basis correspondence also found 1 orbit of seventh rows and all eighth rows equivalent to D1. Hence D consists of the single type D1. [B2 §2](review/v1/B2.md)

**Code:** `normalized32_orbits.py`, `normalized32-classification.json`. This does not rely on the full order of an automorphism group or on existing equivalence-testing software: the permutations used are explicitly checked to preserve the code.

## 7. Excluding extensions of the 3 types to dimension 9

### 7.1. The main route: direct scanning of all cosets

By §3–§6, the doubly-even [52,8,24] codes to examine are the 3 classes D0,D1,D2. [D0](D-representative-0.txt), [D1](D-representative-1.txt), and [D2](D-representative-2.txt) all have rank 8, are doubly-even, and have minimum distance 24. Their pairs (z,b), consisting of the number of zero columns and the number of pairs of equal columns, are respectively (1,0),(0,0),(0,1), and their weight distributions are those in the table in §3. D0 satisfies z=1 (§3.2), D2 satisfies z=0 and A36>0 (§5), and D1 satisfies z=0, A36=0, and A28>0 (§6). Thus each file represents the unique class in the corresponding case. [Verification record](AUDIT.json)

If C⊃D≅Di, applying the coordinate permutation giving that equivalence to all of C puts it in the form **C=〈Di,v〉, v∈Di^⊥, wt(v) even**. It therefore suffices to examine extensions of these 3 representatives; §7.2 is not needed to establish which representatives they are. In each case dim D^⊥=44 and D⊆D^⊥, so dim(D^⊥/D)=36. Extending a basis of D to one of D^⊥ gives a complement V whose **2^36 elements give exactly 1 representative of each coset v+D**. Membership v∈D^⊥ is guaranteed by construction, and 〈D,v〉 is self-orthogonal precisely when wt(v) is even.

Reviewer C constructed this complement using an independently written elimination procedure, scanned all 2^36 representatives in Gray-code order, and tested

\[
\min_{d\in D}\operatorname{wt}(v+d)
\]

for each even-weight representative. A coset can be rejected as soon as 1 word below the threshold is found. Retaining it as meeting the threshold requires checking all 256 words. The trivial coset v∈D has minimum weight 0 and is rejected, so a case that does not increase the dimension cannot be mistakenly accepted.

| D | wt(v)≡2 mod 4, coset minimum weight ≥22 | wt(v)≡0 mod 4, coset minimum weight ≥24 |
|---|---:|---:|
| D0 | 0 | 0 |
| D1 | 0 | 0 |
| D2 | 0 | 0 |

For a 0 mod 4 coset, weight ≥22 and weight ≥24 are the same condition. The left-hand column gives the final exclusion for q≠0. The right-hand column cross-checks the q=0 certificate through the reduction to an arbitrary dimension-8 subcode at the end of §3.1. In the positive control for D0 at threshold 20, there are **1,138,092,541 even cosets** of minimum weight at least 20, all on the 0 mod 4 side. The original implementation is included as [gen_hdr.py](evidence/agentC/gen_hdr.py) and [cosets.c](evidence/agentC/cosets.c); the supporting source is the [v1 C integrated report §1(1)](review/v1/C3-final.md). C's original logs do not name D, so they alone are not used to establish input attribution; the [reruns naming D](evidence/named-rerun/) are also supplied.

Another independent scan uses as representatives the elements of D^⊥ that are zero on an information set P of D. Since D→F2^P is an isomorphism, each coset has exactly 1 such representative. This method also examined both even-weight types over all 2^36 representatives, finding 0 cosets of minimum weight at least 22 for all 3 classes. The available original files are [gen.py](evidence/ext52x/gen.py), [ext52x.c](evidence/ext52x/ext52x.c), the results for [D0](evidence/ext52x/d22-gpt0.out), [D1](evidence/ext52x/d22-gpt1.out), and [D2](evidence/ext52x/d22-gpt2.out), and the [D0 control result](evidence/ext52x/d20-gpt0.out).

The third implementation by v2 reviewer A2, [mkbasis.py](evidence/agentA-v2/mkbasis.py) and [scanA.c](evidence/agentA-v2/scanA.c), likewise returned 0 for [D0](evidence/agentA-v2/scanA0-22.out), [D1](evidence/agentA-v2/scanA1-22.out), and [D2](evidence/agentA-v2/scanA2-22.out); the [T=20 positive control](evidence/agentC-v2/scanA0-20.out) run by C also gave 1,138,092,541. **The 3 independently written implementations cosets.c, ext52x.c, and scanA.c reproduced the same 6 table entries and the positive control, but all 3 assume the classification in §3–§6.** Independence of the code does not remove dependence on the classification. [v2 C §2.2](review/v2/C-final.md)

For a full scan of each D, the expected coverage counts are **2^34−2^17=17,179,738,112** on the 0 mod 4 side and **2^34+2^17=17,180,000,256** on the 2 mod 4 side, totaling 2^35 on the even-weight side; including odd weights, the number of representatives scanned is 2^36. This direct scan is the main route for the final exclusion. It does not depend on T_h, the reduction to 23 orbits, or the quotient-space implementation of `encode`.

These coverage counts can be derived independently of the scan output. For d∈D and v∈D^⊥, wt(d)≡0 mod 4 and v·d=0 imply wt(v+d)≡wt(v) mod 4, so all 256 words of a coset have the same weight modulo 4. Thus, for r=0,2, the number of cosets is N_r=256^(-1)Σ_{j≡r (mod 4)}B_j, where B_j is the weight distribution of D^⊥. Substituting each distribution of D in §3 into the MacWilliams identity B_j=256^(-1)Σ_w A_w K_j(w) gives N_0=2^34−2^17 and N_2=2^34+2^17. This can be checked in the [integer-arithmetic code](evidence/agentC-v3/coverage_macwilliams.py), [reviewer C's output](evidence/agentC-v3/coverage_macwilliams.log), and the [verification during this revision](runs/v3.1-classification-check/coverage.log).

#### The rerun entry point added in v3 and the verification scope of v3.1

[direct_scan.py](direct_scan.py) and [scan_direct.c](scan_direct.c) provide an entry point that regenerates headers from the 3 matrices in the package, compiles with GCC/OpenMP, and scans the 3 classes at T=22 and D0 at T=20. Full-scan mode checks all the coverage counts, zeros, and positive-control counts above, and fails on any mismatch. The results record the SHA-256 hashes of the inputs and C source, commands, scan ranges, coverage counts, and accepted counts. Past results are not overwritten; output is saved in a new directory under `runs/`.

```text
python reproduce.py --check --backend docker --threads 2
python reproduce.py --full --backend docker --threads 16
# To rerun only §7.1
python direct_scan.py --full --backend docker --threads 16
```

The **bounded checks** performed by `--check` comprise independent exhaustive checks of small codes, 4,096 representatives for each Di, and 1 known coset of D0. A full scan does not start unless `--full` is specified explicitly. Full scans with the **range-capable implementation** (the scanner accepting an explicit start index and count) had not been run when v3 was prepared, but **v3 reviewer B ran 4 full scans of 2^36 representatives with the same generated C binaries on 2026/10/8 at 16:49–16:55, obtaining agreement with every expected table entry**. [B1 §4](review/v3/B1.md), [D0 at T=20](evidence/agentB-v3/full-d0-t20.log), and [the 3 classes at T=22](evidence/agentB-v3/full-t22.log) are included. With Docker `gcc:14` and 16 threads, the T=22 runs took about 55–57 seconds and D0 at T=20 about 133 seconds; these are reviewer measurements dependent on the machine and load. These records are from direct invocations of the C binaries, not the JSON from `direct_scan.py --full` or an end-to-end run of `reproduce.py --full`. Long full scans were not run during the v3.1 revision. [v3 bounded-check results](runs/v3-bounded-check/REPRODUCTION-V3.json), [v3.1 bounded-check results](runs/v3.1-bounded-check/REPRODUCTION-V3.1.json)

### 7.2. A cross-check route using reflections and orbit reduction

This section treats q≠0, meaning that every word in the nontrivial coset has weight 2 mod 4. The case q=0 is excluded by the certificate in §3.1 and is also cross-checked by the direct scan in §7.1.

The 51 nonzero coordinates of D0 split into 17 triples for which the corresponding 3 columns of a generator matrix sum to zero. An even-weight representative v∈D0^⊥ decomposes uniquely into a part a of even weight on each triple, additions of 111 on triples, and the final coordinate.

The space of a has dimension 18 after taking the quotient by D0. The 17 bits specifying additions of 111 on triples also determine the parity of the final coordinate. Reducing the 18-dimensional part by coordinate permutations actually preserving the code and the triples gives 23 orbits. The smaller **noncyclic group Z51⋊〈2〉 of order 408 generated by j↦j+1 and j↦2j (mod 51)** gives 695 orbits and was also used in a separate exhaustive search for the fixed D0. Coordinate 51 is fixed, and the order of 2 mod 51 is 8.

For an even-weight h, the orthogonal transformation

\[
T_h(x)=x+(x\cdot h)h
\]

preserves the inner product. If wt(h)=6, it also preserves the weights of even-weight words modulo 4. There are 29,376 weight-6 choices of h containing the zero coordinate of D0 and preserving minimum distance 24. D1 and D2 are included among these; specifically, we use the bitmasks

```
h1 = 2251816993685511
h2 = 2251834173685767
```

Coordinates are indexed from zero, and the original zero coordinate is 51. The support of h1 is {0,1,2,17,34,51}, and that of h2 is {0,1,2,18,35,51}. The code T_h1(D0) has no zero columns and weight set {24,28,32}, so uniqueness in §6 places it in the D1 class; T_h2(D0) has a weight-36 word, so the classification in §5 places it in the D2 class. In addition to checking both weight distributions and zero-column counts, reviewer B used [th_equiv.py](evidence/agentB/th_equiv.py) to check preservation of the weights of all words under a correspondence between bases, directly verifying equivalence as well. [The T_h item in §7 of v1 B1](review/v1/B1.md), [v1 B2 (3)](review/v1/B2.md)

Let G be the group used for orbit reduction. Each coordinate permutation used has been verified to preserve D0 and its triples and to fix coordinate 51. The set of permitted h is defined by “weight 6, containing coordinate 51, and T_h(D0) having minimum distance at least 24,” so it is G-invariant. Moreover,

\[
gT_hg^{-1}=T_{gh}\qquad(g\in G)
\]

Therefore, even after moving the 18-dimensional part of v to an orbit representative, enumerating all of the 17-bit part and all 29,376 choices of h necessarily includes a pair equivalent to the original (v,h). We do not reduce by independently fixing v and h to orbit representatives.

The change in weight of an even-weight word under T_h can only be −4,0,+4. Thus the inverse image of a target extension has coset minimum weight at least 18. All 23 orbits were processed, yielding 985,908 representatives satisfying this condition. For each representative, among the 29,376 choices of h, we tested the necessary and sufficient conditions

- The support intersection with every weight-18 word has size 1.
- The support intersection with every weight-22 word does not have size 5.

There were 0 choices of h satisfying them. Words of weight at least 26 retain weight at least 22 after the transformation, so no additional conditions are needed.

Thus there is no target extension from D1 or D2. Extensions from D0 have also all been excluded by `triple_exhaustive.py`. All 2^34+2^17 cosets of type 2 mod 4 in the even-weight quotient by D0 were recounted using orbit sizes, confirming agreement of the ranges.

**Code:** `triple_search.py`, `geometry.py`, `triple_exhaustive.py`, `joint_switch_search.py`.

## 8. Lower bound and conclusion

Adding the all-one row of length 52 to D0 gives an SO [52,9,20] code. Checking all 512 words gives

\[
W=1+51z^{20}+204z^{24}+204z^{28}+51z^{32}+z^{52}
\]

The generator matrix is `LOWER-52-9-20.txt`; rank 9, self-orthogonality, and minimum distance 20 are recorded in `AUDIT.json`.

The case q=0 is excluded by the certificate in §3.1, and q≠0 by the classification in §3.2–§6 and the direct scan in §7.1. Therefore no SO [52,9] code of minimum distance at least 22 exists. Every word of an SO code has even weight, so minimum distance 21 is also impossible. Together with the lower bound 20, this gives **d_SO(52,9)=20**.

## 9. Scope and limitations of reproduction and verification

- The exhaustive scan in the main route, §7.1, uses C/GCC/OpenMP. At review time, the original implementations took approximately 1–5 minutes per class at T=22 and 3–8 minutes for D0 at T=20. With the new range-capable implementation, v3 reviewer B measured approximately 55–57 seconds at T=22 and 133 seconds at T=20, using Docker `gcc:14` and 16 threads. Both sets of timings are observations that depend on the machine and load; they were not measured during the v3.1 revision. [B1 §4](review/v3/B1.md)
- Classification, header generation, and record keeping use Python 3.10 or later. The author's classification uses NumPy 2 (`bitwise_count`), and the explicit permutation checks for [16,7,6] use NetworkX. In v3.1, the author-specific package search path in [reassess.py](reassess.py) was removed, so the selected Python environment is used. The pre-change code is preserved in [history/v3/reassess.py](history/v3/reassess.py). The main route does not invoke an optimization solver; OR-Tools and pynauty are used for alternative cross-checks.
- [reproduce.py](reproduce.py) performs bounded checks by default. Success in `--full` mode requires the completion lines of all 4 [16,7,6] shards; the single orbit of seventh rows, single class of eighth rows, and candidate counts in §5 and §6; the integer-lifting results of 49 models and 5,318 candidates / 2 branches, 4 cases, and 8,448 candidates, with 0 solutions; the audit checks and the 3 regenerated representatives; and the coverage and accepted counts in §7.1, all satisfying their specified conditions. Only after these pass is `full_proof_reproduced: true` recorded. This does not claim automatic verification of every number in the text.
- The classification work directory is populated only with Python code and the input files `residual16-{0,1,2}.txt`; archived classification JSON files and generated matrices are not copied in. Missing keys in the generated classification results, additional orbits/classes, or mismatched candidate counts cause failure. Only `joint-switch-full-0.jsonl`, the legacy reflection-route log used by the audit for cross-checking, is separately copied as input and is not treated as a fresh rerun. Add `--legacy-cross-checks` only when rerunning §7.2. [README](README.md)
- In v3.1, the [bounded rerun of classification and verification gates](runs/v3.1-classification-check/CHECK-V3.1.json) ran the 5 scripts for §4–§6 and the audit in an initially empty classification work directory, confirming 1 orbit and 1 class and byte equality of the 3 representatives and lower-bound generator matrix. The gate regression checks include rejection of 2 orbits/classes, missing or duplicated data, incorrect candidate counts, UNKNOWN, and unexpected solutions. Imports of OR-Tools were disabled during classification. This does not include the full [16,7,6] equivalence classification or the full length-52 scans in §7.1.
- The [v3.1 bounded-scan record](runs/v3.1-bounded-check/REPRODUCTION-V3.1.json) has `bounded_checks_passed: true` and `full_proof_reproduced: false`. It checked all cosets of 3 small codes, 4,096 representatives of each Di, and the known distance-20 coset of D0, as well as the q=0 certificate and the hashes of the source materials. **The v3.1 revision did not run long full scans, the full [16,7,6] equivalence classification, or the legacy reflection route.**
- The AI re-review of v3 returned the verdict “sound.” Reviewer B verified the 4 full scans in §7.1, and reviewer C verified reruns of the classification and audit, but, as of this revision, an end-to-end run of `reproduce.py --full` had not been performed. As of this revision, no end-to-end run had been performed for v3.1 either. [v3 integrated report §5](review/v3/C-final.md)[^execution-update]
- The 2 entries of Kurz Table 1 are cited as known external classification results. §2.1 adds the supplementary record “agreement by independent recomputation (Claude, 2026/10/8),” but does not claim that stage1/stage2 were rerun during this revision. The text of Simonis's paper, Bouyukliev Table 8, and general-code upper-bound tables are not used in the main route.
- The original locations, SHA-256 hashes, and sizes of the included source materials are recorded in [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json); citations use relative paths within the package. Their roles and rerun precautions are summarized in [evidence/INDEX.md](evidence/INDEX.md). Historical absolute paths and the `/w` directory in the source materials are distinguished from the current entry points.
- The original [REPRODUCTION.json](REPRODUCTION.json) and existing ZIP remain those of v1. Pre-change documents, code, and manifests are preserved in [history/v2](history/v2/) and [history/v3](history/v3/), and current files are recorded in [MANIFEST.json](MANIFEST.json). New runs save to separate directories under `runs/` without overwriting past results.
- No new mathematical assumptions have been added. This is a computer-assisted proof relying on correctness and completeness of the computations, classical theorems, and Kurz's classification table; it has not been formalized. [RESEARCH.md](RESEARCH.md) is an exploration record retaining intermediate UNKNOWN results and unsuccessful attempts; this document specifies the proof route.

## 10. R1–R12 resolved in v2

| Comment | Changes incorporated in the text |
|---|---|
| R1 | §5, type A: added k0=w1, τ_0=±1 from Parseval, the necessary and sufficient bent-function conditions, completeness of the 5,376 candidates, and an independent count check. |
| R2 | §6: added τ_0=0, the reason the −6 support is a graph, the reason for matching the purely quadratic parts on the h side, and the exhaustive cross-check that does not use quadraticity. |
| R3 | §3.2: established at most 2 zero columns, exclusion of weights at least 36, projectivity and 8-divisibility from the moments, and the reduction to D0 using Kurz. |
| R4 | §2.1, §3.2, §6: corrected the citation to the entries (51,8)=1 and (52,8)=0 in Kurz Table 1. |
| R5 | §2.3, §5: replaced dependence on Simonis's classification with independent exhaustive classification, and documented completeness of the normal form, 28,718 candidates, 3 classes, and references. In v3, the supporting evidence was replaced by A2's preserved equivalence-check logs, and the related materials were included. |
| R6 | §7.1, §7.2: supplied the justification that the images under T_h include D1,D2, G-invariance of the set of h, and the conjugation formula; added direct exhaustive scanning to the main route. |
| R7 | §5, types B/C: derived 8 and 11 from A36≤1+#{j≥12}. |
| R8 | §5, type A: derived b≤1 for the whole code directly from N=40−8b≥32, resolving confusion with Parseval applied only to the inside part. |
| R9 | §4, weight 40: added j≥4, absence of zero/repeated columns from dual distance ≥4, and the moment calculation giving equality in Parseval. |
| R10 | §5, types B/C: distinguished the generation range 48≤N≤76 from application of the type-B upper bound 64 in `exact36.py`. |
| R11 | §7.2: corrected “cyclic subgroup” to the noncyclic group Z51⋊〈2〉 of order 408. |
| R12 | §2.4, §3.1: specified that the upper bound needed by the old route is ≤23; the main route in this version also treats q=0, removing dependence on the upper-bound table. |

## 11. Responses for v3

| Comment | Response and reason |
|---|---|
| D1 | §7.1, §9: included the 3 original implementation families, inputs, named completion logs, and positive control; made header generation, compilation, full scanning, and comparison with expected values accessible through `reproduce.py --full`. Only bounded checks were run. |
| D2 | Rewrote the README to match the main route in v3, its dependencies, and the distinction between bounded checks and full scans. |
| D3 | §2.3: replaced the supporting evidence with A2's [classes16.py](evidence/agentA-v2/classes16.py) and 4 completion logs, explicitly identifying the isomorphism-testing part as the independent part. |
| M1 | §6: made explicit that f=0 gives b=4 and hence nonprojectivity, and that Table 1 applies because it allows repeated columns. |
| M2 | §2.1: corrected the stated scope of Table 1 to minimum distance at least 24, and added the reason that this is equivalent to distance 24 for the parameters in question. |
| M3 | §9: distinguished GCC/OpenMP for the main scan from Python/NumPy/NetworkX for classification, and recorded indicative timings from the reviews. |
| M4 | §7.1: stated that the representative files satisfy the conditions for their respective unique classes, and that C=〈Di,v〉 after a coordinate permutation. |
| M5 | §7.2: corrected the citations to the T_h item in §7 of v1 B1 and to v1 B2 (3). |
| M6 | Changed local citations in this document and the README to relative paths within the package. Preserved versions and source materials were left in their original form. |
| O1 | Adopted: the short fixed-coefficient certificate in §3.1 excludes q=0 without classification or external tables, and its verification is short. Coefficient searches were not run during the revision. |
| O2 | Adopted: added the third implementation and positive control to §7.1, explicitly stating that all 3 implementations assume the same classification. No new full scan was needed. |

The additional proposal in C's report §1(3), to exclude f=0 in §6 by another elementary argument, is not incorporated in this version. Instead, the explanation of the applicability of Table 1 was supplemented in accordance with the formal list of requested revisions. This retains the reviewed route in §6; dependence on external classification data remains the 2 entries (51,8)=1 and (52,8)=0.

## 12. Responses for v3.1

| Comment | Disposition, response, and reason |
|---|---|
| C-1 | Addressed: aligned §9 and the README with the implementation; the entry point explicitly checks for 1 orbit of seventh rows, 1 class of eighth rows, candidate counts, and integer-lifting results. Classification outputs are not copied in beforehand, and missing or extra classes do not yield success. |
| C-2 | Addressed: restored in §3.1 the justification relating an arbitrary dimension-8 subcode of C with q=0 and C\D to the right-hand column, with references from §7.1 and the README. |
| C-3 | Adopted: §7.1, §9, and the README cite reviewer B's agreement in all 4 full scans and measured timings. This allows the executor, dates, environment, and distinction from an end-to-end run to be stated explicitly. |
| C-4 | Adopted: §7.1 states the derivation of the coverage counts from the MacWilliams identity and the uniqueness conditions corresponding to D0,D1,D2. This makes it easier to trace the scan coverage and the identification of representatives. |
| C-5 | Adopted: §2.1 and SOURCES state the original wording “minimum distance 24” and explain why, for k=8 and n≤54 here, it agrees with ≥24. This distinguishes the general reading of the table from the 2 entries used. |
| C-6 | Adopted: removed the author-specific search path from reassess.py. This ensures use of dependencies in the selected Python environment while preserving the pre-change code. |
| C-7 | Adopted: INDEX distinguishes the aggregate-only T=20 output of ext52x, and the code names in §5, §7.2, and other locations have relative links. This makes the descriptions of outputs and references accurate. |

As a supplement, the independent recomputation record for Kurz Table 1 is cited in §2.1 and §9. Neither the original C-final nor the included copy was changed; the additional information about verification scope is recorded in this document. Changed files and verification results are summarized in [V3.1-CHANGES.md](V3.1-CHANGES.md).

[^execution-update]: Subsequent execution update, reported by Claude: the v3 `--full` run completed successfully on 2026-10-08 at 17:08–17:22 JST in a review session. Claude's v3.1 `--full` run completed successfully on 2026-10-09 at 01:21–01:29 JST, with all 13 stages passing and `full_proof_reproduced: true`. The execution records are maintained in the public repository. These later runs were not rerun as part of this English clarification.
