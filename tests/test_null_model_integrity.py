from pathlib import Path
import pandas as pd


def test_null_benchmark_files_exist():
    for k in [4, 6, 8]:
        path = Path(f"data/features/demo_primary_null_benchmark_raw_topk_K{k}_time_shift.csv")
        assert path.exists(), f"Missing {path}"


def test_null_benchmark_labels_and_sources():
    for k in [4, 6, 8]:
        path = Path(f"data/features/demo_primary_null_benchmark_raw_topk_K{k}_time_shift.csv")
        df = pd.read_csv(path)

        assert set(df["label"].unique()) == {0, 1}
        assert set(df["source_type"].unique()) == {"real", "null_generated"}
        assert df["obs_id"].is_unique
        assert not df["split_group"].isna().any()
