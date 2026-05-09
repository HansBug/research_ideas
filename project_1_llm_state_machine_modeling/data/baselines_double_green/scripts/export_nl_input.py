#!/usr/bin/env python3
"""导出 NL 输入语料（仅 input_text，跨数据集统一格式）。

适用场景：retrieval 语料、clustering 输入、NL 难度分析、文本统计。

输出字段（一行一个 record）：

- ``record_id``
- ``dataset``
- ``input_text``
- ``input_char_count``
- ``input_word_count_approx``
- ``output_metamodel``

用法示例::

    # 默认输出到 stdout（推荐：流式管道给下游）
    python scripts/export_nl_input.py --dataset all

    # 持久化时落到本目录 datasets/ 子目录（git 可追溯位置；禁止写 /tmp 等仓库外路径）
    python scripts/export_nl_input.py --dataset llms_emp --diagram-type stm \\
        --output datasets/llms_emp_stm_inputs.jsonl
    python scripts/export_nl_input.py --dataset all --format parquet \\
        --output datasets/nl_inputs.parquet
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import DATASETS, iter_dataset, write_records


def build_records(dataset: str, diagram_type: str | None) -> list[dict]:
    out = []
    for r in iter_dataset(dataset, diagram_filter=diagram_type):
        text = r["input_text"] or ""
        out.append(
            {
                "record_id": r["record_id"],
                "dataset": r["dataset"],
                "input_text": text,
                "input_char_count": len(text),
                "input_word_count_approx": len(text.split()),
                "output_metamodel": r["output_metamodel"],
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--dataset",
        choices=("all", *DATASETS),
        default="all",
        help="选择数据集，默认 all 跨 4 个数据集合并",
    )
    ap.add_argument(
        "--diagram-type",
        choices=("stm", "act", "sd"),
        default=None,
        help="仅 llms_emp 有效；过滤为指定 diagram 类型（默认全部）",
    )
    ap.add_argument("--output", "-o", default=None, help="输出文件路径，默认写到 stdout（仅 jsonl）")
    ap.add_argument("--format", choices=("jsonl", "parquet"), default="jsonl", help="输出格式")
    args = ap.parse_args()

    records = build_records(args.dataset, args.diagram_type)
    write_records(records, args.output, args.format)


if __name__ == "__main__":
    main()
