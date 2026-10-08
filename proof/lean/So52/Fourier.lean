import So52.Kernel
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/- Integer-valued character orthogonality and Parseval for a multiset of
   binary linear coordinate functionals. No analytic Fourier axioms or
   externally computed identities are used. -/
namespace So52.Binary
open Classical

def sign (a : F₂) : ℤ := if a = 0 then 1 else -1

@[simp] theorem sign_zero : sign 0 = 1 := by decide
theorem sign_add (a b : F₂) : sign (a + b) = sign a * sign b := by
  have h : ∀ a b : F₂, sign (a + b) = sign a * sign b := by decide
  exact h a b
theorem sign_sub (a b : F₂) : sign (a - b) = sign a * sign b := by
  have h : ∀ a b : F₂, sign (a - b) = sign a * sign b := by decide
  exact h a b

variable {V : Type*} [AddCommGroup V] [Module F₂ V] [Fintype V]

theorem character_sum (f : V →ₗ[F₂] F₂) :
    ∑ x, sign (f x) = if f = 0 then (Fintype.card V : ℤ) else 0 := by
  classical
  by_cases hf : f = 0
  · simp [hf]
  · rw [ite_eq_right hf]
    obtain ⟨v, hv⟩ : ∃ v, f v ≠ 0 := by
      by_contra! h
      exact hf (LinearMap.ext h)
    have hs : sign (f v) = -1 := by simp [sign, hv]
    have he : (∑ x, sign (f (v + x))) = ∑ x, sign (f x) :=
      Fintype.sum_equiv (Equiv.addLeft v) _ _ (fun _ => rfl)
    simp_rw [map_add, sign_add, hs, neg_one_mul] at he
    rw [Finset.sum_neg_distrib] at he
    omega

theorem character_pair_sum (f g : V →ₗ[F₂] F₂) :
    ∑ x, sign (f x) * sign (g x) =
      if f = g then (Fintype.card V : ℤ) else 0 := by
  simpa only [LinearMap.sub_apply, sign_sub, sub_eq_zero] using character_sum (f - g)

variable {ι : Type*} [Fintype ι]

theorem sign_sum_weight (y : ι → F₂) :
    ∑ i, sign (y i) = (Fintype.card ι : ℤ) -
      2 * (Finset.univ.filter fun i => y i ≠ 0).card := by
  have h : ∀ a : F₂, sign a = 1 - 2 * (if a ≠ 0 then (1 : ℤ) else 0) := by decide
  simp_rw [h, Finset.sum_sub_distrib, ← Finset.mul_sum]
  rw [← Finset.sum_filter]
  simp

def fourier (cols : ι → V →ₗ[F₂] F₂) (x : V) : ℤ := ∑ i, sign (cols i x)

noncomputable def collisionCount (cols : ι → V →ₗ[F₂] F₂) : ℕ := by
  classical
  exact ∑ i, (Finset.univ.filter fun j => cols i = cols j).card

omit [Fintype V] in
theorem collisionCount_lower (cols : ι → V →ₗ[F₂] F₂) :
    Fintype.card ι ≤ collisionCount cols := by
  classical
  calc
    Fintype.card ι = ∑ _i : ι, 1 := by simp
    _ ≤ collisionCount cols := by
      apply Finset.sum_le_sum
      intro i _
      exact Finset.card_pos.mpr ⟨i, by simp⟩

/-- Parseval: equal ordered pairs of columns count the sum of squared
    column multiplicities, including repeated and zero columns. -/
theorem fourier_parseval (cols : ι → V →ₗ[F₂] F₂) :
    ∑ x, fourier cols x ^ 2 = (Fintype.card V : ℤ) * collisionCount cols := by
  classical
  simp only [fourier, pow_two, Finset.sum_mul, Finset.mul_sum]
  rw [Finset.sum_comm]
  conv_lhs => arg 2; ext i; rw [Finset.sum_comm]
  simp_rw [character_pair_sum]
  simp only [collisionCount, Nat.cast_sum, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [← Finset.sum_filter]
  simp [eq_comm, mul_comm]

#print axioms character_sum
#print axioms fourier_parseval
end So52.Binary
