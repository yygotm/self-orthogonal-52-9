import So52.Kernel
import Mathlib.Tactic.Ring

namespace So52.Binary

def ConstantOn {ι : Type*} (s : Finset ι) (x : ι → F₂) : Prop :=
  ∀ i ∈ s, ∀ j ∈ s, x i = x j

theorem constantOn_triple_iff {ι : Type*} [DecidableEq ι] (a b c : ι) (x : ι → F₂) :
    ConstantOn {a, b, c} x ↔ x a = x b ∧ x a = x c := by
  constructor
  · intro h
    exact ⟨h a (by simp) b (by simp), h a (by simp) c (by simp)⟩
  · rintro ⟨hab, hac⟩ i hi j hj
    simp only [Finset.mem_insert, Finset.mem_singleton] at hi hj
    rcases hi with rfl | rfl | rfl <;> rcases hj with rfl | rfl | rfl <;> simp_all

private theorem pair_bits (a b c : F₂ × F₂)
    (ha : a ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0)
    (hab : a + b ≠ 0) (hac : a + c ≠ 0) (hbc : b + c ≠ 0) : a + b + c = 0 := by
  have h : ∀ a b c : F₂ × F₂,
      a ≠ 0 → b ≠ 0 → c ≠ 0 → a + b ≠ 0 → a + c ≠ 0 → b + c ≠ 0 → a + b + c = 0 := by
    decide
  exact h a b c ha hb hc hab hac hbc

/-- Three distinct nonzero classes in F₂³ / <111> sum to zero. -/
theorem triple_sum_constant {ι : Type*} [DecidableEq ι] (s : Finset ι) (hs : s.card = 3)
    (x y z : ι → F₂) (hx : ¬ ConstantOn s x) (hy : ¬ ConstantOn s y)
    (hz : ¬ ConstantOn s z) (hxy : ¬ ConstantOn s (x + y))
    (hxz : ¬ ConstantOn s (x + z)) (hyz : ¬ ConstantOn s (y + z)) :
    ConstantOn s (x + y + z) := by
  obtain ⟨i, j, k, _, _, _, rfl⟩ := Finset.card_eq_three.mp hs
  let d (v : ι → F₂) : F₂ × F₂ := (v i - v j, v i - v k)
  have hd (v : ι → F₂) : d v = 0 ↔ ConstantOn {i, j, k} v := by
    simp [d, Prod.ext_iff, constantOn_triple_iff, sub_eq_zero]
  have hadd (v w : ι → F₂) : d (v + w) = d v + d w := by
    ext <;> simp [d] <;> ring
  apply (hd _).mp
  rw [hadd, hadd]
  apply pair_bits
  · exact fun h => hx ((hd _).mp h)
  · exact fun h => hy ((hd _).mp h)
  · exact fun h => hz ((hd _).mp h)
  · rw [← hadd]; exact fun h => hxy ((hd _).mp h)
  · rw [← hadd]; exact fun h => hxz ((hd _).mp h)
  · rw [← hadd]; exact fun h => hyz ((hd _).mp h)

end So52.Binary
