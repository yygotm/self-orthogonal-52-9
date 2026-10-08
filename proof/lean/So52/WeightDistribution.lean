import So52.EvenSpace
import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Data.Fintype.Powerset

namespace So52.Binary
open Classical
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

noncomputable def evenSupportEquiv :
    evenSpace ι ≃ {s : Finset ι // s.card % 2 = 0} where
  toFun y := ⟨Finset.univ.filter (fun i => y.val i ≠ 0), (mem_evenSpace y.val).mp y.property⟩
  invFun s := ⟨fun i => if i ∈ s.val then 1 else 0, by
    apply (mem_evenSpace _).mpr
    simpa using s.property⟩
  left_inv y := by
    apply Subtype.ext
    funext i
    have h : ∀ a : F₂, (if a ≠ 0 then 1 else 0) = a := by decide
    simpa using h (y.val i)
  right_inv s := by
    apply Subtype.ext
    ext i
    simp

theorem sum_evenSpace_weight (f : ℕ → ℤ) :
    ∑ y : evenSpace ι, f (Finset.univ.filter fun i => y.val i ≠ 0).card =
      ∑ j ∈ Finset.range (Fintype.card ι + 1),
        (Fintype.card ι).choose j • (if j % 2 = 0 then f j else 0) := by
  calc
    _ = ∑ s : {s : Finset ι // s.card % 2 = 0}, f s.val.card :=
      Fintype.sum_equiv evenSupportEquiv _ _ (fun _ => rfl)
    _ = ∑ s : Finset ι, if s.card % 2 = 0 then f s.card else 0 := by
      symm
      rw [← Finset.sum_filter]
      exact Finset.sum_subtype _ (by simp) _
    _ = ∑ s ∈ (Finset.univ : Finset ι).powerset,
        if s.card % 2 = 0 then f s.card else 0 := by simp
    _ = _ := by
      simpa only [Finset.card_univ] using
        (Finset.sum_powerset_apply_card (fun j => if j % 2 = 0 then f j else 0)
          (x := (Finset.univ : Finset ι)))

def weight44Bound (j : ℕ) : ℤ := if j = 0 then 44 ^ 2 else (2 * (j : ℤ) - 4) ^ 2

theorem even8_bound_sum (hι : Fintype.card ι = 8) :
    ∑ y : evenSpace ι, weight44Bound (Finset.univ.filter fun i => y.val i ≠ 0).card =
      44^2 + 70*16 + 28*64 + 144 := by
  rw [sum_evenSpace_weight, hι]
  decide

#print axioms sum_evenSpace_weight
#print axioms even8_bound_sum
end So52.Binary
