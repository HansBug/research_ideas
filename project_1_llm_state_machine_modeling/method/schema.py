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


# ---------------------------------------------------------------------------
# LoopConfig — user-facing configuration
# ---------------------------------------------------------------------------

ConditionLiteral = Literal["A0", "A1", "A2", "A3", "A4"]


@dataclass
class LoopConfig:
    """Top-level config for one ``run_agent_loop`` call.

    Attributes
    ----------
    condition
        One of ``"A0"`` (single-prompt baseline, n_iter=1, feedback_sources=[])
        through ``"A4"`` (full agent loop with feedback sources, n_iter=3).
        Path 1 uses A0_strong (external baseline replication) + A4_ours.
        Path 2 uses A0_baseline + A4_ours.
    n_iter
        Maximum number of (feedback → repair) iterations. ``0`` skips the
        feedback/repair phase entirely. The loop may exit early if all
        feedback sources return ``ok=True``.
    feedback_sources
        List of feedback channels to run, in cascade/contract order. Allowed
        values are defined by ``FeedbackSource``: ``"parse"``, ``"semantic"``,
        ``"design"``, ``"sim"``, ``"judge"``, ``"model_review"``,
        ``"repair_review"``. Empty list = A0.
    llm_model
        Override the default ``LLM_MODEL`` env var. ``None`` => use env.
    seed
        Optional integer seed for LLM-call determinism (some providers honor
        this).
    """

    condition: ConditionLiteral = "A4"
    n_iter: int = 3
    feedback_sources: list[str] = field(default_factory=lambda: ["parse", "semantic", "sim", "judge"])
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
        if isinstance(self.stage_kind, str):
            self.stage_kind = StageKind(self.stage_kind)
        if isinstance(self.status, str):
            self.status = StageStatus(self.status)

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


@dataclass
class ScenarioResult:
    """Per-scenario aggregate result (collects all step results + overall status)."""

    name: str = ""
    description: str = ""
    status: StepStatusLiteral = "pass"  # pass if all steps pass; fail if any step fail (no error); error if any step error
    step_results: list[StepResult] = field(default_factory=list)
    setup_error: Optional[str] = None  # SimulationRuntime construction failed (e.g. bad initial_state)


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
    meta: Optional[StageResultMeta] = None

    def __post_init__(self) -> None:
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


@dataclass
class GroundingMap:
    """NL/spec provenance map consumed by repair and repair-review stages."""

    elements: list[GroundedElement] = field(default_factory=list)
    source_summary: dict[str, str] = field(default_factory=dict)


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


@dataclass
class RepairRejection:
    """Evidence explaining why a repaired candidate was rejected."""

    rejected_by_stage: str
    reason: str
    target_resolved: bool = False
    regression_detected: bool = False
    drift_risk: Literal["none", "minor", "major"] = "none"
    evidence: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RevisedFixPlan:
    """Second-pass repair input = original plan plus rejection evidence."""

    original: FixPlan
    rejection: RepairRejection
    revision_count: int = 0


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


StatusLiteral = Literal[
    "converged",          # all 4 feedback ok before n_iter exhausted
    "not_converged",      # n_iter exhausted, some feedback still failing
    "parse_failed_all",   # parse never succeeded across all iters
    "api_failed",         # LLM API failed (5xx, rate limit, etc.)
    "spec_failed",        # SpecExtractor failed to produce valid JSON
    "ok_no_loop",         # A0 condition: spec → model, no feedback/repair
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
    status: Literal["success", "failed", "rejected", "budget_exhausted", "error"]
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
