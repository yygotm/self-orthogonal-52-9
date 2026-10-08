import So52.Weight40

/- A packing argument for an arbitrary even binary [12,7,>=4] code.
   No classification or externally enumerated residual code is used. -/
namespace So52.Binary
open Classical

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def binaryWeight (x : ι → F₂) : ℕ :=
  (Finset.univ.filter fun i => x i ≠ 0).card

def dotMap (z : ι → F₂) : (ι → F₂) →ₗ[F₂] F₂ where
  toFun x := ∑ i, z i * x i
  map_add' x y := by simp [mul_add, Finset.sum_add_distrib]
  map_smul' a x := by simp [Finset.mul_sum, mul_left_comm]

/-- The ordinary coordinate-dot-product dual, on any finite coordinate type. -/
def binaryDual (R : Submodule F₂ (ι → F₂)) : Submodule F₂ (ι → F₂) where
  carrier := {z | ∀ x : R, dotMap z x.val = 0}
  zero_mem' := by simp [dotMap]
  add_mem' := by
    intro z w hz hw x
    simpa [dotMap, add_mul, Finset.sum_add_distrib] using congrArg₂ (· + ·) (hz x) (hw x)
  smul_mem' := by
    intro a z hz x
    simpa [dotMap, mul_assoc, Finset.mul_sum] using congrArg (a * ·) (hz x)

@[simp] theorem dotMap_single (z : ι → F₂) (i : ι) (a : F₂) :
    dotMap z (Pi.single i a) = z i * a := by
  simp [dotMap, Pi.single_apply]

@[simp] theorem parityMap_single (i : ι) (a : F₂) :
    parityMap (Pi.single i a) = a := by simp [parityMap]

theorem binaryWeight_sub_le_two (x y : ι → F₂) (i j : ι)
    (h : x + Pi.single i 1 = y + Pi.single j 1) :
    binaryWeight (x - y) ≤ 2 := by
  have hs : (Finset.univ.filter fun k => (x - y) k ≠ 0) ⊆ {i, j} := by
    intro k hk
    by_contra hn
    simp only [Finset.mem_insert, Finset.mem_singleton, not_or] at hn
    have hi : k ≠ i := hn.1
    have hj : k ≠ j := hn.2
    have he := congrFun h k
    simp [hi, hj] at he
    exact (Finset.mem_filter.mp hk).2 (sub_eq_zero.mpr he)
  exact (Finset.card_le_card hs).trans Finset.card_le_two

/-- Distinct radius-one neighbors are disjoint when the minimum weight is >=4. -/
theorem single_neighbor_injective (R : Submodule F₂ (ι → F₂))
    (hmin : ∀ x : R, x ≠ 0 → 4 ≤ binaryWeight x.val) :
    Function.Injective (fun p : R × ι => p.1.val + Pi.single p.2 (1 : F₂)) := by
  intro ⟨x, i⟩ ⟨y, j⟩ h
  have hw := binaryWeight_sub_le_two x.val y.val i j h
  have hxy : x = y := by
    by_contra hn
    have hm := hmin (x - y) (sub_ne_zero.mpr hn)
    change 4 ≤ binaryWeight (x.val - y.val) at hm
    omega
  subst y
  have he := add_left_cancel h
  have hij : i = j := by
    by_contra hn
    have hv := congrFun he i
    simp [hn] at hv
  subst j
  rfl

theorem parity_dot_surjective (z : ι → F₂) (i j : ι)
    (hi : z i = 1) (hj : z j = 0) :
    Function.Surjective ((parityMap (ι := ι)).prod (dotMap z)) := by
  intro ⟨a, b⟩
  refine ⟨Pi.single i b + Pi.single j (a - b), ?_⟩
  apply Prod.ext <;> simp [hi, hj]

/-- A dual word with both a 1 and a 0 leaves a codimension-two packing space. -/
theorem dual_zero_coordinates_bound (R : Submodule F₂ (ι → F₂))
    [Fintype R]
    (heven : ∀ x : R, binaryWeight x.val % 2 = 0)
    (hmin : ∀ x : R, x ≠ 0 → 4 ≤ binaryWeight x.val)
    (z : binaryDual R) (i j : ι) (hi : z.val i = 1) (hj : z.val j = 0) :
    Fintype.card R * (Fintype.card ι - binaryWeight z.val) ≤
      2 ^ (Fintype.card ι - 2) := by
  let L := (parityMap (ι := ι)).prod (dotMap z.val)
  have hsur : Function.Surjective L := parity_dot_surjective z.val i j hi hj
  have hdim : Module.finrank F₂ (LinearMap.ker L) = Fintype.card ι - 2 := by
    have h := L.finrank_range_add_finrank_ker
    rw [LinearMap.range_eq_top.mpr hsur, finrank_top,
      Module.finrank_prod, Module.finrank_self, Module.finrank_pi] at h
    omega
  have hcard : Fintype.card (LinearMap.ker L) = 2 ^ (Fintype.card ι - 2) := by
    rw [← Nat.card_eq_fintype_card, Module.natCard_eq_pow_finrank (K := F₂), hdim]
    simp [Nat.card_eq_fintype_card, F₂, ZMod.card]
  let Z := {k : ι // z.val k = 0}
  let f : R × Z → LinearMap.ker L := fun p =>
    ⟨p.1.val + Pi.single p.2.val 1 - Pi.single j 1, by
      change L _ = 0
      apply Prod.ext
      · have hp : parityMap p.1.val = 0 := (mem_evenSpace _).mpr (heven p.1)
        simp [L, hp]
      · have hz := z.property p.1
        simp [L, hz, p.2.property, hj]⟩
  have hf : Function.Injective f := by
    intro ⟨x, k⟩ ⟨y, l⟩ h
    have he := congrArg Subtype.val h
    have hn : x.val + Pi.single k.val 1 = y.val + Pi.single l.val 1 :=
      sub_left_inj.mp he
    have hp := single_neighbor_injective R hmin (a₁ := (x, k.val)) (a₂ := (y, l.val)) hn
    have hx : x = y := congrArg Prod.fst hp
    have hk : k = l := Subtype.ext (congrArg Prod.snd hp)
    exact Prod.ext hx hk
  have hc := Fintype.card_le_of_injective f hf
  have hzcard : Fintype.card Z = Fintype.card ι - binaryWeight z.val := by
    have h := Finset.card_filter_add_card_filter_not (s := Finset.univ)
      (fun k => z.val k = 0)
    simp only [Finset.card_univ] at h
    have hZ : Fintype.card Z = (Finset.univ.filter fun k => z.val k = 0).card :=
      Fintype.card_subtype _
    rw [hZ]
    change (Finset.univ.filter fun k => z.val k = 0).card +
      (Finset.univ.filter fun k => z.val k ≠ 0).card = Fintype.card ι at h
    unfold binaryWeight
    omega
  simpa only [Fintype.card_prod, hzcard, hcard] using hc

/-- Every even binary length-12 code of size 128 and minimum weight >=4
    has dual minimum weight >=4, without classifying the code. -/
theorem even12_card128_dual_minWeight_four (R : Submodule F₂ (ι → F₂))
    [Fintype R]
    (hlen : Fintype.card ι = 12) (hcard : Fintype.card R = 128)
    (heven : ∀ x : R, binaryWeight x.val % 2 = 0)
    (hmin : ∀ x : R, x ≠ 0 → 4 ≤ binaryWeight x.val) :
    ∀ z : binaryDual R, z ≠ 0 → 4 ≤ binaryWeight z.val := by
  intro z hz
  by_contra hn
  have hw : binaryWeight z.val ≤ 3 := by omega
  obtain ⟨i, hi⟩ : ∃ i, z.val i ≠ 0 := by
    by_contra! h
    exact hz (Subtype.ext (funext h))
  have hi1 : z.val i = 1 := by
    have h : ∀ a : F₂, a ≠ 0 → a = 1 := by decide
    exact h _ hi
  obtain ⟨j, hj⟩ : ∃ j, z.val j = 0 := by
    by_contra! h
    have he : binaryWeight z.val = 12 := by simp [binaryWeight, h, hlen]
    omega
  have hb := dual_zero_coordinates_bound R heven hmin z i j hi1 hj
  rw [hlen, hcard] at hb
  norm_num at hb
  omega

/-- Backwards-compatible distance-three consequence of the stronger bound. -/
theorem even12_card128_dual_minWeight (R : Submodule F₂ (ι → F₂))
    [Fintype R]
    (hlen : Fintype.card ι = 12) (hcard : Fintype.card R = 128)
    (heven : ∀ x : R, binaryWeight x.val % 2 = 0)
    (hmin : ∀ x : R, x ≠ 0 → 4 ≤ binaryWeight x.val) :
    ∀ z : binaryDual R, z ≠ 0 → 3 ≤ binaryWeight z.val := by
  intro z hz
  exact le_trans (by decide) (even12_card128_dual_minWeight_four R hlen hcard heven hmin z hz)

theorem weight40_residual_dual_minWeight_four {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 40) :
    ∀ z : binaryDual (residualRange C c), z ≠ 0 → 4 ≤ binaryWeight z.val := by
  obtain ⟨hlen, _, heven, hm⟩ := residual40_parameters hD hdim hmin c hc
  have hcard : Fintype.card (residualRange C c) = 128 :=
    weight40_range_card hD hdim hmin c hc
  have he : ∀ y : residualRange C c, binaryWeight y.val % 2 = 0 :=
    fun y => heven y.val y.property
  have hm' : ∀ y : residualRange C c, y ≠ 0 → 4 ≤ binaryWeight y.val :=
    fun y hy => hm y.val y.property (fun h => hy (Subtype.ext h))
  exact even12_card128_dual_minWeight_four (residualRange C c) hlen hcard he hm'

/-- Preserve the original statement as a corollary. -/
theorem weight40_residual_dual_minWeight {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 40) :
    ∀ z : binaryDual (residualRange C c), z ≠ 0 → 3 ≤ binaryWeight z.val := by
  intro z hz
  exact le_trans (by decide) (weight40_residual_dual_minWeight_four hD hdim hmin c hc z hz)

#print axioms even12_card128_dual_minWeight_four
#print axioms weight40_residual_dual_minWeight_four
#print axioms weight40_residual_dual_minWeight
end So52.Binary
