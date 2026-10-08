import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.SymmDiff
import Lean.Elab.Tactic.Omega

/- Support sets model binary vectors. Symmetric difference is addition over F₂.
   These are local lemmas, not a classification or a nonexistence theorem. -/
namespace So52.Support
variable {α : Type*} [DecidableEq α]
open scoped symmDiff

theorem weight_identity (s t : Finset α) :
    (s ∆ t).card + 2 * (s ∩ t).card = s.card + t.card := by
  rw [Finset.symmDiff_def, Finset.card_union_of_disjoint disjoint_sdiff_sdiff]
  have h₁ := Finset.card_sdiff_add_card_inter s t
  have h₂ := Finset.card_sdiff_add_card_inter t s
  rw [Finset.inter_comm t s] at h₂
  omega

/-- Section 3: half the weight modulo 2 is additive on self-orthogonal words. -/
theorem half_weight_add (s t : Finset α)
    (hs : s.card % 2 = 0) (ht : t.card % 2 = 0)
    (hst : (s ∩ t).card % 2 = 0) :
    ((s ∆ t).card / 2) % 2 = (s.card / 2 + t.card / 2) % 2 := by
  have hw := weight_identity s t
  omega

/-- The weight of a nonzero doubly-even word of weight at least 22 is at least 24. -/
theorem doubly_even_lower (w : Nat) (hmin : 22 ≤ w) (hdiv : w % 4 = 0) :
    24 ≤ w := by omega

/-- Section 4: a word other than 0,c cannot lie in the residual kernel when wt(c)<48. -/
theorem residual_kernel_obstruction (s c : Finset α) (hsub : s ⊆ c)
    (hs : 24 ≤ s.card) (hsc : 24 ≤ (s ∆ c).card) (hc : c.card < 48) : False := by
  have hw := weight_identity s c
  rw [Finset.inter_eq_left.mpr hsub] at hw
  omega

def transvection (s h : Finset α) : Finset α :=
  if (s ∩ h).card % 2 = 1 then s ∆ h else s

/-- Section 7: weight-six transvections preserve weight modulo four. -/
theorem transvection_mod_four (s h : Finset α) (hh : h.card = 6) :
    (transvection s h).card % 4 = s.card % 4 := by
  have hw := weight_identity s h
  unfold transvection
  split_ifs with hp
  · omega
  · rfl

theorem transvection_weight_bound (s h : Finset α) (hh : h.card = 6) :
    (transvection s h).card ≤ s.card + 4 ∧
    s.card ≤ (transvection s h).card + 4 := by
  have hw := weight_identity s h
  have hi : (s ∩ h).card ≤ h.card := Finset.card_le_card Finset.inter_subset_right
  unfold transvection
  split_ifs with hp
  · omega
  · omega

theorem inverse_cutoff (s h : Finset α) (hh : h.card = 6)
    (hmin : 22 ≤ (transvection s h).card) : 18 ≤ s.card := by
  have hb := transvection_weight_bound s h hh
  omega

/-- Exact acceptance condition for a weight-18 word. -/
theorem weight18_test (s h : Finset α) (hh : h.card = 6) (hs : s.card = 18) :
    22 ≤ (transvection s h).card ↔ (s ∩ h).card = 1 := by
  have hw := weight_identity s h
  unfold transvection
  split_ifs with hp <;> omega

/-- Exact acceptance condition for a weight-22 word. -/
theorem weight22_test (s h : Finset α) (hh : h.card = 6) (hs : s.card = 22) :
    22 ≤ (transvection s h).card ↔ (s ∩ h).card ≠ 5 := by
  have hw := weight_identity s h
  have hi : (s ∩ h).card ≤ h.card := Finset.card_le_card Finset.inter_subset_right
  unfold transvection
  split_ifs with hp <;> omega

theorem weight26_safe (s h : Finset α) (hh : h.card = 6) (hs : 26 ≤ s.card) :
    22 ≤ (transvection s h).card := by
  have hb := transvection_weight_bound s h hh
  omega

/-- Arithmetic endpoint only: the Fourier/Parseval identity is an explicit hypothesis. -/
theorem weight52_parseval_contradiction (sumSquares : Nat)
    (integer_bound : 52 ≤ sumSquares)
    (parseval : 128 * sumSquares = 52^2 + 127 * 16) : False := by omega

theorem weight44_parseval_contradiction (sumSquares : Nat)
    (integer_bound : 44 ≤ sumSquares)
    (parseval : 128 * sumSquares ≤ 44^2 + 70*16 + 28*64 + 144) : False := by omega

#print axioms weight_identity
#print axioms half_weight_add
#print axioms residual_kernel_obstruction
#print axioms transvection_mod_four
#print axioms transvection_weight_bound
#print axioms inverse_cutoff
#print axioms weight18_test
#print axioms weight22_test
#print axioms weight26_safe
#print axioms weight52_parseval_contradiction
#print axioms weight44_parseval_contradiction
end So52.Support
