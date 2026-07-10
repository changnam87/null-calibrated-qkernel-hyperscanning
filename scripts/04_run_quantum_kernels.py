#!/usr/bin/env python
"""
Run quantum kernel SVM models on demo or project feature matrices.

Minimal pilot:
- input: data/demo/demo_primary_X_raw_topk_K4_time_shift.csv
- models: qkernel_zz, qkernel_pauli
- split: group-aware cross-validation
- outputs:
  - results/primary/quantum_predictions_<feature_set>_K<K>_<null_task>.csv
  - results/primary/quantum_metrics_<feature_set>_K<K>_<null_task>.csv
"""

from pathlib import Path
import argparse
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import numpy as np
import pandas as pd

from sklearn.metrics import balanced_accuracy_score, roc_auc_score, f1_score
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC

from qiskit.circuit.library import ZZFeatureMap, PauliFeatureMap
from qiskit_machine_learning.kernels import FidelityQuantumKernel


def get_feature_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c.startswith("f") and c[1:].isdigit()]


def safe_auc(y_true, y_score):
    try:
        return roc_auc_score(y_true, y_score)
    except ValueError:
        return np.nan


def kernel_alignment(K: np.ndarray, y: np.ndarray) -> float:
    """
    Simple centered-free kernel-target alignment.
    y should be binary {0,1}; convert to {-1,+1}.
    """
    yy = np.where(y == 1, 1.0, -1.0)
    Y = np.outer(yy, yy)
    denom = np.linalg.norm(K, "fro") * np.linalg.norm(Y, "fro")
    if denom == 0:
        return np.nan
    return float(np.sum(K * Y) / denom)


def separability_index(K: np.ndarray, y: np.ndarray):
    real_idx = y == 1
    null_idx = y == 0

    def mean_block(mask_a, mask_b):
        block = K[np.ix_(mask_a, mask_b)]
        if block.size == 0:
            return np.nan
        return float(np.mean(block))

    k_rr = mean_block(real_idx, real_idx)
    k_nn = mean_block(null_idx, null_idx)
    k_rn = mean_block(real_idx, null_idx)

    si = ((k_rr + k_nn) / 2.0) - k_rn
    return si, k_rr, k_nn, k_rn


def make_quantum_kernel(model_name: str, feature_dimension: int, reps: int, entanglement: str):
    if model_name == "qkernel_zz":
        feature_map = ZZFeatureMap(
            feature_dimension=feature_dimension,
            reps=reps,
            entanglement=entanglement,
        )
    elif model_name == "qkernel_pauli":
        feature_map = PauliFeatureMap(
            feature_dimension=feature_dimension,
            reps=reps,
            entanglement=entanglement,
            paulis=["Z", "ZZ"],
        )
    else:
        raise ValueError(f"Unknown quantum kernel model: {model_name}")

    return FidelityQuantumKernel(feature_map=feature_map)


def run_quantum_model(
    df: pd.DataFrame,
    model_name: str,
    reps: int = 1,
    entanglement: str = "linear",
    n_splits: int = 5,
):
    feature_cols = get_feature_columns(df)
    X = df[feature_cols].to_numpy(dtype=float)
    y = df["label"].to_numpy(dtype=int)
    groups = df["group_id"].astype(str).to_numpy()

    cv = GroupKFold(n_splits=n_splits)

    pred_rows = []
    metric_rows = []

    for fold_id, (train_idx, test_idx) in enumerate(cv.split(X, y, groups), start=1):
        scaler = MinMaxScaler(feature_range=(0, np.pi))
        X_train = scaler.fit_transform(X[train_idx])
        X_test = scaler.transform(X[test_idx])

        qkernel = make_quantum_kernel(
            model_name=model_name,
            feature_dimension=X_train.shape[1],
            reps=reps,
            entanglement=entanglement,
        )

        K_train = qkernel.evaluate(x_vec=X_train)
        K_test = qkernel.evaluate(x_vec=X_test, y_vec=X_train)

        clf = SVC(kernel="precomputed", class_weight="balanced")
        clf.fit(K_train, y[train_idx])

        y_pred = clf.predict(K_test)
        y_score = clf.decision_function(K_test)

        ba = balanced_accuracy_score(y[test_idx], y_pred)
        auc = safe_auc(y[test_idx], y_score)
        f1 = f1_score(y[test_idx], y_pred, zero_division=0)

        align = kernel_alignment(K_train, y[train_idx])
        si, k_rr, k_nn, k_rn = separability_index(K_train, y[train_idx])

        split_id = f"fold{fold_id:02d}"

        metric_rows.append({
            "split_id": split_id,
            "repeat_id": 1,
            "fold_id": fold_id,
            "dataset": df["dataset"].iloc[0],
            "null_task": df["null_task"].iloc[0],
            "feature_set": df["feature_set"].iloc[0],
            "K": int(df["K"].iloc[0]),
            "model": model_name,
            "balanced_accuracy": ba,
            "auc": auc,
            "f1": f1,
            "sensitivity": np.nan,
            "specificity": np.nan,
            "kernel_alignment": align,
            "separability_index": si,
            "K_RR": k_rr,
            "K_NN": k_nn,
            "K_RN": k_rn,
        })

        for obs_i, true_i, pred_i, score_i in zip(df.iloc[test_idx]["obs_id"], y[test_idx], y_pred, y_score):
            pred_rows.append({
                "split_id": split_id,
                "repeat_id": 1,
                "fold_id": fold_id,
                "dataset": df["dataset"].iloc[0],
                "null_task": df["null_task"].iloc[0],
                "feature_set": df["feature_set"].iloc[0],
                "K": int(df["K"].iloc[0]),
                "model": model_name,
                "obs_id": obs_i,
                "y_true": int(true_i),
                "y_pred": int(pred_i),
                "y_score": float(score_i),
            })

    return pd.DataFrame(pred_rows), pd.DataFrame(metric_rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="data/demo/demo_primary_X_raw_topk_K4_time_shift.csv",
        help="Path to feature matrix CSV.",
    )
    parser.add_argument(
        "--outdir",
        default="results/primary",
        help="Output directory.",
    )
    parser.add_argument(
        "--splits",
        type=int,
        default=5,
        help="Number of GroupKFold splits.",
    )
    parser.add_argument(
        "--reps",
        type=int,
        default=1,
        help="Quantum feature map repetitions.",
    )
    parser.add_argument(
        "--entanglement",
        default="linear",
        choices=["linear", "full"],
        help="Entanglement pattern.",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=["qkernel_zz", "qkernel_pauli"],
        choices=["qkernel_zz", "qkernel_pauli"],
        help="Quantum kernel models to run.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    all_preds = []
    all_metrics = []

    for model_name in args.models:
        preds, metrics = run_quantum_model(
            df,
            model_name=model_name,
            reps=args.reps,
            entanglement=args.entanglement,
            n_splits=args.splits,
        )
        all_preds.append(preds)
        all_metrics.append(metrics)

    pred_df = pd.concat(all_preds, ignore_index=True)
    metric_df = pd.concat(all_metrics, ignore_index=True)

    k = int(df["K"].iloc[0])
    null_task = df["null_task"].iloc[0]
    feature_set = df["feature_set"].iloc[0]

    pred_path = outdir / f"quantum_predictions_{feature_set}_K{k}_{null_task}.csv"
    metric_path = outdir / f"quantum_metrics_{feature_set}_K{k}_{null_task}.csv"

    pred_df.to_csv(pred_path, index=False)
    metric_df.to_csv(metric_path, index=False)

    print(f"PASS: saved {pred_path}")
    print(f"PASS: saved {metric_path}")
    print(metric_df.groupby("model")[["balanced_accuracy", "auc", "f1", "kernel_alignment", "separability_index"]].mean().round(3))


if __name__ == "__main__":
    main()
