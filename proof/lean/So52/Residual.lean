import So52.Kernel

/- Restriction to the coordinates outside one codeword. These structural
   lemmas do not assert a classification of the residual codes. -/
namespace So52.Binary
open scoped symmDiff

abbrev Outside {n : ℕ} (c : Word n) := {i : Fin n // c i = 0}

theorem outside_card {n : ℕ} (c : Word n) :
    Fintype.card (Outside c) = n - weight c := by
  have h := Finset.card_filter_add_card_filter_not (s := Finset.univ)
    (fun i : Fin n => c i = 0)
  rw [Fintype.card_subtype]
  simp only [Finset.card_univ, Fintype.card_fin] at h
  unfold weight support
  simp only [ne_eq] at h ⊢
  omega

def residualMap {n : ℕ} (C : Code n) (c : C) : C →ₗ[F₂] (Outside c.val → F₂) where
  toFun x i := x.val i.val
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

def residualWeight {n : ℕ} {c : Word n} (y : Outside c → F₂) : ℕ :=
  (Finset.univ.filter fun i => y i ≠ 0).card

theorem residualWeight_eq_sdiff {n : ℕ} {C : Code n} (c x : C) :
    residualWeight (residualMap C c x) = (support x.val \ support c.val).card := by
  apply Finset.card_bij (fun i _ => i.val)
  · intro i hi
    have hi' : x.val i.val ≠ 0 := (Finset.mem_filter.mp hi).2
    simpa [support] using And.intro hi' i.property
  · intro i hi j hj hij
    exact Subtype.ext hij
  · intro i hi
    have hi' : x.val i ≠ 0 ∧ c.val i = 0 := by simpa [support] using hi
    exact ⟨⟨i, hi'.2⟩, Finset.mem_filter.mpr ⟨Finset.mem_univ _, hi'.1⟩, rfl⟩

theorem add_eq_zero_iff {n : ℕ} (x y : Word n) : x + y = 0 ↔ x = y := by
  have h : ∀ a b : F₂, a + b = 0 ↔ a = b := by decide
  constructor
  · intro he
    funext i
    exact (h _ _).mp (congrFun he i)
  · rintro rfl
    funext i
    exact (h _ _).mpr rfl

theorem residual_weight_identity {n : ℕ} {C : Code n} (c x : C) :
    weight x.val + weight (x.val + c.val) =
      weight c.val + 2 * residualWeight (residualMap C c x) := by
  rw [residualWeight_eq_sdiff]
  have h₁ := So52.Support.weight_identity (support x.val) (support c.val)
  have h₂ := Finset.card_sdiff_add_card_inter (support x.val) (support c.val)
  simp only [weight, support_add]
  omega

theorem mem_residual_ker_iff {n : ℕ} {C : Code n} (c x : C) :
    x ∈ LinearMap.ker (residualMap C c) ↔ support x.val ⊆ support c.val := by
  constructor
  · intro hx i hi
    by_contra hc
    have hc0 : c.val i = 0 := by simpa [support] using hc
    have hx0 := congrFun hx (⟨i, hc0⟩ : Outside c.val)
    have hxne : x.val i ≠ 0 := by simpa [support] using hi
    exact hxne hx0
  · intro hs
    change residualMap C c x = 0
    funext i
    by_contra hx
    change x.val i.val ≠ 0 at hx
    have hi : i.val ∈ support c.val := hs (by simpa [support] using hx)
    simp [support, i.property] at hi

/-- Below twice the minimum weight, the only words supported on c are 0,c. -/
theorem residual_ker_words {n d : ℕ} {C : Code n} (hmin : MinWeight C d)
    (c : C) (hc : weight c.val < 2 * d) (x : C)
    (hx : x ∈ LinearMap.ker (residualMap C c)) : x = 0 ∨ x = c := by
  by_cases h0 : x = 0
  · exact Or.inl h0
  right
  by_contra hxc
  have hx0 : x.val ≠ 0 := fun h => h0 (Subtype.ext h)
  have hxc0 : x.val + c.val ≠ 0 := by
    intro h
    exact hxc (Subtype.ext ((add_eq_zero_iff _ _).mp h))
  have h₁ := hmin x.val x.property hx0
  have h₂ := hmin (x.val + c.val) (C.add_mem x.property c.property) hxc0
  have hs := (mem_residual_ker_iff c x).mp hx
  have hw := So52.Support.weight_identity (support x.val) (support c.val)
  rw [Finset.inter_eq_left.mpr hs, ← support_add] at hw
  change weight (x.val + c.val) + 2 * weight x.val = weight x.val + weight c.val at hw
  omega

theorem residual_ker_eq_span {n d : ℕ} {C : Code n} (hmin : MinWeight C d)
    (c : C) (hc : weight c.val < 2 * d) :
    LinearMap.ker (residualMap C c) = Submodule.span F₂ {c} := by
  apply le_antisymm
  · intro x hx
    rcases residual_ker_words hmin c hc x hx with h0 | he
    · rw [h0]; exact Submodule.zero_mem _
    · rw [he]; exact Submodule.subset_span (Set.mem_singleton c)
  · apply Submodule.span_le.mpr
    intro x hx
    have he : x = c := Set.mem_singleton_iff.mp hx
    subst x
    exact (mem_residual_ker_iff c c).mpr (Finset.Subset.refl _)

theorem residual_finrank {n d k : ℕ} {C : Code n} (hmin : MinWeight C d)
    (hdim : Module.finrank F₂ C = k + 1) (c : C)
    (hc0 : c ≠ 0) (hc : weight c.val < 2 * d) :
    Module.finrank F₂ (LinearMap.range (residualMap C c)) = k := by
  have hr := (residualMap C c).finrank_range_add_finrank_ker
  rw [residual_ker_eq_span hmin c hc, finrank_span_singleton hc0, hdim] at hr
  omega

/-- Every nonzero residual word satisfies the usual residual distance inequality. -/
theorem residual_minWeight {n d : ℕ} {C : Code n} (hmin : MinWeight C d)
    (c : C) (y : Outside c.val → F₂)
    (hy : y ∈ LinearMap.range (residualMap C c)) (hy0 : y ≠ 0) :
    2 * d ≤ weight c.val + 2 * residualWeight y := by
  obtain ⟨x, rfl⟩ := hy
  have hx0 : x.val ≠ 0 := by
    intro hx
    apply hy0
    funext i
    exact congrFun hx i.val
  have hxc0 : x.val + c.val ≠ 0 := by
    intro hx
    have he := (add_eq_zero_iff _ _).mp hx
    apply hy0
    funext i
    exact (congrFun he i.val).trans i.property
  have h₁ := hmin x.val x.property hx0
  have h₂ := hmin (x.val + c.val) (C.add_mem x.property c.property) hxc0
  have hw := residual_weight_identity c x
  omega

theorem residual_even {n : ℕ} {C : Code n} (hC : SelfOrthogonal C)
    (c : C) (y : Outside c.val → F₂) (hy : y ∈ LinearMap.range (residualMap C c)) :
    residualWeight y % 2 = 0 := by
  obtain ⟨x, rfl⟩ := hy
  rw [residualWeight_eq_sdiff]
  have hx := even_weight hC x.property
  have hi := even_inter hC x.property c.property
  have hw := Finset.card_sdiff_add_card_inter (support x.val) (support c.val)
  change (support x.val \ support c.val).card + (support x.val ∩ support c.val).card =
    weight x.val at hw
  omega

/-- Common interface for the 36, 40, and 44 branches. The minimum weight is
    a lower bound; no residual classification is used. -/
theorem residual52_parameters {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc0 : 0 < weight c.val) (hc : weight c.val < 48) :
    Fintype.card (Outside c.val) = 52 - weight c.val ∧
    Module.finrank F₂ (LinearMap.range (residualMap C c)) = 7 ∧
    (∀ y ∈ LinearMap.range (residualMap C c), residualWeight y % 2 = 0) ∧
    (∀ y ∈ LinearMap.range (residualMap C c), y ≠ 0 →
      48 ≤ weight c.val + 2 * residualWeight y) := by
  have hn : c ≠ 0 := by
    intro hz
    have hz' : c.val = 0 := congrArg Subtype.val hz
    rw [hz', weight_zero] at hc0
    omega
  exact ⟨outside_card c.val, residual_finrank hmin hdim c hn hc,
    residual_even (doublyEven_selfOrthogonal hD) c, residual_minWeight hmin c⟩

theorem residual36_parameters {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 36) :
    Fintype.card (Outside c.val) = 16 ∧
    Module.finrank F₂ (LinearMap.range (residualMap C c)) = 7 ∧
    (∀ y ∈ LinearMap.range (residualMap C c), residualWeight y % 2 = 0) ∧
    (∀ y ∈ LinearMap.range (residualMap C c), y ≠ 0 → 6 ≤ residualWeight y) := by
  obtain ⟨hl, hk, he, hm⟩ := residual52_parameters hD hdim hmin c (by omega) (by omega)
  refine ⟨by omega, hk, he, ?_⟩
  intro y hy hn
  have h := hm y hy hn
  omega

theorem residual40_parameters {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 40) :
    Fintype.card (Outside c.val) = 12 ∧
    Module.finrank F₂ (LinearMap.range (residualMap C c)) = 7 ∧
    (∀ y ∈ LinearMap.range (residualMap C c), residualWeight y % 2 = 0) ∧
    (∀ y ∈ LinearMap.range (residualMap C c), y ≠ 0 → 4 ≤ residualWeight y) := by
  obtain ⟨hl, hk, he, hm⟩ := residual52_parameters hD hdim hmin c (by omega) (by omega)
  refine ⟨by omega, hk, he, ?_⟩
  intro y hy hn
  have h := hm y hy hn
  omega

theorem residual44_parameters {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 44) :
    Fintype.card (Outside c.val) = 8 ∧
    Module.finrank F₂ (LinearMap.range (residualMap C c)) = 7 ∧
    (∀ y ∈ LinearMap.range (residualMap C c), residualWeight y % 2 = 0) ∧
    (∀ y ∈ LinearMap.range (residualMap C c), y ≠ 0 → 2 ≤ residualWeight y) := by
  obtain ⟨hl, hk, he, hm⟩ := residual52_parameters hD hdim hmin c (by omega) (by omega)
  refine ⟨by omega, hk, he, ?_⟩
  intro y hy hn
  have h := hm y hy hn
  omega

#print axioms residual_weight_identity
#print axioms residual_ker_eq_span
#print axioms residual_finrank
#print axioms residual_minWeight
#print axioms residual36_parameters
#print axioms residual40_parameters
#print axioms residual44_parameters
end So52.Binary
