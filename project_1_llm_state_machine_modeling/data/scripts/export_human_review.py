#!/usr/bin/env python3
"""导出人评对齐 benchmark（含 input + ref + pred + score，跨论文统一字段）。

适用场景：训练 / 评估 LLM-as-judge / reviewer / structured critique 模型。

数据源：``baseline_double_green_human_review_records.parquet``（820 行 × 34 列），
该总表已经把 4 篇论文的人评字段统一到同一 schema。

输出字段（按需子集）：

- ``record_id``：``<paper_slug>::<review_record_id>``
- ``paper_slug``
- ``record_type``、``review_target``、``component``（可用于切片）
- ``input_text``、``ref_output_text``、``pred_output_text``
- ``ref_output_format``、``pred_output_format``
- ``human_review_score``、``human_review_score_unit``
- ``human_review_summary``、``human_review_details_json``、``review_rubric_text``
- ``paper_method_verbatim_excerpt``（论文原文摘录）

用法示例::

    # 全部 820 行（默认输出到 stdout）
    python scripts/export_human_review.py

    # 只看 llms_emp 的人评
    python scripts/export_human_review.py --paper llms_emp

    # 只保留 input + ref + pred 三者都非空的（可直接训 reviewer）
    python scripts/export_human_review.py --require-triplet

    # 持久化到本目录 datasets/ 子目录（git 可追溯位置；禁止写 /tmp 等仓库外路径）
    python scripts/export_human_review.py --format parquet -o datasets/hr.parquet
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import DATA_DIR, write_records


PAPER_CHOICES = (
    "llms_emp",
    "ttool-ai",
    "requirements-capture-and-evaluation-in-nimbus-light-control",
    "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models",
)


def build_records(paper: str | None, require_triplet: bool) -> list[dict]:
    df = pd.read_parquet(DATA_DIR / "human_review_records.parquet")
    if paper:
        df = df[df["paper_slug"] == paper]
    if require_triplet:
        df = df[df["input_text"].fillna("").str.len().gt(0)
                & df["ref_output_text"].fillna("").str.len().gt(0)
                & df["pred_output_text"].fillna("").str.len().gt(0)]

    out = []
    for _, row in df.iterrows():
        rid = row.get("review_record_id") or row.get("case_id") or ""
        out.append(
            {
                "record_id": f"{row['paper_slug']}::{rid}",
                "paper_slug": row["paper_slug"],
                "record_source": row.get("record_source"),
                "record_type": row.get("record_type"),
                "review_target": row.get("review_target"),
                "component": row.get("component"),
                "input_text": row.get("input_text"),
                "ref_output_text": row.get("ref_output_text"),
                "ref_output_format": row.get("ref_output_format"),
                "pred_output_text": row.get("pred_output_text"),
                "pred_output_format": row.get("pred_output_format"),
                "human_review_score": _coerce_score(row.get("human_review_score")),
                "human_review_score_unit": row.get("human_review_score_unit"),
                "human_review_summary": row.get("human_review_summary"),
                "human_review_details_json": row.get("human_review_details_json"),
                "review_rubric_text": row.get("review_rubric_text"),
                "paper_method_verbatim_excerpt": row.get("paper_method_verbatim_excerpt"),
            }
        )
    return out


def _coerce_score(v):
    """评分字段在 4 个数据集口径不同；尽力转 float，失败保持原文。"""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return str(v)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--paper", choices=PAPER_CHOICES, default=None, help="按 paper_slug 过滤；默认 4 篇全要")
    ap.add_argument(
        "--require-triplet",
        action="store_true",
        help="只保留 input/ref/pred 三者都非空的记录（适合训 reviewer）",
    )
    ap.add_argument("--output", "-o", default=None, help="输出文件路径，默认写到 stdout（仅 jsonl）")
    ap.add_argument("--format", choices=("jsonl", "parquet"), default="jsonl", help="输出格式")
    args = ap.parse_args()

    records = build_records(args.paper, args.require_triplet)
    write_records(records, args.output, args.format)


if __name__ == "__main__":
    main()
