import So52.Weight48Cosets

namespace So52.Binary
open Classical

theorem constant_block_weight {ι : Type*} [DecidableEq ι] (s : Finset ι)
    (hs : s.card = 3) (x : ι → F₂) (hx : ConstantOn s x) :
    (s.filter fun i => x i ≠ 0).card = 0 ∨ (s.filter fun i => x i ≠ 0).card = 3 := by
  obtain ⟨i, hi⟩ := Finset.card_pos.mp (show 0 < s.card by omega)
  by_cases hxi : x i = 0
  · left
    apply Finset.card_eq_zero.mpr
    apply Finset.filter_eq_empty_iff.mpr
    intro j hj hne
    exact hne ((hx j hj i hi).trans hxi)
  · right
    rw [Finset.filter_true_of_mem]
    · exact hs
    · intro j hj
      rw [hx j hj i hi]
      exact hxi

theorem block_constant_inside_divisible {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24) (c : C)
    (hc : weight c.val = 48) (x : C)
    (hx : ∀ t : columnTypes (V := residualKernel C c) (kernelColumns c),
      ConstantOn (columnBlock (V := residualKernel C c) (kernelColumns c) t) (fun i => x.val i.val)) :
    3 ∣ insideWeight c.val x.val := by
  have h := sum_columnBlocks (V := residualKernel C c) (kernelColumns c)
    (fun i => if x.val i.val ≠ 0 then (1 : ℕ) else 0)
  simp only [Finset.sum_boole] at h
  change (∑ t : columnTypes (V := residualKernel C c) (kernelColumns c),
    ((columnBlock (V := residualKernel C c) (kernelColumns c) t).filter fun i => x.val i.val ≠ 0).card) =
      insideWeight c.val x.val at h
  rw [← h]
  apply Finset.dvd_sum
  intro t _
  rcases constant_block_weight _ (weight48_block_card hD hdim hmin c hc t) _ (hx t) with ht | ht
  · rw [ht]; exact dvd_zero _
  · rw [ht]

theorem kernel_constant_on_blocks {C : Code 52} (c : C) (k : residualKernel C c)
    (t : columnTypes (V := residualKernel C c) (kernelColumns c)) :
    ConstantOn (columnBlock (V := residualKernel C c) (kernelColumns c) t) (fun i => k.val.val i.val) := by
  intro i hi j hj
  have he : kernelColumns c i = kernelColumns c j :=
    (Finset.mem_filter.mp hi).2.trans (Finset.mem_filter.mp hj).2.symm
  exact LinearMap.congr_fun he k

theorem constantOn_add {ι : Type*} (s : Finset ι) (x y : ι → F₂)
    (hx : ConstantOn s x) (hy : ConstantOn s y) : ConstantOn s (x + y) := by
  intro i hi j hj
  exact congrArg₂ (· + ·) (hx i hi j hj) (hy i hi j hj)

theorem weight48_coset4_constant_impossible {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24) (c : C)
    (hc : weight c.val = 48) (x : C) (hx : residualWeight (residualMap C c x) = 4)
    (hconst : ∀ t : columnTypes (V := residualKernel C c) (kernelColumns c),
      ConstantOn (columnBlock (V := residualKernel C c) (kernelColumns c) t) (fun i => x.val i.val)) : False := by
  have hzero : ∀ k : residualKernel C c,
      weightedFourier (kernelColumns c) (fun i => sign (x.val i.val)) k = 0 := by
    intro k
    let z : C := x + k.val
    have hzconst : ∀ t : columnTypes (V := residualKernel C c) (kernelColumns c),
        ConstantOn (columnBlock (V := residualKernel C c) (kernelColumns c) t) (fun i => z.val i.val) := by
      intro t
      exact constantOn_add _ _ _ (hconst t) (kernel_constant_on_blocks c k t)
    have hdiv := block_constant_inside_divisible hD hdim hmin c hc z hzconst
    have hres : residualMap C c z = residualMap C c x := by
      change residualMap C c (x + k.val) = _
      rw [map_add, show residualMap C c k.val = 0 from k.property, add_zero]
    have hz0 : z.val ≠ 0 := by
      intro hz
      have he := congrArg residualWeight hres
      rw [show z = 0 from Subtype.ext hz, map_zero] at he
      rw [hx] at he
      norm_num [residualWeight] at he
    have hzc : z.val + c.val ≠ 0 := by
      intro hz
      have he := congrArg residualWeight hres
      rw [show z = c from Subtype.ext ((add_eq_zero_iff _ _).mp hz),
        show residualMap C c c = 0 from (kernelWord c).property] at he
      rw [hx] at he
      norm_num [residualWeight] at he
    have h₁ := hmin z.val z.property hz0
    have h₂ := hmin (z.val + c.val) (C.add_mem z.property c.property) hzc
    have hd := hD z.val z.property
    have hi := residual_weight_identity c z
    have hs := weight_split c z
    rw [hres, hx, hc] at hi
    rw [hres, hx] at hs
    have hin : insideWeight c.val z.val = 24 := by
      have hmod := Nat.mod_eq_zero_of_dvd hdiv
      omega
    rw [coset_fourier_eq, hc]
    change (48 : ℤ) - 2 * insideWeight c.val z.val = 0
    rw [hin]
    norm_num
  have hp := weighted_parseval_blocks (V := residualKernel C c) (kernelColumns c)
    (fun i => sign (x.val i.val))
  simp_rw [hzero] at hp
  have hlo : (Fintype.card (columnTypes (V := residualKernel C c) (kernelColumns c)) : ℤ) ≤
      ∑ t : columnTypes (V := residualKernel C c) (kernelColumns c),
        (∑ i ∈ columnBlock (V := residualKernel C c) (kernelColumns c) t, sign (x.val i.val)) ^ 2 := by
    calc
      _ = ∑ _t : columnTypes (V := residualKernel C c) (kernelColumns c), (1 : ℤ) := by simp
      _ ≤ _ := Finset.sum_le_sum (fun t _ =>
        triple_sign_sum_sq_lower _ (weight48_block_card hD hdim hmin c hc t) _)
  rw [weight48_blocks_card hD hdim hmin c hc] at hlo
  have hk : 0 < (Fintype.card (residualKernel C c) : ℤ) := by
    exact_mod_cast Fintype.card_pos
  simp only [zero_pow (by decide : 2 ≠ 0), Finset.sum_const_zero] at hp
  have hz := (mul_eq_zero.mp hp.symm).resolve_left (ne_of_gt hk)
  have hz' : (∑ t : columnTypes (V := residualKernel C c) (kernelColumns c),
      (∑ i ∈ columnBlock (V := residualKernel C c) (kernelColumns c) t,
        sign (x.val i.val)) ^ 2) = 0 := by
    convert hz using 1
  omega

theorem weight48_six_pairs_impossible {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24) (c : C)
    (hc : weight c.val = 48) (x y z : C)
    (hx : residualWeight (residualMap C c x) = 2)
    (hy : residualWeight (residualMap C c y) = 2)
    (hz : residualWeight (residualMap C c z) = 2)
    (hxy : residualWeight (residualMap C c (x+y)) = 2)
    (hxz : residualWeight (residualMap C c (x+z)) = 2)
    (hyz : residualWeight (residualMap C c (y+z)) = 2)
    (hxyz : residualWeight (residualMap C c (x+y+z)) = 4) : False := by
  apply weight48_coset4_constant_impossible hD hdim hmin c hc (x+y+z) hxyz
  intro t
  exact triple_sum_constant _ (weight48_block_card hD hdim hmin c hc t)
    (fun i => x.val i.val) (fun i => y.val i.val) (fun i => z.val i.val)
    (weight48_coset2_nonconstant hD hdim hmin c hc x hx t)
    (weight48_coset2_nonconstant hD hdim hmin c hc y hy t)
    (weight48_coset2_nonconstant hD hdim hmin c hc z hz t)
    (weight48_coset2_nonconstant hD hdim hmin c hc (x+y) hxy t)
    (weight48_coset2_nonconstant hD hdim hmin c hc (x+z) hxz t)
    (weight48_coset2_nonconstant hD hdim hmin c hc (y+z) hyz t)

theorem residualWeight_reindex {n : ℕ} {c : Word n} (e : Outside c ≃ Fin 4) (y : Word 4) :
    residualWeight (fun i => y (e i)) = weight y := by
  apply Finset.card_bij (fun i _ => e i)
  · intro i hi
    simpa [support] using hi
  · intro i hi j hj hij
    exact e.injective hij
  · intro j hj
    exact ⟨e.symm j, by simpa [support] using hj, e.apply_symm_apply j⟩

/-- Exclusion of weight 48 from the same three hypotheses as no_weight44/52. -/
theorem no_weight48 {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) : weight c.val ≠ 48 := by
  intro hc
  have hout : Fintype.card (Outside c.val) = 4 := by rw [outside_card, hc]
  let e : Outside c.val ≃ Fin 4 := Fintype.equivFinOfCardEq hout
  obtain ⟨a, b, d, ha, hb, hd, hab, had, hbd, habd⟩ :
      ∃ a b d : Word 4, weight a = 2 ∧ weight b = 2 ∧ weight d = 2 ∧
        weight (a+b) = 2 ∧ weight (a+d) = 2 ∧ weight (b+d) = 2 ∧ weight (a+b+d) = 4 := by
    exact ⟨![1,1,0,0], ![1,0,1,0], ![1,0,0,1], by decide⟩
  have hlift (v : Word 4) (hv : weight v = 2) : ∃ x : C, residualMap C c x = fun i => v (e i) := by
    have hmem : (fun i => v (e i)) ∈ evenSpace (Outside c.val) := by
      apply (mem_evenSpace _).mpr
      change residualWeight (fun i => v (e i)) % 2 = 0
      rw [residualWeight_reindex, hv]
    rw [← (weight48_kernel_structure hD hdim hmin c hc).2.2] at hmem
    exact hmem
  obtain ⟨x, hx⟩ := hlift a ha
  obtain ⟨y, hy⟩ := hlift b hb
  obtain ⟨z, hz⟩ := hlift d hd
  apply weight48_six_pairs_impossible hD hdim hmin c hc x y z
  · rw [hx, residualWeight_reindex, ha]
  · rw [hy, residualWeight_reindex, hb]
  · rw [hz, residualWeight_reindex, hd]
  · rw [map_add, hx, hy]
    exact (residualWeight_reindex e (a+b)).trans hab
  · rw [map_add, hx, hz]
    exact (residualWeight_reindex e (a+d)).trans had
  · rw [map_add, hy, hz]
    exact (residualWeight_reindex e (b+d)).trans hbd
  · rw [map_add, map_add, hx, hy, hz]
    exact (residualWeight_reindex e (a+b+d)).trans habd

#print axioms weight48_coset4_constant_impossible
#print axioms no_weight48
end So52.Binary
