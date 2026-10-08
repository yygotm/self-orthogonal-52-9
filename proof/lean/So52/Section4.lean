import So52.Weight44
import So52.Weight52
import So52.Weight48Exclusion

/- Conditional assembly of the weight exclusions.
   The weight-40 exclusion is an explicit hypothesis, not a proved result. -/
namespace So52.Binary

theorem max_weight_le36_of_no_weight40 {C : Code 52} (hD : DoublyEven C)
    (hdim : Module.finrank F₂ C = 8) (hmin : MinWeight C 24)
    (h40 : ∀ c : C, weight c.val ≠ 40) :
    ∀ c : C, weight c.val ≤ 36 := by
  intro c
  have hbound : weight c.val ≤ 52 := by
    simpa only [weight, support, Finset.card_univ, Fintype.card_fin] using
      Finset.card_filter_le (Finset.univ : Finset (Fin 52)) (fun i => c.val i ≠ 0)
  have hdiv := hD c.val c.property
  have h44 := no_weight44 hD hdim hmin c
  have h48 := no_weight48 hD hdim hmin c
  have h52 := no_weight52 hD hdim hmin c
  have h40c := h40 c
  omega

#print axioms max_weight_le36_of_no_weight40
end So52.Binary
