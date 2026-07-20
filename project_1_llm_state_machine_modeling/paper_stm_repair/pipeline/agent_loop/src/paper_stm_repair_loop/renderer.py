from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Mapping

from .inputs import PreparedCase

if TYPE_CHECKING:
    from .schemas import DiscoverCompleted


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "record"


def _record_directory(record: dict[str, Any]) -> str:
    return f"L{record['logical_loop_index']:03d}-{record['sequence']:06d}-{_slug(record['record_type'])}"


_V2_RECORD_TYPES = (
    "inputs_frozen",
    "input_segments_created",
    "coverage_requirements_created",
    "source_inventory_created",
    "coverage_plan_registered",
    "assertion_revision_registered",
    "eval_assert_call_prepared",
    "eval_assert_completed",
    "root_projection_completed",
    "discover_completed",
    "discover_report_render_completed",
)

_MANDATORY_RECORD_TYPES = {
    "run_started",
    "input_bridge_completed",
    "capability_manifest",
    "check_fcstm_completed",
    "operationalizability_preflight_completed",
    "agent_attempt_started",
    "agent_attempt_finished",
    "discover_submission_accepted",
    *_V2_RECORD_TYPES,
}


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def _get(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _model_dump(obj: Any) -> Any:
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if isinstance(obj, Mapping):
        return dict(obj)
    return obj


def _records_of(records: Iterable[dict[str, Any]], record_type: str) -> list[dict[str, Any]]:
    return [record for record in records if record.get("record_type") == record_type]


def _latest_payload(records: list[dict[str, Any]], record_type: str) -> dict[str, Any]:
    for record in reversed(records):
        if record.get("record_type") == record_type and isinstance(record.get("payload"), dict):
            return record["payload"]
    return {}


def _first_list(payload: Mapping[str, Any], *keys: str) -> list[Any]:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _segment_sort_key(segment: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        segment.get("order", segment.get("sequence", segment.get("ordinal", 10**9))),
        segment.get("start_offset", 10**9),
        str(segment.get("segment_id", "")),
    )


def _fact_sort_key(fact: Mapping[str, Any]) -> tuple[str, str]:
    return (
        str(fact.get("fact_kind", fact.get("kind", ""))),
        str(fact.get("fact_id", fact.get("source_fact_id", ""))),
    )


def _append_json_record(lines: list[str], record: Mapping[str, Any]) -> None:
    lines.extend(
        [
            f"### `{record.get('record_id')}` `{record.get('record_type')}`",
            "",
            "```json",
            _json(record.get("payload", {})),
            "```",
            "",
        ]
    )


def _append_v2_records_section(lines: list[str], records: list[dict[str, Any]]) -> None:
    if not any(record.get("record_type") in _V2_RECORD_TYPES for record in records):
        return

    inputs = _latest_payload(records, "inputs_frozen")
    segment_payload = _latest_payload(records, "input_segments_created")
    requirement_payload = _latest_payload(records, "coverage_requirements_created")
    inventory_payload = _latest_payload(records, "source_inventory_created")
    plan_payload = _latest_payload(records, "coverage_plan_registered")
    projection_payload = _latest_payload(records, "root_projection_completed")
    completed_payload = _latest_payload(records, "discover_completed")

    lines.extend(["## V2 deterministic coverage record view", ""])
    lines.extend(["### Input identity, hashes, and segmenter", ""])
    if inputs:
        interesting = {
            key: inputs[key]
            for key in sorted(inputs)
            if key
            in {
                "run_id",
                "case_id",
                "nl_sha256",
                "normalized_nl_sha256",
                "raw_source_sha256",
                "fcstm_sha256",
                "source_trace_sha256",
                "model_sha256",
                "segmenter_version",
                "pyfcstm_version",
                "relation_policy",
                "scope_boundary",
                "eligibility",
            }
        }
        lines.extend(["```json", _json(interesting or inputs), "```", ""])
    else:
        lines.extend(["- no `inputs_frozen` record", ""])

    segments = _first_list(segment_payload, "input_segments", "segments")
    lines.extend(["### NL segments", ""])
    if segments:
        for segment in sorted((item for item in segments if isinstance(item, Mapping)), key=_segment_sort_key):
            segment_id = segment.get("segment_id", segment.get("id", "unknown-segment"))
            start = segment.get("start_offset", "?")
            end = segment.get("end_offset", "?")
            sha = segment.get("sha256", "")
            text = str(segment.get("text", "")).replace("\n", "\\n")
            lines.extend([f"- `{segment_id}` [{start}, {end}) sha256=`{sha}` — {text}"])
        lines.append("")
        if "offset_mapping" in segment_payload or "raw_to_normalized_offset_mapping" in segment_payload:
            mapping = segment_payload.get("offset_mapping", segment_payload.get("raw_to_normalized_offset_mapping"))
            lines.extend(["<details><summary>offset mapping</summary>", "", "```json", _json(mapping), "```", "", "</details>", ""])
    else:
        lines.extend(["- no input segments recorded", ""])

    requirements = _first_list(requirement_payload, "requirements")
    lines.extend(["### Controller-enforced clause and cue coverage requirements", ""])
    if requirements:
        for requirement in requirements:
            lines.append(
                f"- `{requirement.get('requirement_id')}` segment=`{requirement.get('segment_id')}` "
                f"clause=`{requirement.get('clause_id')}` "
                f"dimension=`{requirement.get('dimension')}` cue=`{requirement.get('cue_text')}` "
                f"family-options=`{_json(requirement.get('required_function_family_options', []))}`"
            )
        lines.append("")
    else:
        lines.extend(["- no hard clause/cue coverage requirements", ""])

    facts = _first_list(inventory_payload, "source_facts", "facts", "inventory")
    lines.extend(["### SourceFacts inventory", ""])
    if facts:
        for fact in sorted((item for item in facts if isinstance(item, Mapping)), key=_fact_sort_key):
            fact_id = fact.get("fact_id", fact.get("source_fact_id", "unknown-fact"))
            kind = fact.get("fact_kind", fact.get("kind", "unknown"))
            producer = fact.get("producer", fact.get("producer_version", ""))
            refs = fact.get("qualified_refs", fact.get("refs", []))
            summary = fact.get("qualified_name") or fact.get("source") or fact.get("target") or fact.get("statement") or ""
            lines.append(f"- `{fact_id}` `{kind}` producer=`{producer}` refs=`{_json(refs)}` {summary}")
        lines.append("")
    else:
        lines.extend(["- no source facts recorded", ""])

    lines.extend(["### Coverage plan, dispositions, units, roots, and assertion versions", ""])
    plan_objects = {
        "segment_dispositions": _first_list(plan_payload, "segment_dispositions"),
        "fact_dispositions": _first_list(plan_payload, "fact_dispositions", "source_fact_dispositions"),
        "coverage_units": _first_list(plan_payload, "coverage_units"),
        "proposition_roots": _first_list(plan_payload, "proposition_roots", "roots"),
        "latest_assertions": _first_list(plan_payload, "latest_assertions", "logical_assertions", "assertions"),
    }
    if any(plan_objects.values()):
        for label, values in plan_objects.items():
            lines.extend([f"#### {label}", "", "```json", _json(values), "```", ""])
        if "plan_sha256" in plan_payload:
            lines.extend([f"- plan sha256: `{plan_payload['plan_sha256']}`", ""])
    elif plan_payload:
        lines.extend(["```json", _json(plan_payload), "```", ""])
    else:
        lines.extend(["- no coverage plan recorded", ""])

    revision_records = _records_of(records, "assertion_revision_registered")
    if revision_records:
        lines.extend(["### Assertion revisions", ""])
        for record in revision_records:
            _append_json_record(lines, record)

    prepared_records = _records_of(records, "eval_assert_call_prepared")
    completed_records = _records_of(records, "eval_assert_completed")
    lines.extend(["### Eval assert trace, function calls, return values, witnesses", ""])
    if prepared_records or completed_records:
        for record in sorted(prepared_records + completed_records, key=lambda item: item.get("sequence", 0)):
            payload = record.get("payload", {})
            lines.extend(
                [
                    f"#### `{record.get('record_id')}` `{record.get('record_type')}`",
                    "",
                    f"- assertion: `{payload.get('assertion_version_id', payload.get('assertion_chain_id', 'unknown'))}`",
                    f"- root: `{payload.get('root_node_id', 'unknown')}` / unit: `{payload.get('coverage_unit_id', 'unknown')}`",
                    f"- assert sha256: `{payload.get('assert_sha256', '')}`",
                ]
            )
            if "reason" in payload:
                lines.append(f"- raw reason: {payload['reason']}")
            if "assert" in payload:
                lines.extend(["- assert text:", "", "```python", str(payload["assert"]), "```"])
            for key in ("function_calls", "function_call_trace", "call_trace", "trace", "witness", "evidence_refs", "limitations"):
                if key in payload:
                    lines.extend([f"- {key}:", "", "```json", _json(payload[key]), "```"])
            for key in ("python_return", "return_value", "exception", "match_status", "execution_status"):
                if key in payload:
                    lines.append(f"- {key}: `{payload[key]}`")
            lines.append("")
    else:
        lines.extend(["- no eval_assert records", ""])

    lines.extend(["### Root projection", ""])
    if projection_payload:
        for key in (
            "run_outcome",
            "registered_coverage_complete",
            "semantic_coverage_assurance",
            "input_segment_coverage",
            "source_fact_coverage",
            "coverage_requirement_coverage",
            "assertion_execution_coverage",
            "semantic_coverage_review",
            "issue_root_projection",
            "regression_guard_projection",
            "incomplete_root_projection",
            "rationale",
        ):
            if key in projection_payload:
                lines.extend([f"#### {key}", "", "```json", _json(projection_payload[key]), "```", ""])
    else:
        lines.extend(["- no root projection recorded", ""])

    lines.extend(["### Eligibility and scope boundary", ""])
    eligibility = {
        "main_result_eligible": completed_payload.get("main_result_eligible"),
        "main_result_eligibility_owner": completed_payload.get("main_result_eligibility_owner"),
        "main_result_eligibility_reason": completed_payload.get("main_result_eligibility_reason"),
        "agent_real_llm": completed_payload.get("agent_real_llm"),
        "agent_academic_eligible": completed_payload.get("agent_academic_eligible"),
        "test_replay": completed_payload.get("test_replay"),
        "scope_boundary": inputs.get("scope_boundary") or completed_payload.get("scope_boundary"),
    }
    lines.extend(["```json", _json({key: value for key, value in eligibility.items() if value is not None}), "```", ""])


def render_discover(
    outdir: Path,
    case: PreparedCase,
    completed: DiscoverCompleted,
    records: list[dict[str, Any]],
    language: str,
) -> Path:
    """Render the immutable human view deterministically from method facts."""

    if language == "zh-CN":
        title, boundary, roots_title = "B-discover 阶段报告", "方法边界", "发现结果"
        trace_title, mandatory_title = "A 阶段 source trace", "Controller 与执行审计"
        boundary_text = "本报告发布 Controller 对冻结 NL 子句、全部 cue 行、行为 source facts 与逐条断言执行形成的闭包，以及独立语义覆盖审查结果；Controller 不预设缺陷分类，也不把表示语言或审计基础设施单独作为论文贡献。"
        no_root = "本次穷尽覆盖矩阵没有发布 confirmed 或 candidate root issue。"
        zero_metrics = "zero-root 固定记账：`accepted_fix_count=0`、`closure_numerator=0`、`repair_gain=0`。"
    else:
        title, boundary, roots_title = "B-discover stage report", "Method boundary", "Discovery result"
        trace_title, mandatory_title = "A-stage source trace", "Controller and execution audit"
        boundary_text = "This report publishes Controller closure over frozen NL clauses, cue rows, behavior source facts, assertion execution, and the independent semantic-coverage review. The Controller does not predefine defect categories or promote the representation/audit infrastructure as a paper contribution."
        no_root = "This exhaustive-matrix run published no confirmed or candidate root issue."
        zero_metrics = "Zero-root accounting is fixed to `accepted_fix_count=0`, `closure_numerator=0`, and `repair_gain=0`."

    completed_outcome = _get(completed, "outcome")
    v2_roots = _get(completed_outcome, "proposition_roots", []) if completed_outcome is not None else []
    root_count = len(v2_roots)
    no_issue_found = (
        len(_get(completed_outcome, "issue_root_projection", []) or []) == 0
        if completed_outcome is not None
        else True
    )

    lines = [
        f"# {title}",
        "",
        f"- run: `{_get(completed, 'run_id')}`",
        f"- case: `{case.case_id}`",
        f"- model: `{_get(completed, 'model_id')}` / `{_get(completed, 'model_sha256')}`",
        f"- language: `{language}`",
        f"- Agent real LLM: `{str(_get(completed, 'agent_real_llm')).lower()}`",
        f"- Agent academic eligible: `{str(_get(completed, 'agent_academic_eligible')).lower()}`",
        f"- test replay: `{str(_get(completed, 'test_replay')).lower()}`",
        f"- main result eligible: `{str(_get(completed, 'main_result_eligible')).lower()}`",
        f"- main result eligibility owner: `{_get(completed, 'main_result_eligibility_owner')}`",
        f"- main result eligibility reason: {_get(completed, 'main_result_eligibility_reason')}",
        f"- root count: `{root_count}`",
        f"- no issue found: `{str(no_issue_found).lower()}`",
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
        _json(case.source_trace),
        "```",
        "",
    ]
    _append_v2_records_section(lines, records)
    lines.extend([f"## {mandatory_title}", ""])
    for record in records:
        if record["record_type"] not in _MANDATORY_RECORD_TYPES:
            continue
        _append_json_record(lines, record)
    lines.extend([f"## {roots_title}", ""])
    if not v2_roots:
        rationale = _get(completed_outcome, "rationale", "")
        lines.extend([no_root, "", zero_metrics, "", f"- rationale: {rationale}", ""])
    for root in v2_roots or []:
        root_dict = _model_dump(root)
        lines.extend([f"### `{root_dict.get('node_id')}`", "", "```json", _json(root_dict), "```", ""])
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
