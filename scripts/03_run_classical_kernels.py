#!/usr/bin/env python
"""
Run classical kernel SVM baselines on demo or project feature matrices.

Minimal pilot:
- input: data/demo/demo_primary_X_raw_topk_K4_time_shift.csv
- models: linear, polynomial, RBF SVM
- split: group-aware cross-validation
- outputs:
  - results/primary/rq1_classical_predictions.csv
  - results/primary/rq1_classical_metrics.csv
"""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd

from sklearn.metrics import balanced_accuracy_score, roc_auc_score, f1_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC


def get_feature_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c.startswith("f") and c[1:].isdigit()]


def safe_auc(y_true, y_score):
    try:
        return roc_auc_score(y_true, y_score)
    except ValueError:
        return np.nan


def run_model(df: pd.DataFrame, model_name: str, model, n_splits: int = 5):
    feature_cols = get_feature_columns(df)
    X = df[feature_cols].to_numpy(dtype=float)
    y = df["label"].to_numpy(dtype=int)
    groups = df["group_id"].astype(str).to_numpy()

    cv = GroupKFold(n_splits=n_splits)

    pred_rows = []
    metric_rows = []

    for fold_id, (train_idx, test_idx) in enumerate(cv.split(X, y, groups), start=1):
        pipe = Pipeline([
            ("scaler", MinMaxScaler(feature_range=(0, np.pi))),
            ("svc", model),
        ])

        pipe.fit(X[train_idx], y[train_idx])

        y_pred = pipe.predict(X[test_idx])

        if hasattr(pipe.named_steps["svc"], "decision_function"):
            y_score = pipe.decision_function(X[test_idx])
        else:
            y_score = pipe.predict_proba(X[test_idx])[:, 1]

        ba = balanced_accuracy_score(y[test_idx], y_pred)
        auc = safe_auc(y[test_idx], y_score)
        f1 = f1_score(y[test_idx], y_pred, zero_division=0)

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
            "kernel_alignment": np.nan,
            "separability_index": np.nan,
            "K_RR": np.nan,
            "K_NN": np.nan,
            "K_RN": np.nan,
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
    args = parser.parse_args()

    input_path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    models = {
        "linear_svm": SVC(kernel="linear", class_weight="balanced"),
        "poly_svm": SVC(kernel="poly", degree=2, gamma="scale", class_weight="balanced"),
        "rbf_svm": SVC(kernel="rbf", gamma="scale", class_weight="balanced"),
    }

    all_preds = []
    all_metrics = []

    for model_name, model in models.items():
        preds, metrics = run_model(df, model_name, model, n_splits=args.splits)
        all_preds.append(preds)
        all_metrics.append(metrics)

    pred_df = pd.concat(all_preds, ignore_index=True)
    metric_df = pd.concat(all_metrics, ignore_index=True)

    k = int(df["K"].iloc[0])
    null_task = df["null_task"].iloc[0]
    feature_set = df["feature_set"].iloc[0]

    pred_path = outdir / f"classical_predictions_{feature_set}_K{k}_{null_task}.csv"
    metric_path = outdir / f"classical_metrics_{feature_set}_K{k}_{null_task}.csv"

    pred_df.to_csv(pred_path, index=False)
    metric_df.to_csv(metric_path, index=False)

    print(f"PASS: saved {pred_path}")
    print(f"PASS: saved {metric_path}")
    print(metric_df.groupby("model")[["balanced_accuracy", "auc", "f1"]].mean().round(3))


if __name__ == "__main__":
    main()
