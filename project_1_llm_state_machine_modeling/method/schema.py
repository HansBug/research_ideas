"""Core dataclass schema for the agent loop.

All structured data flowing between the three LLM agents (SpecExtractor /
Modeler / Repair) and the four feedback sources (parse / semantic / sim /
judge) is typed via the dataclasses below. Path 1 / Path 2 run scripts and the
final report writers consume these as the single source of truth.

Design choices:

- Pure stdlib ``dataclasses`` (no pydantic / attrs) to keep the dependency
  surface minimal. Submodule-style sprint code should not pull in heavyweight
  frameworks.
- All "feedback" classes carry an ``ok: bool`` field so the loop driver can do
  fast cascade checks (parse_ok -> sem_ok -> sim_ok -> judge).
- ``IterTrace`` captures one round (model output + 4 feedback bundles + repair
  output) for full reconstructability of the agent loop trajectory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Optional


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
        through ``"A4"`` (full agent loop with all 4 feedback sources, n_iter=3).
        Path 1 uses A0_strong (external baseline replication) + A4_ours.
        Path 2 uses A0_baseline + A4_ours.
    n_iter
        Maximum number of (feedback → repair) iterations. ``0`` skips the
        feedback/repair phase entirely. The loop may exit early if all
        feedback sources return ``ok=True``.
    feedback_sources
        List of feedback channels to run, in cascade order. Allowed values:
        ``"parse"``, ``"semantic"``, ``"sim"``, ``"judge"``. Empty list = A0.
    llm_model
        Override the default ``LLM_MODEL`` env var. ``None`` => use env.
    seed
        Optional integer seed for LLM-call determinism (some providers honor
        this).
    """

    condition: ConditionLiteral = "A4"
    n_iter: int = 3
    feedback_sources: list[str] = field(default_factory=lambda: ["parse", "semantic", "sim", "judge"])
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
# Feedback sources
# ---------------------------------------------------------------------------


@dataclass
class ParseFeedback:
    """Output of ``pyfcstm.dsl.parse_with_grammar_entry``."""

    ok: bool = False
    line: Optional[int] = None
    col: Optional[int] = None
    expected_tokens: list[str] = field(default_factory=list)
    got: Optional[str] = None
    snippet: Optional[str] = None
    error_class: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class SemanticFeedback:
    """Output of ``pyfcstm.model.parse_dsl_node_to_state_machine``.

    ``ok=True`` iff AST → state-machine model conversion succeeded with no
    diagnostics. ``missing_states`` / ``dangling_transitions`` / ``undefined_vars``
    / ``type_mismatches`` are populated based on the exception inspector.
    """

    ok: bool = False
    missing_states: list[str] = field(default_factory=list)
    dangling_transitions: list[dict[str, Any]] = field(default_factory=list)
    undefined_vars: list[str] = field(default_factory=list)
    type_mismatches: list[dict[str, Any]] = field(default_factory=list)
    error_class: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class SimFeedback:
    """Output of ``pyfcstm.simulate.SimulationRuntime`` execution.

    ``ok=True`` iff at least one full cycle ran without triggering safety limits
    (1000 steps / 64 stack depth) and without ``SimulationRuntimeDfsError``.
    """

    ok: bool = False
    cycles_completed: int = 0
    unreachable_states: list[str] = field(default_factory=list)
    deadlocks: list[dict[str, Any]] = field(default_factory=list)
    safety_limit_hit: bool = False
    dfs_error_class: Optional[str] = None
    dfs_error_message: Optional[str] = None
    witness_path: list[str] = field(default_factory=list)
    reach_rate: float = 0.0  # fraction of defined states reachable from initial


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
class FeedbackBundle:
    """All 4 feedback signals for one round of an agent loop iteration.

    The loop driver uses ``all_ok`` to decide whether to keep iterating.
    Cascade order: parse → semantic → sim → judge. If any earlier source
    returns ``ok=False`` and ``stop_on_first_fail=True``, downstream sources
    may be skipped (configured in loop.py).
    """

    parse: Optional[ParseFeedback] = None
    semantic: Optional[SemanticFeedback] = None
    sim: Optional[SimFeedback] = None
    judge: Optional[JudgeFeedback] = None

    @property
    def all_ok(self) -> bool:
        """True iff every non-None source reports ``ok``."""
        for src in (self.parse, self.semantic, self.sim, self.judge):
            if src is not None and not src.ok:
                return False
        return True

    def has_any_signal(self) -> bool:
        return any(src is not None for src in (self.parse, self.semantic, self.sim, self.judge))


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
