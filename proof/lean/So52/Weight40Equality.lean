import So52.ResidualMoments

/- Equality in the inner Parseval bound (PROOF, section 4, weight-40 case,
   the Parseval equality paragraph).
   No residual classification, cubic reduction, or enumeration is used. -/
namespace So52.Binary
open Classical

/-- Arithmetic saturation of the two moment bounds. All sums include zero. -/
theorem weight40_moment_saturation
    {α β : Type*} [Fintype α] [Zero α] [DecidableEq α] [Fintype β]
    (j : α → ℕ) (F : α → ℤ) (m : β → ℕ)
    (hcard : Fintype.card α = 128) (hj0 : j 0 = 0)
    (hj1 : ∑ y, j y = 768) (hj2 : ∑ y, j y ^ 2 = 4992)
    (hF0 : F 0 = 40)
    (hb : ∀ y, y ≠ 0 → 8 - 2 * (j y : ℤ) ≤ F y ∧ F y ≤ 2 * (j y : ℤ) - 8)
    (hm : ∑ g, m g = 40)
    (hp : (∑ y, F y ^ 2) = 128 * ∑ g, (m g : ℤ) ^ 2) :
    (∑ y, F y ^ 2) = 5120 ∧
    (∑ g, (m g : ℤ) ^ 2) = 40 ∧
    (∀ g, m g = 0 ∨ m g = 1) ∧
    (∀ y, y ≠ 0 → F y = 2 * (j y : ℤ) - 8 ∨ F y = -(2 * (j y : ℤ) - 8)) ∧
    (∀ y, y ≠ 0 → |F y| = 2 * (j y : ℤ) - 8) := by
  let U (y : α) : ℤ := if y = 0 then 1600 else (2 * (j y : ℤ) - 8) ^ 2
  have hle (y : α) : F y ^ 2 ≤ U y := by
    by_cases hy : y = 0
    · subst y
      simp [U, hF0]
    · obtain ⟨hl, hu⟩ := hb y hy
      have ht := mul_nonneg (sub_nonneg.mpr hl) (sub_nonneg.mpr hu)
      simp only [U, ite_eq_right hy]
      nlinarith
  have hj1z : (∑ y, (j y : ℤ)) = 768 := by exact_mod_cast hj1
  have hj2z : (∑ y, (j y : ℤ) ^ 2) = 4992 := by exact_mod_cast hj2
  have hU (y : α) : U y =
      4 * (j y : ℤ) ^ 2 - 32 * (j y : ℤ) + 64 + (if y = 0 then 1536 else 0) := by
    by_cases hy : y = 0
    · subst y
      norm_num [U, hj0]
    · simp only [U, ite_eq_right hy]
      ring
  have hUsum : (∑ y, U y) = 5120 := by
    simp_rw [hU]
    simp [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum,
      hj1z, hj2z, hcard]
  have hupper : (∑ y, F y ^ 2) ≤ 5120 := by
    rw [← hUsum]
    exact Finset.sum_le_sum (fun y _ => hle y)
  have hmsq (g : β) : (m g : ℤ) ≤ (m g : ℤ) ^ 2 := by
    have hn : (0 : ℤ) ≤ m g := Int.natCast_nonneg _
    by_cases hz : m g = 0
    · simp [hz]
    · have ho : (1 : ℤ) ≤ m g := by exact_mod_cast Nat.one_le_iff_ne_zero.mpr hz
      nlinarith
  have hmz : (∑ g, (m g : ℤ)) = 40 := by exact_mod_cast hm
  have hmlower : (40 : ℤ) ≤ ∑ g, (m g : ℤ) ^ 2 := by
    rw [← hmz]
    exact Finset.sum_le_sum (fun g _ => hmsq g)
  have htotal : (∑ y, F y ^ 2) = 5120 := by omega
  have hmsum : (∑ g, (m g : ℤ) ^ 2) = 40 := by omega
  have hpoint (y : α) : F y ^ 2 = U y :=
    (Finset.sum_eq_sum_iff_of_le (fun y _ => hle y)).mp
      (htotal.trans hUsum.symm) y (Finset.mem_univ y)
  have hbinary (g : β) : m g = 0 ∨ m g = 1 := by
    have he : (m g : ℤ) = (m g : ℤ) ^ 2 :=
      (Finset.sum_eq_sum_iff_of_le (fun g _ => hmsq g)).mp
        (hmz.trans hmsum.symm) g (Finset.mem_univ g)
    have hn : (0 : ℤ) ≤ m g := Int.natCast_nonneg _
    have hu : (m g : ℤ) ≤ 1 := by nlinarith
    have hu' : m g ≤ 1 := by exact_mod_cast hu
    omega
  have hend (y : α) (hy : y ≠ 0) :
      F y = 2 * (j y : ℤ) - 8 ∨ F y = -(2 * (j y : ℤ) - 8) := by
    have he := hpoint y
    simp only [U, ite_eq_right hy] at he
    have hz : (F y - (2 * (j y : ℤ) - 8)) * (F y + (2 * (j y : ℤ) - 8)) = 0 := by
      nlinarith
    rcases mul_eq_zero.mp hz with h | h
    · left; linarith
    · right; linarith
  refine ⟨htotal, hmsum, hbinary, hend, ?_⟩
  intro y hy
  have hb' := hb y hy
  have hn : (0 : ℤ) ≤ 2 * (j y : ℤ) - 8 := by omega
  rcases hend y hy with h | h
  · rw [h, abs_of_nonneg hn]
  · rw [h, abs_neg, abs_of_nonneg hn]

noncomputable local instance {C : Code 52} (c : C) :
    Fintype (residualRange C c →ₗ[F₂] F₂) :=
  Fintype.ofInjective (fun g : residualRange C c →ₗ[F₂] F₂ =>
    (g : residualRange C c → F₂)) DFunLike.coe_injective

/-- Actual sections and column multiplicities attain the inner Parseval bound.
    Only the original four code hypotheses are required. -/
theorem weight40_parseval_equality_with_witnesses {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 40) :
    ∃ s : residualRange C c →ₗ[F₂] C,
    ∃ F : residualRange C c → ℤ, ∃ m : (residualRange C c →ₗ[F₂] F₂) → ℕ,
      (∀ y, residualMap C c (s y) = y.val) ∧
      (∀ y, F y = 40 - 2 * (insideWeight c.val (s y).val : ℤ)) ∧
      (∀ g, m g = (Finset.univ.filter fun i => rangeColumns c s i = g).card) ∧
      F 0 = 40 ∧
      (∀ g, 128 * (m g : ℤ) = ∑ y, F y * sign (g y)) ∧
      (∑ g, m g) = 40 ∧
      (∑ y, F y ^ 2) = 5120 ∧
      (∑ g, (m g : ℤ) ^ 2) = 40 ∧
      (∀ g, m g = 0 ∨ m g = 1) ∧
      (∀ y, y ≠ 0 → F y = 2 * (residualWeight y.val : ℤ) - 8 ∨
        F y = -(2 * (residualWeight y.val : ℤ) - 8)) ∧
      (∀ y, y ≠ 0 → |F y| = 2 * (residualWeight y.val : ℤ) - 8) := by
  obtain ⟨s, F, m, hs, hF, hm, _, _, hcard, _, _, hzero, hbounds,
    hinverse, hsum, hparseval, _⟩ :=
    weight40_integer_constraints_with_witnesses hD hdim hmin c hc
  obtain ⟨hj1, hj2⟩ := weight40_residual_moments hD hdim hmin c hc
  have hj0 : residualWeight (0 : residualRange C c).val = 0 := by
    simp [residualWeight]
  have heq := weight40_moment_saturation (fun y : residualRange C c => residualWeight y.val)
    F m hcard hj0 hj1 hj2 hzero (fun y hy => ⟨(hbounds y hy).1, (hbounds y hy).2.1⟩)
    hsum hparseval
  exact ⟨s, F, m, hs, hF, hm, hzero, (fun g => (hinverse g).2), hsum, heq⟩

#print axioms weight40_moment_saturation
#print axioms weight40_parseval_equality_with_witnesses
end So52.Binary
