# Paper Constitution

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

## Main Experiments

1. Primary triadic dataset: real vs label-permutation null.
2. Primary triadic dataset: real vs time-shift null.
3. Primary triadic dataset: real vs partner-shuffled null.
4. Feature-set comparison: raw top-K, null-sensitive, evidence-aware.
5. External dyadic dataset: framework-level validation.

## Baselines

- Linear kernel SVM
- Polynomial kernel SVM
- RBF kernel SVM
- Quantum ZZFeatureMap kernel
- Quantum PauliFeatureMap kernel

## Primary Metric

Balanced accuracy difference between the pre-specified quantum kernel and the best classical kernel.

## Secondary Metrics

- AUC
- F1
- Kernel-target alignment
- Separability index
- Evidence-aware kernel similarity

## Statistical Plan

- Group-aware repeated cross-validation.
- Paired nonparametric tests.
- Median paired difference.
- Bootstrap 95% confidence interval.
- Rank-biserial or Cliff's delta effect size.
- Holm correction for primary comparisons.
- Benjamini-Hochberg FDR for exploratory analyses.
- Group-aware permutation testing for kernel alignment.

## Main Paper Budget

- Approx. 6,000-6,300 words.
- Four main figures.
- Two main tables.
- One short Appendix only.
- No long Supplement.
- Full reproducibility materials on GitHub.

## Figure and Table Plan

### Fig. 1
Framework overview.

### Fig. 2
RQ1 real-null separability under quantum and classical kernels.

### Fig. 3
RQ2 null-model-specific kernel behavior.

### Fig. 4
RQ3 evidence-aware geometry and external transferability.

### Table I
Dataset, feature, and null benchmark summary.

### Table II
Main statistical comparison.

