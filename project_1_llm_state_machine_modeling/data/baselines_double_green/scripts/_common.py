"""4 个导出脚本共用的数据加载与字段映射工具。

目标：把分散在 4 个数据集 parquet 中的字段统一映射到一组**通用 benchmark 字段**：

- ``record_id``：全数据集唯一的样本 id
- ``dataset``：``llms_emp`` / ``ttool_ai`` / ``light_control_nimbus`` / ``structure_event_driven``
- ``input_text``：自然语言输入
- ``reference_text``：参考 STM 输出（可能为空）
- ``reference_format``：``plantuml`` / ``avatar_xml`` / ``rsmle`` / ``umple`` 等
- ``output_metamodel``：原数据集声明的输出元模型字符串
- ``meta``：原 parquet 行的额外字段（dict，给下游做切片用）

不要在这里读人评、不要在这里做语义清洗 —— 只做"把多源字段对齐到统一 schema"。
人评由 ``export_human_review.py`` 单独处理。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

import pandas as pd

# 数据目录绝对路径（相对于本文件）
DATA_DIR = Path(__file__).resolve().parent.parent

DATASETS = ("llms_emp", "ttool_ai", "light_control_nimbus", "structure_event_driven")


def _load(name: str) -> pd.DataFrame:
    """读取数据资产目录下指定 parquet。"""
    return pd.read_parquet(DATA_DIR / name)


def iter_llms_emp(diagram_filter: str | None = None) -> Iterator[dict]:
    """逐条产出 ``llms_emp`` 的 NL→STM/ACT/SD 样本。

    :param diagram_filter: ``"stm"`` / ``"act"`` / ``"sd"`` 之一，None 表示全部
    """
    df = _load("llms_emp_complete_samples.parquet")
    if diagram_filter:
        df = df[df["diagram_type"].str.lower() == diagram_filter.lower()]
    for _, row in df.iterrows():
        yield {
            "record_id": f"llms_emp::{int(row['row_id'])}",
            "dataset": "llms_emp",
            "input_text": row["requirements_description"],
            "reference_text": row["plantuml_code"],
            "reference_format": "plantuml",
            "output_metamodel": row["output_metamodel"],
            "meta": {
                "row_id": int(row["row_id"]),
                "diagram_type": row["diagram_type"],
                "model_name": row.get("model_name"),
                "selected_by_authors": bool(row.get("selected_by_authors", False)),
                "basic_state_count": _safe_int(row.get("basic_state_count")),
                "basic_transition_count": _safe_int(row.get("basic_transition_count")),
                "basic_hierarchical_state_count": _safe_int(row.get("basic_hierarchical_state_count")),
            },
        }


def iter_ttool_ai() -> Iterator[dict]:
    """逐条产出 ``ttool_ai`` 的 NL spec → AVATAR XML 样本。

    一行一个 model 变体；reference_text 是完整 raw_xml（含状态机面板）。
    """
    df = _load("ttool_ai_models.parquet")
    for _, row in df.iterrows():
        yield {
            "record_id": f"ttool_ai::{row['case_name']}::{row['variant_name']}",
            "dataset": "ttool_ai",
            "input_text": row["input_spec_text"],
            "reference_text": row["raw_xml"],
            "reference_format": "avatar_xml",
            "output_metamodel": row["output_metamodel"],
            "meta": {
                "case_name": row["case_name"],
                "variant_name": row["variant_name"],
                "modeling_type": row.get("modeling_type"),
                "block_panel_count": _safe_int(row.get("block_panel_count")),
                "state_machine_panel_count": _safe_int(row.get("state_machine_panel_count")),
                "state_count": _safe_int(row.get("state_count")),
                "transition_count": _safe_int(row.get("transition_count")),
            },
        }


def iter_light_control_nimbus() -> Iterator[dict]:
    """逐条产出 ``light_control_nimbus`` 的 NL 需求片段 → RSML-e 输出片段样本。"""
    df = _load("light_control_nimbus_fragments.parquet")
    for _, row in df.iterrows():
        yield {
            "record_id": f"light_control_nimbus::{row['case_id']}::{row['fragment_id']}",
            "dataset": "light_control_nimbus",
            "input_text": row["input_requirement_text"],
            "reference_text": row["output_fragment_excerpt"],
            "reference_format": "rsmle",
            "output_metamodel": row["output_metamodel"],
            "meta": {
                "case_id": row["case_id"],
                "fragment_id": row["fragment_id"],
                "abstraction_level": row.get("abstraction_level"),
                "sample_kind": row.get("sample_kind"),
            },
        }


def iter_structure_event_driven(only_paper_eval: bool = True) -> Iterator[dict]:
    """逐条产出 ``structure_event_driven`` 的 NL 描述 → Umple 参考解样本。

    :param only_paper_eval: 仅产出 paper 评测 case（默认开），关闭则也含课堂练习
    """
    df_cases = _load("structure_event_driven_cases.parquet")
    df_refs = _load("structure_event_driven_reference_solutions.parquet")

    if only_paper_eval:
        df_cases = df_cases[df_cases["is_paper_evaluation_case"]]

    refs_by_case = {r["case_id"]: r for _, r in df_refs.iterrows()}
    for _, row in df_cases.iterrows():
        ref = refs_by_case.get(row["case_id"])
        ref_text = ref["reference_solution_text"] if ref is not None else None
        yield {
            "record_id": f"structure_event_driven::{row['case_id']}",
            "dataset": "structure_event_driven",
            "input_text": row["system_description"],
            "reference_text": ref_text,
            "reference_format": "umple",
            "output_metamodel": row["output_metamodel"],
            "meta": {
                "case_id": row["case_id"],
                "case_name": row["case_name"],
                "is_paper_evaluation_case": bool(row["is_paper_evaluation_case"]),
                "has_full_reference_solution": bool(row.get("has_full_reference_solution", False)),
                **(
                    {
                        "reference_states_count": _safe_int(ref.get("reference_states_count")),
                        "reference_transitions_count": _safe_int(ref.get("reference_transitions_count")),
                        "reference_guards_count": _safe_int(ref.get("reference_guards_count")),
                        "reference_actions_count": _safe_int(ref.get("reference_actions_count")),
                        "reference_hierarchical_states_count": _safe_int(ref.get("reference_hierarchical_states_count")),
                        "reference_parallel_regions_count": _safe_int(ref.get("reference_parallel_regions_count")),
                    }
                    if ref is not None
                    else {}
                ),
            },
        }


def iter_dataset(name: str, **kwargs) -> Iterator[dict]:
    """按数据集名称分发到对应迭代器。

    :param name: ``llms_emp`` / ``ttool_ai`` / ``light_control_nimbus`` /
        ``structure_event_driven`` / ``all``
    :param kwargs: 透传给具体迭代器的额外参数（如 ``diagram_filter``）
    """
    if name == "all":
        for ds in DATASETS:
            yield from iter_dataset(ds, **kwargs)
        return
    fn = {
        "llms_emp": iter_llms_emp,
        "ttool_ai": iter_ttool_ai,
        "light_control_nimbus": iter_light_control_nimbus,
        "structure_event_driven": iter_structure_event_driven,
    }[name]
    # 过滤掉迭代器不认识的 kwargs，避免误传
    import inspect

    sig = inspect.signature(fn)
    accepted = {k: v for k, v in kwargs.items() if k in sig.parameters}
    yield from fn(**accepted)


def write_records(records: list[dict], output: str | None, output_format: str) -> None:
    """把 records 列表写到目标位置。

    :param records: 由 ``iter_dataset`` 产出的 dict 列表
    :param output: 输出路径；为 None 时写到 stdout
    :param output_format: ``jsonl`` 或 ``parquet``
    """
    if output_format == "jsonl":
        if output:
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            with open(output, "w", encoding="utf-8") as fh:
                for r in records:
                    fh.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
            print(f"wrote {len(records)} records to {output}")
        else:
            for r in records:
                print(json.dumps(r, ensure_ascii=False, default=str))
    elif output_format == "parquet":
        if not output:
            raise SystemExit("--output is required when --format=parquet")
        df = pd.DataFrame(records)
        # 把 meta dict 列序列化成 JSON 字符串以兼容 parquet
        if "meta" in df.columns:
            df["meta"] = df["meta"].apply(lambda x: json.dumps(x, ensure_ascii=False, default=str))
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(output, index=False)
        print(f"wrote {len(df)} rows to {output}")
    else:
        raise SystemExit(f"unknown --format: {output_format}")


def _safe_int(v) -> int | None:
    """``int(v)``；遇到 NaN / None / 空串时返回 None。"""
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass
    try:
        return int(v)
    except (TypeError, ValueError):
        return None
