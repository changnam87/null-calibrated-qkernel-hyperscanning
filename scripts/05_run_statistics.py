#!/usr/bin/env python
"""
Create paired statistical comparisons between quantum and classical kernels.

Minimal pilot expectation:
- classical metrics:
  results/primary/classical_metrics_raw_topk_K4_time_shift.csv
- quantum metrics:
  results/primary/quantum_metrics_raw_topk_K4_time_shift.csv

Output:
- results/stats/main_comparisons.csv
"""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon


def bootstrap_ci(x: np.ndarray, n_boot: int = 5000, seed: int = 20260710):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]

    if len(x) == 0:
        return np.nan, np.nan

    boots = []
    for _ in range(n_boot):
        sample = rng.choice(x, size=len(x), replace=True)
        boots.append(np.median(sample))

    return float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


def rank_biserial_from_wilcoxon(x: np.ndarray):
    """
    Approximate rank-biserial correlation for paired differences.
    Positive means differences tend to be positive.
    """
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    x = x[x != 0]

    if len(x) == 0:
        return np.nan

    abs_x = np.abs(x)
    ranks = pd.Series(abs_x).rank(method="average").to_numpy()
    r_pos = ranks[x > 0].sum()
    r_neg = ranks[x < 0].sum()
    denom = len(x) * (len(x) + 1) / 2

    if denom == 0:
        return np.nan

    return float((r_pos - r_neg) / denom)


def holm_adjust(p_values):
    """
    Holm-Bonferroni adjustment.
    Returns adjusted p-values in original order.
    """
    p_values = np.asarray(p_values, dtype=float)
    n = len(p_values)
    order = np.argsort(p_values)
    adjusted = np.empty(n, dtype=float)

    running_max = 0.0
    for rank, idx in enumerate(order):
        adj = (n - rank) * p_values[idx]
        running_max = max(running_max, adj)
        adjusted[idx] = min(running_max, 1.0)

    return adjusted


def load_metrics(results_dir: Path, feature_set: str, k: int, null_task: str):
    classical_path = results_dir / f"classical_metrics_{feature_set}_K{k}_{null_task}.csv"
    quantum_path = results_dir / f"quantum_metrics_{feature_set}_K{k}_{null_task}.csv"

    if not classical_path.exists():
        raise FileNotFoundError(f"Missing classical metrics: {classical_path}")

    if not quantum_path.exists():
        raise FileNotFoundError(f"Missing quantum metrics: {quantum_path}")

    classical = pd.read_csv(classical_path)
    quantum = pd.read_csv(quantum_path)

    return classical, quantum


def best_classical_by_split(classical: pd.DataFrame, metric: str):
    idx = classical.groupby("split_id")[metric].idxmax()
    best = classical.loc[idx].copy()
    best["model"] = "best_classical"
    return best


def compare_model_to_best_classical(
    classical: pd.DataFrame,
    quantum: pd.DataFrame,
    quantum_model: str,
    metric: str,
    n_boot: int,
):
    best = best_classical_by_split(classical, metric)
    q = quantum[quantum["model"] == quantum_model].copy()

    merged = q.merge(
        best[["split_id", metric]],
        on="split_id",
        how="inner",
        suffixes=("_quantum", "_best_classical"),
    )

    if merged.empty:
        raise ValueError(f"No overlapping split IDs for {quantum_model} and best classical.")

    delta = merged[f"{metric}_quantum"].to_numpy() - merged[f"{metric}_best_classical"].to_numpy()

    if np.all(delta == 0):
        p_raw = 1.0
    else:
        try:
            p_raw = float(wilcoxon(delta, zero_method="wilcox", alternative="two-sided").pvalue)
        except ValueError:
            p_raw = np.nan

    ci_lower, ci_upper = bootstrap_ci(delta, n_boot=n_boot)
    effect = rank_biserial_from_wilcoxon(delta)

    template = q.iloc[0].to_dict()

    return {
        "comparison_id": f"{quantum_model}_vs_best_classical_{metric}",
        "dataset": template.get("dataset"),
        "null_task": template.get("null_task"),
        "feature_set": template.get("feature_set"),
        "K": int(template.get("K")),
        "metric": metric,
        "model_a": quantum_model,
        "model_b": "best_classical",
        "median_delta": float(np.nanmedian(delta)),
        "mean_delta": float(np.nanmean(delta)),
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "effect_size_name": "rank_biserial",
        "effect_size": effect,
        "p_raw": p_raw,
        "p_adjusted": np.nan,
        "correction_method": "Holm",
        "test_name": "Wilcoxon signed-rank",
        "n_splits": int(len(delta)),
        "interpretation_flag": "pending",
    }


def assign_interpretation(row):
    med = row["median_delta"]
    lo = row["ci_lower"]
    hi = row["ci_upper"]

    negligible = 0.01

    if med > 0 and lo > negligible:
        return "beneficial"
    if med < 0 and hi < -negligible:
        return "negative"
    return "comparable_or_mixed"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results/primary")
    parser.add_argument("--outdir", default="results/stats")
    parser.add_argument("--feature-set", default="raw_topk")
    parser.add_argument("--null-task", default="time_shift")
    parser.add_argument("--k-values", nargs="+", type=int, default=[4, 6, 8])
    parser.add_argument("--metrics", nargs="+", default=["balanced_accuracy", "auc", "f1"])
    parser.add_argument("--quantum-models", nargs="+", default=["qkernel_zz", "qkernel_pauli"])
    parser.add_argument("--n-boot", type=int, default=5000)
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []

    for k in args.k_values:
        classical, quantum = load_metrics(results_dir, args.feature_set, k, args.null_task)

        for metric in args.metrics:
            if metric not in classical.columns or metric not in quantum.columns:
                continue

            for qmodel in args.quantum_models:
                if qmodel not in set(quantum["model"]):
                    continue

                rows.append(
                    compare_model_to_best_classical(
                        classical=classical,
                        quantum=quantum,
                        quantum_model=qmodel,
                        metric=metric,
                        n_boot=args.n_boot,
                    )
                )

    stats = pd.DataFrame(rows)

    if stats.empty:
        raise RuntimeError("No statistical comparisons were created.")

    # Holm correction within each metric family.
    adjusted_rows = []
    for metric, group in stats.groupby("metric", sort=False):
        g = group.copy()
        g["p_adjusted"] = holm_adjust(g["p_raw"].fillna(1.0).to_numpy())
        adjusted_rows.append(g)

    stats = pd.concat(adjusted_rows, ignore_index=True)
    stats["interpretation_flag"] = stats.apply(assign_interpretation, axis=1)

    out_path = outdir / "main_comparisons.csv"
    stats.to_csv(out_path, index=False)

    print(f"PASS: saved {out_path}")
    print(stats[[
        "K", "metric", "model_a", "model_b",
        "median_delta", "ci_lower", "ci_upper",
        "effect_size", "p_adjusted", "interpretation_flag"
    ]].round(4))


if __name__ == "__main__":
    main()
