# Statistical Analysis Plan

## Purpose

This plan defines how quantum and classical kernel models will be compared.

The goal is not to claim quantum advantage. The goal is to evaluate whether quantum kernels provide conditional utility as alternative representations for null-calibrated multi-brain synchrony analysis.

## Primary Outcome

Balanced accuracy difference:

Delta BA = BA_quantum - BA_best_classical

The primary comparison uses the pre-specified ZZFeatureMap quantum kernel versus the best classical kernel among linear, polynomial, and RBF kernels within the same split and feature setting.

## Secondary Outcomes

- AUC
- F1 score
- Kernel-target alignment
- Separability index
- Evidence-aware kernel similarity

## Cross-Validation

All models must use identical splits.

Primary dataset:

- group-aware or triad-aware splitting

External dataset:

- dyad-aware splitting

The same real/null counterpart should not leak across train and test when it would create dependence.

## Main Test

For each split, compute paired differences between quantum and best classical performance.

Report:

- median paired difference
- bootstrap 95% confidence interval
- Wilcoxon signed-rank test
- rank-biserial correlation or Cliff's delta
- Holm-corrected p-value

## Multiple Comparisons

Primary comparison families use Holm correction.

Exploratory feature-set and ablation analyses use Benjamini-Hochberg FDR.

## Permutation Tests

Group-aware permutation tests may be used for:

- kernel-target alignment
- AUC significance
- separability index

Final analyses should use 1000 permutations where feasible.

## Interpretation Rule

Quantum kernels should be interpreted as beneficial only when they show:

1. positive median effect,
2. confidence interval excluding negligible differences,
3. meaningful effect size,
4. corrected statistical support.

Otherwise, results should be described as comparable, mixed, or negative.

## Prohibited Claims

The statistical analysis must not be used to claim:

- quantum advantage,
- quantum superiority,
- proof of true neural coupling,
- causal inter-brain connectivity,
- universal superiority of QML.
