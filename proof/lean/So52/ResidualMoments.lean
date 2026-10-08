import So52.ResidualDual

/- First and second weight moments, derived from the dual distance via
   character orthogonality. Sums include the zero codeword. -/
namespace So52.Binary
open Classical
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def coordinateForms (R : Submodule F₂ (ι → F₂)) (i : ι) : R →ₗ[F₂] F₂ :=
  (LinearMap.proj i).comp R.subtype

theorem binaryWeight_single_le (i : ι) : binaryWeight (Pi.single i (1 : F₂)) ≤ 1 := by
  have hs : (Finset.univ.filter fun k => (Pi.single i 1 : ι → F₂) k ≠ 0) = {i} := by
    ext k
    by_cases h : k = i <;> simp [h]
  simp only [binaryWeight, hs, Finset.card_singleton, le_refl]

theorem dotMap_left_single (i : ι) (x : ι → F₂) :
    dotMap (Pi.single i 1) x = x i := by simp [dotMap, Pi.single_apply]

theorem dual_distance_coordinateForms (R : Submodule F₂ (ι → F₂))
    (hd : ∀ z : binaryDual R, z ≠ 0 → 3 ≤ binaryWeight z.val) :
    (∀ i, coordinateForms R i ≠ 0) ∧ Function.Injective (coordinateForms R) := by
  constructor
  · intro i hi
    have hz : Pi.single i (1 : F₂) ∈ binaryDual R := by
      intro x
      rw [dotMap_left_single]
      exact LinearMap.congr_fun hi x
    have hn : (⟨Pi.single i 1, hz⟩ : binaryDual R) ≠ 0 := by
      intro h
      have he := congrFun (congrArg Subtype.val h) i
      simp at he
    have hl := hd ⟨_, hz⟩ hn
    have hu := binaryWeight_single_le i
    have hbad : 3 ≤ 1 := hl.trans hu
    omega
  · intro i j hij
    by_contra hn
    let z : ι → F₂ := Pi.single i 1 - Pi.single j 1
    have hz : z ∈ binaryDual R := by
      intro x
      have he : x.val i = x.val j := LinearMap.congr_fun hij x
      simp [z, dotMap, sub_mul, Finset.sum_sub_distrib, Pi.single_apply, he]
    have hz0 : (⟨z, hz⟩ : binaryDual R) ≠ 0 := by
      intro h
      have he := congrFun (congrArg Subtype.val h) i
      simp [z, hn] at he
    have hl := hd ⟨z, hz⟩ hz0
    have hu : binaryWeight z ≤ 2 :=
      binaryWeight_sub_le_two (Pi.single i 1) (Pi.single j 1) j i (add_comm _ _)
    have hbad : 3 ≤ 2 := hl.trans hu
    omega

omit [DecidableEq ι] in
theorem projective_fourier_sum (R : Submodule F₂ (ι → F₂))
    [Fintype R]
    (hn : ∀ i, coordinateForms R i ≠ 0) :
    ∑ x : R, fourier (coordinateForms R) x = 0 := by
  unfold fourier
  rw [Finset.sum_comm]
  simp [character_sum, hn]

omit [DecidableEq ι] in
theorem projective_fourier_square_sum (R : Submodule F₂ (ι → F₂))
    [Fintype R]
    (hi : Function.Injective (coordinateForms R)) :
    ∑ x : R, fourier (coordinateForms R) x ^ 2 =
      (Fintype.card R : ℤ) * Fintype.card ι := by
  rw [fourier_parseval]
  have hc : collisionCount (coordinateForms R) = Fintype.card ι := by
    have hfilter (i : ι) :
        (Finset.univ.filter fun j => coordinateForms R i = coordinateForms R j) = {i} := by
      ext j
      simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_singleton]
      exact hi.eq_iff.trans eq_comm
    simp only [collisionCount, hfilter, Finset.card_singleton, Finset.sum_const,
      Finset.card_univ, smul_eq_mul, mul_one]
  rw [hc]

/-- The moments of any projective binary code of length 12 and size 128. -/
theorem length12_card128_weight_moments (R : Submodule F₂ (ι → F₂))
    [Fintype R]
    (hlen : Fintype.card ι = 12) (hcard : Fintype.card R = 128)
    (hd : ∀ z : binaryDual R, z ≠ 0 → 3 ≤ binaryWeight z.val) :
    (∑ x : R, binaryWeight x.val) = 768 ∧
      (∑ x : R, binaryWeight x.val ^ 2) = 4992 := by
  obtain ⟨hn, hi⟩ := dual_distance_coordinateForms R hd
  have hfirst := projective_fourier_sum R hn
  have hsecond := projective_fourier_square_sum R hi
  have hf (x : R) : fourier (coordinateForms R) x =
      12 - 2 * (binaryWeight x.val : ℤ) := by
    have h := sign_sum_weight x.val
    rw [hlen] at h
    exact h
  simp_rw [hf] at hfirst hsecond
  rw [hlen, hcard] at hsecond
  have hsum : (∑ x : R, (binaryWeight x.val : ℤ)) = 768 := by
    simp only [Finset.sum_sub_distrib, ← Finset.mul_sum, Finset.sum_const,
      Finset.card_univ, hcard, nsmul_eq_mul] at hfirst
    omega
  have hsquare : (∑ x : R, (binaryWeight x.val : ℤ) ^ 2) = 4992 := by
    have hexpand (x : R) : (12 - 2 * (binaryWeight x.val : ℤ)) ^ 2 =
        144 - 48 * (binaryWeight x.val : ℤ) + 4 * (binaryWeight x.val : ℤ) ^ 2 := by ring
    simp_rw [hexpand] at hsecond
    simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum,
      Finset.sum_const, Finset.card_univ, hcard, nsmul_eq_mul, hsum] at hsecond
    omega
  constructor
  · exact_mod_cast hsum
  · exact_mod_cast hsquare

theorem weight40_residual_moments {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 40) :
    (∑ y : residualRange C c, residualWeight y.val) = 768 ∧
      (∑ y : residualRange C c, residualWeight y.val ^ 2) = 4992 := by
  have hlen := (residual40_parameters hD hdim hmin c hc).1
  have hcard := weight40_range_card hD hdim hmin c hc
  have hd := weight40_residual_dual_minWeight hD hdim hmin c hc
  exact length12_card128_weight_moments (residualRange C c) hlen hcard hd

#print axioms weight40_residual_moments
end So52.Binary
