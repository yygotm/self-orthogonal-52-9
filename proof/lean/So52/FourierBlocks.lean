import So52.FourierCoefficients
import Mathlib.Tactic.IntervalCases

namespace So52.Binary
open Classical
variable {V : Type*} [AddCommGroup V] [Module F₂ V] [Fintype V]
variable {ι : Type*} [Fintype ι]

def weightedFourier (cols : ι → V →ₗ[F₂] F₂) (a : ι → ℤ) (x : V) : ℤ :=
  ∑ i, a i * sign (cols i x)

theorem weighted_parseval_injective (cols : ι → V →ₗ[F₂] F₂)
    (hinj : Function.Injective cols) (a : ι → ℤ) :
    ∑ x, weightedFourier cols a x ^ 2 = (Fintype.card V : ℤ) * ∑ i, a i ^ 2 := by
  simp only [weightedFourier, pow_two, Finset.sum_mul, Finset.mul_sum]
  have hterm (i j : ι) (x : V) :
      a i * sign (cols i x) * (a j * sign (cols j x)) =
      (a i * a j) * (sign (cols i x) * sign (cols j x)) := by ring
  simp_rw [hterm]
  rw [Finset.sum_comm]
  conv_lhs => arg 2; ext i; rw [Finset.sum_comm]
  simp_rw [← Finset.mul_sum, character_pair_sum, hinj.eq_iff]
  simp [Finset.mul_sum, mul_comm]

noncomputable def columnTypes (cols : ι → V →ₗ[F₂] F₂) : Finset (V →ₗ[F₂] F₂) :=
  Finset.univ.image cols

noncomputable def columnType (cols : ι → V →ₗ[F₂] F₂) (i : ι) : columnTypes cols :=
  ⟨cols i, Finset.mem_image.mpr ⟨i, Finset.mem_univ _, rfl⟩⟩

noncomputable def columnBlock (cols : ι → V →ₗ[F₂] F₂) (t : columnTypes cols) : Finset ι :=
  Finset.univ.filter fun i => cols i = t.val

omit [Fintype V] in
theorem sum_columnBlocks {A : Type*} [AddCommMonoid A]
    (cols : ι → V →ₗ[F₂] F₂) (f : ι → A) :
    ∑ t : columnTypes cols, ∑ i ∈ columnBlock cols t, f i = ∑ i, f i := by
  have h := Finset.sum_fiberwise (Finset.univ : Finset ι) (columnType cols) f
  simpa [columnBlock, columnType, Subtype.ext_iff] using h

omit [Fintype V] in
theorem weightedFourier_grouped (cols : ι → V →ₗ[F₂] F₂) (a : ι → ℤ) (x : V) :
    weightedFourier cols a x =
      weightedFourier (fun t : columnTypes cols => t.val)
        (fun t => ∑ i ∈ columnBlock cols t, a i) x := by
  unfold weightedFourier
  rw [← sum_columnBlocks cols (fun i => a i * sign (cols i x))]
  apply Finset.sum_congr rfl
  intro t _
  rw [Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro i hi
  rw [(Finset.mem_filter.mp hi).2]

theorem weighted_parseval_blocks (cols : ι → V →ₗ[F₂] F₂) (a : ι → ℤ) :
    ∑ x, weightedFourier cols a x ^ 2 =
      (Fintype.card V : ℤ) * ∑ t : columnTypes cols, (∑ i ∈ columnBlock cols t, a i) ^ 2 := by
  conv_lhs => arg 2; ext x; rw [weightedFourier_grouped]
  exact weighted_parseval_injective _ Subtype.val_injective _

omit [Fintype ι] in
theorem sign_sum_finset [DecidableEq ι] (s : Finset ι) (x : ι → F₂) :
    ∑ i ∈ s, sign (x i) = (s.card : ℤ) - 2 * (s.filter fun i => x i ≠ 0).card := by
  have h : ∀ a : F₂, sign a = 1 - 2 * (if a ≠ 0 then (1 : ℤ) else 0) := by decide
  simp_rw [h, Finset.sum_sub_distrib, ← Finset.mul_sum]
  rw [← Finset.sum_filter]
  simp

omit [Fintype ι] in
theorem triple_sign_sum_sq_lower [DecidableEq ι] (s : Finset ι) (hs : s.card = 3)
    (x : ι → F₂) : 1 ≤ (∑ i ∈ s, sign (x i)) ^ 2 := by
  rw [sign_sum_finset, hs]
  have hle := Finset.card_filter_le s (fun i => x i ≠ 0)
  rw [hs] at hle
  interval_cases h : (s.filter fun i => x i ≠ 0).card <;> norm_num

#print axioms weighted_parseval_blocks
end So52.Binary
