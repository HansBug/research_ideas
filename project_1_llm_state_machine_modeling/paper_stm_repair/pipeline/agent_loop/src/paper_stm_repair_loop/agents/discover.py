from __future__ import annotations

import argparse
import importlib.metadata
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

from pydantic import ConfigDict, model_validator

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
from ..schemas import (
    AgentReceiptRef,
    DiscoverCompleted,
    DiscoverSubmission,
    RejectedProposition,
    RootIssue,
)
from ..tools.check_fcstm import execute as check_fcstm
from ..tools.evaluate_checks import build_tool as build_evaluate_checks
from ..tools.guide_access import (
    GuideAccessState,
    guard_tool,
    property_batch_requested,
)
from ..tools.lookup_source_trace import build_tool as build_lookup_source_trace
from ..tools.mandatory import enforce_mandatory_tool
from ..tools.observe_trace import build_tool as build_observe_trace
from ..tools.post_batch_investigation import PostBatchInvestigationState
from ..tools.query_model import build_tool as build_query_model
from ..tools.read_task import build_tool as build_read_task
from ..tools.read_fbmcq_guide import build_tool as build_read_fbmcq_guide
from ..tools.read_fcstm_guide import build_tool as build_read_fcstm_guide
from ..tools.run_scenarios import observe_events


AGENT_TOOL_NAMES = (
    "read_fcstm_guide",
    "read_fbmcq_guide",
    "read_task",
    "query_model",
    "observe_trace",
    "lookup_source_trace",
    "evaluate_checks",
)

_POST_BATCH_NO_PROGRESS_LIMIT = 3
_NO_PROGRESS_EXECUTION_STATUSES = {
    "execution_error",
    "incomplete",
    "invalid_arguments",
    "mandatory_tool_rejected",
    "prerequisite_required",
    "timeout",
    "tool_unavailable",
    "unknown",
}


def _post_batch_no_progress(
    tool_attempt_log: list[dict[str, Any]],
    *,
    limit: int = _POST_BATCH_NO_PROGRESS_LIMIT,
) -> bool:
    """Return true after a consecutive tail of business calls adds no evidence."""

    if limit < 1 or len(tool_attempt_log) < limit:
        return False
    return all(
        str(item.get("execution_status") or "unknown")
        in _NO_PROGRESS_EXECUTION_STATUSES
        for item in tool_attempt_log[-limit:]
    )


def _pyfcstm_commit() -> str:
    completed = subprocess.run(
        ["git", "-C", str(REPO_ROOT / "pyfcstm"), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else "unknown"


def _pyfcstm_gitlink_commit() -> str:
    completed = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD:pyfcstm"],
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
    pyfcstm_gitlink_commit = _pyfcstm_gitlink_commit()
    commit_consistent = (
        pyfcstm_commit != "unknown"
        and pyfcstm_gitlink_commit != "unknown"
        and pyfcstm_commit == pyfcstm_gitlink_commit
    )
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
        "pyfcstm_gitlink_commit": pyfcstm_gitlink_commit,
        "pyfcstm_git_commit_consistent": commit_consistent,
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
    if not commit_consistent:
        store = RecordStore(run_dir)
        store.append(
            "run_failed",
            {
                "failure_reason": "pyfcstm_gitlink_mismatch",
                "pyfcstm_worktree_commit": pyfcstm_commit,
                "pyfcstm_gitlink_commit": pyfcstm_gitlink_commit,
            },
        )
        raise RuntimeError("pyfcstm_gitlink_mismatch")
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
        return observe_events(case.fcstm, events, "inputs/STM_0.fcstm")

    return run


def _accepted_model_refs(checks: list[dict[str, Any]], inspect: Mapping[str, Any]) -> set[str]:
    refs = {ref for check in checks for ref in check.get("binding_refs", []) if isinstance(ref, str)}
    refs.update(f"state:{item['path']}" for item in inspect.get("states", []) if item.get("path"))
    refs.update(f"event:{item['qualified_name']}" for item in inspect.get("events", []) if item.get("qualified_name"))
    refs.update(
        f"variable:{item['qualified_name']}"
        for item in inspect.get("variables", [])
        if item.get("qualified_name")
    )
    transition_indexes = {
        item["transition_index"]
        for item in inspect.get("transitions", [])
        if item.get("transition_index") is not None
    }
    refs.update(f"transition:{index}" for index in transition_indexes)
    refs.update(f"transition:T{index}" for index in transition_indexes)
    refs.update(
        f"forced_transition:{item['original_raw']}"
        for item in inspect.get("forced_transitions", [])
        if item.get("original_raw")
    )
    return refs


def _trace_reference_sets(
    case: PreparedCase,
    accepted_model_refs: set[str],
) -> tuple[set[str], set[str], set[tuple[str, str]]]:
    """Return available source/model refs and exact one-to-one trace pairs."""

    trace = case.source_trace
    if (
        trace.get("relation_policy") == "exact_identity"
        and case.raw_source_format == "fcstm-identity"
        and case.raw_source == case.fcstm
    ):
        refs = set(accepted_model_refs)
        return refs, refs, {(ref, ref) for ref in refs}

    entries = trace.get("entries")
    if not isinstance(entries, list):
        return set(), set(), set()

    available_source_refs: set[str] = set()
    available_model_refs: set[str] = set()
    source_occurrences: dict[str, list[tuple[int, str]]] = {}
    intermediate_occurrences: dict[str, list[tuple[int, str]]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, Mapping):
            continue
        source_refs = [ref for ref in entry.get("source_elements", []) if isinstance(ref, str) and ref]
        intermediate_refs = [ref for ref in entry.get("intermediate_elements", []) if isinstance(ref, str) and ref]
        available_source_refs.update(source_refs)
        available_model_refs.update(intermediate_refs)
        if len(source_refs) != 1 or len(intermediate_refs) != 1:
            continue
        source_ref, intermediate_ref = source_refs[0], intermediate_refs[0]
        source_occurrences.setdefault(source_ref, []).append((index, intermediate_ref))
        intermediate_occurrences.setdefault(intermediate_ref, []).append((index, source_ref))

    exact_pairs: set[tuple[str, str]] = set()
    for source_ref, occurrences in source_occurrences.items():
        if len(occurrences) != 1:
            continue
        index, intermediate_ref = occurrences[0]
        if intermediate_occurrences.get(intermediate_ref) != [(index, source_ref)]:
            continue
        exact_pairs.add((source_ref, intermediate_ref))
    return available_source_refs, available_model_refs, exact_pairs


def _validate_ref_partition(
    item: RootIssue | RejectedProposition,
    *,
    accepted_model_refs: set[str],
    owner_model_refs: set[str],
    available_source_refs: set[str],
    exact_pairs: set[tuple[str, str]],
) -> None:
    model_refs = set(item.model_element_refs)
    source_refs = set(item.source_element_refs)
    if not model_refs.issubset(accepted_model_refs):
        raise ValueError(f"{item.node_id if isinstance(item, RootIssue) else item.proposition_id} references unaccepted model refs")
    if not model_refs.issubset(owner_model_refs):
        raise ValueError(
            f"{item.node_id if isinstance(item, RootIssue) else item.proposition_id} "
            "references model refs unrelated to its owned checks"
        )
    if not source_refs.issubset(available_source_refs):
        raise ValueError(f"{item.node_id if isinstance(item, RootIssue) else item.proposition_id} references unavailable source refs")
    if not isinstance(item, RootIssue) or item.assessment != "confirmed":
        return
    if not model_refs or not source_refs:
        raise ValueError(f"confirmed root {item.node_id} requires both model and source refs")
    source_to_model = {source: model for source, model in exact_pairs}
    model_to_source = {model: source for source, model in exact_pairs}
    if any(source_to_model.get(source) not in model_refs for source in source_refs):
        raise ValueError(f"confirmed root {item.node_id} lacks exact source-to-model attribution")
    if any(model_to_source.get(model) not in source_refs for model in model_refs):
        raise ValueError(f"confirmed root {item.node_id} lacks exact model-to-source attribution")


def _validate_decision_partition(
    submission: DiscoverSubmission,
    *,
    known_checks: set[str],
    relations: Mapping[str, str],
    origins: Mapping[str, str],
) -> None:
    owners: dict[str, str] = {}

    def claim(check_ids: list[str], owner: str) -> None:
        for check_id in check_ids:
            if check_id in owners:
                raise ValueError(
                    f"final check {check_id} has multiple decision owners: {owners[check_id]}, {owner}"
                )
            owners[check_id] = owner

    for root in submission.root_nodes:
        claim(root.required_check_ids, f"root:{root.node_id}")
    for proposition in submission.rejected_propositions:
        claim(proposition.considered_check_ids, f"rejected:{proposition.proposition_id}")
        nl_relations = {
            relations.get(check_id, "inconclusive")
            for check_id in proposition.considered_check_ids
            if origins.get(check_id) == "nl_grounded_behavioral_issue"
        }
        reason = proposition.rejection_reason
        if nl_relations == {"matches"} and reason != "expectation_matched":
            raise ValueError(
                f"rejected proposition {proposition.proposition_id} must use expectation_matched"
            )
        if "contradicts" in nl_relations and reason not in {
            "check_semantically_invalid",
            "out_of_scope",
            "representation_only",
        }:
            raise ValueError(
                f"rejected proposition {proposition.proposition_id} cannot dismiss a contradicted "
                f"NL check with reason {reason}"
            )
        if "contradicts" not in nl_relations and "inconclusive" in nl_relations and reason == "expectation_matched":
            raise ValueError(
                f"rejected proposition {proposition.proposition_id} has inconclusive, not matched, evidence"
            )
        if not nl_relations and reason == "expectation_matched":
            raise ValueError(
                f"raw-source proposition {proposition.proposition_id} cannot use expectation_matched"
            )
    if set(owners) != known_checks:
        missing = sorted(known_checks - set(owners))
        extra = sorted(set(owners) - known_checks)
        raise ValueError(f"discovery proposition coverage mismatch: missing={missing}, extra={extra}")


def _owned_model_refs(
    check_ids: list[str],
    checks_by_id: Mapping[str, Mapping[str, Any]],
) -> set[str]:
    return {
        ref
        for check_id in check_ids
        for ref in checks_by_id.get(check_id, {}).get("binding_refs", [])
        if isinstance(ref, str)
    }


def _required_scenario_refs(
    check_ids: list[str],
    checks_by_id: Mapping[str, Mapping[str, Any]],
) -> set[str]:
    """Return the tested event, precondition, and target refs for owned scenarios."""

    required: set[str] = set()
    for check_id in check_ids:
        check = checks_by_id.get(check_id, {})
        if check.get("check_kind") != "scenario":
            continue
        spec = check.get("executable_spec")
        expected = check.get("expected_outcome")
        if isinstance(spec, Mapping):
            tested_event = spec.get("tested_event")
            precondition = spec.get("precondition_state")
            if isinstance(tested_event, str) and tested_event:
                required.add(f"event:{tested_event}")
            if isinstance(precondition, str) and precondition:
                required.add(f"state:{precondition}")
        if isinstance(expected, Mapping):
            target = expected.get("state_in")
            if isinstance(target, str) and target:
                required.add(f"state:{target}")
    return required


def _validate_required_scenario_refs(
    item: RootIssue | RejectedProposition,
    *,
    required_refs: set[str],
) -> None:
    missing = sorted(required_refs - set(item.model_element_refs))
    if missing:
        item_id = item.node_id if isinstance(item, RootIssue) else item.proposition_id
        raise ValueError(
            f"{item_id} omits scenario semantic-core refs {missing}; each decision "
            "must cite the final check's tested event, declared precondition, and "
            "expected target instead of attaching an unrelated proposition"
        )


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
    accepted_model_refs: set[str],
    available_source_refs: set[str],
    exact_pairs: set[tuple[str, str]],
    relations: Mapping[str, str],
    origins: Mapping[str, str],
) -> DiscoverSubmission:
    submission = raw if isinstance(raw, DiscoverSubmission) else DiscoverSubmission.model_validate(raw)
    known_checks = {str(check["check_id"]) for check in checks}
    checks_by_id = {str(check["check_id"]): check for check in checks}
    records_by_id = {str(record["record_id"]): record for record in records}
    known_records = set(records_by_id)
    if submission.no_issue_found != (len(submission.root_nodes) == 0):
        raise ValueError("zero-root flag and root batch disagree")
    if not submission.rationale.strip():
        raise ValueError("discovery submission requires a non-empty rationale")
    node_ids: set[str] = set()
    for root in submission.root_nodes:
        if root.node_id in node_ids:
            raise ValueError(f"duplicate root node: {root.node_id}")
        node_ids.add(root.node_id)
        if not root.rationale.strip() or not root.statement.strip():
            raise ValueError(f"root {root.node_id} requires statement and rationale")
        if not set(root.required_check_ids).issubset(known_checks):
            raise ValueError(f"root {root.node_id} references unknown checks")
        if not set(root.supporting_record_ids).issubset(known_records):
            raise ValueError(f"root {root.node_id} references unknown records")
        if not set(root.required_check_ids).issubset(executed_check_ids):
            raise ValueError(f"root {root.node_id} references nonexecuted checks")
        _validate_ref_partition(
            root,
            accepted_model_refs=accepted_model_refs,
            owner_model_refs=_owned_model_refs(root.required_check_ids, checks_by_id),
            available_source_refs=available_source_refs,
            exact_pairs=exact_pairs,
        )
        _validate_required_scenario_refs(
            root,
            required_refs=_required_scenario_refs(
                root.required_check_ids, checks_by_id
            ),
        )
        if root.assessment == "confirmed":
            if not root.downstream_repair_allowed:
                raise ValueError(f"confirmed root {root.node_id} must be repair eligible")
            if not root.required_check_ids:
                raise ValueError(f"confirmed root {root.node_id} lacks executed checks")
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
        _validate_ref_partition(
            proposition,
            accepted_model_refs=accepted_model_refs,
            owner_model_refs=_owned_model_refs(
                proposition.considered_check_ids, checks_by_id
            ),
            available_source_refs=available_source_refs,
            exact_pairs=exact_pairs,
        )
        _validate_required_scenario_refs(
            proposition,
            required_refs=_required_scenario_refs(
                proposition.considered_check_ids, checks_by_id
            ),
        )
    _validate_decision_partition(
        submission,
        known_checks=known_checks,
        relations=relations,
        origins=origins,
    )
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


def _summarize_evaluation_attempts(
    invocation_log: list[dict[str, Any]],
    selected_drafts_sha256: str,
    tool_attempt_log: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    selected_invocation_index = next(
        (
            index
            for index in range(len(invocation_log) - 1, -1, -1)
            if (invocation_log[index].get("result") or {}).get("drafts_sha256")
            == selected_drafts_sha256
            and bool(
                ((invocation_log[index].get("result") or {}).get("gate") or {}).get(
                    "eligible"
                )
            )
        ),
        None,
    )

    invocation_summaries: list[dict[str, Any]] = []
    for index, invocation in enumerate(invocation_log):
        result = invocation.get("result") or {}
        gate = result.get("gate") or {}
        selected = index == selected_invocation_index
        if selected:
            discarded_reason = None
        elif result.get("execution_status") != "completed":
            discarded_reason = "execution_not_completed"
        elif not gate.get("eligible"):
            discarded_reason = "gate_ineligible"
        elif not result.get("issue_checks"):
            discarded_reason = "all_drafts_rejected_or_unbound"
        else:
            discarded_reason = "not_final_submission_batch"
        invocation_summaries.append(
            {
                "snapshot_sha256": invocation.get("snapshot_sha256"),
                "request_sha256": sha256_json(invocation.get("request") or []),
                "request": invocation.get("request") or [],
                "drafts_sha256": result.get("drafts_sha256"),
                "execution_status": result.get("execution_status"),
                "gate_eligible": bool(gate.get("eligible")),
                "gate_reasons": list(gate.get("reasons") or []),
                "gate_remediation": list(gate.get("remediation") or []),
                "binding_rejections": list(result.get("binding_rejections") or []),
                "issue_check_ids": [
                    item.get("check_id")
                    for item in result.get("issue_checks") or []
                    if item.get("check_id")
                ],
                "executed_check_ids": list(gate.get("executed_check_ids") or []),
                "limitations": list(result.get("limitations") or []),
                "selected_for_submission": selected,
                "discarded_reason": discarded_reason,
            }
        )

    evaluate_tool_attempts = [
        item
        for item in tool_attempt_log or []
        if item.get("tool_name") == "evaluate_checks"
    ]
    attempts: list[dict[str, Any]] = []
    invocation_index = 0
    for tool_attempt in evaluate_tool_attempts:
        if tool_attempt.get("tool_executed") is True:
            if invocation_index < len(invocation_summaries):
                item = dict(invocation_summaries[invocation_index])
                invocation_index += 1
            else:
                item = {
                    "snapshot_sha256": None,
                    "request_sha256": None,
                    "request": [],
                    "drafts_sha256": None,
                    "execution_status": tool_attempt.get("execution_status"),
                    "gate_eligible": False,
                    "gate_reasons": ["executed_attempt_missing_invocation_record"],
                    "gate_remediation": [],
                    "binding_rejections": [],
                    "issue_check_ids": [],
                    "executed_check_ids": [],
                    "limitations": ["attempt_record_incomplete"],
                    "selected_for_submission": False,
                    "discarded_reason": "attempt_record_incomplete",
                }
        else:
            arguments = tool_attempt.get("arguments") or {}
            kwargs = arguments.get("kwargs") or {}
            positional = arguments.get("args") or []
            request = kwargs.get("checks")
            if request is None and positional:
                request = positional[0]
            request = request if isinstance(request, list) else []
            execution_status = str(
                tool_attempt.get("execution_status") or "not_executed"
            )
            item = {
                "snapshot_sha256": None,
                "request_sha256": sha256_json(request),
                "request": request,
                "drafts_sha256": sha256_json(request) if request else None,
                "execution_status": execution_status,
                "gate_eligible": False,
                "gate_reasons": [execution_status],
                "gate_remediation": [],
                "binding_rejections": [],
                "issue_check_ids": [],
                "executed_check_ids": [],
                "limitations": [
                    "tool_not_executed",
                    "no_check_evidence_produced",
                ],
                "selected_for_submission": False,
                "discarded_reason": f"{execution_status}_not_executed",
            }
        item.update(
            {
                "protocol_sequence": tool_attempt.get("sequence"),
                "required_tool": tool_attempt.get("required_tool"),
                "tool_executed": bool(tool_attempt.get("tool_executed")),
            }
        )
        attempts.append(item)

    for item in invocation_summaries[invocation_index:]:
        attempts.append(
            {
                **item,
                "protocol_sequence": None,
                "required_tool": None,
                "tool_executed": True,
            }
        )

    if not evaluate_tool_attempts:
        attempts = [
            {
                **item,
                "protocol_sequence": None,
                "required_tool": None,
                "tool_executed": True,
            }
            for item in invocation_summaries
        ]
    for index, item in enumerate(attempts, start=1):
        item["attempt_index"] = index
    selected_attempt_index = next(
        (
            item["attempt_index"]
            for item in attempts
            if item.get("selected_for_submission") is True
        ),
        None,
    )
    return {
        "schema_version": "paper1.evaluate_checks_attempts.v1",
        "selected_drafts_sha256": selected_drafts_sha256,
        "selected_attempt_index": selected_attempt_index,
        "attempt_count": len(attempts),
        "attempts": attempts,
    }


def _check_outcome_relations(evaluation: Mapping[str, Any]) -> dict[str, str]:
    """Project deterministic check results to matches/contradicts/inconclusive."""

    relations: dict[str, str] = {}
    sections = (
        (evaluation.get("scenarios") or {}).get("scenario_results", []),
        (evaluation.get("properties") or {}).get("property_results", []),
        (evaluation.get("static_consistency") or {}).get("static_results", []),
    )
    for items in sections:
        for item in items if isinstance(items, list) else []:
            if not isinstance(item, Mapping) or not item.get("check_id"):
                continue
            relation = item.get("expected_outcome_match_status")
            if relation not in {"matches", "contradicts", "inconclusive"}:
                passed = item.get("passed")
                status = item.get("status")
                if passed is True or status == "passed":
                    relation = "matches"
                elif passed is False or status == "failed":
                    relation = "contradicts"
                else:
                    relation = "inconclusive"
            relations[str(item["check_id"])] = str(relation)
    return relations


def _check_origins(evaluation: Mapping[str, Any]) -> dict[str, str]:
    """Return Controller-bound origins for the final executed checks."""

    return {
        str(item["check_id"]): str(item.get("check_origin") or "unknown")
        for item in evaluation.get("issue_checks", [])
        if isinstance(item, Mapping) and item.get("check_id")
    }


def _build_submit_discovery_response(
    invocation_log: list[dict[str, Any]],
    *,
    accepted_model_refs: set[str],
    available_source_refs: set[str],
    exact_pairs: set[tuple[str, str]],
) -> type[DiscoverSubmission]:
    """Build a run-scoped structured-output contract over live tool evidence."""

    class RunSubmitDiscoveryResponse(DiscoverSubmission):
        model_config = ConfigDict(
            extra="forbid",
            strict=True,
            title="submit_discovery",
        )

        @model_validator(mode="after")
        def validate_current_run_evidence(self) -> "RunSubmitDiscoveryResponse":
            evaluation = _matching_evaluation(self, invocation_log)
            executed_checks = set(
                str(item) for item in (evaluation.get("gate") or {}).get("executed_check_ids", [])
            )
            relations = _check_outcome_relations(evaluation)
            origins = _check_origins(evaluation)
            checks_by_id = {
                str(check["check_id"]): check
                for check in evaluation.get("issue_checks", [])
            }
            known_checks = set(checks_by_id)
            confirmation_possible = bool(exact_pairs)

            if not self.rationale.strip():
                raise ValueError("discovery submission requires a non-empty rationale")

            node_ids: set[str] = set()
            for root in self.root_nodes:
                if root.node_id in node_ids:
                    raise ValueError(f"duplicate root node: {root.node_id}")
                node_ids.add(root.node_id)
                if not root.statement.strip() or not root.rationale.strip():
                    raise ValueError(
                        f"root {root.node_id} requires statement and rationale"
                    )
                required = set(root.required_check_ids)
                if not required.issubset(known_checks):
                    unknown = sorted(required - known_checks)
                    raise ValueError(
                        f"root {root.node_id} references unknown final checks {unknown}; "
                        f"valid final check IDs are {sorted(known_checks)}. Use the "
                        "final evaluate_checks issue_checks[].check_id values, never "
                        "Agent-authored draft check IDs"
                    )
                if not required.issubset(executed_checks):
                    raise ValueError(
                        f"root {root.node_id} references nonexecuted final checks; "
                        "use rejected_propositions with insufficient_evidence"
                    )
                _validate_ref_partition(
                    root,
                    accepted_model_refs=accepted_model_refs,
                    owner_model_refs=_owned_model_refs(
                        root.required_check_ids, checks_by_id
                    ),
                    available_source_refs=available_source_refs,
                    exact_pairs=exact_pairs,
                )
                _validate_required_scenario_refs(
                    root,
                    required_refs=_required_scenario_refs(
                        root.required_check_ids, checks_by_id
                    ),
                )
                matched_nl_checks = sorted(
                    check_id
                    for check_id in required
                    if origins.get(check_id) == "nl_grounded_behavioral_issue"
                    and relations.get(check_id) == "matches"
                )
                if matched_nl_checks:
                    raise ValueError(
                        f"root {root.node_id} cites NL-grounded checks that matched their expectations: "
                        f"{matched_nl_checks}; "
                        "passing behavior belongs in rejected_propositions, not root_nodes"
                    )
                if root.assessment == "confirmed":
                    if not confirmation_possible:
                        raise ValueError(
                            "confirmed roots are impossible because this run lacks deterministic "
                            "one-to-one source attribution; use candidate_only"
                        )
                    noncontradicted_nl_checks = sorted(
                        check_id
                        for check_id in required
                        if origins.get(check_id) == "nl_grounded_behavioral_issue"
                        and relations.get(check_id) != "contradicts"
                    )
                    if noncontradicted_nl_checks:
                        raise ValueError(
                            f"confirmed root {root.node_id} has NL-grounded checks without a "
                            f"contradicted expectation: {noncontradicted_nl_checks}"
                        )

            proposition_ids: set[str] = set()
            for proposition in self.rejected_propositions:
                if proposition.proposition_id in proposition_ids or proposition.proposition_id in node_ids:
                    raise ValueError(f"duplicate proposition id: {proposition.proposition_id}")
                proposition_ids.add(proposition.proposition_id)
                if not proposition.statement.strip() or not proposition.rationale.strip():
                    raise ValueError(
                        f"rejected proposition {proposition.proposition_id} "
                        "requires statement and rationale"
                    )
                rejected_checks = set(proposition.considered_check_ids)
                if not rejected_checks.issubset(known_checks):
                    unknown = sorted(rejected_checks - known_checks)
                    raise ValueError(
                        f"rejected proposition {proposition.proposition_id} references "
                        f"unknown final checks {unknown}; valid final check IDs are "
                        f"{sorted(known_checks)}. Use the final evaluate_checks "
                        "issue_checks[].check_id values, never Agent-authored draft "
                        "check IDs"
                    )
                _validate_ref_partition(
                    proposition,
                    accepted_model_refs=accepted_model_refs,
                    owner_model_refs=_owned_model_refs(
                        proposition.considered_check_ids, checks_by_id
                    ),
                    available_source_refs=available_source_refs,
                    exact_pairs=exact_pairs,
                )
                _validate_required_scenario_refs(
                    proposition,
                    required_refs=_required_scenario_refs(
                        proposition.considered_check_ids, checks_by_id
                    ),
                )

            if self.no_issue_found != (len(self.root_nodes) == 0):
                raise ValueError("zero-root flag and root batch disagree")
            _validate_decision_partition(
                self,
                known_checks=known_checks,
                relations=relations,
                origins=origins,
            )
            return self

    RunSubmitDiscoveryResponse.__name__ = "submit_discovery"
    return RunSubmitDiscoveryResponse


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
    if state.first_attempt_at("read_task", after=fcstm_read) is None:
        raise ValueError("read_task was not called after read_fcstm_guide")

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
        item
        for item in property_attempts
        if int(item["sequence"]) < fbmcq_read
        and item.get("tool_executed") is not False
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


def _record_agent_failure(
    store: RecordStore,
    *,
    attempt_record_id: str,
    failure_reason: str,
    error: BaseException,
    result: Any | None = None,
) -> None:
    """Append the two terminal records required for an unsuccessful attempt."""

    result_payload = (
        result.to_dict()
        if result is not None and hasattr(result, "to_dict")
        else {
            "status": "failed",
            "real_llm": True,
            "academic_eligible": False,
            "error": {
                "type": type(error).__name__,
                "message": str(error),
            },
        }
    )
    finished = store.append(
        "agent_attempt_finished",
        {
            "attempt_record_id": attempt_record_id,
            "result": result_payload,
            "termination": "interrupted"
            if isinstance(error, KeyboardInterrupt)
            else "failed",
        },
    )
    store.append(
        "run_failed",
        {
            "failure_reason": failure_reason,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "attempt_record_id": attempt_record_id,
            "attempt_finished_record_id": finished["record_id"],
        },
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
    and receives only ``read_fcstm_guide``, ``read_fbmcq_guide``, ``read_task``,
    ``query_model``, ``observe_trace``, ``lookup_source_trace``, and deterministic
    ``evaluate_checks``; no mutation, arbitrary path/network/shell/Python/Z3,
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
    accepted_model_refs = _accepted_model_refs([], checked["inspect"])
    available_source_refs, _trace_model_refs, exact_pairs = _trace_reference_sets(
        case,
        accepted_model_refs,
    )
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
    tool_attempt_log: list[dict[str, Any]] = []
    investigation_state = PostBatchInvestigationState(evaluation_invocations)
    guide_access = GuideAccessState()

    def mandatory_tool_choice() -> str | None:
        """Force protocol steps without choosing Discover content."""

        if not guide_access.has_read("fcstm"):
            return "read_fcstm_guide"
        if guide_access.first_attempt_at(
            "read_task", after=guide_access.fcstm_read_at
        ) is None:
            return "read_task"
        property_attempted = any(
            item.get("event") == "tool_attempt"
            and item.get("tool_name") == "evaluate_checks"
            and item.get("property_batch") is True
            for item in guide_access.events
        )
        if property_attempted and not guide_access.has_read("fbmcq"):
            return "read_fbmcq_guide"
        if investigation_state.latest_eligible_batch() is None:
            return "evaluate_checks"
        if _post_batch_no_progress(tool_attempt_log):
            return "submit_discovery"
        return None

    base_read_fcstm_guide = build_read_fcstm_guide(guide_access)
    base_read_fbmcq_guide = build_read_fbmcq_guide(guide_access)
    base_read_task = guard_tool(build_read_task(snapshot), guide_access)
    base_query_model = guard_tool(
        build_query_model(snapshot, investigation_state), guide_access
    )
    base_observe_trace = guard_tool(
        build_observe_trace(snapshot, _trace_runner(case), investigation_state),
        guide_access,
    )
    base_lookup_source_trace = guard_tool(
        build_lookup_source_trace(snapshot, investigation_state), guide_access
    )
    base_evaluate_checks = guard_tool(
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
    tools = tuple(
        enforce_mandatory_tool(tool, mandatory_tool_choice, tool_attempt_log)
        for tool in (
            base_read_fcstm_guide,
            base_read_fbmcq_guide,
            base_read_task,
            base_query_model,
            base_observe_trace,
            base_lookup_source_trace,
            base_evaluate_checks,
        )
    )
    (
        read_fcstm_guide,
        read_fbmcq_guide,
        read_task,
        query_model,
        observe_trace,
        lookup_source_trace,
        evaluate_checks,
    ) = tools
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
            "tool_choice_policy": "paper1-discover-mandatory-v2",
            "tool_choice_policy_scope": (
                "mandatory_protocol_steps_and_post_batch_no_progress_submission"
            ),
            "post_batch_no_progress_limit": _POST_BATCH_NO_PROGRESS_LIMIT,
        },
    )
    replay_file = manifest.get("test_replay_file")
    if replay_file:
        submission, receipt_ref = _run_replay(run_dir, Path(replay_file))
        read_fcstm_guide.invoke({})
        read_task.invoke({})
        if any(item.check_kind == "property" for item in submission.check_drafts):
            evaluate_checks.invoke(
                {
                    "checks": [
                        item.model_dump(mode="json")
                        for item in submission.check_drafts
                    ]
                }
            )
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
            output_schema=_build_submit_discovery_response(
                evaluation_invocations,
                accepted_model_refs=accepted_model_refs,
                available_source_refs=available_source_refs,
                exact_pairs=exact_pairs,
            ),
            limits=manifest.get("agent_limits") or None,
            require_tool_call=True,
            retry_missing_structured_output=True,
        )
        app = AgentApp.from_registry(
            spec,
            registry,
            profile=manifest["profile"],
            model_options={"streaming": True, "stream_usage": False, "max_retries": 0},
        )
        result = None
        failure_recorded = False

        try:
            result = app.run(
                user_prompt(snapshot),
                renderer=manifest["renderer"],
                log_level="INFO",
                audit_out=audit_path,
                result_out=result_path,
                compact_trigger_ratio=0.85,
                tool_choice_resolver=mandatory_tool_choice,
                tool_choice_policy_name="paper1-discover-mandatory-v2",
            )
            if (
                result.status != "success"
                or not result.real_llm
                or not result.academic_eligible
            ):
                failure = RuntimeError(
                    f"discover_agent_failed:{result.error or result.status}"
                )
                _record_agent_failure(
                    store,
                    attempt_record_id=attempt_record["record_id"],
                    failure_reason="discover_agent_failed",
                    error=failure,
                    result=result,
                )
                failure_recorded = True
                raise failure
            submission = result.require_output()
            if not isinstance(submission, DiscoverSubmission):
                submission = DiscoverSubmission.model_validate(submission)
            runtime_receipt = audit_path.with_name(audit_path.name + ".receipt.json")
            canonical_receipt = audit_dir / "receipt.json"
            runtime_receipt.replace(canonical_receipt)
            _publish_redaction_report(
                audit_path, audit_dir / "redaction_report.json"
            )
            receipt_ref = AgentReceiptRef(
                audit_path=str(audit_path.relative_to(run_dir)),
                result_path=str(result_path.relative_to(run_dir)),
                receipt_path=str(canonical_receipt.relative_to(run_dir)),
                result_sha256=sha256_file(result_path),
            )
            result_status = result.to_dict()
        except BaseException as exc:
            if not failure_recorded:
                _record_agent_failure(
                    store,
                    attempt_record_id=attempt_record["record_id"],
                    failure_reason=(
                        "discover_agent_interrupted"
                        if isinstance(exc, KeyboardInterrupt)
                        else "discover_agent_exception"
                    ),
                    error=exc,
                    result=result,
                )
            raise
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
                "protocol": "fcstm-first;read-task-required;fbmcq-before-property",
                "events": guide_access.events,
                "fcstm_read_at": guide_access.fcstm_read_at,
                "read_task_at": guide_access.first_attempt_at(
                    "read_task", after=guide_access.fcstm_read_at
                ),
                "fbmcq_read_at": guide_access.fbmcq_read_at,
            },
        )
        evaluation = _matching_evaluation(submission, evaluation_invocations)
        attempts_record = store.append(
            "evaluate_checks_attempts_completed",
            {
                **_summarize_evaluation_attempts(
                    evaluation_invocations,
                    evaluation["drafts_sha256"],
                    tool_attempt_log,
                ),
                "agent_attempt_record_id": attempt_record["record_id"],
            },
        )
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
                attempts_record["record_id"],
                preparation_record["record_id"],
                scenario_record["record_id"],
                property_record["record_id"],
                static_record["record_id"],
                validation_record["record_id"],
                gate_record["record_id"],
            ],
        )
        accepted_model_refs = _accepted_model_refs(checks, checked["inspect"])
        available_source_refs, _trace_model_refs, exact_pairs = _trace_reference_sets(
            case,
            accepted_model_refs,
        )
        validated = _validate_submission(
            submission,
            checks=checks,
            records=store.all(),
            executed_check_ids=set(gate["executed_check_ids"]),
            accepted_model_refs=accepted_model_refs,
            available_source_refs=available_source_refs,
            exact_pairs=exact_pairs,
            relations=_check_outcome_relations(evaluation),
            origins=_check_origins(evaluation),
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
        # B-discover owns bounded issue discovery, not terminal experiment
        # eligibility. The post-loop experiment gate must make that decision.
        "main_result_eligible": False,
        "main_result_eligibility_owner": "post_loop_experiment_gate",
        "main_result_eligibility_reason": (
            "B-discover is an intermediate method stage; only the post-loop "
            "experiment gate may admit a complete run into main-result statistics."
        ),
        "agent_receipt_ref": receipt_ref.model_dump(mode="json"),
        "supporting_record_ids": supporting,
        "preparation_record_ids": [
            check_record["record_id"],
            guide_record["record_id"],
            attempts_record["record_id"],
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


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def _positive_finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed) or parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive finite number")
    return parsed


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
    parser.add_argument("--max-model-calls", type=_positive_int)
    parser.add_argument("--max-tool-calls", type=_positive_int)
    parser.add_argument("--max-turns", type=_positive_int)
    parser.add_argument("--max-seconds", type=_positive_finite_float)
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
