#!/usr/bin/env python
"""
Generate simple pilot figures from saved metrics/statistical outputs.

Outputs:
- figures/main/fig2_demo_rq1_balanced_accuracy.png
- figures/main/fig3_demo_delta_ba.png

These are demo/pipeline-validation figures, not manuscript-final figures.
"""

from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def load_all_metrics(results_dir: Path, feature_set: str, null_task: str, k_values: list[int]):
    dfs = []
    for k in k_values:
        cpath = results_dir / f"classical_metrics_{feature_set}_K{k}_{null_task}.csv"
        qpath = results_dir / f"quantum_metrics_{feature_set}_K{k}_{null_task}.csv"

        if cpath.exists():
            dfs.append(pd.read_csv(cpath))
        if qpath.exists():
            dfs.append(pd.read_csv(qpath))

    if not dfs:
        raise FileNotFoundError("No metric files found.")

    return pd.concat(dfs, ignore_index=True)


def make_balanced_accuracy_figure(metrics: pd.DataFrame, outpath: Path):
    summary = (
        metrics.groupby(["K", "model"], as_index=False)["balanced_accuracy"]
        .mean()
        .sort_values(["K", "model"])
    )

    pivot = summary.pivot(index="K", columns="model", values="balanced_accuracy")

    ax = pivot.plot(kind="bar", figsize=(8, 4))
    ax.set_xlabel("Number of selected features (K)")
    ax.set_ylabel("Balanced accuracy")
    ax.set_title("Demo RQ1: Real–Null Separability by Kernel Model")
    ax.legend(title="Model", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)
    plt.close()


def make_delta_ba_figure(stats: pd.DataFrame, outpath: Path):
    df = stats[stats["metric"] == "balanced_accuracy"].copy()
    df = df.sort_values("K")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.errorbar(
        df["K"],
        df["median_delta"],
        yerr=[
            df["median_delta"] - df["ci_lower"],
            df["ci_upper"] - df["median_delta"],
        ],
        fmt="o",
        capsize=4,
    )
    ax.axhline(0, linestyle="--", linewidth=1)
    ax.set_xlabel("Number of selected features (K)")
    ax.set_ylabel("ΔBA: quantum ZZ − best classical")
    ax.set_title("Demo Statistical Comparison")
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results/primary")
    parser.add_argument("--stats-file", default="results/stats/main_comparisons.csv")
    parser.add_argument("--outdir", default="figures/main")
    parser.add_argument("--feature-set", default="raw_topk")
    parser.add_argument("--null-task", default="time_shift")
    parser.add_argument("--k-values", nargs="+", type=int, default=[4, 6, 8])
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    metrics = load_all_metrics(
        results_dir=results_dir,
        feature_set=args.feature_set,
        null_task=args.null_task,
        k_values=args.k_values,
    )

    fig2_path = outdir / "fig2_demo_rq1_balanced_accuracy.png"
    make_balanced_accuracy_figure(metrics, fig2_path)

    stats_path = Path(args.stats_file)
    if stats_path.exists():
        stats = pd.read_csv(stats_path)
        fig3_path = outdir / "fig3_demo_delta_ba.png"
        make_delta_ba_figure(stats, fig3_path)
    else:
        fig3_path = None

    print(f"PASS: saved {fig2_path}")
    if fig3_path:
        print(f"PASS: saved {fig3_path}")


if __name__ == "__main__":
    main()
