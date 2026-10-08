import So52.Reductions
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.Field.ZMod
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.Tactic.FinCases
import Mathlib.FieldTheory.Finiteness

/- Arbitrary binary linear codes, using the ordinary coordinate dot product.
   No classification or general distance bound is assumed as an axiom. -/
namespace So52.Binary

abbrev F₂ := ZMod 2
abbrev Word (n : ℕ) := Fin n → F₂
abbrev Code (n : ℕ) := Submodule F₂ (Word n)

def support {n : ℕ} (x : Word n) : Finset (Fin n) :=
  Finset.univ.filter fun i => x i ≠ 0

def weight {n : ℕ} (x : Word n) : ℕ := (support x).card

def dot {n : ℕ} (x y : Word n) : F₂ := ∑ i, x i * y i

def SelfOrthogonal {n : ℕ} (C : Code n) : Prop :=
  ∀ x ∈ C, ∀ y ∈ C, dot x y = 0

def DoublyEven {n : ℕ} (C : Code n) : Prop :=
  ∀ x ∈ C, weight x % 4 = 0

def MinWeight {n : ℕ} (C : Code n) (d : ℕ) : Prop :=
  ∀ x ∈ C, x ≠ 0 → d ≤ weight x

open scoped symmDiff

theorem support_add {n : ℕ} (x y : Word n) :
    support (x + y) = support x ∆ support y := by
  ext i
  simp only [support, Finset.mem_filter, Finset.mem_univ, true_and,
    Finset.mem_symmDiff, Pi.add_apply]
  have h : ∀ a b : F₂, a + b ≠ 0 ↔ (a ≠ 0 ∧ ¬b ≠ 0) ∨ (b ≠ 0 ∧ ¬a ≠ 0) := by
    decide
  exact h (x i) (y i)

@[simp] theorem weight_zero (n : ℕ) : weight (0 : Word n) = 0 := by
  simp [weight, support]

theorem dot_eq_card_inter {n : ℕ} (x y : Word n) :
    dot x y = ((support x ∩ support y).card : F₂) := by
  have h : ∀ a b : F₂, a * b = if a ≠ 0 ∧ b ≠ 0 then 1 else 0 := by decide
  simp only [dot, h]
  simp [support, Finset.filter_inter, Finset.filter_filter, Finset.sum_boole, and_comm]

theorem even_inter {n : ℕ} {C : Code n} (hC : SelfOrthogonal C)
    {x y : Word n} (hx : x ∈ C) (hy : y ∈ C) :
    (support x ∩ support y).card % 2 = 0 := by
  have h := hC x hx y hy
  rw [dot_eq_card_inter] at h
  have hv := congrArg ZMod.val h
  simpa [ZMod.val_natCast] using hv

theorem even_weight {n : ℕ} {C : Code n} (hC : SelfOrthogonal C)
    {x : Word n} (hx : x ∈ C) : weight x % 2 = 0 := by
  simpa [weight] using even_inter hC hx hx

theorem doublyEven_selfOrthogonal {n : ℕ} {C : Code n} (hD : DoublyEven C) :
    SelfOrthogonal C := by
  intro x hx y hy
  have hx4 := hD x hx
  have hy4 := hD y hy
  have hxy4 := hD (x + y) (C.add_mem hx hy)
  have hw := So52.Support.weight_identity (support x) (support y)
  rw [← support_add] at hw
  change weight (x + y) + 2 * (support x ∩ support y).card = weight x + weight y at hw
  rw [dot_eq_card_inter, ZMod.natCast_eq_zero_iff, Nat.dvd_iff_mod_eq_zero]
  omega

/-- Half-weight modulo two, as a linear functional on a self-orthogonal code. -/
def q {n : ℕ} (C : Code n) (hC : SelfOrthogonal C) : C →ₗ[F₂] F₂ where
  toFun x := (weight x.val / 2 : ℕ)
  map_add' x y := by
    change ((weight (x.val + y.val) / 2 : ℕ) : F₂) =
      (weight x.val / 2 : ℕ) + (weight y.val / 2 : ℕ)
    rw [← Nat.cast_add]
    apply ZMod.val_injective
    simp only [ZMod.val_natCast]
    simpa only [weight, support_add] using
      So52.Support.half_weight_add (support x.val) (support y.val)
        (even_weight hC x.property) (even_weight hC y.property)
        (even_inter hC x.property y.property)
  map_smul' a x := by
    have ha : a = 0 ∨ a = 1 := by
      have h : ∀ a : F₂, a = 0 ∨ a = 1 := by decide
      exact h a
    rcases ha with rfl | rfl <;> simp

theorem q_eq_zero_iff {n : ℕ} {C : Code n} (hC : SelfOrthogonal C) (x : C) :
    q C hC x = 0 ↔ weight x.val % 4 = 0 := by
  change ((weight x.val / 2 : ℕ) : F₂) = 0 ↔ _
  rw [ZMod.natCast_eq_zero_iff, Nat.dvd_iff_mod_eq_zero]
  have he := even_weight hC x.property
  omega

theorem q_eq_one_iff {n : ℕ} {C : Code n} (hC : SelfOrthogonal C) (x : C) :
    q C hC x = 1 ↔ weight x.val % 4 = 2 := by
  have he := even_weight hC x.property
  change ((weight x.val / 2 : ℕ) : F₂) = 1 ↔ _
  constructor
  · intro h
    have hv : (weight x.val / 2) % 2 = 1 := by
      simpa only [ZMod.val_natCast, ZMod.val_one] using congrArg ZMod.val h
    omega
  · intro h
    apply ZMod.val_injective
    simp only [ZMod.val_natCast, ZMod.val_one]
    omega

theorem q_zero_iff_doublyEven {n : ℕ} {C : Code n} (hC : SelfOrthogonal C) :
    q C hC = 0 ↔ DoublyEven C := by
  constructor
  · intro hz x hx
    apply (q_eq_zero_iff hC ⟨x, hx⟩).mp
    rw [hz]; rfl
  · intro hd
    apply LinearMap.ext
    intro x
    exact (q_eq_zero_iff hC x).mpr (hd x.val x.property)

/-- The kernel embedded back into the original ambient coordinate space. -/
def doublyEvenKernel {n : ℕ} (C : Code n) (hC : SelfOrthogonal C) : Code n :=
  (LinearMap.ker (q C hC)).map C.subtype

theorem mem_doublyEvenKernel {n : ℕ} {C : Code n} (hC : SelfOrthogonal C)
    (x : Word n) : x ∈ doublyEvenKernel C hC ↔ x ∈ C ∧ weight x % 4 = 0 := by
  constructor
  · rintro ⟨y, hy, rfl⟩
    exact ⟨y.property, (q_eq_zero_iff hC y).mp hy⟩
  · rintro ⟨hx, hw⟩
    exact ⟨⟨x, hx⟩, (q_eq_zero_iff hC ⟨x, hx⟩).mpr hw, rfl⟩

theorem doublyEvenKernel_le {n : ℕ} {C : Code n} (hC : SelfOrthogonal C) :
    doublyEvenKernel C hC ≤ C := fun x hx => ((mem_doublyEvenKernel hC x).mp hx).1

theorem doublyEvenKernel_doublyEven {n : ℕ} {C : Code n} (hC : SelfOrthogonal C) :
    DoublyEven (doublyEvenKernel C hC) :=
  fun x hx => ((mem_doublyEvenKernel hC x).mp hx).2

theorem doublyEvenKernel_selfOrthogonal {n : ℕ} {C : Code n} (hC : SelfOrthogonal C) :
    SelfOrthogonal (doublyEvenKernel C hC) :=
  fun x hx y hy => hC x (doublyEvenKernel_le hC hx) y (doublyEvenKernel_le hC hy)

theorem doublyEvenKernel_minWeight {n : ℕ} {C : Code n} (hC : SelfOrthogonal C)
    (hmin : MinWeight C 22) : MinWeight (doublyEvenKernel C hC) 24 := by
  intro x hx hn
  exact So52.Support.doubly_even_lower (weight x)
    (hmin x (doublyEvenKernel_le hC hx) hn) (doublyEvenKernel_doublyEven hC x hx)

theorem q_surjective {n : ℕ} {C : Code n} (hC : SelfOrthogonal C)
    (hq : q C hC ≠ 0) : Function.Surjective (q C hC) := by
  have hex : ∃ x : C, q C hC x ≠ 0 := by
    by_contra! h
    exact hq (LinearMap.ext h)
  obtain ⟨x, hx⟩ := hex
  have hx1 : q C hC x = 1 := by
    have h : ∀ a : F₂, a ≠ 0 → a = 1 := by decide
    exact h _ hx
  intro a
  fin_cases a
  · exact ⟨0, map_zero _⟩
  · exact ⟨x, hx1⟩

theorem doublyEvenKernel_finrank {n k : ℕ} {C : Code n} (hC : SelfOrthogonal C)
    (hdim : Module.finrank F₂ C = k + 1) (hq : q C hC ≠ 0) :
    Module.finrank F₂ (doublyEvenKernel C hC) = k := by
  have hr := (q C hC).finrank_range_add_finrank_ker
  rw [LinearMap.range_eq_top.mpr (q_surjective hC hq), finrank_top,
    Module.finrank_self, hdim] at hr
  rw [doublyEvenKernel, Submodule.finrank_map_subtype_eq]
  omega

/-- Translation by any word with q = 1 identifies the kernel with the other fiber. -/
def kernelEquivOdd {n : ℕ} {C : Code n} (hC : SelfOrthogonal C)
    (v : C) (hv : q C hC v = 1) :
    LinearMap.ker (q C hC) ≃ {x : C // q C hC x = 1} where
  toFun x := ⟨v + x.val, by rw [map_add, hv, x.property, add_zero]⟩
  invFun x := ⟨x.val - v, by
    change q C hC (x.val - v) = 0
    rw [map_sub, x.property, hv, sub_self]⟩
  left_inv x := by apply Subtype.ext; simp
  right_inv x := by apply Subtype.ext; simp

theorem odd_card {n : ℕ} {C : Code n} (hC : SelfOrthogonal C)
    (hdim : Module.finrank F₂ C = 9) (hq : q C hC ≠ 0) :
    Nat.card {x : C // q C hC x = 1} = 256 := by
  obtain ⟨v, hv⟩ := q_surjective hC hq 1
  rw [← Nat.card_congr (kernelEquivOdd hC v hv)]
  have hk : Module.finrank F₂ (LinearMap.ker (q C hC)) = 8 := by
    have hk := doublyEvenKernel_finrank hC hdim hq
    rw [doublyEvenKernel, Submodule.finrank_map_subtype_eq] at hk
    exact hk
  rw [Module.natCard_eq_pow_finrank (K := F₂), hk]
  simp [Nat.card_eq_fintype_card, F₂, ZMod.card]

theorem outside_kernel_iff {n : ℕ} {C : Code n} (hC : SelfOrthogonal C) (x : C) :
    x.val ∉ doublyEvenKernel C hC ↔ q C hC x = 1 := by
  rw [mem_doublyEvenKernel, q_eq_one_iff]
  have he := even_weight hC x.property
  simp only [x.property, true_and]
  omega

/-- Explicit external dependency: every binary [52,9] code has a nonzero word
    of weight at most 22. This proposition is NOT asserted as a theorem. -/
def GeneralBound52_9 : Prop :=
  ∀ C : Code 52, Module.finrank F₂ C = 9 → ∃ x : Word 52, x ∈ C ∧ x ≠ 0 ∧ weight x ≤ 22

theorem q_ne_zero_of_bound (bound : GeneralBound52_9) {C : Code 52}
    (hC : SelfOrthogonal C) (hdim : Module.finrank F₂ C = 9)
    (hmin : MinWeight C 22) : q C hC ≠ 0 := by
  intro hz
  obtain ⟨x, hx, hn, hw⟩ := bound C hdim
  have hq0 : q C hC ⟨x, hx⟩ = 0 := by rw [hz]; rfl
  have hd := (q_eq_zero_iff hC ⟨x, hx⟩).mp hq0
  have hl := So52.Support.doubly_even_lower (weight x) (hmin x hx hn) hd
  omega

/-- Conditional first reduction; neither the general bound nor classification
    and extension exclusion are discharged by this theorem. -/
theorem reduction52 (bound : GeneralBound52_9) {C : Code 52}
    (hC : SelfOrthogonal C) (hdim : Module.finrank F₂ C = 9) (hmin : MinWeight C 22) :
    ∃ D : Code 52, D ≤ C ∧ Module.finrank F₂ D = 8 ∧ DoublyEven D ∧ MinWeight D 24 := by
  exact ⟨doublyEvenKernel C hC, doublyEvenKernel_le hC,
    doublyEvenKernel_finrank hC hdim (q_ne_zero_of_bound bound hC hdim hmin),
    doublyEvenKernel_doublyEven hC, doublyEvenKernel_minWeight hC hmin⟩

#print axioms q
#print axioms q_eq_zero_iff
#print axioms doublyEvenKernel_finrank
#print axioms odd_card
#print axioms outside_kernel_iff
#print axioms reduction52
end So52.Binary
