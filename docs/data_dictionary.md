# Data Dictionary

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
