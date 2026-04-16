#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return None
    if float(number).is_integer():
        return int(number)
    return float(number)


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
    return (
        Path("/home/hansbug/oo-projects/research_ideas-2")
        / "project_1_llm_state_machine_modeling"
        / "baselines"
        / slug
    )


def build_protocols() -> pd.DataFrame:
    rows = [
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
        },
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
        },
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
        },
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
        },
    ]
    return pd.DataFrame(rows)


def build_llms_emp_human_review(raw_root: Path) -> pd.DataFrame:
    workbook = raw_root / "llms_emp_gmodel" / "Experiment Results.xlsx"
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
    frames = base.build_structure_event_driven(raw_root)
    cases_df = frames["structure_event_driven_cases"].copy()
    refs_df = frames["structure_event_driven_reference_solutions"].copy()
    metrics_df = frames["structure_event_driven_metrics"].copy()
    output_index = build_structure_event_output_index(raw_root)

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
        rows.append(
            {
                "paper_slug": "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models",
                "paper_title": PAPER_TITLES[
                    "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models"
                ],
                "record_source": str(raw_root / "llm_state_machine_final_f1_scores.xlsx"),
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
    tables = read_ods_tables(raw_root / "ttool-ai" / "results.ods")
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
    for sheet_name, case_id in sheet_case_map.items():
        table = tables.get(sheet_name, [])
        case_model = model_lookup.get(case_id, {})
        input_text = case_model.get("input_spec_text")
        pred_output_text = case_model.get("raw_xml")
        pred_output_path = case_model.get("xml_path")
        for raw_row in table:
            label = row_value(raw_row, 1)
            if label is None or not re.fullmatch(r"\d+", label):
                continue
            test_index = int(label)
            time_bd = normalize_number(row_value(raw_row, 2))
            grade_bd = normalize_number(row_value(raw_row, 3))
            time_smd = normalize_number(row_value(raw_row, 4))
            grade_smd = normalize_number(row_value(raw_row, 5))
            for review_target, grade, elapsed_s in (
                ("BD", grade_bd, time_bd),
                ("SMD", grade_smd, time_smd),
            ):
                rows.append(
                    {
                        "paper_slug": "ttool-ai",
                        "paper_title": PAPER_TITLES["ttool-ai"],
                        "record_source": str(raw_root / "ttool-ai" / "results.ods"),
                        "record_type": "summary_level_run_score",
                        "review_record_id": f"main:{case_id}:{review_target}:{test_index}",
                        "case_id": case_id,
                        "case_name": case_model.get("case_name"),
                        "split_name": "main_results",
                        "review_target": review_target,
                        "review_index": test_index,
                        "input_text": input_text,
                        "ref_output_text": None,
                        "ref_output_format": None,
                        "ref_output_artifact_path": None,
                        "pred_output_text": pred_output_text,
                        "pred_output_format": "TTool AVATAR XML",
                        "pred_output_artifact_path": pred_output_path,
                        "human_review_score": grade,
                        "human_review_score_unit": "/100",
                        "human_review_summary": "Grade assigned with shared software-engineering quality criteria.",
                        "human_review_details_json": json_compact(
                            {
                                "elapsed_seconds": elapsed_s,
                                "mapping_status": (
                                    "Public repo exposes one XML artifact per case, but not distinct per-test outputs."
                                ),
                            }
                        ),
                        "review_rubric_text": (
                            "Specification adequacy, behavior consistency under TTool simulator, "
                            "exchange richness, readability, number/naming of blocks and states, "
                            "unused attributes, and syntax-checker errors/warnings."
                        ),
                        "public_artifact_limitations": (
                            "主结果表只有测试级分数与时间，没有逐次输出版本，因此分数无法和独立测试产物一一精确绑定。"
                        ),
                    }
                )
    return pd.DataFrame(rows)


def build_ttool_ai_supplementary_review(raw_root: Path) -> pd.DataFrame:
    tables = read_ods_tables(raw_root / "ttool-ai" / "SNCS_complementaryEvaluation" / "evaluation.ods")
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

        for raw_row in table[header_row_idx + 1 :]:
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
                        "record_source": str(
                            raw_root / "ttool-ai" / "SNCS_complementaryEvaluation" / "evaluation.ods"
                        ),
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
