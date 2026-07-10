#!/usr/bin/env bash
set -e

echo "== Step 0: Generate demo data =="
python scripts/00_generate_demo_data.py

echo "== Step 1: Build standardized feature files =="
python scripts/01_build_features.py --input data/demo_tiny/demo_primary_X_raw_topk_K4_time_shift.csv --dataset-name demo_primary
python scripts/01_build_features.py --input data/demo_tiny/demo_primary_X_raw_topk_K6_time_shift.csv --dataset-name demo_primary
python scripts/01_build_features.py --input data/demo_tiny/demo_primary_X_raw_topk_K8_time_shift.csv --dataset-name demo_primary

echo "== Step 2: Generate null benchmarks and splits =="
python scripts/02_generate_null_benchmarks.py --input data/features/demo_primary_X_raw_topk_K4_time_shift.csv --splits 2
python scripts/02_generate_null_benchmarks.py --input data/features/demo_primary_X_raw_topk_K6_time_shift.csv --splits 2
python scripts/02_generate_null_benchmarks.py --input data/features/demo_primary_X_raw_topk_K8_time_shift.csv --splits 2

echo "== Step 3: Run classical kernels =="
python scripts/03_run_classical_kernels.py --input data/demo_tiny/demo_primary_X_raw_topk_K4_time_shift.csv --splits 2
python scripts/03_run_classical_kernels.py --input data/demo_tiny/demo_primary_X_raw_topk_K6_time_shift.csv --splits 2
python scripts/03_run_classical_kernels.py --input data/demo_tiny/demo_primary_X_raw_topk_K8_time_shift.csv --splits 2

echo "== Step 4: Run quantum kernels =="
python scripts/04_run_quantum_kernels.py --input data/demo_tiny/demo_primary_X_raw_topk_K4_time_shift.csv --splits 2 --models qkernel_zz
python scripts/04_run_quantum_kernels.py --input data/demo_tiny/demo_primary_X_raw_topk_K6_time_shift.csv --splits 2 --models qkernel_zz
python scripts/04_run_quantum_kernels.py --input data/demo_tiny/demo_primary_X_raw_topk_K8_time_shift.csv --splits 2 --models qkernel_zz

echo "== Step 5: Run statistics =="
python scripts/05_run_statistics.py --k-values 4 6 8 --quantum-models qkernel_zz --metrics balanced_accuracy auc f1

echo "== Step 6: Make figures =="
python scripts/06_make_figures.py

echo "== Step 7: Make tables =="
python scripts/07_make_tables.py

echo "PASS: Full demo pipeline completed."
