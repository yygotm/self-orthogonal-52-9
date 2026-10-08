import So52.WeightDistribution
import So52.Fourier

namespace So52.Binary
open Classical

abbrev Inside {n : ℕ} (c : Word n) := {i : Fin n // c i ≠ 0}

theorem inside_card {n : ℕ} (c : Word n) : Fintype.card (Inside c) = weight c := by
  simp [Inside, Fintype.card_subtype, weight, support]

def insideWeight {n : ℕ} (c x : Word n) : ℕ :=
  (Finset.univ.filter fun i : Inside c => x i.val ≠ 0).card

theorem insideWeight_eq_inter {n : ℕ} (c x : Word n) :
    insideWeight c x = (support x ∩ support c).card := by
  apply Finset.card_bij (fun i _ => i.val)
  · intro i hi
    have hi' : x i.val ≠ 0 := (Finset.mem_filter.mp hi).2
    simpa [support] using And.intro hi' i.property
  · intro i hi j hj hij
    exact Subtype.ext hij
  · intro i hi
    have hi' : x i ≠ 0 ∧ c i ≠ 0 := by simpa [support] using hi
    exact ⟨⟨i, hi'.2⟩, Finset.mem_filter.mpr ⟨Finset.mem_univ _, hi'.1⟩, rfl⟩

theorem weight_split {n : ℕ} {C : Code n} (c x : C) :
    insideWeight c.val x.val + residualWeight (residualMap C c x) = weight x.val := by
  rw [insideWeight_eq_inter, residualWeight_eq_sdiff]
  exact (Nat.add_comm _ _).trans (Finset.card_sdiff_add_card_inter _ _)

theorem residualWeight_zero_iff {n : ℕ} {c : Word n} (y : Outside c → F₂) :
    residualWeight y = 0 ↔ y = 0 := by
  simp only [residualWeight, Finset.card_eq_zero, Finset.filter_eq_empty_iff]
  constructor
  · intro h
    funext i
    by_contra hi
    exact h (Finset.mem_univ i) hi
  · intro h
    simp [h]

/-- A linear lift exists because the residual image is the entire even space. -/
theorem residual44_lift {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 44) :
    ∃ s : evenSpace (Outside c.val) →ₗ[F₂] C,
      ∀ y, residualMap C c (s y) = y.val := by
  let f : C →ₗ[F₂] evenSpace (Outside c.val) :=
    (residualMap C c).codRestrict _ (fun x => by
      rw [← residual44_eq_evenSpace hD hdim hmin c hc]
      exact LinearMap.mem_range_self _ x)
  have hf : Function.Surjective f := by
    intro y
    have hy : y.val ∈ LinearMap.range (residualMap C c) := by
      simpa only [residual44_eq_evenSpace hD hdim hmin c hc] using y.property
    obtain ⟨x, hx⟩ := hy
    exact ⟨x, Subtype.ext hx⟩
  obtain ⟨s, hs⟩ := f.exists_rightInverse_of_surjective (LinearMap.range_eq_top.mpr hf)
  refine ⟨s, fun y => ?_⟩
  exact congrArg Subtype.val (LinearMap.congr_fun hs y)

def insideColumns {C : Code 52} (c : C)
    (s : evenSpace (Outside c.val) →ₗ[F₂] C) :
    Inside c.val → evenSpace (Outside c.val) →ₗ[F₂] F₂ := fun i =>
  (LinearMap.proj i.val).comp (C.subtype.comp s)

theorem inside_fourier_eq {C : Code 52} (c : C)
    (s : evenSpace (Outside c.val) →ₗ[F₂] C) (y : evenSpace (Outside c.val)) :
    fourier (insideColumns c s) y = (weight c.val : ℤ) - 2 * insideWeight c.val (s y).val := by
  change (∑ i : Inside c.val, sign ((s y).val i.val)) = _
  rw [sign_sum_weight, inside_card]
  rfl

theorem weight44_fourier_bound {C : Code 52} (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 44)
    (s : evenSpace (Outside c.val) →ₗ[F₂] C)
    (hs : ∀ y, residualMap C c (s y) = y.val) (y : evenSpace (Outside c.val)) :
    fourier (insideColumns c s) y ^ 2 ≤ weight44Bound (residualWeight y.val) := by
  rw [inside_fourier_eq, hc]
  by_cases hz : residualWeight y.val = 0
  · have hy : y = 0 := Subtype.ext ((residualWeight_zero_iff y.val).mp hz)
    subst y
    simp [insideWeight, weight44Bound, residualWeight]
  · have hy : y.val ≠ 0 := fun h => hz ((residualWeight_zero_iff y.val).mpr h)
    have hx : (s y).val ≠ 0 := by
      intro h
      apply hy
      rw [← hs y]
      funext i
      exact congrFun h i.val
    have hxc : (s y).val + c.val ≠ 0 := by
      intro h
      have he := (add_eq_zero_iff _ _).mp h
      apply hy
      rw [← hs y]
      funext i
      exact (congrFun he i.val).trans i.property
    have h₁ := hmin (s y).val (s y).property hx
    have h₂ := hmin ((s y).val + c.val) (C.add_mem (s y).property c.property) hxc
    have hsplit := weight_split c (s y)
    have hid := residual_weight_identity c (s y)
    rw [hs y] at hsplit hid
    rw [hc] at hid
    rw [weight44Bound, ite_eq_right hz]
    have hlow : -(2 * (residualWeight y.val : ℤ) - 4) ≤
        44 - 2 * (insideWeight c.val (s y).val : ℤ) := by omega
    have hupp : 44 - 2 * (insideWeight c.val (s y).val : ℤ) ≤
        2 * (residualWeight y.val : ℤ) - 4 := by omega
    exact sq_le_sq' hlow hupp

/-- No word of weight 44 exists in a doubly-even length-52, dimension-8
    code whose nonzero words have weight at least 24. -/
theorem no_weight44 {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) : weight c.val ≠ 44 := by
  intro hc
  obtain ⟨s, hs⟩ := residual44_lift hD hdim hmin c hc
  have hout : Fintype.card (Outside c.val) = 8 := by rw [outside_card, hc]
  have : Nonempty (Outside c.val) := Fintype.card_pos_iff.mp (by omega)
  have hrank : Module.finrank F₂ (evenSpace (Outside c.val)) = 7 := by
    have h := evenSpace_finrank (ι := Outside c.val)
    omega
  have hcard : Fintype.card (evenSpace (Outside c.val)) = 128 := by
    rw [← Nat.card_eq_fintype_card, Module.natCard_eq_pow_finrank (K := F₂), hrank]
    simp [Nat.card_eq_fintype_card, F₂, ZMod.card]
  have hlower : 44 ≤ collisionCount (insideColumns c s) := by
    have h := collisionCount_lower (insideColumns c s)
    rwa [inside_card, hc] at h
  have hp := fourier_parseval (insideColumns c s)
  rw [hcard] at hp
  have hupper := Finset.sum_le_sum (fun y (_ : y ∈ Finset.univ) =>
    weight44_fourier_bound hmin c hc s hs y)
  have hb := even8_bound_sum hout
  change (∑ y : evenSpace (Outside c.val), weight44Bound (residualWeight y.val)) = _ at hb
  rw [hb, hp] at hupper
  apply So52.Support.weight44_parseval_contradiction (collisionCount (insideColumns c s)) hlower
  exact_mod_cast hupper

#print axioms residual44_lift
#print axioms weight44_fourier_bound
#print axioms no_weight44
end So52.Binary
