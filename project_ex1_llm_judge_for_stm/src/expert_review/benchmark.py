from __future__ import annotations

import argparse
from collections import defaultdict
import json
import math
import random
import statistics
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd

from .agent import ExpertReviewAgent
from .schema import ExpertReviewRequest, ExpertReviewResult, judgement_from_score
from .utils import DEFAULT_MODEL


DEFAULT_BENCHMARK_DIR = Path(
    "project_1_llm_state_machine_modeling/discussions/"
    "2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets"
)

ISSUE_TAXONOMY = [
    "syntax_or_notation",
    "missing_required_behavior",
    "wrong_guard_or_trigger",
    "wrong_action_or_effect",
    "unsupported_extra_structure",
    "equivalence_misjudgement",
    "readability_or_naming",
    "unused_or_noisy_structure",
    "evidence_overreach",
]
CRITICAL_ISSUE_TAXONOMY = (
    "syntax_or_notation",
    "missing_required_behavior",
    "wrong_guard_or_trigger",
    "wrong_action_or_effect",
    "unsupported_extra_structure",
)
JUDGEMENT_LABELS = ("poor", "weak", "acceptable", "good", "excellent")

RECORD_LEVEL_RECORD_TYPES = {"sample_level_review"}
SUMMARY_LEVEL_RECORD_TYPES = {"summary_level_run_score", "case_aggregate_stat", "raw_score_row", "summary"}
COMPONENT_LEVEL_RECORD_TYPES = {"component_level_review"}
SPLIT_ORDER = ("train", "dev", "validation", "lockbox")
DEFAULT_SPLIT_RATIOS = {
    "train": 0.50,
    "dev": 0.20,
    "validation": 0.15,
    "lockbox": 0.15,
}
PHASE14_CORE_METRICS = ("HAI", "RAS", "SAS", "CRAS", "PDS")
PHASE14_LOCKBOX_MAX_DEGRADE = 4.0
PHASE7_ERROR_BUCKETS = (
    "contract_understanding_error",
    "element_extraction_error",
    "equivalence_reasoning_error",
    "quality_judgement_error",
    "evidence_discipline_error",
    "calibration_error",
)
COMPONENT_TARGETS = (
    "States",
    "Transitions",
    "Guards",
    "Actions",
    "Hierarchical states",
    "Parallel Regions",
    "History States",
    "All",
)
MAJOR_COMPONENT_TARGETS = tuple(item for item in COMPONENT_TARGETS if item != "All")
COMPONENT_COUNT_TOTAL_FIELDS = {
    "States": "component_reference_total",
    "Transitions": "component_reference_total",
    "Guards": "component_reference_total",
    "Actions": "component_reference_total",
    "Hierarchical states": "component_reference_total",
    "Parallel Regions": "component_reference_total",
    "History States": "component_reference_total",
    "All": "component_reference_total",
}
COMPONENT_REFERENCE_TEXT_ROOTS = (
    Path("/tmp/baseline_double_green/raw/llm_state_machine_modeling_repo/Paper Experiment Resources/Reference Solutions"),
    Path("/tmp/baseline_double_green/raw/llm_state_machine_modeling/Paper Experiment Resources/Reference Solutions"),
)


@dataclass(slots=True)
class BenchmarkTask:
    task_id: str
    eval_bucket: str
    regime_expected: str
    prompt: str
    input_text: str
    pred_output: str
    ref_output: str | None
    human_score: float | None
    human_score_unit: str | None
    human_issue_set: set[str]
    group_key: str
    metadata: dict[str, Any]


def _stable_token(value: Any, *, fallback: str = "na") -> str:
    text = _safe_text(value).strip()
    if not text:
        return fallback
    return text.replace("\n", " ").strip()


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round(0.95 * (len(ordered) - 1))))
    return ordered[index]


def _family_key_for_record_row(row: pd.Series) -> str:
    paper_slug = _stable_token(row.get("paper_slug"), fallback="paper")
    record_type = _stable_token(row.get("record_type"), fallback="record")
    case_id = _stable_token(row.get("case_id"))
    case_name = _stable_token(row.get("case_name"))
    diagram_type = _stable_token(row.get("diagram_type"))
    llm_name = _stable_token(row.get("llm_name"))
    review_target = _stable_token(row.get("review_target"), fallback="target")

    if record_type in RECORD_LEVEL_RECORD_TYPES:
        family_parts = [paper_slug]
        if case_id != "na":
            family_parts.append(case_id)
        elif case_name != "na":
            family_parts.append(case_name)
        if diagram_type != "na":
            family_parts.append(diagram_type)
        if llm_name != "na":
            family_parts.append(llm_name)
        return "::".join(family_parts)

    if record_type in SUMMARY_LEVEL_RECORD_TYPES:
        family_parts = [paper_slug]
        if case_id != "na":
            family_parts.append(case_id)
        elif case_name != "na":
            family_parts.append(case_name)
        else:
            family_parts.append(_stable_token(row.get("split_name"), fallback="summary"))
        family_parts.append(review_target)
        return "::".join(family_parts)

    if record_type in COMPONENT_LEVEL_RECORD_TYPES:
        family_parts = [paper_slug]
        if case_id != "na":
            family_parts.append(case_id)
        elif case_name != "na":
            family_parts.append(case_name)
        if llm_name != "na":
            family_parts.append(llm_name)
        return "::".join(family_parts)

    return "::".join([paper_slug, review_target, record_type])


def _family_key_for_protocol_row(row: pd.Series) -> str:
    return _stable_token(row.get("paper_slug"), fallback="protocol")


def _prepare_record_level_pool(records: pd.DataFrame) -> pd.DataFrame:
    df = records[
        records["record_type"].isin(RECORD_LEVEL_RECORD_TYPES)
        & records["pred_output_text"].notna()
        & records["input_text"].notna()
        & records["ref_output_text"].notna()
    ].copy()
    if not df.empty:
        df["family_key"] = df.apply(_family_key_for_record_row, axis=1)
    return df


def _prepare_summary_level_pool(records: pd.DataFrame) -> pd.DataFrame:
    df = records[
        records["record_type"].isin(SUMMARY_LEVEL_RECORD_TYPES)
        & records["pred_output_text"].notna()
    ].copy()
    if not df.empty:
        df["family_key"] = df.apply(_family_key_for_record_row, axis=1)
    return df


def _safe_json_dict(value: Any) -> dict[str, Any]:
    text = _safe_text(value).strip()
    if not text:
        return {}
    try:
        payload = json.loads(text)
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _safe_json_list(value: Any) -> list[Any]:
    text = _safe_text(value).strip()
    if not text:
        return []
    try:
        payload = json.loads(text)
    except Exception:
        return []
    return payload if isinstance(payload, list) else []


def _safe_float(value: Any) -> float | None:
    try:
        score = float(value)
    except Exception:
        return None
    if math.isnan(score):
        return None
    return score


def _safe_int(value: Any) -> int | None:
    score = _safe_float(value)
    if score is None:
        return None
    try:
        return int(score)
    except Exception:
        return None


def _component_f1_from_counts(tp: int | None, fp: int | None, fn: int | None) -> float | None:
    if tp is None or fp is None or fn is None:
        return None
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return 0.0 if precision + recall == 0 else (2 * precision * recall) / (precision + recall)


@lru_cache(maxsize=128)
def _reference_solution_text_by_basename(basename: str) -> str:
    if not basename:
        return ""
    txt_name = Path(basename).with_suffix(".txt").name
    for root in COMPONENT_REFERENCE_TEXT_ROOTS:
        candidate = root / txt_name
        if candidate.exists():
            return candidate.read_text(encoding="utf-8").strip()
    return ""


def _hydrate_component_public_evidence(row: pd.Series) -> dict[str, Any]:
    details = _safe_json_dict(row.get("human_review_details_json"))
    source = _safe_json_dict(row.get("human_review_source_record_json"))
    original = _safe_json_list(row.get("human_review_original_text_json"))
    public_row_text = ""
    if original and isinstance(original[0], dict):
        public_row_text = _safe_text(original[0].get("text")).strip()
    component_target = _safe_text(row.get("review_target") or row.get("component")).strip() or "Unknown"
    tp = _safe_int(details.get("tp"))
    fn = _safe_int(details.get("fn"))
    fp = _safe_int(details.get("fp"))
    explicit_human_score = _normalize_score(row.get("human_review_score"), row.get("human_review_score_unit"))
    detail_human_score = _normalize_score(details.get("f1_score"), "f1")
    derived_human_score = _component_f1_from_counts(tp, fp, fn)
    human_score = explicit_human_score
    human_score_source = "human_review_score"
    if human_score is None and detail_human_score is not None:
        human_score = detail_human_score
        human_score_source = "details_f1_score"
    elif human_score is None and derived_human_score is not None:
        human_score = derived_human_score
        human_score_source = "derived_from_counts"
    elif human_score is None:
        human_score_source = "missing"
    if human_score is not None:
        human_score = round(human_score, 6)
    public_counts_complete = tp is not None and fp is not None and fn is not None
    main_eval_eligible = public_counts_complete and human_score is not None
    if main_eval_eligible:
        evidence_status = "structured_counts_available"
    elif human_score is not None:
        evidence_status = "score_only_without_structured_counts"
    else:
        evidence_status = "missing_public_score_and_counts"
    image_reference = _safe_text(source.get("image_reference_raw") or source.get("image_reference")).strip()
    ref_basename = Path(_safe_text(row.get("ref_output_artifact_path"))).name
    ref_text = _safe_text(row.get("ref_output_text")).strip() or _reference_solution_text_by_basename(ref_basename)
    system_name = _safe_text(source.get("system_name_normalized") or row.get("case_name")).strip()
    strategy_name = _safe_text(source.get("strategy_name") or row.get("strategy_name")).strip()
    llm_name = _safe_text(source.get("llm_name") or row.get("llm_name")).strip()
    return {
        "component_target": component_target,
        "component_public_tp": tp,
        "component_public_fn": fn,
        "component_public_fp": fp,
        "component_pred_total": None if tp is None or fp is None else tp + fp,
        "component_reference_total": None if tp is None or fn is None else tp + fn,
        "component_human_score": human_score,
        "component_human_score_source": human_score_source,
        "component_public_counts_complete": public_counts_complete,
        "component_main_eval_eligible": main_eval_eligible,
        "component_evidence_status": evidence_status,
        "component_public_row_text": public_row_text,
        "component_public_image_reference": image_reference,
        "component_source_kind": _safe_text(source.get("source_kind")).strip() or "xlsx_row",
        "component_sheet_name": _safe_text(source.get("sheet_name") or row.get("sheet_name")).strip(),
        "component_system_name": system_name,
        "component_strategy_name": strategy_name,
        "component_llm_name": llm_name,
        "component_reference_text": ref_text,
    }


def _prepare_component_level_table(records: pd.DataFrame) -> pd.DataFrame:
    df = records[records["record_type"].isin(COMPONENT_LEVEL_RECORD_TYPES)].copy()
    if not df.empty:
        df["family_key"] = df.apply(_family_key_for_record_row, axis=1)
        df["component_bucket"] = df["review_target"].fillna("NA").astype(str)
        public_evidence = [_hydrate_component_public_evidence(row) for _, row in df.iterrows()]
        evidence_df = pd.DataFrame(public_evidence, index=df.index)
        df = pd.concat([df, evidence_df], axis=1)
    return df


def _prepare_component_level_pool(records: pd.DataFrame) -> pd.DataFrame:
    df = _prepare_component_level_table(records)
    if not df.empty:
        df = df[df["component_main_eval_eligible"]].copy()
    return df


def _prepare_protocol_level_pool(protocols: pd.DataFrame) -> pd.DataFrame:
    df = protocols.copy()
    if not df.empty:
        df["family_key"] = df.apply(_family_key_for_protocol_row, axis=1)
    return df


def build_benchmark_inventory(
    records: pd.DataFrame,
    protocols: pd.DataFrame,
    availability: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    component_all = _prepare_component_level_table(records)
    return {
        "records_all": records.copy(),
        "protocols_all": protocols.copy(),
        "availability_all": availability.copy(),
        "record_level": _prepare_record_level_pool(records),
        "summary_level": _prepare_summary_level_pool(records),
        "component_level_all": component_all,
        "component_level": component_all[component_all["component_main_eval_eligible"]].copy() if not component_all.empty else component_all,
        "protocol_only": _prepare_protocol_level_pool(protocols),
    }


def _counts_dict(series: pd.Series) -> dict[str, int]:
    return {str(key): int(value) for key, value in series.fillna("NA").value_counts().to_dict().items()}


def build_component_alignment_schema(component_df: pd.DataFrame) -> dict[str, Any]:
    if component_df.empty:
        return {
            "rows": 0,
            "family_count": 0,
            "canonical_components": [],
            "score_unit_counts": {},
            "paper_counts": {},
            "llm_counts": {},
            "source_kind_counts": {},
            "family_key_rule": "paper_slug::case_id::llm_name",
        }
    return {
        "rows": int(len(component_df)),
        "family_count": int(component_df["family_key"].nunique()),
        "canonical_components": sorted({str(item) for item in component_df["component_bucket"].dropna().tolist()}),
        "score_unit_counts": _counts_dict(component_df["human_review_score_unit"]),
        "paper_counts": _counts_dict(component_df["paper_slug"]),
        "llm_counts": _counts_dict(component_df["llm_name"]),
        "source_kind_counts": _counts_dict(component_df["component_source_kind"]) if "component_source_kind" in component_df else {},
        "case_count": int(component_df["case_id"].fillna(component_df["case_name"]).nunique()),
        "family_key_rule": "paper_slug::case_id::llm_name",
    }


def summarize_benchmark_coverage(
    records: pd.DataFrame,
    protocols: pd.DataFrame,
    availability: pd.DataFrame,
) -> dict[str, Any]:
    inventory = build_benchmark_inventory(records, protocols, availability)
    record_df = inventory["record_level"]
    summary_df = inventory["summary_level"]
    component_all_df = inventory["component_level_all"]
    component_df = inventory["component_level"]
    protocol_df = inventory["protocol_only"]
    deferred_component_rows = int(len(component_all_df) - len(component_df))

    coverage_gaps: list[str] = []
    if record_df["paper_slug"].nunique() <= 1:
        coverage_gaps.append("record-level 强对齐当前主要集中在单个 paper family，外推性不足。")
    if summary_df["paper_slug"].nunique() <= 1:
        coverage_gaps.append("summary-level 当前主要集中在单个 paper family，排序口径覆盖仍偏窄。")
    if deferred_component_rows:
        coverage_gaps.append(
            f"component_level_review 中有 {deferred_component_rows} 行缺少完整 TP/FP/FN structured public evidence；"
            "在当前非视觉、禁止答案回灌的口径下，这部分仍保留为 deferred。"
        )
    if len(protocol_df) <= 4:
        coverage_gaps.append("protocol-only benchmark 样本数仍较小，应保守解释 protocol discipline 的泛化性。")

    return {
        "table_rows": {
            "records_all": int(len(records)),
            "protocols_all": int(len(protocols)),
            "availability_all": int(len(availability)),
        },
        "main_eval_rows": {
            "record": int(len(record_df)),
            "summary": int(len(summary_df)),
            "component": int(len(component_df)),
            "protocol": int(len(protocol_df)),
        },
        "deferred_rows": {
            "component": deferred_component_rows,
        },
        "family_counts": {
            "record": int(record_df["family_key"].nunique()) if not record_df.empty else 0,
            "summary": int(summary_df["family_key"].nunique()) if not summary_df.empty else 0,
            "protocol": int(protocol_df["family_key"].nunique()) if not protocol_df.empty else 0,
            "component": int(component_df["family_key"].nunique()) if not component_df.empty else 0,
        },
        "paper_coverage": {
            "record": _counts_dict(record_df["paper_slug"]) if not record_df.empty else {},
            "summary": _counts_dict(summary_df["paper_slug"]) if not summary_df.empty else {},
            "protocol": _counts_dict(protocol_df["paper_slug"]) if not protocol_df.empty else {},
            "component": _counts_dict(component_df["paper_slug"]) if not component_df.empty else {},
        },
        "granularity": {
            "record_record_type_counts": _counts_dict(record_df["record_type"]) if not record_df.empty else {},
            "record_diagram_type_counts": _counts_dict(record_df["diagram_type"]) if not record_df.empty else {},
            "record_llm_counts": _counts_dict(record_df["llm_name"]) if not record_df.empty else {},
            "summary_record_type_counts": _counts_dict(summary_df["record_type"]) if not summary_df.empty else {},
            "summary_target_counts": _counts_dict(summary_df["review_target"]) if not summary_df.empty else {},
            "protocol_status_counts": _counts_dict(protocol_df["public_human_review_status"]) if not protocol_df.empty else {},
        },
        "component_alignment_schema": build_component_alignment_schema(component_df),
        "availability_status": {
            "public_human_review_status": _counts_dict(availability["public_human_review_status"])
            if "public_human_review_status" in availability
            else {},
        },
        "coverage_gaps": coverage_gaps,
    }


def _rows_to_tasks(regime_name: str, df: pd.DataFrame) -> list[BenchmarkTask]:
    if df.empty:
        return []
    if regime_name == "record":
        return [_build_record_task(row) for _, row in df.iterrows()]
    if regime_name == "summary":
        return [_build_summary_task(row) for _, row in df.iterrows()]
    if regime_name == "protocol":
        return [_build_protocol_task(row) for _, row in df.iterrows()]
    if regime_name == "component":
        return [_build_component_task(row) for _, row in df.iterrows()]
    raise ValueError(f"Unsupported regime_name: {regime_name}")


def _family_split_assignments(
    df: pd.DataFrame,
    *,
    seed: int,
    split_ratios: dict[str, float] | None = None,
) -> dict[str, set[str]]:
    assignments = {split: set() for split in SPLIT_ORDER}
    if df.empty or "family_key" not in df:
        return assignments

    ratios = dict(DEFAULT_SPLIT_RATIOS if split_ratios is None else split_ratios)
    family_rows = (
        df.groupby("family_key", dropna=False)
        .size()
        .reset_index(name="row_count")
        .sample(frac=1.0, random_state=seed)
        .sort_values("row_count", ascending=False, kind="stable")
        .to_dict("records")
    )
    if not family_rows:
        return assignments

    current_rows = {split: 0 for split in SPLIT_ORDER}
    target_rows = {split: max(1.0, ratios.get(split, 0.0) * len(df)) for split in SPLIT_ORDER}

    if len(family_rows) >= len(SPLIT_ORDER):
        for split, family in zip(SPLIT_ORDER, family_rows[: len(SPLIT_ORDER)]):
            assignments[split].add(str(family["family_key"]))
            current_rows[split] += int(family["row_count"])
        family_rows = family_rows[len(SPLIT_ORDER) :]

    for family in family_rows:
        family_key = str(family["family_key"])
        row_count = int(family["row_count"])
        chosen_split = min(
            SPLIT_ORDER,
            key=lambda split: (
                current_rows[split] / target_rows[split],
                current_rows[split],
                len(assignments[split]),
                split,
            ),
        )
        assignments[chosen_split].add(family_key)
        current_rows[chosen_split] += row_count
    return assignments


def build_benchmark_split_bundle(
    records: pd.DataFrame,
    protocols: pd.DataFrame,
    availability: pd.DataFrame,
    *,
    seed: int = 7,
    split_ratios: dict[str, float] | None = None,
) -> dict[str, Any]:
    inventory = build_benchmark_inventory(records, protocols, availability)
    regime_frames = {
        "record": inventory["record_level"],
        "summary": inventory["summary_level"],
        "component": inventory["component_level"],
        "protocol": inventory["protocol_only"],
    }
    split_frames: dict[str, dict[str, pd.DataFrame]] = {split: {} for split in SPLIT_ORDER}
    manifest: dict[str, Any] = {"ratios": dict(DEFAULT_SPLIT_RATIOS if split_ratios is None else split_ratios), "regimes": {}}

    for offset, (regime_name, frame) in enumerate(regime_frames.items()):
        assignments = _family_split_assignments(frame, seed=seed + offset, split_ratios=split_ratios)
        manifest["regimes"][regime_name] = {}
        for split in SPLIT_ORDER:
            family_keys = assignments[split]
            subset = frame[frame["family_key"].isin(family_keys)].copy() if family_keys else frame.iloc[0:0].copy()
            split_frames[split][regime_name] = subset
            manifest["regimes"][regime_name][split] = {
                "rows": int(len(subset)),
                "family_count": int(subset["family_key"].nunique()) if not subset.empty else 0,
                "family_keys": sorted(str(item) for item in family_keys),
            }

    return {
        "task_bundles": {
            split: {
                "record": _rows_to_tasks("record", split_frames[split]["record"]),
                "summary": _rows_to_tasks("summary", split_frames[split]["summary"]),
                "component": _rows_to_tasks("component", split_frames[split]["component"]),
                "protocol": _rows_to_tasks("protocol", split_frames[split]["protocol"]),
            }
            for split in SPLIT_ORDER
        },
        "manifest": manifest,
    }


def build_lofo_task_bundles(
    records: pd.DataFrame,
    protocols: pd.DataFrame,
    availability: pd.DataFrame,
) -> dict[str, Any]:
    inventory = build_benchmark_inventory(records, protocols, availability)
    regime_frames = {
        "record": inventory["record_level"],
        "summary": inventory["summary_level"],
        "component": inventory["component_level"],
        "protocol": inventory["protocol_only"],
    }
    bundles: dict[str, dict[str, list[BenchmarkTask]]] = {}
    manifest: dict[str, Any] = {"families": {}}

    for regime_name, frame in regime_frames.items():
        if frame.empty:
            continue
        for family_key, subset in frame.groupby("family_key", dropna=False):
            namespaced_key = f"{regime_name}::{family_key}"
            bundles[namespaced_key] = {"record": [], "summary": [], "component": [], "protocol": []}
            bundles[namespaced_key][regime_name] = _rows_to_tasks(regime_name, subset)
            manifest["families"][namespaced_key] = {
                "regime": regime_name,
                "family_key": str(family_key),
                "rows": int(len(subset)),
                "paper_slug_counts": _counts_dict(subset["paper_slug"]) if "paper_slug" in subset else {},
            }

    return {"task_bundles": bundles, "manifest": manifest}


def _load_benchmark_tables(base_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    records = pd.read_parquet(base_dir / "baseline_double_green_human_review_records.parquet")
    protocols = pd.read_parquet(base_dir / "baseline_double_green_human_review_protocols.parquet")
    availability = pd.read_parquet(base_dir / "baseline_double_green_human_review_availability.parquet")
    return records, protocols, availability


def _normalize_score(value: Any, unit: Any) -> float | None:
    score = _safe_float(value)
    if score is None:
        return None
    unit_text = str(unit or "").strip().lower()
    if unit_text in {"f1", "semantic_f1"}:
        return max(0.0, min(1.0, score))
    if unit_text == "/100":
        return max(0.0, min(1.0, score / 100.0))
    if unit_text == "/10":
        return max(0.0, min(1.0, score / 10.0))
    return max(0.0, min(1.0, score))


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _truncate_artifact(value: Any, limit: int) -> str:
    text = _safe_text(value)
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...[truncated {len(text) - limit} chars by benchmark replayer]"


def _collect_strings_from_json(value: Any) -> list[str]:
    results: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                results.extend(_collect_strings_from_json(item))
            elif isinstance(item, str) and item.strip():
                results.append(f"{key}: {item.strip()}")
    elif isinstance(value, list):
        for item in value:
            results.extend(_collect_strings_from_json(item))
    elif isinstance(value, str) and value.strip():
        results.append(value.strip())
    return results


def _taxonomy_from_text(texts: list[str]) -> set[str]:
    tags: set[str] = set()
    for raw in texts:
        text = raw.lower()
        if any(token in text for token in ["syntax", "grammar", "format", "notation", "plantuml"]):
            tags.add("syntax_or_notation")
        if any(token in text for token in ["missing", "omitted", "absence", "fn", "not continue", "lack"]):
            tags.add("missing_required_behavior")
        if any(token in text for token in ["guard", "trigger", "condition", "direction", "polarity"]):
            tags.add("wrong_guard_or_trigger")
        if any(token in text for token in ["action", "effect", "feedback", "unlock", "brake"]):
            tags.add("wrong_action_or_effect")
        if any(token in text for token in ["extra", "unsupported", "hallucination", "fp", "meaningless"]):
            tags.add("unsupported_extra_structure")
        if any(token in text for token in ["equivalent", "equivalence", "different structure", "same behavior"]):
            tags.add("equivalence_misjudgement")
        if any(token in text for token in ["readability", "naming", "clear", "clarity"]):
            tags.add("readability_or_naming")
        if any(token in text for token in ["unused", "noise", "noisy", "complexity", "generic", "empty"]):
            tags.add("unused_or_noisy_structure")
        if any(token in text for token in ["evidence", "protocol", "confidence", "insufficient", "overclaim"]):
            tags.add("evidence_overreach")
    return tags


def _judgement_label_index(label: str) -> int:
    try:
        return JUDGEMENT_LABELS.index(str(label))
    except ValueError:
        return 0


def _weighted_kappa(gold_labels: list[str], pred_labels: list[str]) -> float:
    if not gold_labels or not pred_labels or len(gold_labels) != len(pred_labels):
        return 0.0
    total = len(gold_labels)
    scale = max(1, len(JUDGEMENT_LABELS) - 1)
    gold_indices = [_judgement_label_index(item) for item in gold_labels]
    pred_indices = [_judgement_label_index(item) for item in pred_labels]
    observed = sum(abs(gold - pred) / scale for gold, pred in zip(gold_indices, pred_indices)) / total
    gold_dist = [gold_indices.count(idx) / total for idx in range(len(JUDGEMENT_LABELS))]
    pred_dist = [pred_indices.count(idx) / total for idx in range(len(JUDGEMENT_LABELS))]
    expected = sum(
        gold_prob * pred_prob * abs(gold_idx - pred_idx) / scale
        for gold_idx, gold_prob in enumerate(gold_dist)
        for pred_idx, pred_prob in enumerate(pred_dist)
    )
    if expected <= 1e-12:
        return 1.0 if observed <= 1e-12 else 0.0
    return max(-1.0, min(1.0, 1.0 - observed / expected))


def _human_issue_set_from_record(row: pd.Series) -> set[str]:
    texts: list[str] = []
    for key in ["human_review_summary", "human_review_original_text", "review_rubric_text", "public_artifact_limitations"]:
        value = _safe_text(row.get(key))
        if value.strip():
            texts.append(value)
    details_json = _safe_text(row.get("human_review_details_json"))
    if details_json.strip():
        try:
            payload = json.loads(details_json)
            texts.extend(_collect_strings_from_json(payload))
            payload_str = json.dumps(payload, ensure_ascii=False)
            if '"semantic_fp"' in payload_str and any(char.isdigit() for char in payload_str):
                texts.append("semantic_fp")
            if '"semantic_fn"' in payload_str and any(char.isdigit() for char in payload_str):
                texts.append("semantic_fn")
        except Exception:
            texts.append(details_json)
    component = _safe_text(row.get("component") or row.get("review_target")).lower()
    if component == "guards":
        texts.append("guard component review")
    elif component == "actions":
        texts.append("action component review")
    elif component in {"states", "hierarchical states", "history states", "parallel regions"}:
        texts.append("state component review")
    elif component == "transitions":
        texts.append("transition component review")
    return _taxonomy_from_text(texts)


def _agent_issue_set(result: ExpertReviewResult) -> set[str]:
    tags: set[str] = set()
    issue_type_map = {
        "extra": {"unsupported_extra_structure"},
        "contradiction": {"wrong_guard_or_trigger"},
        "low_grounding": {"unused_or_noisy_structure"},
        "readability_or_naming": {"readability_or_naming"},
        "unused_or_noisy_structure": {"unused_or_noisy_structure"},
        "evidence_overreach": {"evidence_overreach"},
        "wrong_action_or_effect": {"wrong_action_or_effect"},
        "wrong_guard_or_trigger": {"wrong_guard_or_trigger"},
        "missing_required_behavior": {"missing_required_behavior"},
        "syntax_or_notation": {"syntax_or_notation"},
        "unsupported_extra_structure": {"unsupported_extra_structure"},
    }
    for issue in result.unsupported_model_elements:
        mapped = issue_type_map.get(issue.issue_type, set())
        tags.update(mapped)
        if not mapped:
            raw = f"{issue.issue_type} {issue.reason_text} {issue.element_text}".lower()
            tags.update(_taxonomy_from_text([raw]))
    for dimension in result.dimension_results:
        metric_taxonomy = {str(item) for item in dimension.metric_payload.get("issue_taxonomy", []) if str(item)}
        tags.update(metric_taxonomy)
        for issue in dimension.issues:
            mapped = issue_type_map.get(issue.issue_type, set())
            tags.update(mapped)
            if not mapped:
                raw = f"{issue.issue_type} {issue.reason_text} {issue.element_text}".lower()
                tags.update(_taxonomy_from_text([raw]))
        if not metric_taxonomy:
            if dimension.dimension_name == "notation_syntax" and dimension.score < 0.45:
                tags.add("syntax_or_notation")
            if dimension.dimension_name == "semantic_completeness" and dimension.score < 0.45:
                tags.add("missing_required_behavior")
            if dimension.dimension_name == "behavioral_consistency" and dimension.score < 0.45:
                tags.add("wrong_guard_or_trigger")
            if dimension.dimension_name == "requirement_traceability" and dimension.score < 0.45:
                tags.add("unsupported_extra_structure")
            if dimension.dimension_name == "pragmatic_clarity" and dimension.score < 0.45:
                tags.update({"readability_or_naming", "unused_or_noisy_structure"})
            if dimension.dimension_name == "evidence_discipline" and dimension.score < 0.45:
                tags.add("evidence_overreach")
    if not tags:
        tags.update(_taxonomy_from_text([result.overall_reason_text] + result.notes))
    return tags


def _agent_critical_issue_set(result: ExpertReviewResult) -> set[str]:
    tags = set(_agent_issue_set(result)) & set(CRITICAL_ISSUE_TAXONOMY)
    extra_texts: list[str] = [result.overall_reason_text, *result.notes]
    for issue in result.unsupported_model_elements:
        extra_texts.append(f"{issue.issue_type} {issue.reason_text} {issue.element_text}")
    for dimension in result.dimension_results:
        extra_texts.append(dimension.reason_text)
        for issue in dimension.issues:
            extra_texts.append(f"{issue.issue_type} {issue.reason_text} {issue.element_text}")
    tags.update(_taxonomy_from_text(extra_texts) & set(CRITICAL_ISSUE_TAXONOMY))
    return tags


def _issue_f1(human: set[str], agent: set[str]) -> tuple[float, float, float]:
    if not human and not agent:
        return 1.0, 1.0, 1.0
    if not human:
        precision = 0.0 if agent else 1.0
        return precision, 1.0, precision
    tp = len(human & agent)
    precision = tp / len(agent) if agent else 0.0
    recall = tp / len(human)
    f1 = 0.0 if precision + recall == 0 else (2 * precision * recall) / (precision + recall)
    return precision, recall, f1


def _spearman(values_a: list[float], values_b: list[float]) -> float:
    if len(values_a) <= 1 or len(values_b) <= 1:
        return 1.0
    ranks_a = pd.Series(values_a).rank(method="average")
    ranks_b = pd.Series(values_b).rank(method="average")
    if ranks_a.nunique(dropna=False) <= 1 or ranks_b.nunique(dropna=False) <= 1:
        return 0.0
    rho = ranks_a.corr(ranks_b, method="pearson")
    if pd.isna(rho):
        return 0.0
    return float(rho)


def _pairwise_order_accuracy(rows: list[dict[str, Any]], score_key_a: str, score_key_b: str) -> float:
    if len(rows) <= 1:
        return 1.0
    total = 0
    correct = 0
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a_left = rows[i][score_key_a]
            a_right = rows[j][score_key_a]
            b_left = rows[i][score_key_b]
            b_right = rows[j][score_key_b]
            if a_left is None or a_right is None or b_left is None or b_right is None:
                continue
            total += 1
            if (a_left - a_right) == 0 and (b_left - b_right) == 0:
                correct += 1
            elif (a_left - a_right) * (b_left - b_right) > 0:
                correct += 1
    return correct / total if total else 1.0


def _score_align(rows: list[dict[str, Any]]) -> dict[str, float]:
    scored_rows = [row for row in rows if row["human_score"] is not None and row["agent_score"] is not None]
    if not scored_rows:
        return {
            "normalized_mae": 1.0,
            "rmse": 1.0,
            "spearman_rho": 0.0,
            "pairwise_order_accuracy": 0.0,
            "hit_at_003": 0.0,
            "hit_at_005": 0.0,
            "score_bias": 0.0,
            "ScoreAlign": 0.0,
        }
    human = [row["human_score"] for row in scored_rows]
    agent = [row["agent_score"] for row in scored_rows]
    errors = [abs(a - h) for a, h in zip(agent, human)]
    mae = sum(errors) / len(errors)
    rmse = math.sqrt(sum((a - h) ** 2 for a, h in zip(agent, human)) / len(errors))
    rho = _spearman(agent, human)
    rho_plus = (rho + 1.0) / 2.0
    hit_003 = sum(1 for error in errors if error <= 0.03) / len(errors)
    hit_005 = sum(1 for error in errors if error <= 0.05) / len(errors)
    bias = sum(a - h for a, h in zip(agent, human)) / len(errors)
    score_align = 100.0 * (0.4 * (1.0 - mae) + 0.3 * rho_plus + 0.3 * hit_005)
    return {
        "normalized_mae": mae,
        "rmse": rmse,
        "spearman_rho": rho,
        "pairwise_order_accuracy": _pairwise_order_accuracy(scored_rows, "human_score", "agent_score"),
        "hit_at_003": hit_003,
        "hit_at_005": hit_005,
        "score_bias": bias,
        "ScoreAlign": score_align,
    }


def _equivalence_metrics(rows: list[dict[str, Any]]) -> dict[str, float]:
    scored = [row for row in rows if row["human_score"] is not None and row["agent_score"] is not None]
    if not scored:
        return {
            "semantic_match_accept_rate": 0.0,
            "equivalence_false_reject_rate": 1.0,
            "equivalence_false_accept_rate": 1.0,
            "EquivAlign": 0.0,
        }
    human_good = [row for row in scored if row["human_score"] >= 0.75]
    human_bad = [row for row in scored if row["human_score"] <= 0.45]
    accept_rate = (
        sum(1 for row in human_good if row["agent_score"] >= 0.65) / len(human_good) if human_good else 1.0
    )
    false_reject = (
        sum(1 for row in human_good if row["agent_score"] < 0.55) / len(human_good) if human_good else 0.0
    )
    false_accept = (
        sum(1 for row in human_bad if row["agent_score"] > 0.65) / len(human_bad) if human_bad else 0.0
    )
    equiv_align = 100.0 * max(0.0, min(1.0, 0.45 * accept_rate + 0.30 * (1.0 - false_reject) + 0.25 * (1.0 - false_accept)))
    return {
        "semantic_match_accept_rate": accept_rate,
        "equivalence_false_reject_rate": false_reject,
        "equivalence_false_accept_rate": false_accept,
        "EquivAlign": equiv_align,
    }


def _calibration_metrics(rows: list[dict[str, Any]]) -> dict[str, float]:
    scored = [row for row in rows if row["human_score"] is not None]
    if not scored:
        return {"ece": 1.0, "brier_score": 1.0, "high_confidence_error_rate": 1.0, "Calib": 0.0}
    outcomes = [1.0 if abs(row["agent_score"] - row["human_score"]) <= 0.05 else 0.0 for row in scored]
    confidences = [row["agent_confidence"] for row in scored]
    brier = sum((conf - out) ** 2 for conf, out in zip(confidences, outcomes)) / len(scored)
    bins = {}
    for conf, out in zip(confidences, outcomes):
        bin_id = min(9, int(conf * 10))
        bins.setdefault(bin_id, []).append((conf, out))
    ece = 0.0
    for values in bins.values():
        avg_conf = sum(item[0] for item in values) / len(values)
        avg_out = sum(item[1] for item in values) / len(values)
        ece += len(values) / len(scored) * abs(avg_conf - avg_out)
    high_conf_rows = [row for row, out in zip(scored, outcomes) if row["agent_confidence"] >= 0.75]
    high_conf_error_rate = (
        sum(1 for row in high_conf_rows if abs(row["agent_score"] - row["human_score"]) > 0.10) / len(high_conf_rows)
        if high_conf_rows
        else 0.0
    )
    calib = 100.0 * max(0.0, min(1.0, 1.0 - 0.55 * brier - 0.45 * ece))
    return {"ece": ece, "brier_score": brier, "high_confidence_error_rate": high_conf_error_rate, "Calib": calib}


def _stability_metrics(rows: list[dict[str, Any]]) -> dict[str, float]:
    rerun_values = [row.get("rerun_score_delta", 0.0) for row in rows if row.get("rerun_score_delta") is not None]
    rerun_std = statistics.mean(rerun_values) if rerun_values else 0.0
    issue_jaccard = statistics.mean(row.get("rerun_issue_jaccard", 1.0) for row in rows) if rows else 1.0
    stability = 100.0 * max(0.0, min(1.0, 0.65 * (1.0 - rerun_std) + 0.35 * issue_jaccard))
    return {"rerun_score_std": rerun_std, "issue_jaccard_across_runs": issue_jaccard, "Stability": stability}


def _summary_discipline_metrics(rows: list[dict[str, Any]]) -> dict[str, float]:
    if not rows:
        return {
            "summary_only_element_claim_rate": 1.0,
            "low_evidence_self_awareness": 0.0,
            "EvidenceDiscipline": 0.0,
        }
    element_claim_rate = sum(1 for row in rows if row["element_claim_count"] > 0) / len(rows)
    self_awareness = sum(1 for row in rows if row["agent_confidence"] <= 0.70 and row["evidence_discipline_score"] >= 0.60) / len(rows)
    evidence_discipline = 100.0 * max(0.0, min(1.0, 0.55 * (1.0 - element_claim_rate) + 0.45 * self_awareness))
    return {
        "summary_only_element_claim_rate": element_claim_rate,
        "low_evidence_self_awareness": self_awareness,
        "EvidenceDiscipline": evidence_discipline,
    }


def _protocol_metrics(rows: list[dict[str, Any]]) -> dict[str, float]:
    if not rows:
        return {
            "regime_accuracy": 0.0,
            "protocol_only_overclaim_rate": 1.0,
            "vv_role_coverage": 0.0,
            "confidence_discipline": 0.0,
            "PDS": 0.0,
        }
    regime_accuracy = sum(1 for row in rows if row["actual_regime"] == "protocol_only") / len(rows)
    overclaim_rate = sum(1 for row in rows if row["element_claim_count"] > 0 or row["trace_matched_count"] > 0) / len(rows)
    vv_role_coverage = sum(1 for row in rows if row["vv_role_coverage"] >= 0.50) / len(rows)
    confidence_discipline = sum(1 for row in rows if row["agent_confidence"] <= 0.55) / len(rows)
    pds = 100.0 * (
        0.35 * regime_accuracy
        + 0.25 * vv_role_coverage
        + 0.25 * (1.0 - overclaim_rate)
        + 0.15 * confidence_discipline
    )
    return {
        "regime_accuracy": regime_accuracy,
        "protocol_only_overclaim_rate": overclaim_rate,
        "vv_role_coverage": vv_role_coverage,
        "confidence_discipline": confidence_discipline,
        "PDS": pds,
    }


def _reason_alignment_metrics(rows: list[dict[str, Any]]) -> dict[str, float]:
    if not rows:
        return {"human_issue_coverage_recall": 0.0, "unsupported_claim_rate": 1.0, "ReasonAlign": 0.0}
    recalls = [row["issue_recall"] for row in rows]
    unsupported_claim_rate = sum(1.0 - row["issue_precision"] for row in rows) / len(rows)
    reason_align = 100.0 * max(0.0, min(1.0, 0.6 * (sum(recalls) / len(recalls)) + 0.4 * (1.0 - unsupported_claim_rate)))
    return {
        "human_issue_coverage_recall": sum(recalls) / len(recalls),
        "unsupported_claim_rate": unsupported_claim_rate,
        "ReasonAlign": reason_align,
    }


def _judgement_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scored_rows = [row for row in rows if row.get("human_judgement") and row.get("agent_judgement")]
    if not scored_rows:
        return {
            "rows": 0,
            "macro_f1": 0.0,
            "weighted_kappa": 0.0,
            "judgement_flip_rate": 0.0,
            "by_bucket": {},
        }

    gold_labels = [str(row["human_judgement"]) for row in scored_rows]
    pred_labels = [str(row["agent_judgement"]) for row in scored_rows]
    rerun_rows = [row for row in scored_rows if row.get("rerun_judgement_flip") is not None]
    by_bucket: dict[str, Any] = {}
    for bucket in ("record", "summary", "component"):
        subset = [row for row in scored_rows if row.get("eval_bucket") == bucket]
        if not subset:
            continue
        subset_gold = [str(row["human_judgement"]) for row in subset]
        subset_pred = [str(row["agent_judgement"]) for row in subset]
        by_bucket[bucket] = {
            "rows": len(subset),
            "macro_f1": _macro_f1_for_labels(subset_gold, subset_pred),
            "weighted_kappa": _weighted_kappa(subset_gold, subset_pred),
        }
    return {
        "rows": len(scored_rows),
        "macro_f1": _macro_f1_for_labels(gold_labels, pred_labels),
        "weighted_kappa": _weighted_kappa(gold_labels, pred_labels),
        "judgement_flip_rate": (
            sum(1.0 for row in rerun_rows if bool(row.get("rerun_judgement_flip"))) / len(rerun_rows) if rerun_rows else 0.0
        ),
        "by_bucket": by_bucket,
    }


def _critical_issue_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    relevant_rows = [row for row in rows if row.get("eval_bucket") != "component"]
    by_type = {
        issue: {"support": 0, "recalled": 0, "recall": 0.0}
        for issue in CRITICAL_ISSUE_TAXONOMY
    }
    total = 0
    recalled = 0
    for row in relevant_rows:
        human = set(row.get("human_issue_set", [])) & set(CRITICAL_ISSUE_TAXONOMY)
        agent = _agent_critical_issue_set(row["result"])
        total += len(human)
        recalled += len(human & agent)
        for issue in human:
            by_type[issue]["support"] += 1
            if issue in agent:
                by_type[issue]["recalled"] += 1
    for issue, stats in by_type.items():
        support = int(stats["support"])
        stats["recall"] = stats["recalled"] / support if support else 1.0
    return {
        "critical_issue_support": total,
        "critical_issue_recalled": recalled,
        "critical_issue_recall": recalled / total if total else 1.0,
        "by_type": by_type,
    }


def _dimension_map(result: ExpertReviewResult) -> dict[str, Any]:
    return {item.dimension_name: item for item in result.dimension_results}


# A2 简化：移除 `_evidence_locator_valid` / `_evidence_locator_metrics`。
# 22 ablation 实测 `evidence_locator_validity` 在所有 ablation 下恒为 1.0 ——
# 因为 evidence_summary 的 locator 由 score_composer / final_synthesizer 用固定 prefix
# 自己生成，benchmark 又用同一套 prefix 验证，结构上必然 1.0。无判别力。


def _contradiction_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    inspected_rows = [row for row in rows if row.get("eval_bucket") != "protocol"]
    contradiction_counts = {
        "high_evidence_score_despite_limited_evidence": 0,
        "high_completeness_despite_missing": 0,
        "high_traceability_despite_conflict": 0,
        "high_behavior_score_despite_structural_conflict": 0,
    }
    contradictory_rows = 0
    for row in inspected_rows:
        dims = _dimension_map(row["result"])
        row_flags = 0
        evidence = dims.get("evidence_discipline")
        completeness = dims.get("semantic_completeness")
        traceability = dims.get("requirement_traceability")
        behavior = dims.get("behavioral_consistency")
        if evidence is not None:
            missing_flags = list(evidence.metric_payload.get("missing_evidence_flags", []))
            if evidence.score >= 0.82 and missing_flags and row.get("agent_confidence", 0.0) >= 0.68:
                contradiction_counts["high_evidence_score_despite_limited_evidence"] += 1
                row_flags += 1
        if completeness is not None:
            missing_ratio = float(completeness.metric_payload.get("missing_ratio", 0.0) or 0.0)
            missing_signal_count = int(completeness.metric_payload.get("missing_signal_count", 0) or 0)
            if completeness.score >= 0.70 and (missing_ratio >= 0.35 or missing_signal_count >= 6):
                contradiction_counts["high_completeness_despite_missing"] += 1
                row_flags += 1
        if traceability is not None:
            trace_conflict_count = int(traceability.metric_payload.get("trace_conflict_count", 0) or 0)
            missing_ratio = float(traceability.metric_payload.get("missing_ratio", 0.0) or 0.0)
            if traceability.score >= 0.70 and (trace_conflict_count > 0 or missing_ratio >= 0.35):
                contradiction_counts["high_traceability_despite_conflict"] += 1
                row_flags += 1
        if behavior is not None:
            dependency_break_count = int(behavior.metric_payload.get("dependency_break_count", 0) or 0)
            parallel_mismatch = bool(behavior.metric_payload.get("parallel_structure_mismatch"))
            if behavior.score >= 0.70 and (dependency_break_count > 0 or parallel_mismatch):
                contradiction_counts["high_behavior_score_despite_structural_conflict"] += 1
                row_flags += 1
        if row_flags:
            contradictory_rows += 1
    return {
        "rows": len(inspected_rows),
        "contradictory_rows": contradictory_rows,
        "contradiction_rate": contradictory_rows / len(inspected_rows) if inspected_rows else 0.0,
        "by_type": contradiction_counts,
    }


def _macro_f1_for_labels(gold_labels: list[str], pred_labels: list[str]) -> float:
    label_set = sorted(set(gold_labels) | set(pred_labels))
    if not label_set:
        return 1.0
    scores: list[float] = []
    for label in label_set:
        tp = sum(1 for gold, pred in zip(gold_labels, pred_labels) if gold == label and pred == label)
        fp = sum(1 for gold, pred in zip(gold_labels, pred_labels) if gold != label and pred == label)
        fn = sum(1 for gold, pred in zip(gold_labels, pred_labels) if gold == label and pred != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        scores.append(0.0 if precision + recall == 0 else (2 * precision * recall) / (precision + recall))
    return sum(scores) / len(scores)


def _component_alignment_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "rows": 0,
            "normalized_mae": 1.0,
            "rmse": 1.0,
            "spearman_rho": 0.0,
            "pairwise_order_accuracy": 0.0,
            "hit_at_003": 0.0,
            "hit_at_005": 0.0,
            "score_bias": 0.0,
            "ScoreAlign": 0.0,
            "macro_f1": 0.0,
            "major_component_macro_f1": 0.0,
            "CRAS": 0.0,
            "by_component": {},
        }
    score_metrics = _score_align(rows)
    gold_labels = [judgement_from_score(float(row["human_score"])) for row in rows if row["human_score"] is not None]
    pred_labels = [judgement_from_score(float(row["agent_score"])) for row in rows if row["agent_score"] is not None]
    macro_f1 = _macro_f1_for_labels(gold_labels, pred_labels)
    by_component: dict[str, Any] = {}
    major_component_values: list[float] = []
    for target in COMPONENT_TARGETS:
        subset = [row for row in rows if str(row.get("metadata", {}).get("component_target") or "") == target]
        if not subset:
            continue
        subset_score = _score_align(subset)
        subset_gold = [judgement_from_score(float(row["human_score"])) for row in subset if row["human_score"] is not None]
        subset_pred = [judgement_from_score(float(row["agent_score"])) for row in subset if row["agent_score"] is not None]
        subset_macro_f1 = _macro_f1_for_labels(subset_gold, subset_pred)
        by_component[target] = {
            "rows": len(subset),
            **subset_score,
            "macro_f1": subset_macro_f1,
        }
        if target in MAJOR_COMPONENT_TARGETS:
            major_component_values.append(subset_macro_f1)
    major_component_macro_f1 = sum(major_component_values) / len(major_component_values) if major_component_values else 0.0
    cras = 100.0 * max(
        0.0,
        min(
            1.0,
            0.45 * (score_metrics["ScoreAlign"] / 100.0)
            + 0.35 * macro_f1
            + 0.20 * score_metrics["hit_at_005"],
        ),
    )
    return {
        "rows": len(rows),
        **score_metrics,
        "macro_f1": macro_f1,
        "major_component_macro_f1": major_component_macro_f1,
        "CRAS": cras,
        "by_component": by_component,
    }


def _build_record_prompt(row: pd.Series) -> str:
    rubric = _safe_text(row.get("review_rubric_text")).strip()
    limitations = _safe_text(row.get("public_artifact_limitations")).strip()
    diagram_type = _safe_text(row.get("diagram_type")).strip() or "model"
    target = _safe_text(row.get("review_target")).strip() or "generated artifact"
    diagram_semantics = {
        "stm": "state-machine semantics centered on states, transitions, guards, hierarchy, and reactive behavior",
        "sd": "interaction-order semantics centered on participants, messages, and temporal ordering",
        "act": "control-flow semantics centered on actions, branches, joins, and workflow progression",
        "bd": "block-structure semantics centered on components, ports, signals, and composition",
    }.get(diagram_type.lower(), "artifact semantics inferred from the visible modeling notation and structure")
    return (
        "You are an expert reviewer for generated software modeling artifacts.\n"
        f"Target type: {diagram_type} / {target}.\n"
        f"Target semantics: {diagram_semantics}.\n"
        "Treat the prompt as a review contract, not as a generation request.\n"
        "Focus on semantic adequacy, behavioral consistency, requirement traceability, unsupported extra structure, "
        "and equivalent-but-different designs.\n"
        "Interpret the artifact by meaning rather than by surface naming or language-specific keywords.\n"
        "Use the reference as a semantic anchor rather than an exact string target.\n"
        f"Public rubric:\n{rubric or 'No explicit rubric text was published for this row.'}\n"
        f"Public limitations:\n{limitations or 'No extra public limitations were recorded.'}"
    )


def _build_summary_prompt(row: pd.Series) -> str:
    rubric = _safe_text(row.get("review_rubric_text")).strip()
    limitations = _safe_text(row.get("public_artifact_limitations")).strip()
    target = _safe_text(row.get("review_target")).strip() or "artifact"
    public_summary = _safe_text(row.get("human_review_summary")).strip()
    summary_semantics = _summary_semantics_from_row(row)
    target_semantics = {
        "BD": "behavior-description quality with emphasis on visible behavioral coverage and understandable public behavior narratives",
        "SMD": "state-machine design quality with emphasis on structural rigor while still allowing semantically equivalent alternative designs",
        "UCD": "use-case or interaction communication quality with emphasis on publicly visible interaction adequacy",
        "Properties": "property-set quality with emphasis on whether visible constraints and verification targets are coherent and useful",
    }.get(target, "summary-level artifact quality judged from the public evidence that is actually visible")
    return (
        "You are an expert reviewer for generated software modeling artifacts under partial public evidence.\n"
        f"This is a summary-level task for {target}.\n"
        f"Target semantics: {target_semantics}\n"
        f"Public summary row semantics: {summary_semantics}\n"
        "Give an overall review that respects evidence limits. Do not invent precise element-level mismatch claims "
        "when the public evidence only supports overall judgement. If the contract refers to average/max/min/std-dev "
        "style published statistics, calibrate the coarse score to that public summary semantics rather than pretending "
        "you saw hidden per-run annotations.\n"
        "When the target label and the artifact text use different languages or naming styles, follow semantic meaning rather than surface tokens.\n"
        f"Public row note:\n{public_summary or 'No extra public row note was recorded.'}\n"
        f"Public rubric:\n{rubric or 'No explicit rubric text was published for this row.'}\n"
        f"Public limitations:\n{limitations or 'No extra public limitations were recorded.'}"
    )


def _summary_row_type_from_row(row: pd.Series) -> str:
    review_record_id = _safe_text(row.get("review_record_id")).lower()
    record_type = _safe_text(row.get("record_type")).lower()
    if any(token in review_record_id for token in ["std_dev", "std dev", "stddev"]) or "std" in review_record_id:
        return "aggregate_stddev"
    if "average" in review_record_id or record_type in {"summary", "case_aggregate_stat", "overall_aggregate_stat"}:
        return "aggregate_average"
    if any(token in review_record_id for token in [":max", "maximum", "highest"]):
        return "aggregate_max"
    if any(token in review_record_id for token in [":min", "minimum", "lowest"]):
        return "aggregate_min"
    if record_type == "raw_score_row":
        return "raw_score_row"
    if record_type == "summary_level_run_score":
        return "run_level_score"
    return "summary_public_score"


def _artifact_semantics_from_row(row: pd.Series) -> str | None:
    diagram_type = _safe_text(row.get("diagram_type")).strip().lower()
    return {
        "stm": "reactive_state_model",
        "sd": "interaction_sequence_model",
        "act": "control_flow_model",
        "bd": "architecture_structure_model",
    }.get(diagram_type)


def _summary_semantics_from_row(row: pd.Series) -> str:
    row_type = _summary_row_type_from_row(row)
    if row_type == "aggregate_stddev":
        return "This published row is a standard-deviation or dispersion statistic."
    if row_type == "aggregate_average":
        return "This published row is an average or aggregate quality statistic."
    if row_type == "aggregate_max":
        return "This published row is a highest-score or best-case aggregate statistic."
    if row_type == "aggregate_min":
        return "This published row is a minimum-score or worst-case aggregate statistic."
    if row_type == "raw_score_row":
        return "This published row is a raw public score row without per-element justification."
    if row_type == "run_level_score":
        return "This published row is a run-level summary score."
    return "This published row is a public summary-level score."


def _build_protocol_prompt(row: pd.Series) -> str:
    return (
        "You are an expert reviewer of a human evaluation protocol for software modeling artifacts.\n"
        "There is no full per-record prediction/reference evidence in this task. Review what the protocol can validate, "
        "which V&V roles it uses, and what claims should remain uncertain.\n"
        "Do not fabricate precise artifact-level findings."
    )


def _build_component_prompt(row: pd.Series) -> str:
    component_target = _safe_text(row.get("component_target") or row.get("review_target")).strip() or "Component"
    system_name = _safe_text(row.get("component_system_name") or row.get("case_name")).strip() or "the target system"
    strategy_name = _safe_text(row.get("component_strategy_name") or row.get("strategy_name")).strip() or "the published generation strategy"
    llm_name = _safe_text(row.get("component_llm_name") or row.get("llm_name")).strip() or "the published model run"
    rubric = _safe_text(row.get("review_rubric_text")).strip()
    public_row_text = _safe_text(row.get("component_public_row_text")).strip()
    return (
        "You are an expert reviewer for component-level public evidence about generated state-machine artifacts.\n"
        f"Review only the `{component_target}` component family for {system_name}.\n"
        f"The public evidence comes from the published {strategy_name} / {llm_name} component audit row.\n"
        "Treat TP / FP / FN as semantic evidence counts for the target component, not as language-specific tokens.\n"
        "Do not infer hidden image details, and do not rely on surface naming assumptions. Score the component quality "
        "from the structured public evidence that is actually visible.\n"
        "If the prompt, model label, or system description use different languages, keep the judgement grounded in the "
        "component semantics rather than the wording.\n"
        f"Public component row (verbatim, score omitted from structured evidence):\n{public_row_text or 'No extra verbatim row text was recorded.'}\n"
        f"Public rubric:\n{rubric or 'No explicit rubric text was published for this row.'}"
    )


def _build_component_pred_output(row: pd.Series) -> str:
    payload = {
        "artifact_type": "public_component_audit",
        "component_target": _safe_text(row.get("component_target") or row.get("review_target")).strip(),
        "tp": _safe_int(row.get("component_public_tp")),
        "fp": _safe_int(row.get("component_public_fp")),
        "fn": _safe_int(row.get("component_public_fn")),
        "predicted_component_total": _safe_int(row.get("component_pred_total")),
        "reference_component_total": _safe_int(row.get("component_reference_total")),
        "source_kind": _safe_text(row.get("component_source_kind")).strip() or "xlsx_row",
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def _build_component_input_text(row: pd.Series) -> str:
    return "\n".join(
        [
            f"System: {_safe_text(row.get('component_system_name') or row.get('case_name')).strip() or 'Unknown'}",
            f"Strategy: {_safe_text(row.get('component_strategy_name') or row.get('strategy_name')).strip() or 'Unknown'}",
            f"Model: {_safe_text(row.get('component_llm_name') or row.get('llm_name')).strip() or 'Unknown'}",
            f"Component target: {_safe_text(row.get('component_target') or row.get('review_target')).strip() or 'Unknown'}",
            "Use the structured TP/FP/FN evidence in the predicted artifact JSON as the main scoring anchor.",
        ]
    )


def _build_record_task(row: pd.Series) -> BenchmarkTask:
    return BenchmarkTask(
        task_id=str(row["review_record_id"]),
        eval_bucket="record",
        regime_expected="record_level",
        prompt=_build_record_prompt(row),
        input_text=_safe_text(row.get("input_text")),
        pred_output=_truncate_artifact(row.get("pred_output_text"), 12000),
        ref_output=_truncate_artifact(row.get("ref_output_text"), 12000) or None,
        human_score=_normalize_score(row.get("human_review_score"), row.get("human_review_score_unit")),
        human_score_unit=_safe_text(row.get("human_review_score_unit")) or None,
        human_issue_set=_human_issue_set_from_record(row),
        group_key=str(row.get("family_key") or f"{row.get('paper_slug')}::{row.get('diagram_type')}::{row.get('review_target')}"),
        metadata={
            "paper_slug": row.get("paper_slug"),
            "record_type": row.get("record_type"),
            "diagram_type": row.get("diagram_type"),
            "review_target": row.get("review_target"),
            "review_surface": "direct_artifact_review",
            "artifact_semantics": _artifact_semantics_from_row(row),
            "llm_name": row.get("llm_name"),
            "case_id": row.get("case_id"),
            "case_name": row.get("case_name"),
            "split_name": row.get("split_name"),
            "sheet_name": row.get("sheet_name"),
            "family_key": row.get("family_key"),
        },
    )


def _build_summary_task(row: pd.Series) -> BenchmarkTask:
    return BenchmarkTask(
        task_id=str(row["review_record_id"]),
        eval_bucket="summary",
        regime_expected="summary_level",
        prompt=_build_summary_prompt(row),
        input_text=_safe_text(row.get("input_text")),
        pred_output=_truncate_artifact(row.get("pred_output_text"), 9000),
        ref_output=None,
        human_score=_normalize_score(row.get("human_review_score"), row.get("human_review_score_unit")),
        human_score_unit=_safe_text(row.get("human_review_score_unit")) or None,
        human_issue_set=_human_issue_set_from_record(row),
        group_key=str(row.get("family_key") or f"{row.get('paper_slug')}::{row.get('review_target')}::{row.get('record_type')}"),
        metadata={
            "paper_slug": row.get("paper_slug"),
            "record_type": row.get("record_type"),
            "diagram_type": row.get("diagram_type"),
            "review_target": row.get("review_target"),
            "summary_target": row.get("review_target"),
            "review_surface": "summary_public_score",
            "summary_row_type": _summary_row_type_from_row(row),
            "case_id": row.get("case_id"),
            "case_name": row.get("case_name"),
            "split_name": row.get("split_name"),
            "sheet_name": row.get("sheet_name"),
            "family_key": row.get("family_key"),
        },
    )


def _build_protocol_task(row: pd.Series) -> BenchmarkTask:
    input_text = "\n\n".join(
        [
            f"Artifact under review: {_safe_text(row.get('artifact_under_review'))}",
            f"Reference basis: {_safe_text(row.get('reference_basis'))}",
            f"Reviewer pool: {_safe_text(row.get('reviewer_pool'))}",
            f"Review dimensions: {_safe_text(row.get('review_dimensions_json'))}",
            f"Execution steps: {_safe_text(row.get('execution_steps_markdown'))}",
            f"Matching rules: {_safe_text(row.get('matching_rules_markdown'))}",
            f"Public gap notes: {_safe_text(row.get('public_gap_notes'))}",
        ]
    )
    protocol_issue_set = _taxonomy_from_text(
        [
            _safe_text(row.get("execution_steps_markdown")),
            _safe_text(row.get("matching_rules_markdown")),
            _safe_text(row.get("public_gap_notes")),
        ]
    )
    protocol_issue_set.add("evidence_overreach")
    return BenchmarkTask(
        task_id=f"protocol::{row.get('paper_slug')}",
        eval_bucket="protocol",
        regime_expected="protocol_only",
        prompt=_build_protocol_prompt(row),
        input_text=input_text,
        pred_output="",
        ref_output=None,
        human_score=None,
        human_score_unit=None,
        human_issue_set=protocol_issue_set,
        group_key=str(row.get("family_key") or f"protocol::{row.get('paper_slug')}"),
        metadata={
            "paper_slug": row.get("paper_slug"),
            "record_type": "protocol_only",
            "review_surface": "protocol_assurance",
            "family_key": row.get("family_key"),
            "public_human_review_status": row.get("public_human_review_status"),
        },
    )


def _build_component_task(row: pd.Series) -> BenchmarkTask:
    component_target = _safe_text(row.get("component_target") or row.get("review_target")).strip() or "Component"
    return BenchmarkTask(
        task_id=str(row["review_record_id"]),
        eval_bucket="component",
        regime_expected="component_level",
        prompt=_build_component_prompt(row),
        input_text=_build_component_input_text(row),
        pred_output=_build_component_pred_output(row),
        ref_output=None,
        human_score=_safe_float(row.get("component_human_score")),
        human_score_unit=_safe_text(row.get("human_review_score_unit")) or None,
        human_issue_set=set(),
        group_key=str(row.get("family_key") or f"{row.get('paper_slug')}::{row.get('case_id')}::{row.get('llm_name')}"),
        metadata={
            "paper_slug": row.get("paper_slug"),
            "record_type": row.get("record_type"),
            "diagram_type": "stm",
            "artifact_semantics": "reactive_state_model",
            "review_target": row.get("review_target"),
            "review_surface": "summary_public_score",
            "component_target": component_target,
            "component_source_kind": row.get("component_source_kind"),
            "component_sheet_name": row.get("component_sheet_name"),
            "component_public_tp": _safe_int(row.get("component_public_tp")),
            "component_public_fp": _safe_int(row.get("component_public_fp")),
            "component_public_fn": _safe_int(row.get("component_public_fn")),
            "component_pred_total": _safe_int(row.get("component_pred_total")),
            "component_reference_total": _safe_int(row.get("component_reference_total")),
            "component_public_image_reference": row.get("component_public_image_reference"),
            "component_human_score_source": row.get("component_human_score_source"),
            "component_evidence_status": row.get("component_evidence_status"),
            "component_strategy_name": row.get("component_strategy_name"),
            "llm_name": row.get("component_llm_name") or row.get("llm_name"),
            "case_id": row.get("case_id"),
            "case_name": row.get("case_name"),
            "family_key": row.get("family_key"),
        },
    )


def _sample_grouped(df: pd.DataFrame, limit: int, group_fields: list[str], seed: int) -> pd.DataFrame:
    if limit <= 0 or len(df) <= limit:
        return df.copy()
    rng = random.Random(seed)
    groups = [group.copy() for _, group in df.groupby(group_fields, dropna=False)]
    rng.shuffle(groups)
    picked_frames: list[pd.DataFrame] = []
    total = 0
    while groups and total < limit:
        next_round: list[pd.DataFrame] = []
        for group in groups:
            if total >= limit:
                next_round.append(group)
                continue
            picked_frames.append(group.iloc[[0]])
            total += 1
            if len(group) > 1:
                next_round.append(group.iloc[1:].copy())
        groups = next_round
    if not picked_frames:
        return df.head(limit).copy()
    return pd.concat(picked_frames, ignore_index=True)


def build_benchmark_slices(
    records: pd.DataFrame,
    protocols: pd.DataFrame,
    *,
    record_limit: int,
    summary_limit: int,
    component_limit: int,
    protocol_limit: int,
    seed: int,
) -> dict[str, list[BenchmarkTask]]:
    strong_record_df = _prepare_record_level_pool(records)
    summary_df = _prepare_summary_level_pool(records)
    component_df = _prepare_component_level_pool(records)
    sampled_record_df = _sample_grouped(strong_record_df, record_limit, ["paper_slug", "diagram_type", "llm_name"], seed)
    sampled_summary_df = _sample_grouped(
        summary_df,
        summary_limit,
        ["paper_slug", "record_type", "review_target", "case_id"],
        seed + 1,
    )
    sampled_component_df = _sample_grouped(
        component_df,
        component_limit,
        ["paper_slug", "review_target", "llm_name", "case_id"],
        seed + 2,
    )
    sampled_protocol_df = _prepare_protocol_level_pool(protocols).head(protocol_limit).copy()
    return {
        "record": _rows_to_tasks("record", sampled_record_df),
        "summary": _rows_to_tasks("summary", sampled_summary_df),
        "component": _rows_to_tasks("component", sampled_component_df),
        "protocol": _rows_to_tasks("protocol", sampled_protocol_df),
    }


def build_full_available_task_bundle(
    records: pd.DataFrame,
    protocols: pd.DataFrame,
    availability: pd.DataFrame,
) -> dict[str, list[BenchmarkTask]]:
    inventory = build_benchmark_inventory(records, protocols, availability)
    return {
        "record": _rows_to_tasks("record", inventory["record_level"]),
        "summary": _rows_to_tasks("summary", inventory["summary_level"]),
        "component": _rows_to_tasks("component", inventory["component_level"]),
        "protocol": _rows_to_tasks("protocol", inventory["protocol_only"]),
    }


def _regime_from_result(result: ExpertReviewResult) -> str:
    if result.dimension_results and result.dimension_results[0].metric_payload:
        regime = str(result.dimension_results[0].metric_payload.get("regime", "")).strip()
        if regime:
            return regime
    for note in result.notes:
        if "protocol_only" in note:
            return "protocol_only"
        if "mixed_evidence" in note:
            return "mixed_evidence"
        if "record_level" in note:
            return "record_level"
        if "summary_only" in note:
            return "summary_only"
    return "unknown"


def _dimension_score(result: ExpertReviewResult, name: str) -> float:
    for item in result.dimension_results:
        if item.dimension_name == name:
            return item.score
    return 0.0


def _vv_role_coverage(result: ExpertReviewResult) -> float:
    for item in result.dimension_results:
        if item.dimension_name != "evidence_discipline":
            continue
        roles = item.metric_payload.get("vv_roles", [])
        if roles:
            return len({str(role).strip().lower() for role in roles if str(role).strip()}) / 5.0
    text = " ".join([result.overall_reason_text] + result.notes + [item.reason_text for item in result.dimension_results]).lower()
    role_hints = {
        "inspection": ["inspection", "manual", "人工", "逐项对照", "手工"],
        "formal verification": ["formal verification", "verification", "model checker", "model-checking", "形式化验证", "模型检查"],
        "simulation": ["simulation", "simulator", "仿真", "模拟"],
        "testing": ["testing", "test", "测试"],
        "syntax checker": ["syntax checker", "grammar", "format checking", "语法", "格式检查"],
    }
    covered = 0
    for hints in role_hints.values():
        if any(hint in text for hint in hints):
            covered += 1
    return covered / len(role_hints)


def _rerun_subset(
    agent: ExpertReviewAgent,
    tasks: list[BenchmarkTask],
    *,
    rerun_count: int,
) -> dict[str, tuple[float, float, bool]]:
    result: dict[str, tuple[float, float, bool]] = {}
    if rerun_count <= 0:
        return result
    for task in tasks[:rerun_count]:
        request = ExpertReviewRequest(
            prompt=task.prompt,
            input_text=task.input_text,
            pred_output=task.pred_output,
            ref_output=task.ref_output,
            metadata=dict(task.metadata),
        )
        first = agent.review(request)
        second = agent.review(request)
        issue_first = _agent_issue_set(first)
        issue_second = _agent_issue_set(second)
        union = len(issue_first | issue_second)
        jaccard = len(issue_first & issue_second) / union if union else 1.0
        result[task.task_id] = (
            abs(first.overall_score - second.overall_score),
            jaccard,
            str(first.overall_judgement) != str(second.overall_judgement),
        )
    return result


def _error_buckets_for_row(row: dict[str, Any]) -> list[str]:
    if row.get("eval_bucket") == "component":
        return []
    buckets: set[str] = set()
    human_issues = set(row.get("human_issue_set", []))
    agent_issues = set(row.get("agent_issue_set", []))
    expected_regime = str(row.get("expected_regime", ""))
    actual_regime = str(row.get("actual_regime", ""))
    human_score = row.get("human_score")
    agent_score = row.get("agent_score")

    if expected_regime and actual_regime and expected_regime != actual_regime:
        buckets.add("contract_understanding_error")

    extraction_tags = {"syntax_or_notation", "wrong_guard_or_trigger", "wrong_action_or_effect"}
    if (human_issues & extraction_tags) != (agent_issues & extraction_tags):
        buckets.add("element_extraction_error")

    quality_tags = {"readability_or_naming", "unused_or_noisy_structure"}
    if (human_issues & quality_tags) != (agent_issues & quality_tags):
        buckets.add("quality_judgement_error")

    if human_score is not None and agent_score is not None:
        delta = float(agent_score) - float(human_score)
        if abs(delta) > 0.10:
            buckets.add("calibration_error")
        if expected_regime == "record_level" and (
            (human_score >= 0.75 and agent_score < 0.55)
            or (human_score <= 0.45 and agent_score > 0.65)
            or "equivalence_misjudgement" in (human_issues | agent_issues)
        ):
            buckets.add("equivalence_reasoning_error")

    if expected_regime in {"summary_level", "protocol_only"} and (
        int(row.get("element_claim_count", 0)) > 0 or int(row.get("trace_matched_count", 0)) > 0
    ):
        buckets.add("evidence_discipline_error")
    elif row.get("issue_precision") is not None and float(row["issue_precision"]) < 0.5:
        buckets.add("evidence_discipline_error")

    return sorted(buckets)


def _build_error_map(
    normalized_rows: list[dict[str, Any]],
    *,
    record_metrics: dict[str, Any],
    summary_metrics: dict[str, Any],
) -> dict[str, Any]:
    bucket_counts = {bucket: 0 for bucket in PHASE7_ERROR_BUCKETS}
    top_examples: dict[str, list[dict[str, Any]]] = {bucket: [] for bucket in PHASE7_ERROR_BUCKETS}
    regime_confusions: dict[str, int] = defaultdict(int)

    for row in normalized_rows:
        row["error_buckets"] = _error_buckets_for_row(row)
        if row.get("eval_bucket") == "component":
            continue
        if row.get("expected_regime") != row.get("actual_regime"):
            confusion_key = f"{row.get('expected_regime')}->{row.get('actual_regime')}"
            regime_confusions[confusion_key] += 1
        for bucket in row["error_buckets"]:
            if bucket not in bucket_counts:
                continue
            bucket_counts[bucket] += 1
            if len(top_examples[bucket]) < 5:
                human_score = row.get("human_score")
                agent_score = row.get("agent_score")
                delta = None
                if human_score is not None and agent_score is not None:
                    delta = round(float(agent_score) - float(human_score), 4)
                top_examples[bucket].append(
                    {
                        "task_id": row.get("task_id"),
                        "expected_regime": row.get("expected_regime"),
                        "actual_regime": row.get("actual_regime"),
                        "human_score": human_score,
                        "agent_score": agent_score,
                        "delta": delta,
                        "metadata": row.get("metadata", {}),
                    }
                )

    ranking_risk = {
        "record": {
            "spearman_rho": record_metrics.get("spearman_rho", 0.0),
            "pairwise_order_accuracy": record_metrics.get("pairwise_order_accuracy", 0.0),
        },
        "summary": {
            "spearman_rho": summary_metrics.get("spearman_rho", 0.0),
            "pairwise_order_accuracy": summary_metrics.get("pairwise_order_accuracy", 0.0),
        },
    }
    for regime_name, metrics in ranking_risk.items():
        spearman = float(metrics.get("spearman_rho", 0.0))
        pairwise = float(metrics.get("pairwise_order_accuracy", 0.0))
        if spearman >= 0.75 and pairwise >= 0.80:
            risk = "low"
        elif spearman >= 0.55 and pairwise >= 0.65:
            risk = "medium"
        else:
            risk = "high"
        metrics["risk_level"] = risk

    return {
        "bucket_counts": bucket_counts,
        "top_examples": {key: value for key, value in top_examples.items() if value},
        "regime_confusions": dict(sorted(regime_confusions.items())),
        "ranking_risk": ranking_risk,
    }


def _task_inventory(tasks_by_regime: dict[str, list[BenchmarkTask]]) -> dict[str, Any]:
    inventory: dict[str, Any] = {}
    for regime_name, tasks in tasks_by_regime.items():
        inventory[regime_name] = {
            "rows": len(tasks),
            "family_count": len({task.group_key for task in tasks}),
        }
    return inventory


def _runtime_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    latencies = [float(row.get("latency_s", 0.0) or 0.0) for row in rows]
    confidences = [float(row.get("agent_confidence", 0.0) or 0.0) for row in rows]
    llm_rows = [row for row in rows if bool(row.get("llm_configured"))]
    successful_llm_rows = [row for row in llm_rows if bool(row.get("llm_effective_used"))]
    total_tokens = sum(int(row.get("llm_total_tokens", 0) or 0) for row in rows)
    prompt_tokens = sum(int(row.get("llm_prompt_tokens", 0) or 0) for row in rows)
    completion_tokens = sum(int(row.get("llm_completion_tokens", 0) or 0) for row in rows)
    operation_attempts = sum(int(row.get("llm_operation_attempt_count", 0) or 0) for row in rows)
    operation_successes = sum(int(row.get("llm_operation_success_count", 0) or 0) for row in rows)
    operation_failures = sum(int(row.get("llm_operation_failure_count", 0) or 0) for row in rows)
    return {
        "confidence_mean": statistics.mean(confidences) if confidences else 0.0,
        "latency_p50": statistics.median(latencies) if latencies else 0.0,
        "latency_p95": _p95(latencies),
        "llm_configured_record_count": len(llm_rows),
        "llm_effective_record_count": len(successful_llm_rows),
        "llm_effective_record_rate": len(successful_llm_rows) / len(llm_rows) if llm_rows else 0.0,
        "llm_fallback_only_record_rate": (
            sum(1 for row in llm_rows if bool(row.get("llm_fallback_only"))) / len(llm_rows) if llm_rows else 0.0
        ),
        "llm_total_tokens": total_tokens,
        "llm_prompt_tokens": prompt_tokens,
        "llm_completion_tokens": completion_tokens,
        "token_cost_per_record": total_tokens / max(1, len(rows)),
        "llm_operation_attempt_count": operation_attempts,
        "llm_operation_success_count": operation_successes,
        "llm_operation_failure_count": operation_failures,
        "llm_operation_success_rate": operation_successes / max(1, operation_attempts),
    }


def _evaluate_task_bundle(
    tasks_by_regime: dict[str, list[BenchmarkTask]],
    *,
    llm_mode: str,
    rerun_count: int,
    report_label: str,
    metadata: dict[str, Any] | None = None,
    review_cache: dict[str, dict[str, Any]] | None = None,
    model: str | None = None,
    provider_order: list[str] | None = None,
    temperature: float = 0.0,
    timeout: int = 180,
    max_workers: int = 1,
) -> dict[str, Any]:
    if llm_mode == "auto":
        agent = ExpertReviewAgent(
            model=model or DEFAULT_MODEL,
            provider_order=provider_order,
            temperature=temperature,
            timeout=timeout,
        )
    else:
        agent = ExpertReviewAgent(provider_order=[])
    rerun_seed_tasks = (
        tasks_by_regime.get("record", [])[:rerun_count]
        + tasks_by_regime.get("summary", [])[:rerun_count]
        + tasks_by_regime.get("component", [])[:rerun_count]
    )
    reruns = _rerun_subset(agent, rerun_seed_tasks, rerun_count=rerun_count)

    # Flatten ordered task list (preserve regime order for downstream metrics
    # that subset by eval_bucket, but row order doesn't actually matter).
    all_tasks: list[BenchmarkTask] = []
    for tasks in tasks_by_regime.values():
        all_tasks.extend(tasks)

    def _process_task(task):
        request = ExpertReviewRequest(
            prompt=task.prompt,
            input_text=task.input_text,
            pred_output=task.pred_output,
            ref_output=task.ref_output,
            metadata=dict(task.metadata),
        )
        cache_key = f"{llm_mode}::{task.task_id}"
        cached = review_cache.get(cache_key) if review_cache is not None else None
        if cached is None:
            start = time.perf_counter()
            result = agent.review(request)
            latency = time.perf_counter() - start
            if review_cache is not None:
                review_cache[cache_key] = {"result": result, "latency_s": latency}
        else:
            result = cached["result"]
            latency = float(cached.get("latency_s", 0.0))
        return task, result, latency

    if max_workers > 1:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        completed_results: list[tuple] = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_process_task, t): t for t in all_tasks}
            for fut in as_completed(futures):
                completed_results.append(fut.result())
        # Re-sort to original task order to keep deterministic outputs across runs
        order = {t.task_id: i for i, t in enumerate(all_tasks)}
        completed_results.sort(key=lambda x: order[x[0].task_id])
    else:
        completed_results = [_process_task(t) for t in all_tasks]

    normalized_rows: list[dict[str, Any]] = []
    for task, result, latency in completed_results:
        agent_issue_set = _agent_issue_set(result)
        issue_precision, issue_recall, issue_f1 = _issue_f1(task.human_issue_set, agent_issue_set)
        rerun_score_delta, rerun_issue_jaccard, rerun_judgement_flip = reruns.get(task.task_id, (0.0, 1.0, False))
        normalized_rows.append(
            {
                "task_id": task.task_id,
                "eval_bucket": task.eval_bucket,
                "expected_regime": task.regime_expected,
                "actual_regime": _regime_from_result(result),
                "human_score": task.human_score,
                "human_judgement": judgement_from_score(float(task.human_score)) if task.human_score is not None else None,
                "agent_score": result.overall_score,
                "agent_judgement": str(result.overall_judgement or judgement_from_score(result.overall_score)),
                "agent_confidence": result.confidence,
                "human_issue_set": sorted(task.human_issue_set),
                "agent_issue_set": sorted(agent_issue_set),
                "issue_precision": issue_precision,
                "issue_recall": issue_recall,
                "issue_f1": issue_f1,
                "element_claim_count": len(result.unsupported_model_elements),
                "trace_matched_count": sum(1 for item in result.requirement_trace_results if item.status == "matched"),
                "evidence_discipline_score": _dimension_score(result, "evidence_discipline"),
                "vv_role_coverage": _vv_role_coverage(result),
                "latency_s": latency,
                "rerun_score_delta": rerun_score_delta,
                "rerun_issue_jaccard": rerun_issue_jaccard,
                "rerun_judgement_flip": rerun_judgement_flip,
                "used_review_backend": result.used_review_backend,
                "llm_model_name": result.llm_model_name,
                "llm_provider": result.llm_provider,
                "llm_configured": result.llm_usage_summary.llm_configured,
                "llm_effective_used": result.llm_usage_summary.effective_llm_used,
                "llm_fallback_only": result.llm_usage_summary.fallback_only,
                "llm_operation_attempt_count": result.llm_usage_summary.operation_attempt_count,
                "llm_operation_success_count": result.llm_usage_summary.operation_success_count,
                "llm_operation_failure_count": result.llm_usage_summary.operation_failure_count,
                "llm_prompt_tokens": result.llm_usage_summary.prompt_tokens,
                "llm_completion_tokens": result.llm_usage_summary.completion_tokens,
                "llm_total_tokens": result.llm_usage_summary.total_tokens,
                "metadata": task.metadata,
                "result": result,
            }
        )

    record_rows = [row for row in normalized_rows if row["eval_bucket"] == "record"]
    summary_rows = [row for row in normalized_rows if row["eval_bucket"] == "summary"]
    component_rows = [row for row in normalized_rows if row["eval_bucket"] == "component"]
    protocol_rows = [row for row in normalized_rows if row["eval_bucket"] == "protocol"]

    record_score = _score_align(record_rows)
    record_reason = _reason_alignment_metrics(record_rows)
    record_equiv = _equivalence_metrics(record_rows)
    record_calib = _calibration_metrics(record_rows)
    issue_f1 = statistics.mean(row["issue_f1"] for row in record_rows) * 100.0 if record_rows else 0.0
    ras = (
        0.30 * record_score["ScoreAlign"]
        + 0.25 * issue_f1
        + 0.20 * record_reason["ReasonAlign"]
        + 0.15 * record_equiv["EquivAlign"]
        + 0.10 * record_calib["Calib"]
    )

    summary_score = _score_align(summary_rows)
    summary_discipline = _summary_discipline_metrics(summary_rows)
    stability = _stability_metrics(summary_rows + record_rows)
    rank_align = 100.0 * summary_score["pairwise_order_accuracy"]
    sas = (
        0.40 * summary_score["ScoreAlign"]
        + 0.25 * rank_align
        + 0.20 * summary_discipline["EvidenceDiscipline"]
        + 0.15 * stability["Stability"]
    )

    component_metrics = _component_alignment_metrics(component_rows)
    protocol_metrics = _protocol_metrics(protocol_rows)
    judgement_metrics = _judgement_metrics(record_rows + summary_rows + component_rows)
    contradiction_metrics = _contradiction_metrics(normalized_rows)
    critical_issue_metrics = _critical_issue_metrics(record_rows + summary_rows)
    runtime_metrics = _runtime_metrics(normalized_rows)
    # A1 公式重定义：
    # 旧 HAI = 0.55·RAS + 0.25·SAS + 0.20·PDS：PDS 自 Phase 13 起所有 split / LOFO 都是 100，
    # 意味着 HAI 公式中固定 20 分来自一个不再产生信号的 metric；同时 CRAS（component 维度）
    # 完全没进 HAI 公式。新 HAI 重新分配权重让所有项都"会动"，且把 CRAS 拉进 promotion 决策。
    # 旧 HAI 仍以 hai_legacy 形式输出，便于和历史 phase 对比。PDS 转为独立的 binary gate。
    hai_legacy = 0.55 * ras + 0.25 * sas + 0.20 * protocol_metrics["PDS"]
    hai = 0.40 * ras + 0.30 * sas + 0.30 * component_metrics["CRAS"]
    pds_gate_threshold = 95.0
    pds_gate_pass = bool(protocol_metrics["PDS"] >= pds_gate_threshold)

    report = {
        "report_label": report_label,
        "sample_sizes": {
            "record": len(record_rows),
            "summary": len(summary_rows),
            "component": len(component_rows),
            "protocol": len(protocol_rows),
        },
        "task_inventory": _task_inventory(tasks_by_regime),
        "record_metrics": {
            **record_score,
            **record_reason,
            **record_equiv,
            **record_calib,
            "issue_f1": issue_f1 / 100.0,
            "RAS": ras,
        },
        "summary_metrics": {
            **summary_score,
            **summary_discipline,
            **stability,
            "RankAlign": rank_align,
            "SAS": sas,
        },
        "component_metrics": component_metrics,
        "protocol_metrics": protocol_metrics,
        "judgement_metrics": judgement_metrics,
        "contradiction_metrics": contradiction_metrics,
        "critical_issue_metrics": critical_issue_metrics,
        "runtime_metrics": runtime_metrics,
        "HAI": hai,
        "HAI_legacy": hai_legacy,
        "pds_gate": {
            "threshold": pds_gate_threshold,
            "value": protocol_metrics["PDS"],
            "passed": pds_gate_pass,
        },
        "metadata": {} if metadata is None else dict(metadata),
        "normalized_rows": normalized_rows,
    }
    report["error_map"] = _build_error_map(
        normalized_rows,
        record_metrics=report["record_metrics"],
        summary_metrics=report["summary_metrics"],
    )
    return report


def run_benchmark_iteration(
    *,
    base_dir: Path = DEFAULT_BENCHMARK_DIR,
    record_limit: int = 18,
    summary_limit: int = 16,
    component_limit: int = 24,
    protocol_limit: int = 4,
    seed: int = 7,
    rerun_count: int = 4,
    llm_mode: str = "off",
    scope: str = "slice",
    split_name: str | None = None,
    model: str | None = None,
    provider_order: list[str] | None = None,
    temperature: float = 0.0,
    timeout: int = 180,
    max_workers: int = 1,
) -> dict[str, Any]:
    records, protocols, availability = _load_benchmark_tables(base_dir)
    if scope == "slice":
        task_bundle = build_benchmark_slices(
            records,
            protocols,
            record_limit=record_limit,
            summary_limit=summary_limit,
            component_limit=component_limit,
            protocol_limit=protocol_limit,
            seed=seed,
        )
        report_label = "slice"
        metadata = {
            "scope": "slice",
            "record_limit": record_limit,
            "summary_limit": summary_limit,
            "component_limit": component_limit,
            "protocol_limit": protocol_limit,
            "seed": seed,
        }
    elif scope == "full":
        task_bundle = build_full_available_task_bundle(records, protocols, availability)
        report_label = "full_available"
        metadata = {"scope": "full"}
    elif scope == "split":
        if split_name not in SPLIT_ORDER:
            raise ValueError(f"split scope requires split_name in {SPLIT_ORDER}, got {split_name!r}")
        split_bundle = build_benchmark_split_bundle(records, protocols, availability, seed=seed)
        task_bundle = split_bundle["task_bundles"][split_name]
        report_label = f"split:{split_name}"
        metadata = {
            "scope": "split",
            "split_name": split_name,
            "split_manifest": split_bundle["manifest"],
        }
    else:
        raise ValueError(f"Unsupported scope: {scope}")

    return _evaluate_task_bundle(
        task_bundle,
        llm_mode=llm_mode,
        rerun_count=rerun_count,
        report_label=report_label,
        metadata=metadata,
        model=model,
        provider_order=provider_order,
        temperature=temperature,
        timeout=timeout,
        max_workers=max_workers,
    )


def _summarize_lofo_reports(lofo_reports: dict[str, dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for report in lofo_reports.values():
        regime = str(report.get("metadata", {}).get("lofo_regime", "unknown"))
        grouped[regime].append(report)

    summary: dict[str, Any] = {}
    for regime, reports in grouped.items():
        if regime == "record":
            worst_family, min_ras = min(
                (
                    (str(report.get("metadata", {}).get("lofo_family", "unknown")), report["record_metrics"]["RAS"])
                    for report in reports
                ),
                key=lambda item: item[1],
            )
            summary[regime] = {
                "family_count": len(reports),
                "avg_RAS": statistics.mean(report["record_metrics"]["RAS"] for report in reports),
                "avg_normalized_mae": statistics.mean(report["record_metrics"]["normalized_mae"] for report in reports),
                "avg_spearman_rho": statistics.mean(report["record_metrics"]["spearman_rho"] for report in reports),
                "avg_pairwise_order_accuracy": statistics.mean(
                    report["record_metrics"]["pairwise_order_accuracy"] for report in reports
                ),
                "min_RAS": min_ras,
                "worst_family": worst_family,
            }
        elif regime == "summary":
            worst_family, min_sas = min(
                (
                    (str(report.get("metadata", {}).get("lofo_family", "unknown")), report["summary_metrics"]["SAS"])
                    for report in reports
                ),
                key=lambda item: item[1],
            )
            summary[regime] = {
                "family_count": len(reports),
                "avg_SAS": statistics.mean(report["summary_metrics"]["SAS"] for report in reports),
                "avg_normalized_mae": statistics.mean(report["summary_metrics"]["normalized_mae"] for report in reports),
                "avg_spearman_rho": statistics.mean(report["summary_metrics"]["spearman_rho"] for report in reports),
                "avg_pairwise_order_accuracy": statistics.mean(
                    report["summary_metrics"]["pairwise_order_accuracy"] for report in reports
                ),
                "min_SAS": min_sas,
                "worst_family": worst_family,
            }
        elif regime == "component":
            worst_family, min_cras = min(
                (
                    (str(report.get("metadata", {}).get("lofo_family", "unknown")), report["component_metrics"]["CRAS"])
                    for report in reports
                ),
                key=lambda item: item[1],
            )
            summary[regime] = {
                "family_count": len(reports),
                "avg_CRAS": statistics.mean(report["component_metrics"]["CRAS"] for report in reports),
                "avg_macro_f1": statistics.mean(report["component_metrics"]["macro_f1"] for report in reports),
                "avg_major_component_macro_f1": statistics.mean(
                    report["component_metrics"]["major_component_macro_f1"] for report in reports
                ),
                "min_CRAS": min_cras,
                "worst_family": worst_family,
            }
        elif regime == "protocol":
            worst_family, min_pds = min(
                (
                    (str(report.get("metadata", {}).get("lofo_family", "unknown")), report["protocol_metrics"]["PDS"])
                    for report in reports
                ),
                key=lambda item: item[1],
            )
            summary[regime] = {
                "family_count": len(reports),
                "avg_PDS": statistics.mean(report["protocol_metrics"]["PDS"] for report in reports),
                "avg_vv_role_coverage": statistics.mean(report["protocol_metrics"]["vv_role_coverage"] for report in reports),
                "avg_protocol_only_overclaim_rate": statistics.mean(
                    report["protocol_metrics"]["protocol_only_overclaim_rate"] for report in reports
                ),
                "min_PDS": min_pds,
                "worst_family": worst_family,
            }
    return summary


def _summarize_split_reports(split_reports: dict[str, dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for split in SPLIT_ORDER:
        report = split_reports.get(split)
        if report is None:
            continue
        summary[split] = {
            "HAI": report["HAI"],
            "RAS": report["record_metrics"]["RAS"],
            "SAS": report["summary_metrics"]["SAS"],
            "CRAS": report["component_metrics"]["CRAS"],
            "PDS": report["protocol_metrics"]["PDS"],
            "record_normalized_mae": report["record_metrics"]["normalized_mae"],
            "record_spearman_rho": report["record_metrics"]["spearman_rho"],
            "summary_spearman_rho": report["summary_metrics"]["spearman_rho"],
            "component_macro_f1": report["component_metrics"]["macro_f1"],
        }
    return summary


def _summarize_lofo_generalization(
    full_report: dict[str, Any],
    lofo_summary: dict[str, Any],
) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    if "record" in lofo_summary:
        summary["record"] = {
            "full_RAS": full_report["record_metrics"]["RAS"],
            "avg_RAS": lofo_summary["record"]["avg_RAS"],
            "avg_gap_vs_full": full_report["record_metrics"]["RAS"] - lofo_summary["record"]["avg_RAS"],
            "worst_holdout_RAS": lofo_summary["record"]["min_RAS"],
            "worst_holdout_gap_vs_full": full_report["record_metrics"]["RAS"] - lofo_summary["record"]["min_RAS"],
            "worst_family": lofo_summary["record"]["worst_family"],
        }
    if "summary" in lofo_summary:
        summary["summary"] = {
            "full_SAS": full_report["summary_metrics"]["SAS"],
            "avg_SAS": lofo_summary["summary"]["avg_SAS"],
            "avg_gap_vs_full": full_report["summary_metrics"]["SAS"] - lofo_summary["summary"]["avg_SAS"],
            "worst_holdout_SAS": lofo_summary["summary"]["min_SAS"],
            "worst_holdout_gap_vs_full": full_report["summary_metrics"]["SAS"] - lofo_summary["summary"]["min_SAS"],
            "worst_family": lofo_summary["summary"]["worst_family"],
        }
    if "component" in lofo_summary:
        summary["component"] = {
            "full_CRAS": full_report["component_metrics"]["CRAS"],
            "avg_CRAS": lofo_summary["component"]["avg_CRAS"],
            "avg_gap_vs_full": full_report["component_metrics"]["CRAS"] - lofo_summary["component"]["avg_CRAS"],
            "worst_holdout_CRAS": lofo_summary["component"]["min_CRAS"],
            "worst_holdout_gap_vs_full": full_report["component_metrics"]["CRAS"] - lofo_summary["component"]["min_CRAS"],
            "worst_family": lofo_summary["component"]["worst_family"],
        }
    if "protocol" in lofo_summary:
        summary["protocol"] = {
            "full_PDS": full_report["protocol_metrics"]["PDS"],
            "avg_PDS": lofo_summary["protocol"]["avg_PDS"],
            "avg_gap_vs_full": full_report["protocol_metrics"]["PDS"] - lofo_summary["protocol"]["avg_PDS"],
            "worst_holdout_PDS": lofo_summary["protocol"]["min_PDS"],
            "worst_holdout_gap_vs_full": full_report["protocol_metrics"]["PDS"] - lofo_summary["protocol"]["min_PDS"],
            "worst_family": lofo_summary["protocol"]["worst_family"],
        }
    return summary


def _core_metric_value(report: dict[str, Any], metric_name: str) -> float:
    if metric_name == "HAI":
        return float(report.get("HAI", 0.0))
    if metric_name == "RAS":
        return float(report.get("record_metrics", {}).get("RAS", 0.0))
    if metric_name == "SAS":
        return float(report.get("summary_metrics", {}).get("SAS", 0.0))
    if metric_name == "CRAS":
        return float(report.get("component_metrics", {}).get("CRAS", 0.0))
    if metric_name == "PDS":
        return float(report.get("protocol_metrics", {}).get("PDS", 0.0))
    raise KeyError(f"Unsupported core metric: {metric_name}")


def _build_phase14_lockbox_gate(split_reports: dict[str, dict[str, Any]]) -> dict[str, Any]:
    validation_report = split_reports.get("validation")
    lockbox_report = split_reports.get("lockbox")
    if validation_report is None or lockbox_report is None:
        return {
            "status": "failed",
            "reason": "missing_validation_or_lockbox_report",
            "lockbox_max_core_metric_degrade": PHASE14_LOCKBOX_MAX_DEGRADE,
            "core_metric_deltas": {},
        }

    core_metric_deltas: dict[str, Any] = {}
    max_degrade = 0.0
    passed = True
    for metric_name in PHASE14_CORE_METRICS:
        validation_value = _core_metric_value(validation_report, metric_name)
        lockbox_value = _core_metric_value(lockbox_report, metric_name)
        degrade = validation_value - lockbox_value
        metric_passed = degrade <= PHASE14_LOCKBOX_MAX_DEGRADE
        max_degrade = max(max_degrade, degrade)
        passed = passed and metric_passed
        core_metric_deltas[metric_name] = {
            "validation": validation_value,
            "lockbox": lockbox_value,
            "degrade": degrade,
            "passed": metric_passed,
        }

    return {
        "status": "passed" if passed else "failed",
        "lockbox_max_core_metric_degrade": PHASE14_LOCKBOX_MAX_DEGRADE,
        "max_observed_degrade": max_degrade,
        "core_metric_deltas": core_metric_deltas,
    }


def _build_phase14_lofo_gate(lofo_generalization: dict[str, Any]) -> dict[str, Any]:
    if not lofo_generalization:
        return {
            "status": "failed",
            "reason": "missing_lofo_generalization",
            "LOFO_generalization_gap": {},
        }

    max_avg_gap = 0.0
    max_worst_gap = 0.0
    gap_payload: dict[str, Any] = {}
    for regime_name, metrics in lofo_generalization.items():
        avg_gap = float(metrics.get("avg_gap_vs_full", 0.0))
        worst_gap = float(metrics.get("worst_holdout_gap_vs_full", 0.0))
        max_avg_gap = max(max_avg_gap, avg_gap)
        max_worst_gap = max(max_worst_gap, worst_gap)
        gap_payload[regime_name] = {
            "avg_gap_vs_full": avg_gap,
            "worst_holdout_gap_vs_full": worst_gap,
            "worst_family": metrics.get("worst_family"),
        }

    return {
        "status": "passed",
        "LOFO_generalization_gap": gap_payload,
        "max_avg_gap_vs_full": max_avg_gap,
        "max_worst_holdout_gap_vs_full": max_worst_gap,
    }


def _score_delta(row: dict[str, Any]) -> float | None:
    human_score = row.get("human_score")
    agent_score = row.get("agent_score")
    if human_score is None or agent_score is None:
        return None
    return float(agent_score) - float(human_score)


def _lockbox_primary_bucket(row: dict[str, Any]) -> str:
    buckets = list(row.get("error_buckets") or [])
    if buckets:
        return str(buckets[0])

    delta = _score_delta(row)
    if row.get("eval_bucket") == "component":
        if delta is not None and abs(delta) > 0.05:
            return "component_score_gap"
        return "clean"

    if delta is not None and abs(delta) > 0.10:
        return "calibration_error"
    if row.get("issue_f1") is not None and float(row.get("issue_f1", 1.0)) < 0.5:
        return "evidence_discipline_error"
    return "clean"


def _lockbox_cluster_focus(row: dict[str, Any]) -> str:
    metadata = row.get("metadata") or {}
    eval_bucket = str(row.get("eval_bucket", "unknown"))
    if eval_bucket == "record":
        return str(metadata.get("diagram_type") or metadata.get("review_target") or "generic")
    if eval_bucket == "summary":
        return str(metadata.get("review_target") or metadata.get("paper_slug") or "generic")
    if eval_bucket == "component":
        return str(metadata.get("component_target") or "generic")
    return str(metadata.get("paper_slug") or metadata.get("family_key") or "generic")


def _summarize_lockbox_residual_clusters(
    lockbox_report: dict[str, Any] | None,
    *,
    top_k: int = 6,
) -> dict[str, Any]:
    if lockbox_report is None:
        return {
            "status": "failed",
            "reason": "missing_lockbox_report",
            "analyzed_rows": 0,
            "residual_rows": 0,
            "residual_row_rate": 0.0,
            "bucket_counts": {},
            "clusters": [],
        }

    normalized_rows = list(lockbox_report.get("normalized_rows", []))
    residual_rows: list[dict[str, Any]] = []
    bucket_counts: dict[str, int] = defaultdict(int)
    cluster_rows: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)

    for row in normalized_rows:
        primary_bucket = _lockbox_primary_bucket(row)
        if primary_bucket == "clean":
            continue
        bucket_counts[primary_bucket] += 1
        cluster_key = (str(row.get("eval_bucket", "unknown")), primary_bucket, _lockbox_cluster_focus(row))
        cluster_rows[cluster_key].append(row)
        residual_rows.append(row)

    clusters: list[dict[str, Any]] = []
    for (eval_bucket, primary_bucket, focus_key), rows in cluster_rows.items():
        deltas = [abs(delta) for delta in (_score_delta(row) for row in rows) if delta is not None]
        issue_f1_values = [float(row["issue_f1"]) for row in rows if row.get("issue_f1") is not None]
        family_keys = sorted(
            {
                str((row.get("metadata") or {}).get("family_key") or "unknown")
                for row in rows
            }
        )
        clusters.append(
            {
                "eval_bucket": eval_bucket,
                "primary_bucket": primary_bucket,
                "focus_key": focus_key,
                "rows": len(rows),
                "family_count": len(family_keys),
                "avg_abs_score_delta": statistics.mean(deltas) if deltas else 0.0,
                "avg_issue_f1": statistics.mean(issue_f1_values) if issue_f1_values else 0.0,
                "sample_families": family_keys[:3],
                "sample_task_ids": [str(row.get("task_id")) for row in rows[:3]],
            }
        )

    clusters.sort(
        key=lambda item: (
            -int(item["rows"]),
            -float(item["avg_abs_score_delta"]),
            str(item["eval_bucket"]),
            str(item["primary_bucket"]),
            str(item["focus_key"]),
        )
    )
    analyzed_rows = len(normalized_rows)
    residual_count = len(residual_rows)
    return {
        "status": "passed",
        "analyzed_rows": analyzed_rows,
        "residual_rows": residual_count,
        "residual_row_rate": (residual_count / analyzed_rows) if analyzed_rows else 0.0,
        "bucket_counts": dict(sorted(bucket_counts.items())),
        "clusters": clusters[:top_k],
    }


def _build_phase14_promotion_evaluation(
    *,
    candidate_version: str | None,
    split_reports: dict[str, dict[str, Any]],
    lofo_generalization: dict[str, Any],
    lockbox_residuals: dict[str, Any],
) -> dict[str, Any]:
    validation_report = split_reports.get("validation")
    validation_stage = {
        "status": "passed" if validation_report is not None else "failed",
        "required_artifact": "validation_report",
        "metrics": (
            {metric_name: _core_metric_value(validation_report, metric_name) for metric_name in PHASE14_CORE_METRICS}
            if validation_report is not None
            else {}
        ),
    }
    lockbox_stage = _build_phase14_lockbox_gate(split_reports)
    lofo_stage = _build_phase14_lofo_gate(lofo_generalization)
    residual_stage = {
        "status": "passed" if lockbox_residuals.get("status") == "passed" else "failed",
        "required_artifact": "lockbox_residual_analysis",
        "residual_rows": lockbox_residuals.get("residual_rows", 0),
        "residual_row_rate": lockbox_residuals.get("residual_row_rate", 0.0),
        "cluster_count": len(lockbox_residuals.get("clusters", [])),
    }
    # A1: 显式 PDS binary gate（之前 PDS 通过 0.20 权重隐式进入 HAI；现在 HAI 公式不再含 PDS，
    # 改为独立 gate，确保 PDS 退化能阻止 promotion，但不再"占 HAI 20 分恒值"）。
    pds_gate_threshold = 95.0

    def _resolve_pds_gate(report: dict[str, Any] | None) -> dict[str, Any] | None:
        if report is None:
            return None
        existing = report.get("pds_gate")
        if isinstance(existing, dict) and "passed" in existing:
            return existing
        pds_value = float(report.get("protocol_metrics", {}).get("PDS", 0.0))
        return {
            "threshold": pds_gate_threshold,
            "value": pds_value,
            "passed": bool(pds_value >= pds_gate_threshold),
        }

    validation_pds_gate = _resolve_pds_gate(validation_report)
    lockbox_pds_gate = _resolve_pds_gate(split_reports.get("lockbox"))
    pds_gate_passed = bool(
        validation_pds_gate and validation_pds_gate.get("passed")
        and lockbox_pds_gate and lockbox_pds_gate.get("passed")
    )
    pds_gate_stage = {
        "status": "passed" if pds_gate_passed else "failed",
        "required_artifact": "pds_gate",
        "validation": validation_pds_gate,
        "lockbox": lockbox_pds_gate,
    }

    stages = {
        "validation": validation_stage,
        "lockbox": lockbox_stage,
        "lofo": lofo_stage,
        "residual_audit": residual_stage,
        "pds_gate": pds_gate_stage,
    }
    all_passed = all(stage.get("status") == "passed" for stage in stages.values())
    return {
        "candidate_version": candidate_version or "unlabeled",
        "default_acceptance_surface": "validation + lockbox + LOFO + lockbox_residual_audit + pds_gate",
        "stages": stages,
        "generalization_evidence_ready": all_passed,
        "promotion_status": "promoted_to_phase14_default" if all_passed else "hold",
    }


def run_phase7_evaluation_bundle(
    *,
    base_dir: Path = DEFAULT_BENCHMARK_DIR,
    record_limit: int = 18,
    summary_limit: int = 16,
    component_limit: int = 24,
    protocol_limit: int = 4,
    seed: int = 7,
    rerun_count: int = 4,
    llm_mode: str = "off",
    model: str | None = None,
    provider_order: list[str] | None = None,
    temperature: float = 0.0,
    timeout: int = 180,
) -> dict[str, Any]:
    records, protocols, availability = _load_benchmark_tables(base_dir)
    coverage = summarize_benchmark_coverage(records, protocols, availability)
    slice_tasks = build_benchmark_slices(
        records,
        protocols,
        record_limit=record_limit,
        summary_limit=summary_limit,
        component_limit=component_limit,
        protocol_limit=protocol_limit,
        seed=seed,
    )
    full_tasks = build_full_available_task_bundle(records, protocols, availability)
    split_bundle = build_benchmark_split_bundle(records, protocols, availability, seed=seed)
    lofo_bundle = build_lofo_task_bundles(records, protocols, availability)
    review_cache: dict[str, dict[str, Any]] | None = {} if llm_mode == "off" else None

    slice_report = _evaluate_task_bundle(
        slice_tasks,
        llm_mode=llm_mode,
        rerun_count=rerun_count,
        report_label="phase7:slice",
        metadata={"scope": "slice", "seed": seed},
        review_cache=review_cache,
        model=model,
        provider_order=provider_order,
        temperature=temperature,
        timeout=timeout,
    )
    full_report = _evaluate_task_bundle(
        full_tasks,
        llm_mode=llm_mode,
        rerun_count=rerun_count,
        report_label="phase7:full_available",
        metadata={"scope": "full"},
        review_cache=review_cache,
        model=model,
        provider_order=provider_order,
        temperature=temperature,
        timeout=timeout,
    )
    split_reports = {
        split: _evaluate_task_bundle(
            task_bundle,
            llm_mode=llm_mode,
            rerun_count=0,
            report_label=f"phase7:split:{split}",
            metadata={"scope": "split", "split_name": split},
            review_cache=review_cache,
            model=model,
            provider_order=provider_order,
            temperature=temperature,
            timeout=timeout,
        )
        for split, task_bundle in split_bundle["task_bundles"].items()
    }
    lofo_reports = {
        namespaced_key: _evaluate_task_bundle(
            task_bundle,
            llm_mode=llm_mode,
            rerun_count=0,
            report_label=f"phase7:lofo:{namespaced_key}",
            metadata={
                "scope": "lofo",
                "lofo_family": namespaced_key,
                "lofo_regime": lofo_bundle["manifest"]["families"][namespaced_key]["regime"],
            },
            review_cache=review_cache,
            model=model,
            provider_order=provider_order,
            temperature=temperature,
            timeout=timeout,
        )
        for namespaced_key, task_bundle in lofo_bundle["task_bundles"].items()
    }

    lofo_summary = _summarize_lofo_reports(lofo_reports)
    split_summary = _summarize_split_reports(split_reports)

    return {
        "coverage": coverage,
        "slice_report": slice_report,
        "full_report": full_report,
        "split_manifest": split_bundle["manifest"],
        "split_reports": split_reports,
        "split_summary": split_summary,
        "lofo_manifest": lofo_bundle["manifest"],
        "lofo_reports": lofo_reports,
        "lofo_summary": lofo_summary,
        "lofo_generalization": _summarize_lofo_generalization(full_report, lofo_summary),
    }


def run_phase14_evaluation_bundle(
    *,
    base_dir: Path = DEFAULT_BENCHMARK_DIR,
    record_limit: int = 18,
    summary_limit: int = 16,
    component_limit: int = 24,
    protocol_limit: int = 4,
    seed: int = 7,
    rerun_count: int = 4,
    llm_mode: str = "off",
    candidate_version: str | None = None,
    model: str | None = None,
    provider_order: list[str] | None = None,
    temperature: float = 0.0,
    timeout: int = 180,
) -> dict[str, Any]:
    bundle = run_phase7_evaluation_bundle(
        base_dir=base_dir,
        record_limit=record_limit,
        summary_limit=summary_limit,
        component_limit=component_limit,
        protocol_limit=protocol_limit,
        seed=seed,
        rerun_count=rerun_count,
        llm_mode=llm_mode,
        model=model,
        provider_order=provider_order,
        temperature=temperature,
        timeout=timeout,
    )
    lockbox_residuals = _summarize_lockbox_residual_clusters(bundle["split_reports"].get("lockbox"))
    promotion_evaluation = _build_phase14_promotion_evaluation(
        candidate_version=candidate_version,
        split_reports=bundle["split_reports"],
        lofo_generalization=bundle["lofo_generalization"],
        lockbox_residuals=lockbox_residuals,
    )
    return {
        **bundle,
        "candidate_version": candidate_version or "unlabeled",
        "phase14_policy": {
            "split_order": list(SPLIT_ORDER),
            "split_ratios": dict(DEFAULT_SPLIT_RATIOS),
            "lockbox_max_core_metric_degrade": PHASE14_LOCKBOX_MAX_DEGRADE,
            "core_metrics": list(PHASE14_CORE_METRICS),
        },
        "lockbox_residual_analysis": lockbox_residuals,
        "promotion_evaluation": promotion_evaluation,
    }


def _metric_delta(candidate: dict[str, Any], baseline: dict[str, Any], key: str) -> float:
    return float(candidate.get(key, 0.0) or 0.0) - float(baseline.get(key, 0.0) or 0.0)


def _phase15_recommendation(comparison: dict[str, Any]) -> str:
    candidate_runtime = comparison["candidate_runtime"]
    candidate_alignment = comparison["candidate_alignment"]
    deltas = comparison["delta"]
    if candidate_runtime.get("llm_effective_record_rate", 0.0) < 0.50:
        return "deterministic_default_llm_not_effective_enough"
    if candidate_alignment["summary_metrics"].get("rerun_score_std", 1.0) > 0.03:
        return "deterministic_default_llm_drift_too_high"
    if deltas["HAI"] <= 0.0 and candidate_runtime.get("token_cost_per_record", 0.0) > 0.0:
        return "deterministic_default_no_alignment_gain"
    if deltas["HAI"] >= 1.0 and candidate_alignment["summary_metrics"].get("rerun_score_std", 1.0) <= 0.03:
        return "llm_optional_gain_visible"
    return "deterministic_default_llm_optional"


def _build_phase15_report_comparison(
    baseline_report: dict[str, Any],
    candidate_report: dict[str, Any],
) -> dict[str, Any]:
    delta = {
        "HAI": _metric_delta(candidate_report, baseline_report, "HAI"),
        "RAS": _metric_delta(candidate_report["record_metrics"], baseline_report["record_metrics"], "RAS"),
        "SAS": _metric_delta(candidate_report["summary_metrics"], baseline_report["summary_metrics"], "SAS"),
        "CRAS": _metric_delta(candidate_report["component_metrics"], baseline_report["component_metrics"], "CRAS"),
        "PDS": _metric_delta(candidate_report["protocol_metrics"], baseline_report["protocol_metrics"], "PDS"),
        "record_spearman_rho": _metric_delta(
            candidate_report["record_metrics"],
            baseline_report["record_metrics"],
            "spearman_rho",
        ),
        "record_pairwise_order_accuracy": _metric_delta(
            candidate_report["record_metrics"],
            baseline_report["record_metrics"],
            "pairwise_order_accuracy",
        ),
        "summary_spearman_rho": _metric_delta(
            candidate_report["summary_metrics"],
            baseline_report["summary_metrics"],
            "spearman_rho",
        ),
        "summary_pairwise_order_accuracy": _metric_delta(
            candidate_report["summary_metrics"],
            baseline_report["summary_metrics"],
            "pairwise_order_accuracy",
        ),
        "weighted_kappa": _metric_delta(
            candidate_report["judgement_metrics"],
            baseline_report["judgement_metrics"],
            "weighted_kappa",
        ),
        "confidence_mean": _metric_delta(
            candidate_report["runtime_metrics"],
            baseline_report["runtime_metrics"],
            "confidence_mean",
        ),
        "rerun_score_std": _metric_delta(
            candidate_report["summary_metrics"],
            baseline_report["summary_metrics"],
            "rerun_score_std",
        ),
        "issue_jaccard_across_runs": _metric_delta(
            candidate_report["summary_metrics"],
            baseline_report["summary_metrics"],
            "issue_jaccard_across_runs",
        ),
        "latency_p50": _metric_delta(
            candidate_report["runtime_metrics"],
            baseline_report["runtime_metrics"],
            "latency_p50",
        ),
        "latency_p95": _metric_delta(
            candidate_report["runtime_metrics"],
            baseline_report["runtime_metrics"],
            "latency_p95",
        ),
        "token_cost_per_record": _metric_delta(
            candidate_report["runtime_metrics"],
            baseline_report["runtime_metrics"],
            "token_cost_per_record",
        ),
        "llm_effective_record_rate": _metric_delta(
            candidate_report["runtime_metrics"],
            baseline_report["runtime_metrics"],
            "llm_effective_record_rate",
        ),
        "llm_fallback_only_record_rate": _metric_delta(
            candidate_report["runtime_metrics"],
            baseline_report["runtime_metrics"],
            "llm_fallback_only_record_rate",
        ),
    }
    comparison = {
        "baseline_alignment": {
            "HAI": baseline_report["HAI"],
            "record_metrics": baseline_report["record_metrics"],
            "summary_metrics": baseline_report["summary_metrics"],
            "component_metrics": baseline_report["component_metrics"],
            "protocol_metrics": baseline_report["protocol_metrics"],
        },
        "candidate_alignment": {
            "HAI": candidate_report["HAI"],
            "record_metrics": candidate_report["record_metrics"],
            "summary_metrics": candidate_report["summary_metrics"],
            "component_metrics": candidate_report["component_metrics"],
            "protocol_metrics": candidate_report["protocol_metrics"],
        },
        "baseline_runtime": baseline_report["runtime_metrics"],
        "candidate_runtime": candidate_report["runtime_metrics"],
        "delta": delta,
    }
    comparison["default_path_recommendation"] = _phase15_recommendation(comparison)
    return comparison


def run_phase15_comparison_bundle(
    *,
    base_dir: Path = DEFAULT_BENCHMARK_DIR,
    record_limit: int = 18,
    summary_limit: int = 16,
    component_limit: int = 24,
    protocol_limit: int = 4,
    seed: int = 7,
    rerun_count: int = 4,
    comparison_scope: str = "full",
    split_name: str | None = None,
    candidate_version: str | None = None,
    model: str | None = None,
    provider_order: list[str] | None = None,
    temperature: float = 0.0,
    timeout: int = 180,
) -> dict[str, Any]:
    if comparison_scope == "phase14":
        baseline_payload = run_phase14_evaluation_bundle(
            base_dir=base_dir,
            record_limit=record_limit,
            summary_limit=summary_limit,
            component_limit=component_limit,
            protocol_limit=protocol_limit,
            seed=seed,
            rerun_count=rerun_count,
            llm_mode="off",
            candidate_version="deterministic_baseline",
            model=model,
            provider_order=provider_order,
            temperature=temperature,
            timeout=timeout,
        )
        candidate_payload = run_phase14_evaluation_bundle(
            base_dir=base_dir,
            record_limit=record_limit,
            summary_limit=summary_limit,
            component_limit=component_limit,
            protocol_limit=protocol_limit,
            seed=seed,
            rerun_count=rerun_count,
            llm_mode="auto",
            candidate_version=candidate_version or "llm_enabled_candidate",
            model=model,
            provider_order=provider_order,
            temperature=temperature,
            timeout=timeout,
        )
        baseline_report = baseline_payload["full_report"]
        candidate_report = candidate_payload["full_report"]
    else:
        baseline_payload = run_benchmark_iteration(
            base_dir=base_dir,
            record_limit=record_limit,
            summary_limit=summary_limit,
            component_limit=component_limit,
            protocol_limit=protocol_limit,
            seed=seed,
            rerun_count=rerun_count,
            llm_mode="off",
            scope=comparison_scope,
            split_name=split_name,
            model=model,
            provider_order=provider_order,
            temperature=temperature,
            timeout=timeout,
        )
        candidate_payload = run_benchmark_iteration(
            base_dir=base_dir,
            record_limit=record_limit,
            summary_limit=summary_limit,
            component_limit=component_limit,
            protocol_limit=protocol_limit,
            seed=seed,
            rerun_count=rerun_count,
            llm_mode="auto",
            scope=comparison_scope,
            split_name=split_name,
            model=model,
            provider_order=provider_order,
            temperature=temperature,
            timeout=timeout,
        )
        baseline_report = baseline_payload
        candidate_report = candidate_payload

    return {
        "comparison_scope": comparison_scope,
        "split_name": split_name,
        "candidate_model": model or DEFAULT_MODEL,
        "provider_order": [] if provider_order is None else list(provider_order),
        "baseline_payload": _jsonable_phase14_bundle(baseline_payload) if comparison_scope == "phase14" else _jsonable_report(baseline_payload),
        "candidate_payload": _jsonable_phase14_bundle(candidate_payload) if comparison_scope == "phase14" else _jsonable_report(candidate_payload),
        "comparison": _build_phase15_report_comparison(baseline_report, candidate_report),
    }


def _format_report(report: dict[str, Any]) -> str:
    sample_sizes = report["sample_sizes"]
    task_inventory = report.get("task_inventory", {})
    record = report["record_metrics"]
    summary = report["summary_metrics"]
    component = report["component_metrics"]
    protocol = report["protocol_metrics"]
    judgement = report.get("judgement_metrics", {})
    contradiction = report.get("contradiction_metrics", {})
    critical = report.get("critical_issue_metrics", {})
    runtime = report.get("runtime_metrics", {})
    lines = [
        f"# Alignment Report: {report.get('report_label', 'unnamed')}",
        "",
        "## Sample Sizes",
        f"- record: {sample_sizes['record']}",
        f"- summary: {sample_sizes['summary']}",
        f"- component: {sample_sizes['component']}",
        f"- protocol: {sample_sizes['protocol']}",
        "",
        "## Task Inventory",
        f"- record families: {task_inventory.get('record', {}).get('family_count', 0)}",
        f"- summary families: {task_inventory.get('summary', {}).get('family_count', 0)}",
        f"- component families: {task_inventory.get('component', {}).get('family_count', 0)}",
        f"- protocol families: {task_inventory.get('protocol', {}).get('family_count', 0)}",
        "",
        "## Record Metrics",
        f"- ScoreAlign: {record['ScoreAlign']:.2f}",
        f"- issue_f1: {record['issue_f1']:.3f}",
        f"- ReasonAlign: {record['ReasonAlign']:.2f}",
        f"- EquivAlign: {record['EquivAlign']:.2f}",
        f"- Calib: {record['Calib']:.2f}",
        f"- normalized_mae: {record['normalized_mae']:.4f}",
        f"- hit@0.05: {record['hit_at_005']:.4f}",
        f"- equivalence_false_reject_rate: {record['equivalence_false_reject_rate']:.4f}",
        f"- unsupported_claim_rate: {record['unsupported_claim_rate']:.4f}",
        f"- RAS: {record['RAS']:.2f}",
        "",
        "## Summary Metrics",
        f"- ScoreAlign: {summary['ScoreAlign']:.2f}",
        f"- RankAlign: {summary['RankAlign']:.2f}",
        f"- EvidenceDiscipline: {summary['EvidenceDiscipline']:.2f}",
        f"- Stability: {summary['Stability']:.2f}",
        f"- summary_only_element_claim_rate: {summary['summary_only_element_claim_rate']:.4f}",
        f"- SAS: {summary['SAS']:.2f}",
        "",
        "## Component Metrics",
        f"- ScoreAlign: {component['ScoreAlign']:.2f}",
        f"- macro_f1: {component['macro_f1']:.4f}",
        f"- major_component_macro_f1: {component['major_component_macro_f1']:.4f}",
        f"- normalized_mae: {component['normalized_mae']:.4f}",
        f"- hit@0.05: {component['hit_at_005']:.4f}",
        f"- CRAS: {component['CRAS']:.2f}",
        "",
        "## Protocol Metrics",
        f"- regime_accuracy: {protocol['regime_accuracy']:.4f}",
        f"- protocol_only_overclaim_rate: {protocol['protocol_only_overclaim_rate']:.4f}",
        f"- vv_role_coverage: {protocol['vv_role_coverage']:.4f}",
        f"- confidence_discipline: {protocol['confidence_discipline']:.4f}",
        f"- PDS: {protocol['PDS']:.2f}",
        "",
        "## Judgement Metrics",
        f"- macro_f1: {judgement.get('macro_f1', 0.0):.4f}",
        f"- weighted_kappa: {judgement.get('weighted_kappa', 0.0):.4f}",
        f"- judgement_flip_rate: {judgement.get('judgement_flip_rate', 0.0):.4f}",
        "",
        "## Reason / Evidence Reliability",
        f"- critical_issue_recall: {critical.get('critical_issue_recall', 0.0):.4f}",
        f"- unsupported_claim_rate: {record['unsupported_claim_rate']:.4f}",
        f"- contradiction_rate: {contradiction.get('contradiction_rate', 0.0):.4f}",
        "",
        "## Runtime / LLM Observability",
        f"- confidence_mean: {runtime.get('confidence_mean', 0.0):.4f}",
        f"- latency_p50: {runtime.get('latency_p50', 0.0):.4f}",
        f"- latency_p95: {runtime.get('latency_p95', 0.0):.4f}",
        f"- token_cost_per_record: {runtime.get('token_cost_per_record', 0.0):.2f}",
        f"- llm_effective_record_rate: {runtime.get('llm_effective_record_rate', 0.0):.4f}",
        f"- llm_fallback_only_record_rate: {runtime.get('llm_fallback_only_record_rate', 0.0):.4f}",
        "",
        "## Overall",
        f"- HAI: {report['HAI']:.2f}    (公式 v2 = 0.40·RAS + 0.30·SAS + 0.30·CRAS)",
        f"- HAI_legacy: {report.get('HAI_legacy', 0.0):.2f}    (公式 v1 = 0.55·RAS + 0.25·SAS + 0.20·PDS)",
        f"- PDS gate: {'PASS' if report.get('pds_gate', {}).get('passed') else 'FAIL'}    "
        f"(value={report.get('pds_gate', {}).get('value', 0.0):.2f}, threshold={report.get('pds_gate', {}).get('threshold', 95.0)})",
    ]
    return "\n".join(lines)


def _jsonable_report(report: dict[str, Any]) -> dict[str, Any]:
    jsonable = dict(report)
    jsonable["normalized_rows"] = [
        {key: value for key, value in row.items() if key != "result"}
        for row in report.get("normalized_rows", [])
    ]
    return jsonable


def _jsonable_phase7_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    return {
        "coverage": bundle["coverage"],
        "slice_report": _jsonable_report(bundle["slice_report"]),
        "full_report": _jsonable_report(bundle["full_report"]),
        "split_manifest": bundle["split_manifest"],
        "split_reports": {key: _jsonable_report(value) for key, value in bundle["split_reports"].items()},
        "split_summary": bundle["split_summary"],
        "lofo_manifest": bundle["lofo_manifest"],
        "lofo_reports": {key: _jsonable_report(value) for key, value in bundle["lofo_reports"].items()},
        "lofo_summary": bundle["lofo_summary"],
        "lofo_generalization": bundle["lofo_generalization"],
    }


def _jsonable_phase14_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    payload = _jsonable_phase7_bundle(bundle)
    payload.update(
        {
            "candidate_version": bundle["candidate_version"],
            "phase14_policy": bundle["phase14_policy"],
            "lockbox_residual_analysis": bundle["lockbox_residual_analysis"],
            "promotion_evaluation": bundle["promotion_evaluation"],
        }
    )
    return payload


def _jsonable_phase15_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    return {
        "comparison_scope": bundle["comparison_scope"],
        "split_name": bundle["split_name"],
        "candidate_model": bundle["candidate_model"],
        "provider_order": bundle["provider_order"],
        "baseline_payload": bundle["baseline_payload"],
        "candidate_payload": bundle["candidate_payload"],
        "comparison": bundle["comparison"],
    }


def _format_phase7_bundle(bundle: dict[str, Any]) -> str:
    coverage = bundle["coverage"]
    component_schema = coverage["component_alignment_schema"]
    full_error_map = bundle["full_report"]["error_map"]
    lines = [
        "# Phase 7 Evaluation Bundle",
        "",
        "## Coverage",
        f"- main record rows: {coverage['main_eval_rows']['record']}",
        f"- main summary rows: {coverage['main_eval_rows']['summary']}",
        f"- main component rows: {coverage['main_eval_rows']['component']}",
        f"- protocol rows: {coverage['main_eval_rows']['protocol']}",
        f"- deferred component rows: {coverage['deferred_rows']['component']}",
        f"- record families: {coverage['family_counts']['record']}",
        f"- summary families: {coverage['family_counts']['summary']}",
        f"- protocol families: {coverage['family_counts']['protocol']}",
        f"- component families: {coverage['family_counts']['component']}",
        "",
        "## Component Alignment Schema",
        f"- component rows: {component_schema['rows']}",
        f"- component families: {component_schema['family_count']}",
        f"- component cases: {component_schema.get('case_count', 0)}",
        f"- canonical components: {', '.join(component_schema['canonical_components']) if component_schema['canonical_components'] else 'none'}",
        f"- component source kinds: {json.dumps(component_schema.get('source_kind_counts', {}), ensure_ascii=False, sort_keys=True)}",
        "",
        "## Coverage Gaps",
    ]
    gaps = coverage.get("coverage_gaps", [])
    if gaps:
        lines.extend(f"- {item}" for item in gaps)
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Slice Report",
            f"- HAI: {bundle['slice_report']['HAI']:.2f}",
            f"- RAS: {bundle['slice_report']['record_metrics']['RAS']:.2f}",
            f"- SAS: {bundle['slice_report']['summary_metrics']['SAS']:.2f}",
            f"- PDS: {bundle['slice_report']['protocol_metrics']['PDS']:.2f}",
            "",
            "## Full Available Report",
            f"- HAI: {bundle['full_report']['HAI']:.2f}",
            f"- RAS: {bundle['full_report']['record_metrics']['RAS']:.2f}",
            f"- SAS: {bundle['full_report']['summary_metrics']['SAS']:.2f}",
            f"- CRAS: {bundle['full_report']['component_metrics']['CRAS']:.2f}",
            f"- PDS: {bundle['full_report']['protocol_metrics']['PDS']:.2f}",
            f"- record normalized_mae: {bundle['full_report']['record_metrics']['normalized_mae']:.4f}",
            f"- record spearman_rho: {bundle['full_report']['record_metrics']['spearman_rho']:.4f}",
            f"- summary spearman_rho: {bundle['full_report']['summary_metrics']['spearman_rho']:.4f}",
            f"- component macro_f1: {bundle['full_report']['component_metrics']['macro_f1']:.4f}",
            "",
            "## Split Metrics",
        ]
    )
    for split in SPLIT_ORDER:
        metrics = bundle["split_summary"][split]
        record_rows = bundle["split_manifest"]["regimes"]["record"][split]["rows"]
        summary_rows = bundle["split_manifest"]["regimes"]["summary"][split]["rows"]
        component_rows = bundle["split_manifest"]["regimes"]["component"][split]["rows"]
        protocol_rows = bundle["split_manifest"]["regimes"]["protocol"][split]["rows"]
        lines.append(
            f"- {split}: record={record_rows}, summary={summary_rows}, component={component_rows}, protocol={protocol_rows}, "
            f"HAI={metrics['HAI']:.2f}, RAS={metrics['RAS']:.2f}, SAS={metrics['SAS']:.2f}, CRAS={metrics['CRAS']:.2f}, PDS={metrics['PDS']:.2f}"
        )
    lines.extend(
        [
            "",
            "## LOFO Summary",
        ]
    )
    for regime_name, metrics in bundle["lofo_summary"].items():
        if regime_name == "record":
            lines.append(
                "- record: "
                f"families={metrics['family_count']}, "
                f"avg_RAS={metrics['avg_RAS']:.2f}, "
                f"min_RAS={metrics['min_RAS']:.2f}, "
                f"avg_normalized_mae={metrics['avg_normalized_mae']:.4f}, "
                f"avg_spearman_rho={metrics['avg_spearman_rho']:.4f}, "
                f"worst_family={metrics['worst_family']}"
            )
        elif regime_name == "summary":
            lines.append(
                "- summary: "
                f"families={metrics['family_count']}, "
                f"avg_SAS={metrics['avg_SAS']:.2f}, "
                f"min_SAS={metrics['min_SAS']:.2f}, "
                f"avg_normalized_mae={metrics['avg_normalized_mae']:.4f}, "
                f"avg_spearman_rho={metrics['avg_spearman_rho']:.4f}, "
                f"worst_family={metrics['worst_family']}"
            )
        elif regime_name == "component":
            lines.append(
                "- component: "
                f"families={metrics['family_count']}, "
                f"avg_CRAS={metrics['avg_CRAS']:.2f}, "
                f"min_CRAS={metrics['min_CRAS']:.2f}, "
                f"avg_macro_f1={metrics['avg_macro_f1']:.4f}, "
                f"avg_major_component_macro_f1={metrics['avg_major_component_macro_f1']:.4f}, "
                f"worst_family={metrics['worst_family']}"
            )
        elif regime_name == "protocol":
            lines.append(
                "- protocol: "
                f"families={metrics['family_count']}, "
                f"avg_PDS={metrics['avg_PDS']:.2f}, "
                f"min_PDS={metrics['min_PDS']:.2f}, "
                f"avg_vv_role_coverage={metrics['avg_vv_role_coverage']:.4f}, "
                f"worst_family={metrics['worst_family']}"
            )
    lines.extend(
        [
            "",
            "## LOFO Generalization",
        ]
    )
    for regime_name, metrics in bundle["lofo_generalization"].items():
        if regime_name == "record":
            lines.append(
                "- record: "
                f"full_RAS={metrics['full_RAS']:.2f}, "
                f"avg_gap_vs_full={metrics['avg_gap_vs_full']:.2f}, "
                f"worst_holdout_gap_vs_full={metrics['worst_holdout_gap_vs_full']:.2f}, "
                f"worst_family={metrics['worst_family']}"
            )
        elif regime_name == "summary":
            lines.append(
                "- summary: "
                f"full_SAS={metrics['full_SAS']:.2f}, "
                f"avg_gap_vs_full={metrics['avg_gap_vs_full']:.2f}, "
                f"worst_holdout_gap_vs_full={metrics['worst_holdout_gap_vs_full']:.2f}, "
                f"worst_family={metrics['worst_family']}"
            )
        elif regime_name == "component":
            lines.append(
                "- component: "
                f"full_CRAS={metrics['full_CRAS']:.2f}, "
                f"avg_gap_vs_full={metrics['avg_gap_vs_full']:.2f}, "
                f"worst_holdout_gap_vs_full={metrics['worst_holdout_gap_vs_full']:.2f}, "
                f"worst_family={metrics['worst_family']}"
            )
        elif regime_name == "protocol":
            lines.append(
                "- protocol: "
                f"full_PDS={metrics['full_PDS']:.2f}, "
                f"avg_gap_vs_full={metrics['avg_gap_vs_full']:.2f}, "
                f"worst_holdout_gap_vs_full={metrics['worst_holdout_gap_vs_full']:.2f}, "
                f"worst_family={metrics['worst_family']}"
            )
    lines.extend(
        [
            "",
            "## Full Error Map",
        ]
    )
    for bucket_name, count in full_error_map["bucket_counts"].items():
        lines.append(f"- {bucket_name}: {count}")
    ranking_risk = full_error_map.get("ranking_risk", {})
    if ranking_risk:
        lines.extend(
            [
                "",
                "## Ranking Risk",
                f"- record: risk={ranking_risk['record']['risk_level']}, spearman={ranking_risk['record']['spearman_rho']:.4f}, pairwise={ranking_risk['record']['pairwise_order_accuracy']:.4f}",
                f"- summary: risk={ranking_risk['summary']['risk_level']}, spearman={ranking_risk['summary']['spearman_rho']:.4f}, pairwise={ranking_risk['summary']['pairwise_order_accuracy']:.4f}",
            ]
        )
    return "\n".join(lines)


def _format_phase14_bundle(bundle: dict[str, Any]) -> str:
    validation_report = bundle["split_reports"]["validation"]
    lockbox_report = bundle["split_reports"]["lockbox"]
    lockbox_gate = bundle["promotion_evaluation"]["stages"]["lockbox"]
    lofo_gate = bundle["promotion_evaluation"]["stages"]["lofo"]
    residuals = bundle["lockbox_residual_analysis"]
    lines = [
        "# Phase 14 Generalization Bundle",
        "",
        "## Candidate",
        f"- candidate_version: {bundle['candidate_version']}",
        f"- default_acceptance_surface: {bundle['promotion_evaluation']['default_acceptance_surface']}",
        f"- promotion_status: {bundle['promotion_evaluation']['promotion_status']}",
        f"- generalization_evidence_ready: {bundle['promotion_evaluation']['generalization_evidence_ready']}",
        "",
        "## Split Policy",
        f"- split_order: {', '.join(bundle['phase14_policy']['split_order'])}",
        f"- split_ratios: {json.dumps(bundle['phase14_policy']['split_ratios'], ensure_ascii=False, sort_keys=True)}",
        f"- lockbox_max_core_metric_degrade: {bundle['phase14_policy']['lockbox_max_core_metric_degrade']:.2f}",
        "",
        "## Full Reference Metrics",
        f"- HAI: {bundle['full_report']['HAI']:.2f}",
        f"- RAS: {bundle['full_report']['record_metrics']['RAS']:.2f}",
        f"- SAS: {bundle['full_report']['summary_metrics']['SAS']:.2f}",
        f"- CRAS: {bundle['full_report']['component_metrics']['CRAS']:.2f}",
        f"- PDS: {bundle['full_report']['protocol_metrics']['PDS']:.2f}",
        "",
        "## Validation Metrics",
        f"- HAI: {validation_report['HAI']:.2f}",
        f"- RAS: {validation_report['record_metrics']['RAS']:.2f}",
        f"- SAS: {validation_report['summary_metrics']['SAS']:.2f}",
        f"- CRAS: {validation_report['component_metrics']['CRAS']:.2f}",
        f"- PDS: {validation_report['protocol_metrics']['PDS']:.2f}",
        "",
        "## Lockbox Metrics",
        f"- HAI: {lockbox_report['HAI']:.2f}",
        f"- RAS: {lockbox_report['record_metrics']['RAS']:.2f}",
        f"- SAS: {lockbox_report['summary_metrics']['SAS']:.2f}",
        f"- CRAS: {lockbox_report['component_metrics']['CRAS']:.2f}",
        f"- PDS: {lockbox_report['protocol_metrics']['PDS']:.2f}",
        "",
        "## Validation To Lockbox Core Delta",
    ]
    for metric_name in PHASE14_CORE_METRICS:
        metric = lockbox_gate["core_metric_deltas"][metric_name]
        lines.append(
            f"- {metric_name}: validation={metric['validation']:.2f}, lockbox={metric['lockbox']:.2f}, "
            f"degrade={metric['degrade']:.2f}, status={'pass' if metric['passed'] else 'fail'}"
        )
    lines.extend(
        [
            "",
            "## LOFO Generalization Gap",
        ]
    )
    for regime_name, metrics in lofo_gate["LOFO_generalization_gap"].items():
        lines.append(
            f"- {regime_name}: avg_gap_vs_full={metrics['avg_gap_vs_full']:.2f}, "
            f"worst_holdout_gap_vs_full={metrics['worst_holdout_gap_vs_full']:.2f}, "
            f"worst_family={metrics['worst_family']}"
        )
    lines.extend(
        [
            "",
            "## Lockbox Residual Analysis",
            f"- analyzed_rows: {residuals['analyzed_rows']}",
            f"- residual_rows: {residuals['residual_rows']}",
            f"- residual_row_rate: {residuals['residual_row_rate']:.4f}",
            f"- bucket_counts: {json.dumps(residuals['bucket_counts'], ensure_ascii=False, sort_keys=True)}",
        ]
    )
    if residuals["clusters"]:
        lines.append("")
        lines.append("## Lockbox Residual Clusters")
        for cluster in residuals["clusters"]:
            lines.append(
                "- "
                f"{cluster['eval_bucket']} / {cluster['primary_bucket']} / {cluster['focus_key']}: "
                f"rows={cluster['rows']}, families={cluster['family_count']}, "
                f"avg_abs_score_delta={cluster['avg_abs_score_delta']:.4f}, "
                f"avg_issue_f1={cluster['avg_issue_f1']:.4f}, "
                f"sample_families={json.dumps(cluster['sample_families'], ensure_ascii=False)}, "
                f"sample_task_ids={json.dumps(cluster['sample_task_ids'], ensure_ascii=False)}"
            )
    lines.extend(
        [
            "",
            "## Promotion Stages",
            f"- validation: {bundle['promotion_evaluation']['stages']['validation']['status']}",
            f"- lockbox: {lockbox_gate['status']} (max_observed_degrade={lockbox_gate.get('max_observed_degrade', 0.0):.2f})",
            f"- lofo: {lofo_gate['status']} (max_avg_gap_vs_full={lofo_gate.get('max_avg_gap_vs_full', 0.0):.2f}, "
            f"max_worst_holdout_gap_vs_full={lofo_gate.get('max_worst_holdout_gap_vs_full', 0.0):.2f})",
            f"- residual_audit: {bundle['promotion_evaluation']['stages']['residual_audit']['status']}",
        ]
    )
    return "\n".join(lines)


def _format_phase15_bundle(bundle: dict[str, Any]) -> str:
    comparison = bundle["comparison"]
    delta = comparison["delta"]
    baseline_runtime = comparison["baseline_runtime"]
    candidate_runtime = comparison["candidate_runtime"]
    lines = [
        "# Phase 15 Comparison Bundle",
        "",
        "## Scope",
        f"- comparison_scope: {bundle['comparison_scope']}",
        f"- split_name: {bundle['split_name'] or 'n/a'}",
        f"- candidate_model: {bundle['candidate_model']}",
        f"- provider_order: {json.dumps(bundle['provider_order'], ensure_ascii=False)}",
        "",
        "## Alignment Delta",
        f"- HAI: {delta['HAI']:.2f}",
        f"- RAS: {delta['RAS']:.2f}",
        f"- SAS: {delta['SAS']:.2f}",
        f"- CRAS: {delta['CRAS']:.2f}",
        f"- PDS: {delta['PDS']:.2f}",
        f"- record_spearman_rho: {delta['record_spearman_rho']:.4f}",
        f"- record_pairwise_order_accuracy: {delta['record_pairwise_order_accuracy']:.4f}",
        f"- summary_spearman_rho: {delta['summary_spearman_rho']:.4f}",
        f"- summary_pairwise_order_accuracy: {delta['summary_pairwise_order_accuracy']:.4f}",
        f"- weighted_kappa: {delta['weighted_kappa']:.4f}",
        "",
        "## Stability / Confidence Delta",
        f"- confidence_mean: {delta['confidence_mean']:.4f}",
        f"- rerun_score_std: {delta['rerun_score_std']:.4f}",
        f"- issue_jaccard_across_runs: {delta['issue_jaccard_across_runs']:.4f}",
        "",
        "## Runtime Delta",
        f"- latency_p50: {delta['latency_p50']:.4f}",
        f"- latency_p95: {delta['latency_p95']:.4f}",
        f"- token_cost_per_record: {delta['token_cost_per_record']:.2f}",
        f"- llm_effective_record_rate: {delta['llm_effective_record_rate']:.4f}",
        f"- llm_fallback_only_record_rate: {delta['llm_fallback_only_record_rate']:.4f}",
        "",
        "## Candidate Runtime",
        f"- latency_p50: {candidate_runtime.get('latency_p50', 0.0):.4f}",
        f"- latency_p95: {candidate_runtime.get('latency_p95', 0.0):.4f}",
        f"- token_cost_per_record: {candidate_runtime.get('token_cost_per_record', 0.0):.2f}",
        f"- llm_effective_record_rate: {candidate_runtime.get('llm_effective_record_rate', 0.0):.4f}",
        f"- llm_fallback_only_record_rate: {candidate_runtime.get('llm_fallback_only_record_rate', 0.0):.4f}",
        f"- llm_total_tokens: {candidate_runtime.get('llm_total_tokens', 0)}",
        "",
        "## Baseline Runtime",
        f"- latency_p50: {baseline_runtime.get('latency_p50', 0.0):.4f}",
        f"- latency_p95: {baseline_runtime.get('latency_p95', 0.0):.4f}",
        f"- token_cost_per_record: {baseline_runtime.get('token_cost_per_record', 0.0):.2f}",
        "",
        "## Recommendation",
        f"- default_path_recommendation: {comparison['default_path_recommendation']}",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark-dir", type=Path, default=DEFAULT_BENCHMARK_DIR)
    parser.add_argument("--record-limit", type=int, default=18)
    parser.add_argument("--summary-limit", type=int, default=16)
    parser.add_argument("--component-limit", type=int, default=24)
    parser.add_argument("--protocol-limit", type=int, default=4)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--rerun-count", type=int, default=4)
    parser.add_argument("--llm-mode", choices=["off", "auto"], default="off")
    parser.add_argument("--scope", choices=["slice", "full", "split", "phase7", "phase14", "phase15"], default="slice")
    parser.add_argument("--split-name", choices=SPLIT_ORDER, default=None)
    parser.add_argument("--candidate-version", type=str, default=None)
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--provider-order", nargs="*", default=None)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--phase15-comparison-scope", choices=["slice", "full", "split", "phase14"], default="full")
    parser.add_argument("--output-markdown", type=Path, default=None)
    parser.add_argument("--output-json", type=Path, default=None)
    args = parser.parse_args()
    if args.scope == "phase7":
        payload = run_phase7_evaluation_bundle(
            base_dir=args.benchmark_dir,
            record_limit=args.record_limit,
            summary_limit=args.summary_limit,
            component_limit=args.component_limit,
            protocol_limit=args.protocol_limit,
            seed=args.seed,
            rerun_count=args.rerun_count,
            llm_mode=args.llm_mode,
            model=args.model,
            provider_order=args.provider_order,
            temperature=args.temperature,
            timeout=args.timeout,
        )
        markdown = _format_phase7_bundle(payload)
        if args.output_markdown is not None:
            args.output_markdown.write_text(markdown + "\n", encoding="utf-8")
        if args.output_json is not None:
            args.output_json.write_text(
                json.dumps(_jsonable_phase7_bundle(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        print(markdown)
        return
    if args.scope == "phase14":
        payload = run_phase14_evaluation_bundle(
            base_dir=args.benchmark_dir,
            record_limit=args.record_limit,
            summary_limit=args.summary_limit,
            component_limit=args.component_limit,
            protocol_limit=args.protocol_limit,
            seed=args.seed,
            rerun_count=args.rerun_count,
            llm_mode=args.llm_mode,
            candidate_version=args.candidate_version,
            model=args.model,
            provider_order=args.provider_order,
            temperature=args.temperature,
            timeout=args.timeout,
        )
        markdown = _format_phase14_bundle(payload)
        if args.output_markdown is not None:
            args.output_markdown.write_text(markdown + "\n", encoding="utf-8")
        if args.output_json is not None:
            args.output_json.write_text(
                json.dumps(_jsonable_phase14_bundle(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        print(markdown)
        return
    if args.scope == "phase15":
        payload = run_phase15_comparison_bundle(
            base_dir=args.benchmark_dir,
            record_limit=args.record_limit,
            summary_limit=args.summary_limit,
            component_limit=args.component_limit,
            protocol_limit=args.protocol_limit,
            seed=args.seed,
            rerun_count=args.rerun_count,
            comparison_scope=args.phase15_comparison_scope,
            split_name=args.split_name,
            candidate_version=args.candidate_version,
            model=args.model,
            provider_order=args.provider_order,
            temperature=args.temperature,
            timeout=args.timeout,
        )
        markdown = _format_phase15_bundle(payload)
        if args.output_markdown is not None:
            args.output_markdown.write_text(markdown + "\n", encoding="utf-8")
        if args.output_json is not None:
            args.output_json.write_text(
                json.dumps(_jsonable_phase15_bundle(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        print(markdown)
        return

    report = run_benchmark_iteration(
        base_dir=args.benchmark_dir,
        record_limit=args.record_limit,
        summary_limit=args.summary_limit,
        component_limit=args.component_limit,
        protocol_limit=args.protocol_limit,
        seed=args.seed,
        rerun_count=args.rerun_count,
        llm_mode=args.llm_mode,
        scope=args.scope,
        split_name=args.split_name,
        model=args.model,
        provider_order=args.provider_order,
        temperature=args.temperature,
        timeout=args.timeout,
    )
    markdown = _format_report(report)
    if args.output_markdown is not None:
        args.output_markdown.write_text(markdown + "\n", encoding="utf-8")
    if args.output_json is not None:
        args.output_json.write_text(
            json.dumps(_jsonable_report(report), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(markdown)


if __name__ == "__main__":
    main()
