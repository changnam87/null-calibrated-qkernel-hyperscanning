#!/usr/bin/env python
from pathlib import Path

DOCS = Path("docs")
DOCS.mkdir(exist_ok=True)

FILES = {}

FILES["paper_constitution.md"] = """# Paper Constitution

## Title

Null-Calibrated Quantum Kernel Learning for Multi-Brain Synchrony Analysis in Human–Human Interaction Systems

## Target Journal

IEEE Transactions on Cybernetics

## Positioning

This paper is positioned as a computational intelligence and methodological contribution for human-human interaction systems. It is not framed as a neuroscience-only EEG hyperscanning paper or as a simple application of quantum machine learning to EEG classification.

The central task is real-versus-null synchrony representation, not cooperation/noncooperation prediction.

## Core Thesis

Multi-brain EEG synchrony analysis should not rely only on raw synchrony magnitude because apparent synchrony may reflect shared task timing, common stimulus structure, frequency-band effects, or pseudo-dyad reproducibility.

This paper formulates EEG hyperscanning synchrony analysis as a null-calibrated real-versus-null representation geometry problem. Quantum kernel learning is evaluated as an alternative Hilbert-space embedding for separating real interaction-related synchrony from null-reproducible synchrony.

The paper does not claim quantum advantage or definitive neural coupling. It evaluates the conditional utility and limitations of quantum kernels under rigorous classical baselines, null models, statistical testing, and external validation.

## Research Questions

### RQ1. Real-Null Separability

Can quantum kernel learning improve or alter the separability between real multi-brain synchrony and null-generated synchrony compared with classical kernel methods?

### RQ2. Null-Model Specificity

Do label-permutation, time-shift, and partner-shuffled null models exhibit different separability patterns under quantum and classical kernels?

### RQ3. Evidence-Aware Geometry and Transferability

Does quantum kernel geometry align with null-calibrated synchrony evidence and transfer across triadic and dyadic human-human interaction datasets?

## Contributions

1. Formulate EEG hyperscanning synchrony analysis as a null-calibrated real-versus-null representation problem.
2. Propose a quantum kernel learning framework for multi-brain synchrony analysis in human-human interaction systems.
3. Construct a null-specific benchmark using label-permutation, time-shift, and partner-shuffled pseudo-dyad models.
4. Compare quantum kernels against classical linear, polynomial, and RBF kernels using predefined statistical tests.
5. Evaluate evidence-aware kernel geometry and framework-level transferability across triadic and dyadic hyperscanning datasets.

## Related Work Logic

The Related Work section should justify the RQs rather than simply list prior work.

### Subsection A: EEG Hyperscanning and the Need for Real-Null Synchrony Separation

Purpose: justify RQ1.

Logic: EEG hyperscanning provides measures of inter-brain synchrony, but raw synchrony is vulnerable to shared timing, common stimuli, analysis choices, and null-reproducible structure. Therefore, real-versus-null separation is necessary.

### Subsection B: Null-Calibrated Evidence Mapping and Null-Model Specificity

Purpose: justify RQ2.

Logic: Different null models test different alternative explanations. Label-permutation, time-shift, and partner-shuffled pseudo-dyad nulls should not be collapsed into a single generic null without first examining their specific behavior.

### Subsection C: Kernel Learning and Quantum Kernels for Neurophysiological Representation

Purpose: justify RQ3.

Logic: EEG/BCI methods have long focused on representation learning and feature extraction. Quantum kernels provide an alternative Hilbert-space representation, but their utility for null-calibrated multi-brain synchrony geometry has not been systematically evaluated.

## Claims Allowed

- Quantum kernels are evaluated as alternative Hilbert-space representations.
- The framework tests real-versus-null synchrony separability.
- Results show conditional utility or limitations of quantum kernel learning.
- Retained synchrony structure is candidate interaction-sensitive evidence.
- External validation is framework-level, not pattern-level replication.

## Claims Prohibited

- Quantum advantage.
- Quantum superiority.
- QML proves true neural coupling.
- QML is inherently better than classical ML.
- EEG hyperscanning requires quantum computing.
- Retained units are causal or source-localized neural interactions.

## Main Paper Budget

- Approx. 6,000-6,300 words.
- Four main figures.
- Two main tables.
- One short Appendix only.
- No long Supplement.
- Full reproducibility materials on GitHub.
"""

FILES["experiment_plan.md"] = """# Experiment Plan

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
"""

FILES["statistical_analysis_plan.md"] = """# Statistical Analysis Plan

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
"""

FILES["data_dictionary.md"] = """# Data Dictionary

## Core Objects

- Synchrony unit table
- Observation-level feature matrix
- Feature map table
- Null benchmark table
- Cross-validation split table
- Prediction output table
- Metric output table
- Statistical result table

## Observation-Level Feature Matrix

Required columns:

- obs_id
- dataset
- group_id
- session_id
- trial_id
- window_id
- dyad_id
- condition
- null_task
- label
- feature_set
- K
- f001 ... f00K

The label column uses:

- 1 = real
- 0 = null-generated

## Feature Map Table

Required columns:

- feature_name
- feature_index
- unit_id
- dataset
- window
- band
- dyad_label
- edge_id
- channel_i
- channel_j
- metric
- selection_rule
- selection_rank
- selection_score

## Null Benchmark Table

Required columns:

- obs_id
- paired_obs_id
- dataset
- null_task
- group_id
- session_id
- trial_id
- dyad_id
- label
- source_type
- feature_set
- K
- split_group

Use source_type values:

- real
- null_generated

Do not use the literal string null because pandas may parse it as missing data.

## Prediction Output Table

Required columns:

- split_id
- repeat_id
- fold_id
- dataset
- null_task
- feature_set
- K
- model
- obs_id
- y_true
- y_pred
- y_score

## Metric Output Table

Required columns:

- split_id
- repeat_id
- fold_id
- dataset
- null_task
- feature_set
- K
- model
- balanced_accuracy
- auc
- f1
- sensitivity
- specificity
- kernel_alignment
- separability_index
- K_RR
- K_NN
- K_RN

## Statistical Result Table

Required columns:

- comparison_id
- dataset
- null_task
- feature_set
- K
- metric
- model_a
- model_b
- median_delta
- mean_delta
- ci_lower
- ci_upper
- effect_size_name
- effect_size
- p_raw
- p_adjusted
- correction_method
- test_name
- n_splits
- interpretation_flag
"""

for name, content in FILES.items():
    path = DOCS / name
    path.write_text(content)
    print(f"PASS: updated {path}")

print("PASS: all core documentation files updated.")
