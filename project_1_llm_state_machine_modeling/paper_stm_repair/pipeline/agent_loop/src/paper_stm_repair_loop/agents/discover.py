from __future__ import annotations

import argparse
import importlib.metadata
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping

from pydantic import model_validator

from pyfcstm.config.meta import __VERSION__ as PYFCSTM_SOURCE_VERSION
from pyfcstm.llm import (
    get_fbmcq_language_guide_prompt_metadata_for_llm,
    get_grammar_guide_prompt_metadata_for_llm,
)
from utils.agent import AgentApp, AgentSpec
from utils.llm import LLMRegistry, load_llm_registry

from ..config import LANGUAGES, REPO_ROOT
from ..context import publish_context, validate_reference_blind
from ..eval_env import EvalEnvironment
from ..controller import DiscoverController
from ..inputs import (
    PreparedCase,
    load_custom,
    load_pair,
    load_run_case,
    prepare_run_dir,
)
from ..prompts.discover import system_prompt, user_prompt
from ..records import RecordStore, sha256_file, sha256_json
from ..renderer import render_discover
from ..schemas import (
    AgentReceiptRef,
    DiscoverCompleted,
    DiscoverOutcome,
    DiscoverSubmission,
)
from ..schemas.coverage import CoverageRequirement, InputSegment, SourceFact
from ..schemas.coverage_review import CoverageReviewVerdict
from ..schemas.inspect import InspectModelInput, InspectModelResult
from ..schemas.tool_reason import EvalAssertInput
from ..schemas.tools import (
    ObserveTraceInput,
    QueryModelInput,
    ReadGuideInput,
    ReadTaskInput,
)
from ..tools.check_fcstm import execute as check_fcstm
from ..tools.inspect_model import project_check_result
from ..tools.eval_assert import build_tool as build_eval_assert
from ..tools.guide_access import GuideAccessState, guard_tool
from ..tools.inspect_model import build_tool as build_inspect_model
from ..tools.lookup_source_trace import build_tool as build_lookup_source_trace
from ..tools.mandatory import enforce_mandatory_tool
from ..tools.observe_trace import build_tool as build_observe_trace
from ..tools.query_model import build_tool as build_query_model
from ..tools.read_fbmcq_guide import build_tool as build_read_fbmcq_guide
from ..tools.read_fcstm_guide import build_tool as build_read_fcstm_guide
from ..tools.read_task import build_tool as build_read_task
from ..tools.register_coverage_plan import build_tool as build_register_coverage_plan
from ..tools.review_discovery_coverage import (
    CoverageReviewGate,
    LLMCoverageReviewRunner,
    build_tool as build_review_discovery_coverage,
)
from ..tools.revise_assertion import build_tool as build_revise_assertion


AGENT_TOOL_NAMES = (
    "read_fcstm_guide",
    "read_fbmcq_guide",
    "read_task",
    "inspect_model",
    "register_coverage_plan",
    "revise_assertion",
    "query_model",
    "eval_assert",
    "observe_trace",
    "lookup_source_trace",
    "review_discovery_coverage",
)


def _agent_tool_names(*, formal_profile: bool) -> tuple[str, ...]:
    if formal_profile:
        return AGENT_TOOL_NAMES
    return tuple(name for name in AGENT_TOOL_NAMES if name != "read_fbmcq_guide")


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


def _schema_hashes() -> dict[str, str]:
    """Return stable hashes for the Agent-visible Issue #165 contract schemas."""

    models = {
        "DiscoverOutcome": DiscoverOutcome,
        "DiscoverSubmission": DiscoverSubmission,
        "CoverageRequirement": CoverageRequirement,
        "InputSegment": InputSegment,
        "SourceFact": SourceFact,
        "CoverageReviewVerdict": CoverageReviewVerdict,
        "InspectModelInput": InspectModelInput,
        "InspectModelResult": InspectModelResult,
        "ReadGuideInput": ReadGuideInput,
        "ReadTaskInput": ReadTaskInput,
        "QueryModelInput": QueryModelInput,
        "ObserveTraceInput": ObserveTraceInput,
        "EvalAssertInput": EvalAssertInput,
    }
    return {
        name: sha256_json(model.model_json_schema())
        for name, model in sorted(models.items())
    }


def _diagnostic_registry_identity(check_result: Mapping[str, Any]) -> dict[str, Any]:
    try:
        from pyfcstm.diagnostics import CODE_REGISTRY

        codes = {
            str(code): {
                "severity": str(getattr(spec, "severity", "")),
                "description_sha256": sha256_json(
                    str(getattr(spec, "description", ""))
                ),
            }
            for code, spec in sorted(CODE_REGISTRY.items())
        }
        status = "available"
    except Exception as exc:
        codes = {}
        status = f"unavailable:{type(exc).__name__}"
    observed = sorted(
        {
            str(item.get("code"))
            for item in check_result.get("diagnostics", [])
            if isinstance(item, Mapping) and item.get("code")
        }
    )
    return {
        "schema_version": "pyfcstm.diagnostic_registry_identity.v1",
        "status": status,
        "registry_size": len(codes),
        "registry_sha256": sha256_json(codes),
        "observed_codes": observed,
        "observed_codes_sha256": sha256_json(observed),
    }


def _write_capability_manifest(
    run_dir: Path,
    manifest: Mapping[str, Any],
    case: PreparedCase,
    check_result: Mapping[str, Any],
) -> dict[str, Any]:
    """Freeze pyfcstm/tool capability identity before Agent dispatch."""

    try:
        from pyfcstm.entry.bmc import build_bmc_output  # noqa: F401

        bmc_available = True
    except Exception:
        bmc_available = False
    formal_required = bool(manifest.get("formal_profile", True))
    distribution_version = importlib.metadata.version("pyfcstm")
    commit = _pyfcstm_commit()
    gitlink = _pyfcstm_gitlink_commit()
    prompt_resources = {
        "fcstm": dict(get_grammar_guide_prompt_metadata_for_llm()),
        "fbmcq": dict(get_fbmcq_language_guide_prompt_metadata_for_llm()),
    }
    version_consistent = distribution_version == PYFCSTM_SOURCE_VERSION and all(
        item.get("pyfcstm_version") == PYFCSTM_SOURCE_VERSION
        for item in prompt_resources.values()
    )
    commit_consistent = commit != "unknown" and commit == gitlink
    fbmcq_limits = dict(manifest.get("fbmcq_limits") or {})
    evidence_policy = {
        "policy_id": "paper1-discover-issue165-v1",
        "formal_profile": formal_required,
        "fbmcq_limits": fbmcq_limits,
        "tool_choice": "proposition_quantification_v1",
    }
    try:
        env = EvalEnvironment(
            model_text=case.fcstm if check_result.get("executable") else None,
            model_path="inputs/STM_0.fcstm",
            inspect=check_result.get("inspect") or {},
            source_mappings=case.source_trace.get("entries") or [],
            timeout_seconds=None,
            formal_verification_enabled=formal_required,
            fbmcq_solver_timeout_ms=fbmcq_limits.get("solver_timeout_ms"),
            fbmcq_max_bound=fbmcq_limits.get("max_bound"),
            fbmcq_process_wall_seconds=fbmcq_limits.get("process_wall_seconds"),
        )
        topology_path_available = "topology" in env.locals and "path" in env.locals
        function_registry_hash = env.function_registry_hash
    except Exception:
        topology_path_available = False
        function_registry_hash = "unavailable"
    inspect_projection = project_check_result(
        check_result, reason="Capability manifest freezes inspect_model result schema."
    )
    capabilities = {
        "schema_version": "paper1.capability_manifest.v3",
        "issue_contract_ref": "Issue #165 §11.2",
        "experiment_profile": "full" if formal_required else "non-formal-ablation",
        "pyfcstm_version": PYFCSTM_SOURCE_VERSION,
        "pyfcstm_distribution_version": distribution_version,
        "pyfcstm_version_consistent": version_consistent,
        "pyfcstm_git_commit": commit,
        "pyfcstm_gitlink_commit": gitlink,
        "pyfcstm_git_commit_consistent": commit_consistent,
        "schema_hashes": _schema_hashes(),
        "prompt_resources": prompt_resources,
        "prompt_evidence_policy_fingerprint": sha256_json(
            {
                "system_prompt": system_prompt(
                    str(manifest.get("content_language") or "zh-CN"),
                    formal_profile=formal_required,
                ),
                "prompt_resources": prompt_resources,
                "evidence_policy": evidence_policy,
            }
        ),
        "evidence_policy": {
            **evidence_policy,
            "policy_hash": sha256_json(evidence_policy),
            "evidence_policy_fingerprint": sha256_json(evidence_policy),
        },
        "agent_tools": list(_agent_tool_names(formal_profile=formal_required)),
        "eval_functions": [
            "states",
            "events",
            "variables",
            "initial_child",
            "transitions",
            "transition_exists",
            "guards_overlap",
            "effects",
            "effect_delta",
            "effect_deltas",
            "topology",
            "path",
            "simulate",
            "mapped_source_refs",
            "mapped_fcstm_refs",
            "bound_model_refs",
        ]
        + (["fbmcq"] if formal_required else []),
        "hot_start_capability": {
            "available": True,
            "mode": "exact_state_and_complete_variables",
            "missing_or_partial_initial_vars_policy": "fail_closed",
        },
        "topology_path_backend": {
            "available": topology_path_available,
            "backend": "paper_stm_repair_loop.eval_env.topology.TopologyAPI",
            "source": "controller_frozen_inspect_plus_pyfcstm_topology",
            "function_registry_hash": function_registry_hash,
        },
        "process_isolation_policy": {
            "fbmcq_backend": "multiprocessing_spawn",
            "result_transport": "private_temporary_json_file",
            "fallback_for_unpickleable_test_seam": "direct_unpickleable_test_seam",
            "process_wall_seconds": fbmcq_limits.get("process_wall_seconds"),
            "timeout_policy": "terminate_then_kill_fail_closed",
        },
        "cli_resource_profile": {
            "agent_limits": dict(manifest.get("agent_limits") or {}),
            "reviewer_limits": dict(manifest.get("reviewer_limits") or {}),
            "fbmcq_limits": fbmcq_limits,
            "python_executable": sys.executable,
            "process_id": os.getpid(),
        },
        "frozen_check_result": {
            "check_result_sha256": sha256_json(dict(check_result)),
            "check_record_id": check_result.get("record_id"),
            "check_record_sha256": check_result.get("record_sha256"),
            "model_sha256": case.fcstm_sha256,
            "parse_status": check_result.get("parse_status"),
            "semantic_status": check_result.get("semantic_status"),
            "inspect_status": check_result.get("inspect_status"),
            "executable": bool(check_result.get("executable", False)),
        },
        "diagnostic_schema_code_registry_identity": _diagnostic_registry_identity(
            check_result
        ),
        "inspect_model_result_schema_hash": sha256_json(
            InspectModelResult.model_json_schema()
        ),
        "inspect_model_result_sha256": sha256_json(inspect_projection),
        "bmc_backend_available": bmc_available,
        "formal_verification_available": formal_required and bmc_available,
        "formal_claim_eligible": formal_required and bmc_available,
    }
    store = RecordStore(run_dir)
    store.write_immutable_json("capability_manifest.json", capabilities)
    store.append("capability_manifest", capabilities)
    if not version_consistent:
        store.append(
            "run_failed",
            {
                "failure_reason": "pyfcstm_version_mismatch",
                "source_version": PYFCSTM_SOURCE_VERSION,
                "distribution_version": distribution_version,
            },
        )
        raise RuntimeError("pyfcstm_version_mismatch")
    if not commit_consistent:
        store.append(
            "run_failed",
            {
                "failure_reason": "pyfcstm_gitlink_mismatch",
                "pyfcstm_worktree_commit": commit,
                "pyfcstm_gitlink_commit": gitlink,
            },
        )
        raise RuntimeError("pyfcstm_gitlink_mismatch")
    if formal_required and not bmc_available:
        store.append(
            "run_failed",
            {
                "failure_reason": "required_capability_unavailable",
                "capability": "fbmcq",
            },
        )
        raise RuntimeError("required_capability_unavailable:fbmcq")
    return capabilities


def _without_rationale(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): _without_rationale(item)
            for key, item in value.items()
            if key not in {"rationale", "reason"}
        }
    if isinstance(value, list):
        return [_without_rationale(item) for item in value]
    return value


def _projection_mismatches(
    expected: Any,
    actual: Any,
    *,
    path: str = "outcome",
    limit: int = 24,
) -> list[str]:
    """Return bounded field-level guidance for a rejected terminal projection."""

    mismatches: list[str] = []

    def preview(value: Any) -> str:
        rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
        return rendered if len(rendered) <= 240 else rendered[:237] + "..."

    def compare(expected_value: Any, actual_value: Any, current_path: str) -> None:
        if len(mismatches) >= limit:
            return
        if isinstance(expected_value, dict) and isinstance(actual_value, dict):
            expected_keys = set(expected_value)
            actual_keys = set(actual_value)
            for key in sorted(expected_keys - actual_keys):
                if len(mismatches) >= limit:
                    return
                mismatches.append(
                    f"{current_path}.{key}: missing; expected="
                    f"{preview(expected_value[key])}"
                )
            for key in sorted(actual_keys - expected_keys):
                if len(mismatches) >= limit:
                    return
                mismatches.append(
                    f"{current_path}.{key}: unexpected; actual="
                    f"{preview(actual_value[key])}"
                )
            for key in sorted(expected_keys & actual_keys):
                compare(expected_value[key], actual_value[key], f"{current_path}.{key}")
            return
        if isinstance(expected_value, list) and isinstance(actual_value, list):
            if len(expected_value) != len(actual_value):
                mismatches.append(
                    f"{current_path}: list length actual={len(actual_value)}; "
                    f"expected={len(expected_value)}"
                )
            for index, (expected_item, actual_item) in enumerate(
                zip(expected_value, actual_value)
            ):
                compare(expected_item, actual_item, f"{current_path}[{index}]")
            return
        if expected_value != actual_value:
            mismatches.append(
                f"{current_path}: actual={preview(actual_value)}; "
                f"expected={preview(expected_value)}"
            )

    compare(expected, actual, path)
    return mismatches


def _build_submit_schema(controller: DiscoverController) -> type[DiscoverSubmission]:
    """Create the provider-native terminal schema tied to Controller state."""

    class SubmitDiscoveryResponse(DiscoverSubmission):
        @model_validator(mode="after")
        def validate_against_controller(self) -> "SubmitDiscoveryResponse":
            projection = controller.projection(record_gate=False)
            submitted = self.outcome.model_dump(mode="json")
            expected = _without_rationale(projection)
            actual = _without_rationale(submitted)
            if actual != expected:
                mismatches = _projection_mismatches(expected, actual)
                raise ValueError(
                    "submit_discovery outcome must match the Controller projection; "
                    f"field_mismatches={json.dumps(mismatches, ensure_ascii=False)}; "
                    "corrective_action=copy every named expected value into the next "
                    "submit_discovery outcome, preserve all unmentioned Controller "
                    "fields, and do not submit a shortened projection"
                )
            return self

    SubmitDiscoveryResponse.__name__ = "submit_discovery"
    SubmitDiscoveryResponse.__qualname__ = "submit_discovery"
    return SubmitDiscoveryResponse


def _build_tools(
    controller: DiscoverController,
    snapshot: dict[str, Any],
    attempt_log: list[dict[str, Any]],
    review_gate: CoverageReviewGate | None = None,
) -> tuple[tuple[Any, ...], Any]:
    registry = controller.require_registry()
    state = controller.guide_access
    if review_gate is None and registry.semantic_review_gate is not None:
        review_gate = registry.semantic_review_gate
    if review_gate is None:
        def unavailable_review_runner(*_args: Any, **_kwargs: Any) -> Any:
            raise RuntimeError("coverage_review_runner_not_configured")

        review_gate = CoverageReviewGate(
            registry=registry,
            task_snapshot=snapshot,
            runner=unavailable_review_runner,
        )
        registry.semantic_review_gate = review_gate

    def mandatory_tool_choice() -> str | None:
        if not state.has_read("fcstm"):
            return "read_fcstm_guide"
        if state.first_attempt_at("read_task", after=state.fcstm_read_at) is None:
            return "read_task"
        if bool(controller.manifest.get("formal_profile", True)) and not state.has_read(
            "fbmcq"
        ):
            return "read_fbmcq_guide"
        required_read_count = (
            3 if bool(controller.manifest.get("formal_profile", True)) else 2
        )
        executed_attempt_count = sum(
            1 for item in attempt_log if item.get("tool_executed") is True
        )
        if (
            not registry.plan_registered
            and executed_attempt_count > required_read_count
        ):
            return "register_coverage_plan"
        if review_gate.has_terminal_failure():
            raise RuntimeError("discover_reviewer_contract_failure")
        if registry.plan_registered and registry.missing_latest_required_assertions():
            return "eval_assert"
        if registry.plan_registered and registry.incomplete_latest_required_assertions():
            return "revise_assertion"
        latest_review = review_gate.latest_result or {}
        if (
            registry.plan_registered
            and not registry.missing_latest_required_assertions()
            and not registry.incomplete_latest_required_assertions()
            and not review_gate.has_terminal_failure()
            and not review_gate.current_passed()
            and (
                review_gate.latest_result is None
                or latest_review.get("execution_status")
                == "retryable_reviewer_failure"
                or bool(latest_review.get("programmatic_errors"))
                or (
                    latest_review.get("passed") is True
                    and latest_review.get("reviewed_state_fingerprint")
                    != review_gate.state_fingerprint()
                )
            )
        ):
            return "review_discovery_coverage"
        return None

    fcstm_guide = build_read_fcstm_guide(state)
    fbmcq_guide = build_read_fbmcq_guide(state)
    guarded = (
        guard_tool(build_read_task(snapshot), state),
        guard_tool(build_inspect_model(controller.check_result), state),
        guard_tool(build_register_coverage_plan(registry), state),
        guard_tool(build_revise_assertion(registry), state),
        guard_tool(
            build_query_model(
                snapshot,
                registered_root_ids=lambda: set(registry.roots),
            ),
            state,
        ),
        guard_tool(build_eval_assert(registry), state),
        guard_tool(
            build_observe_trace(
                snapshot,
                registered_root_ids=lambda: set(registry.roots),
            ),
            state,
        ),
        guard_tool(build_lookup_source_trace(snapshot), state),
        guard_tool(build_review_discovery_coverage(review_gate), state),
    )
    physical = (
        (fcstm_guide, fbmcq_guide, *guarded)
        if bool(controller.manifest.get("formal_profile", True))
        else (fcstm_guide, *guarded)
    )
    tools = tuple(
        enforce_mandatory_tool(tool, mandatory_tool_choice, attempt_log)
        for tool in physical
    )
    expected_names = _agent_tool_names(
        formal_profile=bool(controller.manifest.get("formal_profile", True))
    )
    if tuple(tool.name for tool in tools) != expected_names:
        raise AssertionError("Discover Agent physical tool allowlist drift")
    return tools, mandatory_tool_choice


def _validate_guide_protocol(controller: DiscoverController) -> None:
    state = controller.guide_access
    if state.fcstm_read_at is None:
        raise ValueError("fcstm_guide_not_read")
    read_task_at = state.first_attempt_at("read_task", after=state.fcstm_read_at)
    if read_task_at is None:
        raise ValueError("read_task_not_called_after_fcstm_guide")
    if bool(controller.manifest.get("formal_profile", True)):
        if state.fbmcq_read_at is None or state.fbmcq_read_at <= read_task_at:
            raise ValueError("fbmcq_guide_not_read_after_task")
    registry = controller.require_registry()
    if any(
        "fbmcq(" in version.assert_text for version in registry.latest_versions()
    ) and state.fbmcq_read_at is None:
        raise ValueError("fbmcq_guide_not_read_before_fbmcq_assertion")


def _coverage_plan_publication(controller: DiscoverController) -> dict[str, Any]:
    registry = controller.require_registry()
    return {
        "schema_version": "paper1.coverage_plan_publication.v1",
        "segment_dispositions": [
            item for _, item in sorted(registry.segment_dispositions.items())
        ],
        "fact_dispositions": [
            item for _, item in sorted(registry.fact_dispositions.items())
        ],
        "coverage_units": [
            item for _, item in sorted(registry.coverage_units.items())
        ],
        "proposition_roots": [item for _, item in sorted(registry.roots.items())],
        "assertion_chains": {
            chain_id: [version.to_record() for version in versions]
            for chain_id, versions in sorted(registry.chains.items())
        },
        "registration_reason": registry.registered_plan_reason,
    }


def _publish_redaction_report(audit_path: Path, destination: Path) -> Path:
    """Create the canonical redaction report from the Agent receipt."""

    receipt_path = audit_path.with_name(audit_path.name + ".receipt.json")
    report: dict[str, Any] = {
        "schema_version": "paper1.agent_redaction_report.v1",
        "audit_path": audit_path.name,
        "receipt_path": receipt_path.name if receipt_path.exists() else None,
        "redaction_applied": False,
        "redaction_count": 0,
        "redaction_reasons": [],
    }
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        redaction = receipt.get("redaction") or receipt.get("redaction_report") or {}
        if isinstance(redaction, Mapping):
            report["redaction_applied"] = bool(redaction.get("applied", False))
            report["redaction_count"] = int(redaction.get("count", 0) or 0)
            report["redaction_reasons"] = list(redaction.get("reasons") or [])
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return destination


def _run_replay(
    run_dir: Path,
    replay_file: Path,
    controller: DiscoverController,
    tools: tuple[Any, ...],
) -> tuple[DiscoverSubmission, AgentReceiptRef, dict[str, Any]]:
    """Execute a deterministic V2 replay fixture through the real tool contracts."""

    payload = json.loads(replay_file.read_text(encoding="utf-8"))
    by_name = {tool.name: tool for tool in tools}
    by_name["read_fcstm_guide"].invoke(
        {"reason": "Replay the mandatory FCSTM guide-first protocol."}
    )
    by_name["read_task"].invoke(
        {"reason": "Replay the immutable task read after the FCSTM guide."}
    )
    if bool(controller.manifest.get("formal_profile", True)):
        by_name["read_fbmcq_guide"].invoke(
            {"reason": "Replay the full-formal guide normalization before planning."}
        )
    plan_call = by_name["register_coverage_plan"].invoke(
        {"plan": payload["coverage_plan"], "reason": payload["plan_reason"]}
    )
    if not plan_call.get("accepted"):
        raise ValueError(f"replay coverage plan rejected: {plan_call}")
    for item in payload["eval_assertions"]:
        result = by_name["eval_assert"].invoke(item)
        if not result.get("accepted", True) and result.get("execution_status") != "completed":
            raise ValueError(f"replay eval assertion rejected: {result}")
    review_gate = controller.require_registry().semantic_review_gate
    if review_gate is None:
        raise ValueError("replay coverage review gate missing")

    def replay_review_runner(kind: str, review_payload: Mapping[str, Any], _attempt: int):
        configured = (payload.get("coverage_review_verdicts") or {}).get(kind)
        if configured:
            return CoverageReviewVerdict.model_validate(configured)
        contract = review_payload["review_contract"]
        return CoverageReviewVerdict(
            review_kind=kind,
            passed=True,
            reviewed_segment_ids=contract["required_segment_ids"],
            reviewed_requirement_ids=contract["required_requirement_ids"],
            reviewed_source_fact_ids=contract["required_source_fact_ids"],
            reviewed_root_ids=contract["required_root_ids"],
            findings=[],
            coverage_analysis=(
                "测试 replay 已逐项覆盖全部冻结义务、行为事实、Root、断言和执行证据；"
                "该结果只验证工作流合同，不具备真实 LLM 学术资格。"
            ),
            rationale="确定性 replay 审查仅用于测试 review gate 与台账指纹合同。",
        )

    review_gate.runner = replay_review_runner
    reviewed = by_name["review_discovery_coverage"].invoke(
        {"reason": "Replay the mandatory current-ledger semantic coverage review."}
    )
    if not reviewed.get("passed"):
        raise ValueError(f"replay coverage review rejected: {reviewed}")
    projection = controller.projection()
    submitted = copy_submission = dict(payload.get("submission") or {})
    if not submitted:
        copy_submission = {
            "submission_type": "submit_discovery",
            "outcome": projection,
            "reason": "Deterministic replay matches the Controller projection.",
        }
    submission = _build_submit_schema(controller).model_validate(copy_submission)
    audit_dir = run_dir / "agent_audit" / "discover"
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit_path = audit_dir / "audit.jsonl"
    result_path = audit_dir / "result.json"
    receipt_path = audit_dir / "receipt.json"
    audit_path.write_text(
        json.dumps({"event": "deterministic_replay", "source": str(replay_file)})
        + "\n",
        encoding="utf-8",
    )
    result_path.write_text(
        json.dumps(submission.model_dump(mode="json"), indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    receipt_path.write_text(
        json.dumps({"real_llm": False, "academic_eligible": False}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    receipt = AgentReceiptRef(
        audit_path=str(audit_path.relative_to(run_dir)),
        result_path=str(result_path.relative_to(run_dir)),
        receipt_path=str(receipt_path.relative_to(run_dir)),
        result_sha256=sha256_file(result_path),
    )
    return submission, receipt, {
        "status": "success",
        "real_llm": False,
        "academic_eligible": False,
        "test_replay": True,
    }


def run_discover(run_dir: Path, registry: LLMRegistry) -> DiscoverCompleted:
    """Run one complete Issue #165 B-discover attempt with one AgentApp.run.

    The deterministic Controller owns input freezing, mechanical segmentation,
    source/FCSTM inventory, registered-coverage gates, direct assertion eval,
    Root projection, append-only records and report rendering.  The single LLM
    Agent owns semantic CoverageUnits, Roots, positive assertion expressions and
    natural-language rationales.  No Repair/Confirm/model mutation occurs.
    """

    case, manifest = load_run_case(run_dir)
    store = RecordStore(run_dir)
    if store.all():
        raise ValueError("run_discover requires a fresh method record prefix")
    store.append(
        "run_started",
        {
            "run_id": manifest["run_id"],
            "case_id": case.case_id,
            "profile": manifest["profile"],
        },
    )
    store.append(
        "input_bridge_completed",
        {
            "model_id": "STM_0",
            "model_sha256": case.fcstm_sha256,
            "source_trace_schema_version": case.source_trace.get("schema_version"),
            "relation_policy": case.source_trace.get("relation_policy"),
            "bridge_attribution": "representation_lowering_not_repair",
        },
    )
    checked = check_fcstm(case.fcstm, "inputs/STM_0.fcstm")
    check_record = store.append("check_fcstm_completed", checked)
    checked = {
        **checked,
        "record_id": check_record["record_id"],
        "record_sha256": check_record["record_sha256"],
    }
    _write_capability_manifest(run_dir, manifest, case, checked)
    if not checked.get("executable"):
        store.append(
            "run_failed",
            {
                "failure_reason": "fcstm_not_executable",
                "check_record_id": check_record["record_id"],
            },
        )
        raise RuntimeError("fcstm_not_executable")

    guide_access = GuideAccessState()
    controller = DiscoverController(
        case, manifest, checked, store, guide_access=guide_access
    )
    frozen = controller.prepare()
    snapshot = controller.task_snapshot()
    validate_reference_blind(snapshot)
    prompt = system_prompt(
        manifest["content_language"],
        formal_profile=bool(manifest.get("formal_profile", True)),
    )
    attempt_id = "discover-attempt-001"
    context_manifest = publish_context(
        store,
        attempt_id=attempt_id,
        system_prompt=prompt,
        snapshot=snapshot,
        content_language=manifest["content_language"],
    )
    attempt_log: list[dict[str, Any]] = []
    review_runner = LLMCoverageReviewRunner(
        llm_registry=registry,
        profile=manifest["profile"],
        audit_root=run_dir / "agent_audit" / "discover" / "coverage_reviews",
        content_language=manifest["content_language"],
        limits=manifest.get("reviewer_limits") or None,
    )
    review_gate = CoverageReviewGate(
        registry=controller.require_registry(),
        task_snapshot=snapshot,
        runner=review_runner,
    )
    controller.require_registry().semantic_review_gate = review_gate
    tools, mandatory_tool_choice = _build_tools(
        controller, snapshot, attempt_log, review_gate
    )
    attempt_record = store.append(
        "agent_attempt_started",
        {
            "attempt_id": attempt_id,
            "context_snapshot_head": context_manifest["context_snapshot_head"],
            "allowed_tools": list(
                _agent_tool_names(
                    formal_profile=bool(manifest.get("formal_profile", True))
                )
            ),
            "required_agent_tool_calls": [
                "read_fcstm_guide",
                "read_task",
                *(
                    ["read_fbmcq_guide"]
                    if bool(manifest.get("formal_profile", True))
                    else []
                ),
                "register_coverage_plan",
                "eval_assert:each_latest_required_assertion",
                "review_discovery_coverage:must_pass_current_ledger",
            ],
            "conditional_agent_tool_calls": {},
            "tool_choice_policy": "paper1-discover-issue165-v1",
        },
    )

    replay_file = manifest.get("test_replay_file")
    if replay_file:
        submission, receipt_ref, result_status = _run_replay(
            run_dir, Path(replay_file), controller, tools
        )
    else:
        audit_dir = run_dir / "agent_audit" / "discover"
        audit_dir.mkdir(parents=True, exist_ok=True)
        audit_path = audit_dir / "audit.jsonl"
        result_path = audit_dir / "result.json"
        spec = AgentSpec(
            name="paper1-b-discover",
            system_prompt=prompt,
            tools=tools,
            output_schema=_build_submit_schema(controller),
            limits=manifest.get("agent_limits") or None,
            require_tool_call=True,
            retry_missing_structured_output=True,
        )
        app = AgentApp.from_registry(
            spec,
            registry,
            profile=manifest["profile"],
            model_options={"streaming": True, "max_retries": 0},
        )
        result = None
        try:
            result = app.run(
                user_prompt(snapshot),
                renderer=manifest["renderer"],
                log_level="INFO",
                audit_out=audit_path,
                result_out=result_path,
                compact_trigger_ratio=0.85,
                tool_choice_resolver=mandatory_tool_choice,
                tool_choice_policy_name="paper1-discover-issue165-v1",
            )
            if result.status != "success" or not result.real_llm:
                raise RuntimeError(
                    f"discover_agent_failed:{result.error or result.status}"
                )
            submission = result.require_output()
            if not isinstance(submission, DiscoverSubmission):
                submission = _build_submit_schema(controller).model_validate(submission)
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
            store.append(
                "run_failed",
                {
                    "failure_reason": "discover_agent_exception",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "attempt_record_id": attempt_record["record_id"],
                    "partial_result": result.to_dict() if result is not None else None,
                },
            )
            raise

    attempt_finished = store.append(
        "agent_attempt_finished",
        {
            "attempt_record_id": attempt_record["record_id"],
            "result": result_status,
            "agent_receipt_ref": receipt_ref.model_dump(mode="json"),
            "tool_attempts": attempt_log,
        },
    )
    _validate_guide_protocol(controller)
    projection = controller.projection()
    if _without_rationale(submission.outcome.model_dump(mode="json")) != _without_rationale(
        projection
    ):
        store.append(
            "run_failed",
            {
                "failure_reason": "discover_submission_projection_mismatch",
                "attempt_record_id": attempt_record["record_id"],
            },
        )
        raise ValueError("discover_submission_projection_mismatch")
    submission_record = store.append(
        "discover_submission_accepted",
        {
            "submission": submission.model_dump(mode="json"),
            "controller_projection": projection,
            "attempt_finished_record_id": attempt_finished["record_id"],
        },
    )
    outcome = DiscoverOutcome.model_validate(projection)
    coverage_plan = _coverage_plan_publication(controller)
    supporting_record_ids = [
        record["record_id"]
        for record in store.all()
        if record["record_type"]
        in {
            "input_segments_created",
            "coverage_requirements_created",
            "source_inventory_created",
            "coverage_plan_registered",
            "assertion_revision_registered",
            "eval_assert_completed",
            "root_projection_completed",
            "discover_submission_accepted",
        }
    ]
    completed_payload = {
        "schema_version": "paper1.discover_completed.v2",
        "run_id": manifest["run_id"],
        "stage": "B-discover",
        "loop_no": 0,
        "model_id": "STM_0",
        "model_sha256": case.fcstm_sha256,
        "input_segments": [
            item.model_dump(mode="json") for item in frozen.input_segments
        ],
        "coverage_requirements": [
            item.model_dump(mode="json")
            for item in frozen.coverage_requirements
        ],
        "source_facts": [item.model_dump(mode="json") for item in frozen.source_facts],
        "coverage_plan": coverage_plan,
        "outcome": outcome.model_dump(mode="json"),
        "agent_real_llm": bool(result_status.get("real_llm", False)),
        "agent_academic_eligible": bool(
            result_status.get("academic_eligible", False)
        ),
        "test_replay": bool(result_status.get("test_replay", False)),
        "main_result_eligible": False,
        "main_result_eligibility_owner": "post_loop_experiment_gate",
        "main_result_eligibility_reason": (
            "B-discover is an intermediate method stage; only the post-loop "
            "experiment gate may admit a complete run into main-result statistics."
        ),
        "agent_receipt_ref": receipt_ref.model_dump(mode="json"),
        "supporting_record_ids": supporting_record_ids,
    }
    completed_record = store.append("discover_completed", completed_payload)
    completed = DiscoverCompleted(
        **completed_payload,
        completed_record_id=completed_record["record_id"],
        completed_record_sha256=completed_record["record_sha256"],
    )
    report = render_discover(
        run_dir, case, completed, store.all(), manifest["content_language"]
    )
    store.append(
        "discover_report_render_completed",
        {
            "report_path": str(report.relative_to(run_dir)),
            "report_sha256": sha256_file(report),
            "discover_completed_record_id": completed_record["record_id"],
            "submission_record_id": submission_record["record_id"],
        },
    )
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
    parser.add_argument(
        "--renderer", choices=("auto", "rich", "jsonl", "quiet"), default="rich"
    )
    parser.add_argument(
        "--formal-profile", action=argparse.BooleanOptionalAction, default=True
    )
    parser.add_argument("--max-model-calls", type=_positive_int)
    parser.add_argument("--max-tool-calls", type=_positive_int)
    parser.add_argument("--max-turns", type=_positive_int)
    parser.add_argument("--max-seconds", type=_positive_finite_float)
    parser.add_argument("--review-max-model-calls", type=_positive_int)
    parser.add_argument("--review-max-turns", type=_positive_int)
    parser.add_argument("--review-max-seconds", type=_positive_finite_float)
    parser.add_argument(
        "--fbmcq-process-wall-seconds", type=_positive_finite_float
    )
    parser.add_argument("--fbmcq-solver-timeout-ms", type=_positive_int)
    parser.add_argument("--fbmcq-max-bound", type=_positive_int)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--replay-file", type=Path, help=argparse.SUPPRESS)
    return parser


def _case_from_args(args: argparse.Namespace) -> PreparedCase:
    if args.pair_id:
        if any(
            value is not None
            for value in (
                args.nl_file,
                args.case_id,
                args.fcstm_file,
                args.raw_source_file,
                args.source_trace_file,
            )
        ):
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
        llm_registry = load_llm_registry(args.config)
        llm_registry.require(args.profile)
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
            reviewer_limits={
                key: value
                for key, value in {
                    "model_calls": args.review_max_model_calls,
                    "turns": args.review_max_turns,
                    "seconds": args.review_max_seconds,
                }.items()
                if value is not None
            },
            fbmcq_limits={
                key: value
                for key, value in {
                    "process_wall_seconds": args.fbmcq_process_wall_seconds,
                    "solver_timeout_ms": args.fbmcq_solver_timeout_ms,
                    "max_bound": args.fbmcq_max_bound,
                }.items()
                if value is not None
            },
        )
        result = run_discover(args.output_dir, llm_registry)
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
