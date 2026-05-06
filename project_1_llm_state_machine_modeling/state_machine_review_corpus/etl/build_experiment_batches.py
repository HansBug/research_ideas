"""Sample baseline (820) and new protocol-FSM (153) parquets into matched
JSONL batches for the LLM reviewer experiment.

We deliberately keep the sample small (~30 rows per side) because each row
hits the LLM ≥1 time. Sampling is stratified by paper_slug × case_id so the
reviewer sees diversity rather than 30 copies of the same family.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import pandas as pd

CORPUS_ROOT = Path(__file__).resolve().parent.parent
ETL_OUT = CORPUS_ROOT / "etl" / "out"
BASELINE_DIR = (
    CORPUS_ROOT.parent
    / "discussions"
    / "2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets"
)

random.seed(20260506)


def _row_to_batch_item(row: pd.Series) -> dict:
    return {
        "item_id": str(row.get("review_record_id") or row.name),
        "prompt": (
            f"Evaluate the LLM-generated artifact against the human-annotated reference. "
            f"Score 0..1 on overall correctness. Paper={row.get('paper_slug')}, "
            f"target={row.get('review_target')}."
        ),
        "input_text": str(row.get("input_text") or "")[:6000],
        "pred_output": str(row.get("pred_output_text") or "")[:6000],
        "ref_output": str(row.get("ref_output_text") or "")[:6000],
        "metadata": {
            "paper_slug": str(row.get("paper_slug") or ""),
            "case_id": str(row.get("case_id") or ""),
            "diagram_type": str(row.get("diagram_type") or ""),
            "llm_name": str(row.get("llm_name") or row.get("strategy_name") or ""),
            "review_target": str(row.get("review_target") or ""),
            "record_type": str(row.get("record_type") or ""),
            "human_review_score": (
                float(row["human_review_score"])
                if row.get("human_review_score") is not None and not pd.isna(row.get("human_review_score"))
                else None
            ),
            "human_review_score_unit": str(row.get("human_review_score_unit") or ""),
        },
    }


def _stratified_sample(df: pd.DataFrame, group_cols: list[str], n_per_group: int, max_total: int) -> pd.DataFrame:
    """Take up to n_per_group rows per group; cap total at max_total."""
    if df.empty:
        return df
    samples = []
    for _, sub in df.groupby(group_cols, dropna=False):
        if len(sub) <= n_per_group:
            samples.append(sub)
        else:
            samples.append(sub.sample(n=n_per_group, random_state=20260506))
    sampled = pd.concat(samples, ignore_index=True)
    if len(sampled) > max_total:
        sampled = sampled.sample(n=max_total, random_state=20260506).reset_index(drop=True)
    return sampled


def build_baseline_sample() -> list[dict]:
    """24 rows from baseline 820, stratified across the 3 papers + main record types.

    Uses only rows where the reviewer can actually score (pred_output_text not null):
    - structure-event-driven: 8 component_level_review (all 8 — only 8 of 512 have pred_output)
    - llms_emp: 8 from 192 sample_level_review
    - ttool-ai: 8 from 84 summary-level rows (mix of summary_level_run_score / case_aggregate_stat)
    """
    df = pd.read_parquet(BASELINE_DIR / "baseline_double_green_human_review_records.parquet")

    # SED: only 8 rows have pred_output (none have ref_output) — take all 8
    sed = df[
        (df["paper_slug"] == "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models")
        & (df["record_type"] == "component_level_review")
        & df["pred_output_text"].notna() & df["input_text"].notna()
    ]
    llmsemp = df[
        (df["paper_slug"] == "llms_emp")
        & (df["record_type"] == "sample_level_review")
        & df["pred_output_text"].notna() & df["input_text"].notna() & df["ref_output_text"].notna()
    ]
    ttool = df[
        (df["paper_slug"] == "ttool-ai")
        & (df["record_type"].isin(["summary_level_run_score", "case_aggregate_stat"]))
        & df["pred_output_text"].notna()
    ]

    s_sed = sed.copy()  # take all 8
    s_llms = _stratified_sample(llmsemp, ["llm_name"], 2, 8)
    s_ttool = _stratified_sample(ttool, ["case_id"], 2, 8)

    combined = pd.concat([s_sed, s_llms, s_ttool], ignore_index=True)
    return [_row_to_batch_item(row) for _, row in combined.iterrows()]


def build_new_sample() -> list[dict]:
    """30 rows from new 153, stratified across PSMBench LLMs/protocols + RFCNLP."""
    df = pd.read_parquet(ETL_OUT / "protocol_fsm_human_review_records.parquet")

    psm = df[
        (df["paper_slug"] == "psmbench")
        & (df["record_type"] == "summary_level_run_score")
        & df["pred_output_text"].notna()
    ]
    rfc = df[
        (df["paper_slug"] == "rfcnlp")
        & (df["record_type"] == "summary_level_run_score")
        & df["pred_output_text"].notna()
    ]

    # Stratify PSMBench by LLM (9 LLMs × ~3 protocols each = ~27 rows)
    s_psm = _stratified_sample(psm, ["llm_name"], 3, 27)
    s_rfc = rfc.copy()  # only 4 rows total — take all

    combined = pd.concat([s_psm, s_rfc], ignore_index=True)
    return [_row_to_batch_item(row) for _, row in combined.iterrows()]


def main() -> None:
    baseline_items = build_baseline_sample()
    new_items = build_new_sample()

    print(f"baseline sample: {len(baseline_items)} rows")
    print(f"new sample: {len(new_items)} rows")

    baseline_path = ETL_OUT / "experiment_baseline_sample.jsonl"
    new_path = ETL_OUT / "experiment_new_sample.jsonl"

    with baseline_path.open("w", encoding="utf-8") as fh:
        for r in baseline_items:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with new_path.open("w", encoding="utf-8") as fh:
        for r in new_items:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Wrote: {baseline_path}")
    print(f"Wrote: {new_path}")

    # Quick stats per sample
    for label, items in [("baseline", baseline_items), ("new", new_items)]:
        scores = [it["metadata"]["human_review_score"] for it in items if it["metadata"]["human_review_score"] is not None]
        papers = sorted({it["metadata"]["paper_slug"] for it in items})
        print(f"  {label}: papers={papers}, score mean={sum(scores)/len(scores):.3f}, range=[{min(scores):.3f}, {max(scores):.3f}]")


if __name__ == "__main__":
    main()
