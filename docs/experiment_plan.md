# Experiment Plan

## Purpose

This document defines the computational experiments for the manuscript.

The goal is to evaluate whether quantum kernel learning provides a useful alternative representation geometry for separating real multi-brain EEG synchrony from null-generated synchrony.

The study will not claim quantum advantage. The study will compare quantum kernels with strong classical kernel baselines under null-calibrated EEG hyperscanning benchmarks.

## Datasets

### Primary Dataset

Triadic Prisoner's Dilemma EEG hyperscanning dataset.

Role: primary analysis for RQ1, RQ2, and RQ3.

### External Dataset

Dyadic collaboration/competition EEG hyperscanning dataset.

Role: framework-level validation for RQ3.

## Null Tasks

1. Real vs label-permutation null.
2. Real vs time-shift null.
3. Real vs partner-shuffled pseudo-dyad null.

Pooled-null analysis is exploratory only.

## Feature Sets

### Raw Top-K

Features selected by raw synchrony contrast.

### Null-Sensitive

Features selected by real-minus-null attenuation or null sensitivity.

### Evidence-Aware

Features selected by null-calibrated evidence score or structured neighborhood around retained units.

Main K values: 4, 6, 8.

Exploratory K values: 10, 12.

## Models

Classical baselines:

- Linear kernel SVM
- Polynomial kernel SVM
- RBF kernel SVM

Quantum kernels:

- ZZFeatureMap quantum kernel
- PauliFeatureMap quantum kernel

Primary quantum model: ZZFeatureMap.

## Main Experiments

### Experiment 1: RQ1 Real-Null Separability

Compare quantum and classical kernels across real/null tasks.

### Experiment 2: RQ2 Null-Model Specificity

Compare separability patterns across label-permutation, time-shift, and partner-shuffled nulls.

### Experiment 3: RQ3 Evidence-Aware Geometry

Compare raw top-K, null-sensitive, and evidence-aware feature sets.

### Experiment 4: External Validation

Apply the framework to the external dyadic dataset for framework-level transferability.

## Main Outputs

- Fig. 1: Framework overview
- Fig. 2: RQ1 real-null separability
- Fig. 3: RQ2 null-model specificity
- Fig. 4: RQ3 evidence-aware geometry and transferability
- Table I: Dataset, feature, and null benchmark summary
- Table II: Main statistical comparison

## Implementation Phases

### Phase 1

Minimal pilot with synthetic demo data.

### Phase 2

Primary dataset with time-shift and label-permutation nulls.

### Phase 3

Add partner-shuffled null and evidence-aware features.

### Phase 4

External dyadic validation.

### Phase 5

Final figures, tables, appendix, and manuscript writing.
