#!/usr/bin/env python
"""
Generate synthetic demo feature matrices for minimal pipeline testing.

This is not real EEG data. It only follows the project schema so that
classical/quantum kernel scripts can be tested end-to-end.
"""

from pathlib import Path
import numpy as np
import pandas as pd


def make_demo_dataset(k: int, n_groups: int = 10, obs_per_group: int = 12, seed: int = 20260710):
    rng = np.random.default_rng(seed + k)

    rows = []
    for group in range(n_groups):
        group_shift = rng.normal(0, 0.15, size=k)

        for i in range(obs_per_group):
            # Real observation
            x_real = rng.normal(0.60, 0.18, size=k) + group_shift
            rows.append({
                "obs_id": f"G{group:02d}_R{i:03d}",
                "dataset": "demo_primary",
                "group_id": f"G{group:02d}",
                "session_id": "S01",
                "trial_id": i,
                "window_id": "feedback",
                "dyad_id": "pair23",
                "condition": "real",
                "null_task": "time_shift",
                "label": 1,
                "feature_set": "raw_topk",
                "K": k,
                **{f"f{j+1:03d}": x_real[j] for j in range(k)}
            })

            # Null observation
            x_null = rng.normal(0.45, 0.18, size=k) + 0.6 * group_shift
            rows.append({
                "obs_id": f"G{group:02d}_N{i:03d}",
                "dataset": "demo_primary",
                "group_id": f"G{group:02d}",
                "session_id": "S01",
                "trial_id": i,
                "window_id": "feedback",
                "dyad_id": "pair23",
                "condition": "null",
                "null_task": "time_shift",
                "label": 0,
                "feature_set": "raw_topk",
                "K": k,
                **{f"f{j+1:03d}": x_null[j] for j in range(k)}
            })

    return pd.DataFrame(rows)


def make_feature_map(k: int):
    rows = []
    for j in range(k):
        rows.append({
            "feature_name": f"f{j+1:03d}",
            "feature_index": j + 1,
            "unit_id": f"DEMO_U{j+1:03d}",
            "dataset": "demo_primary",
            "window": "feedback",
            "band": ["delta", "theta", "alpha", "beta", "gamma"][j % 5],
            "dyad_label": "pair23",
            "edge_id": f"E{j+1:03d}",
            "channel_i": f"P2_CH{j+1}",
            "channel_j": f"P3_CH{j+1}",
            "metric": "combined",
            "selection_rule": "raw_topk",
            "selection_rank": j + 1,
            "selection_score": 1.0 / (j + 1),
        })
    return pd.DataFrame(rows)


def main():
    out_dir = Path("data/demo")
    out_dir.mkdir(parents=True, exist_ok=True)

    for k in [4, 6, 8]:
        df = make_demo_dataset(k)
        df.to_csv(out_dir / f"demo_primary_X_raw_topk_K{k}_time_shift.csv", index=False)

        fmap = make_feature_map(k)
        fmap.to_csv(out_dir / f"demo_primary_feature_map_raw_topk_K{k}.csv", index=False)

    print("PASS: demo data generated in data/demo/")


if __name__ == "__main__":
    main()
