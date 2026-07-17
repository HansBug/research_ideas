from __future__ import annotations

import argparse
import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

from utils.agent import AgentApp, AgentSpec
from utils.llm import LLMRegistry, load_llm_registry
from pyfcstm.config.meta import __VERSION__ as PYFCSTM_SOURCE_VERSION
from pyfcstm.llm import (
    get_fbmcq_language_guide_prompt_metadata_for_llm,
    get_grammar_guide_prompt_metadata_for_llm,
)

from ..config import LANGUAGES, REPO_ROOT
from ..context import freeze_task_snapshot, publish_context, validate_reference_blind
from ..inputs import PreparedCase, load_custom, load_pair, load_run_case, prepare_run_dir
from ..prompts.discover import system_prompt, user_prompt
from ..records import RecordStore, sha256_file, sha256_json
from ..renderer import render_discover
from ..schemas import AgentReceiptRef, DiscoverCompleted, DiscoverSubmission
from ..tools.check_fcstm import execute as check_fcstm
from ..tools.evaluate_checks import build_tool as build_evaluate_checks
from ..tools.guide_access import (
    GuideAccessState,
    guard_tool,
    property_batch_requested,
)
from ..tools.lookup_source_trace import build_tool as build_lookup_source_trace
from ..tools.observe_trace import build_tool as build_observe_trace
from ..tools.query_model import build_tool as build_query_model
from ..tools.read_task import build_tool as build_read_task
from ..tools.read_fbmcq_guide import build_tool as build_read_fbmcq_guide
from ..tools.read_fcstm_guide import build_tool as build_read_fcstm_guide
from ..tools.run_scenarios import execute as run_scenarios


AGENT_TOOL_NAMES = (
    "read_fcstm_guide",
    "read_fbmcq_guide",
    "read_task",
    "query_model",
    "observe_trace",
    "lookup_source_trace",
    "evaluate_checks",
)


def _pyfcstm_commit() -> str:
    completed = subprocess.run(
        ["git", "-C", str(REPO_ROOT / "pyfcstm"), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else "unknown"


def _write_capability_manifest(run_dir: Path, manifest: Mapping[str, Any]) -> dict[str, Any]:
    try:
        from pyfcstm.entry.bmc import build_bmc_output  # noqa: F401

        bmc_available = True
    except Exception:
        bmc_available = False
    formal_required = bool(manifest.get("formal_profile", True))
    distribution_version = importlib.metadata.version("pyfcstm")
    pyfcstm_version = PYFCSTM_SOURCE_VERSION
    pyfcstm_commit = _pyfcstm_commit()
    prompt_resources = {
        "fcstm": dict(get_grammar_guide_prompt_metadata_for_llm()),
        "fbmcq": dict(get_fbmcq_language_guide_prompt_metadata_for_llm()),
    }
    version_consistent = (
        distribution_version == pyfcstm_version
        and all(
            item.get("pyfcstm_version") == pyfcstm_version
            for item in prompt_resources.values()
        )
    )
    capabilities = {
        "schema_version": "paper1.capability_manifest.v1",
        "experiment_profile": "full" if formal_required else "non-formal-ablation",
        "pyfcstm_version": pyfcstm_version,
        "pyfcstm_distribution_version": distribution_version,
        "pyfcstm_version_consistent": version_consistent,
        "pyfcstm_git_commit": pyfcstm_commit,
        "prompt_resources": prompt_resources,
        "tools": {
            name: {
                "tool_name": name,
                "adapter_name": f"paper_stm_repair_loop.{name}",
                "adapter_version": "v1",
                "upstream_version": pyfcstm_version,
                "upstream_git_commit": pyfcstm_commit,
                "upstream_available": True,
                "adapter_available": bmc_available if name == "verify_properties" else True,
                "profile_required": formal_required if name == "verify_properties" else True,
                "timeout": 30_000 if name == "verify_properties" else None,
                "retry_policy": "none",
            }
            for name in (
                "check_fcstm",
                "validate_discovery_checks",
                "run_scenarios",
                "verify_properties",
                "verify_static_consistency",
                *AGENT_TOOL_NAMES,
            )
        },
        "formal_verification_available": formal_required and bmc_available,
        "formal_verification_executed": False,
        "formal_claim_eligible": formal_required and bmc_available,
    }
    RecordStore(run_dir).write_immutable_json("capability_manifest.json", capabilities)
    if not version_consistent:
        store = RecordStore(run_dir)
        store.append(
            "run_failed",
            {
                "failure_reason": "pyfcstm_version_mismatch",
                "source_version": pyfcstm_version,
                "distribution_version": distribution_version,
                "prompt_versions": {
                    key: value.get("pyfcstm_version")
                    for key, value in prompt_resources.items()
                },
            },
        )
        raise RuntimeError("pyfcstm_version_mismatch")
    if formal_required and not bmc_available:
        store = RecordStore(run_dir)
        store.append("run_failed", {"failure_reason": "required_capability_unavailable", "tool_name": "verify_properties"})
        raise RuntimeError("required_capability_unavailable:verify_properties")
    return capabilities


def _current_records(store: RecordStore, case: PreparedCase) -> dict[str, Any]:
    by_type: dict[str, Any] = {}
    for record in store.all():
        by_type[record["record_type"]] = {
            "record_id": record["record_id"],
            "record_sha256": record["record_sha256"],
            "payload": record["payload"],
        }
    by_type["nl"] = {"content": case.nl, "sha256": sha256_json(case.nl)}
    by_type["raw_source"] = {"format": case.raw_source_format, "content": case.raw_source, "sha256": sha256_json(case.raw_source)}
    by_type["source_trace"] = case.source_trace
    return by_type


def _trace_runner(case: PreparedCase):
    def run(events: list[str], max_steps: int | None = None) -> dict[str, Any]:
        check = {
            "check_id": "AGENT-TRACE",
            "check_origin": "nl_grounded_behavioral_issue",
            "check_kind": "scenario",
            "statement": "Agent-selected exploratory trace.",
            "expected_outcome": {},
            "basis_hashes": {},
            "source_basis": [],
            "nl_basis": [],
            "executable_spec": {"events": events},
            "binding_refs": [f"event:{event}" for event in events],
            "required": False,
        }
        result = run_scenarios(case.fcstm, [check], "inputs/STM_0.fcstm")
        observations = result.get("scenario_results", [])
        if observations:
            item = dict(observations[0])
            item["execution_status"] = result.get("execution_status", "completed")
            item["model_sha256"] = case.fcstm_sha256
            item["cycles"] = item.get("cycles", len(events))
            return item
        return {"execution_status": "execution_error", "model_sha256": case.fcstm_sha256, "errors": result.get("errors", [])}

    return run


def _accepted_source_refs(case: PreparedCase, checks: list[dict[str, Any]], inspect: Mapping[str, Any]) -> set[str]:
    refs = {ref for check in checks for ref in check.get("binding_refs", []) if isinstance(ref, str)}
    refs.update(f"state:{item['path']}" for item in inspect.get("states", []) if item.get("path"))
    refs.update(f"event:{item['qualified_name']}" for item in inspect.get("events", []) if item.get("qualified_name"))
    refs.update(f"transition:{item['transition_index']}" for item in inspect.get("transitions", []) if item.get("transition_index") is not None)
    for entry in case.source_trace.get("entries", []) or []:
        source = [item for item in entry.get("source_elements", []) if isinstance(item, str)]
        intermediate = [item for item in entry.get("intermediate_elements", []) if isinstance(item, str)]
        if len(source) == 1 and len(intermediate) == 1:
            refs.update(source)
            refs.update(intermediate)
    return refs


def _confirmed_source_refs(case: PreparedCase, accepted_refs: set[str]) -> set[str]:
    """Return refs with deterministic one-to-one source attribution."""

    trace = case.source_trace
    if (
        trace.get("relation_policy") == "exact_identity"
        and case.raw_source_format == "fcstm-identity"
        and case.raw_source == case.fcstm
    ):
        return set(accepted_refs)

    entries = trace.get("entries")
    if not isinstance(entries, list):
        return set()

    source_occurrences: dict[str, list[tuple[int, str]]] = {}
    intermediate_occurrences: dict[str, list[tuple[int, str]]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, Mapping):
            continue
        source_refs = [ref for ref in entry.get("source_elements", []) if isinstance(ref, str) and ref]
        intermediate_refs = [ref for ref in entry.get("intermediate_elements", []) if isinstance(ref, str) and ref]
        if len(source_refs) != 1 or len(intermediate_refs) != 1:
            continue
        source_ref, intermediate_ref = source_refs[0], intermediate_refs[0]
        source_occurrences.setdefault(source_ref, []).append((index, intermediate_ref))
        intermediate_occurrences.setdefault(intermediate_ref, []).append((index, source_ref))

    exact_refs: set[str] = set()
    for source_ref, occurrences in source_occurrences.items():
        if len(occurrences) != 1:
            continue
        index, intermediate_ref = occurrences[0]
        if intermediate_occurrences.get(intermediate_ref) != [(index, source_ref)]:
            continue
        exact_refs.update((source_ref, intermediate_ref))
    return exact_refs


def _payload_contains_check_id(value: Any, check_id: str) -> bool:
    if isinstance(value, Mapping):
        if value.get("check_id") == check_id:
            return True
        return any(_payload_contains_check_id(item, check_id) for item in value.values())
    if isinstance(value, list):
        return any(_payload_contains_check_id(item, check_id) for item in value)
    return False


def _validate_submission(
    raw: Any,
    *,
    checks: list[dict[str, Any]],
    records: list[dict[str, Any]],
    executed_check_ids: set[str],
    accepted_refs: set[str],
    confirmed_refs: set[str],
) -> DiscoverSubmission:
    submission = raw if isinstance(raw, DiscoverSubmission) else DiscoverSubmission.model_validate(raw)
    known_checks = {str(check["check_id"]) for check in checks}
    records_by_id = {str(record["record_id"]): record for record in records}
    known_records = set(records_by_id)
    if submission.no_issue_found != (len(submission.root_nodes) == 0):
        raise ValueError("zero-root flag and root batch disagree")
    if not submission.rationale.strip():
        raise ValueError("discovery submission requires a non-empty rationale")
    node_ids: set[str] = set()
    considered_checks: set[str] = set()
    for root in submission.root_nodes:
        if root.node_id in node_ids:
            raise ValueError(f"duplicate root node: {root.node_id}")
        node_ids.add(root.node_id)
        if not root.rationale.strip() or not root.statement.strip():
            raise ValueError(f"root {root.node_id} requires statement and rationale")
        if not set(root.required_check_ids).issubset(known_checks):
            raise ValueError(f"root {root.node_id} references unknown checks")
        considered_checks.update(root.required_check_ids)
        if not set(root.supporting_record_ids).issubset(known_records):
            raise ValueError(f"root {root.node_id} references unknown records")
        if root.assessment == "confirmed":
            if not root.downstream_repair_allowed:
                raise ValueError(f"confirmed root {root.node_id} must be repair eligible")
            if not root.required_check_ids or not set(root.required_check_ids).issubset(executed_check_ids):
                raise ValueError(f"confirmed root {root.node_id} lacks executed checks")
            if not root.source_element_refs or not set(root.source_element_refs).issubset(confirmed_refs):
                raise ValueError(f"confirmed root {root.node_id} lacks exact source attribution")
            preparation_records = [
                records_by_id[record_id]
                for record_id in root.supporting_record_ids
                if records_by_id[record_id]["record_type"] == "issue_check_preparation_completed"
            ]
            execution_records = [
                records_by_id[record_id]
                for record_id in root.supporting_record_ids
                if records_by_id[record_id]["record_type"]
                in {
                    "run_scenarios_completed",
                    "verify_properties_completed",
                    "check_fcstm_static_consistency_completed",
                }
            ]
            for check_id in root.required_check_ids:
                if not any(_payload_contains_check_id(record["payload"], check_id) for record in preparation_records):
                    raise ValueError(f"confirmed root {root.node_id} lacks preparation evidence for {check_id}")
                if not any(_payload_contains_check_id(record["payload"], check_id) for record in execution_records):
                    raise ValueError(f"confirmed root {root.node_id} lacks execution evidence for {check_id}")
        elif root.downstream_repair_allowed:
            raise ValueError(f"candidate root {root.node_id} cannot be repair eligible")
    proposition_ids: set[str] = set()
    for proposition in submission.rejected_propositions:
        if proposition.proposition_id in proposition_ids or proposition.proposition_id in node_ids:
            raise ValueError(f"duplicate proposition id: {proposition.proposition_id}")
        proposition_ids.add(proposition.proposition_id)
        if not proposition.statement.strip() or not proposition.rationale.strip():
            raise ValueError(f"rejected proposition {proposition.proposition_id} requires statement and rationale")
        if not proposition.considered_check_ids or not set(proposition.considered_check_ids).issubset(known_checks):
            raise ValueError(f"rejected proposition {proposition.proposition_id} lacks valid considered checks")
        if not set(proposition.supporting_record_ids).issubset(known_records):
            raise ValueError(f"rejected proposition {proposition.proposition_id} references unknown records")
        if not set(proposition.source_element_refs).issubset(accepted_refs):
            raise ValueError(f"rejected proposition {proposition.proposition_id} references unaccepted source/model refs")
        considered_checks.update(proposition.considered_check_ids)
    if considered_checks != known_checks:
        missing = sorted(known_checks - considered_checks)
        extra = sorted(considered_checks - known_checks)
        raise ValueError(f"discovery proposition coverage mismatch: missing={missing}, extra={extra}")
    validate_reference_blind(submission.model_dump(mode="json"))
    return submission


def _augment_submission_evidence(
    submission: DiscoverSubmission,
    record_ids: list[str],
) -> DiscoverSubmission:
    def merged(existing: list[str]) -> list[str]:
        return sorted(set(existing) | set(record_ids))

    return submission.model_copy(
        update={
            "root_nodes": [
                root.model_copy(update={"supporting_record_ids": merged(root.supporting_record_ids)})
                for root in submission.root_nodes
            ],
            "rejected_propositions": [
                proposition.model_copy(
                    update={"supporting_record_ids": merged(proposition.supporting_record_ids)}
                )
                for proposition in submission.rejected_propositions
            ],
        }
    )


def _matching_evaluation(
    submission: DiscoverSubmission,
    invocation_log: list[dict[str, Any]],
) -> dict[str, Any]:
    drafts = [item.model_dump(mode="json") for item in submission.check_drafts]
    expected_sha256 = sha256_json(drafts)
    matches = [
        item["result"]
        for item in invocation_log
        if item.get("result", {}).get("drafts_sha256") == expected_sha256
    ]
    if not matches:
        raise ValueError("final check_drafts were not evaluated in this Agent attempt")
    result = matches[-1]
    if result.get("execution_status") != "completed":
        raise ValueError("final check_drafts evaluation did not complete")
    gate = result.get("gate") or {}
    if not gate.get("eligible"):
        raise ValueError(
            "final check_drafts are not mechanically eligible:"
            + ",".join(str(item) for item in gate.get("reasons", []))
        )
    return result


def _validate_guide_protocol(
    state: GuideAccessState,
    submission: DiscoverSubmission,
) -> None:
    """Fail closed when an Agent attempted model/query work before its guide."""

    fcstm_read = state.fcstm_read_at
    if fcstm_read is None:
        raise ValueError("read_fcstm_guide was not called successfully")
    if not state.events or state.events[0].get("guide_kind") != "fcstm":
        raise ValueError(
            "fcstm guide-first protocol violated: "
            "read_fcstm_guide was not the first business tool call"
        )
    model_attempts = [
        item
        for item in state.events
        if item.get("event") == "tool_attempt"
    ]
    early_model_attempts = [
        item for item in model_attempts if int(item["sequence"]) < fcstm_read
    ]
    if early_model_attempts:
        raise ValueError(
            "fcstm guide-first protocol violated before:"
            + ",".join(str(item.get("tool_name")) for item in early_model_attempts)
        )

    property_requested = any(
        draft.check_kind == "property" for draft in submission.check_drafts
    )
    property_attempts = [
        item for item in model_attempts if item.get("property_batch") is True
    ]
    if not property_requested and not property_attempts:
        return
    fbmcq_read = state.fbmcq_read_at
    if fbmcq_read is None:
        raise ValueError("read_fbmcq_guide was not called before property work")
    early_property_attempts = [
        item for item in property_attempts if int(item["sequence"]) < fbmcq_read
    ]
    if early_property_attempts:
        raise ValueError("fbmcq guide-first protocol violated before property evaluation")


def _publish_redaction_report(audit_path: Path, destination: Path) -> Path:
    finish: dict[str, Any] = {}
    for line in audit_path.read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        if item.get("record_type") == "finish" or item.get("record") == "finish":
            finish = item
    destination.write_text(
        json.dumps({"schema_version": "paper1.redaction_report.v1", "channels": finish.get("redaction_report", [])}, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return destination


def _run_replay(run_dir: Path, replay_file: Path) -> tuple[DiscoverSubmission, AgentReceiptRef]:
    data = json.loads(replay_file.read_text(encoding="utf-8"))
    submission = DiscoverSubmission.model_validate(data["submission"])
    directory = run_dir / "agent_audit" / "discover"
    directory.mkdir(parents=True, exist_ok=True)
    audit = directory / "audit.jsonl"
    result = directory / "result.json"
    receipt = directory / "receipt.json"
    redaction = directory / "redaction_report.json"
    audit.write_text(json.dumps({"record": "finish", "status": "success", "test_replay": True, "redaction_report": []}, ensure_ascii=False) + "\n", encoding="utf-8")
    result.write_text(json.dumps({"status": "success", "real_llm": False, "academic_eligible": False, "output": submission.model_dump(mode="json")}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt.write_text(json.dumps({"status": "test_replay", "result_sha256": sha256_file(result)}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    redaction.write_text(json.dumps({"schema_version": "paper1.redaction_report.v1", "channels": []}, indent=2) + "\n", encoding="utf-8")
    return submission, AgentReceiptRef(
        audit_path=str(audit.relative_to(run_dir)),
        result_path=str(result.relative_to(run_dir)),
        receipt_path=str(receipt.relative_to(run_dir)),
        result_sha256=sha256_file(result),
    )


def run_discover(run_dir: Path, registry: LLMRegistry) -> DiscoverCompleted:
    """Run and publish one complete, read-only ``B-discover`` stage.

    Purpose: orchestrate deterministic FCSTM preflight, one complete Discover
    Agent attempt with in-attempt check evaluation, deterministic submission
    validation, append-only publication, and the human-readable Discover report.
    The stage never edits ``STM_0`` and never performs Repair, Confirm, C-stage
    projection, source closure, or scientific evaluation.

    Parameters: ``run_dir`` is a newly prepared run root whose immutable
    ``manifest.json`` and ``inputs/`` were created by ``prepare_run_dir``.
    ``registry`` is the repository ``utils.llm.LLMRegistry`` used for the single
    Discover Agent. Provider/profile,
    content language, renderer, formal profile, and input roles come only from
    the manifest; callers cannot inject arbitrary model text, paths, another
    run/case, URLs, shell/Python/Z3, or reference/gold assets through this API.

    Returns: ``DiscoverCompleted`` containing the immutable check batch,
    confirmed/candidate root nodes, rejected propositions, zero-root flag and
    rationale, model hash, Agent receipt reference, supporting records, and the
    final ``discover_completed`` record ID/hash.

    Execution: validate the fresh record prefix; append run/input/capability
    records; parse and inspect the frozen model; freeze the six-field Agent
    context; expose four bounded read-only investigation tools plus the
    deterministic ``evaluate_checks`` tool; run exactly one ``AgentApp.run`` in
    which the Agent forms, evaluates, investigates, and adjudicates one complete
    check batch; require the final submitted drafts to match an eligible tool
    invocation; validate full proposition/check coverage and all refs; append
    ``discover_completed``; render ``loops/discover.md``; then validate the hash
    chain. Every published stage fact is append-only and tied to the same model.

    Failure semantics: non-fresh output, stale/tampered input, unavailable
    required capability, non-executable FCSTM, empty/invalid checks, unknown or
    replay-invalid evaluation results, provider failure, invalid Agent
    schema, incomplete proposition coverage, forbidden reference content, or
    invalid record/check/source refs fail closed. The run appends a safe
    ``run_failed`` record when a method prefix exists and never publishes a
    partial ``discover_completed`` batch as success.

    Evidence limitations: completion means this run produced an auditable,
    mechanically eligible bounded Discover result. It does not prove check
    semantic fidelity, NL completeness, source closure, absence of missed
    issues, global correctness, repairability, or method-level effectiveness.

    Permissions: Controller code may read only manifest-declared current-run
    inputs and invoke configured providers/pyfcstm. The main Agent is read-only
    and receives only ``read_task``, ``query_model``, ``observe_trace``,
    ``lookup_source_trace``, and deterministic ``evaluate_checks``; no mutation,
    arbitrary path/network/shell/Python/Z3,
    alternate run/case, future-stage, seed/reference/gold, or hidden evaluator
    access is exposed.

    Example: ``run_discover(Path("runs/paper1/discover/case-0001"), registry)``
    returns ``DiscoverCompleted`` and writes all records, context, audit, receipt,
    redaction report, and ``loops/discover.md`` below that same run directory.
    """

    case, manifest = load_run_case(run_dir)
    store = RecordStore(run_dir)
    if store.all():
        raise ValueError("run_discover requires a fresh method record prefix")
    store.append("run_started", {"run_id": manifest["run_id"], "case_id": case.case_id, "profile": manifest["profile"]})
    store.append(
        "input_bridge_completed",
        {
            "model_id": "STM_0",
            "model_sha256": case.fcstm_sha256,
            "source_trace_schema_version": case.source_trace.get("schema_version"),
            "bridge_attribution": "representation_lowering_not_repair",
        },
    )
    _write_capability_manifest(run_dir, manifest)
    checked = check_fcstm(case.fcstm, "inputs/STM_0.fcstm")
    check_record = store.append("check_fcstm_completed", checked)
    if not checked.get("executable"):
        store.append("run_failed", {"failure_reason": "fcstm_not_executable", "check_record_id": check_record["record_id"]})
        raise RuntimeError("fcstm_not_executable")
    current = _current_records(store, case)
    snapshot = freeze_task_snapshot(
        model_text=case.fcstm,
        model_sha256=case.fcstm_sha256,
        normalized_inspect=checked["inspect"],
        current_records=current,
    )
    prompt = system_prompt(manifest["content_language"])
    attempt_id = "discover-attempt-001"
    context_manifest = publish_context(
        store,
        attempt_id=attempt_id,
        system_prompt=prompt,
        snapshot=snapshot,
        content_language=manifest["content_language"],
    )
    evaluation_invocations: list[dict[str, Any]] = []
    guide_access = GuideAccessState()
    read_fcstm_guide = build_read_fcstm_guide(guide_access)
    read_fbmcq_guide = build_read_fbmcq_guide(guide_access)
    read_task = guard_tool(build_read_task(snapshot), guide_access)
    query_model = guard_tool(build_query_model(snapshot), guide_access)
    observe_trace = guard_tool(
        build_observe_trace(snapshot, _trace_runner(case)), guide_access
    )
    lookup_source_trace = guard_tool(
        build_lookup_source_trace(snapshot), guide_access
    )
    evaluate_checks = guard_tool(
        build_evaluate_checks(
            snapshot,
            model_text=case.fcstm,
            check_result=checked,
            model_path=run_dir / "inputs/STM_0.fcstm",
            formal_required=bool(manifest.get("formal_profile", True)),
            invocation_log=evaluation_invocations,
        ),
        guide_access,
        require_fbmcq_when=property_batch_requested,
    )
    tools = (
        read_fcstm_guide,
        read_fbmcq_guide,
        read_task,
        query_model,
        observe_trace,
        lookup_source_trace,
        evaluate_checks,
    )
    if tuple(tool.name for tool in tools) != AGENT_TOOL_NAMES:
        raise AssertionError("Discover Agent physical tool allowlist drift")
    attempt_record = store.append(
        "agent_attempt_started",
        {
            "attempt_id": attempt_id,
            "context_snapshot_head": context_manifest["context_snapshot_head"],
            "allowed_tools": list(AGENT_TOOL_NAMES),
            "required_agent_tool_calls": [
                "read_fcstm_guide",
                "read_task",
                "evaluate_checks",
            ],
            "conditional_agent_tool_calls": {
                "property_batch": ["read_fbmcq_guide"],
            },
        },
    )
    replay_file = manifest.get("test_replay_file")
    if replay_file:
        submission, receipt_ref = _run_replay(run_dir, Path(replay_file))
        read_fcstm_guide.invoke({})
        if any(item.check_kind == "property" for item in submission.check_drafts):
            read_fbmcq_guide.invoke({})
        evaluate_checks.invoke(
            {"checks": [item.model_dump(mode="json") for item in submission.check_drafts]}
        )
        result_status = {"status": "success", "real_llm": False, "academic_eligible": False, "test_replay": True}
    else:
        audit_dir = run_dir / "agent_audit" / "discover"
        audit_dir.mkdir(parents=True, exist_ok=True)
        audit_path = audit_dir / "audit.jsonl"
        result_path = audit_dir / "result.json"
        spec = AgentSpec(
            name="paper1-b-discover",
            system_prompt=prompt,
            tools=tools,
            output_schema=DiscoverSubmission,
            limits=manifest.get("agent_limits") or None,
            require_tool_call=True,
        )
        app = AgentApp.from_registry(
            spec,
            registry,
            profile=manifest["profile"],
            model_options={"streaming": True, "stream_usage": False, "max_retries": 0},
        )
        result = app.run(
            user_prompt(snapshot),
            renderer=manifest["renderer"],
            log_level="INFO",
            audit_out=audit_path,
            result_out=result_path,
            compact_trigger_ratio=0.85,
        )
        if result.status != "success" or not result.real_llm or not result.academic_eligible:
            store.append("agent_attempt_finished", {"attempt_record_id": attempt_record["record_id"], "result": result.to_dict()})
            store.append("run_failed", {"failure_reason": "discover_agent_failed", "error": result.error})
            raise RuntimeError(f"discover_agent_failed:{result.error or result.status}")
        submission = result.require_output()
        if not isinstance(submission, DiscoverSubmission):
            submission = DiscoverSubmission.model_validate(submission)
        runtime_receipt = audit_path.with_name(audit_path.name + ".receipt.json")
        canonical_receipt = audit_dir / "receipt.json"
        runtime_receipt.replace(canonical_receipt)
        _publish_redaction_report(audit_path, audit_dir / "redaction_report.json")
        receipt_ref = AgentReceiptRef(
            audit_path=str(audit_path.relative_to(run_dir)),
            result_path=str(result_path.relative_to(run_dir)),
            receipt_path=str(canonical_receipt.relative_to(run_dir)),
            result_sha256=sha256_file(result_path),
        )
        result_status = result.to_dict()
    attempt_finished = store.append(
        "agent_attempt_finished",
        {"attempt_record_id": attempt_record["record_id"], "result": result_status, "agent_receipt_ref": receipt_ref.model_dump(mode="json")},
    )
    try:
        _validate_guide_protocol(guide_access, submission)
        guide_record = store.append(
            "guide_access_completed",
            {
                "schema_version": "paper1.guide_access.v1",
                "protocol": "fcstm-first;fbmcq-before-property",
                "events": guide_access.events,
                "fcstm_read_at": guide_access.fcstm_read_at,
                "fbmcq_read_at": guide_access.fbmcq_read_at,
            },
        )
        evaluation = _matching_evaluation(submission, evaluation_invocations)
        checks = list(evaluation["issue_checks"])
        preparation_record = store.append(
            "issue_check_preparation_completed",
            {
                "schema_version": "paper1.single_agent_issue_checks.v1",
                "run_id": manifest["run_id"],
                "model_id": "STM_0",
                "model_sha256": case.fcstm_sha256,
                "agent_attempt_record_id": attempt_record["record_id"],
                "drafts_sha256": evaluation["drafts_sha256"],
                "check_drafts": [
                    item.model_dump(mode="json") for item in submission.check_drafts
                ],
                "binding_rejections": evaluation["binding_rejections"],
                "checks": checks,
            },
        )
        scenarios = evaluation["scenarios"]
        scenario_record = store.append("run_scenarios_completed", scenarios)
        properties = evaluation["properties"]
        property_record = store.append("verify_properties_completed", properties)
        static = evaluation["static_consistency"]
        static_record = store.append(
            "check_fcstm_static_consistency_completed", static
        )
        validation = evaluation["validation"]
        validation_record = store.append(
            "validate_discovery_checks_completed", validation
        )
        gate = evaluation["gate"]
        gate_record = store.append(
            "discover_mandatory_preparation_completed", gate
        )
        submission = _augment_submission_evidence(
            submission,
            [
                guide_record["record_id"],
                preparation_record["record_id"],
                scenario_record["record_id"],
                property_record["record_id"],
                static_record["record_id"],
                validation_record["record_id"],
                gate_record["record_id"],
            ],
        )
        accepted_refs = _accepted_source_refs(case, checks, checked["inspect"])
        validated = _validate_submission(
            submission,
            checks=checks,
            records=store.all(),
            executed_check_ids=set(gate["executed_check_ids"]),
            accepted_refs=accepted_refs,
            confirmed_refs=_confirmed_source_refs(case, accepted_refs),
        )
    except Exception as exc:
        store.append(
            "run_failed",
            {
                "failure_reason": "discover_submission_invalid",
                "error_type": type(exc).__name__,
                "error_code": str(exc),
                "attempt_record_id": attempt_record["record_id"],
                "attempt_finished_record_id": attempt_finished["record_id"],
            },
        )
        raise
    supporting = sorted(
        {record_id for root in validated.root_nodes for record_id in root.supporting_record_ids}
        | {
            record_id
            for proposition in validated.rejected_propositions
            for record_id in proposition.supporting_record_ids
        }
    )
    completed_payload = {
        "schema_version": "paper1.discover_completed.v1",
        "run_id": manifest["run_id"],
        "stage": "B-discover",
        "loop_no": 0,
        "model_id": "STM_0",
        "model_sha256": case.fcstm_sha256,
        "issue_checks": checks,
        "root_nodes": [root.model_dump(mode="json") for root in validated.root_nodes],
        "rejected_propositions": [item.model_dump(mode="json") for item in validated.rejected_propositions],
        "no_issue_found": validated.no_issue_found,
        "rationale": validated.rationale,
        "agent_real_llm": bool(result_status.get("real_llm", False)),
        "agent_academic_eligible": bool(result_status.get("academic_eligible", False)),
        "test_replay": bool(result_status.get("test_replay", False)),
        "main_result_eligible": False,
        "agent_receipt_ref": receipt_ref.model_dump(mode="json"),
        "supporting_record_ids": supporting,
        "preparation_record_ids": [
            check_record["record_id"],
            guide_record["record_id"],
            preparation_record["record_id"],
            scenario_record["record_id"],
            property_record["record_id"],
            static_record["record_id"],
            validation_record["record_id"],
            gate_record["record_id"],
            attempt_finished["record_id"],
        ],
    }
    completed_record = store.append("discover_completed", completed_payload)
    completed = DiscoverCompleted(
        **{key: value for key, value in completed_payload.items() if key != "preparation_record_ids"},
        completed_record_id=completed_record["record_id"],
        completed_record_sha256=completed_record["record_sha256"],
    )
    report = render_discover(run_dir, case, completed, store.all(), manifest["content_language"])
    store.append("discover_report_render_completed", {"report_path": str(report.relative_to(run_dir)), "report_sha256": sha256_file(report)})
    store.validate_chain()
    return completed


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run paper1 B-discover Agent")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--pair-id")
    source.add_argument("--case-id")
    parser.add_argument("--nl-file", type=Path)
    parser.add_argument("--fcstm-file", type=Path)
    parser.add_argument("--raw-source-file", type=Path)
    parser.add_argument("--source-trace-file", type=Path)
    parser.add_argument("--profile", default="gpt-5.5")
    parser.add_argument("--content-language", choices=LANGUAGES, default="zh-CN")
    parser.add_argument("--renderer", choices=("auto", "rich", "jsonl", "quiet"), default="rich")
    parser.add_argument("--formal-profile", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--max-model-calls", type=int)
    parser.add_argument("--max-tool-calls", type=int)
    parser.add_argument("--max-turns", type=int)
    parser.add_argument("--max-seconds", type=float)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--replay-file", type=Path, help=argparse.SUPPRESS)
    return parser


def _case_from_args(args: argparse.Namespace) -> PreparedCase:
    if args.pair_id:
        if args.nl_file or args.case_id or args.fcstm_file or args.raw_source_file or args.source_trace_file:
            raise ValueError("pair mode cannot use custom input arguments")
        return load_pair(args.pair_id)
    if not args.nl_file or not args.fcstm_file:
        raise ValueError("custom mode requires --case-id --nl-file --fcstm-file")
    return load_custom(
        args.case_id,
        args.nl_file,
        args.fcstm_file,
        raw_source_file=args.raw_source_file,
        source_trace_file=args.source_trace_file,
    )


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        registry = load_llm_registry(args.config)
        registry.require(args.profile)
        case = _case_from_args(args)
        prepare_run_dir(
            args.output_dir,
            case,
            profile=args.profile,
            content_language=args.content_language,
            renderer=args.renderer,
            formal_profile=args.formal_profile,
            replay_file=args.replay_file,
            agent_limits={
                key: value
                for key, value in {
                    "model_calls": args.max_model_calls,
                    "tool_calls": args.max_tool_calls,
                    "turns": args.max_turns,
                    "seconds": args.max_seconds,
                }.items()
                if value is not None
            },
        )
        result = run_discover(args.output_dir, registry)
        print(
            json.dumps(
                {
                    "status": "discover_completed",
                    "run_id": result.run_id,
                    "record_id": result.completed_record_id,
                    "outdir": str(args.output_dir),
                    "report": str(args.output_dir / "loops/discover.md"),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except Exception as exc:
        print(f"discover failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
