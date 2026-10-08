import So52.Fourier

namespace So52.Binary
open Classical
variable {V : Type*} [AddCommGroup V] [Module F₂ V] [Fintype V]
variable {ι : Type*} [Fintype ι]

/-- Inverse Fourier coefficient for any binary linear functional. -/
theorem fourier_dual_coefficient (cols : ι → V →ₗ[F₂] F₂) (g : V →ₗ[F₂] F₂) :
    ∑ x, fourier cols x * sign (g x) =
      (Fintype.card V : ℤ) * (Finset.univ.filter fun j => cols j = g).card := by
  simp only [fourier, Finset.sum_mul]
  rw [Finset.sum_comm]
  simp_rw [character_pair_sum]
  rw [← Finset.sum_filter]
  simp [mul_comm]

/-- Extract a column multiplicity by character orthogonality. -/
theorem fourier_column_coefficient (cols : ι → V →ₗ[F₂] F₂) (i : ι) :
    ∑ x, fourier cols x * sign (cols i x) =
      (Fintype.card V : ℤ) * (Finset.univ.filter fun j => cols j = cols i).card := by
  simp only [fourier, Finset.sum_mul]
  rw [Finset.sum_comm]
  simp_rw [character_pair_sum]
  rw [← Finset.sum_filter]
  simp [mul_comm]

variable [Fintype (V →ₗ[F₂] F₂)]

omit [Fintype V] in
/-- The multiplicities of all linear column types sum to the number of columns. -/
theorem column_multiplicity_sum (cols : ι → V →ₗ[F₂] F₂) :
    ∑ g : V →ₗ[F₂] F₂, (Finset.univ.filter fun i => cols i = g).card =
      Fintype.card ι := by
  have h := Finset.sum_fiberwise (Finset.univ : Finset ι) cols (fun _ => (1 : ℕ))
  simpa using h

omit [Fintype V] in
/-- Ordered collisions are exactly the sum of squares of column multiplicities. -/
theorem collisionCount_eq_sum_multiplicity_sq (cols : ι → V →ₗ[F₂] F₂) :
    collisionCount cols =
      ∑ g : V →ₗ[F₂] F₂, (Finset.univ.filter fun i => cols i = g).card ^ 2 := by
  have h := Finset.sum_fiberwise (Finset.univ : Finset ι) cols
    (fun i => (Finset.univ.filter fun j => cols j = cols i).card)
  calc
    collisionCount cols =
        ∑ g : V →ₗ[F₂] F₂, ∑ i ∈ Finset.univ.filter (fun i => cols i = g),
          (Finset.univ.filter fun j => cols j = cols i).card := by
      simpa [collisionCount, eq_comm] using h.symm
    _ = _ := by
      apply Finset.sum_congr rfl
      intro g _
      calc
        _ = ∑ _i ∈ Finset.univ.filter (fun i => cols i = g),
            (Finset.univ.filter fun j => cols j = g).card := by
          apply Finset.sum_congr rfl
          intro i hi
          rw [(Finset.mem_filter.mp hi).2]
        _ = _ := by simp [pow_two]

end So52.Binary
