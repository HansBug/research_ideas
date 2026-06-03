"""Deterministic SD-stage façade functions for the PR-1A backbone.

The functions in this module are intentionally LLM-free and do not read
``.env``.  They wrap existing parse/semantic/sim feedback implementations and
pyfcstm ``inspect_model()`` diagnostics behind the PR-0 stage contract so that
later loop wiring can call one canonical deterministic surface.
"""

from __future__ import annotations

import copy
import hashlib
import re
from dataclasses import asdict
from typing import Any, Iterable, Literal

from method.feedback.parse import check_parse
from method.feedback.semantic import check_semantic
from method.feedback.sim import check_sim
from method.schema import (
    BudgetState,
    DesignDiagnosticItem,
    DesignFeedback,
    FeedbackBundle,
    FixPlan,
    GroundedElement,
    GroundingMap,
    ModelReviewFeedback,
    ParseFeedback,
    RepairRejection,
    RepairReviewFeedback,
    RevisedFixPlan,
    ScenarioSet,
    ScenarioStep,
    SemanticFeedback,
    SimFeedback,
    StageContext,
    StageResultMeta,
    TestScenario,
)
from method.stages.ids import FEEDBACK_SOURCE_TO_STAGE_ID, STAGE_SPECS_BY_ID, StageId, StageStatus
from method.stages.sd_context import BuildResult, build_model_from_dsl, update_context_with_build

DesignPolicyProfile = Literal["experiment_default", "generated_candidate", "signed_ref_model", "path_smoke", "audit_only"]

_HIGH_RISK_WARNING_CODES = {
    "W_UNREACHABLE_STATE",
    "W_DEADLOCK_LEAF",
    "W_UNWRITTEN_READ_VAR",
    "W_GUARD_CONST_FALSE",
    "W_FORCED_NEVER_EXPANDS",
    "W_INITIAL_UNCONDITIONAL_MISSING",
    "W_GUARD_VARS_NEVER_CHANGE",
}

_ADVISORY_WARNING_CODES = {
    "W_UNUSED_EVENT",
    "W_WRITE_ONLY_VAR",
    "W_UNREFERENCED_VAR",
    "W_HIGH_VAR_TO_LEAF_RATIO",
    "W_DEEP_HIERARCHY",
    "W_LARGE_COMPOSITE",
    "W_REDUNDANT_TRANSITION",
    "W_SELF_TRANSITION_NOP",
    "W_EFFECT_SELF_ASSIGN",
    "W_GUARD_CONST_TRUE",
    "W_DURING_CONST_ASSIGN",
}
DEFAULT_WARNING_REPAIR_BUDGET = 2
COUNT_DRIFT_THRESHOLD = 0.30

_EXTERNAL_INPUT_DECLARATION_PATTERNS = (
    re.compile(
        r"\b(?:reads?|measures?|observes?|monitors?|samples?)\b"
        r"(?P<segment>[^.;:\n]{0,180})",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:external|environment(?:al)?|sensor|input|measured|observed|monitored)\s+"
        r"(?:variables?|values?|signals?|inputs?|parameters?|readings?)\b"
        r"(?P<segment>[^.;:\n]{0,180})",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?P<segment>[^.;:\n]{0,180})"
        r"\b(?:as|from)\s+"
        r"(?:external|environment(?:al)?|sensor|input)\s+"
        r"(?:variables?|values?|signals?|inputs?|parameters?|readings?)\b",
        re.IGNORECASE,
    ),
)
_NL_IDENTIFIER_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
_EXTERNAL_INPUT_SEGMENT_STOP_RE = re.compile(
    r"\b(?:before|after|when|while|where|then|otherwise|until|unless|because|so\s+that)\b",
    re.IGNORECASE,
)


def _trim_external_input_segment(segment: str) -> str:
    """Keep only the declaration phrase, not subsequent control-flow prose.

    PR-E1 uses this detector only as a conservative deterministic hint for
    NL-declared read-only environment inputs.  A phrase such as
    ``reads temperature T before selecting the next mode`` should ground ``T``
    but must not accidentally classify a declared variable named ``mode`` as an
    external input merely because it appears after the temporal connector
    ``before``.  Explicit declarations before the connector, including
    ``reads mode as an external input before ...``, remain detectable.
    """

    match = _EXTERNAL_INPUT_SEGMENT_STOP_RE.search(segment)
    if not match:
        return segment
    return segment[: match.start()]


def _external_input_variables_from_nl(nl: str) -> set[str]:
    """Infer explicitly declared read-only environment variables from NL text.

    The detector is deliberately *sample-agnostic*: it only uses generic
    linguistic declarations such as "reads ...", "sensor variables ...", or
    "... as external inputs".  It must not contain benchmark-domain lexicons,
    case IDs, or acronym aliases by hand.  Ambiguous cases stay blocking so
    SL-9 can reason about external-vs-internal variable intent from the full
    prompt instead of the deterministic loop overfitting to known samples.
    """

    if not nl:
        return set()
    found: set[str] = set()
    for pattern in _EXTERNAL_INPUT_DECLARATION_PATTERNS:
        for match in pattern.finditer(nl):
            segment = _trim_external_input_segment(match.group("segment"))
            for token_match in _NL_IDENTIFIER_RE.finditer(segment):
                token = token_match.group(0)
                if len(token) <= 40:
                    found.add(token)
    return found


def _guard_vars(item: DesignDiagnosticItem) -> set[str]:
    raw = item.refs.get("guard_vars")
    if isinstance(raw, list):
        return {str(v) for v in raw}
    return set()


def _external_input_advisory_rationale(item: DesignDiagnosticItem, nl_external_vars: set[str]) -> str | None:
    if item.code == "W_UNWRITTEN_READ_VAR":
        var = str(item.refs.get("var_name") or "")
        if var and var in nl_external_vars:
            return (
                f"Downgraded because `{var}` is NL-grounded as an external "
                "sensor/environment input; adding invented writes would be "
                "less faithful than leaving it read-only."
            )
    if item.code == "W_GUARD_VARS_NEVER_CHANGE":
        vars_in_guard = _guard_vars(item)
        if vars_in_guard and vars_in_guard.issubset(nl_external_vars):
            return (
                "Downgraded because all guard variables are NL-grounded "
                f"external inputs: {', '.join(sorted(vars_in_guard))}."
            )
    return None


def _hash_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _stage_meta(stage_id: StageId | str, *, ok: bool, status: StageStatus | str | None = None, stage_error: str | None = None) -> StageResultMeta:
    sid = stage_id.value if isinstance(stage_id, StageId) else stage_id
    spec = STAGE_SPECS_BY_ID[sid]
    resolved = status or (StageStatus.OK if ok else StageStatus.FAIL)
    return StageResultMeta(
        stage_id=sid,
        stage_kind=spec.kind,
        enabled=True,
        ran=True,
        status=resolved,
        ok=ok,
        stage_error=stage_error,
    )


def _attach_meta(context: StageContext | None, feedback: Any, meta: StageResultMeta) -> StageResultMeta:
    if hasattr(feedback, "meta"):
        feedback.meta = meta
    if context is not None:
        context.stage_results.append(meta)
    return meta


def _span_to_dict(span: Any) -> dict[str, Any] | None:
    if span is None:
        return None
    return {
        "line": getattr(span, "line", None),
        "column": getattr(span, "column", None),
        "end_line": getattr(span, "end_line", None),
        "end_column": getattr(span, "end_column", None),
    }


def _normalize_ref(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if hasattr(value, "line") and hasattr(value, "column"):
        return _span_to_dict(value)
    if isinstance(value, dict):
        return {str(k): _normalize_ref(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_normalize_ref(v) for v in value]
    return str(value)


def _diag_to_dict(diag: Any) -> dict[str, Any]:
    if isinstance(diag, dict):
        return copy.deepcopy(diag)
    return {
        "code": getattr(diag, "code", None),
        "severity": getattr(diag, "severity", None),
        "message": getattr(diag, "message", ""),
        "span": _span_to_dict(getattr(diag, "span", None)),
        "refs": _normalize_ref(dict(getattr(diag, "refs", {}) or {})),
    }


def _diagnostic_instance_key(diag: dict[str, Any]) -> str:
    code = str(diag.get("code") or "UNKNOWN")
    refs = diag.get("refs") or {}
    preferred_keys = (
        "state_path",
        "from_path",
        "to_path",
        "var_name",
        "event_ref",
        "transition_id",
        "transition_span",
        "reason",
    )
    parts = [f"{key}={refs[key]}" for key in preferred_keys if key in refs and refs[key] is not None]
    if parts:
        return f"{code}:" + ":".join(parts)
    return f"{code}:" + hashlib.sha256(repr(sorted(refs.items())).encode("utf-8")).hexdigest()[:12]


def _extract_suggested_fix_hints(diag: dict[str, Any]) -> list[dict[str, Any]]:
    hints: list[dict[str, Any]] = []
    refs = diag.get("refs") or {}
    for payload in (diag.get("suggested_fix"), refs.get("suggested_fix")):
        if isinstance(payload, dict):
            hints.append(copy.deepcopy(payload))
    code = diag.get("code")
    try:
        from pyfcstm.diagnostics.codes import CODE_REGISTRY

        spec = CODE_REGISTRY.get(code)
        if spec is not None:
            if spec.suggested_fix is not None:
                hints.append(asdict(spec.suggested_fix))
            if spec.for_llm is not None:
                hints.append(
                    {
                        "kind": "for_llm_guidance",
                        "summary": spec.for_llm.summary,
                        "recommended_actions": [dict(item) for item in spec.for_llm.recommended_actions],
                        "do_not": list(spec.for_llm.do_not),
                    }
                )
    except Exception:
        pass
    return hints


def _budget_state_for(diag: dict[str, Any], warning_budget_state: dict[str, BudgetState]) -> BudgetState:
    key = _diagnostic_instance_key(diag)
    if key not in warning_budget_state:
        warning_budget_state[key] = BudgetState(
            instance_key=key,
            diagnostic_code=str(diag.get("code") or "UNKNOWN"),
            repair_count=0,
            budget_remaining=DEFAULT_WARNING_REPAIR_BUDGET,
            budget_exhausted=False,
            last_status="new",
            last_stage=StageId.SD_4_DESIGN.value,
        )
    return warning_budget_state[key]



def mark_warning_repair_attempt(
    warning_budget_state: dict[str, BudgetState],
    instance_keys: Iterable[str],
    *,
    last_status: str = "repair_attempted",
    last_stage: str = StageId.SL_9_REPAIR.value,
) -> dict[str, BudgetState]:
    """Decrement per-instance warning repair budgets after an SL-9 attempt.

    PR-1A only provides the deterministic state transition; later loop wiring
    decides exactly when to call it. Missing keys are ignored so stale review
    evidence cannot create phantom budget entries.
    """
    for key in instance_keys:
        state = warning_budget_state.get(key)
        if state is None or state.budget_exhausted:
            continue
        state.repair_count += 1
        state.budget_remaining = max(0, state.budget_remaining - 1)
        state.budget_exhausted = state.budget_remaining == 0
        state.last_status = last_status
        state.last_stage = last_stage
    return warning_budget_state


def _design_policy_action(
    diag: dict[str, Any],
    state: BudgetState,
    *,
    policy_profile: DesignPolicyProfile = "generated_candidate",
) -> str:
    severity = diag.get("severity")
    code = str(diag.get("code") or "")
    if severity == "error" or code.startswith("E_"):
        return "hard_block"
    if severity == "info" or code.startswith("I_"):
        return "info"
    if not code.startswith("W_"):
        return "requires_policy_classification"
    if policy_profile in {"path_smoke", "audit_only"}:
        return "advisory"
    if code in _ADVISORY_WARNING_CODES:
        return "advisory"
    if code not in _HIGH_RISK_WARNING_CODES:
        return "requires_policy_classification"
    if state.budget_exhausted or state.budget_remaining <= 0:
        return "advisory"
    return "budgeted_repair"


def _design_item_from_diag(
    diag: dict[str, Any],
    state: BudgetState | None = None,
    *,
    policy_profile: DesignPolicyProfile = "generated_candidate",
) -> DesignDiagnosticItem:
    if state is None:
        state = BudgetState(
            instance_key=_diagnostic_instance_key(diag),
            diagnostic_code=str(diag.get("code") or "UNKNOWN"),
        )
    action = _design_policy_action(diag, state, policy_profile=policy_profile)
    return DesignDiagnosticItem(
        code=str(diag.get("code") or "UNKNOWN"),
        pyfcstm_severity=str(diag.get("severity") or "warning"),
        policy_action=action,
        instance_key=state.instance_key,
        refs=copy.deepcopy(diag.get("refs") or {}),
        message=str(diag.get("message") or ""),
        suggested_fix_hints=_extract_suggested_fix_hints(diag),
        budget_remaining=state.budget_remaining,
        budget_exhausted=state.budget_exhausted,
    )


def run_sd2_parse(current_dsl: str, context: StageContext | None = None) -> tuple[ParseFeedback, StageResultMeta]:
    feedback = check_parse(current_dsl)
    meta = _stage_meta(StageId.SD_2_PARSE, ok=feedback.ok)
    _attach_meta(context, feedback, meta)
    return feedback, meta


def run_sd3_semantic(parse_ok_dsl: str, context: StageContext | None = None) -> tuple[SemanticFeedback, StageResultMeta, BuildResult]:
    feedback = check_semantic(parse_ok_dsl)
    build = update_context_with_build(context or StageContext(), parse_ok_dsl)
    if context is not None:
        context.current_dsl = parse_ok_dsl
        context.ast = build.ast
        context.model = build.model
    meta = _stage_meta(StageId.SD_3_SEMANTIC, ok=feedback.ok)
    _attach_meta(context, feedback, meta)
    return feedback, meta, build


def run_sd4_design(
    context: StageContext,
    *,
    policy_profile: DesignPolicyProfile = "generated_candidate",
    warning_budget_state: dict[str, BudgetState] | None = None,
) -> tuple[DesignFeedback, StageResultMeta]:
    if warning_budget_state is None:
        warning_budget_state = context.warning_budget_state
    if context.model is None:
        feedback = DesignFeedback(ok=False, policy_profile=policy_profile, inspect_summary={"stage_error": "StageContext.model is missing"})
        meta = _stage_meta(StageId.SD_4_DESIGN, ok=False, status=StageStatus.ERROR, stage_error="StageContext.model is missing")
        _attach_meta(context, feedback, meta)
        return feedback, meta

    from pyfcstm.diagnostics import inspect_model

    inspect_json = inspect_model(context.model).to_json()
    context.inspect_json = inspect_json
    diagnostics = [_diag_to_dict(diag) for diag in inspect_json.get("diagnostics", [])]
    declared_vars = set(str(name) for name in (getattr(context.model, "defines", {}) or {}).keys())
    nl_external_vars = _external_input_variables_from_nl(context.nl) & declared_vars
    blocking: list[DesignDiagnosticItem] = []
    advisory: list[DesignDiagnosticItem] = []
    info: list[DesignDiagnosticItem] = []

    for diag in diagnostics:
        state = _budget_state_for(diag, warning_budget_state)
        item = _design_item_from_diag(diag, state, policy_profile=policy_profile)
        external_rationale = _external_input_advisory_rationale(item, nl_external_vars)
        if external_rationale is not None and item.policy_action == "budgeted_repair":
            item.policy_action = "advisory"
            item.rationale = external_rationale
            state.last_status = "external_input_advisory"
        elif external_rationale is not None:
            item.rationale = external_rationale
        state.last_status = item.policy_action
        state.last_stage = StageId.SD_4_DESIGN.value
        if item.policy_action in {"hard_block", "budgeted_repair", "requires_policy_classification"}:
            blocking.append(item)
        elif item.policy_action == "info":
            info.append(item)
        else:
            advisory.append(item)

    feedback = DesignFeedback(
        ok=not blocking,
        blocking_items=blocking,
        advisory_items=advisory,
        info_items=info,
        policy_profile=policy_profile,
        inspect_summary={
            "policy_profile": policy_profile,
            "n_errors": sum(1 for d in diagnostics if d.get("severity") == "error"),
            "n_warnings": sum(1 for d in diagnostics if d.get("severity") == "warning"),
            "n_infos": sum(1 for d in diagnostics if d.get("severity") == "info"),
            "diagnostic_codes": [d.get("code") for d in diagnostics],
            "blocking_instance_keys": [item.instance_key for item in blocking],
            "advisory_instance_keys": [item.instance_key for item in advisory],
            "info_instance_keys": [item.instance_key for item in info],
            "prompt_ready_summary": [
                {
                    "code": item.code,
                    "action": item.policy_action,
                    "instance_key": item.instance_key,
                    "message": item.message,
                    "refs": item.refs,
                    "budget_remaining": item.budget_remaining,
                }
                for item in [*blocking, *advisory, *info]
            ],
            "warning_budget_state": {key: asdict(value) for key, value in sorted(warning_budget_state.items())},
            "nl_external_input_vars": sorted(nl_external_vars),
        },
    )
    status = StageStatus.OK if feedback.ok else StageStatus.FAIL
    meta = _stage_meta(StageId.SD_4_DESIGN, ok=feedback.ok, status=status)
    _attach_meta(context, feedback, meta)
    return feedback, meta


def run_sd5a_scenario_coverage(current_dsl: str, scenarios: Iterable[Any]) -> tuple[dict[str, Any], StageResultMeta]:
    from method.scenariogen_validate import coverage_directive, validate_coverage

    scenario_list = list(scenarios or [])
    coverage_report = validate_coverage(current_dsl, scenario_list)
    directive = coverage_directive(coverage_report)
    output = {
        "coverage_report": coverage_report,
        "retry_directive": directive,
        "coverage_gap": directive is not None,
    }
    meta = _stage_meta(StageId.SD_5A_SCENARIO_COVERAGE, ok=directive is None, status=StageStatus.OK if directive is None else StageStatus.ADVISORY)
    return output, meta


def freeze_scenario_set(
    scenarios: Iterable[Any],
    *,
    source_dsl_hash: str,
    source_inspect_hash: str = "",
    source_grounding_hash: str | None = None,
    coverage_report: dict[str, Any] | None = None,
    epoch: int = 0,
    scenario_set_id: str | None = None,
) -> tuple[ScenarioSet, StageResultMeta]:
    scenario_list = list(scenarios or [])
    if scenario_set_id is None:
        scenario_set_id = "scenario-set-" + hashlib.sha256(repr([getattr(s, "name", str(s)) for s in scenario_list]).encode("utf-8")).hexdigest()[:12]
    scenario_set = ScenarioSet(
        scenario_set_id=scenario_set_id,
        scenarios=scenario_list,
        source_dsl_hash=source_dsl_hash,
        source_inspect_hash=source_inspect_hash,
        source_grounding_hash=source_grounding_hash,
        coverage_report=coverage_report or {},
        epoch=epoch,
        frozen=True,
    )
    meta = _stage_meta(StageId.SC_5F_SCENARIO_FREEZE, ok=True)
    return scenario_set, meta


_NORMALIZED_HOT_START_MARKER = "[PR-E1/default-normalized:"
_ORIGINAL_INITIAL_STATE_RE = re.compile(r"original_initial_state=([^;\]]+)")


def _normalized_original_initial_state(description: str | None) -> str | None:
    if not description or _NORMALIZED_HOT_START_MARKER not in description:
        return None
    match = _ORIGINAL_INITIAL_STATE_RE.search(description)
    if not match:
        return None
    value = match.group(1).strip()
    return value or None


def _same_state_path(left: str | None, right: str | None) -> bool:
    if not left or not right:
        return False
    a = left.strip()
    b = right.strip()
    return a == b or a.endswith(f".{b}") or b.endswith(f".{a}")


def _default_runtime_state(current_dsl: str) -> str | None:
    probe = TestScenario(
        name="__pr_e1_default_init_probe__",
        steps=[ScenarioStep(events=[], name="default_initial_dispatch_probe")],
    )
    feedback = check_sim(current_dsl, [probe])
    if not feedback.scenario_results:
        return None
    result = feedback.scenario_results[0]
    if not result.step_results:
        return None
    return result.step_results[0].actual_state or None


def _weak_normalized_hot_start_failures(current_dsl: str, scenario_set: ScenarioSet, feedback: SimFeedback) -> dict[str, Any] | None:
    """Return weak-oracle evidence only when every failure is truly hot-start-only.

    PR-E1 clears SL-5 hot-start ``initial_state`` before running scenarios on
    the default path.  The marker attached by ``_normalize_scenarios_for_runtime``
    is only provenance: it does **not** by itself prove a weak oracle.  A
    normalized failure is weak only when its original hot-start state differs
    from the model's default runtime state.  If the original state is the same
    as the default state, the failure is reproducible from default init and must
    remain ordinary SD-6 blocking feedback so the repair loop can see it.
    """

    default_state = _default_runtime_state(current_dsl)
    weak: list[dict[str, str | None]] = []
    real_or_unknown: list[dict[str, str | None]] = []
    scenarios = list(scenario_set.scenarios)
    for scenario, result in zip(scenarios, feedback.scenario_results):
        if result.status == "pass":
            continue
        original_state = _normalized_original_initial_state(getattr(scenario, "description", ""))
        if default_state is None:
            real_or_unknown.append({"scenario_name": result.name, "reason": "default_state_probe_failed", "original_initial_state": original_state, "default_state": default_state})
        elif original_state is None:
            real_or_unknown.append({"scenario_name": result.name, "reason": "no_normalized_hot_start_provenance", "default_state": default_state})
        elif _same_state_path(original_state, default_state):
            real_or_unknown.append(
                {
                    "scenario_name": result.name,
                    "reason": "failure_reproducible_from_default_initial_state",
                    "original_initial_state": original_state,
                    "default_state": default_state,
                }
            )
        else:
            weak.append(
                {
                    "scenario_name": result.name,
                    "reason": "original_hot_start_state_not_default_reachable_without_prefix",
                    "original_initial_state": original_state,
                    "default_state": default_state,
                }
            )
    if weak and not real_or_unknown:
        return {
            "scenario_names": [item["scenario_name"] for item in weak],
            "default_state": default_state,
            "weak_failures": weak,
            "policy": (
                "Default main path clears SL-5 hot-start initial_state. "
                "Only failures whose original hot-start state differs from the default runtime state "
                "are treated as weak oracle evidence; default-state failures remain repairable SD-6 feedback."
            ),
        }
    return None


def run_sd6_sim(current_dsl: str, scenario_set: ScenarioSet | None, context: StageContext | None = None) -> tuple[SimFeedback, StageResultMeta]:
    if scenario_set is None:
        feedback = SimFeedback(ok=False, setup_error="ScenarioSet is missing")
        meta = _stage_meta(StageId.SD_6_SIM, ok=False, status=StageStatus.ERROR, stage_error="ScenarioSet is missing")
        _attach_meta(context, feedback, meta)
        return feedback, meta
    feedback = check_sim(current_dsl, list(scenario_set.scenarios))
    if not feedback.ok:
        weak_evidence = _weak_normalized_hot_start_failures(current_dsl, scenario_set, feedback)
        if weak_evidence is not None:
            feedback.oracle_weak = True
            feedback.weak_oracle_reason = "normalized_hot_start_scenario_failed"
            feedback.weak_oracle_evidence = weak_evidence
    meta = _stage_meta(StageId.SD_6_SIM, ok=feedback.ok)
    _attach_meta(context, feedback, meta)
    return feedback, meta


def _as_evidence(item: Any) -> dict[str, Any]:
    if hasattr(item, "__dataclass_fields__"):
        return asdict(item)
    if isinstance(item, dict):
        return copy.deepcopy(item)
    return {"value": str(item)}


def _grounding_hints(grounding_map: GroundingMap | None) -> tuple[list[str], list[str]]:
    if grounding_map is None:
        return [], []
    target_ids = [e.element_id for e in grounding_map.elements]
    required = [e.element_id for e in grounding_map.elements if e.requiredness == "required"]
    return target_ids, required


def run_sd8_fix_plan(
    selected_feedback: Any,
    *,
    source: str,
    source_stage: str | None = None,
    grounding_map: GroundingMap | None = None,
    before_dsl: str = "",
    rejection: RepairRejection | None = None,
    original: FixPlan | None = None,
) -> tuple[FixPlan | RevisedFixPlan, StageResultMeta]:
    if rejection is not None and original is not None:
        revised = RevisedFixPlan(original=original, rejection=rejection, revision_count=1)
        return revised, _stage_meta(StageId.SD_8_FIX_PLAN, ok=True)

    target = source if source in {"parse", "semantic", "design", "sim", "model_review"} else "design"
    severity = "error"
    evidence: list[dict[str, Any]] = []
    diagnostic_ids: list[str] = []
    suggested_fix_hints: list[dict[str, Any]] = []
    summary = ""

    if isinstance(selected_feedback, ParseFeedback):
        severity = "error"
        evidence = selected_feedback.diagnostics or [_as_evidence(selected_feedback)]
        diagnostic_ids = [str(d.get("code", "parse")) for d in selected_feedback.diagnostics]
        summary = selected_feedback.error_message or "parse failed"
    elif isinstance(selected_feedback, SemanticFeedback):
        severity = "error"
        evidence = selected_feedback.diagnostics or [_as_evidence(selected_feedback)]
        diagnostic_ids = [str(d.get("code", "semantic")) for d in selected_feedback.diagnostics]
        summary = selected_feedback.error_message or "semantic failed"
    elif isinstance(selected_feedback, DesignFeedback):
        items = selected_feedback.blocking_items or selected_feedback.advisory_items or selected_feedback.info_items
        evidence = [asdict(item) for item in items]
        diagnostic_ids = [item.instance_key for item in items]
        suggested_fix_hints = [hint for item in items for hint in item.suggested_fix_hints]
        severity = "blocking_warning" if selected_feedback.blocking_items else "advisory_warning"
        summary = "; ".join(item.message or item.code for item in items[:3]) or "design feedback selected"
    elif isinstance(selected_feedback, SimFeedback):
        severity = "sim_fail"
        evidence = [asdict(sr) for sr in selected_feedback.scenario_results if sr.status != "pass"]
        diagnostic_ids = [sr.name for sr in selected_feedback.scenario_results if sr.status != "pass"]
        summary = selected_feedback.setup_error or "simulation failed"
    elif isinstance(selected_feedback, ModelReviewFeedback):
        severity = "review_fail"
        evidence = selected_feedback.blocking_findings or selected_feedback.findings
        diagnostic_ids = [str(item.get("id") or item.get("code") or i) for i, item in enumerate(evidence)]
        summary = "model review failed"

    target_ids, required_ids = _grounding_hints(grounding_map)
    plan = FixPlan(
        target=target,
        source_stage=source_stage or FEEDBACK_SOURCE_TO_STAGE_ID.get(source, StageId.SD_8_FIX_PLAN.value),
        source_feedback_id=diagnostic_ids[0] if diagnostic_ids else f"{target}:feedback",
        severity=severity,
        diagnostic_ids=diagnostic_ids,
        problem_summary=summary,
        evidence=evidence,
        suggested_fix_hints=suggested_fix_hints,
        recommended_strategy=[
            "Use diagnostics as hints; choose the smallest globally consistent repair.",
            "Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.",
        ],
        forbidden_edits=[
            "Do not delete grounded required elements merely to silence diagnostics.",
            "Do not invent internal plant/environment dynamics merely to make external input variables appear written.",
        ],
        target_element_ids=target_ids,
        required_preserve_element_ids=required_ids,
        before_dsl_hash=_hash_text(before_dsl) if before_dsl else "",
    )
    return plan, _stage_meta(StageId.SD_8_FIX_PLAN, ok=True)


def _strip_line_comments(dsl_text: str) -> str:
    return re.sub(r"//.*", "", dsl_text)


def _identifier_token_present(text: str, token: str) -> bool:
    if not token:
        return False
    return re.search(rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])", text) is not None


def _ref_leaf(value: str) -> str:
    parts = [part for part in re.split(r"[.:/\s>\-]+", value) if part]
    return parts[-1] if parts else value


def _grounded_token_missing(candidate_dsl: str, element: GroundedElement) -> bool:
    """Fallback textual required-element check with token boundaries.

    SD-10 prefers typed checks against the parsed pyfcstm model.  This fallback
    is used only when no candidate model is available, and therefore avoids raw
    substring matching and strips line comments first.
    """
    full_ref = (element.element_ref or "").strip()
    if not full_ref:
        return False
    text = _strip_line_comments(candidate_dsl)
    if "." in full_ref and full_ref in text:
        return False
    leaf = _ref_leaf(full_ref)
    return bool(leaf) and not _identifier_token_present(text, leaf)


def _path_str(value: Any) -> str:
    if value is None:
        return ""
    path = getattr(value, "path", None)
    if isinstance(path, (tuple, list)):
        return ".".join(str(part) for part in path)
    name = getattr(value, "name", None)
    return str(name) if name is not None else str(value)


def _iter_model_states(model: Any) -> list[Any]:
    root = getattr(model, "root_state", None)
    if root is None:
        return []
    try:
        return list(root.walk_states())
    except Exception:
        states = [root]
        for child in getattr(root, "substates", {}).values():
            states.extend(_iter_model_states(type("M", (), {"root_state": child})()))
        return states


def _event_ref_str(event: Any) -> str:
    if event is None:
        return ""
    name = getattr(event, "name", None)
    state_path = getattr(event, "state_path", None)
    if name is not None and isinstance(state_path, (tuple, list)) and state_path:
        return ".".join([*(str(part) for part in state_path), str(name)])
    return _path_str(event)


def _transition_endpoint(owner_state: str, endpoint: Any) -> str:
    raw = _path_str(endpoint)
    if not raw or raw in {"INIT_STATE", "EXIT_STATE", "[*]"} or raw.startswith("Root."):
        return raw
    if owner_state and "." not in raw:
        return f"{owner_state}.{raw}"
    return raw


def _component_index(model: Any) -> dict[str, set[str]]:
    states = _iter_model_states(model)
    index: dict[str, set[str]] = {
        "state_paths": set(),
        "state_names": set(),
        "event_refs": set(),
        "event_names": set(),
        "variable_names": set(),
        "transition_refs": set(),
        "guard_refs": set(),
        "action_refs": set(),
    }
    for state in states:
        state_path = _path_str(state)
        if state_path:
            index["state_paths"].add(state_path)
            index["state_names"].add(_ref_leaf(state_path))
        for event_name in getattr(state, "events", {}) or {}:
            event_ref = f"{state_path}.{event_name}" if state_path else str(event_name)
            index["event_refs"].add(event_ref)
            index["event_names"].add(str(event_name))
        for transition in getattr(state, "transitions", []) or []:
            from_ref = _transition_endpoint(state_path, getattr(transition, "from_state", None))
            to_ref = _transition_endpoint(state_path, getattr(transition, "to_state", None))
            event_ref = _event_ref_str(getattr(transition, "event", None))
            event_leaf = _ref_leaf(event_ref) if event_ref else ""
            if event_ref:
                index["event_refs"].add(event_ref)
                index["event_names"].add(event_leaf)
            base = f"{from_ref}->{to_ref}"
            index["transition_refs"].add(base)
            if event_ref:
                index["transition_refs"].add(f"{base}::{event_ref}")
            if event_leaf and event_leaf != event_ref:
                index["transition_refs"].add(f"{base}::{event_leaf}")
            guard = getattr(transition, "guard", None)
            if guard is not None:
                index["guard_refs"].add(str(guard))
            for effect in getattr(transition, "effects", []) or []:
                index["action_refs"].add(str(effect))
    defines = getattr(model, "defines", {}) or {}
    index["variable_names"].update(str(name) for name in defines.keys())
    return index


def _element_ref_for_matching(element: GroundedElement) -> str:
    ref = (element.element_ref or "").strip()
    element_id = (element.element_id or "").strip()
    if "." not in ref and ":" in element_id:
        _, id_ref = element_id.split(":", 1)
        id_ref = id_ref.strip()
        if "." in id_ref:
            return id_ref
    return ref


def _grounded_element_present(index: dict[str, set[str]], element: GroundedElement) -> bool:
    ref = _element_ref_for_matching(element)
    if not ref:
        return True
    leaf = _ref_leaf(ref)
    kind = element.element_kind
    if kind in {"state", "hierarchical_state"}:
        if "." in ref:
            return ref in index["state_paths"]
        return leaf in index["state_names"]
    if kind == "event":
        if "." in ref:
            return ref in index["event_refs"]
        return leaf in index["event_names"]
    if kind == "variable":
        return ref in index["variable_names"] or leaf in index["variable_names"]
    if kind == "transition":
        normalized_ref = re.sub(r"\s+", "", ref)
        return any(re.sub(r"\s+", "", item) == normalized_ref for item in index["transition_refs"])
    if kind == "guard":
        return any(ref == item or leaf == _ref_leaf(item) for item in index["guard_refs"])
    if kind == "action":
        return any(ref == item or leaf == _ref_leaf(item) for item in index["action_refs"])
    return False


def _grounded_element_missing(candidate_dsl: str, element: GroundedElement, candidate_model: Any | None) -> bool:
    if candidate_model is not None:
        return not _grounded_element_present(_component_index(candidate_model), element)
    return _grounded_token_missing(candidate_dsl, element)


def _model_summary(model: Any) -> dict[str, Any]:
    states = _iter_model_states(model)
    index = _component_index(model)
    transitions: list[dict[str, Any]] = []
    n_forced = 0
    n_transition_effects = 0
    for state in states:
        state_path = _path_str(state)
        for transition in getattr(state, "transitions", []) or []:
            effects = list(getattr(transition, "effects", []) or [])
            is_forced = bool(getattr(transition, "is_forced", False))
            n_forced += int(is_forced)
            n_transition_effects += len(effects)
            transitions.append(
                {
                    "owner_state": state_path,
                    "from": _transition_endpoint(state_path, getattr(transition, "from_state", None)),
                    "to": _transition_endpoint(state_path, getattr(transition, "to_state", None)),
                    "event": _event_ref_str(getattr(transition, "event", None)),
                    "has_guard": getattr(transition, "guard", None) is not None,
                    "n_effects": len(effects),
                    "is_forced": is_forced,
                }
            )
    return {
        "n_states": len(index["state_paths"]),
        "state_paths": sorted(index["state_paths"]),
        "n_events": len(index["event_names"]),
        "event_refs": sorted(index["event_refs"]),
        "n_variables": len(index["variable_names"]),
        "variable_names": sorted(index["variable_names"]),
        "n_transitions": len(transitions),
        "transitions": transitions,
        "n_forced_transitions": n_forced,
        "n_transition_effects": n_transition_effects,
    }


def _count_drift_evidence(old_summary: dict[str, Any], new_summary: dict[str, Any], fix_plan: FixPlan) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    count_fields = ("n_states", "n_events", "n_variables", "n_transitions")
    for field in count_fields:
        old_value = int(old_summary.get(field) or 0)
        new_value = int(new_summary.get(field) or 0)
        if old_value <= 0:
            continue
        drift = (new_value - old_value) / old_value
        if abs(drift) > COUNT_DRIFT_THRESHOLD:
            item = {
                "kind": "count_drift",
                "field": field,
                "old": old_value,
                "new": new_value,
                "drift_ratio": round(drift, 4),
                "direction": "increase" if drift > 0 else "decrease",
                "fix_target": fix_plan.target,
            }
            if drift < 0:
                item["reduction_ratio"] = round(abs(drift), 4)
            evidence.append(item)
    old_forced = int(old_summary.get("n_forced_transitions") or 0)
    new_forced = int(new_summary.get("n_forced_transitions") or 0)
    if old_forced != new_forced:
        evidence.append(
            {
                "kind": "forced_transition_count_drift",
                "old": old_forced,
                "new": new_forced,
                "fix_target": fix_plan.target,
            }
        )
    return evidence


def _remaining_design_targets(feedback: DesignFeedback, fix_plan: FixPlan) -> list[DesignDiagnosticItem]:
    target_ids = set(fix_plan.diagnostic_ids or [])
    if fix_plan.source_feedback_id:
        target_ids.add(fix_plan.source_feedback_id)
    if not target_ids:
        return []
    remaining: list[DesignDiagnosticItem] = []
    for item in [*feedback.blocking_items, *feedback.advisory_items, *feedback.info_items]:
        if item.instance_key in target_ids or item.code in target_ids:
            remaining.append(item)
    return remaining


def _design_feedback_for_review_baseline(nl: str, dsl_text: str) -> DesignFeedback | None:
    """Return SD-4 feedback for a comparable repair-review baseline if possible.

    Old DSL can be syntactically or semantically invalid for parse/semantic
    repairs. In that case there is no reliable pre-repair design baseline, so
    callers should conservatively treat candidate blocking diagnostics as
    newly introduced.
    """
    context = StageContext(nl=nl, current_dsl=dsl_text)
    parse_feedback, _ = run_sd2_parse(dsl_text, context)
    if not parse_feedback.ok:
        return None
    semantic_feedback, _, _ = run_sd3_semantic(dsl_text, context)
    if not semantic_feedback.ok:
        return None
    design_feedback, _ = run_sd4_design(context)
    return design_feedback


def run_sd10_repair_review(
    *,
    nl: str,
    grounding_map: GroundingMap | None,
    old_dsl: str,
    candidate_dsl: str,
    fix_plan: FixPlan,
    scenario_set: ScenarioSet | None = None,
) -> tuple[RepairReviewFeedback, StageResultMeta]:
    """Review a repair candidate with local deterministic gates.

    ``scenario_set=None`` means this SD-10 call does not have a frozen scenario
    oracle available, so scenario-level regression is skipped while parse,
    semantic, design-health, count-drift, forced-transition, and grounding
    checks still run.
    """
    evidence: list[dict[str, Any]] = []
    candidate_context = StageContext(nl=nl, current_dsl=candidate_dsl)
    parse_fb, _ = run_sd2_parse(candidate_dsl, candidate_context)
    if not parse_fb.ok:
        rejection = RepairRejection(
            rejected_by_stage=StageId.SD_10_REPAIR_REVIEW.value,
            reason="candidate parse failed",
            target_resolved=False,
            drift_risk="major",
            evidence=parse_fb.diagnostics,
        )
        feedback = RepairReviewFeedback(ok=False, target_resolved=False, drift_risk="major", local_rejection=rejection)
        meta = _stage_meta(StageId.SD_10_REPAIR_REVIEW, ok=False, status=StageStatus.FAIL)
        _attach_meta(None, feedback, meta)
        return feedback, meta

    sem_fb, _, _ = run_sd3_semantic(candidate_dsl, candidate_context)
    if not sem_fb.ok:
        rejection = RepairRejection(
            rejected_by_stage=StageId.SD_10_REPAIR_REVIEW.value,
            reason="candidate semantic failed",
            target_resolved=False,
            drift_risk="major",
            evidence=sem_fb.diagnostics,
        )
        feedback = RepairReviewFeedback(ok=False, target_resolved=False, drift_risk="major", local_rejection=rejection)
        meta = _stage_meta(StageId.SD_10_REPAIR_REVIEW, ok=False, status=StageStatus.FAIL)
        _attach_meta(None, feedback, meta)
        return feedback, meta

    design_feedback, _ = run_sd4_design(candidate_context)
    remaining_design: list[DesignDiagnosticItem] = []
    if fix_plan.target == "design":
        remaining_design = _remaining_design_targets(design_feedback, fix_plan)
        if remaining_design:
            evidence.append({"kind": "design_target_unresolved", "items": [asdict(item) for item in remaining_design]})
    remaining_keys = {item.instance_key for item in remaining_design}
    old_design_feedback = _design_feedback_for_review_baseline(nl, old_dsl)
    old_blocking_keys = {item.instance_key for item in old_design_feedback.blocking_items} if old_design_feedback is not None else set()
    new_blocking_design = [
        item
        for item in design_feedback.blocking_items
        if item.instance_key not in remaining_keys and item.instance_key not in old_blocking_keys
    ]
    if new_blocking_design:
        evidence.append({"kind": "new_blocking_design_diagnostic", "items": [asdict(item) for item in new_blocking_design]})

    regression_detected = False
    sim_feedback = None
    if scenario_set is not None:
        sim_feedback, _ = run_sd6_sim(candidate_dsl, scenario_set, None)
        regression_detected = not sim_feedback.ok
        if regression_detected:
            evidence.append({"kind": "scenario_regression", "sim_feedback": asdict(sim_feedback)})

    old_build = build_model_from_dsl(old_dsl)
    if old_build.model is not None and candidate_context.model is not None:
        old_summary = _model_summary(old_build.model)
        new_summary = _model_summary(candidate_context.model)
        evidence.extend(_count_drift_evidence(old_summary, new_summary, fix_plan))

    missing_required: list[str] = []
    if grounding_map is not None:
        for element in grounding_map.elements:
            if element.requiredness == "required" and _grounded_element_missing(candidate_dsl, element, candidate_context.model):
                missing_required.append(element.element_id)
    if missing_required:
        evidence.append({"kind": "missing_required_grounding", "element_ids": missing_required})

    target_resolved = not evidence
    major_drift_kinds = {"missing_required_grounding", "count_drift", "forced_transition_count_drift"}
    has_major_drift = any(item.get("kind") in major_drift_kinds for item in evidence)
    drift_risk = "major" if has_major_drift else ("minor" if regression_detected else "none")
    rejection = None
    if not target_resolved:
        rejection = RepairRejection(
            rejected_by_stage=StageId.SD_10_REPAIR_REVIEW.value,
            reason="; ".join(item["kind"] for item in evidence),
            target_resolved=False,
            regression_detected=regression_detected,
            drift_risk=drift_risk,
            evidence=evidence,
        )
    feedback = RepairReviewFeedback(
        ok=target_resolved,
        target_resolved=target_resolved,
        regression_detected=regression_detected,
        drift_risk=drift_risk,
        local_rejection=rejection,
    )
    meta = _stage_meta(StageId.SD_10_REPAIR_REVIEW, ok=feedback.ok, status=StageStatus.OK if feedback.ok else StageStatus.FAIL)
    _attach_meta(None, feedback, meta)
    return feedback, meta
