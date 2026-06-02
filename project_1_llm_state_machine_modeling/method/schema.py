"""Core dataclass schema for the agent loop.

All structured data flowing between the LLM stages, deterministic feedback
stages, and control/audit stages is typed via the dataclasses below. Path 1 /
Path 2 run scripts and the final report writers consume these as the single
source of truth.

Design choices:

- Pure stdlib ``dataclasses`` (no pydantic / attrs) to keep the dependency
  surface minimal. Submodule-style sprint code should not pull in heavyweight
  frameworks.
- All "feedback" classes carry an ``ok: bool`` field so the loop driver can do
  fast contract checks in strict ``enabled_sources`` mode.
- ``IterTrace`` captures one round (model output + feedback bundle + repair
  output) for full reconstructability of the agent loop trajectory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from method.stages.ids import (
    FEEDBACK_SOURCE_TO_STAGE_ID,
    STAGE_SPECS_BY_ID,
    FeedbackSource,
    StageKind,
    StageStatus,
)


def _coerce_nested_dataclass(value: Any, cls: type[Any]) -> Any:
    """Coerce JSON-loaded dicts into nested stdlib dataclasses.

    PR-0 intentionally uses stdlib dataclasses instead of pydantic.  Without a
    small coercion hook, dataclass construction from fixture/run-record JSON
    would leave nested objects such as ``ModelReviewFeedback.review_meta`` as
    plain dicts, silently breaking typed replay consumers.  Unknown keys remain
    schema errors because ``cls(**value)`` is deliberately strict.
    """
    if value is None or isinstance(value, cls):
        return value
    if isinstance(value, dict):
        return cls(**value)
    raise TypeError(f"expected {cls.__name__} or dict, got {type(value).__name__}")


def _coerce_dataclass_list(values: list[Any], cls: type[Any]) -> list[Any]:
    """Coerce a JSON-loaded list of dicts into typed dataclass objects."""
    return [_coerce_nested_dataclass(value, cls) for value in values]


def _coerce_dataclass_dict(values: dict[str, Any], cls: type[Any]) -> dict[str, Any]:
    """Coerce a JSON-loaded dict of dataclass payloads into typed objects."""
    return {key: _coerce_nested_dataclass(value, cls) for key, value in values.items()}


def _coerce_bool(value: Any, field_name: str) -> bool:
    """Reject JSON/schema values that only look truthy/falsy."""
    if not isinstance(value, bool):
        raise TypeError(f"{field_name} must be a bool")
    return value


def _require_one_of(value: str, allowed: set[str], field_name: str) -> str:
    """Validate runtime values for fields annotated as Literal."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a str")
    if value not in allowed:
        allowed_text = ", ".join(sorted(allowed))
        raise ValueError(f"{field_name} must be one of: {allowed_text}")
    return value


def _coerce_non_negative_number(value: Any, field_name: str) -> float:
    """Coerce numeric metadata while rejecting bool/string lookalikes."""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be a number")
    if float(value) < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return float(value)


def _coerce_optional_int(value: Any, field_name: str) -> int | None:
    """Coerce optional integer metadata while rejecting bool/string lookalikes."""
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be an int or None")
    return value


def _coerce_non_negative_int(value: Any, field_name: str) -> int:
    """Coerce required integer metadata while rejecting bool/string lookalikes."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _coerce_optional_non_negative_int(value: Any, field_name: str) -> int | None:
    """Coerce optional non-negative integer metadata for JSON schema fields."""
    if value is None:
        return None
    return _coerce_non_negative_int(value, field_name)


# ---------------------------------------------------------------------------
# LoopConfig — user-facing configuration
# ---------------------------------------------------------------------------

ConditionLiteral = Literal["A0", "A1", "A2", "A3", "A4"]
DEFAULT_ACADEMIC_QUESTION = "默认满血 staged agent-loop 是否能提升 NL→FCSTM 建模可靠性与可审计性"


def _deepcopy_jsonable(value: Any) -> Any:
    """Copy JSON-like config payloads without adding new dependencies."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _deepcopy_jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_deepcopy_jsonable(v) for v in value]
    if isinstance(value, tuple):
        return [_deepcopy_jsonable(v) for v in value]
    return value


DEFAULT_STAGE_SWITCHES: dict[str, bool] = {
    "enforce_top_down_revalidation": True,
    "enable_initial_modeling": True,
    "enable_parse": True,
    "enable_semantic": True,
    "enable_design_inspect": True,
    "enable_scenario_generation": True,
    "enable_scenario_coverage": True,
    "enable_simulation": True,
    "enable_model_review": True,
    "enable_fix_plan": True,
    "enable_repair": True,
    "enable_repair_review": True,
    "enable_delta_review": True,
    "enable_run_record": True,
}


def _default_stage_switches() -> dict[str, bool]:
    return dict(DEFAULT_STAGE_SWITCHES)


def _default_feedback_policy() -> dict[str, Any]:
    return {
        "parse_fail": "blocking",
        "semantic_error": "blocking",
        "design_error": "hard_block",
        "design_high_conf_warning": "budgeted_repair",
        "design_unknown_warning": "requires_policy_classification",
        "design_info": "trace_only",
        "scenario_coverage_gap": "targeted_retry_then_weak_oracle",
        "sim_fail": "blocking",
        "model_review": "blocking_major_only",
        "repair_review": "blocking",
        "delta_review": "blocking_major_only",
        "suggested_fix": "context_only_not_mandatory",
    }


def _default_budget_policy() -> dict[str, Any]:
    return {
        "max_iterations": 5,
        "pre_scenario_max_repairs": 3,
        "llm_max_retries": 2,
        "scenario_max_retries": 2,
        "warning_repair_budget_per_instance": 1,
        "token_budget": None,
        "time_budget_seconds": None,
    }


def _default_scenario_policy() -> dict[str, Any]:
    return {
        "generation": "generate_if_absent_or_invalidated",
        "freeze_after_coverage": True,
        "reuse_frozen_oracle_after_repair": True,
        "coverage_retry": "targeted",
        "weak_oracle_marks_main_result_ineligible": True,
    }


def _default_llm_policy() -> dict[str, Any]:
    return {
        "provider_mode": "real_env",
        "model": None,
        "temperature": 0.0,
        "seed": None,
        "retry_on": ["provider_error", "network_error", "timeout", "rate_limit", "schema_invalid", "empty_output"],
        "deterministic_stage_retry": False,
    }


def _default_record_policy() -> dict[str, Any]:
    return {
        "write_run_record": True,
        "record_prompts": True,
        "record_raw_outputs": True,
        "redact_secrets": True,
        "schema_invalid_excludes_main_result": True,
        "record_path_suffix": ".agent_loop.json.gz",
    }


def _default_eligibility_policy() -> dict[str, Any]:
    return {
        "main_result_requires_success": True,
        "exclude_weak_oracle": True,
        "exclude_schema_invalid": True,
        "exclude_unredacted_secret": True,
        "exclude_fake_or_replay_default_path": True,
    }


@dataclass
class AblationCondition:
    """Research-facing condition contract for future ablation studies.

    The contract intentionally stores policy dictionaries instead of locking a
    complete experiment matrix in PR-A.  This gives PR-B1/B2/C a stable schema
    while preserving academic traceability: every non-default condition must say
    what changed and which research question it answers.
    """

    condition_id: str
    condition_family: str
    base_condition_id: str = "full_staged_v1"
    changed_factors: list[str] = field(default_factory=list)
    stage_switches: dict[str, bool] = field(default_factory=_default_stage_switches)
    feedback_policy: dict[str, Any] = field(default_factory=_default_feedback_policy)
    budget_policy: dict[str, Any] = field(default_factory=_default_budget_policy)
    scenario_policy: dict[str, Any] = field(default_factory=_default_scenario_policy)
    llm_policy: dict[str, Any] = field(default_factory=_default_llm_policy)
    record_policy: dict[str, Any] = field(default_factory=_default_record_policy)
    eligibility_policy: dict[str, Any] = field(default_factory=_default_eligibility_policy)
    academic_question: str = ""

    def __post_init__(self) -> None:
        if not self.condition_id:
            raise ValueError("AblationCondition.condition_id is required")
        if not self.condition_family:
            raise ValueError("AblationCondition.condition_family is required")
        if self.condition_id != "full_staged_v1" and not self.changed_factors:
            raise ValueError("non-default ablation condition must declare changed_factors")
        if self.condition_id != "full_staged_v1" and not self.academic_question:
            raise ValueError("non-default ablation condition must declare academic_question")
        for key, value in self.stage_switches.items():
            if not isinstance(value, bool):
                raise TypeError(f"stage_switches.{key} must be a bool")

    def to_resolved_dict(self) -> dict[str, Any]:
        return {
            "condition_id": self.condition_id,
            "condition_family": self.condition_family,
            "base_condition_id": self.base_condition_id,
            "changed_factors": list(self.changed_factors),
            "stage_switches": dict(self.stage_switches),
            "feedback_policy": _deepcopy_jsonable(self.feedback_policy),
            "budget_policy": _deepcopy_jsonable(self.budget_policy),
            "scenario_policy": _deepcopy_jsonable(self.scenario_policy),
            "llm_policy": _deepcopy_jsonable(self.llm_policy),
            "record_policy": _deepcopy_jsonable(self.record_policy),
            "eligibility_policy": _deepcopy_jsonable(self.eligibility_policy),
            "academic_question": self.academic_question,
        }


def experiment_default_condition() -> AblationCondition:
    return AblationCondition(
        condition_id="full_staged_v1",
        condition_family="canonical_agent_loop",
        base_condition_id="full_staged_v1",
        changed_factors=[],
        stage_switches=_default_stage_switches(),
        feedback_policy=_default_feedback_policy(),
        budget_policy=_default_budget_policy(),
        scenario_policy=_default_scenario_policy(),
        llm_policy=_default_llm_policy(),
        record_policy=_default_record_policy(),
        eligibility_policy=_default_eligibility_policy(),
        academic_question=DEFAULT_ACADEMIC_QUESTION,
    )


def _condition_hash(payload: dict[str, Any]) -> str:
    import hashlib
    import json

    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return "sha256:" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()


@dataclass
class LoopConfig:
    """Canonical full staged agent-loop config.

    ``LoopConfig()`` is the recommended default for Path1/Path2 main
    experiments and resolves to ``experiment_default/full_staged_v1``.  Any
    ablation that disables stages, weakens oracle policy, disables review, or
    changes budgets must be declared through an explicit ``AblationCondition``
    / ``condition_id`` instead of silently mutating the default path.
    """

    condition_id: str = "full_staged_v1"
    condition_family: str = "canonical_agent_loop"
    base_condition_id: str = "full_staged_v1"
    changed_factors: list[str] = field(default_factory=list)
    policy_profile: str = "experiment_default"
    max_iterations: int = 5
    pre_scenario_max_repairs: int = 3
    llm_provider_mode: Literal["real_env", "fake_replay", "mock"] = "real_env"
    llm_max_retries: int = 2
    scenario_max_retries: int = 2
    stage_switches: dict[str, bool] = field(default_factory=_default_stage_switches)
    feedback_policy: dict[str, Any] = field(default_factory=_default_feedback_policy)
    budget_policy: dict[str, Any] = field(default_factory=_default_budget_policy)
    scenario_policy: dict[str, Any] = field(default_factory=_default_scenario_policy)
    llm_policy: dict[str, Any] = field(default_factory=_default_llm_policy)
    record_policy: dict[str, Any] = field(default_factory=_default_record_policy)
    eligibility_policy: dict[str, Any] = field(default_factory=_default_eligibility_policy)
    academic_question: str = DEFAULT_ACADEMIC_QUESTION
    model_review_mode: str = "blocking_major_only"
    delta_review_mode: str = "blocking_major_only"
    write_run_record: bool = True
    output_dir: str = "runs"
    run_id: Optional[str] = None
    llm_model: Optional[str] = None
    seed: Optional[int] = None
    config_source: str = "LoopConfig()"
    compatibility_mode: str = "canonical_staged"
    ablation_condition: Optional[AblationCondition] = None

    def __post_init__(self) -> None:
        self.write_run_record = _coerce_bool(self.write_run_record, "LoopConfig.write_run_record")
        self.max_iterations = _coerce_non_negative_int(self.max_iterations, "LoopConfig.max_iterations")
        self.pre_scenario_max_repairs = _coerce_non_negative_int(
            self.pre_scenario_max_repairs,
            "LoopConfig.pre_scenario_max_repairs",
        )
        self.llm_max_retries = _coerce_non_negative_int(self.llm_max_retries, "LoopConfig.llm_max_retries")
        self.scenario_max_retries = _coerce_non_negative_int(self.scenario_max_retries, "LoopConfig.scenario_max_retries")
        self.llm_provider_mode = _require_one_of(
            self.llm_provider_mode,
            {"real_env", "fake_replay", "mock"},
            "LoopConfig.llm_provider_mode",
        )
        if self.ablation_condition is not None:
            self.ablation_condition = _coerce_nested_dataclass(self.ablation_condition, AblationCondition)
            self._apply_ablation_condition(self.ablation_condition)
            self.llm_provider_mode = _require_one_of(
                self.llm_provider_mode,
                {"real_env", "fake_replay", "mock"},
                "LoopConfig.llm_provider_mode",
            )
        for key, value in self.stage_switches.items():
            if not isinstance(value, bool):
                raise TypeError(f"LoopConfig.stage_switches.{key} must be a bool")
        if self.condition_id == "full_staged_v1":
            if self.changed_factors:
                raise ValueError("default full_staged_v1 must not declare changed_factors")
            self._reject_implicit_default_ablation()
        else:
            if not self.changed_factors:
                raise ValueError("non-default LoopConfig requires explicit changed_factors")
            if not self.academic_question or self.academic_question == DEFAULT_ACADEMIC_QUESTION:
                raise ValueError("non-default LoopConfig requires explicit non-default academic_question")

    @property
    def n_iter(self) -> int:
        """Deprecated compatibility alias for legacy callers."""
        return self.max_iterations

    @property
    def feedback_sources(self) -> list[str]:
        """Canonical required feedback sources enabled by stage switches."""
        sources: list[str] = []
        if self.stage_switches.get("enable_parse", False):
            sources.append(FeedbackSource.PARSE.value)
        if self.stage_switches.get("enable_semantic", False):
            sources.append(FeedbackSource.SEMANTIC.value)
        if self.stage_switches.get("enable_design_inspect", False):
            sources.append(FeedbackSource.DESIGN.value)
        if self.stage_switches.get("enable_simulation", False):
            sources.append(FeedbackSource.SIM.value)
        if self.stage_switches.get("enable_model_review", False):
            sources.append(FeedbackSource.MODEL_REVIEW.value)
        return sources

    def _apply_ablation_condition(self, condition: AblationCondition) -> None:
        resolved = condition.to_resolved_dict()
        self.condition_id = condition.condition_id
        self.condition_family = condition.condition_family
        self.base_condition_id = condition.base_condition_id
        self.changed_factors = list(condition.changed_factors)
        self.stage_switches = dict(condition.stage_switches)
        self.feedback_policy = _deepcopy_jsonable(condition.feedback_policy)
        self.budget_policy = _deepcopy_jsonable(condition.budget_policy)
        self.scenario_policy = _deepcopy_jsonable(condition.scenario_policy)
        self.llm_policy = _deepcopy_jsonable(condition.llm_policy)
        self.record_policy = _deepcopy_jsonable(condition.record_policy)
        self.eligibility_policy = _deepcopy_jsonable(condition.eligibility_policy)
        self.academic_question = condition.academic_question
        self.max_iterations = int(self.budget_policy.get("max_iterations", self.max_iterations))
        self.pre_scenario_max_repairs = int(self.budget_policy.get("pre_scenario_max_repairs", self.pre_scenario_max_repairs))
        self.llm_max_retries = int(self.budget_policy.get("llm_max_retries", self.llm_max_retries))
        self.scenario_max_retries = int(self.budget_policy.get("scenario_max_retries", self.scenario_max_retries))
        self.llm_provider_mode = self.llm_policy.get("provider_mode", self.llm_provider_mode)
        self.write_run_record = bool(self.record_policy.get("write_run_record", self.write_run_record))
        self.config_source = f"AblationCondition:{condition.condition_id}"

    def _reject_implicit_default_ablation(self) -> None:
        defaults = experiment_default_condition()
        default_switches = defaults.stage_switches
        if self.stage_switches != default_switches:
            raise ValueError(
                "LoopConfig() default path cannot silently change stage_switches; "
                "declare a non-default condition_id with changed_factors for ablation"
            )
        default_budget = defaults.budget_policy
        expected_budget = {
            "max_iterations": self.max_iterations,
            "pre_scenario_max_repairs": self.pre_scenario_max_repairs,
            "llm_max_retries": self.llm_max_retries,
            "scenario_max_retries": self.scenario_max_retries,
            "warning_repair_budget_per_instance": self.budget_policy.get("warning_repair_budget_per_instance", 1),
            "token_budget": self.budget_policy.get("token_budget"),
            "time_budget_seconds": self.budget_policy.get("time_budget_seconds"),
        }
        if expected_budget != default_budget or self.budget_policy != default_budget:
            raise ValueError(
                "LoopConfig() default path cannot silently change budget_policy; "
                "declare a non-default condition_id with changed_factors for ablation"
            )
        if self.feedback_policy != defaults.feedback_policy:
            raise ValueError(
                "LoopConfig() default path cannot silently change feedback_policy; "
                "declare a non-default condition_id with changed_factors for feedback-policy ablation"
            )
        if self.scenario_policy != defaults.scenario_policy:
            raise ValueError(
                "LoopConfig() default path cannot silently change scenario_policy; "
                "declare a non-default condition_id with changed_factors for scenario/oracle ablation"
            )
        if self.llm_policy != defaults.llm_policy:
            raise ValueError(
                "LoopConfig() default path cannot silently change llm_policy; "
                "declare a non-default condition_id with changed_factors for provider/model/retry ablation"
            )
        if self.eligibility_policy != defaults.eligibility_policy:
            raise ValueError(
                "LoopConfig() default path cannot silently change eligibility_policy; "
                "declare a non-default condition_id with changed_factors for eligibility ablation"
            )
        if self.model_review_mode != "blocking_major_only" or self.delta_review_mode != "blocking_major_only":
            raise ValueError(
                "LoopConfig() default path cannot silently weaken review modes; "
                "declare a non-default condition_id with changed_factors for review ablation"
            )
        if self.record_policy != defaults.record_policy or self.write_run_record is not True:
            raise ValueError(
                "LoopConfig() default path must write schema-valid run records; "
                "declare a non-default condition_id with changed_factors for record-policy ablation"
            )
        if self.llm_provider_mode != "real_env":
            raise ValueError(
                "LoopConfig() default path must use real_env; use explicit non-default condition for fake/replay/mock"
            )

    def resolved_config(self) -> dict[str, Any]:
        payload = {
            "condition_id": self.condition_id,
            "condition_family": self.condition_family,
            "base_condition_id": self.base_condition_id,
            "changed_factors": list(self.changed_factors),
            "policy_profile": self.policy_profile,
            "max_iterations": self.max_iterations,
            "pre_scenario_max_repairs": self.pre_scenario_max_repairs,
            "llm_provider_mode": self.llm_provider_mode,
            "llm_max_retries": self.llm_max_retries,
            "scenario_max_retries": self.scenario_max_retries,
            "stage_switches": dict(self.stage_switches),
            "feedback_sources": self.feedback_sources,
            "feedback_policy": _deepcopy_jsonable(self.feedback_policy),
            "budget_policy": _deepcopy_jsonable(self.budget_policy),
            "scenario_policy": _deepcopy_jsonable(self.scenario_policy),
            "llm_policy": _deepcopy_jsonable(self.llm_policy),
            "record_policy": _deepcopy_jsonable(self.record_policy),
            "eligibility_policy": _deepcopy_jsonable(self.eligibility_policy),
            "academic_question": self.academic_question,
            "model_review_mode": self.model_review_mode,
            "delta_review_mode": self.delta_review_mode,
            "write_run_record": self.write_run_record,
            "output_dir": self.output_dir,
            "run_id": self.run_id,
            "llm_model": self.llm_model,
            "seed": self.seed,
            "config_source": self.config_source,
            "compatibility_mode": self.compatibility_mode,
        }
        payload["condition_hash"] = _condition_hash(payload)
        return payload


@dataclass
class LegacyLoopConfig:
    """Deprecated config for the old A0-A4 legacy loop."""

    condition: ConditionLiteral = "A4"
    n_iter: int = 3
    feedback_sources: list[str] = field(default_factory=lambda: ["parse", "semantic", "sim"])
    modeling_mode: Literal["single_prompt", "multi_step"] = "multi_step"
    llm_model: Optional[str] = None
    seed: Optional[int] = None


# ---------------------------------------------------------------------------
# Agent outputs
# ---------------------------------------------------------------------------


@dataclass
class SpecJson:
    """Structured-spec output from SpecExtractor (NL → JSON)."""

    states: list[str] = field(default_factory=list)
    events: list[str] = field(default_factory=list)
    variables: list[dict[str, Any]] = field(default_factory=list)
    transitions: list[dict[str, Any]] = field(default_factory=list)
    hierarchy: list[dict[str, Any]] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelArtifact:
    """A pyfcstm DSL output from Modeler or Repair."""

    dsl_text: str = ""
    iteration: int = 0
    produced_by: Literal["modeler", "repair"] = "modeler"


# ---------------------------------------------------------------------------
# PR-0 stage contract metadata
# ---------------------------------------------------------------------------


@dataclass
class StageResultMeta:
    """Uniform execution metadata for one ``SL-*`` / ``SD-*`` / ``SC-*`` stage.

    PR-0 freezes this as the minimal cross-PR contract: every enabled stage must
    either produce a meta row or be treated as an enabled-but-missing error by
    ``FeedbackBundle.all_ok`` / later loop wiring.
    """

    stage_id: str
    stage_kind: StageKind | str
    enabled: bool
    ran: bool
    status: StageStatus | str
    ok: bool
    skipped_reason: Optional[str] = None
    stage_error: Optional[str] = None
    output_validation_error: Optional[str] = None
    input_hash: Optional[str] = None
    output_hash: Optional[str] = None
    prompt_hash: Optional[str] = None
    elapsed_ms: Optional[int] = None

    def __post_init__(self) -> None:
        self.enabled = _coerce_bool(self.enabled, "StageResultMeta.enabled")
        self.ran = _coerce_bool(self.ran, "StageResultMeta.ran")
        self.ok = _coerce_bool(self.ok, "StageResultMeta.ok")
        if isinstance(self.stage_kind, str):
            self.stage_kind = StageKind(self.stage_kind)
        elif not isinstance(self.stage_kind, StageKind):
            raise TypeError("StageResultMeta.stage_kind must be a StageKind or str")
        if isinstance(self.status, str):
            self.status = StageStatus(self.status)
        elif not isinstance(self.status, StageStatus):
            raise TypeError("StageResultMeta.status must be a StageStatus or str")

    def contract_errors(self) -> list[str]:
        """Return PR-0 contract violations for this stage meta row.

        A stage can legitimately report ``fail`` or ``advisory`` as an
        execution result, but contract-shape problems (for example ``skipped``
        without reason) must be visible to ``FeedbackBundle.all_ok`` and later
        run-record validation.
        """
        errors: list[str] = []
        spec = STAGE_SPECS_BY_ID.get(self.stage_id)
        if spec is None:
            errors.append(f"unknown stage_id: {self.stage_id}")
        elif self.stage_kind != spec.kind:
            errors.append(
                f"stage_kind mismatch for {self.stage_id}: "
                f"expected {spec.kind.value}, got {self.stage_kind.value}"
            )
        if self.enabled and self.status == StageStatus.SKIPPED and not self.skipped_reason:
            errors.append("skipped stage must provide skipped_reason")
        if self.enabled and self.status == StageStatus.ERROR and not (self.stage_error or self.output_validation_error):
            errors.append("error stage must provide stage_error or output_validation_error")
        if self.enabled and self.ran and self.status == StageStatus.SKIPPED:
            errors.append("skipped stage cannot be marked ran=True")
        if self.enabled and not self.ran and self.status not in {StageStatus.SKIPPED, StageStatus.ERROR}:
            errors.append("enabled stage that did not run must be skipped or error")
        return errors

    @property
    def contract_ok(self) -> bool:
        return not self.contract_errors()

    @property
    def blocks_all_ok(self) -> bool:
        """Whether this meta row should make a feedback bundle non-ok."""
        if not self.enabled:
            return False
        if not self.contract_ok:
            return True
        if self.status in {StageStatus.FAIL, StageStatus.ERROR}:
            return True
        if self.status == StageStatus.OK and not self.ok:
            return True
        return False


@dataclass
class BudgetState:
    """Per-diagnostic warning repair budget state.

    The key is an instance-level diagnostic identity such as
    ``W_DEADLOCK_LEAF:state=Root.Idle`` rather than only the warning code.
    """

    instance_key: str
    diagnostic_code: str
    repair_count: int = 0
    budget_remaining: int = 0
    budget_exhausted: bool = False
    last_status: Optional[str] = None
    last_stage: Optional[str] = None

    def __post_init__(self) -> None:
        self.budget_exhausted = _coerce_bool(self.budget_exhausted, "BudgetState.budget_exhausted")
        if not isinstance(self.repair_count, int) or isinstance(self.repair_count, bool):
            raise TypeError("BudgetState.repair_count must be an int")
        if not isinstance(self.budget_remaining, int) or isinstance(self.budget_remaining, bool):
            raise TypeError("BudgetState.budget_remaining must be an int")
        if self.repair_count < 0:
            raise ValueError("BudgetState.repair_count must be >= 0")
        if self.budget_remaining < 0:
            raise ValueError("BudgetState.budget_remaining must be >= 0")
        if self.budget_exhausted and self.budget_remaining != 0:
            raise ValueError("BudgetState.budget_exhausted requires budget_remaining == 0")


# ---------------------------------------------------------------------------
# Feedback sources
# ---------------------------------------------------------------------------


@dataclass
class ParseFeedback:
    """Output of ``pyfcstm.dsl.parse_with_grammar_entry``.

    ``diagnostics`` carries normalized parser-error entries extracted from
    ``GrammarParseError.errors``. The human ``error_message`` is kept for
    display only; repair logic should prefer the structured fields.
    """

    ok: bool = False
    line: Optional[int] = None
    col: Optional[int] = None
    expected_tokens: list[str] = field(default_factory=list)
    got: Optional[str] = None
    snippet: Optional[str] = None
    error_class: Optional[str] = None
    error_message: Optional[str] = None
    diagnostics: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.ok = _coerce_bool(self.ok, "ParseFeedback.ok")


@dataclass
class SemanticFeedback:
    """Output of ``pyfcstm.model.parse_dsl_node_to_state_machine``.

    ``ok=True`` iff AST → state-machine model conversion succeeded with no
    error-level diagnostics. Category fields are populated from stable
    ``ModelDiagnostic.code`` / ``refs`` payloads. The full normalized
    diagnostic list is preserved for LLM repair prompts and auditability.
    """

    ok: bool = False
    missing_states: list[str] = field(default_factory=list)
    dangling_transitions: list[dict[str, Any]] = field(default_factory=list)
    unresolved_event_refs: list[dict[str, Any]] = field(default_factory=list)
    undefined_vars: list[str] = field(default_factory=list)
    type_mismatches: list[dict[str, Any]] = field(default_factory=list)
    other_errors: list[dict[str, Any]] = field(default_factory=list)
    diagnostics: list[dict[str, Any]] = field(default_factory=list)
    error_class: Optional[str] = None
    error_message: Optional[str] = None

    def __post_init__(self) -> None:
        self.ok = _coerce_bool(self.ok, "SemanticFeedback.ok")


StepStatusLiteral = Literal["pass", "fail", "error"]


@dataclass
class ScenarioStep:
    """One step in a multi-step scenario.

    Execution semantics (per step):

      1. ``cycle()`` × ``before_cycles``         (empty cycles to let model advance freely)
      2. depending on ``events``:
           - ``None``        => skip the cycle entirely (no advancing this step)
           - ``[]``          => ``cycle()``                (one cycle, no events injected)
           - ``[e1, e2,...]``=> ``cycle(events=[e1,e2,...])`` (one cycle, all events injected as
                                                          a single batch — supports pseudo-state
                                                          chained jumps that need multiple events
                                                          all triggered together)
      3. checkpoint: assert state == ``expected_state`` (if not None) and ``actual_vars``
         contains the listed ``expected_vars`` (if not None / non-empty). Vars NOT listed
         in ``expected_vars`` are "don't care" (not checked).
    """

    before_cycles: int = 0
    events: Optional[list[str]] = None
    expected_state: Optional[str] = None
    expected_vars: Optional[dict[str, Any]] = None
    name: str = ""  # optional checkpoint label for trace

    def __post_init__(self) -> None:
        self.before_cycles = _coerce_non_negative_int(self.before_cycles, "ScenarioStep.before_cycles")


@dataclass
class StepResult:
    """Outcome of executing one ScenarioStep against a runtime."""

    step_index: int = 0
    step_name: str = ""
    status: StepStatusLiteral = "pass"
    actual_state: str = ""                       # state at end of step
    actual_vars: dict[str, Any] = field(default_factory=dict)  # all vars at end of step
    state_assertion_ok: Optional[bool] = None    # None if expected_state was None
    var_assertion_ok: Optional[bool] = None      # None if expected_vars was None/empty
    var_mismatches: dict[str, dict[str, Any]] = field(default_factory=dict)  # {var: {expected, actual}}
    runtime_error: Optional[str] = None          # set if status == 'error'

    def __post_init__(self) -> None:
        self.step_index = _coerce_non_negative_int(self.step_index, "StepResult.step_index")
        self.status = _require_one_of(self.status, {"pass", "fail", "error"}, "StepResult.status")
        if self.state_assertion_ok is not None:
            self.state_assertion_ok = _coerce_bool(self.state_assertion_ok, "StepResult.state_assertion_ok")
        if self.var_assertion_ok is not None:
            self.var_assertion_ok = _coerce_bool(self.var_assertion_ok, "StepResult.var_assertion_ok")


@dataclass
class TestScenario:
    """A multi-step model-level test scenario (BDD-style, not LTL/CTL).

    Composed of:
      - hot-start setup (``initial_state`` + ``initial_vars``)
      - a sequence of ``steps``, each is a (before_cycles, events, expected_*) tuple
        with an embedded checkpoint

    Empty ``steps`` list is legal — represents a "hot-start sanity check" scenario
    that only verifies the runtime can be constructed at ``initial_state`` /
    ``initial_vars`` without errors.
    """

    name: str = ""
    description: str = ""
    initial_state: Optional[str] = None  # hot-start state path (None => default initial transition)
    initial_vars: dict[str, Any] = field(default_factory=dict)
    steps: list[ScenarioStep] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.steps = _coerce_dataclass_list(self.steps, ScenarioStep)


@dataclass
class ScenarioResult:
    """Per-scenario aggregate result (collects all step results + overall status)."""

    name: str = ""
    description: str = ""
    status: StepStatusLiteral = "pass"  # pass if all steps pass; fail if any step fail (no error); error if any step error
    step_results: list[StepResult] = field(default_factory=list)
    setup_error: Optional[str] = None  # SimulationRuntime construction failed (e.g. bad initial_state)

    def __post_init__(self) -> None:
        self.status = _require_one_of(self.status, {"pass", "fail", "error"}, "ScenarioResult.status")
        self.step_results = _coerce_dataclass_list(self.step_results, StepResult)


@dataclass
class SimFeedback:
    """Output of running pyfcstm ``SimulationRuntime`` against a list of scenarios.

    ``ok=True`` iff every scenario's overall status is ``pass``. The detailed
    per-scenario, per-step results (with state/vars/assertion info) are in
    ``scenario_results`` and consumed downstream by the Repair agent prompt.
    """

    ok: bool = False
    n_scenarios: int = 0
    n_scenarios_passed: int = 0
    scenario_results: list[ScenarioResult] = field(default_factory=list)
    setup_error: Optional[str] = None  # global parse/sem fail before any scenario could run

    def __post_init__(self) -> None:
        self.ok = _coerce_bool(self.ok, "SimFeedback.ok")
        self.n_scenarios = _coerce_non_negative_int(self.n_scenarios, "SimFeedback.n_scenarios")
        self.n_scenarios_passed = _coerce_non_negative_int(
            self.n_scenarios_passed,
            "SimFeedback.n_scenarios_passed",
        )
        self.scenario_results = _coerce_dataclass_list(self.scenario_results, ScenarioResult)


@dataclass
class JudgeFeedback:
    """Output of ex1 ``ExpertReviewAgent`` adapter.

    rubric_scores keys (5 dim): coverage / fidelity / structure / executability / safety.
    Each in ``[0, 1]``. ``overall`` is the rubric total in ``[0, 1]``.
    ``ok=True`` iff overall >= 0.7 (sprint threshold; tuneable).
    """

    ok: bool = False
    rubric_scores: dict[str, float] = field(default_factory=dict)
    overall: float = 0.0
    evidence_spans: list[dict[str, Any]] = field(default_factory=list)
    judge_error: Optional[str] = None

    def __post_init__(self) -> None:
        self.ok = _coerce_bool(self.ok, "JudgeFeedback.ok")


@dataclass
class DesignDiagnosticItem:
    """Normalized pyfcstm design-health diagnostic item."""

    code: str
    pyfcstm_severity: Literal["error", "warning", "info"]
    policy_action: Literal[
        "hard_block",
        "budgeted_repair",
        "advisory",
        "info",
        "requires_policy_classification",
    ]
    instance_key: str
    refs: dict[str, Any] = field(default_factory=dict)
    message: str = ""
    suggested_fix_hints: list[dict[str, Any]] = field(default_factory=list)
    budget_remaining: Optional[int] = None
    budget_exhausted: bool = False

    def __post_init__(self) -> None:
        self.pyfcstm_severity = _require_one_of(
            self.pyfcstm_severity,
            {"error", "warning", "info"},
            "DesignDiagnosticItem.pyfcstm_severity",
        )
        self.policy_action = _require_one_of(
            self.policy_action,
            {"hard_block", "budgeted_repair", "advisory", "info", "requires_policy_classification"},
            "DesignDiagnosticItem.policy_action",
        )
        self.budget_remaining = _coerce_optional_non_negative_int(
            self.budget_remaining,
            "DesignDiagnosticItem.budget_remaining",
        )
        self.budget_exhausted = _coerce_bool(
            self.budget_exhausted,
            "DesignDiagnosticItem.budget_exhausted",
        )


@dataclass
class DesignFeedback:
    """Output contract for ``SD-4 DesignFeedback``."""

    ok: bool = False
    blocking_items: list[DesignDiagnosticItem] = field(default_factory=list)
    advisory_items: list[DesignDiagnosticItem] = field(default_factory=list)
    info_items: list[DesignDiagnosticItem] = field(default_factory=list)
    policy_profile: str = "generated_candidate"
    inspect_summary: dict[str, Any] = field(default_factory=dict)
    meta: Optional[StageResultMeta] = None

    def __post_init__(self) -> None:
        self.ok = _coerce_bool(self.ok, "DesignFeedback.ok")
        self.blocking_items = _coerce_dataclass_list(self.blocking_items, DesignDiagnosticItem)
        self.advisory_items = _coerce_dataclass_list(self.advisory_items, DesignDiagnosticItem)
        self.info_items = _coerce_dataclass_list(self.info_items, DesignDiagnosticItem)
        self.meta = _coerce_nested_dataclass(self.meta, StageResultMeta)


@dataclass
class ReviewRunMeta:
    """Replay/audit metadata for one LLM review or delta-review call."""

    provider: str = ""
    model_id: str = ""
    resolved_model_id: Optional[str] = None
    prompt_template_version: str = ""
    prompt_hash: str = ""
    input_hash: str = ""
    temperature: float = 0.0
    seed: Optional[int] = None
    retry_count: int = 0
    raw_output_hash: str = ""
    raw_output_path: Optional[str] = None
    parsed_schema_version: str = ""
    schema_validation_ok: bool = False
    schema_validation_error: Optional[str] = None
    cache_key: str = ""
    decision_threshold: Optional[float] = None
    failure_policy: Literal["fail_open", "fail_closed", "audit_only"] = "fail_closed"
    replay_key: str = ""

    def __post_init__(self) -> None:
        self.schema_validation_ok = _coerce_bool(self.schema_validation_ok, "ReviewRunMeta.schema_validation_ok")
        self.temperature = _coerce_non_negative_number(self.temperature, "ReviewRunMeta.temperature")
        self.seed = _coerce_optional_int(self.seed, "ReviewRunMeta.seed")
        if self.decision_threshold is not None:
            if not isinstance(self.decision_threshold, (int, float)) or isinstance(self.decision_threshold, bool):
                raise TypeError("ReviewRunMeta.decision_threshold must be a number or None")
            if not 0 <= float(self.decision_threshold) <= 1:
                raise ValueError("ReviewRunMeta.decision_threshold must be within [0, 1]")
            self.decision_threshold = float(self.decision_threshold)
        if self.failure_policy not in {"fail_open", "fail_closed", "audit_only"}:
            raise ValueError("ReviewRunMeta.failure_policy must be fail_open, fail_closed, or audit_only")
        if not isinstance(self.retry_count, int) or isinstance(self.retry_count, bool):
            raise TypeError("ReviewRunMeta.retry_count must be an int")
        if self.retry_count < 0:
            raise ValueError("ReviewRunMeta.retry_count must be >= 0")


@dataclass
class ModelReviewFeedback:
    """Output contract for ``SL-7 Lightweight Model Review``."""

    ok: bool = False
    decision: Literal["pass", "fail", "audit_only", "invalid_output"] = "audit_only"
    risk_level: Literal["none", "minor", "major"] = "none"
    findings: list[dict[str, Any]] = field(default_factory=list)
    blocking_findings: list[dict[str, Any]] = field(default_factory=list)
    review_meta: Optional[ReviewRunMeta] = None
    meta: Optional[StageResultMeta] = None

    def __post_init__(self) -> None:
        self.ok = _coerce_bool(self.ok, "ModelReviewFeedback.ok")
        self.decision = _require_one_of(
            self.decision,
            {"pass", "fail", "audit_only", "invalid_output"},
            "ModelReviewFeedback.decision",
        )
        self.risk_level = _require_one_of(
            self.risk_level,
            {"none", "minor", "major"},
            "ModelReviewFeedback.risk_level",
        )
        self.review_meta = _coerce_nested_dataclass(self.review_meta, ReviewRunMeta)
        self.meta = _coerce_nested_dataclass(self.meta, StageResultMeta)


@dataclass
class RepairReviewFeedback:
    """Output contract for ``SD-10`` plus optional ``SL-10B`` delta review."""

    ok: bool = False
    target_resolved: bool = False
    regression_detected: bool = False
    drift_risk: Literal["none", "minor", "major"] = "none"
    local_rejection: Optional["RepairRejection"] = None
    delta_review: Optional[dict[str, Any]] = None
    review_meta: Optional[ReviewRunMeta] = None
    meta: Optional[StageResultMeta] = None

    def __post_init__(self) -> None:
        self.ok = _coerce_bool(self.ok, "RepairReviewFeedback.ok")
        self.target_resolved = _coerce_bool(self.target_resolved, "RepairReviewFeedback.target_resolved")
        self.regression_detected = _coerce_bool(self.regression_detected, "RepairReviewFeedback.regression_detected")
        self.drift_risk = _require_one_of(
            self.drift_risk,
            {"none", "minor", "major"},
            "RepairReviewFeedback.drift_risk",
        )
        self.local_rejection = _coerce_nested_dataclass(self.local_rejection, RepairRejection)
        self.review_meta = _coerce_nested_dataclass(self.review_meta, ReviewRunMeta)
        if self.delta_review is not None and self.review_meta is None:
            raise ValueError("RepairReviewFeedback.review_meta is required when delta_review is present")
        self.meta = _coerce_nested_dataclass(self.meta, StageResultMeta)


@dataclass
class GroundedElement:
    """One model element grounded in NL/spec/upstream evidence."""

    element_id: str
    element_kind: Literal[
        "state",
        "event",
        "variable",
        "transition",
        "guard",
        "action",
        "hierarchical_state",
    ]
    element_ref: str
    source_stage: str
    evidence_text: str
    nl_span: Optional[tuple[int, int]] = None
    requirement_id: Optional[str] = None
    confidence: Optional[float] = None
    requiredness: Literal["required", "optional", "speculative", "unknown"] = "unknown"

    def __post_init__(self) -> None:
        self.element_kind = _require_one_of(
            self.element_kind,
            {"state", "event", "variable", "transition", "guard", "action", "hierarchical_state"},
            "GroundedElement.element_kind",
        )
        self.requiredness = _require_one_of(
            self.requiredness,
            {"required", "optional", "speculative", "unknown"},
            "GroundedElement.requiredness",
        )
        if self.confidence is not None:
            if not isinstance(self.confidence, (int, float)) or isinstance(self.confidence, bool):
                raise TypeError("GroundedElement.confidence must be a number or None")
            if not 0 <= float(self.confidence) <= 1:
                raise ValueError("GroundedElement.confidence must be within [0, 1]")
            self.confidence = float(self.confidence)


@dataclass
class GroundingMap:
    """NL/spec provenance map consumed by repair and repair-review stages."""

    elements: list[GroundedElement] = field(default_factory=list)
    source_summary: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.elements = _coerce_dataclass_list(self.elements, GroundedElement)


@dataclass
class ScenarioSet:
    """Frozen scenario oracle plus provenance hashes."""

    scenario_set_id: str = ""
    scenarios: list[TestScenario] = field(default_factory=list)
    source_dsl_hash: str = ""
    source_inspect_hash: str = ""
    source_grounding_hash: Optional[str] = None
    coverage_report: dict[str, Any] = field(default_factory=dict)
    epoch: int = 0
    frozen: bool = True
    invalidated_by: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.scenarios = _coerce_dataclass_list(self.scenarios, TestScenario)
        self.epoch = _coerce_non_negative_int(self.epoch, "ScenarioSet.epoch")
        self.frozen = _coerce_bool(self.frozen, "ScenarioSet.frozen")


FixTarget = Literal["parse", "semantic", "design", "sim", "model_review"]


@dataclass
class FixPlan:
    """Structured repair plan produced before ``SL-9 Repair``."""

    target: FixTarget
    source_stage: str
    source_feedback_id: str
    severity: Literal["error", "blocking_warning", "advisory_warning", "review_fail", "sim_fail"]
    diagnostic_ids: list[str] = field(default_factory=list)
    problem_summary: str = ""
    evidence: list[dict[str, Any]] = field(default_factory=list)
    suggested_fix_hints: list[dict[str, Any]] = field(default_factory=list)
    recommended_strategy: list[str] = field(default_factory=list)
    forbidden_edits: list[str] = field(default_factory=list)
    nl_grounding_hints: list[str] = field(default_factory=list)
    target_element_ids: list[str] = field(default_factory=list)
    required_preserve_element_ids: list[str] = field(default_factory=list)
    allowed_edit_kinds: list[str] = field(default_factory=list)
    verification_plan: list[str] = field(default_factory=list)
    max_edit_scope: str = ""
    before_dsl_hash: str = ""

    def __post_init__(self) -> None:
        self.target = _require_one_of(
            self.target,
            {"parse", "semantic", "design", "sim", "model_review"},
            "FixPlan.target",
        )
        self.severity = _require_one_of(
            self.severity,
            {"error", "blocking_warning", "advisory_warning", "review_fail", "sim_fail"},
            "FixPlan.severity",
        )


@dataclass
class RepairRejection:
    """Evidence explaining why a repaired candidate was rejected."""

    rejected_by_stage: str
    reason: str
    target_resolved: bool = False
    regression_detected: bool = False
    drift_risk: Literal["none", "minor", "major"] = "none"
    evidence: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.target_resolved = _coerce_bool(self.target_resolved, "RepairRejection.target_resolved")
        self.regression_detected = _coerce_bool(self.regression_detected, "RepairRejection.regression_detected")
        self.drift_risk = _require_one_of(
            self.drift_risk,
            {"none", "minor", "major"},
            "RepairRejection.drift_risk",
        )


@dataclass
class RevisedFixPlan:
    """Second-pass repair input = original plan plus rejection evidence."""

    original: FixPlan
    rejection: RepairRejection
    revision_count: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.revision_count, int) or isinstance(self.revision_count, bool):
            raise TypeError("RevisedFixPlan.revision_count must be an int")
        if self.revision_count < 0:
            raise ValueError("RevisedFixPlan.revision_count must be >= 0")
        self.original = _coerce_nested_dataclass(self.original, FixPlan)
        self.rejection = _coerce_nested_dataclass(self.rejection, RepairRejection)


@dataclass
class FeedbackBundle:
    """Feedback signals for one round of an agent loop iteration.

    The loop driver uses ``all_ok`` to decide whether to keep iterating. In
    strict PR-0 mode, ``enabled_sources`` plus ``stage_results`` define the
    authority boundary: enabled stage outputs and their nested feedback
    ``meta`` entries must describe the same execution fact, and any enabled
    blocking stage meta makes the bundle non-ok.
    """

    parse: Optional[ParseFeedback] = None
    semantic: Optional[SemanticFeedback] = None
    sim: Optional[SimFeedback] = None
    judge: Optional[JudgeFeedback] = None
    design: Optional[DesignFeedback] = None
    model_review: Optional[ModelReviewFeedback] = None
    repair_review: Optional[RepairReviewFeedback] = None
    enabled_sources: list[str] = field(default_factory=list)
    stage_results: list[StageResultMeta] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.parse = _coerce_nested_dataclass(self.parse, ParseFeedback)
        self.semantic = _coerce_nested_dataclass(self.semantic, SemanticFeedback)
        self.sim = _coerce_nested_dataclass(self.sim, SimFeedback)
        self.judge = _coerce_nested_dataclass(self.judge, JudgeFeedback)
        self.design = _coerce_nested_dataclass(self.design, DesignFeedback)
        self.model_review = _coerce_nested_dataclass(self.model_review, ModelReviewFeedback)
        self.repair_review = _coerce_nested_dataclass(self.repair_review, RepairReviewFeedback)
        self.stage_results = _coerce_dataclass_list(self.stage_results, StageResultMeta)

    @property
    def all_ok(self) -> bool:
        """True iff the configured feedback contract is satisfied.

        Backward-compatible mode: when ``enabled_sources`` is empty, only
        non-None feedback objects are inspected and stage meta is not required.

        PR-0 contract mode: when ``enabled_sources`` is non-empty, only those
        sources are authoritative.  Non-enabled feedback objects are ignored,
        every enabled source must have an output object, and every enabled
        source with a canonical ``SD/SL`` feedback stage must also have a
        passing ``StageResultMeta`` row.
        """
        if not self.enabled_sources:
            return all(src.ok for src in self._feedback_values() if src is not None)

        return not self.stage_contract_errors()

    def has_any_signal(self) -> bool:
        return any(src is not None for src in self._feedback_values())

    def _feedback_values(self) -> tuple[Any, ...]:
        return (
            self.parse,
            self.semantic,
            self.design,
            self.sim,
            self.judge,
            self.model_review,
            self.repair_review,
        )

    def _source_value(self, source: str) -> Any:
        return getattr(self, source, None)

    def _stage_meta_by_id(self) -> dict[str, StageResultMeta]:
        """Current feedback-round stage meta rows keyed by ``stage_id``.

        ``FeedbackBundle.stage_results`` is the authoritative meta set for the
        current feedback bundle.  ``IterTrace.stage_results`` persists the same
        information at iteration granularity for run-record/audit consumers.
        """
        return {meta.stage_id: meta for meta in self.stage_results}

    @staticmethod
    def _meta_conflict_fields(left: StageResultMeta, right: StageResultMeta) -> list[str]:
        """Return core fields whose mismatch means two meta rows conflict."""
        fields_to_compare = (
            "stage_id",
            "stage_kind",
            "enabled",
            "ran",
            "status",
            "ok",
            "skipped_reason",
            "stage_error",
            "output_validation_error",
            "input_hash",
            "output_hash",
            "prompt_hash",
        )
        return [
            field_name
            for field_name in fields_to_compare
            if getattr(left, field_name) != getattr(right, field_name)
        ]

    def _expected_stage_meta_for_source(self, source: str) -> tuple[str, StageResultMeta | None, bool]:
        """Resolve and validate the canonical stage meta bound to a feedback source.

        Returns ``(stage_id, meta, uses_nested)`` where ``meta`` is selected
        only when its ``stage_id`` exactly equals the source's canonical stage.
        Nested feedback ``meta`` is allowed for feedback dataclasses that carry
        it, but it is never allowed to satisfy a different enabled stage.
        """
        stage_id = FEEDBACK_SOURCE_TO_STAGE_ID[source]
        stage_meta = self._stage_meta_by_id().get(stage_id)
        feedback = self._source_value(source)
        nested_meta = getattr(feedback, "meta", None) if feedback is not None and hasattr(feedback, "meta") else None
        if stage_meta is not None:
            return stage_id, stage_meta, False
        if nested_meta is not None and nested_meta.stage_id == stage_id:
            return stage_id, nested_meta, True
        return stage_id, None, False

    def missing_enabled_sources(self) -> list[str]:
        """Enabled feedback sources that do not have an output object yet."""
        return [source for source in self.enabled_sources if self._source_value(source) is None]

    def missing_enabled_stage_metas(self) -> list[str]:
        """Canonical stage IDs missing valid meta rows for enabled feedback sources."""
        missing: list[str] = []
        for source in self.enabled_sources:
            if source not in FEEDBACK_SOURCE_TO_STAGE_ID:
                continue
            stage_id, meta, _uses_nested = self._expected_stage_meta_for_source(source)
            if meta is None:
                missing.append(stage_id)
        return missing

    def stage_contract_errors(self) -> list[str]:
        """Human-readable stage contract errors for PR-0 tests/review."""
        errors: list[str] = []
        stage_counts: dict[str, int] = {}
        for meta in self.stage_results:
            stage_counts[meta.stage_id] = stage_counts.get(meta.stage_id, 0) + 1
            errors.extend(f"{meta.stage_id}: {error}" for error in meta.contract_errors())
            if meta.enabled and meta.blocks_all_ok:
                errors.append(f"stage meta blocks all_ok: {meta.stage_id} status={meta.status.value} ok={meta.ok}")
        for stage_id, count in stage_counts.items():
            if count > 1:
                errors.append(f"duplicate stage meta: {stage_id}")

        for source in self.enabled_sources:
            if source not in FeedbackSource._value2member_map_:
                errors.append(f"unknown enabled source: {source}")

            feedback = self._source_value(source)
            if feedback is None:
                errors.append(f"enabled source missing feedback: {source}")
                continue
            if not getattr(feedback, "ok", False):
                errors.append(f"enabled source not ok: {source}")
            if source == FeedbackSource.MODEL_REVIEW.value and getattr(feedback, "review_meta", None) is None:
                errors.append(f"enabled source missing review_meta: {source}")
            if (
                source == FeedbackSource.REPAIR_REVIEW.value
                and getattr(feedback, "delta_review", None) is not None
                and getattr(feedback, "review_meta", None) is None
            ):
                errors.append(f"enabled source missing review_meta: {source}")

            if hasattr(feedback, "meta"):
                nested_meta = getattr(feedback, "meta")
                if nested_meta is None:
                    errors.append(f"enabled source missing nested meta: {source}")
                else:
                    errors.extend(f"{source}.meta/{nested_meta.stage_id}: {error}" for error in nested_meta.contract_errors())
                    expected_stage_id = FEEDBACK_SOURCE_TO_STAGE_ID.get(source)
                    if expected_stage_id is not None and nested_meta.stage_id != expected_stage_id:
                        errors.append(
                            f"enabled source nested meta stage mismatch: {source} "
                            f"expected {expected_stage_id}, got {nested_meta.stage_id}"
                        )
                    if expected_stage_id is not None and not nested_meta.enabled:
                        errors.append(f"enabled source nested meta disabled: {source}/{expected_stage_id}")
                    if expected_stage_id is not None and nested_meta.blocks_all_ok:
                        errors.append(
                            f"enabled source nested meta blocks all_ok: "
                            f"{source}/{expected_stage_id} status={nested_meta.status.value} ok={nested_meta.ok}"
                        )
                    stage_meta = self._stage_meta_by_id().get(expected_stage_id) if expected_stage_id else None
                    if stage_meta is not None and expected_stage_id is not None:
                        conflicts = self._meta_conflict_fields(stage_meta, nested_meta)
                        if conflicts:
                            errors.append(
                                f"conflicting stage meta for {source}/{expected_stage_id}: "
                                f"fields={','.join(conflicts)}"
                            )

        for source in self.enabled_sources:
            if source not in FEEDBACK_SOURCE_TO_STAGE_ID:
                continue
            stage_id, meta, _uses_nested = self._expected_stage_meta_for_source(source)
            if meta is None:
                errors.append(f"enabled source missing stage meta: {stage_id}")
                continue
            if not meta.enabled:
                errors.append(f"enabled source stage meta disabled: {stage_id}")
            if meta.blocks_all_ok:
                errors.append(f"enabled source stage meta blocks all_ok: {stage_id} status={meta.status.value} ok={meta.ok}")

        return errors


# ---------------------------------------------------------------------------
# Iteration trace + final result
# ---------------------------------------------------------------------------


@dataclass
class IterTrace:
    """One iteration of the agent loop: (model, feedback, repair)."""

    iteration: int = 0
    model: Optional[ModelArtifact] = None
    feedback: Optional[FeedbackBundle] = None
    repair: Optional[ModelArtifact] = None
    repair_skipped: bool = False  # True if feedback.all_ok and we early-exit
    stage_results: list[StageResultMeta] = field(default_factory=list)
    stage_context_summary: dict[str, Any] = field(default_factory=dict)
    warning_budget_state: dict[str, BudgetState] = field(default_factory=dict)
    scenario_epoch: Optional[int] = None
    repair_review: Optional[RepairReviewFeedback] = None

    def __post_init__(self) -> None:
        self.feedback = _coerce_nested_dataclass(self.feedback, FeedbackBundle)
        self.stage_results = _coerce_dataclass_list(self.stage_results, StageResultMeta)
        self.warning_budget_state = _coerce_dataclass_dict(self.warning_budget_state, BudgetState)
        self.repair_review = _coerce_nested_dataclass(self.repair_review, RepairReviewFeedback)


StatusLiteral = Literal[
    "converged",          # all 4 feedback ok before n_iter exhausted
    "not_converged",      # n_iter exhausted, some feedback still failing
    "parse_failed_all",   # parse never succeeded across all iters
    "api_failed",         # LLM API failed (5xx, rate limit, etc.)
    "spec_failed",        # SpecExtractor failed to produce valid JSON
    "ok_no_loop",         # A0 condition: spec → model, no feedback/repair
    "contract_only",      # PR-A façade: config/stage graph contract only
]


@dataclass
class AgentLoopResult:
    """Final output of ``run_agent_loop``.

    Path 1 / Path 2 run scripts persist this (one row per sample) into a
    parquet file under ``reproduction/results/sprint_pathX/predictions.parquet``.
    """

    final_dsl: str = ""
    final_artifact: Optional[ModelArtifact] = None
    spec: Optional[SpecJson] = None
    iter_traces: list[IterTrace] = field(default_factory=list)
    token_usage: dict[str, int] = field(default_factory=lambda: {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "n_calls": 0,
    })
    status: StatusLiteral = "ok_no_loop"
    final_feedback: Optional[FeedbackBundle] = None
    error_message: Optional[str] = None
    llm_model: Optional[str] = None  # the model actually used (from env or override)
    run_record_path: Optional[str] = None
    run_record_id: Optional[str] = None
    # Phase E v3 (f): per-retry coverage report from scenariogen self-validation.
    # Each element is the {mutation_name: {status, n_variants, ...}} dict for
    # one scenariogen attempt (index 0 = initial gen, 1+ = targeted retries).
    scenariogen_coverage: list[dict] = field(default_factory=list)
    resolved_config: dict[str, Any] = field(default_factory=dict)
    planned_stage_graph: dict[str, Any] = field(default_factory=dict)


@dataclass
class StageContextSummary:
    """Persistable summary of the loop-internal StageContext.

    This intentionally avoids storing pyfcstm runtime/model objects directly.
    """

    current_dsl_hash: str = ""
    has_ast: bool = False
    has_model: bool = False
    inspect_hash: Optional[str] = None
    grounding_hash: Optional[str] = None
    scenario_set_id: Optional[str] = None
    warning_budget_keys: list[str] = field(default_factory=list)


@dataclass
class StageContext:
    """Loop-internal working state shared by SD/SL stages.

    This object may contain non-serializable pyfcstm AST/model/runtime objects.
    Persisted artifacts must use ``to_summary()`` plus explicit stage records
    and ``AgentLoopRunRecord`` payloads instead of serializing this object
    wholesale.
    """

    nl: str = ""
    current_dsl: str = ""
    ast: Any | None = None
    model: Any | None = None
    inspect_json: dict[str, Any] | None = None
    grounding_map: GroundingMap | None = None
    scenario_set: ScenarioSet | None = None
    warning_budget_state: dict[str, BudgetState] = field(default_factory=dict)
    stage_results: list[StageResultMeta] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.grounding_map = _coerce_nested_dataclass(self.grounding_map, GroundingMap)
        self.scenario_set = _coerce_nested_dataclass(self.scenario_set, ScenarioSet)
        self.warning_budget_state = _coerce_dataclass_dict(self.warning_budget_state, BudgetState)
        self.stage_results = _coerce_dataclass_list(self.stage_results, StageResultMeta)

    def to_summary(self) -> StageContextSummary:
        return StageContextSummary(
            current_dsl_hash=self._hash_placeholder(self.current_dsl),
            has_ast=self.ast is not None,
            has_model=self.model is not None,
            inspect_hash=self._hash_placeholder(self.inspect_json),
            grounding_hash=self._hash_placeholder(self.grounding_map),
            scenario_set_id=self.scenario_set.scenario_set_id if self.scenario_set else None,
            warning_budget_keys=sorted(self.warning_budget_state.keys()),
        )

    @staticmethod
    def _hash_placeholder(value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, str) and not value:
            return ""
        return "sha256:<computed-by-runner>"


@dataclass
class AgentLoopRunRecord:
    """Self-contained single-file audit/replay record for one agent-loop run."""

    schema_version: str
    run_id: str
    created_at: str
    status: Literal["success", "failed", "rejected", "budget_exhausted", "error", "invalid", "contract_only"]
    input_bundle: dict[str, Any]
    run_config: dict[str, Any]
    environment: dict[str, Any]
    stage_graph: dict[str, Any]
    stage_records: list[dict[str, Any]]
    iteration_records: list[dict[str, Any]]
    llm_interactions: list[dict[str, Any]] = field(default_factory=list)
    deterministic_feedback: dict[str, Any] = field(default_factory=dict)
    repair_history: list[dict[str, Any]] = field(default_factory=list)
    scenario_history: list[dict[str, Any]] = field(default_factory=list)
    final_artifacts: dict[str, Any] = field(default_factory=dict)
    logs: list[dict[str, Any]] = field(default_factory=list)
    replay_index: dict[str, Any] = field(default_factory=dict)
    redaction_report: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.status = _require_one_of(
            self.status,
            {"success", "failed", "rejected", "budget_exhausted", "error", "invalid", "contract_only"},
            "AgentLoopRunRecord.status",
        )
        stage_metas = _coerce_dataclass_list(self.stage_records, StageResultMeta)
        for meta in stage_metas:
            errors = meta.contract_errors()
            if errors:
                raise ValueError(f"AgentLoopRunRecord.stage_records invalid {meta.stage_id}: {'; '.join(errors)}")
