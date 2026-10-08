import So52.Weight48
import So52.FourierBlocks
import So52.TripleBits

namespace So52.Binary
open Classical

theorem weight48_block_card {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24) (c : C)
    (hc : weight c.val = 48) (t : columnTypes (V := residualKernel C c) (kernelColumns c)) :
    (columnBlock (V := residualKernel C c) (kernelColumns c) t).card = 3 := by
  obtain ⟨i, _, hi⟩ := Finset.mem_image.mp t.property
  change (Finset.univ.filter fun j => kernelColumns c j = t.val).card = 3
  rw [← hi]
  exact (weight48_kernel_structure hD hdim hmin c hc).2.1 i

theorem weight48_blocks_card {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24) (c : C)
    (hc : weight c.val = 48) : Fintype.card (columnTypes (V := residualKernel C c) (kernelColumns c)) = 16 := by
  have h := sum_columnBlocks (V := residualKernel C c) (kernelColumns c) (fun _ => (1 : ℕ))
  simp only [Finset.sum_const, smul_eq_mul, mul_one] at h
  simp_rw [weight48_block_card hD hdim hmin c hc] at h
  simp only [Finset.sum_const, Finset.card_univ, smul_eq_mul, inside_card] at h
  omega

theorem coset_fourier_eq {C : Code 52} (c x : C) (k : residualKernel C c) :
    weightedFourier (kernelColumns c) (fun i => sign (x.val i.val)) k =
      (weight c.val : ℤ) - 2 * insideWeight c.val (x.val + k.val.val) := by
  change (∑ i : Inside c.val, sign (x.val i.val) * sign (k.val.val i.val)) = _
  simp_rw [← sign_add]
  rw [sign_sum_weight, inside_card]
  rfl

theorem weight48_coset2_square {C : Code 52} (hD : DoublyEven C)
    (hmin : MinWeight C 24) (c : C) (hc : weight c.val = 48)
    (x : C) (hx : residualWeight (residualMap C c x) = 2) (k : residualKernel C c) :
    weightedFourier (kernelColumns c) (fun i => sign (x.val i.val)) k ^ 2 = 16 := by
  let z : C := x + k.val
  have hzres : residualMap C c z = residualMap C c x := by
    change residualMap C c (x + k.val) = _
    rw [map_add, show residualMap C c k.val = 0 from k.property, add_zero]
  have hz0 : z.val ≠ 0 := by
    intro hz
    have h : z = 0 := Subtype.ext hz
    have he := congrArg residualWeight hzres
    rw [h, map_zero] at he
    rw [hx] at he
    norm_num [residualWeight] at he
  have hzc : z.val + c.val ≠ 0 := by
    intro hz
    have h : z = c := Subtype.ext ((add_eq_zero_iff _ _).mp hz)
    have he := congrArg residualWeight hzres
    rw [h, show residualMap C c c = 0 from (kernelWord c).property] at he
    rw [hx] at he
    norm_num [residualWeight] at he
  have h₁ := hmin z.val z.property hz0
  have h₂ := hmin (z.val + c.val) (C.add_mem z.property c.property) hzc
  have hd := hD z.val z.property
  have hi := residual_weight_identity c z
  have hs := weight_split c z
  rw [hzres, hx, hc] at hi
  rw [hzres, hx] at hs
  have hin : insideWeight c.val z.val = 22 ∨ insideWeight c.val z.val = 26 := by omega
  rw [coset_fourier_eq, hc]
  change ((48 : ℤ) - 2 * insideWeight c.val z.val) ^ 2 = 16
  rcases hin with hin | hin <;> rw [hin] <;> norm_num

theorem weight48_coset2_block_square {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 48) (x : C)
    (hx : residualWeight (residualMap C c x) = 2) (t : columnTypes (V := residualKernel C c) (kernelColumns c)) :
    (∑ i ∈ columnBlock (V := residualKernel C c) (kernelColumns c) t, sign (x.val i.val)) ^ 2 = 1 := by
  have hp := weighted_parseval_blocks (V := residualKernel C c) (kernelColumns c)
    (fun i => sign (x.val i.val))
  have hk : Fintype.card (residualKernel C c) = 32 := by
    rw [← Nat.card_eq_fintype_card, Module.natCard_eq_pow_finrank (K := F₂),
      (weight48_kernel_structure hD hdim hmin c hc).1]
    simp [Nat.card_eq_fintype_card, F₂, ZMod.card]
  simp_rw [weight48_coset2_square hD hmin c hc x hx] at hp
  simp only [Finset.sum_const, Finset.card_univ, hk] at hp
  have hsum : (∑ t : columnTypes (V := residualKernel C c) (kernelColumns c),
      (∑ i ∈ columnBlock (V := residualKernel C c) (kernelColumns c) t, sign (x.val i.val)) ^ 2) = 16 := by
    apply (mul_left_cancel₀ (by norm_num : (32 : ℤ) ≠ 0))
    simp only [nsmul_eq_mul] at hp
    convert hp.symm using 2
  have hle : ∀ t : columnTypes (V := residualKernel C c) (kernelColumns c), 1 ≤
      (∑ i ∈ columnBlock (V := residualKernel C c) (kernelColumns c) t, sign (x.val i.val)) ^ 2 := fun t =>
    triple_sign_sum_sq_lower _ (weight48_block_card hD hdim hmin c hc t) _
  have heq : (∑ _t : columnTypes (V := residualKernel C c) (kernelColumns c), (1 : ℤ)) =
      ∑ t : columnTypes (V := residualKernel C c) (kernelColumns c),
        (∑ i ∈ columnBlock (V := residualKernel C c) (kernelColumns c) t, sign (x.val i.val)) ^ 2 := by
    rw [hsum]
    simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one]
    rw [weight48_blocks_card hD hdim hmin c hc]
    rfl
  exact ((Finset.sum_eq_sum_iff_of_le (fun t _ => hle t)).mp heq t (Finset.mem_univ _)).symm

theorem weight48_coset2_nonconstant {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (c : C) (hc : weight c.val = 48) (x : C)
    (hx : residualWeight (residualMap C c x) = 2) (t : columnTypes (V := residualKernel C c) (kernelColumns c)) :
    ¬ ConstantOn (columnBlock (V := residualKernel C c) (kernelColumns c) t) (fun i => x.val i.val) := by
  intro hconst
  have hcard := weight48_block_card hD hdim hmin c hc t
  obtain ⟨i, hi⟩ := Finset.card_pos.mp (show 0 < (columnBlock (V := residualKernel C c) (kernelColumns c) t).card by omega)
  have hs := weight48_coset2_block_square hD hdim hmin c hc x hx t
  have he : (∑ j ∈ columnBlock (V := residualKernel C c) (kernelColumns c) t, sign (x.val j.val)) =
      3 * sign (x.val i.val) := by
    calc
      _ = ∑ _j ∈ columnBlock (V := residualKernel C c) (kernelColumns c) t, sign (x.val i.val) :=
        Finset.sum_congr rfl (fun j hj => congrArg sign (hconst j hj i hi))
      _ = _ := by simp [hcard]
  rw [he] at hs
  have hsign : ∀ a : F₂, sign a = 1 ∨ sign a = -1 := by decide
  rcases hsign (x.val i.val) with h | h <;> rw [h] at hs <;> norm_num at hs

#print axioms weight48_coset2_nonconstant
end So52.Binary
