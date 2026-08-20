"""Independent semantic hit/false-positive adjudication for the Luna matrix.

The judge receives the frozen ledger for one pair and all six emitted cells
(method/baseline x three rounds). It decides semantic correspondence from the
full claim, location, and reason; this module contains no lexical matching,
similarity score, or keyword shortcut.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, ValidationError

ROOT = Path(__file__).resolve().parents[6]
FEEDBACK_SRC = (
    ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/feedback_loop/src"
)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(FEEDBACK_SRC) not in sys.path:
    sys.path.insert(0, str(FEEDBACK_SRC))

from paper_stm_feedback_loop.discover.responder import (
    DEFAULT_TRANSPORT_RETRIES,
    DirectStructuredResponder,
    StructuredOutputValidationError,
)

Arm = Literal["method", "baseline"]
Cell = Literal[
    "method_run1",
    "method_run2",
    "method_run3",
    "baseline_run1",
    "baseline_run2",
    "baseline_run3",
]

MAX_PROVIDER_RETRY_BURSTS = 8
MAX_ATOMIC_SCHEMA_REPAIRS = 3


class ProviderRetryExhausted(RuntimeError):
    """Provider-only retries ended; the caller must preserve an audit result."""


class HitAssessment(BaseModel):
    """Semantic coverage decision for one ledger item in one frozen output cell."""

    hit: bool = Field(
        description="True only when the supplied output semantically covers the ledger item's location and property."
    )
    supporting_finding_ids: list[str] = Field(
        default_factory=list,
        description="Exact emitted issue IDs supporting a true decision; empty for a miss.",
    )
    reason: str = Field(
        min_length=1,
        description="Concise semantic basis for the decision, grounded only in the supplied inputs.",
    )
    confidence: Literal["high", "medium", "low"] | None = Field(
        default=None,
        description="Reviewer confidence in this semantic correspondence decision.",
    )


class LedgerAssessment(BaseModel):
    """Complete six-cell coverage assessment for one ledger item."""

    ledger_id: str = Field(description="Exact supplied ledger item identifier.")
    method_run1: HitAssessment = Field(description="Coverage decision for method run 1.")
    method_run2: HitAssessment = Field(description="Coverage decision for method run 2.")
    method_run3: HitAssessment = Field(description="Coverage decision for method run 3.")
    baseline_run1: HitAssessment = Field(description="Coverage decision for baseline run 1.")
    baseline_run2: HitAssessment = Field(description="Coverage decision for baseline run 2.")
    baseline_run3: HitAssessment = Field(description="Coverage decision for baseline run 3.")


class EmissionAssessment(BaseModel):
    """Semantic correspondence and false-positive decision for one emitted issue."""

    cell: Cell = Field(description="Frozen output cell containing the emitted issue.")
    emitted_id: str = Field(description="Exact emitted issue identifier within the cell.")
    matched_ledger_ids: list[str] = Field(
        default_factory=list,
        description="Supplied ledger item IDs semantically covered by this issue; empty means no correspondence.",
    )
    false_positive: bool = Field(
        description="True when this emitted D1/D2 issue has no valid semantic ledger correspondence."
    )
    reason: str = Field(
        min_length=1,
        description="Concise semantic basis for the correspondence or false-positive decision.",
    )
    confidence: Literal["high", "medium", "low"] | None = Field(
        default=None,
        description="Reviewer confidence in this semantic correspondence decision.",
    )


class PairJudgement(BaseModel):
    """Structured independent judgement for all supplied ledger items and emissions of one pair."""

    pair: str = Field(description="Pair identifier supplied by the evaluation harness.")
    ledger_assessments: list[LedgerAssessment] = Field(
        description="One complete six-cell assessment for every supplied ledger item."
    )
    emission_assessments: list[EmissionAssessment] = Field(
        description="One correspondence assessment for every supplied emitted issue."
    )
    pair_reason: str = Field(
        min_length=1,
        description="Short audit summary of the pair-level semantic judgement; do not add new issues.",
    )


class AtomicMatchDecision(BaseModel):
    """Single semantic ledger-to-emission correspondence decision used by fallback judging."""

    matches: bool = Field(
        description="True only when the two supplied claims identify the same location and property."
    )
    reason: str = Field(
        min_length=1,
        description="Concise semantic reason based only on this ledger/emission pair.",
    )
    confidence: Literal["high", "medium", "low"] = Field(
        description="Reviewer confidence in the atomic correspondence decision."
    )


SYSTEM_PROMPT = """你是独立的状态机缺陷覆盖评审员。你的任务是把一个 pair 的冻结台账条目与两个被测臂的六个输出格做语义对齐。你只能依据本次输入中的自然语言规格、PlantUML/FCSTM 相关定位、台账条目的完整主张，以及输出 issue 的完整主张作判断；不得使用关键词命中、字符串包含、编辑距离、向量相似度或任何其他词法捷径。

命中判据必须同时满足：1）同一处：输出指认的元素或位置与台账指认的是同一状态、迁移、事件、区域或表达式；2）同一性质：输出主张的是同一种缺失、多余、错位、不可达、无出路、不终止、层次归属、记法槽位或数量问题。措辞不同、只描述后果、没有可执行断言都不影响覆盖命中。只在背景中顺带提到元素、只说上位类别、方向相反，或把多条输出拼起来才能凑成台账主张，都不算命中。

方法侧输入已经是末端可发布 issue：仅含 D2 或 D1 的 `report_issue_clusters`。D0 审计发现不在本次输入中，也绝不能间接计入命中或 false positive。对每个台账条目，六个格都必须给出 hit、支持该命中的 issue id、语义理由和置信度。对每个格中的每一条输出也必须给出是否为 false positive；若它语义上对应台账条目，列出一个或多个对应 ledger id，否则标记 false_positive=true。一个输出 issue 可以覆盖至多条台账，但只有确实同处同性质时才允许。不要因为有正式证书就自动命中，证书只作为主张的一部分；也不要因为没有证书就自动否定覆盖。

这是测量覆盖的独立评审，不是重新修改台账，不得创造新的台账条目。请完整返回要求的结构化对象，不要省略零命中条目或没有 finding 的格。"""

ATOMIC_SYSTEM_PROMPT = """你是独立的状态机缺陷覆盖评审员。现在只裁定一个冻结台账条目与一个被测系统输出 issue 是否语义对应。matches=true 当且仅当二者同时满足“同一处”和“同一性质”：指认同一个状态、迁移、事件、区域或表达式，并主张同一种缺失、多余、错位、不可达、无出路、不终止、层次归属、记法槽位或数量问题。只描述后果、只说上位类别、方向相反或需要与别的 issue 拼接才能覆盖完整台账主张时，必须判 false。不得使用关键词、字符串包含、编辑距离、向量相似度或任何词法捷径。只能裁定输入中的这一对，不得创造台账条目，不得引用其它 emission。请给出明确的语义理由和置信度。"""


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _compact_method_report_issue(item: dict[str, Any]) -> dict[str, Any]:
    """Serialize one final D1/D2 issue cluster for the independent judge.

    Raw finding facets, including D0 audit observations, are intentionally not
    part of the evaluation surface.  The cluster is the method's final output.
    """

    return {
        "finding_id": item.get("report_issue_id") or item.get("cause_key"),
        "claims": item.get("claims", []),
        "locations": item.get("locations", []),
        "obligations": item.get("obligations", []),
        "basis": item.get("source_attribution", []),
        "d_level": item.get("d_level"),
        "l_level": item.get("l_level"),
        "witness_level": item.get("witness_level"),
        "facet_count": item.get("facet_count"),
        "facet_keys": item.get("facet_keys", []),
    }


def _compact_baseline_issue(item: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "finding_id": f"baseline_issue_{index + 1}",
        "issue": item.get("issue"),
        "reason": item.get("reason"),
        "where": item.get("where"),
    }


def _ledger_payload(items: dict[str, Any], pair: str) -> list[dict[str, Any]]:
    return [
        {
            "ledger_id": row["id"],
            "pair": row["pair"],
            "D": row["D"],
            "L": row["L"],
            "summary": row["summary"],
            "detail": row["detail"],
            "D_basis": row["D_basis"],
            "L_basis": row["L_basis"],
            "axes": row.get("axes", {}),
        }
        for row in items.values()
        if row.get("pair") == pair
    ]


def _cell_payload(root: Path, arm: Arm, pair: str, run: int) -> dict[str, Any]:
    folder = root / f"run{run}" / f"{pair}-luna" / "record.json"
    if arm == "baseline" and not folder.exists():
        folder = root / f"run{run}" / f"{pair}-luna-x1v2" / "record.json"
    if not folder.exists():
        return {"cell": f"{arm}_run{run}", "status": "missing", "findings": []}
    record = _read_json(folder)
    if arm == "method":
        findings = [
            _compact_method_report_issue(item)
            for item in record.get("report_issue_clusters", [])
            if item.get("d_level") in {"D1", "D2"}
        ]
        return {
            "cell": f"{arm}_run{run}",
            "status": record.get("status") or "ok",
            "findings": findings,
        }
    parsed = record.get("parsed_output") or {}
    findings = [
        _compact_baseline_issue(item, index)
        for index, item in enumerate(parsed.get("issues", []))
        if isinstance(item, dict)
    ]
    return {
        "cell": f"{arm}_run{run}",
        "status": record.get("status"),
        "findings": findings,
    }


def _expected_emission_ids(cells: list[dict[str, Any]]) -> set[tuple[str, str]]:
    return {
        (str(cell["cell"]), str(finding["finding_id"]))
        for cell in cells
        for finding in cell.get("findings", [])
    }


def _drop_unknown_emission_rows(
    result: PairJudgement,
    cells: list[dict[str, Any]],
) -> PairJudgement:
    """Remove structural placeholder rows that do not name an input emission.

    This is exact-ID normalization only. It never creates a relation, fills a
    missing assessment, or changes any semantic decision for a real emission.
    """

    expected = _expected_emission_ids(cells)
    result.emission_assessments = [
        row
        for row in result.emission_assessments
        if (row.cell, row.emitted_id) in expected
    ]
    return result


def _observation_audit(observation: Any) -> dict[str, Any]:
    """Serialize billing and failure evidence without retaining prompt bodies."""

    return {
        "llm_call_id": observation.llm_call_id,
        "role": observation.role,
        "profile": observation.profile,
        "adapter": observation.adapter,
        "provider": observation.provider,
        "streaming": getattr(observation, "streaming", None),
        "configured_model": observation.configured_model,
        "observed_model": observation.observed_model,
        "started_at": observation.started_at.isoformat(),
        "finished_at": observation.finished_at.isoformat(),
        "elapsed_ms": observation.elapsed_ms,
        "status": observation.status,
        "usage": observation.usage,
        "attempts": list(observation.attempts),
        "structured_schema_sha256": observation.structured_schema_sha256,
        "prompt_cache": observation.prompt_cache,
        "pricing": observation.pricing,
        "failure": observation.failure,
    }


def _provider_failure_only(observation: Any) -> bool:
    attempts = list(getattr(observation, "attempts", ()))
    return bool(attempts) and all(
        attempt.get("status") == "failed"
        and attempt.get("retryable") is True
        and attempt.get("failure_phase") in {"provider_response", "transport"}
        for attempt in attempts
    )


def _invoke_judge(
    *,
    responder: DirectStructuredResponder,
    role: str,
    schema: type[BaseModel],
    system_prompt: str,
    user_input: str,
    observations: list[dict[str, Any]],
) -> BaseModel:
    """Invoke one semantic decision, persisting through provider outages.

    A responder budget bounds one transport burst, not the existence of the
    final judgement. If every attempt in that burst is a typed provider error,
    the same prompt is resent in this process. The terminal attempt of the old
    burst is then exempt because a real retry follows it.
    """

    for provider_burst in range(MAX_PROVIDER_RETRY_BURSTS + 1):
        try:
            result = responder.invoke_structured(
                role=role,
                schema=schema,
                system_prompt=system_prompt,
                user_input=user_input,
            )
        except Exception:
            observation = responder.take_last_observation()
            if observation is not None and _provider_failure_only(observation):
                audit = _observation_audit(observation)
                terminal = audit["attempts"][-1]
                terminal["cost_counted"] = False
                terminal["billing_disposition"] = "provider_error_retry_exempt"
                terminal["retry_after_seconds"] = 240.0
                observations.append(audit)
                if provider_burst >= MAX_PROVIDER_RETRY_BURSTS:
                    raise ProviderRetryExhausted(
                        "provider retries exhausted after "
                        f"{MAX_PROVIDER_RETRY_BURSTS} retry bursts"
                    )
                time.sleep(240.0)
                continue
            if observation is not None:
                observations.append(_observation_audit(observation))
            raise
        observation = responder.take_last_observation()
        if observation is not None:
            observations.append(_observation_audit(observation))
        return result
    raise ProviderRetryExhausted("provider retry loop terminated without a result")


def _validate_shape(
    result: PairJudgement, ledger: list[dict[str, Any]], cells: list[dict[str, Any]]
) -> list[str]:
    errors: list[str] = []
    expected_ledger = {str(row["ledger_id"]) for row in ledger}
    expected_by_cell = {
        str(cell["cell"]): {
            str(finding["finding_id"]) for finding in cell.get("findings", [])
        }
        for cell in cells
    }
    supplied_ledger = {row.ledger_id for row in result.ledger_assessments}
    if supplied_ledger != expected_ledger:
        errors.append(
            "ledger_assessments must contain each supplied ledger_id exactly once"
        )
    if len(supplied_ledger) != len(result.ledger_assessments):
        errors.append("ledger_assessments contains duplicate ledger_id")
    expected_emissions = _expected_emission_ids(cells)
    supplied_emissions = {
        (row.cell, row.emitted_id) for row in result.emission_assessments
    }
    if supplied_emissions != expected_emissions:
        errors.append(
            "emission_assessments must contain each supplied emitted issue exactly once"
        )
    if len(supplied_emissions) != len(result.emission_assessments):
        errors.append("emission_assessments contains duplicate cell/emitted_id")
    for assessment in result.ledger_assessments:
        for field in (
            "method_run1",
            "method_run2",
            "method_run3",
            "baseline_run1",
            "baseline_run2",
            "baseline_run3",
        ):
            hit = getattr(assessment, field)
            if any(not isinstance(item, str) for item in hit.supporting_finding_ids):
                errors.append(
                    f"{assessment.ledger_id}.{field} has invalid supporting id"
                )
                continue
            supporting_ids = set(hit.supporting_finding_ids)
            unknown_ids = supporting_ids - expected_by_cell[field]
            if unknown_ids:
                errors.append(
                    f"{assessment.ledger_id}.{field} references unknown supporting ids: "
                    + ", ".join(sorted(unknown_ids))
                )
            if hit.hit and not supporting_ids:
                errors.append(
                    f"{assessment.ledger_id}.{field} hit requires a supporting id"
                )
            if not hit.hit and supporting_ids:
                errors.append(
                    f"{assessment.ledger_id}.{field} miss must not carry supporting ids"
                )
    for assessment in result.emission_assessments:
        matched_ledger = set(assessment.matched_ledger_ids)
        unknown_ledger = matched_ledger - expected_ledger
        if unknown_ledger:
            errors.append(
                f"{assessment.cell}.{assessment.emitted_id} references unknown ledger ids: "
                + ", ".join(sorted(unknown_ledger))
            )
        if assessment.false_positive == bool(matched_ledger):
            errors.append(
                f"{assessment.cell}.{assessment.emitted_id} false_positive must equal "
                "whether matched_ledger_ids is empty"
            )
    return errors


def _prompt(
    pair: str,
    ledger: list[dict[str, Any]],
    cells: list[dict[str, Any]],
    feedback: str | None = None,
) -> str:
    required_emissions = sorted(_expected_emission_ids(cells))
    payload = {
        "pair": pair,
        "frozen_ledger_entries": ledger,
        "six_output_cells": cells,
        "required_emission_keys_exactly_once": [
            {"cell": cell, "emitted_id": emitted_id}
            for cell, emitted_id in required_emissions
        ],
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if feedback:
        text += (
            "\n\n结构完整性反馈：上一版没有满足以下机械结构要求。保持语义判断不变，只补齐缺失项或删除未知项：\n"
            + feedback
        )
    return (
        "请评审以下单个 pair。输入中的台账是冻结的预期集合，六个输出格分别属于新方法和 X1v2 baseline 的三轮运行。\n\n"
        + text
    )


def _atomic_prompt(
    pair: str,
    ledger: dict[str, Any],
    cell: str,
    finding: dict[str, Any],
    feedback: str | None = None,
) -> str:
    payload = {
        "pair": pair,
        "frozen_ledger_entry": ledger,
        "output_cell": cell,
        "single_release_issue": finding,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if feedback:
        text += (
            "\n\n上一版结构错误，请重新返回完整的 matches、reason、confidence：\n"
            + feedback
        )
    return "请独立裁定以下唯一一对台账条目与 release issue。\n\n" + text


def _atomic_llm_fallback(
    pair: str,
    ledger: list[dict[str, Any]],
    cells: list[dict[str, Any]],
    responder: DirectStructuredResponder,
    observations: list[dict[str, Any]],
) -> tuple[PairJudgement, list[dict[str, Any]]]:
    """Recover a complete semantic judgement through atomic LLM decisions.

    Deterministic code only joins decisions by the exact IDs supplied in the
    input. Every semantic edge in the ledger/emission bipartite graph is decided
    by the LLM and retained with its reason; no missing edge is imputed as a
    match or repaired through text rules.
    """

    relations: list[dict[str, Any]] = []
    for ledger_row in ledger:
        for cell in cells:
            for finding in cell.get("findings", []):
                feedback: str | None = None
                decision: AtomicMatchDecision | None = None
                for repair_index in range(MAX_ATOMIC_SCHEMA_REPAIRS + 1):
                    try:
                        decision = _invoke_judge(
                            responder=responder,
                            role="paper1_atomic_semantic_hit_judge",
                            schema=AtomicMatchDecision,
                            system_prompt=ATOMIC_SYSTEM_PROMPT,
                            user_input=_atomic_prompt(
                                pair,
                                ledger_row,
                                str(cell["cell"]),
                                finding,
                                feedback,
                            ),
                            observations=observations,
                        )
                        break
                    except (StructuredOutputValidationError, ValidationError) as exc:
                        feedback = f"{type(exc).__name__}: {exc}"
                        if repair_index >= MAX_ATOMIC_SCHEMA_REPAIRS:
                            decision = AtomicMatchDecision(
                                matches=False,
                                reason=(
                                    "结构化 judge 在有界修复后仍未满足契约，"
                                    "该对应关系保留为未决并按保守 miss 处理。"
                                ),
                                confidence="low",
                            )
                    except Exception as exc:  # noqa: BLE001 - preserve one relation
                        decision = AtomicMatchDecision(
                            matches=False,
                            reason=(
                                "该对应关系的 judge 调用未能完成："
                                f"{type(exc).__name__}: {exc}"
                            ),
                            confidence="low",
                        )
                        break
                if decision is None:
                    decision = AtomicMatchDecision(
                        matches=False,
                        reason="judge 未返回可审计的结构化对应关系，按保守 miss 处理。",
                        confidence="low",
                    )
                relations.append(
                    {
                        "ledger_id": str(ledger_row["ledger_id"]),
                        "cell": str(cell["cell"]),
                        "emitted_id": str(finding["finding_id"]),
                        **decision.model_dump(mode="json"),
                    }
                )

    relation_index = {
        (row["ledger_id"], row["cell"], row["emitted_id"]): row for row in relations
    }
    ledger_assessments: list[LedgerAssessment] = []
    for ledger_row in ledger:
        ledger_id = str(ledger_row["ledger_id"])
        by_cell: dict[str, HitAssessment] = {}
        for cell in cells:
            cell_id = str(cell["cell"])
            rows = [
                relation_index[(ledger_id, cell_id, str(finding["finding_id"]))]
                for finding in cell.get("findings", [])
            ]
            matched = [row for row in rows if row["matches"]]
            if matched:
                by_cell[cell_id] = HitAssessment(
                    hit=True,
                    supporting_finding_ids=[row["emitted_id"] for row in matched],
                    reason="；".join(
                        f"{row['emitted_id']}: {row['reason']}" for row in matched
                    ),
                    confidence=(
                        "low"
                        if any(row["confidence"] == "low" for row in matched)
                        else "medium"
                        if any(row["confidence"] == "medium" for row in matched)
                        else "high"
                    ),
                )
            else:
                by_cell[cell_id] = HitAssessment(
                    hit=False,
                    supporting_finding_ids=[],
                    reason=(
                        "该 cell 没有 release issue。"
                        if not rows
                        else "；".join(
                            f"{row['emitted_id']}: {row['reason']}" for row in rows
                        )
                    ),
                    confidence=(
                        "low"
                        if any(row["confidence"] == "low" for row in rows)
                        else "medium"
                        if any(row["confidence"] == "medium" for row in rows)
                        else "high"
                    ),
                )
        ledger_assessments.append(LedgerAssessment(ledger_id=ledger_id, **by_cell))

    emission_assessments: list[EmissionAssessment] = []
    for cell in cells:
        cell_id = str(cell["cell"])
        for finding in cell.get("findings", []):
            emitted_id = str(finding["finding_id"])
            rows = [
                relation_index[(str(ledger_row["ledger_id"]), cell_id, emitted_id)]
                for ledger_row in ledger
            ]
            matched = [row for row in rows if row["matches"]]
            emission_assessments.append(
                EmissionAssessment(
                    cell=cell_id,
                    emitted_id=emitted_id,
                    matched_ledger_ids=[row["ledger_id"] for row in matched],
                    false_positive=not bool(matched),
                    reason="；".join(
                        f"{row['ledger_id']}: {row['reason']}"
                        for row in (matched or rows)
                    ),
                    confidence=(
                        "low"
                        if any(row["confidence"] == "low" for row in rows)
                        else "medium"
                        if any(row["confidence"] == "medium" for row in rows)
                        else "high"
                    ),
                )
            )
    result = PairJudgement(
        pair=pair,
        ledger_assessments=ledger_assessments,
        emission_assessments=emission_assessments,
        pair_reason="Pair-wide structured adjudication failed its mechanical contract; every ledger/emission relation was independently re-adjudicated by the atomic LLM judge.",
    )
    return result, relations


def judge_pair(
    pair: str,
    ledger_items: dict[str, Any],
    method_root: Path,
    baseline_root: Path,
    responder: DirectStructuredResponder,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    ledger = _ledger_payload(ledger_items, pair)
    cells = [
        _cell_payload(root, arm, pair, run)
        for arm, root in (("method", method_root), ("baseline", baseline_root))
        for run in (1, 2, 3)
    ]
    observations: list[dict[str, Any]] = []
    feedback: str | None = None
    last_error: str | None = None
    for attempt in range(3):
        try:
            result = _invoke_judge(
                responder=responder,
                role="paper1_luna_semantic_hit_judge",
                schema=PairJudgement,
                system_prompt=SYSTEM_PROMPT,
                user_input=_prompt(pair, ledger, cells, feedback),
                observations=observations,
            )
            result = _drop_unknown_emission_rows(result, cells)
            errors = _validate_shape(result, ledger, cells)
            if not errors:
                return {
                    "schema": "paper1.luna_semantic_pair_judgement.v1",
                    "pair": pair,
                    "ledger": ledger,
                    "cells": cells,
                    "judgement": result.model_dump(mode="json"),
                    "status": "ok",
                    "attempts": attempt + 1,
                }, observations
            feedback = "; ".join(errors)
            last_error = feedback
        except Exception as exc:  # noqa: BLE001 - preserve exact audit failure
            last_error = f"{type(exc).__name__}: {exc}"
            if not isinstance(exc, (StructuredOutputValidationError, ValidationError)):
                break
            feedback = last_error
    result, relations = _atomic_llm_fallback(
        pair, ledger, cells, responder, observations
    )
    errors = _validate_shape(result, ledger, cells)
    if errors:
        raise RuntimeError(
            "atomic LLM judge produced inconsistent exact-ID aggregation: "
            + "; ".join(errors)
        )
    return {
        "schema": "paper1.luna_semantic_pair_judgement.v1",
        "pair": pair,
        "ledger": ledger,
        "cells": cells,
        "judgement": result.model_dump(mode="json"),
        "status": "ok",
        "attempts": 3,
        "adjudication_mode": "atomic_llm_fallback",
        "pair_wide_failure": last_error,
        "atomic_relations": relations,
    }, observations


def build_parser() -> argparse.ArgumentParser:
    """Build the semantic-judge CLI parser with streaming as the default."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--method-root", type=Path, required=True)
    parser.add_argument("--baseline-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--profile", default="gpt-5.6-luna")
    parser.add_argument(
        "--transport-retries", type=int, default=DEFAULT_TRANSPORT_RETRIES
    )
    stream_mode = parser.add_mutually_exclusive_group()
    stream_mode.add_argument(
        "--stream",
        dest="streaming",
        action="store_true",
        help="Use streaming responses (the default).",
    )
    stream_mode.add_argument(
        "--no-stream",
        dest="streaming",
        action="store_false",
        help="Use complete non-streaming responses.",
    )
    # Keep judge transport aligned with method runs: stream by default to avoid
    # pre-first-token gateway timeouts on the hosted provider.
    parser.set_defaults(streaming=True)
    parser.add_argument("--max-output-tokens", type=int, default=20_000)
    parser.add_argument("--pairs", nargs="*", default=None)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    ledger_path = (
        ROOT
        / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/ledger.json"
    )
    ledger_items = _read_json(ledger_path)["items"]
    discovered_pairs = {
        path.name[:4]
        for root in (args.method_root, args.baseline_root)
        for path in root.glob("run*/*-luna")
        if len(path.name) >= 4 and path.name[:4].isdigit()
    }
    ledger_pairs = {str(row["pair"]) for row in ledger_items.values()}
    pairs = args.pairs or sorted(discovered_pairs | ledger_pairs)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    responder = DirectStructuredResponder(
        args.profile,
        max_output_tokens=args.max_output_tokens,
        transport_retries=args.transport_retries,
        streaming=args.streaming,
        repeat_schema_in_prompt=False,
        prompt_cache_ttl="1h",
    )
    index: list[dict[str, Any]] = []
    started = time.perf_counter()
    for pair in pairs:
        result, observations = judge_pair(
            pair, ledger_items, args.method_root, args.baseline_root, responder
        )
        output = args.output_dir / f"{pair}.json"
        output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        index.append(
            {
                "pair": pair,
                "status": result["status"],
                "file": output.name,
                "observations": observations,
            }
        )
        print(f"[{result['status']}] pair={pair} -> {output}", flush=True)
    manifest = {
        "schema": "paper1.luna_semantic_judge_manifest.v1",
        "profile": args.profile,
        "method_root": str(args.method_root),
        "baseline_root": str(args.baseline_root),
        "ledger": str(ledger_path),
        "started_epoch_seconds": started,
        "elapsed_seconds": time.perf_counter() - started,
        "pairs": index,
    }
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0 if all(row["status"] == "ok" for row in index) else 1


if __name__ == "__main__":
    raise SystemExit(main())
