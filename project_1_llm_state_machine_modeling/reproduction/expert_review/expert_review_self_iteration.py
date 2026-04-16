from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from .expert_review_agent import ExpertReviewAgent
from .expert_review_schema import ExpertReviewRequest, ExpertReviewResult


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


@dataclass(slots=True)
class BenchmarkTask:
    task_id: str
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


def _load_benchmark_tables(base_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    records = pd.read_parquet(base_dir / "baseline_double_green_human_review_records.parquet")
    protocols = pd.read_parquet(base_dir / "baseline_double_green_human_review_protocols.parquet")
    availability = pd.read_parquet(base_dir / "baseline_double_green_human_review_availability.parquet")
    return records, protocols, availability


def _normalize_score(value: Any, unit: Any) -> float | None:
    if value is None:
        return None
    try:
        score = float(value)
    except Exception:
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


def _build_record_prompt(row: pd.Series) -> str:
    rubric = _safe_text(row.get("review_rubric_text")).strip()
    limitations = _safe_text(row.get("public_artifact_limitations")).strip()
    diagram_type = _safe_text(row.get("diagram_type")).strip() or "model"
    target = _safe_text(row.get("review_target")).strip() or "generated artifact"
    return (
        "You are an expert reviewer for generated software modeling artifacts.\n"
        f"Target type: {diagram_type} / {target}.\n"
        "Treat the prompt as a review contract, not as a generation request.\n"
        "Focus on semantic adequacy, behavioral consistency, requirement traceability, unsupported extra structure, "
        "and equivalent-but-different designs.\n"
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
    return (
        "You are an expert reviewer for generated software modeling artifacts under partial public evidence.\n"
        f"This is a summary-level task for {target}.\n"
        f"Public summary row semantics: {summary_semantics}\n"
        "Give an overall review that respects evidence limits. Do not invent precise element-level mismatch claims "
        "when the public evidence only supports overall judgement. If the contract refers to average/max/min/std-dev "
        "style published statistics, calibrate the coarse score to that public summary semantics rather than pretending "
        "you saw hidden per-run annotations.\n"
        f"Public row note:\n{public_summary or 'No extra public row note was recorded.'}\n"
        f"Public rubric:\n{rubric or 'No explicit rubric text was published for this row.'}\n"
        f"Public limitations:\n{limitations or 'No extra public limitations were recorded.'}"
    )


def _summary_semantics_from_row(row: pd.Series) -> str:
    review_record_id = _safe_text(row.get("review_record_id")).lower()
    record_type = _safe_text(row.get("record_type")).lower()
    if any(token in review_record_id for token in ["std_dev", "std dev", "stddev"]) or "std" in review_record_id:
        return "This published row is a standard-deviation or dispersion statistic."
    if "average" in review_record_id or record_type in {"summary", "case_aggregate_stat", "overall_aggregate_stat"}:
        return "This published row is an average or aggregate quality statistic."
    if any(token in review_record_id for token in [":max", "maximum", "highest"]):
        return "This published row is a highest-score or best-case aggregate statistic."
    if any(token in review_record_id for token in [":min", "minimum", "lowest"]):
        return "This published row is a minimum-score or worst-case aggregate statistic."
    if record_type == "raw_score_row":
        return "This published row is a raw public score row without per-element justification."
    if record_type == "summary_level_run_score":
        return "This published row is a run-level summary score."
    return "This published row is a public summary-level score."


def _build_protocol_prompt(row: pd.Series) -> str:
    return (
        "You are an expert reviewer of a human evaluation protocol for software modeling artifacts.\n"
        "There is no full per-record prediction/reference evidence in this task. Review what the protocol can validate, "
        "which V&V roles it uses, and what claims should remain uncertain.\n"
        "Do not fabricate precise artifact-level findings."
    )


def _build_record_task(row: pd.Series) -> BenchmarkTask:
    return BenchmarkTask(
        task_id=str(row["review_record_id"]),
        regime_expected="record_level",
        prompt=_build_record_prompt(row),
        input_text=_safe_text(row.get("input_text")),
        pred_output=_truncate_artifact(row.get("pred_output_text"), 12000),
        ref_output=_truncate_artifact(row.get("ref_output_text"), 12000) or None,
        human_score=_normalize_score(row.get("human_review_score"), row.get("human_review_score_unit")),
        human_score_unit=_safe_text(row.get("human_review_score_unit")) or None,
        human_issue_set=_human_issue_set_from_record(row),
        group_key=f"{row.get('paper_slug')}::{row.get('diagram_type')}::{row.get('review_target')}",
        metadata={
            "paper_slug": row.get("paper_slug"),
            "record_type": row.get("record_type"),
            "diagram_type": row.get("diagram_type"),
            "review_target": row.get("review_target"),
        },
    )


def _build_summary_task(row: pd.Series) -> BenchmarkTask:
    return BenchmarkTask(
        task_id=str(row["review_record_id"]),
        regime_expected="summary_level",
        prompt=_build_summary_prompt(row),
        input_text=_safe_text(row.get("input_text")),
        pred_output=_truncate_artifact(row.get("pred_output_text"), 9000),
        ref_output=None,
        human_score=_normalize_score(row.get("human_review_score"), row.get("human_review_score_unit")),
        human_score_unit=_safe_text(row.get("human_review_score_unit")) or None,
        human_issue_set=_human_issue_set_from_record(row),
        group_key=f"{row.get('paper_slug')}::{row.get('review_target')}::{row.get('record_type')}",
        metadata={
            "paper_slug": row.get("paper_slug"),
            "record_type": row.get("record_type"),
            "diagram_type": row.get("diagram_type"),
            "review_target": row.get("review_target"),
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
        regime_expected="protocol_only",
        prompt=_build_protocol_prompt(row),
        input_text=input_text,
        pred_output="",
        ref_output=None,
        human_score=None,
        human_score_unit=None,
        human_issue_set=protocol_issue_set,
        group_key=f"protocol::{row.get('paper_slug')}",
        metadata={"paper_slug": row.get("paper_slug"), "record_type": "protocol_only"},
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
    protocol_limit: int,
    seed: int,
) -> dict[str, list[BenchmarkTask]]:
    strong_record_df = records[
        (records["record_type"] == "sample_level_review")
        & records["pred_output_text"].notna()
        & records["input_text"].notna()
        & records["ref_output_text"].notna()
    ].copy()
    summary_df = records[
        records["record_type"].isin(
            ["summary_level_run_score", "case_aggregate_stat", "raw_score_row", "summary"]
        )
        & records["pred_output_text"].notna()
    ].copy()
    sampled_record_df = _sample_grouped(strong_record_df, record_limit, ["paper_slug", "record_type", "review_target"], seed)
    sampled_summary_df = _sample_grouped(summary_df, summary_limit, ["paper_slug", "record_type", "review_target"], seed + 1)
    sampled_protocol_df = protocols.head(protocol_limit).copy()
    return {
        "record": [_build_record_task(row) for _, row in sampled_record_df.iterrows()],
        "summary": [_build_summary_task(row) for _, row in sampled_summary_df.iterrows()],
        "protocol": [_build_protocol_task(row) for _, row in sampled_protocol_df.iterrows()],
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
) -> dict[str, tuple[float, float]]:
    result: dict[str, tuple[float, float]] = {}
    for task in tasks[:rerun_count]:
        request = ExpertReviewRequest(
            prompt=task.prompt,
            input_text=task.input_text,
            pred_output=task.pred_output,
            ref_output=task.ref_output,
        )
        first = agent.review(request)
        second = agent.review(request)
        issue_first = _agent_issue_set(first)
        issue_second = _agent_issue_set(second)
        union = len(issue_first | issue_second)
        jaccard = len(issue_first & issue_second) / union if union else 1.0
        result[task.task_id] = (abs(first.overall_score - second.overall_score), jaccard)
    return result


def run_benchmark_iteration(
    *,
    base_dir: Path = DEFAULT_BENCHMARK_DIR,
    record_limit: int = 18,
    summary_limit: int = 16,
    protocol_limit: int = 4,
    seed: int = 7,
    rerun_count: int = 4,
    llm_mode: str = "off",
) -> dict[str, Any]:
    records, protocols, _availability = _load_benchmark_tables(base_dir)
    slices = build_benchmark_slices(
        records,
        protocols,
        record_limit=record_limit,
        summary_limit=summary_limit,
        protocol_limit=protocol_limit,
        seed=seed,
    )
    provider_order = None if llm_mode == "auto" else []
    agent = ExpertReviewAgent(provider_order=provider_order)
    reruns = _rerun_subset(agent, slices["record"][:rerun_count] + slices["summary"][:rerun_count], rerun_count=rerun_count)

    normalized_rows: list[dict[str, Any]] = []
    for regime_name, tasks in slices.items():
        for task in tasks:
            request = ExpertReviewRequest(
                prompt=task.prompt,
                input_text=task.input_text,
                pred_output=task.pred_output,
                ref_output=task.ref_output,
            )
            start = time.perf_counter()
            result = agent.review(request)
            latency = time.perf_counter() - start
            agent_issue_set = _agent_issue_set(result)
            issue_precision, issue_recall, issue_f1 = _issue_f1(task.human_issue_set, agent_issue_set)
            rerun_score_delta, rerun_issue_jaccard = reruns.get(task.task_id, (0.0, 1.0))
            normalized_rows.append(
                {
                    "task_id": task.task_id,
                    "expected_regime": task.regime_expected,
                    "actual_regime": _regime_from_result(result),
                    "human_score": task.human_score,
                    "agent_score": result.overall_score,
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
                    "metadata": task.metadata,
                    "result": result,
                }
            )

    record_rows = [row for row in normalized_rows if row["expected_regime"] == "record_level"]
    summary_rows = [row for row in normalized_rows if row["expected_regime"] == "summary_level"]
    protocol_rows = [row for row in normalized_rows if row["expected_regime"] == "protocol_only"]

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

    protocol_metrics = _protocol_metrics(protocol_rows)
    hai = 0.55 * ras + 0.25 * sas + 0.20 * protocol_metrics["PDS"]

    return {
        "sample_sizes": {
            "record": len(record_rows),
            "summary": len(summary_rows),
            "protocol": len(protocol_rows),
        },
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
        "protocol_metrics": protocol_metrics,
        "HAI": hai,
        "normalized_rows": normalized_rows,
    }


def _format_report(report: dict[str, Any]) -> str:
    sample_sizes = report["sample_sizes"]
    record = report["record_metrics"]
    summary = report["summary_metrics"]
    protocol = report["protocol_metrics"]
    lines = [
        "# Alignment Report",
        "",
        "## Sample Sizes",
        f"- record: {sample_sizes['record']}",
        f"- summary: {sample_sizes['summary']}",
        f"- protocol: {sample_sizes['protocol']}",
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
        "## Protocol Metrics",
        f"- regime_accuracy: {protocol['regime_accuracy']:.4f}",
        f"- protocol_only_overclaim_rate: {protocol['protocol_only_overclaim_rate']:.4f}",
        f"- vv_role_coverage: {protocol['vv_role_coverage']:.4f}",
        f"- confidence_discipline: {protocol['confidence_discipline']:.4f}",
        f"- PDS: {protocol['PDS']:.2f}",
        "",
        "## Overall",
        f"- HAI: {report['HAI']:.2f}",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark-dir", type=Path, default=DEFAULT_BENCHMARK_DIR)
    parser.add_argument("--record-limit", type=int, default=18)
    parser.add_argument("--summary-limit", type=int, default=16)
    parser.add_argument("--protocol-limit", type=int, default=4)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--rerun-count", type=int, default=4)
    parser.add_argument("--llm-mode", choices=["off", "auto"], default="off")
    args = parser.parse_args()
    report = run_benchmark_iteration(
        base_dir=args.benchmark_dir,
        record_limit=args.record_limit,
        summary_limit=args.summary_limit,
        protocol_limit=args.protocol_limit,
        seed=args.seed,
        rerun_count=args.rerun_count,
        llm_mode=args.llm_mode,
    )
    print(_format_report(report))


if __name__ == "__main__":
    main()
