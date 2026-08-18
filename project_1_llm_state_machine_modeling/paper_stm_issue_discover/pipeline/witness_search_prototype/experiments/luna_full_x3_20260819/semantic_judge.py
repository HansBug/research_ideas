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

from paper_stm_feedback_loop.discover.responder import (  # noqa: E402
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


class HitAssessment(BaseModel):
    hit: bool
    supporting_finding_ids: list[str] = Field(default_factory=list)
    reason: str
    confidence: Literal["high", "medium", "low"] | None = None


class LedgerAssessment(BaseModel):
    ledger_id: str
    method_run1: HitAssessment
    method_run2: HitAssessment
    method_run3: HitAssessment
    baseline_run1: HitAssessment
    baseline_run2: HitAssessment
    baseline_run3: HitAssessment


class EmissionAssessment(BaseModel):
    cell: Cell
    emitted_id: str
    matched_ledger_ids: list[str] = Field(default_factory=list)
    false_positive: bool
    reason: str
    confidence: Literal["high", "medium", "low"] | None = None


class PairJudgement(BaseModel):
    pair: str
    ledger_assessments: list[LedgerAssessment]
    emission_assessments: list[EmissionAssessment]
    pair_reason: str


SYSTEM_PROMPT = """你是独立的状态机缺陷覆盖评审员。你的任务是把一个 pair 的冻结台账条目与两个被测臂的六个输出格做语义对齐。你只能依据本次输入中的自然语言规格、PlantUML/FCSTM 相关定位、台账条目的完整主张，以及输出 finding 的完整主张作判断；不得使用关键词命中、字符串包含、编辑距离、向量相似度或任何其他词法捷径。

命中判据必须同时满足：1）同一处：输出指认的元素或位置与台账指认的是同一状态、迁移、事件、区域或表达式；2）同一性质：输出主张的是同一种缺失、多余、错位、不可达、无出路、不终止、层次归属、记法槽位或数量问题。措辞不同、只描述后果、没有可执行断言都不影响覆盖命中。只在背景中顺带提到元素、只说上位类别、方向相反，或把多条输出拼起来才能凑成台账主张，都不算命中。

对每个台账条目，六个格都必须给出 hit、支持该命中的 finding id、语义理由和置信度。对每个格中的每一条输出也必须给出是否为 false positive；若它语义上对应台账条目，列出一个或多个对应 ledger id，否则标记 false_positive=true。一个输出 finding 可以覆盖至多条台账，但只有确实同处同性质时才允许。不要因为有正式证书就自动命中，证书只作为主张的一部分；也不要因为没有证书就自动否定覆盖。

这是测量覆盖的独立评审，不是重新修改台账，不得创造新的台账条目。请完整返回要求的结构化对象，不要省略零命中条目或没有 finding 的格。"""


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _compact_method_finding(item: dict[str, Any]) -> dict[str, Any]:
    decision = item.get("d_decision") or {}
    certificates = item.get("execution_certificates") or []
    evidence = []
    for cert in certificates:
        if not isinstance(cert, dict):
            continue
        evidence.append(
            {
                "verdict": cert.get("verdict"),
                "counterexample_found": cert.get("counterexample_found"),
                "observations": cert.get("observations", []),
            }
        )
    return {
        "finding_id": item.get("finding_key") or item.get("candidate_index"),
        "claims": item.get("claims", []),
        "model_claims": item.get("model_claims", []),
        "locations": item.get("locations", []),
        "obligations": item.get("obligations", []),
        "basis": item.get("basis_kind"),
        "d_level": decision.get("d_level") or item.get("d_status"),
        "l_level": item.get("l_level"),
        "d_rationale": decision.get("rationale"),
        "evidence_status": item.get("evidence_status"),
        "execution_evidence": evidence,
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
    if not folder.exists():
        return {"cell": f"{arm}_run{run}", "status": "missing", "findings": []}
    record = _read_json(folder)
    if arm == "method":
        findings = [_compact_method_finding(x) for x in record.get("finding_records", [])]
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
    return {"cell": f"{arm}_run{run}", "status": record.get("status"), "findings": findings}


def _expected_emission_ids(cells: list[dict[str, Any]]) -> set[tuple[str, str]]:
    return {
        (str(cell["cell"]), str(finding["finding_id"]))
        for cell in cells
        for finding in cell.get("findings", [])
    }


def _observation_audit(observation: Any) -> dict[str, Any]:
    """Serialize billing and failure evidence without retaining prompt bodies."""

    return {
        "llm_call_id": observation.llm_call_id,
        "role": observation.role,
        "profile": observation.profile,
        "adapter": observation.adapter,
        "provider": observation.provider,
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


def _validate_shape(result: PairJudgement, ledger: list[dict[str, Any]], cells: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    expected_ledger = {str(row["ledger_id"]) for row in ledger}
    supplied_ledger = {row.ledger_id for row in result.ledger_assessments}
    if supplied_ledger != expected_ledger:
        errors.append("ledger_assessments must contain each supplied ledger_id exactly once")
    if len(supplied_ledger) != len(result.ledger_assessments):
        errors.append("ledger_assessments contains duplicate ledger_id")
    expected_emissions = _expected_emission_ids(cells)
    supplied_emissions = {(row.cell, row.emitted_id) for row in result.emission_assessments}
    if supplied_emissions != expected_emissions:
        errors.append("emission_assessments must contain each supplied emitted finding exactly once")
    if len(supplied_emissions) != len(result.emission_assessments):
        errors.append("emission_assessments contains duplicate cell/emitted_id")
    for assessment in result.ledger_assessments:
        for field in ("method_run1", "method_run2", "method_run3", "baseline_run1", "baseline_run2", "baseline_run3"):
            hit = getattr(assessment, field)
            if any(not isinstance(item, str) for item in hit.supporting_finding_ids):
                errors.append(f"{assessment.ledger_id}.{field} has invalid supporting id")
    return errors


def _prompt(pair: str, ledger: list[dict[str, Any]], cells: list[dict[str, Any]], feedback: str | None = None) -> str:
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
        text += "\n\n结构完整性反馈：上一版没有满足以下机械结构要求。保持语义判断不变，只补齐缺失项或删除未知项：\n" + feedback
    return "请评审以下单个 pair。输入中的台账是冻结的预期集合，六个输出格分别属于新方法和 X1v2 baseline 的三轮运行。\n\n" + text


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
            result = responder.invoke_structured(
                role="paper1_luna_semantic_hit_judge",
                schema=PairJudgement,
                system_prompt=SYSTEM_PROMPT,
                user_input=_prompt(pair, ledger, cells, feedback),
            )
            observation = responder.take_last_observation()
            if observation is not None:
                observations.append(_observation_audit(observation))
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
            observation = responder.take_last_observation()
            if observation is not None:
                observations.append(_observation_audit(observation))
            last_error = f"{type(exc).__name__}: {exc}"
            if not isinstance(exc, (StructuredOutputValidationError, ValidationError)):
                break
            feedback = last_error
    return {
        "schema": "paper1.luna_semantic_pair_judgement.v1",
        "pair": pair,
        "ledger": ledger,
        "cells": cells,
        "status": "failed",
        "failure": {"class": "semantic_judge_output", "message": last_error},
    }, observations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method-root", type=Path, required=True)
    parser.add_argument("--baseline-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--profile", default="gpt-5.6-luna")
    parser.add_argument("--transport-retries", type=int, default=2)
    parser.add_argument("--max-output-tokens", type=int, default=20_000)
    parser.add_argument("--pairs", nargs="*", default=None)
    args = parser.parse_args()
    ledger_path = ROOT / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/ledger_v2/ledger.json"
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
        repeat_schema_in_prompt=False,
        prompt_cache_ttl="1h",
    )
    index: list[dict[str, Any]] = []
    started = time.perf_counter()
    for pair in pairs:
        result, observations = judge_pair(pair, ledger_items, args.method_root, args.baseline_root, responder)
        output = args.output_dir / f"{pair}.json"
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        index.append({"pair": pair, "status": result["status"], "file": output.name, "observations": observations})
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
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if all(row["status"] == "ok" for row in index) else 1


if __name__ == "__main__":
    raise SystemExit(main())
