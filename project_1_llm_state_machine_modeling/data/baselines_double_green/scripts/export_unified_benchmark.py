#!/usr/bin/env python3
"""导出跨数据集统一格式 benchmark（generation + 可选人评 + 切片元信息）。

把 4 个数据集的 generation 主表（NL→STM）跟 820 行人评总表 join 到一起，
按 ``record_id`` 对齐，便于一次性跑 generation + judge benchmark。

输出字段：

- ``record_id``、``dataset``、``paper_slug``
- ``input_text``、``reference_text``、``reference_format``、``output_metamodel``
- ``human_review_count``：该 generation 样本对应的人评行数（可能 0 或多个）
- ``human_review_summaries``：list[dict]，每个含 score / unit / summary / target / component
- ``meta``：原 generation 行的额外字段

注意：

1. ``ttool_ai`` 的 generation 主表 = 15 model 变体；人评 116 行包含 case-level /
   split-level / overall 等多种 record_type，无法逐 variant 1:1 join，本脚本会
   把 case_name 作为弱关联，把所有该 case 的人评行汇总到 ``human_review_summaries``
   里
2. 同理，``light_control_nimbus`` 没有逐样本评分，``human_review_count`` 几乎全为 0
3. ``llms_emp`` 与 ``structure_event_driven`` 才能做 1:1 严格对齐

用法示例::

    # 完整统一表（所有 4 数据集 + 人评，默认输出到 stdout）
    python scripts/export_unified_benchmark.py

    # 只要 llms_emp + structure_event_driven（这俩才能严格 1:1 对齐人评）
    python scripts/export_unified_benchmark.py --strict-alignable-only

    # 持久化到本目录 datasets/ 子目录（git 可追溯位置；禁止写 /tmp 等仓库外路径）
    python scripts/export_unified_benchmark.py --drop-no-ref \\
        --format parquet -o datasets/unified.parquet
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import DATA_DIR, DATASETS, iter_dataset, write_records


# 把 dataset_id 映射到 baselines 的 paper_slug（与 SUMMARY 主表对应）
DATASET_TO_PAPER = {
    "llms_emp": "llms_emp",
    "ttool_ai": "ttool-ai",
    "light_control_nimbus": "requirements-capture-and-evaluation-in-nimbus-light-control",
    "structure_event_driven": "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models",
}


def build_human_review_index() -> dict[tuple[str, str], list[dict]]:
    """读 820 行人评总表，按 ``(paper_slug, alignment_key)`` 分组。

    alignment_key 选择规则（按数据集差异）：

    - llms_emp：``review_record_id`` —— 1:1 对齐 row_id
    - structure_event_driven：``case_id`` —— 1:1 对齐 case
    - ttool_ai：``case_name`` —— 1:N 弱对齐（case 下多个 variant 共享）
    - light_control_nimbus：``case_id``（实际 0 行有效）
    """
    df = pd.read_parquet(DATA_DIR / "cross_paper" / "human_review_records.parquet")
    index: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for _, row in df.iterrows():
        paper = row["paper_slug"]
        if paper == "llms_emp":
            key = str(row.get("review_record_id") or "")
        elif paper == "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models":
            key = str(row.get("case_id") or "")
        elif paper == "ttool-ai":
            key = str(row.get("case_name") or "")
        else:
            key = str(row.get("case_id") or "")
        if not key:
            continue
        index[(paper, key)].append(
            {
                "review_record_id": row.get("review_record_id"),
                "review_target": row.get("review_target"),
                "component": row.get("component"),
                "score": _safe_score(row.get("human_review_score")),
                "score_unit": row.get("human_review_score_unit"),
                "summary": row.get("human_review_summary"),
            }
        )
    return index


def _alignment_key(record: dict) -> str:
    """从 generation record.meta 抽出该数据集对应的 alignment_key。"""
    ds = record["dataset"]
    meta = record.get("meta", {})
    if ds == "llms_emp":
        return str(meta.get("row_id", ""))
    if ds == "structure_event_driven":
        return str(meta.get("case_id", ""))
    if ds == "ttool_ai":
        return str(meta.get("case_name", ""))
    if ds == "light_control_nimbus":
        return str(meta.get("case_id", ""))
    return ""


def _safe_score(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return str(v)


def build_records(strict_alignable_only: bool, drop_no_ref: bool) -> list[dict]:
    hr_index = build_human_review_index()
    out = []
    for r in iter_dataset("all"):
        ds = r["dataset"]
        if strict_alignable_only and ds in ("ttool_ai", "light_control_nimbus"):
            continue
        if drop_no_ref and not r.get("reference_text"):
            continue

        paper = DATASET_TO_PAPER[ds]
        align = _alignment_key(r)
        reviews = hr_index.get((paper, align), [])

        out.append(
            {
                "record_id": r["record_id"],
                "dataset": ds,
                "paper_slug": paper,
                "input_text": r["input_text"],
                "reference_text": r["reference_text"],
                "reference_format": r["reference_format"],
                "output_metamodel": r["output_metamodel"],
                "human_review_count": len(reviews),
                "human_review_summaries": reviews,
                "meta": r["meta"],
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--strict-alignable-only",
        action="store_true",
        help="仅保留能严格 1:1 对齐人评的 llms_emp + structure_event_driven",
    )
    ap.add_argument(
        "--drop-no-ref",
        action="store_true",
        help="丢弃 reference_text 为空的样本",
    )
    ap.add_argument("--output", "-o", default=None, help="输出文件路径，默认写到 stdout（仅 jsonl）")
    ap.add_argument("--format", choices=("jsonl", "parquet"), default="jsonl", help="输出格式")
    args = ap.parse_args()

    records = build_records(args.strict_alignable_only, args.drop_no_ref)
    write_records(records, args.output, args.format)


if __name__ == "__main__":
    main()
