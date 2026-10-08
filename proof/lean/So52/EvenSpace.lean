import So52.Residual
import Mathlib.LinearAlgebra.Pi

namespace So52.Binary

variable {ι : Type*} [Fintype ι]

def parityMap : (ι → F₂) →ₗ[F₂] F₂ where
  toFun y := ∑ i, y i
  map_add' y z := Finset.sum_add_distrib
  map_smul' a y := by simp [Finset.mul_sum]

def evenSpace (ι : Type*) [Fintype ι] : Submodule F₂ (ι → F₂) :=
  LinearMap.ker parityMap

theorem parity_eq_weight (y : ι → F₂) :
    parityMap y = ((Finset.univ.filter fun i => y i ≠ 0).card : F₂) := by
  have h : ∀ a : F₂, a = if a ≠ 0 then 1 else 0 := by decide
  change (∑ i, y i) = _
  conv_lhs => arg 2; ext i; rw [h (y i)]
  rw [← Finset.sum_filter]
  simp

theorem mem_evenSpace (y : ι → F₂) :
    y ∈ evenSpace ι ↔ (Finset.univ.filter fun i => y i ≠ 0).card % 2 = 0 := by
  change parityMap y = 0 ↔ _
  rw [parity_eq_weight, ZMod.natCast_eq_zero_iff, Nat.dvd_iff_mod_eq_zero]

theorem parity_surjective [Nonempty ι] : Function.Surjective (parityMap (ι := ι)) := by
  classical
  intro a
  obtain ⟨i⟩ := ‹Nonempty ι›
  exact ⟨Pi.single i a, by simp [parityMap]⟩

theorem evenSpace_finrank [Nonempty ι] :
    Module.finrank F₂ (evenSpace ι) + 1 = Fintype.card ι := by
  have h := (parityMap (ι := ι)).finrank_range_add_finrank_ker
  rw [LinearMap.range_eq_top.mpr parity_surjective, finrank_top,
    Module.finrank_self, Module.finrank_pi] at h
  change 1 + Module.finrank F₂ (evenSpace ι) = Fintype.card ι at h
  omega

theorem residual44_eq_evenSpace {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 44) :
    LinearMap.range (residualMap C c) = evenSpace (Outside c.val) := by
  obtain ⟨hl, hk, he, _⟩ := residual44_parameters hD hdim hmin c hc
  have : Nonempty (Outside c.val) := Fintype.card_pos_iff.mp (by omega)
  apply Submodule.eq_of_le_of_finrank_eq
  · intro y hy
    exact (mem_evenSpace y).mpr (he y hy)
  · have hd := evenSpace_finrank (ι := Outside c.val)
    omega

#print axioms residual44_eq_evenSpace
end So52.Binary
