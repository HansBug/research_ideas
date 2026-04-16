#!/usr/bin/env python3
from __future__ import annotations

import argparse
from functools import lru_cache
import importlib.util
import json
import math
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import pandas as pd


RAW_ROOT_DEFAULT = Path("/tmp/baseline_double_green/raw")
ASSET_DIR = Path(__file__).resolve().parent
BASE_BUILD_SCRIPT = ASSET_DIR / "build_baseline_double_green_parquets.py"
REPO_ROOT = ASSET_DIR.parents[2]
BASELINES_DIR = REPO_ROOT / "project_1_llm_state_machine_modeling" / "baselines"

PAPER_TITLES = {
    "llms_emp": "Generating SysML Behavior Models via Large Language Models: an Empirical Study",
    "ttool-ai": "System Architects Are not Alone Anymore: Automatic System Modeling with AI",
    "requirements-capture-and-evaluation-in-nimbus-light-control": (
        "Requirements Capture and Evaluation in Nimbus: The Light-Control Case Study"
    ),
    "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models": (
        "Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models"
    ),
}

ODS_NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}

PAPER_METHOD_EXCERPT_SPECS = {
    "llms_emp": [
        ("reviewer_pool", 339, 347),
        ("evaluation_process", 410, 453),
        ("hallucination_examples", 701, 708),
    ],
    "ttool-ai": [
        ("review_setup", 868, 893),
        ("results_summary", 895, 905),
    ],
    "requirements-capture-and-evaluation-in-nimbus-light-control": [
        ("vv_triage", 598, 610),
        ("manual_inspection_roles", 605, 609),
        ("modeling_team", 941, 948),
    ],
    "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models": [
        ("evaluation_procedure", 331, 357),
        ("matching_rules", 377, 427),
        ("bias_statement", 840, 845),
    ],
}


def load_base_module():
    spec = importlib.util.spec_from_file_location("baseline_double_green_build", BASE_BUILD_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {BASE_BUILD_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_base_module()
json_compact = base.json_compact
normalize_text = base.normalize_text
write_parquet = base.write_parquet


def normalize_number(value: Any) -> float | int | None:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, str):
        value = value.strip()
        if value in {"", "-", "nan"}:
            return None
        if "." not in value and value.count(",") == 1 and re.fullmatch(r"-?\d+,\d+", value):
            value = value.replace(",", ".")
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return None
    if float(number).is_integer():
        return int(number)
    return float(number)


def raw_source_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (list, dict)):
        return value
    try:
        if pd.isna(value):
            return None
    except TypeError:
        pass
    if isinstance(value, str):
        return value.replace("\r\n", "\n").replace("\r", "\n")
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if math.isnan(value):
            return None
        if value.is_integer():
            return int(value)
        return float(value)
    try:
        normalized = normalize_number(value)
        if normalized is not None:
            return normalized
    except Exception:
        pass
    return str(value)


def row_to_original_json(row: pd.Series, columns: list[str]) -> str:
    payload = {column: raw_source_value(row[column]) for column in columns if column in row.index}
    return json_compact(payload)


def lines_excerpt(path: Path, start: int, end: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[start - 1 : end]).strip()


@lru_cache(maxsize=None)
def paper_method_excerpt_bundle(slug: str) -> tuple[str | None, str | None]:
    specs = PAPER_METHOD_EXCERPT_SPECS.get(slug, [])
    if not specs:
        return None, None
    path = paper_dir(slug) / "paper_content.txt"
    if not path.exists():
        return None, None
    segments = []
    for label, start, end in specs:
        text = lines_excerpt(path, start, end)
        if not text:
            continue
        segments.append(
            {
                "label": label,
                "source_path": str(path),
                "start_line": start,
                "end_line": end,
                "text": text,
                "verbatim_extracted": True,
            }
        )
    if not segments:
        return None, None
    combined = "\n\n".join(f"[{segment['label']}]\n{segment['text']}" for segment in segments)
    return combined, json_compact(segments)


def verbatim_entries_to_text(entries: list[dict[str, Any]]) -> str | None:
    if not entries:
        return None
    blocks = []
    for entry in entries:
        label = entry.get("label") or entry.get("column_name") or "excerpt"
        text = entry.get("text")
        if not text:
            continue
        blocks.append(f"[{label}]\n{text}")
    if not blocks:
        return None
    return "\n\n".join(blocks)


def normalize_structure_metric_case_name(value: Any) -> str | None:
    text = normalize_text(value)
    if not text:
        return None
    text = text.split("\n", 1)[0].strip()
    text = re.sub(r"\s*\([^)]*\)\s*$", "", text).strip()
    return text or None


def xlsx_verbatim_entry(
    *,
    sheet_name: str,
    row_idx: int,
    column_name: str,
    label: str,
    text: str,
) -> dict[str, Any]:
    return {
        "source_kind": "xlsx_cell",
        "sheet_name": sheet_name,
        "row_index_0_based": row_idx,
        "row_number_1_based_with_header": row_idx + 2,
        "column_name": column_name,
        "label": label,
        "text": text,
        "verbatim_extracted": True,
    }


def ods_verbatim_row_payload(
    *,
    source_path: Path,
    sheet_name: str,
    row_label: str | None,
    header_row: list[str | None],
    raw_row: list[str | None],
    row_index: int | None = None,
    header_row_index: int | None = None,
    extra_rows: dict[str, list[str | None]] | None = None,
    extra_row_indexes: dict[str, int] | None = None,
) -> str:
    payload: dict[str, Any] = {
        "source_kind": "ods_row",
        "source_path": str(source_path),
        "sheet_name": sheet_name,
        "row_label": row_label,
        "header_row": [raw_source_value(value) for value in header_row],
        "raw_row": [raw_source_value(value) for value in raw_row],
        "header_to_value": {},
    }
    if row_index is not None:
        payload["row_index_0_based"] = row_index
    if header_row_index is not None:
        payload["header_row_index_0_based"] = header_row_index
    for idx, header in enumerate(header_row):
        if header is None:
            continue
        cell_value = raw_row[idx] if idx < len(raw_row) else None
        payload["header_to_value"][str(header)] = raw_source_value(cell_value)
    if extra_rows:
        payload["extra_rows"] = {
            key: [raw_source_value(value) for value in values] for key, values in extra_rows.items()
        }
    if extra_row_indexes:
        payload["extra_row_indexes_0_based"] = dict(extra_row_indexes)
    return json_compact(payload)


def raw_ods_row_text(raw_row: list[str | None]) -> str | None:
    values = [raw_source_value(value) for value in raw_row]
    values = [value for value in values if value not in {None, ""}]
    if not values:
        return None
    return "\t".join(str(value) for value in values)


TTOOL_STAT_LABEL_MAP = {
    "average": "average",
    "std. d.": "std_dev",
    "std dev": "std_dev",
    "std dev.": "std_dev",
    "highest grade": "highest_grade",
    "lowest grade": "lowest_grade",
}


def normalize_ttool_stat_label(value: str | None) -> str | None:
    text = normalize_text(value)
    if not text:
        return None
    return TTOOL_STAT_LABEL_MAP.get(text.lower())


def df_value(row: pd.Series, *candidates: str) -> Any:
    for column in candidates:
        if column in row.index:
            value = row[column]
            if pd.isna(value):
                continue
            return value
    return None


def column_in(df: pd.DataFrame, *candidates: str) -> str | None:
    for column in candidates:
        if column in df.columns:
            return column
    return None


def paper_dir(slug: str) -> Path:
    return BASELINES_DIR / slug


LLMS_EMP_REVIEW_SOURCE_COLUMNS = [
    "Model Source",
    "Model Name",
    "Requirement Description",
    "PlantUML",
    "Grammar Point",
    "Prompt",
    "LLMs",
    "Generation PlantUML",
    "Generation Time",
    "PlantUML Accuracy",
    "Plantuml Accuracy",
    "PlantUML Accuracy Rate",
    "SysML Grammar Accuracy",
    "SysML Grammar Accuracy Rate",
    "True Positive",
    "False Positive",
    "False Negative",
    "F1 Score",
    "Format Hallucinations",
    "Result with Format Checking",
    "Resolved",
    "PlantUML Accuracy.1",
    "Generation Time.1",
    "SysML Grammar Hallucinations",
    "Result with Grammar Checking",
    "Resolved.1",
    "SysML Grammar Accuracy.1",
    "Generation Time.2",
    "Semmantic Hallucinations",
    "SysML Semmantic Hallucinations",
    "Result with Semantic Checking",
    "Resolved.2",
    "True Positive.1",
    "False Positive.1",
    "False Negative.1",
    "F1 Score.1",
    "Generation PlantUML.1",
    "Generation PlantUML.2",
    "Generation PlantUML.3",
    "Generation Time.3",
    "Grammar Accuracy",
]

LLMS_EMP_REVIEW_TEXT_COLUMNS = [
    ("Format Hallucinations", "format_hallucinations"),
    ("SysML Grammar Hallucinations", "grammar_hallucinations"),
    ("Semmantic Hallucinations", "semantic_hallucinations"),
    ("SysML Semmantic Hallucinations", "semantic_hallucinations"),
]


def llms_emp_verbatim_entries(row: pd.Series, sheet_name: str, row_idx: int) -> list[dict[str, Any]]:
    entries = []
    seen: set[tuple[str, str]] = set()
    for column_name, label in LLMS_EMP_REVIEW_TEXT_COLUMNS:
        if column_name not in row.index:
            continue
        text = raw_source_value(row[column_name])
        if not isinstance(text, str) or not text.strip():
            continue
        dedupe_key = (column_name, text)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        entries.append(
            xlsx_verbatim_entry(
                sheet_name=sheet_name,
                row_idx=row_idx,
                column_name=column_name,
                label=label,
                text=text,
            )
        )
    return entries


def structure_event_raw_review_index(workbook_path: Path) -> dict[tuple[str, str, str, str], str]:
    sheet_specs = {
        "SinglePrompt": ("single_prompt", [("GPT-4o", 0), ("Claude 3.5 Sonnet", 10)]),
        "StructureDriven": ("structure_driven", [("GPT-4o", 0), ("Claude 3.5 Sonnet", 10)]),
        "EventDriven": ("event_driven", [("GPT-4o", 0), ("Claude 3.5 Sonnet", 10)]),
        "Hybrid": ("hybrid", [("GPT-4o", 0), ("Claude 3.5 Sonnet", 10)]),
    }
    index: dict[tuple[str, str, str, str], str] = {}
    for sheet_name, (strategy_name, blocks) in sheet_specs.items():
        df = pd.read_excel(workbook_path, sheet_name=sheet_name, header=None)
        for llm_name, col in blocks:
            header_row = None
            for idx in range(len(df)):
                if normalize_text(df.iat[idx, col]) == "System Name":
                    header_row = idx
                    break
            if header_row is None:
                continue
            current_system = None
            current_image_reference = None
            header_values = [raw_source_value(df.iat[header_row, col + offset]) for offset in range(9)]
            for row_idx in range(header_row + 1, len(df)):
                system_value = df.iat[row_idx, col]
                component_value = df.iat[row_idx, col + 1] if col + 1 < df.shape[1] else None
                if pd.isna(system_value) and pd.isna(component_value):
                    continue
                normalized_system = normalize_structure_metric_case_name(system_value)
                if normalized_system:
                    current_system = normalized_system
                    current_image_reference = raw_source_value(df.iat[row_idx, col + 8])
                if current_system is None:
                    continue
                component = normalize_text(component_value)
                if not component:
                    continue
                key = (
                    strategy_name,
                    llm_name,
                    base.canonical_structure_event_case_id(current_system),
                    component,
                )
                raw_row = [raw_source_value(df.iat[row_idx, col + offset]) for offset in range(9)]
                payload = {
                    "source_kind": "xlsx_row",
                    "source_path": str(workbook_path),
                    "sheet_name": sheet_name,
                    "row_index_0_based": row_idx,
                    "row_number_1_based_with_header": row_idx + 1,
                    "strategy_name": strategy_name,
                    "llm_name": llm_name,
                    "system_name_raw": raw_source_value(system_value),
                    "system_name_normalized": current_system,
                    "component_raw": raw_source_value(component_value),
                    "image_reference_raw": current_image_reference,
                    "header_row": header_values,
                    "raw_row": raw_row,
                    "header_to_value": {
                        str(header_values[offset]): raw_row[offset]
                        for offset in range(min(len(header_values), len(raw_row)))
                        if header_values[offset] not in {None, ""}
                    },
                }
                index[key] = json_compact(payload)
    return index


def build_protocols() -> pd.DataFrame:
    def protocol_row(base_row: dict[str, Any]) -> dict[str, Any]:
        excerpt_text, excerpt_json = paper_method_excerpt_bundle(base_row["paper_slug"])
        base_row["paper_method_verbatim_excerpt"] = excerpt_text
        base_row["paper_method_verbatim_excerpt_json"] = excerpt_json
        base_row["paper_method_verbatim_verified"] = excerpt_text is not None
        return base_row

    rows = [
        protocol_row(
            {
            "paper_slug": "llms_emp",
            "paper_title": PAPER_TITLES["llms_emp"],
            "paper_local_path": str(paper_dir("llms_emp") / "paper_content.txt"),
            "public_human_review_status": "sample_level_available",
            "human_review_artifact": str(
                RAW_ROOT_DEFAULT / "llms_emp_gmodel" / "Experiment Results.xlsx"
            ),
            "reviewer_pool": (
                "G_Model 组由 1 名高年级本科生、2 名硕士生、2 名博士生组成；"
                "团队成员均有软件工程与 MDD 背景，并具有 100+ 小时建模经验。"
            ),
            "reference_basis": (
                "参考模型为公开 G_Model 数据集中的人工构建 PlantUML/SysML 行为模型；"
                "SysML 语法和 55 条语义检查项来自 SysML v1.6 规范。"
            ),
            "artifact_under_review": (
                "LLM 生成的 PlantUML 行为模型，按 STM / ACT / SD 三类任务逐样本评审。"
            ),
            "review_dimensions_json": json_compact(
                [
                    "PlantUML format accuracy (自动)",
                    "SysML grammar accuracy (人工)",
                    "semantic consistency F1-score (人工)",
                    "hallucination taxonomy",
                ]
            ),
            "execution_steps_markdown": (
                "1. 用论文给定 prompt 模板向 LLM 生成 PlantUML。 "
                "2. 先做 PlantUML 格式检查。 "
                "3. 人工逐项对照 SysML v1.6 语法点记录语法错误。 "
                "4. 人工逐项检查 55 条 SysML 语义约束记录语义违规。 "
                "5. 将生成模型与参考模型做 TP/FP/FN 对照并计算 F1。 "
                "6. 把检测到的问题反馈回提示词，重新生成并重复同一检查。"
            ),
            "matching_rules_markdown": (
                "语法检查逐项对照 SysML 规范；语义检查逐条对照 55 条语义规则；"
                "需求语义一致性用参考模型做组件级 TP/FP/FN 统计。"
            ),
            "public_gap_notes": (
                "公开包给出了逐样本结果表，但没有把人工检查过程的逐条注释拆成独立日志文件。"
            ),
        }
        ),
        protocol_row(
            {
            "paper_slug": "ttool-ai",
            "paper_title": PAPER_TITLES["ttool-ai"],
            "paper_local_path": str(paper_dir("ttool-ai") / "paper_content.txt"),
            "public_human_review_status": "summary_only_available",
            "human_review_artifact": str(RAW_ROOT_DEFAULT / "ttool-ai" / "results.ods"),
            "reviewer_pool": (
                "约 15 名 master-level 学生在 21 小时课程训练后参加对照实验；"
                "TTool-AI 与学生使用相同评分标准。"
            ),
            "reference_basis": (
                "不是 gold reference 模型对齐打分，而是按软件工程质量标准对生成图进行整体评分。"
            ),
            "artifact_under_review": (
                "Block Diagram (BD) 与 State Machine Diagram (SMD) 的整体设计质量；"
                "补充包还给出 connectedDevice / packagingLine 的 UCD / BD / SMD / Properties 分数。"
            ),
            "review_dimensions_json": json_compact(
                [
                    "adequacy to specification",
                    "behavior consistency under TTool simulator",
                    "quantity of exchanges between blocks",
                    "diagram readability",
                    "number of blocks/states and naming consistency",
                    "unused attributes in blocks",
                    "syntactic correctness via TTool syntax checker",
                ]
            ),
            "execution_steps_markdown": (
                "1. 给学生系统规格，训练后限时 1.5 小时手工画图。 "
                "2. 对 TTool-AI 关闭人工交互，直接生成模型。 "
                "3. 按同一软件工程质量标准分别给 BD 和 SMD 打 /100 分。 "
                "4. 记录生成/作图时间。 "
                "5. 汇总平均分、标准差、最高/最低分。"
            ),
            "matching_rules_markdown": (
                "论文只公开了评分维度说明和总分，没有公开逐题 rubric 或逐项扣分明细。"
            ),
            "public_gap_notes": (
                "主仓库公开了规格、XML 模型与总分表，但没有公开每次测试的独立输出版本与逐项评分表，"
                "因此只能恢复 summary-level 人评。"
            ),
        }
        ),
        protocol_row(
            {
            "paper_slug": "requirements-capture-and-evaluation-in-nimbus-light-control",
            "paper_title": PAPER_TITLES["requirements-capture-and-evaluation-in-nimbus-light-control"],
            "paper_local_path": str(
                paper_dir("requirements-capture-and-evaluation-in-nimbus-light-control")
                / "paper_content.txt"
            ),
            "public_human_review_status": "method_only_no_raw_scores",
            "human_review_artifact": str(RAW_ROOT_DEFAULT / "light-case-jucs.pdf"),
            "reviewer_pool": (
                "两名熟悉 RSML-e 与 Nimbus 的研究生参与建模；"
                "manual inspections 面向规格团队、客户、系统工程师和监管代表。"
            ),
            "reference_basis": (
                "不是 LLM 输出评分类 benchmark，而是对 Light Control 规格进行 "
                "manual inspections + formal verification + simulation/testing 的三联 V&V。"
            ),
            "artifact_under_review": (
                "REQ/SOFT 层 RSML-e 规格、环境模型、控制面板 mockup 与模拟执行结果。"
            ),
            "review_dimensions_json": json_compact(
                [
                    "manual inspections",
                    "formal verification of desired properties",
                    "simulation and testing of the specification",
                    "usability evaluation of room control panel mockup",
                ]
            ),
            "execution_steps_markdown": (
                "1. 用 RSML-e 捕获 REQ/SOFT 规格。 "
                "2. 用 Nimbus 做 manual inspection 可视化审查。 "
                "3. 通过形式化验证检查所需性质。 "
                "4. 通过环境模型、控制面板 mockup 和测试文件做仿真/测试。 "
                "5. 依据仿真结果与用户交互反馈修改需求和面板设计。"
            ),
            "matching_rules_markdown": (
                "论文明确强调三种 V&V 手段必须联合使用，但未公开逐条 inspection checklist 或评分表。"
            ),
            "public_gap_notes": (
                "公开材料是案例规格与论文说明，不存在逐样本人评原始分数表。"
            ),
        }
        ),
        protocol_row(
            {
            "paper_slug": "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models",
            "paper_title": PAPER_TITLES[
                "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models"
            ],
            "paper_local_path": str(
                paper_dir(
                    "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models"
                )
                / "paper_content.txt"
            ),
            "public_human_review_status": "sample_level_available",
            "human_review_artifact": str(
                RAW_ROOT_DEFAULT / "llm_state_machine_final_f1_scores.xlsx"
            ),
            "reviewer_pool": (
                "每个设计策略由单个作者负责评审；论文说明实验手工评审由部分作者完成，"
                "并通过事先约定评审准则降低偏差。"
            ),
            "reference_basis": (
                "8 个英文建模题目，每题有 modeling experts 手工绘制的 ground-truth UML state machine。"
            ),
            "artifact_under_review": (
                "Single Prompt / Structure-Driven / Event-Driven / Hybrid 生成结果；"
                "单提示输出是 Umple 代码，其余策略输出是 HTML 表格再渲染成图。"
            ),
            "review_dimensions_json": json_compact(
                [
                    "states",
                    "transitions",
                    "guards",
                    "actions (transition actions only)",
                    "hierarchical states",
                    "parallel regions",
                    "history states",
                    "All",
                ]
            ),
            "execution_steps_markdown": (
                "1. 为每个案例准备英文问题描述和 ground-truth 状态机。 "
                "2. 运行各生成策略得到 Umple 或中间 HTML 表。 "
                "3. 把生成结果与 ground-truth 图逐组件人工对照。 "
                "4. 对每个组件记 TP/FP/FN："
                " exact match 或 semantic match 计 TP；"
                " 多余组件计 FP；漏掉的 ground-truth 组件计 FN。 "
                "5. 若状态不匹配，则依附其上的 transition/guard/action 默认按严格口径记为 FP。 "
                "6. 按组件计算 precision / recall / F1。"
            ),
            "matching_rules_markdown": (
                "允许 near-exact/semantic match，例如不同命名但表达同一概念可算匹配；"
                "superstate/parallel region 若子状态集合等价也可算匹配；"
                "但 transitions/guards/actions 对错误状态依赖采取严格惩罚口径。"
            ),
            "public_gap_notes": (
                "公开 artifact 给出逐组件 TP/FN/FP/F1 和预测图像，但大多数预测的文本版 Umple 未公开。"
            ),
        }
        ),
    ]
    return pd.DataFrame(rows)


def build_llms_emp_human_review(raw_root: Path) -> pd.DataFrame:
    workbook = raw_root / "llms_emp_gmodel" / "Experiment Results.xlsx"
    paper_excerpt_text, paper_excerpt_json = paper_method_excerpt_bundle("llms_emp")
    rows: list[dict[str, Any]] = []
    for sheet_name, diagram_type in (
        ("STM Results", "stm"),
        ("ACT Results", "act"),
        ("SD Results", "sd"),
    ):
        df = pd.read_excel(workbook, sheet_name=sheet_name)
        for row_idx, row in df.iterrows():
            input_text = normalize_text(df_value(row, "Requirement Description"))
            ref_output = normalize_text(df_value(row, "PlantUML"))
            pred_output = normalize_text(df_value(row, "Generation PlantUML"))
            llm_name = normalize_text(df_value(row, "LLMs"))
            if not input_text or not ref_output or not pred_output or not llm_name:
                continue
            source_row_json = row_to_original_json(row, LLMS_EMP_REVIEW_SOURCE_COLUMNS)
            verbatim_entries = llms_emp_verbatim_entries(row, sheet_name, row_idx)

            details = {
                "initial": {
                    "plantuml_accuracy_count": normalize_text(
                        df_value(row, "PlantUML Accuracy", "Plantuml Accuracy")
                    ),
                    "plantuml_accuracy_rate": normalize_number(
                        df_value(row, "PlantUML Accuracy Rate")
                    ),
                    "sysml_grammar_accuracy_count": normalize_text(
                        df_value(row, "SysML Grammar Accuracy")
                    ),
                    "sysml_grammar_accuracy_rate": normalize_number(
                        df_value(row, "SysML Grammar Accuracy Rate")
                    ),
                    "semantic_tp": normalize_number(df_value(row, "True Positive")),
                    "semantic_fp": normalize_number(df_value(row, "False Positive")),
                    "semantic_fn": normalize_number(df_value(row, "False Negative")),
                    "semantic_f1": normalize_number(df_value(row, "F1 Score")),
                    "format_hallucinations": normalize_text(
                        df_value(row, "Format Hallucinations")
                    ),
                    "grammar_hallucinations": normalize_text(
                        df_value(row, "SysML Grammar Hallucinations")
                    ),
                    "semantic_hallucinations": normalize_text(
                        df_value(row, "Semmantic Hallucinations", "SysML Semmantic Hallucinations")
                    ),
                },
                "regenerated": {
                    "after_format_output": normalize_text(
                        df_value(row, "Result with Format Checking", "Generation PlantUML.1")
                    ),
                    "after_format_accuracy_count": normalize_text(
                        df_value(row, "PlantUML Accuracy.1", "PlantUML Accuracy")
                    ),
                    "after_format_generation_time_s": normalize_number(
                        df_value(row, "Generation Time.1")
                    ),
                    "after_grammar_output": normalize_text(
                        df_value(row, "Result with Grammar Checking", "Generation PlantUML.2")
                    ),
                    "after_grammar_accuracy_count": normalize_text(
                        df_value(row, "SysML Grammar Accuracy.1", "Grammar Accuracy")
                    ),
                    "after_grammar_generation_time_s": normalize_number(
                        df_value(row, "Generation Time.2")
                    ),
                    "after_semantic_output": normalize_text(
                        df_value(row, "Result with Semantic Checking", "Generation PlantUML.3")
                    ),
                    "after_semantic_tp": normalize_number(df_value(row, "True Positive.1")),
                    "after_semantic_fp": normalize_number(df_value(row, "False Positive.1")),
                    "after_semantic_fn": normalize_number(df_value(row, "False Negative.1")),
                    "after_semantic_f1": normalize_number(df_value(row, "F1 Score.1")),
                    "after_semantic_generation_time_s": normalize_number(
                        df_value(row, "Generation Time.3")
                    ),
                },
            }

            rows.append(
                {
                    "paper_slug": "llms_emp",
                    "paper_title": PAPER_TITLES["llms_emp"],
                    "record_source": str(workbook),
                    "sheet_name": sheet_name,
                    "diagram_type": diagram_type,
                    "record_type": "sample_level_review",
                    "review_record_id": f"{sheet_name}:{row_idx}",
                    "model_source": normalize_text(df_value(row, "Model Source")),
                    "model_name": normalize_text(df_value(row, "Model Name")),
                    "llm_name": llm_name,
                    "prompt_text": normalize_text(df_value(row, "Prompt")),
                    "input_text": input_text,
                    "ref_output_text": ref_output,
                    "ref_output_format": "PlantUML / SysML behavior model",
                    "ref_output_artifact_path": str(raw_root / "llms_emp_gmodel" / "Dataset.xlsx"),
                    "pred_output_text": pred_output,
                    "pred_output_format": "PlantUML / SysML behavior model",
                    "pred_output_artifact_path": str(workbook),
                    "review_target": "generated_behavior_model",
                    "human_review_score": normalize_number(df_value(row, "F1 Score")),
                    "human_review_score_unit": "semantic_f1",
                    "human_review_summary": (
                        "Manual grammar + semantic review with reference-model TP/FP/FN accounting."
                    ),
                    "human_review_details_json": json_compact(details),
                    "human_review_source_record_json": source_row_json,
                    "human_review_original_text": verbatim_entries_to_text(verbatim_entries),
                    "human_review_original_text_json": json_compact(verbatim_entries),
                    "paper_method_verbatim_excerpt": paper_excerpt_text,
                    "paper_method_verbatim_excerpt_json": paper_excerpt_json,
                    "verbatim_extraction_verified": True,
                    "review_rubric_text": (
                        "Grammar: manual comparison against SysML v1.6 grammar points. "
                        "Semantics: manual check against 55 semantics. "
                        "Requirement alignment: TP/FP/FN and F1 against the reference model."
                    ),
                    "public_artifact_limitations": (
                        "Workbook公开了逐样本结果，但人工审查日志只以汇总列形式保留在结果表中。"
                    ),
                }
            )
    return pd.DataFrame(rows)


def normalize_path_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def build_structure_event_output_index(raw_root: Path) -> dict[tuple[str, str, str], Path]:
    resources_root = raw_root / "llm_state_machine_modeling" / "Paper Experiment Resources"
    strategy_dirs = {
        "single_prompt": resources_root / "Final Single Prompt",
        "structure_driven": resources_root / "Final Structure-Driven",
        "event_driven": resources_root / "Final Event-Driven",
        "hybrid": resources_root / "Final Hybrid Approach",
    }
    index: dict[tuple[str, str, str], Path] = {}
    for strategy_name, strategy_dir in strategy_dirs.items():
        if not strategy_dir.exists():
            continue
        for path in strategy_dir.rglob("*.png"):
            llm_dir = path.parent.name
            index[(strategy_name, normalize_path_key(llm_dir), path.name)] = path
    return index


STRUCTURE_EVENT_CASE_FILE_ALIASES = {
    "printer_winter_2017": ["Printer"],
    "spa_manager_winter_2018": ["SpaManager", "Spa_Manager", "Spamanager"],
    "dishwasher_winter_2019": ["Dishwasher"],
    "chess_clock_fall_2019": ["ChessClock", "Chess_Clock", "Digital_Chess_Clock"],
    "automatic_bread_maker_fall_2020": ["Breadmaker", "BreadMaker", "Automatic_Bread_Maker"],
    "thermomix_fall_2021": ["Thermomix"],
    "WUMPLE_fall_2023": ["WUMPLE", "Wumple"],
    "SSC7_fall_2024": ["SSC7", "Ssc7"],
}


def llm_folder_tokens(llm_name: str) -> list[str]:
    tokens = [normalize_path_key(llm_name)]
    if llm_name == "GPT-4o":
        tokens.append(normalize_path_key("GPT4o"))
    if llm_name == "Claude 3.5 Sonnet":
        tokens.append(normalize_path_key("Claude Sonnet 3.5"))
        tokens.append(normalize_path_key("Claude 3.5 Sonnet"))
    return tokens


def structure_event_output_paths(
    output_index: dict[tuple[str, str, str], Path],
    strategy_name: str,
    llm_name: str,
    case_id: str,
    image_reference: str | None,
) -> list[Path]:
    if not image_reference:
        image_reference = None
    if image_reference:
        image_reference = image_reference.strip()
    llm_keys = llm_folder_tokens(llm_name)
    for llm_key in llm_keys:
        if image_reference:
            candidate = output_index.get((strategy_name, llm_key, image_reference))
            if candidate is not None:
                return [candidate]

    aliases = STRUCTURE_EVENT_CASE_FILE_ALIASES.get(case_id, [])
    matches: list[Path] = []
    for (strategy_key, llm_key, basename), path in output_index.items():
        if strategy_key != strategy_name or llm_key not in llm_keys:
            continue
        if any(alias.lower() in basename.lower() for alias in aliases):
            matches.append(path)
    deduped = sorted({path.resolve() for path in matches})
    return [Path(path) for path in deduped]


def build_structure_event_human_review(raw_root: Path) -> pd.DataFrame:
    source_path = raw_root / "llm_state_machine_final_f1_scores.xlsx"
    paper_excerpt_text, paper_excerpt_json = paper_method_excerpt_bundle(
        "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models"
    )
    frames = base.build_structure_event_driven(raw_root)
    cases_df = frames["structure_event_driven_cases"].copy()
    refs_df = frames["structure_event_driven_reference_solutions"].copy()
    metrics_df = frames["structure_event_driven_metrics"].copy()
    output_index = build_structure_event_output_index(raw_root)
    raw_index = structure_event_raw_review_index(source_path)

    cases = cases_df.set_index("case_id").to_dict(orient="index")
    refs = refs_df.set_index("case_id").to_dict(orient="index")

    rows: list[dict[str, Any]] = []
    for idx, metric in metrics_df.iterrows():
        case_id = metric.get("case_id")
        if not case_id:
            continue
        case_row = cases.get(case_id, {})
        ref_row = refs.get(case_id, {})
        pred_paths = structure_event_output_paths(
            output_index,
            metric["strategy_name"],
            metric["llm_name"],
            case_id,
            metric.get("image_reference"),
        )
        pred_path = pred_paths[0] if len(pred_paths) == 1 else None
        pred_text_path = pred_path.with_suffix(".txt") if pred_path is not None else None
        pred_text = (
            pred_text_path.read_text(encoding="utf-8").strip()
            if pred_text_path is not None and pred_text_path.exists()
            else None
        )
        raw_record_json = raw_index.get(
            (
                metric["strategy_name"],
                metric["llm_name"],
                case_id,
                metric["component"],
            )
        )
        raw_record_text = None
        if raw_record_json is not None:
            raw_payload = json.loads(raw_record_json)
            raw_row = raw_payload.get("raw_row") or []
            raw_record_text = "\t".join(str(value) for value in raw_row if value not in {None, ""}) or None
        rows.append(
            {
                "paper_slug": "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models",
                "paper_title": PAPER_TITLES[
                    "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models"
                ],
                "record_source": str(source_path),
                "record_type": "component_level_review",
                "review_record_id": f"{metric['strategy_name']}:{metric['llm_name']}:{case_id}:{metric['component']}:{idx}",
                "case_id": case_id,
                "case_name": case_row.get("case_name"),
                "strategy_name": metric["strategy_name"],
                "llm_name": metric["llm_name"],
                "component": metric["component"],
                "input_text": case_row.get("system_description"),
                "ref_output_text": ref_row.get("reference_solution_text"),
                "ref_output_format": ref_row.get("reference_solution_representation"),
                "ref_output_artifact_path": ref_row.get("reference_image_local_path"),
                "pred_output_text": pred_text,
                "pred_output_format": "Rendered UML state machine image",
                "pred_output_artifact_path": (
                    str(pred_path)
                    if pred_path is not None
                    else (json_compact([str(path) for path in pred_paths]) if pred_paths else None)
                ),
                "review_target": metric["component"],
                "human_review_score": metric["f1_score"],
                "human_review_score_unit": "f1",
                "human_review_summary": (
                    "Manual TP/FP/FN matching against expert ground-truth state machines."
                ),
                "human_review_details_json": json_compact(
                    {
                        "tp": metric["tp"],
                        "fn": metric["fn"],
                        "fp": metric["fp"],
                        "precision": metric["precision"],
                        "recall": metric["recall"],
                        "f1_score": metric["f1_score"],
                    }
                ),
                "human_review_source_record_json": raw_record_json,
                "human_review_original_text": raw_record_text,
                "human_review_original_text_json": json_compact(
                    [
                        {
                            "source_kind": "xlsx_row",
                            "sheet_name": metric["sheet_name"],
                            "label": metric["component"],
                            "text": raw_record_text,
                            "verbatim_extracted": raw_record_text is not None,
                        }
                    ]
                    if raw_record_text is not None
                    else []
                ),
                "paper_method_verbatim_excerpt": paper_excerpt_text,
                "paper_method_verbatim_excerpt_json": paper_excerpt_json,
                "verbatim_extraction_verified": True,
                "review_rubric_text": (
                    "Exact or near-exact semantic matches count as TP; "
                    "extra components count as FP; missing ground-truth components count as FN; "
                    "transitions/guards/actions attached to incorrect states are judged strictly."
                ),
                "public_artifact_limitations": (
                    "大部分预测只公开了渲染图片，没有公开对应的完整 Umple 文本。"
                ),
            }
        )
    return pd.DataFrame(rows)


def ods_cell_text(cell: ET.Element) -> str | None:
    paragraphs = ["".join(p.itertext()).strip() for p in cell.findall("text:p", ODS_NS)]
    text = "\n".join(p for p in paragraphs if p).strip()
    if text:
        return text
    for key in ("{urn:oasis:names:tc:opendocument:xmlns:office:1.0}value",):
        value = cell.attrib.get(key)
        if value not in {None, ""}:
            return value
    return None


def read_ods_tables(path: Path) -> dict[str, list[list[str | None]]]:
    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("content.xml"))
    spreadsheet = root.find("office:body/office:spreadsheet", ODS_NS)
    if spreadsheet is None:
        return {}
    tables: dict[str, list[list[str | None]]] = {}
    for table in spreadsheet.findall("table:table", ODS_NS):
        table_name = table.attrib.get(f"{{{ODS_NS['table']}}}name")
        table_rows: list[list[str | None]] = []
        for row in table.findall("table:table-row", ODS_NS):
            repeat_rows = int(row.attrib.get(f"{{{ODS_NS['table']}}}number-rows-repeated", "1"))
            values: list[str | None] = []
            for cell in list(row):
                if cell.tag not in {
                    f"{{{ODS_NS['table']}}}table-cell",
                    f"{{{ODS_NS['table']}}}covered-table-cell",
                }:
                    continue
                repeat_cols = int(
                    cell.attrib.get(f"{{{ODS_NS['table']}}}number-columns-repeated", "1")
                )
                value = ods_cell_text(cell) if cell.tag.endswith("table-cell") else None
                values.extend([value] * repeat_cols)
            while values and values[-1] is None:
                values.pop()
            for _ in range(repeat_rows):
                table_rows.append(values.copy())
        tables[table_name] = table_rows
    return tables


def row_value(row: list[str | None], idx: int) -> str | None:
    if idx < 0 or idx >= len(row):
        return None
    return normalize_text(row[idx])


def build_ttool_ai_main_review(raw_root: Path, models_df: pd.DataFrame) -> pd.DataFrame:
    source_path = raw_root / "ttool-ai" / "results.ods"
    paper_excerpt_text, paper_excerpt_json = paper_method_excerpt_bundle("ttool-ai")
    tables = read_ods_tables(source_path)
    model_lookup = (
        models_df.drop_duplicates(subset=["case_id"], keep="first")
        .set_index("case_id")
        .to_dict(orient="index")
    )
    sheet_case_map = {
        "Platooning": "platooning",
        "Space-based system": "space_based_system",
        "Automated braking": "automated_braking",
    }
    rows: list[dict[str, Any]] = []

    def append_main_record(
        *,
        sheet_name: str,
        case_id: str,
        case_name: str | None,
        record_type: str,
        review_record_id: str,
        split_name: str,
        review_target: str,
        review_index: int | None,
        human_review_score: float | int | None,
        row_label: str | None,
        raw_row: list[str | None],
        row_idx: int,
        header_row: list[str | None],
        header_row_idx: int,
        input_text: str | None,
        pred_output_text: str | None,
        pred_output_format: str | None,
        pred_output_path: str | None,
        elapsed_s: float | int | None,
        statistic_kind: str | None,
        review_population: str,
        summary_scope: str,
        student_count: int | None = None,
    ) -> None:
        mapping_status = None
        if review_population == "ttool_ai" and pred_output_path is not None:
            if summary_scope == "run":
                mapping_status = (
                    "Public repo exposes one XML artifact per case, but not distinct per-test outputs."
                )
            else:
                mapping_status = (
                    "Public repo exposes one XML artifact per case, but not the full set of artifacts behind "
                    "aggregate score rows."
                )
        rows.append(
            {
                "paper_slug": "ttool-ai",
                "paper_title": PAPER_TITLES["ttool-ai"],
                "record_source": str(source_path),
                "record_type": record_type,
                "review_record_id": review_record_id,
                "case_id": case_id,
                "case_name": case_name,
                "split_name": split_name,
                "review_target": review_target,
                "review_index": review_index,
                "input_text": input_text,
                "ref_output_text": None,
                "ref_output_format": None,
                "ref_output_artifact_path": None,
                "pred_output_text": pred_output_text,
                "pred_output_format": pred_output_format,
                "pred_output_artifact_path": pred_output_path,
                "human_review_score": human_review_score,
                "human_review_score_unit": "/100",
                "human_review_summary": (
                    "Grade row copied verbatim from the public results.ods sheet."
                    if summary_scope == "run"
                    else "Aggregate score row copied verbatim from the public results.ods sheet."
                ),
                "human_review_details_json": json_compact(
                    {
                        "elapsed_seconds": elapsed_s,
                        "statistic_kind": statistic_kind,
                        "review_population": review_population,
                        "summary_scope": summary_scope,
                        "student_count": student_count,
                        "mapping_status": mapping_status,
                    }
                ),
                "human_review_source_record_json": ods_verbatim_row_payload(
                    source_path=source_path,
                    sheet_name=sheet_name,
                    row_label=row_label,
                    header_row=header_row,
                    raw_row=raw_row,
                    row_index=row_idx,
                    header_row_index=header_row_idx,
                ),
                "human_review_original_text": raw_ods_row_text(raw_row),
                "human_review_original_text_json": json_compact(
                    [
                        {
                            "source_kind": "ods_row",
                            "sheet_name": sheet_name,
                            "row_index_0_based": row_idx,
                            "header_row_index_0_based": header_row_idx,
                            "row_label": row_label,
                            "text": raw_ods_row_text(raw_row),
                            "verbatim_extracted": True,
                        }
                    ]
                ),
                "paper_method_verbatim_excerpt": paper_excerpt_text,
                "paper_method_verbatim_excerpt_json": paper_excerpt_json,
                "verbatim_extraction_verified": True,
                "review_rubric_text": (
                    "Specification adequacy, behavior consistency under TTool simulator, "
                    "exchange richness, readability, number/naming of blocks and states, "
                    "unused attributes, and syntax-checker errors/warnings."
                ),
                "public_artifact_limitations": (
                    "主结果表公开了测试级与汇总级分数，但没有公开每次测试的独立输出版本，"
                    "学生分数也只给了 cohort 统计。"
                ),
            }
        )

    for sheet_name, case_id in sheet_case_map.items():
        table = tables.get(sheet_name, [])
        case_model = model_lookup.get(case_id, {})
        input_text = case_model.get("input_spec_text")
        pred_output_text = case_model.get("raw_xml")
        pred_output_path = case_model.get("xml_path")
        header_row_idx = next(
            (
                idx
                for idx, row in enumerate(table)
                if any(normalize_text(cell) == "Test" for cell in row if cell is not None)
            ),
            None,
        )
        if header_row_idx is None:
            continue
        header_row = table[header_row_idx]
        student_header_idx = next(
            (
                idx
                for idx in range(header_row_idx + 1, len(table))
                if (row_value(table[idx], 1) or "").startswith("Students:")
            ),
            None,
        )

        run_rows_end = student_header_idx if student_header_idx is not None else len(table)
        for row_idx in range(header_row_idx + 1, run_rows_end):
            raw_row = table[row_idx]
            label = row_value(raw_row, 1)
            if label is None:
                continue
            time_bd = normalize_number(row_value(raw_row, 2))
            grade_bd = normalize_number(row_value(raw_row, 3))
            time_smd = normalize_number(row_value(raw_row, 4))
            grade_smd = normalize_number(row_value(raw_row, 5))
            if re.fullmatch(r"\d+", label):
                test_index = int(label)
                for review_target, grade, elapsed_s in (
                    ("BD", grade_bd, time_bd),
                    ("SMD", grade_smd, time_smd),
                ):
                    append_main_record(
                        sheet_name=sheet_name,
                        case_id=case_id,
                        case_name=case_model.get("case_name"),
                        record_type="summary_level_run_score",
                        review_record_id=f"main:{case_id}:ttool_ai:{review_target}:{test_index}",
                        split_name="main_results",
                        review_target=review_target,
                        review_index=test_index,
                        human_review_score=grade,
                        row_label=label,
                        raw_row=raw_row,
                        row_idx=row_idx,
                        header_row=header_row,
                        header_row_idx=header_row_idx,
                        input_text=input_text,
                        pred_output_text=pred_output_text,
                        pred_output_format="TTool AVATAR XML",
                        pred_output_path=pred_output_path,
                        elapsed_s=elapsed_s,
                        statistic_kind=None,
                        review_population="ttool_ai",
                        summary_scope="run",
                    )
                continue

            statistic_kind = normalize_ttool_stat_label(label)
            if statistic_kind is None:
                continue
            for review_target, grade, elapsed_s in (
                ("BD", grade_bd, time_bd),
                ("SMD", grade_smd, time_smd),
            ):
                if grade is None and elapsed_s is None:
                    continue
                append_main_record(
                    sheet_name=sheet_name,
                    case_id=case_id,
                    case_name=case_model.get("case_name"),
                    record_type="case_aggregate_stat",
                    review_record_id=f"main:{case_id}:ttool_ai:{review_target}:{statistic_kind}",
                    split_name="main_results",
                    review_target=review_target,
                    review_index=None,
                    human_review_score=grade,
                    row_label=label,
                    raw_row=raw_row,
                    row_idx=row_idx,
                    header_row=header_row,
                    header_row_idx=header_row_idx,
                    input_text=input_text,
                    pred_output_text=pred_output_text,
                    pred_output_format="TTool AVATAR XML",
                    pred_output_path=pred_output_path,
                    elapsed_s=elapsed_s,
                    statistic_kind=statistic_kind,
                    review_population="ttool_ai",
                    summary_scope="case",
                )

        if student_header_idx is not None:
            student_header_row = table[student_header_idx]
            student_count_match = re.search(r"Students:\s*(\d+)", row_value(student_header_row, 1) or "")
            student_count = int(student_count_match.group(1)) if student_count_match else None
            for row_idx in range(student_header_idx + 1, len(table)):
                raw_row = table[row_idx]
                label = row_value(raw_row, 1)
                statistic_kind = normalize_ttool_stat_label(label)
                if statistic_kind is None:
                    continue
                time_bd = normalize_number(row_value(raw_row, 2))
                grade_bd = normalize_number(row_value(raw_row, 3))
                time_smd = normalize_number(row_value(raw_row, 4))
                grade_smd = normalize_number(row_value(raw_row, 5))
                for review_target, grade, elapsed_s in (
                    ("BD", grade_bd, time_bd),
                    ("SMD", grade_smd, time_smd),
                ):
                    if grade is None and elapsed_s is None:
                        continue
                    append_main_record(
                        sheet_name=sheet_name,
                        case_id=case_id,
                        case_name=case_model.get("case_name"),
                        record_type="case_aggregate_stat",
                        review_record_id=f"main:{case_id}:students:{review_target}:{statistic_kind}",
                        split_name="main_results",
                        review_target=review_target,
                        review_index=None,
                        human_review_score=grade,
                        row_label=label,
                        raw_row=raw_row,
                        row_idx=row_idx,
                        header_row=student_header_row,
                        header_row_idx=student_header_idx,
                        input_text=input_text,
                        pred_output_text=None,
                        pred_output_format=None,
                        pred_output_path=None,
                        elapsed_s=elapsed_s,
                        statistic_kind=statistic_kind,
                        review_population="students",
                        summary_scope="case",
                        student_count=student_count,
                    )

    overall_table = tables.get("Overall", [])
    overall_sections = {
        "TTool + AI": "ttool_ai",
        "Students": "students",
    }
    for section_label, review_population in overall_sections.items():
        section_idx = next(
            (
                idx
                for idx, row in enumerate(overall_table)
                if row_value(row, 1) == section_label
            ),
            None,
        )
        if section_idx is None:
            continue
        section_row = overall_table[section_idx]
        next_section_idx = min(
            [
                idx
                for idx, row in enumerate(overall_table)
                if idx > section_idx and row_value(row, 1) in overall_sections
            ]
            or [len(overall_table)]
        )
        for row_idx in range(section_idx + 1, next_section_idx):
            raw_row = overall_table[row_idx]
            label = row_value(raw_row, 1)
            statistic_kind = normalize_ttool_stat_label(label)
            if statistic_kind is None:
                continue
            time_bd = normalize_number(row_value(raw_row, 2))
            grade_bd = normalize_number(row_value(raw_row, 3))
            time_smd = normalize_number(row_value(raw_row, 4))
            grade_smd = normalize_number(row_value(raw_row, 5))
            for review_target, grade, elapsed_s in (
                ("BD", grade_bd, time_bd),
                ("SMD", grade_smd, time_smd),
            ):
                if grade is None and elapsed_s is None:
                    continue
                append_main_record(
                    sheet_name="Overall",
                    case_id="overall",
                    case_name="Overall",
                    record_type="overall_aggregate_stat",
                    review_record_id=f"overall:{review_population}:{review_target}:{statistic_kind}",
                    split_name="overall_summary",
                    review_target=review_target,
                    review_index=None,
                    human_review_score=grade,
                    row_label=label,
                    raw_row=raw_row,
                    row_idx=row_idx,
                    header_row=section_row,
                    header_row_idx=section_idx,
                    input_text=None,
                    pred_output_text=None,
                    pred_output_format=None,
                    pred_output_path=None,
                    elapsed_s=elapsed_s,
                    statistic_kind=statistic_kind,
                    review_population=review_population,
                    summary_scope="overall",
                )
    return pd.DataFrame(rows)


def build_ttool_ai_supplementary_review(raw_root: Path) -> pd.DataFrame:
    source_path = raw_root / "ttool-ai" / "SNCS_complementaryEvaluation" / "evaluation.ods"
    paper_excerpt_text, paper_excerpt_json = paper_method_excerpt_bundle("ttool-ai")
    tables = read_ods_tables(source_path)
    case_meta = {
        "connectedDevice": {
            "case_id": "connected_device",
            "case_name": "Connected Device / Pumpkin",
            "spec_path": raw_root / "ttool-ai" / "SNCS_complementaryEvaluation" / "connectedDevice" / "spec2",
            "xml_path": raw_root / "ttool-ai" / "SNCS_complementaryEvaluation" / "connectedDevice" / "pumpkin.xml",
            "properties_dir": raw_root / "ttool-ai" / "SNCS_complementaryEvaluation" / "connectedDevice",
        },
        "packagingChain": {
            "case_id": "packaging_line",
            "case_name": "Packaging Line",
            "spec_path": raw_root / "ttool-ai" / "SNCS_complementaryEvaluation" / "packagingLine" / "spec1",
            "xml_path": raw_root / "ttool-ai" / "SNCS_complementaryEvaluation" / "packagingLine" / "packagingLine.xml",
            "properties_dir": raw_root / "ttool-ai" / "SNCS_complementaryEvaluation" / "packagingLine",
        },
    }
    rows: list[dict[str, Any]] = []
    for sheet_name, meta in case_meta.items():
        table = tables.get(sheet_name, [])
        if not table:
            continue
        input_text = meta["spec_path"].read_text(encoding="utf-8").strip()
        xml_text = meta["xml_path"].read_text(encoding="utf-8")
        header_row_idx = None
        for idx, raw_row in enumerate(table):
            normalized_row = [normalize_text(cell) for cell in raw_row]
            if normalized_row and any(cell == "Ttool-AI" for cell in normalized_row if cell):
                header_row_idx = idx
                break
        if header_row_idx is None or header_row_idx == 0:
            continue
        group_row = table[header_row_idx - 1]
        header_row = table[header_row_idx]
        ttool_columns: list[tuple[int, str]] = []
        for col_idx, cell in enumerate(header_row):
            if normalize_text(cell) != "Ttool-AI":
                continue
            dimension = None
            for search_idx in range(col_idx, -1, -1):
                candidate = row_value(group_row, search_idx)
                if candidate:
                    dimension = candidate
                    break
            if dimension is None:
                continue
            ttool_columns.append((col_idx, dimension))

        for row_idx, raw_row in enumerate(table[header_row_idx + 1 :], start=header_row_idx + 1):
            first_cell = row_value(raw_row, 0)
            if first_cell in {"Average", "Std Dev", "Std dev"}:
                record_type = "summary"
                review_index = None
            elif first_cell is None and any(normalize_text(row_value(raw_row, col)) for col, _ in ttool_columns):
                record_type = "raw_score_row"
                review_index = sum(
                    1 for existing in rows
                    if existing["paper_slug"] == "ttool-ai"
                    and existing.get("split_name") == "sncs_complementary"
                    and existing.get("case_id") == meta["case_id"]
                    and existing["record_type"] == "raw_score_row"
                ) // max(len(ttool_columns), 1) + 1
            else:
                continue

            for col_idx, dimension in ttool_columns:
                score = normalize_number(row_value(raw_row, col_idx))
                if score is None:
                    continue
                properties_path = (
                    meta["properties_dir"] / f"properties{review_index}.md"
                    if record_type == "raw_score_row" and review_index is not None
                    else None
                )
                pred_output_text = (
                    properties_path.read_text(encoding="utf-8").strip()
                    if dimension == "Properties"
                    and properties_path is not None
                    and properties_path.exists()
                    else xml_text
                )
                pred_output_path = (
                    str(properties_path)
                    if dimension == "Properties"
                    and properties_path is not None
                    and properties_path.exists()
                    else str(meta["xml_path"])
                )
                pred_output_format = "Markdown property proposals" if dimension == "Properties" else "TTool XML"
                rows.append(
                    {
                        "paper_slug": "ttool-ai",
                        "paper_title": PAPER_TITLES["ttool-ai"],
                        "record_source": str(source_path),
                        "record_type": record_type,
                        "review_record_id": f"sncs:{meta['case_id']}:{dimension}:{first_cell or review_index}",
                        "case_id": meta["case_id"],
                        "case_name": meta["case_name"],
                        "split_name": "sncs_complementary",
                        "review_target": dimension,
                        "review_index": review_index,
                        "input_text": input_text,
                        "ref_output_text": None,
                        "ref_output_format": None,
                        "ref_output_artifact_path": None,
                        "pred_output_text": pred_output_text,
                        "pred_output_format": pred_output_format,
                        "pred_output_artifact_path": pred_output_path,
                        "human_review_score": score,
                        "human_review_score_unit": "/10",
                        "human_review_summary": "Supplementary human score from the public SNCS complementary evaluation sheet.",
                        "human_review_details_json": json_compact(
                            {
                                "summary_label": first_cell,
                                "row_semantics_documented": False,
                            }
                        ),
                        "human_review_source_record_json": ods_verbatim_row_payload(
                            source_path=source_path,
                            sheet_name=sheet_name,
                            row_label=first_cell,
                            header_row=header_row,
                            raw_row=raw_row,
                            row_index=row_idx,
                            header_row_index=header_row_idx,
                            extra_rows={
                                "group_row": group_row,
                            },
                            extra_row_indexes={
                                "group_row": header_row_idx - 1,
                            },
                        ),
                        "human_review_original_text": raw_ods_row_text(raw_row),
                        "human_review_original_text_json": json_compact(
                            [
                                {
                                    "source_kind": "ods_row",
                                    "sheet_name": sheet_name,
                                    "row_index_0_based": row_idx,
                                    "header_row_index_0_based": header_row_idx,
                                    "row_label": first_cell,
                                    "text": raw_ods_row_text(raw_row),
                                    "verbatim_extracted": True,
                                }
                            ]
                        ),
                        "paper_method_verbatim_excerpt": paper_excerpt_text,
                        "paper_method_verbatim_excerpt_json": paper_excerpt_json,
                        "verbatim_extraction_verified": True,
                        "review_rubric_text": (
                            "仓库只公开了分数字段，没有在主论文中解释该补充表的逐行评审组织方式；"
                            "因此仅保留原始分数，不对 row-level 语义做额外推断。"
                        ),
                        "public_artifact_limitations": (
                            "补充评估表逐行含义未在论文正文详细说明，UCD/BD/SMD 也没有分 run 独立 XML。"
                        ),
                    }
                )
    return pd.DataFrame(rows)


def build_ttool_ai_human_review(raw_root: Path) -> pd.DataFrame:
    models_df = base.build_ttool_ai(raw_root)["ttool_ai_models"]
    main_df = build_ttool_ai_main_review(raw_root, models_df)
    supplementary_df = build_ttool_ai_supplementary_review(raw_root)
    return pd.concat([main_df, supplementary_df], ignore_index=True, sort=False)


def build_availability_catalog(
    llms_df: pd.DataFrame,
    ttool_df: pd.DataFrame,
    structure_df: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "paper_slug": "llms_emp",
                "paper_title": PAPER_TITLES["llms_emp"],
                "public_human_review_status": "sample_level_available",
                "extracted_record_count": int(len(llms_df)),
                "raw_artifact_path": str(RAW_ROOT_DEFAULT / "llms_emp_gmodel" / "Experiment Results.xlsx"),
                "input_available": True,
                "reference_output_available": True,
                "prediction_available": True,
                "notes": "公开结果表含逐样本 input / ref / pred 与人工语法/语义评审结果。",
            },
            {
                "paper_slug": "ttool-ai",
                "paper_title": PAPER_TITLES["ttool-ai"],
                "public_human_review_status": "summary_only_available",
                "extracted_record_count": int(len(ttool_df)),
                "raw_artifact_path": str(RAW_ROOT_DEFAULT / "ttool-ai" / "results.ods"),
                "input_available": True,
                "reference_output_available": False,
                "prediction_available": True,
                "notes": "公开包保留了规格、XML 与分数，但没有逐次测试的独立输出版本或 gold reference。",
            },
            {
                "paper_slug": "requirements-capture-and-evaluation-in-nimbus-light-control",
                "paper_title": PAPER_TITLES["requirements-capture-and-evaluation-in-nimbus-light-control"],
                "public_human_review_status": "method_only_no_raw_scores",
                "extracted_record_count": 0,
                "raw_artifact_path": str(RAW_ROOT_DEFAULT / "light-case-jucs.pdf"),
                "input_available": True,
                "reference_output_available": True,
                "prediction_available": False,
                "notes": "公开的是案例和方法，不是 LLM 输出评分表；可复原人工/形式化/仿真三联 V&V 流程，但无逐样本分数。",
            },
            {
                "paper_slug": "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models",
                "paper_title": PAPER_TITLES[
                    "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models"
                ],
                "public_human_review_status": "sample_level_available",
                "extracted_record_count": int(len(structure_df)),
                "raw_artifact_path": str(RAW_ROOT_DEFAULT / "llm_state_machine_final_f1_scores.xlsx"),
                "input_available": True,
                "reference_output_available": True,
                "prediction_available": True,
                "notes": "公开了逐组件 TP/FN/FP/F1 和预测图像；大多数预测的文本版 Umple 未公开。",
            },
        ]
    )


def build_combined_records(
    llms_df: pd.DataFrame,
    ttool_df: pd.DataFrame,
    structure_df: pd.DataFrame,
) -> pd.DataFrame:
    common_columns = [
        "paper_slug",
        "paper_title",
        "record_source",
        "record_type",
        "review_record_id",
        "case_id",
        "case_name",
        "split_name",
        "sheet_name",
        "diagram_type",
        "strategy_name",
        "llm_name",
        "review_target",
        "review_index",
        "component",
        "input_text",
        "ref_output_text",
        "ref_output_format",
        "ref_output_artifact_path",
        "pred_output_text",
        "pred_output_format",
        "pred_output_artifact_path",
        "human_review_score",
        "human_review_score_unit",
        "human_review_summary",
        "human_review_details_json",
        "human_review_source_record_json",
        "human_review_original_text",
        "human_review_original_text_json",
        "paper_method_verbatim_excerpt",
        "paper_method_verbatim_excerpt_json",
        "verbatim_extraction_verified",
        "review_rubric_text",
        "public_artifact_limitations",
    ]
    frames = []
    for frame in (llms_df, ttool_df, structure_df):
        prepared = frame.copy()
        for column in common_columns:
            if column not in prepared.columns:
                prepared[column] = None
        frames.append(prepared[common_columns])
    return pd.concat(frames, ignore_index=True, sort=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", type=Path, default=RAW_ROOT_DEFAULT)
    parser.add_argument("--output-dir", type=Path, default=ASSET_DIR)
    args = parser.parse_args()

    llms_df = build_llms_emp_human_review(args.raw_root)
    ttool_df = build_ttool_ai_human_review(args.raw_root)
    structure_df = build_structure_event_human_review(args.raw_root)
    protocols_df = build_protocols()
    availability_df = build_availability_catalog(llms_df, ttool_df, structure_df)
    combined_df = build_combined_records(llms_df, ttool_df, structure_df)

    outputs = {
        "llms_emp_human_review": llms_df,
        "ttool_ai_human_review": ttool_df,
        "structure_event_driven_human_review": structure_df,
        "baseline_double_green_human_review_protocols": protocols_df,
        "baseline_double_green_human_review_availability": availability_df,
        "baseline_double_green_human_review_records": combined_df,
    }

    for name, frame in outputs.items():
        write_parquet(frame, args.output_dir / f"{name}.parquet")

    summary = {name: {"rows": int(len(frame)), "columns": list(frame.columns)} for name, frame in outputs.items()}
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
