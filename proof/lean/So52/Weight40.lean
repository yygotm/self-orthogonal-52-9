import So52.Weight44
import So52.FourierCoefficients

/- Necessary integer constraints for the weight-40 branch.
   This file does NOT assert that these constraints have no solutions. -/
namespace So52.Binary
open Classical

abbrev residualRange {n : ℕ} (C : Code n) (c : C) := LinearMap.range (residualMap C c)

noncomputable local instance {C : Code 52} (c : C) :
    Fintype (residualRange C c →ₗ[F₂] F₂) :=
  Fintype.ofInjective (fun g : residualRange C c →ₗ[F₂] F₂ =>
    (g : residualRange C c → F₂)) DFunLike.coe_injective

theorem residual_range_lift {n : ℕ} (C : Code n) (c : C) :
    ∃ s : residualRange C c →ₗ[F₂] C, ∀ y, residualMap C c (s y) = y.val := by
  obtain ⟨s, hs⟩ := (residualMap C c).rangeRestrict.exists_rightInverse_of_surjective
    (residualMap C c).range_rangeRestrict
  exact ⟨s, fun y => congrArg Subtype.val (LinearMap.congr_fun hs y)⟩

def rangeColumns {C : Code 52} (c : C) (s : residualRange C c →ₗ[F₂] C) :
    Inside c.val → residualRange C c →ₗ[F₂] F₂ := fun i =>
  (LinearMap.proj i.val).comp (C.subtype.comp s)

theorem range_fourier_eq {C : Code 52} (c : C)
    (s : residualRange C c →ₗ[F₂] C) (y : residualRange C c) :
    fourier (rangeColumns c s) y = (weight c.val : ℤ) - 2 * insideWeight c.val (s y).val := by
  change (∑ i : Inside c.val, sign ((s y).val i.val)) = _
  rw [sign_sum_weight, inside_card]
  rfl

theorem weight40_range_card {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 40) : Fintype.card (residualRange C c) = 128 := by
  have hr := (residual40_parameters hD hdim hmin c hc).2.1
  rw [← Nat.card_eq_fintype_card, Module.natCard_eq_pow_finrank (K := F₂), hr]
  simp [Nat.card_eq_fintype_card, F₂, ZMod.card]

theorem weight40_fourier_constraints {C : Code 52} (hD : DoublyEven C)
    (hmin : MinWeight C 24) (c : C) (hc : weight c.val = 40)
    (s : residualRange C c →ₗ[F₂] C) (hs : ∀ y, residualMap C c (s y) = y.val)
    (y : residualRange C c) (hy : y ≠ 0) :
    8 - 2 * (residualWeight y.val : ℤ) ≤ fourier (rangeColumns c s) y ∧
    fourier (rangeColumns c s) y ≤ 2 * (residualWeight y.val : ℤ) - 8 ∧
    (fourier (rangeColumns c s) y - 2 * (residualWeight y.val : ℤ)) % 8 = 0 := by
  have hy0 : y.val ≠ 0 := fun h => hy (Subtype.ext h)
  have hx0 : (s y).val ≠ 0 := by
    intro h
    apply hy0
    rw [← hs y]
    funext i
    exact congrFun h i.val
  have hxc : (s y).val + c.val ≠ 0 := by
    intro h
    have he := (add_eq_zero_iff _ _).mp h
    apply hy0
    rw [← hs y]
    funext i
    exact (congrFun he i.val).trans i.property
  have h₁ := hmin (s y).val (s y).property hx0
  have h₂ := hmin ((s y).val + c.val) (C.add_mem (s y).property c.property) hxc
  have hd := hD (s y).val (s y).property
  have hi := residual_weight_identity c (s y)
  have hw := weight_split c (s y)
  rw [hc, hs y] at hi
  rw [hs y] at hw
  rw [range_fourier_eq, hc]
  omega

/-- Necessary conditions retaining the actual section, its Fourier function,
    and its column multiplicities. No dual-distance or moment claim is made. -/
theorem weight40_integer_constraints_with_witnesses {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 40) :
    ∃ s : residualRange C c →ₗ[F₂] C,
    ∃ F : residualRange C c → ℤ, ∃ m : (residualRange C c →ₗ[F₂] F₂) → ℕ,
      (∀ y, residualMap C c (s y) = y.val) ∧
      (∀ y, F y = 40 - 2 * (insideWeight c.val (s y).val : ℤ)) ∧
      (∀ g, m g = (Finset.univ.filter fun i => rangeColumns c s i = g).card) ∧
      Fintype.card (Outside c.val) = 12 ∧
      Module.finrank F₂ (residualRange C c) = 7 ∧
      Fintype.card (residualRange C c) = 128 ∧
      (∀ y : residualRange C c, residualWeight y.val % 2 = 0) ∧
      (∀ y : residualRange C c, y ≠ 0 → 4 ≤ residualWeight y.val) ∧
      F 0 = 40 ∧
      (∀ y, y ≠ 0 →
        8 - 2 * (residualWeight y.val : ℤ) ≤ F y ∧
        F y ≤ 2 * (residualWeight y.val : ℤ) - 8 ∧
        (F y - 2 * (residualWeight y.val : ℤ)) % 8 = 0) ∧
      (∀ g, m g ≤ 40 ∧ 128 * (m g : ℤ) = ∑ y, F y * sign (g y)) ∧
      (∑ g, m g) = 40 ∧
      (∑ y, F y ^ 2) = 128 * ∑ g, (m g : ℤ) ^ 2 ∧
      128 * (40 : ℤ) ≤ ∑ y, F y ^ 2 := by
  obtain ⟨s, hs⟩ := residual_range_lift C c
  let cols := rangeColumns c s
  let m (g : residualRange C c →ₗ[F₂] F₂) : ℕ :=
    (Finset.univ.filter fun i => cols i = g).card
  obtain ⟨hlen, hrank, heven, hminimum⟩ := residual40_parameters hD hdim hmin c hc
  refine ⟨s, fourier cols, m, hs, ?_, (fun _ => rfl), hlen, hrank,
    weight40_range_card hD hdim hmin c hc,
    (fun y => heven y.val y.property), ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro y
    simpa [hc, cols] using range_fourier_eq c s y
  · intro y hy
    exact hminimum y.val y.property (fun h => hy (Subtype.ext h))
  · simp only [fourier, map_zero, sign_zero, Finset.sum_const,
      Finset.card_univ, nsmul_eq_mul, mul_one, inside_card, hc]
    norm_num
  · exact weight40_fourier_constraints hD hmin c hc s hs
  · intro g
    refine ⟨?_, ?_⟩
    · have h := Finset.card_filter_le (Finset.univ : Finset (Inside c.val)) (fun i => cols i = g)
      simp only [Finset.card_univ, inside_card, hc] at h
      exact h
    · have h := fourier_dual_coefficient (V := residualRange C c) cols g
      rw [weight40_range_card hD hdim hmin c hc] at h
      exact h.symm
  · simpa only [inside_card, hc] using column_multiplicity_sum cols
  · have h := fourier_parseval (V := residualRange C c) cols
    rw [weight40_range_card hD hdim hmin c hc,
      collisionCount_eq_sum_multiplicity_sq] at h
    simpa [Nat.cast_sum, Nat.cast_pow, m] using h
  · have h := fourier_parseval (V := residualRange C c) cols
    rw [weight40_range_card hD hdim hmin c hc] at h
    rw [h]
    have hl := collisionCount_lower (V := residualRange C c) cols
    rw [inside_card, hc] at hl
    omega

/-- The original necessary integer system, as a corollary of the witness theorem.
    Its inconsistency and reduction to normalized residual types remain unproved. -/
theorem weight40_integer_constraints {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 40) :
    ∃ F : residualRange C c → ℤ, ∃ m : (residualRange C c →ₗ[F₂] F₂) → ℕ,
      F 0 = 40 ∧
      (∀ y, y ≠ 0 →
        8 - 2 * (residualWeight y.val : ℤ) ≤ F y ∧
        F y ≤ 2 * (residualWeight y.val : ℤ) - 8 ∧
        (F y - 2 * (residualWeight y.val : ℤ)) % 8 = 0) ∧
      (∀ g, m g ≤ 40 ∧ 128 * (m g : ℤ) = ∑ y, F y * sign (g y)) ∧
      128 * (40 : ℤ) ≤ ∑ y, F y ^ 2 := by
  obtain ⟨s, F, m, hs, hF, hm, hlen, hrank, hcard, heven, hminimum,
    hzero, hbounds, hinverse, hsum, hparseval, hlower⟩ :=
    weight40_integer_constraints_with_witnesses hD hdim hmin c hc
  exact ⟨F, m, hzero, hbounds, hinverse, hlower⟩

#print axioms weight40_integer_constraints_with_witnesses
#print axioms weight40_integer_constraints
end So52.Binary
