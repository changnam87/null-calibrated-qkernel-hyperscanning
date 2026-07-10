# Statistical Analysis Plan

## Primary Outcome

Balanced accuracy difference:

Delta BA = BA_quantum - BA_best_classical

## Secondary Outcomes

- AUC
- F1
- Kernel-target alignment
- Separability index
- Evidence-aware kernel similarity

## Cross-Validation

Use group-aware repeated cross-validation with identical splits across all quantum and classical kernels.

Primary dataset:
- triad-aware or group-session-aware splitting

External dataset:
- dyad-aware splitting

## Main Test

Use paired comparisons across repeated splits.

Report:
- median paired difference
- bootstrap 95% confidence interval
- Wilcoxon signed-rank test
- rank-biserial correlation or Cliff's delta
- Holm-corrected p-value

## Multiple Comparisons

- Holm correction for primary comparison families
- Benjamini-Hochberg FDR for exploratory feature-set and ablation analyses

## Interpretation

Results support conditional utility or limitations of quantum kernel representations. They do not support claims of quantum advantage or proof of interaction-specific neural coupling.
