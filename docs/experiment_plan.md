# Experiment Plan

## Purpose

Evaluate whether quantum kernel learning provides a useful alternative representation geometry for separating real multi-brain EEG synchrony from null-generated synchrony.

## Main Experiments

1. RQ1: Real-null separability in the primary triadic dataset.
2. RQ2: Null-model-specific behavior across label-permutation, time-shift, and partner-shuffled nulls.
3. RQ3: Evidence-aware geometry and external dyadic framework-level validation.

## Feature Sets

- Raw top-K synchrony features.
- Null-sensitive features.
- Evidence-aware features.

Main K values: 4, 6, 8.

## Models

Classical:
- Linear SVM
- Polynomial SVM
- RBF SVM

Quantum:
- ZZFeatureMap quantum kernel
- PauliFeatureMap quantum kernel

## Main Outputs

- Fig. 1: Framework overview
- Fig. 2: RQ1 separability
- Fig. 3: RQ2 null-model specificity
- Fig. 4: RQ3 evidence-aware geometry and transferability
- Table I: Dataset, feature, and null benchmark summary
- Table II: Main statistical comparison
