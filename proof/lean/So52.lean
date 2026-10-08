import So52.LowerBound
import So52.Reductions
import So52.Kernel
import So52.Residual
import So52.Weight44
import So52.Weight52
import So52.Weight48Exclusion
import So52.Weight40
import So52.ResidualMoments
import So52.Weight40Equality
import So52.Section4

/- Review entry point.
   Proved: an explicit self-orthogonal [52,9,20] construction, the half-weight
   linear functional/kernel reduction, residual-code parameter bounds,
   and exclusion of weights 44, 48, and 52 in a doubly-even [52,8,>=24] code.
   Weight 40: necessary integer Fourier constraints with actual witnesses, NOT exclusion.
   Maximum weight <= 36 is proved only conditional on exclusion of weight 40.
   Weight-40 residual dual distance >= 4 (with the old >= 3 corollary) is proved.
   Weight moments 768/4992 and inner Parseval equality 5120 are proved.
   Assuming a weight-40 codeword exists, its actual inner column multiplicities
   are 0/1, and Fourier values at nonzero residual words attain endpoints.
   Residual classification, cubic reduction, and exhaustive exclusion remain unproved.
   The [52,9] general distance upper bound is an explicit argument to reduction52.
   NOT proved: nonexistence of self-orthogonal [52,9,22] codes.
   External classifications and exhaustive-search completeness are not axioms here. -/

#print axioms So52.lower_bound_certificate
#print axioms So52.Binary.no_weight44
#print axioms So52.Binary.no_weight52
#print axioms So52.Binary.no_weight48
#print axioms So52.Binary.weight40_integer_constraints
#print axioms So52.Binary.weight40_integer_constraints_with_witnesses
#print axioms So52.Binary.max_weight_le36_of_no_weight40
#print axioms So52.Binary.column_multiplicity_sum
#print axioms So52.Binary.collisionCount_eq_sum_multiplicity_sq
#print axioms So52.Binary.even12_card128_dual_minWeight
#print axioms So52.Binary.length12_card128_weight_moments
#print axioms So52.Binary.weight40_residual_dual_minWeight
#print axioms So52.Binary.weight40_residual_moments
#print axioms So52.Binary.even12_card128_dual_minWeight_four
#print axioms So52.Binary.weight40_residual_dual_minWeight_four
#print axioms So52.Binary.weight40_moment_saturation
#print axioms So52.Binary.weight40_parseval_equality_with_witnesses
