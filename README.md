# Null-Calibrated Quantum Kernel Learning for Multi-Brain Synchrony Analysis

This repository contains code, configuration files, and reproducibility materials for the manuscript:

**Null-Calibrated Quantum Kernel Learning for Multi-Brain Synchrony Analysis in Human–Human Interaction Systems**

The project evaluates quantum kernel learning as an alternative representation framework for EEG hyperscanning synchrony analysis. The central goal is to test whether real multi-brain synchrony can be separated from null-generated synchrony under quantum and classical kernel representations.

This work does **not** claim quantum advantage. Instead, it provides a null-calibrated benchmark and evaluation pipeline for testing the conditional utility and limitations of quantum kernel learning in human–human interaction systems.

## Research Questions

### RQ1. Real–Null Separability
Can quantum kernel learning improve or alter the separability between real multi-brain synchrony and null-generated synchrony compared with classical kernel methods?

### RQ2. Null-Model Specificity
Do label-permutation, time-shift, and partner-shuffled null models exhibit different separability patterns under quantum and classical kernels?

### RQ3. Evidence-Aware Geometry and Transferability
Does quantum kernel geometry align with null-calibrated synchrony evidence and transfer across triadic and dyadic human–human interaction datasets?

## Main Pipeline

1. Build synchrony feature matrices.
2. Generate real-versus-null benchmarks.
3. Run classical kernel baselines.
4. Run quantum kernel models using Qiskit.
5. Run statistical comparisons.
6. Generate manuscript figures.
7. Generate manuscript tables.

## Interpretation Policy

Allowed:
- quantum kernels as alternative Hilbert-space representations;
- conditional utility under specific null tasks or feature sets;
- framework-level transferability.

Prohibited:
- quantum advantage;
- quantum superiority;
- proof of true neural coupling;
- causal inter-brain connectivity;
- universal superiority of QML over classical methods.

## Repository Structure

See `docs/data_dictionary.md`, `docs/experiment_plan.md`, and `docs/statistical_analysis_plan.md`.

## Data Availability

Raw EEG data are not stored in this repository. Where permitted, anonymized feature-level matrices or synthetic demo matrices will be provided.

## Status

Repository structure initialized. Analysis code and reproducibility materials are under development.
