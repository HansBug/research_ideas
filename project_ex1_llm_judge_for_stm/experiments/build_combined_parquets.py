"""Combine baseline 820-row parquets with the 153-row protocol-FSM ETL output.

Outputs three sibling parquet files:
    combined_human_review_records.parquet      (820 + 153 = 973 rows)
    combined_human_review_protocols.parquet    (4 + 3 = 7 rows)
    combined_human_review_availability.parquet (4 + 3 = 7 rows)

These keep the same 34/15/9-column schemas as the baseline parquets so the
existing reviewer benchmark loader can consume them without modification.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

CORPUS_ROOT = Path(__file__).resolve().parent.parent
ETL_OUT = CORPUS_ROOT / "etl" / "out"
BASELINE_DIR = (
    CORPUS_ROOT.parent
    / "discussions"
    / "2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets"
)


def _safe_concat(base: pd.DataFrame, extra: pd.DataFrame) -> pd.DataFrame:
    base_cols = list(base.columns)
    aligned = extra.reindex(columns=base_cols)
    return pd.concat([base, aligned], ignore_index=True)


def main() -> None:
    pairs = [
        ("baseline_double_green_human_review_records.parquet",
         "protocol_fsm_human_review_records.parquet",
         "combined_human_review_records.parquet"),
        ("baseline_double_green_human_review_protocols.parquet",
         "protocol_fsm_human_review_protocols.parquet",
         "combined_human_review_protocols.parquet"),
        ("baseline_double_green_human_review_availability.parquet",
         "protocol_fsm_human_review_availability.parquet",
         "combined_human_review_availability.parquet"),
    ]

    for base_name, extra_name, out_name in pairs:
        base = pd.read_parquet(BASELINE_DIR / base_name)
        extra = pd.read_parquet(ETL_OUT / extra_name)
        combined = _safe_concat(base, extra)
        out_path = ETL_OUT / out_name
        combined.to_parquet(out_path, index=False)
        print(f"{out_name}: base={len(base)} + extra={len(extra)} → {len(combined)} rows")
        if "paper_slug" in combined.columns:
            print(combined["paper_slug"].value_counts().to_string())
            print()


if __name__ == "__main__":
    main()
