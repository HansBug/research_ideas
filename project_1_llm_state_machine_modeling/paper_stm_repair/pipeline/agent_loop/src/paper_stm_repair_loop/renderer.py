from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .inputs import PreparedCase
from .schemas import DiscoverCompleted


def _record_directory(record: dict[str, Any]) -> str:
    return f"L{record['logical_loop_index']:03d}-{record['sequence']:06d}-{record['record_type'].replace('_', '-')}"


_MANDATORY_RECORD_TYPES = {
    "check_fcstm_completed",
    "issue_check_preparation_completed",
    "run_scenarios_completed",
    "verify_properties_completed",
    "check_fcstm_static_consistency_completed",
    "validate_discovery_checks_completed",
    "discover_mandatory_preparation_completed",
}


def render_discover(
    outdir: Path,
    case: PreparedCase,
    completed: DiscoverCompleted,
    records: list[dict[str, Any]],
    language: str,
) -> Path:
    """Render the immutable human view deterministically from method facts."""

    if language == "zh-CN":
        title, boundary, checks_title, roots_title = "B-discover 阶段报告", "方法边界", "运行内检查项", "发现结果"
        trace_title, mandatory_title, rejected_title = "A 阶段 source trace", "Controller 必跑结果", "未形成 root 的 proposition"
        boundary_text = "本报告仅记录 B-discover 的有界发现结果，不声明模型全局正确、源层闭合、表示语言优越性或论文实验成功。"
        no_root = "本次运行没有发布 confirmed 或 candidate root issue；这不等于模型无错。"
        zero_metrics = "zero-root 固定记账：`accepted_fix_count=0`、`closure_numerator=0`、`repair_gain=0`；漏检只能由方法终止后的隐藏 evaluator 判断。"
    else:
        title, boundary, checks_title, roots_title = "B-discover stage report", "Method boundary", "Run-local checks", "Discovery result"
        trace_title, mandatory_title, rejected_title = "A-stage source trace", "Controller mandatory results", "Propositions not published as roots"
        boundary_text = "This report records bounded B-discover results only. It does not claim global correctness, source closure, representation superiority, or scientific success."
        no_root = "This run published no confirmed or candidate root issue; that does not mean the model is defect-free."
        zero_metrics = "Zero-root accounting is fixed to `accepted_fix_count=0`, `closure_numerator=0`, and `repair_gain=0`; missed issues can be measured only by the hidden post-run evaluator."
    lines = [
        f"# {title}",
        "",
        f"- run: `{completed.run_id}`",
        f"- case: `{case.case_id}`",
        f"- model: `{completed.model_id}` / `{completed.model_sha256}`",
        f"- language: `{language}`",
        f"- Agent real LLM: `{str(completed.agent_real_llm).lower()}`",
        f"- Agent academic eligible: `{str(completed.agent_academic_eligible).lower()}`",
        f"- test replay: `{str(completed.test_replay).lower()}`",
        f"- main result eligible: `{str(completed.main_result_eligible).lower()}`",
        f"- root count: `{len(completed.root_nodes)}`",
        f"- no issue found: `{str(completed.no_issue_found).lower()}`",
        "",
        f"## {boundary}",
        "",
        boundary_text,
        "",
        "## NL",
        "",
        case.nl,
        "",
        "## Raw/source STM_0",
        "",
        f"```{case.raw_source_format}",
        case.raw_source.rstrip(),
        "```",
        "",
        "## fcstm STM_0",
        "",
        "```text",
        case.fcstm.rstrip(),
        "```",
        "",
        f"## {trace_title}",
        "",
        "```json",
        json.dumps(case.source_trace, ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        f"## {checks_title}",
        "",
    ]
    for check in completed.issue_checks:
        lines.extend(
            [
                f"### `{check.check_id}`",
                "",
                f"- origin: `{check.check_origin}`",
                f"- kind: `{check.check_kind}`",
                f"- required: `{str(check.required).lower()}`",
                f"- statement: {check.statement}",
                f"- bindings: `{', '.join(check.binding_refs)}`",
                "- full immutable check:",
                "",
                "```json",
                json.dumps(check.model_dump(mode="json"), ensure_ascii=False, indent=2, sort_keys=True),
                "```",
                "",
            ]
        )
    lines.extend([f"## {mandatory_title}", ""])
    for record in records:
        if record["record_type"] not in _MANDATORY_RECORD_TYPES:
            continue
        lines.extend(
            [
                f"### `{record['record_id']}` `{record['record_type']}`",
                "",
                "```json",
                json.dumps(record["payload"], ensure_ascii=False, indent=2, sort_keys=True),
                "```",
                "",
            ]
        )
    lines.extend([f"## {roots_title}", ""])
    if not completed.root_nodes:
        lines.extend([no_root, "", zero_metrics, "", f"- rationale: {completed.rationale}", ""])
    for root in completed.root_nodes:
        lines.extend(
            [
                f"### `{root.node_id}`",
                "",
                f"- issue id: `{root.issue_id}`",
                f"- assessment: `{root.assessment}`",
                f"- repair allowed: `{str(root.downstream_repair_allowed).lower()}`",
                f"- statement: {root.statement}",
                f"- rationale: {root.rationale}",
                f"- checks: `{', '.join(root.required_check_ids)}`",
                f"- source/model refs: `{', '.join(root.source_element_refs)}`",
                f"- supporting records: `{', '.join(root.supporting_record_ids)}`",
                "",
            ]
        )
    lines.extend([f"## {rejected_title}", ""])
    for proposition in completed.rejected_propositions:
        lines.extend(
            [
                f"### `{proposition.proposition_id}`",
                "",
                f"- assessment: `{proposition.assessment}`",
                f"- statement: {proposition.statement}",
                f"- rationale: {proposition.rationale}",
                f"- considered checks: `{', '.join(proposition.considered_check_ids)}`",
                f"- source/model refs: `{', '.join(proposition.source_element_refs)}`",
                f"- supporting records: `{', '.join(proposition.supporting_record_ids)}`",
                "",
            ]
        )
    if not completed.rejected_propositions:
        lines.extend(["- none", ""])
    lines.extend(["## Audit links", ""])
    for record in records:
        directory = _record_directory(record)
        lines.append(f"- [`{record['record_id']}` {record['record_type']}](../records/{directory}/record.json)")
    lines.extend(
        [
            "- [Discover Agent audit](../agent_audit/discover/audit.jsonl)",
            "- [Discover Agent result](../agent_audit/discover/result.json)",
            "- [Discover Agent receipt](../agent_audit/discover/receipt.json)",
            "- [Context manifest](../contexts/discover-attempt-001/context_manifest.json)",
            "",
        ]
    )
    target = outdir / "loops" / "discover.md"
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"immutable report already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return target
