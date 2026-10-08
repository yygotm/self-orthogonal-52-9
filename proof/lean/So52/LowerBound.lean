import Std.Tactic

/- Independent encoding: coordinate 0 is the LEFTMOST character in the source matrix.
   This file proves the explicit construction only, not the nonexistence upper bound. -/
namespace So52
set_option maxRecDepth 100000
set_option maxHeartbeats 2000000
local instance : Std.Associative Bool.xor := ⟨Bool.xor_assoc⟩
local instance : Std.Commutative Bool.xor := ⟨Bool.xor_comm⟩

def encode (m : BitVec 9) : BitVec 52 :=
  (if m.getLsbD 0 then (15609764721841 : BitVec 52) else 0) ^^^
  (if m.getLsbD 1 then (31219529443682 : BitVec 52) else 0) ^^^
  (if m.getLsbD 2 then (62439058887364 : BitVec 52) else 0) ^^^
  (if m.getLsbD 3 then (124878117774728 : BitVec 52) else 0) ^^^
  (if m.getLsbD 4 then (249756235549456 : BitVec 52) else 0) ^^^
  (if m.getLsbD 5 then (499512471098912 : BitVec 52) else 0) ^^^
  (if m.getLsbD 6 then (999024942197824 : BitVec 52) else 0) ^^^
  (if m.getLsbD 7 then (1998049884395648 : BitVec 52) else 0) ^^^
  (if m.getLsbD 8 then (4503599627370495 : BitVec 52) else 0)

def dotParity (x y : BitVec 52) : Bool :=
  (x &&& y).getLsbD 0 ^^
  (x &&& y).getLsbD 1 ^^
  (x &&& y).getLsbD 2 ^^
  (x &&& y).getLsbD 3 ^^
  (x &&& y).getLsbD 4 ^^
  (x &&& y).getLsbD 5 ^^
  (x &&& y).getLsbD 6 ^^
  (x &&& y).getLsbD 7 ^^
  (x &&& y).getLsbD 8 ^^
  (x &&& y).getLsbD 9 ^^
  (x &&& y).getLsbD 10 ^^
  (x &&& y).getLsbD 11 ^^
  (x &&& y).getLsbD 12 ^^
  (x &&& y).getLsbD 13 ^^
  (x &&& y).getLsbD 14 ^^
  (x &&& y).getLsbD 15 ^^
  (x &&& y).getLsbD 16 ^^
  (x &&& y).getLsbD 17 ^^
  (x &&& y).getLsbD 18 ^^
  (x &&& y).getLsbD 19 ^^
  (x &&& y).getLsbD 20 ^^
  (x &&& y).getLsbD 21 ^^
  (x &&& y).getLsbD 22 ^^
  (x &&& y).getLsbD 23 ^^
  (x &&& y).getLsbD 24 ^^
  (x &&& y).getLsbD 25 ^^
  (x &&& y).getLsbD 26 ^^
  (x &&& y).getLsbD 27 ^^
  (x &&& y).getLsbD 28 ^^
  (x &&& y).getLsbD 29 ^^
  (x &&& y).getLsbD 30 ^^
  (x &&& y).getLsbD 31 ^^
  (x &&& y).getLsbD 32 ^^
  (x &&& y).getLsbD 33 ^^
  (x &&& y).getLsbD 34 ^^
  (x &&& y).getLsbD 35 ^^
  (x &&& y).getLsbD 36 ^^
  (x &&& y).getLsbD 37 ^^
  (x &&& y).getLsbD 38 ^^
  (x &&& y).getLsbD 39 ^^
  (x &&& y).getLsbD 40 ^^
  (x &&& y).getLsbD 41 ^^
  (x &&& y).getLsbD 42 ^^
  (x &&& y).getLsbD 43 ^^
  (x &&& y).getLsbD 44 ^^
  (x &&& y).getLsbD 45 ^^
  (x &&& y).getLsbD 46 ^^
  (x &&& y).getLsbD 47 ^^
  (x &&& y).getLsbD 48 ^^
  (x &&& y).getLsbD 49 ^^
  (x &&& y).getLsbD 50 ^^
  (x &&& y).getLsbD 51

def weight (x : BitVec 52) : Nat := x.cpop.toNat

def decode (x : BitVec 52) : BitVec 9 :=
  (if x.getLsbD 0 ^^ x.getLsbD 51 then (1 : BitVec 9) else 0) ^^^
  (if x.getLsbD 1 ^^ x.getLsbD 51 then (2 : BitVec 9) else 0) ^^^
  (if x.getLsbD 2 ^^ x.getLsbD 51 then (4 : BitVec 9) else 0) ^^^
  (if x.getLsbD 3 ^^ x.getLsbD 51 then (8 : BitVec 9) else 0) ^^^
  (if x.getLsbD 0 ^^ x.getLsbD 4 then (16 : BitVec 9) else 0) ^^^
  (if x.getLsbD 0 ^^ x.getLsbD 1 ^^ x.getLsbD 5 ^^ x.getLsbD 51 then (32 : BitVec 9) else 0) ^^^
  (if x.getLsbD 1 ^^ x.getLsbD 2 ^^ x.getLsbD 6 ^^ x.getLsbD 51 then (64 : BitVec 9) else 0) ^^^
  (if x.getLsbD 0 ^^ x.getLsbD 2 ^^ x.getLsbD 3 ^^ x.getLsbD 7 then (128 : BitVec 9) else 0) ^^^
  (if x.getLsbD 51 then (256 : BitVec 9) else 0)

theorem select_xor (a b : Bool) (r : BitVec 52) :
    (if a ^^ b then r else 0) =
      ((if a then r else 0) ^^^ (if b then r else 0)) := by
  cases a <;> cases b <;> simp

theorem dot_xor_left (x y z : BitVec 52) :
    dotParity (x ^^^ y) z = (dotParity x z ^^ dotParity y z) := by
  simp only [dotParity, BitVec.getLsbD_and, BitVec.getLsbD_xor,
    Bool.and_xor_distrib_right]
  ac_rfl

theorem dot_xor_right (x y z : BitVec 52) :
    dotParity x (y ^^^ z) = (dotParity x y ^^ dotParity x z) := by
  simp only [dotParity, BitVec.getLsbD_and, BitVec.getLsbD_xor,
    Bool.and_xor_distrib_left]
  ac_rfl

theorem dot_select_left (b : Bool) (x y : BitVec 52) :
    dotParity (if b then x else 0) y = (b && dotParity x y) := by
  cases b <;> simp [dotParity]

theorem dot_select_right (b : Bool) (x y : BitVec 52) :
    dotParity x (if b then y else 0) = (b && dotParity x y) := by
  cases b <;> simp [dotParity]

theorem encode_zero : encode 0 = 0 := by decide

theorem encode_linear (a b : BitVec 9) :
    encode (a ^^^ b) = encode a ^^^ encode b := by
  simp only [encode, BitVec.getLsbD_xor, select_xor]
  ac_rfl

theorem decode_encode : ∀ m : BitVec 9, decode (encode m) = m := by decide

theorem encode_injective (a b : BitVec 9) (h : encode a = encode b) : a = b := by
  have hd := congrArg decode h
  simpa only [decode_encode] using hd

theorem self_orthogonal (a b : BitVec 9) :
    dotParity (encode a) (encode b) = false := by
  simp only [encode, dot_xor_left, dot_xor_right, dot_select_left, dot_select_right]
  simp [dotParity]

theorem minimum_weight_lower :
    ∀ m : BitVec 9, m ≠ 0 → 20 ≤ weight (encode m) := by
  decide

theorem minimum_weight_attained :
    ∃ m : BitVec 9, m ≠ 0 ∧ weight (encode m) = 20 := by
  decide

theorem pairwise_distance_lower (a b : BitVec 9) (hab : a ≠ b) :
    20 ≤ weight (encode a ^^^ encode b) := by
  rw [← encode_linear]
  exact minimum_weight_lower (a ^^^ b) (fun hz => hab (BitVec.xor_eq_zero_iff.mp hz))

/-- A binary linear encoder with 9 independent message bits, length 52,
    orthogonal image, minimum distance at least 20 and an attained weight of 20. -/
theorem lower_bound_certificate :
    encode 0 = 0 ∧
    (∀ a b, encode (a ^^^ b) = encode a ^^^ encode b) ∧
    (∀ a b, encode a = encode b → a = b) ∧
    (∀ a b, dotParity (encode a) (encode b) = false) ∧
    (∀ a b, a ≠ b → 20 ≤ weight (encode a ^^^ encode b)) ∧
    (∃ m : BitVec 9, m ≠ 0 ∧ weight (encode m) = 20) :=
  ⟨encode_zero, encode_linear, encode_injective, self_orthogonal,
    pairwise_distance_lower, minimum_weight_attained⟩

#print axioms encode_linear
#print axioms encode_injective
#print axioms self_orthogonal
#print axioms minimum_weight_lower
#print axioms minimum_weight_attained
#print axioms pairwise_distance_lower
#print axioms lower_bound_certificate
end So52
