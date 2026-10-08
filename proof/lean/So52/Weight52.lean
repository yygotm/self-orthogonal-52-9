import So52.Weight44

namespace So52.Binary
open Classical

def codeColumns {n : ℕ} (C : Code n) : Fin n → C →ₗ[F₂] F₂ := fun i =>
  (LinearMap.proj i).comp C.subtype

theorem code_fourier_eq {n : ℕ} {C : Code n} (x : C) :
    fourier (codeColumns C) x = (n : ℤ) - 2 * weight x.val := by
  change (∑ i, sign (x.val i)) = _
  rw [sign_sum_weight]
  simp [weight, support]

theorem weight52_complement {C : Code 52} (c : C) (hc : weight c.val = 52) (x : C) :
    weight x.val + weight (x.val + c.val) = 52 := by
  have hcard : Fintype.card (Outside c.val) = 0 := by rw [outside_card, hc]
  have : IsEmpty (Outside c.val) := Fintype.card_eq_zero_iff.mp hcard
  have h := residual_weight_identity c x
  simpa [residualWeight, hc] using h

theorem weight52_fourier_sq {C : Code 52} (hD : DoublyEven C) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 52) (x : C) :
    fourier (codeColumns C) x ^ 2 =
      16 + (if x = 0 then 2688 else 0) + (if x = c then 2688 else 0) := by
  have hc0 : c ≠ 0 := by
    intro h
    have h' : c.val = 0 := congrArg Subtype.val h
    rw [h', weight_zero] at hc
    omega
  rw [code_fourier_eq]
  by_cases hx0 : x = 0
  · subst x
    simp [Ne.symm hc0]
  · by_cases hxc : x = c
    · subst x
      simp [hc, hc0]
    · rw [ite_eq_right hx0, ite_eq_right hxc]
      have hx : x.val ≠ 0 := fun h => hx0 (Subtype.ext h)
      have hxc' : x.val + c.val ≠ 0 := fun h => hxc (Subtype.ext ((add_eq_zero_iff _ _).mp h))
      have h₁ := hmin x.val x.property hx
      have h₂ := hmin (x.val + c.val) (C.add_mem x.property c.property) hxc'
      have hd := hD x.val x.property
      have hsum := weight52_complement c hc x
      have hw : weight x.val = 24 ∨ weight x.val = 28 := by omega
      rcases hw with hw | hw <;> rw [hw] <;> norm_num

/-- The full-support branch is excluded without a general code bound or a classification. -/
theorem no_weight52 {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) : weight c.val ≠ 52 := by
  intro hc
  have hcard : Fintype.card C = 256 := by
    rw [← Nat.card_eq_fintype_card, Module.natCard_eq_pow_finrank (K := F₂), hdim]
    simp [Nat.card_eq_fintype_card, F₂, ZMod.card]
  have hp := fourier_parseval (codeColumns C)
  rw [hcard] at hp
  have hsum : (∑ x : C, fourier (codeColumns C) x ^ 2) = 2 * (52^2 + 127*16) := by
    simp_rw [weight52_fourier_sq hD hmin c hc]
    simp [Finset.sum_add_distrib, hcard]
  have hlower : 52 ≤ collisionCount (codeColumns C) := by
    simpa using collisionCount_lower (codeColumns C)
  apply So52.Support.weight52_parseval_contradiction (collisionCount (codeColumns C)) hlower
  omega

#print axioms weight52_fourier_sq
#print axioms no_weight52
end So52.Binary
