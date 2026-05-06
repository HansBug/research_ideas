"""Convert protocol_fsm parquet rows into the JSONL batch input format
expected by `reproduction.expert_review.batch.load_batch_items`.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

CORPUS_ROOT = Path(__file__).resolve().parent.parent
ETL_OUT = CORPUS_ROOT / "etl" / "out"


def df_to_batch_rows(df: pd.DataFrame) -> list[dict]:
    rows: list[dict] = []
    for _, row in df.iterrows():
        item = {
            "item_id": row["review_record_id"],
            "prompt": (
                f"Evaluate the LLM-extracted protocol state machine against the human-annotated "
                f"reference for the {row['case_name']} protocol. Score 0..1 on overall correctness."
            ),
            "input_text": str(row["input_text"] or ""),
            "pred_output": str(row["pred_output_text"] or ""),
            "ref_output": str(row["ref_output_text"] or ""),
            "metadata": {
                "paper_slug": row["paper_slug"],
                "case_id": row["case_id"],
                "llm_name": row.get("llm_name") or row.get("strategy_name"),
                "diagram_type": row["diagram_type"],
                "review_target": row["review_target"],
                "human_review_score": (
                    float(row["human_review_score"])
                    if row["human_review_score"] is not None and not pd.isna(row["human_review_score"])
                    else None
                ),
                "human_review_score_unit": row.get("human_review_score_unit"),
            },
        }
        rows.append(item)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-slug", action="append", default=None,
                        help="Filter by paper_slug (repeat). Default: all.")
    parser.add_argument("--case-id", action="append", default=None,
                        help="Filter by case_id (repeat). Default: all.")
    parser.add_argument("--record-type", default="summary_level_run_score",
                        help="record_type to include (default: summary_level_run_score)")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_parquet(ETL_OUT / "protocol_fsm_human_review_records.parquet")
    df = df[df["record_type"] == args.record_type]
    if args.paper_slug:
        df = df[df["paper_slug"].isin(args.paper_slug)]
    if args.case_id:
        df = df[df["case_id"].isin(args.case_id)]
    if args.limit:
        df = df.head(args.limit)

    rows = df_to_batch_rows(df)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows)} batch items → {args.output}")


if __name__ == "__main__":
    main()
