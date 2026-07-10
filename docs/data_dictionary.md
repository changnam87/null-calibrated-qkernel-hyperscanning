# Data Dictionary

## Core Files

- synchrony unit table
- observation-level feature matrix
- feature map table
- null benchmark table
- cross-validation split table
- prediction output table
- metric output table
- statistical result table

## Observation-Level Feature Matrix Columns

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

## Prediction Output Columns

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

## Metric Output Columns

- split_id
- dataset
- null_task
- feature_set
- K
- model
- balanced_accuracy
- auc
- f1
- kernel_alignment
- separability_index
