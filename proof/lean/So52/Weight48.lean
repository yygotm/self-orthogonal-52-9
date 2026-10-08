import So52.Weight52
import So52.FourierCoefficients
import Mathlib.Tactic.IntervalCases

namespace So52.Binary
open Classical

abbrev residualKernel {n : ℕ} (C : Code n) (c : C) :=
  LinearMap.ker (residualMap C c)

def kernelWord {n : ℕ} {C : Code n} (c : C) : residualKernel C c :=
  ⟨c, (mem_residual_ker_iff c c).mpr (Finset.Subset.refl _)⟩

def kernelColumns {C : Code 52} (c : C) :
    Inside c.val → residualKernel C c →ₗ[F₂] F₂ := fun i =>
  (LinearMap.proj i.val).comp (C.subtype.comp (residualKernel C c).subtype)

theorem kernel_insideWeight {C : Code 52} (c : C) (x : residualKernel C c) :
    insideWeight c.val x.val.val = weight x.val.val := by
  have h := weight_split c x.val
  have hx : residualMap C c x.val = 0 := x.property
  rw [hx] at h
  simpa [residualWeight] using h

theorem kernel_fourier_eq {C : Code 52} (c : C) (x : residualKernel C c) :
    fourier (kernelColumns c) x = (weight c.val : ℤ) - 2 * weight x.val.val := by
  change (∑ i : Inside c.val, sign (x.val.val i.val)) = _
  rw [sign_sum_weight, inside_card]
  change _ - 2 * (insideWeight c.val x.val.val : ℤ) = _
  rw [kernel_insideWeight]

theorem weight48_kernel_weight {C : Code 52} (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 48) (x : residualKernel C c)
    (hx0 : x ≠ 0) (hxc : x ≠ kernelWord c) : weight x.val.val = 24 := by
  have hx : x.val.val ≠ 0 := fun h => hx0 (Subtype.ext (Subtype.ext h))
  have hxc' : x.val.val + c.val ≠ 0 := fun h =>
    hxc (Subtype.ext (Subtype.ext ((add_eq_zero_iff _ _).mp h)))
  have h₁ := hmin x.val.val x.val.property hx
  have h₂ := hmin (x.val.val + c.val) (C.add_mem x.val.property c.property) hxc'
  have hid := residual_weight_identity c x.val
  have hker : residualMap C c x.val = 0 := x.property
  rw [hker, hc] at hid
  simp [residualWeight] at hid
  omega

theorem weight48_kernel_fourier {C : Code 52} (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 48) (x : residualKernel C c) :
    fourier (kernelColumns c) x =
      (if x = 0 then 48 else 0) - (if x = kernelWord c then 48 else 0) := by
  have hc0 : kernelWord c ≠ 0 := by
    intro h
    have h' : c.val = 0 := congrArg (fun x : residualKernel C c => x.val.val) h
    rw [h', weight_zero] at hc
    omega
  rw [kernel_fourier_eq, hc]
  by_cases hx0 : x = 0
  · subst x
    simp [Ne.symm hc0]
  · by_cases hxc : x = kernelWord c
    · subst x
      rw [ite_eq_right hc0, ite_eq_left rfl]
      change (48 : ℤ) - 2 * (weight c.val : ℤ) = 0 - 48
      rw [hc]
      norm_num
    · rw [weight48_kernel_weight hmin c hc x hx0 hxc]
      simp [hx0, hxc]

theorem weight48_column_multiplicity {C : Code 52} (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 48) (i : Inside c.val) :
    (Fintype.card (residualKernel C c) : ℤ) *
      (Finset.univ.filter fun j => kernelColumns c j = kernelColumns c i).card = 96 := by
  have hcoef := fourier_column_coefficient (V := residualKernel C c) (kernelColumns c) i
  rw [← hcoef]
  simp_rw [weight48_kernel_fourier hmin c hc, sub_mul, Finset.sum_sub_distrib,
    ite_mul, zero_mul]
  have hci : c.val i.val = 1 := by
    have h : ∀ a : F₂, a ≠ 0 → a = 1 := by decide
    exact h _ i.property
  rw [Finset.sum_ite_eq', Finset.sum_ite_eq']
  simp [kernelColumns, kernelWord, sign, hci]

theorem weight48_kernel_rank_bounds {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (c : C) (hc : weight c.val = 48) :
    5 ≤ Module.finrank F₂ (residualKernel C c) ∧
      Module.finrank F₂ (residualKernel C c) ≤ 8 := by
  have hout : Fintype.card (Outside c.val) = 4 := by rw [outside_card, hc]
  have : Nonempty (Outside c.val) := Fintype.card_pos_iff.mp (by omega)
  have hle : LinearMap.range (residualMap C c) ≤ evenSpace (Outside c.val) := by
    intro y hy
    exact (mem_evenSpace y).mpr (residual_even (doublyEven_selfOrthogonal hD) c y hy)
  have hdimle := Submodule.finrank_mono hle
  have heven := evenSpace_finrank (ι := Outside c.val)
  have hsum := (residualMap C c).finrank_range_add_finrank_ker
  change _ + Module.finrank F₂ (residualKernel C c) = _ at hsum
  omega

theorem weight48_kernel_structure {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 48) :
    Module.finrank F₂ (residualKernel C c) = 5 ∧
      (∀ i : Inside c.val,
        (Finset.univ.filter fun j => kernelColumns c j = kernelColumns c i).card = 3) ∧
      LinearMap.range (residualMap C c) = evenSpace (Outside c.val) := by
  have ⟨hlo, hhi⟩ := weight48_kernel_rank_bounds hD hdim c hc
  have hcard : Fintype.card (residualKernel C c) =
      2 ^ Module.finrank F₂ (residualKernel C c) := by
    rw [← Nat.card_eq_fintype_card, Module.natCard_eq_pow_finrank (K := F₂)]
    simp [Nat.card_eq_fintype_card, F₂, ZMod.card]
  have hni : Nonempty (Inside c.val) := Fintype.card_pos_iff.mp (by rw [inside_card, hc]; decide)
  obtain ⟨i⟩ := hni
  have hm := weight48_column_multiplicity hmin c hc i
  rw [hcard] at hm
  have hrank : Module.finrank F₂ (residualKernel C c) = 5 := by
    interval_cases hr : Module.finrank F₂ (residualKernel C c) <;> norm_num [hr] at hm ⊢ <;> omega
  refine ⟨hrank, ?_, ?_⟩
  · intro j
    have hj := weight48_column_multiplicity hmin c hc j
    rw [hcard, hrank] at hj
    norm_num at hj
    omega
  · have hout : Fintype.card (Outside c.val) = 4 := by rw [outside_card, hc]
    have : Nonempty (Outside c.val) := Fintype.card_pos_iff.mp (by omega)
    apply Submodule.eq_of_le_of_finrank_eq
    · intro y hy
      exact (mem_evenSpace y).mpr (residual_even (doublyEven_selfOrthogonal hD) c y hy)
    · have hsum := (residualMap C c).finrank_range_add_finrank_ker
      have heven := evenSpace_finrank (ι := Outside c.val)
      change _ + Module.finrank F₂ (residualKernel C c) = _ at hsum
      omega

#print axioms weight48_kernel_structure
end So52.Binary
