# Null-Calibrated Quantum Kernel Learning for Multi-Brain Synchrony Analysis

This repository contains code, configuration files, and reproducibility materials for the manuscript:

**Null-Calibrated Quantum Kernel Learning for Multi-Brain Synchrony Analysis in Human-Human Interaction Systems**

This work does **not** claim quantum advantage. It provides a null-calibrated benchmark and evaluation pipeline for testing the conditional utility and limitations of quantum kernel learning in EEG hyperscanning.

## Research Questions

### RQ1. Real-Null Separability

Can quantum kernel learning improve or alter the separability between real multi-brain synchrony and null-generated synchrony compared with classical kernel methods?

### RQ2. Null-Model Specificity

Do label-permutation, time-shift, and partner-shuffled null models exhibit different separability patterns under quantum and classical kernels?

### RQ3. Evidence-Aware Geometry and Transferability

Does quantum kernel geometry align with null-calibrated synchrony evidence and transfer across triadic and dyadic human-human interaction datasets?

## Demo Pipeline

Run:

```bash
bash scripts/run_demo_pipeline.sh
```

The demo data are synthetic and are used only for pipeline validation. They are not EEG data and should not be interpreted scientifically.

## Tests

Run:

```bash
pytest -q
```

## Quantum Kernel Analysis

Quantum kernel learning is implemented using Qiskit with ZZFeatureMap and PauliFeatureMap.

Quantum kernels are evaluated as alternative Hilbert-space representations for real/null synchrony separation. They are not used to claim quantum advantage.

## Classical Baselines

Quantum kernels are compared against:

- linear kernel SVM
- polynomial kernel SVM
- RBF kernel SVM

## Data Availability

Raw EEG data are not stored in this repository.

Where permitted, anonymized feature-level matrices or synthetic demo matrices will be provided.

## Known Warnings

Current Qiskit versions may produce deprecation warnings for ZZFeatureMap and PauliFeatureMap. These warnings do not affect the current demo pipeline.

## License

This repository is currently released under the MIT License.
