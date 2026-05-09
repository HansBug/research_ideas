#!/usr/bin/env python3
"""导出 NL→STM benchmark（input + reference 对齐，跨数据集统一格式）。

适用场景：state-machine 生成模型的 standard generation benchmark。

输出字段（一行一个 record）：

- ``record_id``
- ``dataset``
- ``input_text``
- ``reference_text``
- ``reference_format``：``plantuml`` / ``avatar_xml`` / ``rsmle`` / ``umple``
- ``output_metamodel``
- ``meta``（dict；含状态/迁移计数等切片字段）

注意：

1. 默认仅产出 reference_text 非空的 record；用 ``--include-no-ref`` 关闭过滤
2. ``ttool_ai`` 的 reference 是完整 AVATAR XML（不是手抄状态机文本），下游若要做
   逐状态评测，再从 ``ttool_ai_states.parquet`` / ``ttool_ai_transitions.parquet``
   读结构化数据
3. ``light_control_nimbus`` 的 reference 是片段化的 RSML-e 状态/规则摘录，**不是**
   完整 RSML-e 程序；详见 [`../README.md`](../README.md) §3.4

用法示例::

    python scripts/export_nl_to_stm.py --dataset llms_emp
    python scripts/export_nl_to_stm.py --dataset all --output /tmp/nl2stm.jsonl
    python scripts/export_nl_to_stm.py --dataset structure_event_driven \\
        --include-non-eval-cases  # 把非 paper 评测 case 也带上
    python scripts/export_nl_to_stm.py --dataset all --format parquet \\
        --output /tmp/nl2stm.parquet
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import DATASETS, iter_dataset, write_records


def build_records(
    dataset: str,
    diagram_type: str | None,
    include_no_ref: bool,
    include_non_eval_cases: bool,
) -> list[dict]:
    kwargs: dict = {}
    if dataset in ("llms_emp", "all"):
        kwargs["diagram_filter"] = diagram_type
    if dataset in ("structure_event_driven", "all"):
        kwargs["only_paper_eval"] = not include_non_eval_cases

    out = []
    for r in iter_dataset(dataset, **kwargs):
        if not include_no_ref and not r.get("reference_text"):
            continue
        out.append(
            {
                "record_id": r["record_id"],
                "dataset": r["dataset"],
                "input_text": r["input_text"],
                "reference_text": r["reference_text"],
                "reference_format": r["reference_format"],
                "output_metamodel": r["output_metamodel"],
                "meta": r["meta"],
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--dataset",
        choices=("all", *DATASETS),
        default="all",
    )
    ap.add_argument(
        "--diagram-type",
        choices=("stm", "act", "sd"),
        default=None,
        help="仅 llms_emp 有效；过滤为指定 diagram 类型（默认全部）",
    )
    ap.add_argument(
        "--include-no-ref",
        action="store_true",
        help="保留 reference_text 为空的样本（默认丢弃）",
    )
    ap.add_argument(
        "--include-non-eval-cases",
        action="store_true",
        help="仅 structure_event_driven 有效；保留非 paper 评测 case（默认仅 paper 评测 case）",
    )
    ap.add_argument("--output", "-o", default=None, help="输出文件路径，默认写到 stdout（仅 jsonl）")
    ap.add_argument("--format", choices=("jsonl", "parquet"), default="jsonl", help="输出格式")
    args = ap.parse_args()

    records = build_records(
        args.dataset,
        args.diagram_type,
        args.include_no_ref,
        args.include_non_eval_cases,
    )
    write_records(records, args.output, args.format)


if __name__ == "__main__":
    main()
