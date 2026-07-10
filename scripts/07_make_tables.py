#!/usr/bin/env python
"""
Generate demo table CSV files for manuscript table pipeline.

Outputs:
- tables/main/table1_dataset_feature_null_summary.csv
- tables/main/table2_main_statistical_comparison.csv

These are demo/pipeline-validation tables, not final manuscript tables.
"""

from pathlib import Path
import argparse
import pandas as pd


def make_table1(outpath: Path):
    rows = [
        {
            "Component": "Dataset",
            "Primary triadic dataset": "Triadic Prisoner's Dilemma EEG hyperscanning",
            "External dyadic dataset": "Dyadic collaboration/competition EEG hyperscanning",
        },
        {
            "Component": "Interaction structure",
            "Primary triadic dataset": "11 triads",
            "External dyadic dataset": "16 dyads",
        },
        {
            "Component": "Synchrony metrics",
            "Primary triadic dataset": "PLV, coherence, combined contrast",
            "External dyadic dataset": "PLV, coherence, combined contrast",
        },
        {
            "Component": "Unit definition",
            "Primary triadic dataset": "window × band × dyad × edge",
            "External dyadic dataset": "task/window × band × dyad × edge",
        },
        {
            "Component": "Null models",
            "Primary triadic dataset": "label permutation; time shift; partner shuffle",
            "External dyadic dataset": "time shift; partner shuffle",
        },
        {
            "Component": "Feature sets",
            "Primary triadic dataset": "raw top-K; null-sensitive; evidence-aware",
            "External dyadic dataset": "matched raw top-K; null-sensitive where feasible",
        },
        {
            "Component": "Main validation role",
            "Primary triadic dataset": "RQ1–RQ3 primary analysis",
            "External dyadic dataset": "RQ3 framework-level transferability",
        },
    ]

    pd.DataFrame(rows).to_csv(outpath, index=False)


def make_table2(stats_path: Path, outpath: Path):
    if not stats_path.exists():
        raise FileNotFoundError(f"Missing statistics file: {stats_path}")

    stats = pd.read_csv(stats_path)

    keep_cols = [
        "dataset",
        "null_task",
        "feature_set",
        "K",
        "metric",
        "model_a",
        "model_b",
        "median_delta",
        "ci_lower",
        "ci_upper",
        "effect_size",
        "p_adjusted",
        "interpretation_flag",
    ]

    table = stats[keep_cols].copy()

    # Keep the demo table compact: primary metric first.
    table["metric_order"] = table["metric"].map({
        "balanced_accuracy": 0,
        "auc": 1,
        "f1": 2,
    }).fillna(99)

    table = table.sort_values(["metric_order", "K"]).drop(columns=["metric_order"])

    table.to_csv(outpath, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stats-file", default="results/stats/main_comparisons.csv")
    parser.add_argument("--outdir", default="tables/main")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    table1_path = outdir / "table1_dataset_feature_null_summary.csv"
    table2_path = outdir / "table2_main_statistical_comparison.csv"

    make_table1(table1_path)
    make_table2(Path(args.stats_file), table2_path)

    print(f"PASS: saved {table1_path}")
    print(f"PASS: saved {table2_path}")


if __name__ == "__main__":
    main()
