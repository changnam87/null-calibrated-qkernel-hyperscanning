#!/usr/bin/env python
"""
Generate standardized real-versus-null benchmark and group-aware split files.

Current role:
- Validate feature matrix schema.
- Create paired/null benchmark metadata.
- Create group-aware CV split table.
- Export benchmark and split CSVs.

This script does not generate null EEG signals. It formats already-created
real/null feature matrices into benchmark-ready files.
"""

from pathlib import Path
import argparse
import pandas as pd
from sklearn.model_selection import GroupKFold


REQUIRED_COLUMNS = [
    "obs_id",
    "dataset",
    "group_id",
    "session_id",
    "trial_id",
    "window_id",
    "dyad_id",
    "condition",
    "null_task",
    "label",
    "feature_set",
    "K",
]


def validate_input(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if set(df["label"].unique()) != {0, 1}:
        raise ValueError("Expected binary labels with both 0=null and 1=real.")

    if df["group_id"].isna().any():
        raise ValueError("group_id contains missing values.")

    if df["obs_id"].duplicated().any():
        raise ValueError("obs_id must be unique.")


def make_benchmark_table(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["label"] = pd.to_numeric(df["label"], errors="raise").astype(int)

    out = df[[
        "obs_id",
        "dataset",
        "null_task",
        "group_id",
        "session_id",
        "trial_id",
        "dyad_id",
        "label",
        "condition",
        "feature_set",
        "K",
    ]].copy()

    out["source_type"] = out["label"].apply(lambda x: "real" if int(x) == 1 else "null_generated")
    out["split_group"] = out["group_id"].astype(str)

    # Simple paired ID based on group/session/trial/dyad when available.
    out["pair_key"] = (
        out["group_id"].astype(str)
        + "_"
        + out["session_id"].astype(str)
        + "_"
        + out["trial_id"].astype(str)
        + "_"
        + out["dyad_id"].astype(str)
    )

    pair_map = {}
    for key, g in out.groupby("pair_key"):
        real_ids = g.loc[g["label"] == 1, "obs_id"].tolist()
        null_ids = g.loc[g["label"] == 0, "obs_id"].tolist()
        if real_ids and null_ids:
            for rid in real_ids:
                pair_map[rid] = null_ids[0]
            for nid in null_ids:
                pair_map[nid] = real_ids[0]

    out["paired_obs_id"] = out["obs_id"].map(pair_map).fillna("")

    ordered_cols = [
        "obs_id",
        "paired_obs_id",
        "dataset",
        "null_task",
        "group_id",
        "session_id",
        "trial_id",
        "dyad_id",
        "label",
        "source_type",
        "feature_set",
        "K",
        "split_group",
    ]

    return out[ordered_cols]


def make_group_splits(df: pd.DataFrame, n_splits: int) -> pd.DataFrame:
    groups = df["group_id"].astype(str)
    unique_groups = groups.nunique()

    if unique_groups < n_splits:
        raise ValueError(f"n_splits={n_splits} exceeds number of groups={unique_groups}.")

    X_dummy = df[["obs_id"]]
    y = df["label"]
    cv = GroupKFold(n_splits=n_splits)

    rows = []
    for fold_id, (train_idx, test_idx) in enumerate(cv.split(X_dummy, y, groups), start=1):
        split_id = f"fold{fold_id:02d}"

        for idx in train_idx:
            rows.append({
                "split_id": split_id,
                "repeat_id": 1,
                "fold_id": fold_id,
                "obs_id": df.iloc[idx]["obs_id"],
                "dataset": df.iloc[idx]["dataset"],
                "split": "train",
                "split_group": str(df.iloc[idx]["group_id"]),
                "null_task": df.iloc[idx]["null_task"],
                "feature_set": df.iloc[idx]["feature_set"],
                "K": int(df.iloc[idx]["K"]),
            })

        for idx in test_idx:
            rows.append({
                "split_id": split_id,
                "repeat_id": 1,
                "fold_id": fold_id,
                "obs_id": df.iloc[idx]["obs_id"],
                "dataset": df.iloc[idx]["dataset"],
                "split": "test",
                "split_group": str(df.iloc[idx]["group_id"]),
                "null_task": df.iloc[idx]["null_task"],
                "feature_set": df.iloc[idx]["feature_set"],
                "K": int(df.iloc[idx]["K"]),
            })

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input standardized feature matrix CSV.")
    parser.add_argument("--outdir", default="data/features", help="Output benchmark directory.")
    parser.add_argument("--split-outdir", default="data/splits", help="Output split directory.")
    parser.add_argument("--splits", type=int, default=2, help="Number of group-aware folds.")
    args = parser.parse_args()

    input_path = Path(args.input)
    outdir = Path(args.outdir)
    split_outdir = Path(args.split_outdir)

    outdir.mkdir(parents=True, exist_ok=True)
    split_outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    validate_input(df)

    dataset = df["dataset"].iloc[0]
    feature_set = df["feature_set"].iloc[0]
    k = int(df["K"].iloc[0])
    null_task = df["null_task"].iloc[0]

    benchmark = make_benchmark_table(df)
    splits = make_group_splits(df, n_splits=args.splits)

    benchmark_path = outdir / f"{dataset}_null_benchmark_{feature_set}_K{k}_{null_task}.csv"
    splits_path = split_outdir / f"{dataset}_group_cv_splits_{feature_set}_K{k}_{null_task}.csv"

    benchmark.to_csv(benchmark_path, index=False)
    splits.to_csv(splits_path, index=False)

    print(f"PASS: saved benchmark {benchmark_path}")
    print(f"PASS: saved splits {splits_path}")


if __name__ == "__main__":
    main()
