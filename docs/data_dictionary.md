# Data Dictionary

This document defines the standardized data formats for the project:

**Null-Calibrated Quantum Kernel Learning for Multi-Brain Synchrony Analysis in Human-Human Interaction Systems**

The purpose of this document is to ensure that synchrony units, feature matrices, null benchmarks, cross-validation splits, model predictions, metrics, and statistical outputs use consistent machine-readable formats.

---

# 1. Core Data Objects

The project uses the following core data objects.

| Object | File type | Purpose |
|---|---|---|
| Actual synchrony unit table | `.csv` | Bridge from existing EEG hyperscanning outputs to this repository |
| Observation-level feature matrix | `.csv` | Input matrix for classical and quantum kernel models |
| Feature map table | `.csv` | Maps feature columns to synchrony units |
| Null benchmark table | `.csv` | Real-versus-null benchmark metadata |
| Cross-validation split table | `.csv` | Group-aware train/test split definitions |
| Prediction output table | `.csv` | Model-level predictions |
| Metric output table | `.csv` | Fold-level performance and kernel metrics |
| Statistical result table | `.csv` | Paired model comparisons and corrected statistics |

---

# 2. Actual Synchrony Unit Table

## 2.1 Purpose

The actual synchrony unit table is the bridge between existing EEG hyperscanning analysis outputs and this repository's quantum/classical kernel pipeline.

Each row represents one synchrony unit:

```text
u = (window, band, dyad, edge, metric)
```

Recommended filenames:

```text
data/features/primary_synchrony_units.csv
data/features/external_synchrony_units.csv
```

## 2.2 Required Columns

```text
unit_id
dataset
group_id
session_id
condition
window
band
dyad_label
edge_id
channel_i
channel_j
metric
real_score
label_null_score
time_null_score
partner_null_score
raw_contrast
label_attenuation
time_attenuation
partner_attenuation
evidence_score
```

## 2.3 Column Definitions

| Column | Meaning |
|---|---|
| `unit_id` | Unique synchrony unit ID |
| `dataset` | `primary`, `external`, or `demo_primary` |
| `group_id` | Triad, group, dyad, or session identifier |
| `session_id` | Session or recording identifier |
| `condition` | Cooperation, noncooperation, collaboration, competition, or other task condition |
| `window` | Decision, feedback, task03, task04, or other event window |
| `band` | Frequency band: delta, theta, alpha, beta, gamma |
| `dyad_label` | Pair or dyad label, e.g., pair12, pair13, pair23, dyad01 |
| `edge_id` | Inter-brain channel-pair identifier |
| `channel_i` | EEG channel from participant i |
| `channel_j` | EEG channel from participant j |
| `metric` | PLV, coherence, or combined |
| `real_score` | Synchrony score or synchrony contrast from real data |
| `label_null_score` | Corresponding label-permutation null score |
| `time_null_score` | Corresponding time-shift null score |
| `partner_null_score` | Corresponding partner-shuffled null score |
| `raw_contrast` | Raw ranking score |
| `label_attenuation` | Real score minus label-null score |
| `time_attenuation` | Real score minus time-shift null score |
| `partner_attenuation` | Real score minus partner-shuffled null score |
| `evidence_score` | Null-calibrated evidence score |

## 2.4 Recommended Score Definitions

Initial v1 definitions:

```text
raw_contrast = abs(real_score)
label_attenuation = real_score - label_null_score
time_attenuation = real_score - time_null_score
partner_attenuation = real_score - partner_null_score
```

Normalized attenuation may be added later:

```text
attenuation_ratio = 1 - null_score / real_score
```

However, difference-based attenuation is preferred for v1 because it is more stable when real scores are near zero.

## 2.5 Optional Columns

```text
plv_real
coh_real
plv_label_null
coh_label_null
plv_time_null
coh_time_null
plv_partner_null
coh_partner_null
p_label
p_time
p_partner
z_label
z_time
z_partner
rank_raw
rank_null_sensitive
rank_evidence
```

## 2.6 Adapter Principle

Existing EEG hyperscanning outputs should first be converted into the synchrony unit table. The standard feature-building pipeline should then convert the synchrony unit table into observation-level feature matrices for quantum/classical kernel analysis.

Pipeline:

```text
existing TNSRE/hyperscanning outputs
        ↓
primary_synchrony_units.csv
        ↓
feature selection: raw_topk / null_sensitive / evidence_aware
        ↓
observation-level feature matrix
        ↓
classical + quantum kernel analysis
```

---

# 3. Observation-Level Feature Matrix

## 3.1 Purpose

The observation-level feature matrix is the direct input to classical and quantum kernel models.

Each row is one real or null-generated observation.

Each feature column corresponds to one selected synchrony unit.

Shape:

```text
X = n observations × K selected features
```

Recommended filenames:

```text
data/features/primary_X_raw_topk_K4_time_shift.csv
data/features/primary_X_null_sensitive_K6_label_permutation.csv
data/features/primary_X_evidence_aware_K8_partner_shuffle.csv
data/demo_tiny/demo_primary_X_raw_topk_K4_time_shift.csv
```

## 3.2 Required Columns

```text
obs_id
dataset
group_id
session_id
trial_id
window_id
dyad_id
condition
null_task
label
feature_set
K
f001
f002
...
f00K
```

## 3.3 Column Definitions

| Column | Meaning |
|---|---|
| `obs_id` | Unique observation ID |
| `dataset` | Dataset name, e.g., primary, external, demo_primary |
| `group_id` | Group, triad, session, or dyad identifier used for group-aware splitting |
| `session_id` | Session identifier |
| `trial_id` | Trial or segment identifier |
| `window_id` | Event window or task segment |
| `dyad_id` | Dyad identifier |
| `condition` | Real condition or null condition label |
| `null_task` | `label_permutation`, `time_shift`, `partner_shuffle`, or `real` |
| `label` | Binary learning label: 1 = real, 0 = null-generated |
| `feature_set` | `raw_topk`, `null_sensitive`, or `evidence_aware` |
| `K` | Number of selected features |
| `f001...f00K` | Selected synchrony feature values |

## 3.4 Label Convention

```text
1 = real synchrony
0 = null-generated synchrony
```

---

# 4. Feature Map Table

## 4.1 Purpose

The feature map table links generic feature columns such as `f001`, `f002`, and `f003` back to the actual synchrony units they represent.

Recommended filenames:

```text
data/features/primary_feature_map_raw_topk_K4.csv
data/features/primary_feature_map_null_sensitive_K6.csv
data/features/primary_feature_map_evidence_aware_K8.csv
```

## 4.2 Required Columns

```text
feature_name
feature_index
unit_id
dataset
window
band
dyad_label
edge_id
channel_i
channel_j
metric
selection_rule
selection_rank
selection_score
```

## 4.3 Column Definitions

| Column | Meaning |
|---|---|
| `feature_name` | Feature column name, e.g., f001 |
| `feature_index` | Numeric feature index |
| `unit_id` | Synchrony unit ID |
| `dataset` | Dataset name |
| `window` | Event window or task segment |
| `band` | Frequency band |
| `dyad_label` | Dyad label |
| `edge_id` | Inter-brain channel-pair edge ID |
| `channel_i` | Channel from participant i |
| `channel_j` | Channel from participant j |
| `metric` | PLV, coherence, or combined |
| `selection_rule` | raw_topk, null_sensitive, or evidence_aware |
| `selection_rank` | Rank within selected feature set |
| `selection_score` | Score used for feature selection |

---

# 5. Null Benchmark Table

## 5.1 Purpose

The null benchmark table stores metadata for real-versus-null classification tasks.

Recommended filenames:

```text
data/features/primary_null_benchmark_raw_topk_K4_time_shift.csv
data/features/primary_null_benchmark_null_sensitive_K6_label_permutation.csv
data/features/primary_null_benchmark_evidence_aware_K8_partner_shuffle.csv
```

## 5.2 Required Columns

```text
obs_id
paired_obs_id
dataset
null_task
group_id
session_id
trial_id
dyad_id
label
source_type
feature_set
K
split_group
```

## 5.3 Column Definitions

| Column | Meaning |
|---|---|
| `obs_id` | Observation ID |
| `paired_obs_id` | Matched real/null counterpart, if available |
| `dataset` | Dataset name |
| `null_task` | Null task name |
| `group_id` | Group or dyad identifier |
| `session_id` | Session identifier |
| `trial_id` | Trial identifier |
| `dyad_id` | Dyad identifier |
| `label` | 1 = real, 0 = null-generated |
| `source_type` | `real` or `null_generated` |
| `feature_set` | Feature selection family |
| `K` | Number of selected features |
| `split_group` | Grouping variable for group-aware splitting |

## 5.4 Source Type Convention

Use:

```text
real
null_generated
```

Do not use the literal string `null` because pandas may parse it as missing data.

---

# 6. Cross-Validation Split Table

## 6.1 Purpose

The cross-validation split table stores group-aware train/test assignments.

Recommended filenames:

```text
data/splits/primary_group_cv_splits_raw_topk_K4_time_shift.csv
data/splits/external_group_cv_splits_raw_topk_K4_partner_shuffle.csv
```

## 6.2 Required Columns

```text
split_id
repeat_id
fold_id
obs_id
dataset
split
split_group
null_task
feature_set
K
```

## 6.3 Column Definitions

| Column | Meaning |
|---|---|
| `split_id` | Unique split identifier |
| `repeat_id` | Repetition index |
| `fold_id` | Fold index |
| `obs_id` | Observation ID |
| `dataset` | Dataset name |
| `split` | `train` or `test` |
| `split_group` | Grouping variable used for leakage control |
| `null_task` | Null task name |
| `feature_set` | Feature selection family |
| `K` | Number of selected features |

## 6.4 Integrity Rule

Within each split, the same `obs_id` must not appear in both train and test.

Where feasible, the same `split_group` should not appear in both train and test.

---

# 7. Prediction Output Table

## 7.1 Purpose

The prediction table stores observation-level model outputs.

Recommended filenames:

```text
results/primary/classical_predictions_raw_topk_K4_time_shift.csv
results/primary/quantum_predictions_raw_topk_K4_time_shift.csv
```

## 7.2 Required Columns

```text
split_id
repeat_id
fold_id
dataset
null_task
feature_set
K
model
obs_id
y_true
y_pred
y_score
```

## 7.3 Column Definitions

| Column | Meaning |
|---|---|
| `split_id` | Split identifier |
| `repeat_id` | Repetition index |
| `fold_id` | Fold index |
| `dataset` | Dataset name |
| `null_task` | Null task name |
| `feature_set` | Feature selection family |
| `K` | Number of selected features |
| `model` | Model name |
| `obs_id` | Observation ID |
| `y_true` | True label |
| `y_pred` | Predicted label |
| `y_score` | Decision score or probability-like score |

---

# 8. Metric Output Table

## 8.1 Purpose

The metric table stores split-level model performance and kernel-geometry metrics.

Recommended filenames:

```text
results/primary/classical_metrics_raw_topk_K4_time_shift.csv
results/primary/quantum_metrics_raw_topk_K4_time_shift.csv
```

## 8.2 Required Columns

```text
split_id
repeat_id
fold_id
dataset
null_task
feature_set
K
model
balanced_accuracy
auc
f1
sensitivity
specificity
kernel_alignment
separability_index
K_RR
K_NN
K_RN
```

## 8.3 Column Definitions

| Column | Meaning |
|---|---|
| `balanced_accuracy` | Primary performance metric |
| `auc` | Area under ROC curve |
| `f1` | F1 score |
| `sensitivity` | True positive rate |
| `specificity` | True negative rate |
| `kernel_alignment` | Alignment between kernel matrix and target label matrix |
| `separability_index` | Within-class similarity minus between-class similarity |
| `K_RR` | Mean kernel similarity among real observations |
| `K_NN` | Mean kernel similarity among null-generated observations |
| `K_RN` | Mean kernel similarity between real and null-generated observations |

---

# 9. Statistical Result Table

## 9.1 Purpose

The statistical result table stores paired model comparisons.

Recommended filename:

```text
results/stats/main_comparisons.csv
```

## 9.2 Required Columns

```text
comparison_id
dataset
null_task
feature_set
K
metric
model_a
model_b
median_delta
mean_delta
ci_lower
ci_upper
effect_size_name
effect_size
p_raw
p_adjusted
correction_method
test_name
n_splits
interpretation_flag
```

## 9.3 Column Definitions

| Column | Meaning |
|---|---|
| `comparison_id` | Unique comparison identifier |
| `dataset` | Dataset name |
| `null_task` | Null task name |
| `feature_set` | Feature selection family |
| `K` | Number of selected features |
| `metric` | Metric being compared |
| `model_a` | Usually quantum model |
| `model_b` | Usually best classical model |
| `median_delta` | Median paired difference |
| `mean_delta` | Mean paired difference |
| `ci_lower` | Lower bootstrap confidence interval |
| `ci_upper` | Upper bootstrap confidence interval |
| `effect_size_name` | Name of effect size |
| `effect_size` | Effect size value |
| `p_raw` | Uncorrected p-value |
| `p_adjusted` | Multiple-comparison-corrected p-value |
| `correction_method` | Holm, BH-FDR, or none |
| `test_name` | Statistical test name |
| `n_splits` | Number of paired splits |
| `interpretation_flag` | beneficial, comparable_or_mixed, negative, or exploratory |

---

# 10. Kernel Matrix Files

## 10.1 Purpose

Kernel matrices may be saved when needed for debugging, figure generation, or reproducibility.

Recommended format:

```text
.npz
```

Recommended filename:

```text
results/primary/kernels/split001_qkernel_zz_raw_topk_K4_time_shift.npz
```

## 10.2 Required Contents

```text
K_train
K_test
train_obs_ids
test_obs_ids
model
feature_set
K
null_task
split_id
```

## 10.3 Integrity Rules

- `K_train` must be symmetric.
- `K_train` must have finite values.
- Observation ordering must be saved.
- Train/test IDs must match split files.

---

# 11. Figure Data Tables

Every manuscript figure should be generated from saved plot-data tables when possible.

Recommended files:

```text
figures/main/fig2_rq1_plotdata.csv
figures/main/fig3_rq2_plotdata.csv
figures/main/fig4_rq3_plotdata.csv
```

---

# 12. Table Data Files

Every manuscript table should be generated from saved table CSVs.

Recommended files:

```text
tables/main/table1_dataset_feature_null_summary.csv
tables/main/table2_main_statistical_comparison.csv
```

---

# 13. Naming Convention

Use consistent file naming:

```text
<dataset>_<object>_<feature_set>_K<K>_<null_task>.<ext>
```

Examples:

```text
primary_X_raw_topk_K4_time_shift.csv
primary_null_benchmark_raw_topk_K4_time_shift.csv
primary_metrics_raw_topk_K4_time_shift.csv
external_X_null_sensitive_K6_partner_shuffle.csv
```

---

# 14. Data Sharing Note

Raw EEG data should not be committed to GitHub unless explicitly permitted.

Allowed in GitHub:

- code
- configs
- documentation
- synthetic demo data
- anonymized feature-level matrices when permitted
- generated non-sensitive summary metrics

Not allowed unless explicitly cleared:

- raw EEG
- identifiable participant metadata
- restricted or proprietary data
- IRB-restricted files