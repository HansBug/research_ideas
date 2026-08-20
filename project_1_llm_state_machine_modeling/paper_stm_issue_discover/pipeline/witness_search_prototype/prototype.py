"""Source-aware executable-evidence prototype for paper1.

LLMs extract NL contracts, propose backend-independent semantic goals, and
adjudicate D once per pair. All model evaluation and W/L classification are
deterministic and replayable. The ledger is absent from runtime imports/inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, ValidationError


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists() and (candidate / "utils" / "llm").is_dir():
            return candidate
    raise RuntimeError(f"cannot locate repository root from {start}")


HERE = Path(__file__).resolve().parent
REPO_ROOT = _find_repo_root(HERE)
PAPER_ROOT = HERE.parents[1]
DEFAULT_REPORT_ROOT = (
    PAPER_ROOT / "pipeline" / "representation" / "reports" / "llms_emp_r45_java_60"
)
FEEDBACK_SRC = PAPER_ROOT / "pipeline" / "feedback_loop" / "src"
for path in (REPO_ROOT, FEEDBACK_SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from paper_stm_feedback_loop.assertions import (
    build_eval_environment,
    parse_assertion_script,
)
from paper_stm_feedback_loop.discover.responder import (
    DEFAULT_TRANSPORT_RETRIES,
    DirectStructuredResponder,
)

from project_1_llm_state_machine_modeling.paper_stm_issue_discover.pipeline.witness_search_prototype.guard_solver import (
    UnsupportedGuard,
    pairwise_overlaps,
)
from project_1_llm_state_machine_modeling.paper_stm_issue_discover.pipeline.witness_search_prototype.uml_transition_profile import (
    PROFILE_ID as UML_GUARD_ONLY_PROFILE_ID,
)
from project_1_llm_state_machine_modeling.paper_stm_issue_discover.pipeline.witness_search_prototype.uml_transition_profile import (
    GuardOnlyLabel,
    parse_guard_only_label,
)

ProofTemplate = Literal[
    "T01_initial_contract",
    "T02_inventory_effect",
    "T03_transition_contract",
    "T04_containment_contract",
    "T05_label_semantics",
    "T06_guard_determinism",
    "T07_topology_entry",
    "T08_reachable_then_escapable",
    "T09_reachability_certificate",
    "T10_stable_termination",
    "T11_wrong_target_after_event",
    "T12_event_response",
    "T13_transition_target_consistency",
]

GoalRelation = Literal[
    "initial_target",
    "state_exists",
    "final_pseudostate_exists",
    "variable_exists",
    "event_exists",
    "action_exists",
    "effect_exists",
    "transition_contract",
    "transition_exists",
    "transition_absent",
    "transition_target_consistency",
    "completion_transition_fireable",
    "contained_in",
    "child_count",
    "guard_present",
    "guards_distinguishable",
    "target_reachable",
    "state_escapable",
    "event_reaches_target",
    "event_avoids_scope",
    "event_consumed",
    "event_consumed_in_scope",
    "eventually_responds",
    "termination_target",
    "eventually_terminates",
]


class ElementObligation(BaseModel):
    """Typed obligation about declaration, absence, kind, or cardinality."""

    family: Literal["element"] = Field(
        default="element", description="Discriminator for the element obligation family."
    )
    element_kind: Literal[
        "state",
        "final_pseudostate",
        "event",
        "variable",
        "action",
        "effect",
        "transition",
    ] = Field(description="Formal element kind selected by semantic grounding.")
    operator: Literal["exists", "absent", "kind_is", "cardinality"] = Field(
        description="Exact typed operation; it is lowered by the compiler, not interpreted from prose."
    )
    subject_ref: str | None = Field(
        default=None, description="Exact source/FCSTM element identifier, when applicable."
    )
    expected_kind: str | None = Field(
        default=None, description="Expected formal kind for a kind_is obligation."
    )
    expected_count: int | None = Field(
        default=None, ge=0, le=128, description="Exact expected cardinality for a cardinality obligation."
    )


class AttachmentObligation(BaseModel):
    """Typed obligation about how exact formal elements are connected."""

    family: Literal["attachment"] = Field(
        default="attachment", description="Discriminator for the attachment obligation family."
    )
    attachment: Literal[
        "containment",
        "initial_target",
        "transition_endpoints",
        "transition_target_consistency",
        "trigger",
        "guard",
        "effect",
        "action_phase",
    ] = Field(description="Formal attachment relation to inspect."
    )
    subject_ref: str | None = Field(
        default=None, description="Exact transition or element ID being checked."
    )
    owner_ref: str | None = Field(
        default=None, description="Exact owning state/scope ID, when required."
    )
    reference_ref: str | None = Field(
        default=None, description="Exact comparison/reference transition ID, when required."
    )
    action_ref: str | None = Field(
        default=None, description="Exact lifecycle action identity, when the attachment is action_phase."
    )
    phase: Literal["entry", "exit", "during"] | None = Field(
        default=None,
        description=(
            "Exact lifecycle phase when the requirement fixes one; null means "
            "that the named action may be attached to any lifecycle phase."
        ),
    )
    expected: bool = Field(
        default=True, description="Required truth value of the typed attachment relation."
    )


class GuardConditionBinding(BaseModel):
    """Explicit semantic bridge from one authored label to a formal guard expression.

    The transition ID and source label are checked against the canonical source
    artifact before parsing. The compiler never decides that an ordinary event
    or action label is a guard merely because its text resembles an expression.
    """

    transition_id: str = Field(
        min_length=1,
        max_length=160,
        description="Exact authored transition ID whose label is semantically a guard condition.",
    )
    source_label: str = Field(
        min_length=1,
        max_length=800,
        description=(
            "Exact raw source label copied from the selected transition; it is "
            "compared structurally before formal guard parsing."
        ),
    )
    semantic_role: Literal["guard_condition"] = Field(
        description=(
            "LLM semantic declaration that this exact source label is a guard "
            "condition rather than an event, action, or display label."
        ),
    )


class GuardSetObligation(BaseModel):
    """Typed obligation over a semantically selected set of outgoing transitions."""

    family: Literal["guard_set"] = Field(
        default="guard_set", description="Discriminator for the guard-set obligation family."
    )
    property: Literal["satisfiable", "disjoint", "complete", "equivalent", "implies"] = Field(
        description="Formal relation to evaluate over the selected transition guards."
    )
    scope_ref: str | None = Field(
        default=None, description="Exact source scope whose outgoing set is under analysis."
    )
    transition_refs: list[str] = Field(
        default_factory=list,
        description="Exact authored transition IDs selected by semantic grounding; never inferred by text matching.",
    )
    guard_bindings: list[GuardConditionBinding] = Field(
        default_factory=list,
        description=(
            "Fresh candidates must supply one binding per transition_ref. The "
            "compiler requires an exact source-label match and then parses that "
            "formal expression; missing bindings degrade the goal to W1."
        ),
    )
    expected: bool = Field(
        default=True, description="Required truth value of the guard-set property."
    )


class GraphObligation(BaseModel):
    """Typed topology obligation evaluated over the canonical state graph."""

    family: Literal["graph"] = Field(
        default="graph", description="Discriminator for the graph obligation family."
    )
    property: Literal[
        "reachable",
        # ``target_reachable`` is a typed vocabulary alias emitted by some
        # models for the same unbounded graph reachability operator. It is
        # normalized at the typed lowering boundary, never inferred from prose.
        "target_reachable",
        "escapable",
        "deadlock_free",
        "stable_termination",
        "path_absent",
        "event_target_reachable",
        "event_consumer_reachable",
    ] = Field(description="Graph property to evaluate with the registered topology backend.")
    source_ref: str | None = Field(
        default=None, description="Exact source state/scope ID, when the property has a source."
    )
    target_ref: str | None = Field(
        default=None, description="Exact target state/scope ID, when the property has a target."
    )
    forbidden_scope_ref: str | None = Field(
        default=None, description="Exact scope that a certified path must avoid."
    )
    bound: int | None = Field(
        default=None, ge=1, le=16, description="Optional bounded-trace limit; unsupported bounds remain W1."
    )
    expected: bool = Field(
        default=True, description="Required truth value of the graph property."
    )


class TemporalObligation(BaseModel):
    """Typed temporal-pattern obligation reserved for registered trace operators."""

    family: Literal["temporal"] = Field(
        default="temporal", description="Discriminator for the temporal obligation family."
    )
    pattern: Literal[
        "response",
        "precedence",
        "existence",
        "absence",
        "universality",
        "termination",
        "persistence",
    ] = Field(description="Temporal pattern whose semantics are defined by the registered backend."
    )
    scope: Literal["global", "before", "after", "between", "after_until"] = Field(
        default="global", description="Temporal scope of the pattern."
    )
    trigger_ref: str | None = Field(default=None, description="Exact trigger/event identity, when applicable.")
    response_ref: str | None = Field(default=None, description="Exact response identity, when applicable.")
    state_ref: str | None = Field(default=None, description="Exact state identity, when applicable.")
    scope_ref: str | None = Field(default=None, description="Exact state-machine scope, when applicable.")
    bound: int | None = Field(
        default=None, ge=1, le=16, description="Optional bounded trace horizon."
    )
    expected: bool = Field(default=True, description="Required truth value of the temporal property.")


DomainObligation = Annotated[
    ElementObligation
    | AttachmentObligation
    | GuardSetObligation
    | GraphObligation
    | TemporalObligation,
    Field(discriminator="family"),
]

ObligationSurfaceRole = Literal[
    "core",
    "derived_macro",
    "backend_comparison",
    "under_supported_extension",
]


class SupportDisposition(BaseModel):
    """Compiler-derived support metadata; never invent a domain verdict from it."""

    status: Literal["executable", "located_only", "prose_only"] = Field(
        description="Whether the typed obligation has a registered executable lowering."
    )
    w_ceiling: Literal["W2", "W1", "W0"] = Field(
        description="Maximum witness level allowed by the available formal support."
    )
    surface_role: ObligationSurfaceRole | Literal["legacy_untyped"] = Field(
        description="Role of this obligation surface in the preregistered method."
    )
    reason_code: Literal[
        "sound_lowering_available",
        "no_sound_lowering",
        "legacy_replay",
    ] = Field(description="Machine-readable reason for the support disposition.")
    reason: str = Field(description="Short audit explanation; it is not a semantic finding.")


ProbeKind = Literal[
    "state_declared",
    "variable_declared",
    "event_declared",
    "containment",
    "initial_target",
    "edge_declared",
    "effect_declared",
    "action_declared",
    "guard_distinguishable",
    "cardinality",
    "reaches",
    "terminates",
    "occupancy_after",
    "event_consumed",
    "stays_in",
    "variable_delta_after",
    "invariant",
    "response_within",
    "persists_until",
]

DLevel = Literal["D2", "D1", "D0"]
DSubclass = Literal["D2-lit", "D2-impl", "D2-norm", "not_applicable"]
SemanticBindingAuthority = Literal[
    "paper1_discovery_grounding_llm",
    "paper1_semantic_grounding_llm",
    "paper1_evidence_planning_llm",
    "formal_source_ast",
    "formal_pyfcstm_diagnostic",
]

EXECUTABLE_ASSERTION_MESSAGE = "paper1 formal evidence assertion failed"


class ProbeCheck(BaseModel):
    """One typed executable check.

    Optional fields are checked by the deterministic compiler. Keeping that
    check outside schema validation lets a malformed item degrade without
    killing the pair.
    """

    role: Literal["precondition", "primary"] = Field(
        default="primary", description="Whether this check establishes a prerequisite or tests the claim."
    )
    kind: ProbeKind | None = Field(default=None, description="Registered executable predicate shape.")
    source: str | None = Field(default=None, description="Exact formal source binding, when applicable.")
    trigger: str | None = Field(default=None, description="Exact event/trigger binding, when applicable.")
    target: str | None = Field(default=None, description="Exact formal target binding, when applicable.")
    within_cycles: int | None = Field(
        default=None, ge=1, le=16, description="Optional bounded execution horizon."
    )
    expected: bool = Field(default=True, description="Expected boolean result of this check.")
    bindings: dict[str, str | int | float | bool] = Field(
        default_factory=dict,
        description="Explicit predicate arguments; the compiler validates their signature exactly.",
    )


class ProbeCandidate(BaseModel):
    """Legacy executable candidate retained for replay and deterministic scouts."""

    obligation: str = Field(default="", description="Human-readable obligation under test.")
    claim: str = Field(min_length=1, description="Localized issue hypothesis to test.")
    basis_kind: Literal["nl_literal", "implicit_oracle", "domain_norm"] = Field(
        description="Provenance class of the obligation basis."
    )
    nl_quote: str | None = Field(default=None, description="Verbatim NL evidence span, when applicable.")
    priority: int = Field(ge=1, le=5, description="Semantic priority assigned by the planning stage.")
    locations: list[str] = Field(
        default_factory=list, description="Exact source, FCSTM, or formal locations supporting localization."
    )
    broad_candidate_ids: list[str] = Field(
        default_factory=list, max_length=3, description="IDs of broad hypotheses refined by this candidate."
    )
    probe_seed_ids: list[str] = Field(
        default_factory=list, max_length=3, description="Deterministic scout seed IDs used as localization clues."
    )
    checks: list[ProbeCheck] = Field(
        default_factory=list, max_length=2, description="At most two typed executable checks."
    )


class ProbePlan(BaseModel):
    """Bounded collection of legacy candidates passed to the predicate executor."""

    candidates: list[ProbeCandidate] = Field(
        max_length=4, description="Candidates to execute independently; one malformed item cannot erase peers."
    )


class EvidenceGoal(BaseModel):
    """Backend-independent semantic goal emitted by the LLM.

    The compiler checks relation-specific required fields. They remain optional
    here so one malformed goal degrades to W1 instead of killing the pair.
    """

    relation: GoalRelation = Field(
        description="Semantic relation to compile; choose only from the registered goal surface."
    )
    observed_transition_id: str | None = Field(
        default=None, description="Exact authored transition ID selected by semantic grounding."
    )
    reference_transition_id: str | None = Field(
        default=None, description="Exact comparison transition ID for a target-consistency goal."
    )
    subject: str | None = Field(default=None, description="Exact formal subject state/element ID, when applicable.")
    source: str | None = Field(default=None, description="Exact formal source state/scope ID, when applicable.")
    trigger: str | None = Field(default=None, description="Exact formal event/trigger ID, when applicable.")
    condition_role: Literal["event", "qualified_guard", "unknown"] | None = Field(
        default=None,
        description=(
            "LLM semantic classification of a normative condition: event means the "
            "condition is exactly the selected event/action; qualified_guard means "
            "the NL adds a guard/value/phase qualifier that requires an exact formal "
            "guard; unknown is fail-closed and never upgrades an unbound qualifier."
        ),
    )
    target: str | None = Field(default=None, description="Normative exact target ID, when applicable.")
    forbidden_scope: str | None = Field(
        default=None, description="Exact scope that a route must avoid, when applicable."
    )
    # Event-scope obligations retain their LLM-declared applicability and the
    # complete set of exact formal scopes.  These are formal IDs, not prose
    # hints; the executor uses them only against the source AST inventory.
    scope_applicability: Literal[
        "one_scope",
        "scope_and_descendants",
        "each_operating_mode",
    ] | None = Field(
        default=None,
        description="LLM-declared event applicability; never infer it from the number or names of states.",
    )
    required_scope_ids: list[str] = Field(
        default_factory=list,
        max_length=128,
        description="Complete exact scope-ID set required by the applicability declaration.",
    )
    response: str | None = Field(default=None, description="Exact response event/state ID, when applicable.")
    variable: str | None = Field(default=None, description="Exact formal variable ID, when applicable.")
    sign: Literal["positive", "negative", "changed"] | None = Field(
        default=None, description="Required effect direction; changed requires a registered sound operator."
    )
    phase: Literal["entry", "exit", "during"] | None = Field(
        default=None, description="Lifecycle action phase."
    )
    action: str | None = Field(
        default=None,
        description=(
            "Exact lifecycle action identity when the obligation names one. "
            "The compiler compares this value only against the structured FCSTM "
            "action inventory; it never interprets action prose."
        ),
    )
    count: int | None = Field(default=None, ge=0, le=128, description="Exact expected cardinality, when applicable.")
    condition: str | None = Field(default=None, description="Opaque formal condition supplied as a binding, not NL evidence.")
    within_cycles: int | None = Field(
        default=None, ge=1, le=16, description="Optional bounded execution horizon."
    )
    expected: bool = Field(default=True, description="Required truth value of the goal relation.")


class EvidenceCandidate(BaseModel):
    """Prompt-facing issue hypothesis paired with a typed executable goal."""

    obligation: str = Field(
        min_length=1,
        description="Requirement or domain obligation that this candidate tests.",
    )
    claim: str = Field(
        min_length=1,
        description="Localized issue hypothesis; state what may be wrong without adding unsupported facts.",
    )
    basis: str = Field(
        default="",
        max_length=1200,
        description=(
            "Concise natural-language basis for proposing this candidate: connect "
            "the cited requirement to the observed formal fact. Fresh discovery "
            "outputs must fill this field; the compiler never interprets it."
        ),
    )
    basis_kind: Literal["nl_literal", "implicit_oracle", "domain_norm"] = Field(
        description="Why the obligation is justified: exact NL, formal oracle, or explicit domain norm."
    )
    nl_quote: str | None = Field(
        default=None, description="Verbatim requirement span; it must not contain artifact conclusions."
    )
    priority: int = Field(ge=1, le=5, description="Semantic priority of the candidate.")
    locations: list[str] = Field(
        default_factory=list,
        max_length=3,
        description="Exact formal/source locations used for localization, not a semantic substitute.",
    )
    requirement_group_id: str | None = Field(
        default=None,
        pattern=r"^RG-[A-Za-z0-9_-]{1,64}$",
        description="LLM-declared semantic bundle ID for facets that must be reported together.",
    )
    proposed_l: Literal["L0", "L1", "L2"] = Field(
        description="Planner's localization suggestion; the compiler derives the final L level."
    )
    domain_obligation: DomainObligation | None = Field(
        default=None,
        description=(
            "Paper-level typed obligation for the semantic candidate. The compiler "
            "requires this field for newly proposed candidates."
        ),
    )
    goal: EvidenceGoal = Field(
        description="Typed semantic goal that the compiler may lower to an executable obligation."
    )


class EvidencePlan(BaseModel):
    """Typed candidates sent to the deterministic evidence compiler."""

    candidates: list[EvidenceCandidate] = Field(
        max_length=64, description="Independent candidates; each receives its own execution result."
    )


class BalancedEvidenceCandidate(EvidenceCandidate):
    """Issue candidate with an audit-only observed-fact summary."""

    obligation: str = Field(
        min_length=1,
        description="Requirement or domain obligation that this candidate tests.",
    )
    claim: str = Field(
        min_length=1,
        description="Localized issue hypothesis; state what may be wrong without adding unsupported facts.",
    )
    nl_quote: str | None = Field(
        default=None,
        description="Verbatim requirement span when the candidate is grounded in an explicit NL statement.",
    )
    locations: list[str] = Field(
        default_factory=list,
        description=(
            "Exact NL, source, FCSTM, or formal-ID citations. Citation count is "
            "not a semantic validity condition; output budget is enforced outside "
            "the schema."
        ),
    )
    observed_fact: str = Field(
        default="",
        description=(
            "Optional audit-only summary of the formal fact that motivated the "
            "candidate. Empty is accepted when the typed goal and basis already "
            "carry the evidence; this field is never used for compilation."
        ),
    )
    goal: EvidenceGoal = Field(
        description="Typed semantic goal that the compiler may lower to an executable obligation."
    )


class BalancedEvidencePlan(BaseModel):
    """Small bounded plan used by the complementary planning lenses."""

    surface_candidates: list[BalancedEvidenceCandidate] = Field(
        max_length=3, description="Surface candidates for structural or representation obligations."
    )
    behavior_candidates: list[BalancedEvidenceCandidate] = Field(
        max_length=3, description="Behavior candidates for executable dynamic obligations."
    )

    @property
    def candidates(self) -> list[BalancedEvidenceCandidate]:
        return [*self.surface_candidates, *self.behavior_candidates]


class SurfaceObligation(BaseModel):
    """Explicit requirement obligation that can be compiled from a typed goal."""

    obligation: str = Field(min_length=1, description="Requirement obligation stated by the extraction stage.")
    nl_quote: str = Field(min_length=1, description="Verbatim NL span supporting the obligation.")
    locations: list[str] = Field(
        default_factory=list, max_length=2, description="Exact formal/source locations for localization."
    )
    priority: int = Field(ge=1, le=5, description="Semantic priority of the obligation.")
    proposed_l: Literal["L0", "L1"] = Field(
        description="Planner localization suggestion; final L is derived after execution."
    )
    goal: EvidenceGoal = Field(
        description="Typed semantic goal for the surface obligation; do not encode a verdict in the goal."
    )

    def as_candidate(self) -> EvidenceCandidate:
        return EvidenceCandidate(
            obligation=self.obligation,
            claim=f"Executable obligation: {self.obligation}",
            basis=(
                "The contract extractor supplied this explicit natural-language "
                "obligation and its verbatim source span."
            ),
            basis_kind="nl_literal",
            nl_quote=self.nl_quote,
            priority=self.priority,
            locations=self.locations,
            proposed_l=self.proposed_l,
            goal=self.goal,
        )


class HybridEvidencePlan(BaseModel):
    """Combined surface and behavior plan used by the fixed discovery frontend."""

    surface_obligations: list[SurfaceObligation] = Field(
        max_length=12,
        description="Explicit requirement obligations reserved for structural and representation checks.",
    )
    behavior_candidates: list[BalancedEvidenceCandidate] = Field(
        max_length=3,
        description="Behavior hypotheses reserved for executable dynamic checks.",
    )

    @property
    def candidates(self) -> list[EvidenceCandidate]:
        return [
            *(item.as_candidate() for item in self.surface_obligations),
            *self.behavior_candidates,
        ]


class ExpectedTransitionTarget(BaseModel):
    """One semantically extracted target alternative from an NL transition group."""

    target: str = Field(min_length=1, description="Normative target concept or exact grounded state ID.")
    target_concept_id: str | None = Field(
        default=None,
        pattern=r"^C-[A-Za-z0-9_-]{1,64}$",
        description="Stable semantic concept ID for the normative target, when one was assigned.",
    )
    condition: str | None = Field(
        default=None, description="Condition semantically attached to this target alternative."
    )
    observed_transition_id: str | None = Field(
        default=None,
        max_length=160,
        description="Exact authored transition ID that realizes this relation, when one exists.",
    )
    formal_condition: str | None = Field(
        default=None,
        max_length=800,
        description=(
            "Grounding-only exact formal condition binding. The contract extractor "
            "must leave this null; grounding may fill it only from the canonical "
            "transition AST, while the normative condition remains unchanged."
        ),
    )
    condition_role: Literal["event", "qualified_guard", "unknown"] | None = Field(
        default=None,
        description=(
            "Semantic role of the normative condition. Use event when the NL merely "
            "names the selected event/action; use qualified_guard when it adds an "
            "independent formal qualifier such as a value, phase, or zero-time rule; "
            "use unknown when the distinction cannot be grounded."
        ),
    )


class ExpectedTransitionGroup(BaseModel):
    """One NL sentence/group whose alternatives share a semantically grounded source."""

    source: str = Field(min_length=1, description="Normative source concept or exact grounded state ID.")
    source_concept_id: str | None = Field(
        default=None,
        pattern=r"^C-[A-Za-z0-9_-]{1,64}$",
        description="Stable semantic concept ID for the normative source, when one was assigned.",
    )
    targets: list[ExpectedTransitionTarget] = Field(
        min_length=1, description="All semantically named target alternatives; do not truncate the group."
    )
    nl_line: int = Field(ge=1, description="One-based numbered NL line containing the obligation.")
    nl_quote: str | None = Field(default=None, min_length=1, description="Optional verbatim NL span.")
    priority: int = Field(ge=1, le=5, description="Semantic priority of the transition group.")


class ExpectedInitialContract(BaseModel):
    """One explicit initial-entry obligation extracted from the requirements."""

    composite: str = Field(min_length=1, description="Normative composite/scope concept or exact state ID.")
    composite_concept_id: str | None = Field(
        default=None,
        pattern=r"^C-[A-Za-z0-9_-]{1,64}$",
        description="Stable semantic concept ID for the normative composite, when one was assigned.",
    )
    target: str = Field(min_length=1, description="Normative initial child concept or exact state ID.")
    target_concept_id: str | None = Field(
        default=None,
        pattern=r"^C-[A-Za-z0-9_-]{1,64}$",
        description="Stable semantic concept ID for the normative initial target, when one was assigned.",
    )
    nl_line: int = Field(ge=1, description="One-based numbered NL line containing the initial obligation.")
    nl_quote: str | None = Field(default=None, min_length=1, description="Optional verbatim NL span.")
    requirement_group_id: str | None = Field(
        default=None,
        pattern=r"^RG-[A-Za-z0-9_-]{1,64}$",
        description=(
            "LLM-declared semantic bundle identity for initial obligations that "
            "must be reported together. Deterministic code only preserves it."
        ),
    )
    priority: int = Field(ge=1, le=5, description="Semantic priority of the initial obligation.")


class ExpectedContainmentContract(BaseModel):
    """One explicit parent-child containment obligation from the requirements."""

    parent: str = Field(min_length=1, description="Normative parent concept or exact scope ID.")
    parent_concept_id: str | None = Field(
        default=None,
        pattern=r"^C-[A-Za-z0-9_-]{1,64}$",
        description="Stable semantic concept ID for the normative parent, when one was assigned.",
    )
    child: str = Field(min_length=1, description="Normative child concept or exact state ID.")
    child_concept_id: str | None = Field(
        default=None,
        pattern=r"^C-[A-Za-z0-9_-]{1,64}$",
        description="Stable semantic concept ID for the normative child, when one was assigned.",
    )
    nl_line: int = Field(ge=1, description="One-based numbered NL line containing the containment obligation.")
    nl_quote: str | None = Field(default=None, min_length=1, description="Optional verbatim NL span.")
    priority: int = Field(ge=1, le=5, description="Semantic priority of the containment obligation.")


class RequiredStateContract(BaseModel):
    """One LLM-declared NL concept that requires a state realization."""

    concept: str = Field(min_length=1, description="Natural-language state concept requiring realization.")
    concept_id: str = Field(
        pattern=r"^C-[A-Za-z0-9_-]{1,64}$", description="Stable semantic concept ID reused only for true coreference."
    )
    scope_concept_id: str | None = Field(
        default=None,
        pattern=r"^C-[A-Za-z0-9_-]{1,64}$",
        description="Stable semantic concept ID for the containing scope, when one was assigned.",
    )
    role: Literal[
        "operating_state",
        "condition_state",
        "initial_state",
        "termination_state",
        "other_state",
    ] = Field(description="Semantic role of the required state in the requirement.")
    nl_quote: str = Field(min_length=1, description="Verbatim NL span establishing the state requirement.")
    priority: int = Field(ge=1, le=5, description="Semantic priority of the required state.")


class RequiredEventScopeContract(BaseModel):
    """One LLM-declared event obligation and its normative scope concept."""

    event_concept: str = Field(min_length=1, description="Natural-language event concept whose coverage is required.")
    scope_concept: str = Field(min_length=1, description="Natural-language scope concept to which coverage applies.")
    scope_concept_id: str | None = Field(
        default=None,
        pattern=r"^C-[A-Za-z0-9_-]{1,64}$",
        description="Stable semantic concept ID for the required scope, when one was assigned.",
    )
    applicability: Literal[
        "one_scope",
        "scope_and_descendants",
        "each_operating_mode",
    ] = Field(description="LLM semantic applicability mode; do not infer it lexically."
    )
    nl_quote: str = Field(min_length=1, description="Verbatim NL span establishing event coverage.")
    priority: int = Field(ge=1, le=5, description="Semantic priority of the required event scope.")


class RequiredActionContract(BaseModel):
    """One explicit state-owned action or output obligation extracted from NL."""

    action_concept: str = Field(
        min_length=1,
        description="Exact normative action or output identity supplied by semantic extraction.",
    )
    owner_concept: str = Field(
        min_length=1,
        description="Natural-language state concept that owns the required action.",
    )
    owner_concept_id: str = Field(
        pattern=r"^C-[A-Za-z0-9_-]{1,64}$",
        description="Stable semantic concept ID for the owning state.",
    )
    phase: Literal["entry", "exit", "during", "any"] = Field(
        description=(
            "Lifecycle phase established by the requirement; use any only when "
            "the requirement assigns the action to the state without fixing a phase."
        )
    )
    action_kind: Literal["state_action", "output_signal"] = Field(
        description="Semantic action category; transition triggers and conditions are excluded."
    )
    nl_quote: str = Field(
        min_length=1, description="Verbatim NL span establishing this one atomic action obligation."
    )
    priority: int = Field(ge=1, le=5, description="Semantic priority of the required action.")


class ContractLensPlan(BaseModel):
    """Fixed discovery frontend selected after the balanced/hybrid pilots.

    Transition contracts are extracted in groups so enumerated alternatives do
    not compete for candidate slots. The remaining slots are reserved for
    non-transition surface mismatches and behavior hypotheses.
    """

    transition_groups: list[ExpectedTransitionGroup] = Field(
        max_length=10, description="Grouped direct-transition obligations extracted from NL."
    )
    surface_candidates: list[BalancedEvidenceCandidate] = Field(
        max_length=3, description="Surface hypotheses reserved by the lens."
    )
    behavior_candidates: list[BalancedEvidenceCandidate] = Field(
        max_length=4, description="Behavior hypotheses reserved by the lens."
    )

    @property
    def candidates(self) -> list[BalancedEvidenceCandidate]:
        return [*self.surface_candidates, *self.behavior_candidates]


class ContractExtractionPlan(BaseModel):
    """Lossless semantic extraction of explicit NL obligations before grounding."""

    initial_contracts: list[ExpectedInitialContract] = Field(
        description="Every explicit initial-entry obligation; preserve all members of a semantic bundle."
    )
    containment_contracts: list[ExpectedContainmentContract] = Field(
        default_factory=list, description="Every explicit parent-child obligation."
    )
    transition_groups: list[ExpectedTransitionGroup] = Field(
        description="Every explicit direct-transition group, including all alternatives."
    )
    required_state_contracts: list[RequiredStateContract] = Field(
        default_factory=list, description="State concepts that the requirements require to be realized."
    )
    required_event_scope_contracts: list[RequiredEventScopeContract] = Field(
        default_factory=list, description="Event/scope coverage obligations established by NL semantics."
    )
    required_action_contracts: list[RequiredActionContract] = Field(
        default_factory=list,
        description=(
            "Every explicit state-owned named action or output signal obligation, "
            "kept atomic and independent of persistence or transition obligations."
        ),
    )


class GroundedContractPlan(ContractExtractionPlan):
    """Lossless internal contract after LLM plans have been merged."""

    initial_contracts: list[ExpectedInitialContract] = Field(
        default_factory=list,
        description="Merged initial-entry obligations preserved after grounding.",
    )
    containment_contracts: list[ExpectedContainmentContract] = Field(
        default_factory=list,
        description="Merged parent-child obligations preserved after grounding.",
    )
    transition_groups: list[ExpectedTransitionGroup] = Field(
        default_factory=list,
        description="Merged direct-transition groups with every normative alternative preserved.",
    )
    required_state_contracts: list[RequiredStateContract] = Field(
        default_factory=list,
        description="Merged required-state obligations preserved after grounding.",
    )
    required_event_scope_contracts: list[RequiredEventScopeContract] = Field(
        default_factory=list,
        description="Merged event/scope coverage obligations preserved after grounding.",
    )
    required_action_contracts: list[RequiredActionContract] = Field(
        default_factory=list,
        description="Merged state-owned action obligations preserved after grounding.",
    )


class IssueDiscoveryPlan(BaseModel):
    """Typed issue hypotheses after semantic grounding, ready for execution."""

    surface_candidates: list[BalancedEvidenceCandidate] = Field(
        max_length=96, description="Grounded structural and representation hypotheses."
    )
    behavior_candidates: list[BalancedEvidenceCandidate] = Field(
        max_length=5, description="Grounded behavior hypotheses with typed goals."
    )

    @property
    def candidates(self) -> list[BalancedEvidenceCandidate]:
        return [*self.surface_candidates, *self.behavior_candidates]


class SemanticGroundingGap(BaseModel):
    """Explicit unresolved semantic binding retained for audit instead of guessing."""

    scope: Literal["contract", "surface_candidate", "behavior_candidate"] = Field(
        description="Plan lane in which the unresolved binding occurred."
    )
    item_index: int = Field(ge=0, description="Zero-based item index in that lane.")
    field: str = Field(min_length=1, description="Field whose semantic binding remains unresolved.")
    reason: str = Field(min_length=1, description="Short semantic reason for withholding a binding.")


class EvidenceGoalBinding(BaseModel):
    """Compact exact-ID patch applied to an already proposed goal."""

    lane: Literal["surface_candidates", "behavior_candidates"] = Field(
        description="Candidate lane receiving this binding patch."
    )
    item_index: int = Field(ge=0, le=4, description="Zero-based candidate index in the lane.")
    observed_transition_id: str | None = Field(default=None, max_length=160, description="Exact observed transition ID.")
    reference_transition_id: str | None = Field(default=None, max_length=160, description="Exact reference transition ID.")
    subject: str | None = Field(default=None, max_length=200, description="Exact formal subject ID.")
    source: str | None = Field(default=None, max_length=200, description="Exact formal source ID.")
    trigger: str | None = Field(default=None, max_length=200, description="Exact formal trigger/event ID.")
    condition_role: Literal["event", "qualified_guard", "unknown"] | None = Field(
        default=None,
        description=(
            "Semantic role for a normative condition; qualified_guard is only valid "
            "when the selected transition has an exact formal guard binding."
        ),
    )
    target: str | None = Field(default=None, max_length=200, description="Normative exact target ID.")
    forbidden_scope: str | None = Field(default=None, max_length=200, description="Exact forbidden scope ID.")
    response: str | None = Field(default=None, max_length=200, description="Exact response ID.")
    variable: str | None = Field(default=None, max_length=200, description="Exact variable ID.")
    action: str | None = Field(default=None, max_length=200, description="Exact lifecycle action identity.")


class SemanticConceptBinding(BaseModel):
    """One semantic concept-to-source-state binding produced by grounding."""

    concept_id: str = Field(
        pattern=r"^C-[A-Za-z0-9_-]{1,64}$", description="Stable semantic concept ID."
    )
    source_state_id: str = Field(
        min_length=1, max_length=200, description="Exact author-source state ID selected by semantic reasoning."
    )
    nl_lines: list[int] = Field(
        default_factory=list, description="Numbered NL lines supporting the concept binding."
    )


class SemanticGroundingPlan(BaseModel):
    """Semantic re-audit plus exact formal bindings; it does not generate verdicts."""

    contract_plan: ContractExtractionPlan = Field(
        description="Re-audited contract plan with normative relations preserved."
    )
    concept_bindings: list[SemanticConceptBinding] = Field(
        default_factory=list, description="Exact concept-to-state bindings."
    )
    evidence_bindings: list[EvidenceGoalBinding] = Field(
        description="Exact-ID patches for candidate goals."
    )
    unresolved: list[SemanticGroundingGap] = Field(
        default_factory=list, description="Bindings intentionally withheld because semantics remain ambiguous."
    )


class CompactConceptBinding(BaseModel):
    """Compact exact concept binding used by the discovery-grounding response."""

    concept_id: str = Field(
        pattern=r"^C-[A-Za-z0-9_-]{1,64}$", description="Stable semantic concept ID."
    )
    source_state_id: str = Field(
        min_length=1,
        max_length=200,
        description=(
            "Exact author-source state ID copied verbatim from the supplied inventory; "
            "never shorten a qualified path or remove its pair namespace."
        ),
    )


class InitialContractGrounding(BaseModel):
    """Sparse semantic decision about one extracted initial contract."""

    item_index: int = Field(ge=0, description="Zero-based initial-contract index.")
    status: Literal["grounded", "rejected", "unresolved"] = Field(
        description="Semantic status; silence means the raw contract is accepted."
    )
    composite: str | None = Field(default=None, min_length=1, max_length=200, description="Exact grounded composite ID.")
    target: str | None = Field(default=None, min_length=1, max_length=200, description="Exact grounded initial target ID.")
    reason: str | None = Field(default=None, min_length=1, description="Reason for rejecting or withholding the contract.")


class ContainmentContractGrounding(BaseModel):
    """Sparse semantic decision about one extracted containment contract."""

    item_index: int = Field(ge=0, description="Zero-based containment-contract index.")
    status: Literal["grounded", "rejected", "unresolved"] = Field(
        description="Semantic status; deterministic code does not infer containment."
    )
    parent: str | None = Field(default=None, min_length=1, max_length=200, description="Exact grounded parent scope ID.")
    child: str | None = Field(default=None, min_length=1, max_length=200, description="Exact grounded child state ID.")
    reason: str | None = Field(default=None, min_length=1, description="Reason for rejecting or withholding the contract.")


class TransitionTargetGrounding(BaseModel):
    """Exact target binding for one member of a transition group."""

    target_index: int = Field(ge=0, description="Zero-based target index in the raw transition group.")
    target: str = Field(min_length=1, max_length=200, description="Normative exact target ID; do not rewrite it to match the artifact.")
    observed_transition_id: str | None = Field(
        default=None, max_length=160, description="Exact authored transition ID realizing this relation, when semantically selected."
    )
    condition_binding: str | None = Field(
        default=None,
        max_length=800,
        description=(
            "Exact formal event/guard/raw-label identity copied from the selected "
            "source transition. Required for a conditioned target when W2 is "
            "claimed; never use prose, Markdown, or a paraphrase."
        ),
    )
    condition_role: Literal["event", "qualified_guard", "unknown"] | None = Field(
        default=None,
        description=(
            "LLM semantic condition role copied to the grounded target. This is not "
            "inferred from labels: event is an event-level obligation, while "
            "qualified_guard requires an exact parsed guard in the selected AST."
        ),
    )


class TransitionGroupGrounding(BaseModel):
    """Exhaustive semantic binding for one transition alternative group."""

    item_index: int = Field(
        ge=0,
        description="Zero-based index of the raw transition group being resolved.",
    )
    status: Literal["grounded", "rejected", "unresolved"] = Field(
        description=(
            "grounded when the NL relation is semantically valid; rejected when "
            "the raw extractor invented it; unresolved only for a genuine competing "
            "NL reading"
        )
    )
    source: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Exact author-source state ID for a grounded raw group.",
    )
    targets: list[TransitionTargetGrounding] = Field(
        default_factory=list,
        description=(
            "For a grounded group, exactly one row per raw target in target_index "
            "order, carrying its normative exact target and the semantically "
            "corresponding authored transition ID when one exists."
        ),
    )
    reason: str | None = Field(
        default=None,
        min_length=1,
        description="Semantic reason for rejection or unresolved grounding.",
    )


class RequiredStateGrounding(BaseModel):
    """Semantic resolution of a required state concept against the source inventory."""

    item_index: int = Field(ge=0, description="Zero-based required-state index.")
    status: Literal["realized", "missing", "unresolved"] = Field(
        description="Whether the required state is realized, absent, or semantically unresolved."
    )
    formal_kind: Literal["state", "final_pseudostate"] | None = Field(
        default=None, description="Formal kind of a realized element."
    )
    realized_state_id: str | None = Field(default=None, max_length=200, description="Exact realized source state ID.")
    parent_scope_id: str | None = Field(default=None, max_length=200, description="Exact parent scope ID used for anchoring.")
    normative_formal_path: str | None = Field(default=None, max_length=200, description="Normative formal path when the required element is absent.")
    reason: str | None = Field(default=None, min_length=1, description="Semantic reason for a missing or unresolved result.")


class RequiredEventScopeGrounding(BaseModel):
    """Exact event identity and scope set for a required event-coverage obligation."""

    item_index: int = Field(ge=0, description="Zero-based required-event-scope index.")
    status: Literal["grounded", "unresolved"] = Field(description="Semantic binding status.")
    observed_transition_id: str | None = Field(
        default=None, max_length=160, description="Exact transition used to bind the event identity."
    )
    required_scope_ids: list[str] = Field(
        default_factory=list, description="Exact formal scope IDs covered by the requirement."
    )
    reason: str | None = Field(default=None, min_length=1, description="Reason for withholding a scope binding.")


class RequiredActionGrounding(BaseModel):
    """Sparse semantic veto for one NL-extracted state-owned action contract."""

    item_index: int = Field(ge=0, description="Zero-based required-action index.")
    status: Literal["rejected", "unresolved"] = Field(
        description=(
            "Reject an incorrectly classified action obligation or withhold a "
            "genuinely ambiguous owner/action/phase reading. Silence accepts the contract."
        )
    )
    reason: str = Field(
        min_length=1,
        description="Auditable semantic reason for rejecting or withholding the action contract.",
    )


class UnauthorizedTransitionGrounding(BaseModel):
    """An LLM-semantic audit result for one authored edge.

    The compiler never infers authorization from labels or from an omitted NL
    mention.  It only consumes this explicit semantic decision and checks the
    selected transition ID plus the cited NL span before lowering it to the
    existing ``transition_absent`` proof route.
    """

    observed_transition_id: str = Field(
        min_length=1,
        max_length=160,
        description="Exact authored transition ID selected by semantic review.",
    )
    status: Literal["unauthorized", "unresolved"] = Field(
        description="Semantic disposition of the selected authored transition.",
    )
    nl_quote: str | None = Field(
        default=None,
        min_length=1,
        description="Verbatim requirement span supporting the authorization decision, when available.",
    )
    nl_lines: list[int] = Field(
        default_factory=list,
        max_length=8,
        description="Numbered NL lines supporting the authorization decision.",
    )
    rationale: str = Field(
        min_length=1,
        max_length=800,
        description="Auditable semantic reason; do not infer authorization from labels or omission.",
    )


class DiscoveryGroundingPlan(BaseModel):
    """One compact cross-view semantic patch plus executable hypotheses.

    Initial and containment bindings are sparse veto/ambiguity patches. Transition
    bindings are exhaustive in fresh runs because their conditions and actions
    cannot be bound by deterministic text rules.
    """

    concept_bindings: list[CompactConceptBinding] = Field(
        default_factory=list, description="Exact semantic concept-to-source bindings."
    )
    initial_contract_bindings: list[InitialContractGrounding] = Field(
        default_factory=list,
        description=(
            "Sparse rejected/unresolved patches; grounded rows are accepted only "
            "when the corresponding semantic contract is explicitly supported."
        ),
    )
    containment_contract_bindings: list[ContainmentContractGrounding] = Field(
        default_factory=list,
        description=(
            "Sparse rejected/unresolved patches; grounded rows are accepted only "
            "when the corresponding semantic contract is explicitly supported."
        ),
    )
    transition_group_bindings: list[TransitionGroupGrounding] = Field(
        default_factory=list,
        description=(
            "Fresh-run exhaustive resolutions: exactly one row for every raw "
            "transition group and, when grounded, exactly one target row for every "
            "raw target."
        ),
    )
    required_state_bindings: list[RequiredStateGrounding] = Field(
        default_factory=list, description="Resolutions for required state concepts."
    )
    required_event_scope_bindings: list[RequiredEventScopeGrounding] = Field(
        default_factory=list, description="Resolutions for required event/scope coverage."
    )
    required_action_bindings: list[RequiredActionGrounding] = Field(
        default_factory=list,
        description=(
            "Sparse rejected/unresolved vetoes for state-owned named action contracts; "
            "silence accepts the NL-only extraction after exact owner concept binding."
        ),
    )
    unauthorized_transition_bindings: list[UnauthorizedTransitionGrounding] = Field(
        default_factory=list,
        description=(
            "Sparse semantic audit results for authored transitions that the NL "
            "does not authorize. Every row must name an exact source transition "
            "ID; omission is not interpreted as authorization or rejection."
        ),
    )
    additional_contracts: ContractExtractionPlan = Field(
        default_factory=lambda: ContractExtractionPlan(
            initial_contracts=[], containment_contracts=[], transition_groups=[]
        ),
        description="Additional semantically identified contracts omitted by the first extraction pass.",
    )
    surface_candidates: list[BalancedEvidenceCandidate] = Field(
        max_length=6, description="Fresh structural hypotheses with typed obligations."
    )
    behavior_candidates: list[BalancedEvidenceCandidate] = Field(
        max_length=5, description="Fresh behavioral hypotheses with typed obligations."
    )
    unresolved: list[SemanticGroundingGap] = Field(
        default_factory=list, description="Explicit semantic gaps; never fill them by lexical guessing."
    )

    @property
    def evidence_plan(self) -> IssueDiscoveryPlan:
        return IssueDiscoveryPlan(
            surface_candidates=self.surface_candidates,
            behavior_candidates=self.behavior_candidates,
        )


class FreshBalancedEvidenceCandidate(BalancedEvidenceCandidate):
    """Candidate contract for a live discovery response."""

    basis: str = Field(
        min_length=1,
        max_length=1200,
        description=(
            "Required audit reason linking the quoted obligation to the exact "
            "formal observation; do not state an execution result."
        ),
    )

    observed_fact: str = Field(
        default="",
        description=(
            "Audit-only summary of the exact formal/source/inspect fact that "
            "motivated this candidate; always fill it in live responses and do "
            "not predict execution. An omission is recorded as an audit gap, not "
            "a schema-fatal error, because prose completeness is semantic."
        ),
    )
    domain_obligation: DomainObligation = Field(
        description=(
            "Required typed obligation for a fresh candidate. It must match the "
            "goal relation and expose every exact formal binding needed by the compiler."
        ),
    )


class FreshDiscoveryGroundingPlan(DiscoveryGroundingPlan):
    """Live cross-view grounding response with typed formal bindings."""

    surface_candidates: list[FreshBalancedEvidenceCandidate] = Field(
        default_factory=list,
        max_length=6,
        description="Structural hypotheses, each with an observed fact and typed domain obligation.",
    )
    behavior_candidates: list[FreshBalancedEvidenceCandidate] = Field(
        default_factory=list,
        max_length=5,
        description="Behavioral hypotheses, each with an observed fact and typed domain obligation.",
    )


class BroadCandidate(BaseModel):
    """Broad hypothesis envelope used only before typed goal refinement."""

    candidate_id: str = Field(
        pattern=r"^B-[0-9]{2}$", description="Stable broad-hypothesis ID copied into refined candidates."
    )
    obligation: str = Field(min_length=1, description="Natural-language obligation under consideration.")
    claim: str = Field(min_length=1, description="Broad localized issue hypothesis.")
    basis_kind: Literal["nl_literal", "implicit_oracle", "domain_norm"] = Field(
        description="Provenance class of the broad hypothesis."
    )
    nl_quote: str | None = Field(default=None, description="Verbatim requirement span, when applicable.")
    locations: list[str] = Field(
        default_factory=list, max_length=4, description="Exact locations supporting localization."
    )
    proposed_l: Literal["L0", "L1", "L2"] = Field(
        description="Pre-refinement localization suggestion only."
    )
    priority: int = Field(ge=1, le=5, description="Semantic priority of the broad hypothesis.")


class BroadDiscoveryPlan(BaseModel):
    """Bounded broad-hypothesis output that must be refined before execution."""

    candidates: list[BroadCandidate] = Field(
        max_length=6, description="Broad hypotheses for later semantic grounding and typed compilation."
    )


class DDecision(BaseModel):
    """LLM semantic D-level adjudication for one located or executed finding."""

    finding_key: str = Field(min_length=1, description="Exact finding key being adjudicated.")
    grounding: Literal["lit", "lang", "impl", "dom", "none"] = Field(
        description=(
            "Normative basis for the first reading: lit is an exact requirement "
            "quote, lang is an applicable language clause, impl is only the "
            "closed protocol source-grounded deadlock family, dom is an explicit "
            "indispensable typed domain norm, and none means no grounded reading."
        )
    )
    violated_obligation: str = Field(
        min_length=1, description="Concise statement of the obligation judged violated."
    )
    strongest_defeater: str | None = Field(
        default=None,
        description="Strongest alternative reading or defeater considered by the judge; null only when none exists.",
    )
    defeater_kind: Literal["none", "undercutting", "rebutting"] = Field(
        description="Type of the strongest defeater."
    )
    defeater_disposition: Literal["defeated", "survives", "unresolved"] = Field(
        description="Whether the strongest defeater is defeated, survives, or remains unresolved."
    )
    rationale: str = Field(
        min_length=1, description="Auditable natural-language reason for the D decision; do not introduce new formal facts."
    )
    duplicate_of: str | None = Field(
        default=None,
        description=(
            "Exact earlier finding_key for the same technical defect, or null when "
            "this finding is an independent report issue."
        ),
    )
    duplicate_rationale: str | None = Field(
        default=None,
        description=(
            "One sentence naming the shared exact source cause and violated "
            "property when duplicate_of is non-null."
        ),
    )
    d_subclass: DSubclass = Field(
        description=(
            "Issue-189 D2 provenance subclass: D2-lit for literal/language "
            "grounding, D2-impl only for the closed operational deadlock "
            "certificates, D2-norm only for a typed indispensable domain norm; "
            "use not_applicable for D1 or D0."
        )
    )
    d_level: DLevel = Field(
        description=(
            "Issue-189 evidence grade after defeater adjudication, not a model "
            "confidence score: D2 has no competent surviving defeater, D1 has a "
            "grounded first reading with a surviving or unresolved undercutting "
            "alternative, and D0 is rebutted or lacks an established violated "
            "obligation."
        )
    )


class DAdjudicationPlan(BaseModel):
    """One D decision per finding, kept separate from executable W evidence."""

    decisions: list[DDecision] = Field(
        description="Complete adjudication set for the supplied findings; do not omit unresolved findings."
    )


SYSTEM_PROMPT = """
Design executable tests for NL satisfaction of the author-source state machine.
Prioritize L2 behavior: reachability, event response, traps, and termination.

Return at most four distinct candidates. For each one:
- state the obligation and localized claim concisely;
- use an exact NL quote for `nl_literal`; reserve `implicit_oracle` for blatant
  failures needing no domain knowledge; spell out any `domain_norm`;
- cite concrete `PUML:L<n>` lines, FCSTM `F<n>` lines, or exact state paths in
  `locations`;
- when upgrading a supplied broad candidate, copy its `candidate_id` into
  `broad_candidate_ids`;
- select at most one exact `probe_seed_id` when its hypothesis fits the NL
  obligation; otherwise write no more than two custom checks. Never combine a
  seed with custom checks in the same candidate;
- mark a prerequisite such as reachability as `precondition`, and the check that
  can falsify the claim as `primary`.

Available custom checks are the 19 established predicate shapes: declaration
and structure checks, transition/effect checks, simulation checks, and bounded
formal checks. Put predicate arguments in `bindings`; the legacy source/trigger/
target/within_cycles fields are also accepted for the common behavior shapes.
The deterministic compiler validates each predicate signature. If no predicate
shape expresses a claim, leave checks empty and return a W1/W0 candidate instead
of inventing an API. The production method may use additional typed trace,
topology, or bounded-formula IR nodes; this prototype only executes predicate
calls.

Inspect diagnostics and probe seeds are localization clues, not requirements or
verdicts. The executor preserves each seed as an independent probe group, so a
failed seed cannot be reported as evidence for a different custom claim. Respect
the execution/source attribution boundary: compiler-owned or capability-excluded
behavior is representation debt unless a separate source assertion and compiler
cause certificate establish the source defect without claiming behavior
equivalence.
Do not predict probe results, use ledger knowledge, or propose repairs.
""".strip()


CONTRACT_SYSTEM_PROMPT = """
Extract every explicit initial-state, containment, and direct-transition
contract from the numbered natural-language requirements. This is semantic
extraction, not defect discovery.

Assign a stable `C-...` concept ID to each state concept. Reuse one concept ID
only when your semantic reading says that multiple mentions denote the same
state; never infer coreference from spelling, token overlap, or repetition.
Put the concept ID beside every source, target, parent, child, composite, and
initial target. The next LLM binds each concept once to a formal state ID.

Put “begins in”, “starts in”, “initially in”, and an explicit “first transitions
to/enters” statement into `initial_contracts`; these are default-entry
obligations, not ordinary direct source-state transitions. In particular, a
sentence such as “the system first transitions to PumpState” must produce an
initial contract for the enclosing operating scope and the named first target,
with the complete verbatim NL span. Put only later named state-to-state
relations in `transition_groups`. Do not silently reduce a first-entry
statement to a `required_state_contract` because that loses the normative
entry relation needed by the formal source certificate.

When two or more initial-state contracts are semantically one reportable
requirement bundle, assign them the same stable `requirement_group_id` in the
form `RG-...`. This is a semantic grouping judgment: use it only when one issue
report must state all members together to preserve the requirement, and never
derive it from shared words, adjacent lines, identifier spelling, or the
observed artifact. Leave it null for independent initial obligations.

Put every explicit parent/child relation in `containment_contracts`, including
relations expressed by “substate”, “inside”, “within”, or an equally explicit
hierarchical statement. Record the semantic parent and child concepts from NL;
do not infer containment merely because one sentence mentions two states.

Independently enumerate `required_state_contracts` for every NL concept that a
competent semantic reading requires to be realized as a state, including a state
used as an initial/terminal target or as a condition such as “while/in/after
state q”. Do not classify an event, numeric predicate, action, or ordinary noun
as a state merely because of its wording. This is an LLM semantic decision, not
a token or identifier rule. Reuse the same concept ID for genuine coreference
and give the containing-scope concept ID when NL establishes one.

Enumerate `required_event_scope_contracts` whenever NL semantically requires an
event to be accepted in one state scope, throughout a composite scope, or in
each operating mode. Decide eventhood, subject, and applicability from meaning,
not from capitalization, keywords, label spelling, or punctuation. Keep numeric
predicates and state conditions out of this list unless the NL semantically
describes an externally offered event.
Use `one_scope` for one exact active state scope, `scope_and_descendants` when
one composite requirement explicitly covers its nested active states, and
`each_operating_mode` when the NL quantifies over semantically distinct modes.
These are semantic applicability declarations; do not choose among them by the
number of source states or by identifier shape.

Independently enumerate `required_action_contracts` for every atomic, named
action or output signal that the NL assigns to a particular state. Include
entry, exit, and during actions; when the requirement assigns the action to a
state but fixes no lifecycle phase, use `phase=any`. Assign one exact owner
concept ID and keep each action/output separate. Do not merge an action with
persistence, reachability, a transition trigger, a guard condition, or a later
effect. A transition event such as “on obstacle detected” is not a state-owned
action unless the NL separately says that the state performs or sends that
action. Use `action_kind=state_action` for lifecycle actions and
`action_kind=output_signal` for explicitly emitted signals. This is a semantic
inventory pass: do not infer an action from capitalization, punctuation, a
slash, or a label token, and do not omit an action merely because the source
model has no corresponding formal element. Quote the smallest contiguous NL
span that establishes this one action obligation.

Group alternatives by source state and cite `nl_line`, an exact contiguous
`nl_quote` when a shorter span is needed, and the exact source/target/condition
names. Omit optional `nl_quote` when the full numbered line already states the
contract; downstream replay uses that exact physical line. Any supplied quote
need not equal a physical file line, but must be copied byte-for-byte from the NL.
Preserve every target
named after “to”, “either”, “or”, “returns to”, “exits to”, or equivalent direct
transition language. Attach a trailing condition to multiple alternatives only
when semantic reading establishes that it governs the whole enumeration. A
coordinated clause such as “q0 reaches q1, and if c it further reaches q2” may
instead describe a second step or admit multiple competent attachment readings;
do not turn grammar or proximity into a source/condition decision. Never replace
a required A->C edge with a later B->C edge.

Keep semantically distinct control effects distinct even when both eventually
leave a scope. In particular, a local mode exit under one condition and a later
mode/system completion under another condition are different target concepts
unless the NL explicitly identifies them. Do not reuse a named final/completion
state as the target of an earlier unnamed local-exit relation merely because both
can be paraphrased as leaving something. Create a separate semantic target
concept for the local exit and let the grounding LLM bind it.

Worked rule for the critical grammatical shape:
“In A, the system begins in x, and can transition to y or z based on p and q”
becomes one group: source=x, targets=[(y, p and q), (z, p and q)].

The deterministic layer checks only whether each quote is an exact source span.
It does not decide whether that span semantically supports the extracted
contract; this semantic responsibility remains with this LLM and adjudication.

Do not report issues, observed model facts, W/D/L labels, backends, code, or
repairs. Preserve the natural-language concepts as written; a later LLM
semantic-grounding stage will bind them to exact source-model identifiers.
""".strip()


SEMANTIC_GROUNDING_SYSTEM_PROMPT = """
Semantically ground two already-generated plans against the exact author-source
state-machine inventory. This stage is the only authority for interpreting
natural-language concepts as source states, transitions, events, or conditions.
Do not use lexical overlap, substring occurrence, token similarity, stemming,
or identifier-shape heuristics as a substitute for semantic interpretation.

Return one `SemanticGroundingPlan` with:

1. `contract_plan`: re-audit every numbered NL line and return every explicit
   initial-state, containment, and direct-transition contract, including
   alternatives omitted by the raw extraction. Replace state concepts with
   exact state IDs from the supplied inventory. Bind every containment parent
   and child independently of their observed source nesting. When an existing
   source transition is semantically the artifact's attempted realization of a
   required relation, put its exact `id` in `observed_transition_id`. The
   NL-required source and target remain normative fields; the selected observed
   transition may have a wrong endpoint. Leave the field null when the required
   edge is absent or no transition can be semantically selected. Never replace a
   normative source or target with an observed endpoint.
2. `concept_bindings`: bind each `C-...` concept ID exactly once to one supplied
   state ID. Preserve repeated concept IDs from raw extraction. Coreference and
   scope are semantic decisions made here, not by deterministic text processing.
3. `evidence_bindings`: return exactly one compact patch for every raw evidence
   candidate, addressed by its zero-based array index and lane. Put only exact
   supplied formal IDs in binding fields. For event/transition goals, provide
   the exact `observed_transition_id` whenever one existing source transition is
   the semantically intended event relation; the compiler derives its formal
   consumer source and event from that ID while preserving an explicitly bound
   descendant response target. For a conditioned transition, set
   `condition_role=event` when the prose merely names the selected event/action,
   `condition_role=qualified_guard` when it adds an independent value, state,
   phase, or zero-time qualifier, and `condition_role=unknown` when the
   distinction is unresolved. Candidate prose and non-binding goal semantics
   are immutable and therefore are not repeated in your output.
4. `unresolved`: record every binding that remains genuinely ambiguous or lacks
   a corresponding formal element. Do not invent identifiers to make the plan
   look complete.

Exact identifier existence and same-concept consistency are checked
deterministically after this call. Those checks do not decide language meaning.
Do not report new defects, remove issue candidates, choose a backend, emit code,
predict execution, assign W/D, use a ledger or baseline result, or propose a
repair.

Bind the concrete element that exists in the observed author-source artifact,
even when the candidate claims that the element should have occupied another
normative position. For example, if the artifact nests `q2` under `q1` but the
claim says `q2` should be a sibling, bind the actual nested `Root.q1.q2`; do not
leave it unresolved merely because the ideal sibling element does not exist.

The NL contract is normative and the source model is the object under test.
Never rewrite a required contract to agree with an existing source edge: do not
move a target to a different source, delete an alternative, or remove/reassign a
condition stated by NL. Binding may qualify a concept with its exact formal ID,
and re-audit may add an omitted NL contract, but neither may change its semantic
relation. If NL requires `q0 -> q2` and only `q1 -> q2` exists, keep exact
`q0 -> q2` and leave `observed_transition_id` null. If NL assigns shared condition
`c` to `q0 -> q1 or q2`, preserve `c` on both targets even when one source edge
is unlabelled or absent.

For every contract, copy `nl_quote` as one exact contiguous source span that
states the contract. It need not equal a physical file line. Downstream code
checks only that the bytes occur in the supplied NL; whether the quote supports
the contract remains an LLM/D-adjudication question.

Relation-specific binding fields are fixed: `initial_target` uses
`subject=composite` and `target=initial child`; `contained_in` uses
`subject=child` and `target=parent`; `state_escapable` and
`termination_target` uses `subject` for a named state whose entry is explicitly
said to end the behavior; `eventually_terminates` uses `subject` for a broader
liveness obligation; `event_reaches_target` uses `source`,
`trigger`, and the exact required `target` plus `observed_transition_id` for the
event-consuming source edge; `effect_exists` uses `source`, `trigger`, and
`variable`; `action_exists` uses `subject=state`, `phase`, and the exact
semantically grounded `action` identity. `event_avoids_scope` uses `source`, `forbidden_scope`, and
`observed_transition_id`; the compiler derives the observed event and target
from that exact transition. A required event target may be the initial descendant of the source
transition's composite target, so preserve that exact descendant in `target`
rather than replacing it with the transition endpoint.

Use `transition_target_consistency` only after semantic reasoning establishes
that two distinct NL behaviors have the same normative target role. Put the
suspected wrong edge in `observed_transition_id`, an in-model conforming edge in
`reference_transition_id`, and the exact normative state in `target`. The
reference edge is evidence only for the already-made semantic judgment; equal
labels, conditions, event text, identifier spelling, or endpoints must never be
used downstream to infer same-role semantics. Synthetic example: if NL assigns
two different actions to leave one mode through `q_exit`, select their two exact
transition IDs and `target=q_exit`; the compiler then checks only their formal
endpoints and mapped FCSTM projections.

For a required state that is absent, use `state_exists` with `expected=true`,
put the exact existing parent scope in `source`, and put the LLM-declared
normative formal path in `subject`. The compiler validates only formal path
grammar and exact parent anchoring; it never invents the missing name. For an
event obligation that applies in a scope lacking a consumer, use
`event_consumed_in_scope`: put the exact missing scope in `source` and select an
exact `observed_transition_id` elsewhere solely to bind the event identity. The
compiler preserves the normative missing scope and derives only the event from
that transition.

Synthetic example only: if NL says `q0` reaches `q1` on `evt_a` and the formal
inventory contains transition `tr_a` from `M.q0` to `M.q1` with event `evt_a`,
the grounded goal may select `observed_transition_id=tr_a`; the compiler then
validates that ID and derives the formal endpoints. If two transitions remain
semantically plausible, select neither and record an unresolved binding.
""".strip()


DISCOVERY_GROUNDING_SYSTEM_PROMPT = """
Discover NL-satisfaction defects and bind every proposed executable goal to the
exact author-source state-machine inventory in one cross-view pass. You receive
numbered NL, author PlantUML, mapping-annotated FCSTM, pyfcstm inspect facts, a
raw NL-only contract plan, and exact source state/transition IDs.

This LLM call is the sole authority for NL semantics in discovery and grounding.
Semantic equivalence, coreference, condition scope, normative obligation,
whether a source transition realizes an NL relation, and which formal element a
description denotes must be decided by semantic reasoning here. Never replace
that reasoning with keyword presence, substring overlap, connector words such as
`and`/`or`, stemming, edit distance, embeddings, identifier shape, suffixes, or
unique-candidate completion. Deterministic code downstream checks only schema,
exact IDs, AST/mapping facts, inspect/topology/trace/SMT results, hashes, and
budgets. If a semantic binding is not justified, record it in `unresolved`; do
not guess.

Hierarchy/alternative-state audit is mandatory when applicable: if the NL
semantically treats two named configurations as sibling or mutually exclusive
operating states, compare their exact source parent edges and reserve a surface
candidate for a typed negative containment goal when one is nested under the
other. Set `relation=contained_in`, bind the exact child and parent IDs, and set
`expected=false`; include the supporting NL quote, basis, and observed hierarchy
fact. This candidate is permitted only when the NL establishes the alternative
relation. Never infer it from state names, capitalization, labels, or identifier
similarity; unresolved alternative status must remain an unresolved binding.

Return one `FreshDiscoveryGroundingPlan`:

1. `concept_bindings`: bind each realized raw `C-...` concept exactly once to one
   exact source state ID, including ordinary realized required-state concepts.
   A concept denoting the whole machine may bind to the supplied exact
   `root_scope_id`; do not force it onto a child state. Reuse a concept ID only
   for genuine semantic coreference. A required-state concept judged missing, a
   final pseudostate, or unresolved is handled by its indexed required-state
   resolution; do not invent an ID for it.
2. `initial_contract_bindings` and `containment_contract_bindings` are sparse
   semantic vetoes. Re-audit every raw item, but output a row only when its status
   is `rejected` or `unresolved`. `rejected` means the raw extractor invented the
   relation, such as treating ordinary sequential prose as composite
   initialization. `unresolved` means multiple competent readings remain. Leave
   formal fields empty and state one short reason. Silence means the LLM accepts
   the raw relation and the deterministic assembler substitutes only this plan's
   exact `concept_bindings`; it never matches names or searches text.

   `transition_group_bindings` is deliberately exhaustive because condition and
   action descriptions cannot be matched by deterministic text rules. Return
   exactly one indexed row for every raw transition group. A `grounded` row must
   provide the exact normative source and exactly one target row for every raw
   target. Each target row preserves the normative exact target and supplies the
   exact `observed_transition_id` when one authored transition semantically
   realizes that NL relation. If the intended edge is absent, leave that ID null.
   If an authored edge realizes the stated action or condition but has the wrong
   target, select that exact wrong-edge ID while preserving the normative target;
   execution will test the mismatch. For every conditioned target with a
   selected observed transition, copy the exact canonical event/guard/raw-label
   identity into `condition_binding`; do not copy prose or Markdown. Also set
   `condition_role=event` when the NL condition merely names that event/action,
   `condition_role=qualified_guard` when the NL adds an independent value,
   state, phase, zero-time, or other guard qualifier, and
   `condition_role=unknown` only when the distinction cannot be grounded. A
   qualified guard requires an exact parsed guard in the selected source AST;
   an event label alone never discharges it. If no exact formal identity can be
   justified, leave `condition_binding` null and let the compiler keep the
   candidate at W1. Use `rejected` or `unresolved` with empty formal fields only
   when the NL relation itself is rejected or ambiguous.
   Every live response must satisfy this indexed completeness contract.

   Judge every status from the NL relation, never from whether the observed artifact
   satisfies it. If NL truly says state `q` is inside `P` while the inventory
   places `q` at root, the contract is `grounded` with normative parent `P` and
   observed child ID `q`; that mismatch is exactly what execution must test. If
   NL merely says `q` runs after `P`, a raw containment contract is `rejected`.
   One clause may impose more than one compatible relation. Synthetic example:
   “P transitions into the q substate” states both a transition into `q` and
   containment of `q` by `P`; accepting the transition reading does not cancel
   the explicit substate relation. Reject a raw relation only when the NL itself
   does not support it, not because another relation from the same clause also
   exists.
   Likewise, a valid NL transition remains `grounded` when its authored edge is
   absent or has a wrong endpoint. Omit `reason` for routine grounded bindings;
   reserve it for rejected, unresolved, or genuinely non-obvious resolutions.
   When a coordinated sentence permits two competent source or condition-scope
   readings, set `status=unresolved`; do not select the reading that best matches
   the authored artifact. Synthetic example: “q0 reaches q1, and if c it further
   reaches q2” may leave open whether the second relation starts at q0 or q1 and
   which relation carries c. The source model cannot resolve that NL ambiguity.
3. `additional_contracts`: re-audit all NL lines and put only explicit initial,
   containment, direct-transition, or atomic state-owned action/output contracts
   omitted by the raw plan here. These additions use exact source IDs or exact
   owner concept bindings but preserve normative endpoints and action identity
   even when the observed source model is wrong. Keep an added action separate
   from transition, effect, persistence, and reachability claims.
   When the NL presents two named configurations as alternative operating states,
   reserve a surface candidate for an explicit negative containment obligation
   when the semantic reading requires them to be siblings rather than nested.
   Ground the exact child and parent IDs through concept bindings, set the typed
   goal expectation to false, and retain the supporting NL span and basis. This
   is a semantic alternative-state decision, not a name or label test; if the
   alternative relation is unresolved, record the unresolved binding instead of
   inventing this candidate.
   If a raw group collapses two semantically different targets, mark that raw
   group `rejected` and put the corrected explicit relation in
   `additional_contracts`; do not silently preserve the wrong target. A local
   exit and a separately stated global/mode completion are not the same target
   without explicit NL coreference.
4. `required_state_bindings` is also sparse. Omit an ordinary `state` realization
   already represented by `concept_bindings`. Output an indexed row for every
   `missing`, `unresolved`, or `final_pseudostate` decision. `missing` gives one
   exact existing parent scope plus an explicitly declared absent normative
   formal path. `unresolved` records genuine semantic ambiguity. Always set
   `formal_kind` on an emitted row: use `state` for a named ordinary state and
   `final_pseudostate` for the formal completion marker of a scope. A missing
   final pseudostate needs the exact parent scope but no invented ordinary-state
   path. Never choose among these statuses or kinds by identifier spelling,
   label overlap, suffixes, or unique-candidate completion.
   The supplied `final_pseudostates` list is the exact formal inventory for this
   decision. If the semantically corresponding marker is present there, use
   `realized` with that exact marker ID; use `missing` only when the exact marker
   for the grounded scope is absent.
5. `required_event_scope_bindings`: return exactly one indexed resolution for
   every raw event-scope contract. A grounded resolution selects one exact source
   transition only to bind event identity. For `one_scope`, list that exact scope;
   for `scope_and_descendants`, list the exact anchor scope and let the compiler
   expand its canonical `parent` closure; for `each_operating_mode`, enumerate
   every exact scope that semantic reading classifies as an operating mode. The
   compiler checks each covered scope and its active ancestors; it never derives
   event identity, scope applicability, or operating-mode status from labels. Use
   `unresolved` rather than guessing an event or scope.
6. `required_action_bindings`: re-audit every raw state-owned action/output
   contract. Emit a row only when the extractor incorrectly classified a
   trigger, condition, or transition effect as a state-owned action (`rejected`)
   or when the owner, action identity, or lifecycle phase has two competent
   semantic readings (`unresolved`). Silence accepts the atomic contract, and
   the compiler then uses its exact owner concept binding to test action
   ownership. Never suppress an action merely because the source action is
   absent. Do not combine a missing action with persistence or transition
   candidates; each obligation remains an independent candidate with its own
   exact owner, phase, and action identity.
7. `surface_candidates`: at most six distinct L0/L1 hypotheses concerning
   inventory, containment, entry, label/effect, transition, or guard structure.
8. `behavior_candidates`: at most five distinct L2 hypotheses concerning path,
   reachability, response, escapability, wrong scope, deadlock, or termination.
9. `unauthorized_transition_bindings`: a sparse result of the complete authored-
   edge authorization audit. Emit one row only when semantic comparison supports
   the conclusion that an exact authored transition is forbidden or extraneous;
   include its exact transition ID, one verbatim NL span that supplies the
   normative context, the physical NL line numbers used, and a concise semantic
   rationale. Use `status=unresolved` when two competent authorization readings
   remain. Do not treat omission from this list as authorization, and do not
   classify an edge as unauthorized merely because its label or identifier is
   absent from NL. The compiler turns only `status=unauthorized` rows into the
   fixed `transition_absent` evidence lane.
10. `unresolved`: list ambiguous or unavailable candidate/concept bindings not
   already represented by an indexed contract status. An unresolved item may
   remain as a W1/W0 coverage gap, but must not be made executable by guessing.

For every candidate, state one obligation, one falsifiable claim, one concise
natural-language `basis`, and one concise observed source/FCSTM/inspect fact.
`basis` explains why the cited obligation and observation justify testing this
candidate; it is an audit field, not a compiler input. `observed_fact` states only
the exact formal observation and must not predict execution. `domain_obligation`
is the paper-level typed surface and is required for every new candidate:
- use `element` for existence or an NL-explicit cardinality; absence is the
  derived negation of existence, while kind comparison is compiler IR rather
  than an independent domain property;
- use `attachment` for containment, initial target, transition endpoints, trigger,
  guard, effect, or action-phase ownership;
- use `guard_set` for satisfiability, pairwise disjointness, or coverage;
  equivalence and implication are backend comparison operations, not new domain
  properties;
- use `graph` for reachability, deadlock freedom, or path exclusion; escapability,
  event-target reachability, and stable termination are derived macros;
- use `temporal` for response, precedence, existence, absence, or universality
  under an explicit scope; termination and holds-until behavior are derived from
  these base patterns.
The `goal.relation` field is only a compiler-lowering operation. It must be
compatible with the exact typed operator, but neither field selects a proof
backend. Do not output execution-support or W-ceiling fields. The compiler
derives one `SupportDisposition`: executable/W2 ceiling, located-only/W1 ceiling,
or prose-only/W0 ceiling. A meaningful orthogonal-region, history, opaque-action,
or unsupported temporal issue remains in its closest semantic family and is
degraded by that compiler decision; unsupportedness is not a sixth obligation.
Keep the paper-level operator and compiler relation distinct. In particular, a
wrong-scope route uses `domain_obligation.family=graph` with
`domain_obligation.property=path_absent`, while its lowering relation is
`goal.relation=event_avoids_scope`; `event_avoids_scope` is never a graph
property. Likewise, use only the enumerated typed operators in each obligation
family and only the enumerated lowering relations in `goal.relation`.

 A `nl_literal` candidate must copy one exact
 contiguous NL span verbatim in `nl_quote` and cite its physical `NL<n>` line when
 available. Use exact source IDs in
 state fields and exact transition IDs in `observed_transition_id`. Choose only a
 value copied verbatim from the supplied author-source inventory; never shorten a
 qualified ID to a leaf name, remove its pair namespace, or synthesize a path. If
 no inventory entry is a competent semantic binding, emit the typed unresolved
 row instead of guessing.
semantic `relation`; do not choose a proof template or backend. Use
`transition_absent` only after semantic comparison identifies one concrete
authored edge as forbidden or extraneous. Use `event_avoids_scope` only when one
semantically selected transition must avoid an exact state scope. Use
`termination_target` only when NL explicitly designates a named state as ending,
exiting, or completing behavior. Do not duplicate a deterministic frontier item
unless you attach a distinct NL obligation or a distinct source cause.

Candidate slots are for suspected violations, not coverage demonstrations. Do
not output a candidate whose claim says that the model correctly realizes or
satisfies the obligation, and do not spend behavior slots restating transitions
whose observed source, event, target, scope, and continuation all agree with NL.
Before returning, perform three general semantic audits over the supplied exact
inventory: (a) authored transitions that no competent reading of any NL contract
authorizes, (b) selected event routes whose exact target ancestry enters a scope
that the NL behavior must avoid, and (c) states explicitly designated by NL as a
completion/ending target that still admit a nonterminating continuation. Record
audit (a) in `unauthorized_transition_bindings`, not in the bounded candidate
array; record (b) and (c) as executable candidates when supported. Emit a row or
candidate only when semantic reasoning supports the violation; otherwise emit
nothing for that audit. These audits are LLM judgments over the complete views,
never deterministic text matching. For audit (a), a closed-world conclusion is
allowed only when the NL clause semantically enumerates the relevant source/role
alternatives or otherwise excludes the authored edge; simple non-mention is never
enough.

Also perform two coverage audits by semantic reasoning: (d) every raw
`required_state_contract`, especially a state concept referenced by an NL
condition, must either have a concept binding or an explicit sparse
`required_state_binding`; a `missing` resolution is mechanically compiled into
`state_exists` or `final_pseudostate_exists`, so do not duplicate it in candidate
slots, and (e) every raw event-scope contract must receive a binding. The compiler
expands each required scope in (e) into
`event_consumed_in_scope`, using one exact observed transition only to bind the
event identity. Do not infer either audit from words in identifiers or labels.

Synthetic worked examples only: if a raw required-state contract semantically
denotes `q_done` within `q_mode`, the exact inventory contains only `q_mode.q_a`
and `q_mode.q_b`, and semantic reasoning finds no state that realizes it, emit a
`missing` binding with `parent_scope_id=q_mode` and
`normative_formal_path=q_mode.q_done` and `formal_kind=state`. If the concept
instead denotes the scope's UML final pseudostate, use
`formal_kind=final_pseudostate`, `parent_scope_id=q_mode`, and no invented path.
The ordinary-state path is your semantic declaration, not a deterministic name
guess. If an event-scope contract says
system event `evt_stop` applies in every operating mode, exact transition
`tr_evt` consumes it in `q_manual`, and semantic audit says `q_manual` and
`q_auto` are both required scopes, bind `observed_transition_id=tr_evt` and
`required_scope_ids=[q_manual,q_auto]`; the compiler reads the event identity
from `tr_evt` and never invents or overwrites either scope. If instead the typed
applicability is `scope_and_descendants`, bind only the exact composite anchor;
the compiler expands descendants from structured parent edges and records both
per-scope consumers and the aggregate consumer set.

When an audit is supported, reserve its candidate before optional response
checks. Encode an unauthorized authored edge as `transition_absent` with its
exact `observed_transition_id`. Encode a route that must keep an ancestor mode
inactive as `event_avoids_scope` with the exact transition ID and
`forbidden_scope` equal to that ancestor scope, not the leaf endpoint. Encode an
NL-designated ending state as `termination_target` with that exact state in
`subject`, not `target`. Encode a state-target response as
`event_reaches_target` with exact `source`, required `target`, and
`observed_transition_id`; reserve `eventually_responds` for a genuine named
response event rather than a state name. Do not use a satisfied response check
in place of an applicable unauthorized-edge, wrong-scope, or stable-termination
violation. Cite the exact locations needed for the claim and keep the list
concise; citation count is not a semantic validity condition.

`event_reaches_target` requires the selected observed transition to be the
artifact's attempted realization of the response from the grounded normative
source. Never select a transition in another scope solely to borrow its event
identity. A missing consumer in a required scope is already represented by the
indexed `required_event_scope_binding`; do not duplicate it as an
`event_reaches_target` candidate.

The reporting axes are independent and are supplied here so candidates have the
right granularity, but you do not output their final values:

- W2: a compiled assertion was actually executed on the exact FCSTM and returned
  a terminal verdict. W1: a concrete element/assertion target is localized but
  execution is absent or inconclusive. W0: only a prose hypothesis remains.
- L0: direct inventory/edge/label fact. L1: derived static structure or guard
  relation. L2: path, reachability, event response, escape, or termination.
- D2: a grounded violated obligation survives all competent defeaters. D1: a
  grounded first reading exists but a concrete competent alternative reading
  survives. D0: the claim is rebutted or no violated obligation is established.

Synthetic examples only: if NL says `M begins in q0` and the exact inventory has
states `M` and `M.q0`, emit an `initial_target` goal with those exact IDs; the
compiler later decides W. If NL says event `evt_a` from `M.q0` must avoid scope
`M.q_bad`, and semantic inspection selects exact transition `tr_a`, emit
`event_avoids_scope` with `source=M.q0`, `forbidden_scope=M.q_bad`, and
`observed_transition_id=tr_a`. If two transitions are semantically plausible,
emit neither ID and record an unresolved binding. If an executed structural fact
is compatible with two readings of “region”, do not use the shared word or a
matching count to select one reading; leave the D distinction to adjudication.

Do not output Python, pyfcstm predicates, backend choices, diagnostic IDs, W/D
labels, ledger knowledge, baseline results, predicted execution results, or
repairs. Inspect is evidence for discovery, not a normative oracle. The NL is the
specification and the source model is the object under test; never rewrite the
specification to agree with the artifact.
""".strip()


DISCOVERY_GROUNDING_AUDIT_LENSES: tuple[tuple[str, str], ...] = (
    (
        "contract_structure_contrast",
        """
Fixed audit lens for this branch: contract, structure, and contrastive
consistency. Complete every mandatory concept, contract, required-state, and
required-event resolution from the base instructions. Then spend discretionary
candidate slots first on: omitted or collapsed direct contracts; containment
and default-entry defects; guard conflicts; unauthorized edges; and
cross-context inconsistencies where NL semantically assigns the same action or
condition role but the authored transitions realize incompatible target roles.
When the NL semantically presents two named states or modes as alternative
operating configurations, inspect the exact source parent edges for a possible
scope contradiction. If the semantic reading says those alternatives must not
be nested, emit a typed `contained_in` goal with the exact child and parent IDs,
`expected=false`, and preserve the NL span and basis. Do this only when the NL
meaning establishes the alternative relation; never infer it from state names,
capitalization, or a label word. If the relation is not grounded, record an
unresolved binding instead of inventing a containment obligation.
An authored edge may serve as an in-model contrastive oracle only after you
semantically establish the shared NL role. Never infer equivalence from equal
words, labels, identifiers, or condition strings. When a discrepant edge is
identified, bind its exact transition ID and express the corrected relation via
an additional contract or executable candidate.
""".strip(),
    ),
    (
        "behavior_consequence",
        """
Fixed audit lens for this branch: behavioral consequence. Complete every
mandatory concept, contract, required-state, and required-event resolution from
the base instructions. Then spend discretionary candidate slots first on root
reachability, event response, forbidden-scope entry, escapability, deadlock,
and stable termination. Trace exact target ancestry and active-ancestor
continuations. When NL explicitly designates an ending or completion target,
reserve a candidate if the exact model admits a continuing path or cycle.
Prefer the deepest executable consequence and its author-source cause over
surface restatements, while still reporting a distinct structural defect when
it establishes a different violated obligation.
""".strip(),
    ),
)


EVIDENCE_SYSTEM_PROMPT = """
Find substantive NL-satisfaction defects in the author-source state machine.
Explicit transition contracts are handled by a separate extraction stage, so
do not enumerate satisfied requirements. The method, not you, chooses and
combines execution backends.

Evidence levels are fixed by the method: W2 means a compiled assertion was
actually run on the exact FCSTM artifact and returned a terminal verdict; W1
means a concrete source/artifact element is localized but execution is absent
or inconclusive; W0 means only a prose hypothesis is available. You never emit
W. Supply precise semantic bindings so the compiler can maximize W2.

Return exactly two arrays:

1. `surface_candidates`: at most four suspected L0/L1 defects from T01-T07,
   including inventory, containment, entry, missing labels, and genuinely
   suspicious same-`(source,event)` guard conflicts.
2. `behavior_candidates`: at most four suspected T08-T12 L2 defects. Each must
   state the concrete contradictory source/inspect fact in `observed_fact`.

Never put reachability, response, escape, deadlock, or termination claims in
`surface_candidates`; those belong only in `behavior_candidates`. Do not
duplicate a deterministic frontier cause unless you attach a specific NL
obligation that the frontier lacks. Every surface and behavior candidate must
include `observed_fact`; state the exact source/FCSTM/inspect fact that motivated
the hypothesis, without predicting execution. For every candidate:
- keep `obligation`, `claim`, `basis`, and `observed_fact` to one concise sentence
  each; `basis` explains why the cited NL obligation and observed fact make this
  candidate worth testing, while `observed_fact` states only the exact formal,
  source, or inspect observation. Do not repeat the same rationale across fields,
  and always return both arrays even when one is empty;
- state one violated obligation and one falsifiable claim;
- quote one complete numbered NL line verbatim for `nl_literal`; reserve `implicit_oracle` for a
  source-grounded reachable non-final terminal; spell out any `domain_norm`;
- cite at most three exact NL/PUML/FCSTM locations or model paths;
- choose only the semantic relation and bind its source elements, event, target,
  condition, or bound; omit `template`, because the deterministic compiler owns
  the proof template and backend;
- use L0 for direct inventory/edge/label comparison, L1 for derived static
  structure or guard relations, and L2 only for paths, reachability, response,
  escape, or termination.

Guard-conflict discipline: inspect each source with two or more explicitly
conditioned alternatives. Report a conflict only when the conditions are
jointly satisfiable and the target actions are plausibly mutually exclusive.
Do not label an unguarded default edge plus unrelated higher-level event exits
as a guard-overlap issue; missing conditions are handled by contract execution.
For a guard-set obligation, transition_refs alone are insufficient. Return one
guard_bindings row per selected exact transition, copy that transition's exact
raw source label into source_label, and set semantic_role to guard_condition
only after semantic inspection establishes that the label is a condition rather
than an event, action, or display label. Never manufacture a binding from an
identifier or from a label that was not selected exactly. The compiler compares
each copied label to the canonical source artifact and then parses the formal
condition; missing or mismatched bindings become W1.

Use `effect_exists` for a variable update required on a transition and supply
its source, trigger, variable, and sign. Use `action_exists` only for an action
owned by a state at entry, exit, or during phase; supply its exact `action`
identity together with `subject=state` and `phase`, and never use it for a
transition effect.

Synthetic examples only: a state `q_stop` explicitly designated terminal is not
defective merely because it has no outgoing edge; guarded outgoing transitions
do not require an unconditional escape; compiler-generated helpers are not
defects unless inspect/execution reports a concrete failed consequence. Do not
recast an L2 unreachable component as a surface child-count claim.

You must not output Python, pyfcstm predicate names, diagnostic IDs, probe seed
IDs, backend choices, W levels, D levels, ledger knowledge, predicted tool
results, or repairs. Inspect facts are discovery clues, not normative verdicts.
The deterministic compiler may fan one goal out into static, guard-solver,
topology, trace, and bounded-formal evidence and will degrade unsupported goals
without aborting the pair.

Use `termination_target` only when NL explicitly says that reaching one named
state ends, exits, or completes the behavior. Use `eventually_terminates` for a
broader liveness obligation that is not tied to one terminal target.

Use `transition_absent` only after semantic comparison concludes that one
specific authored transition is forbidden or extraneous; grounding must select
its exact `observed_transition_id`. Use `event_avoids_scope` when one
semantically selected event transition must not enter a particular state scope;
bind that scope explicitly and let the compiler execute the observed route.
Use `transition_target_consistency` when semantic comparison establishes that
two different NL behaviors share one normative target role: bind the suspected
edge, a conforming reference edge, and the exact normative target. Do not infer
the shared role from condition strings, transition labels, names, or formal
endpoint equality.
""".strip()


BROAD_SYSTEM_PROMPT = """
Discover at most six high-priority NL-satisfaction issues from only the natural
language requirements and author-source PlantUML. Preserve broad L0/L1 recall
while allowing L2 hypotheses when the source itself makes them apparent.

For every candidate, state one violated obligation and one concrete claim. Quote
one complete numbered NL line verbatim for `nl_literal`; state the indispensable obligation for
`domain_norm`; reserve `implicit_oracle` for a blatant reachable deadlock. Cite
specific PUML lines or source element paths when possible. Assign L0 only when
surface terms suffice, L1 when a static structural fact must be derived, and L2
when a time-ordered behavior/reachability argument is necessary. Rank by likely
substantive defect impact. Do not inspect converted FCSTM, choose an execution
backend, write code, predict tool results, use a ledger, or propose repairs.
""".strip()


D_SYSTEM_PROMPT = """
Adjudicate every supplied finding from NL and author-source evidence. This is the
method's D prediction, not experiment truth. Never use a ledger, baseline,
expected issue list, identifier-word heuristic, or repair knowledge.

The axes are independent. W2 means a compiled assertion actually ran on the
exact FCSTM and returned a terminal verdict; W1 means concrete localization but
absent/inconclusive execution; W0 means prose only. L0 is a direct inventory,
edge, or label fact; L1 is a derived static structure/guard relation; L2 requires
a path, reachability, response, escape, or termination argument. You output only
D: D2 means a grounded violated obligation survives every competent defeater;
D1 means a grounded first reading exists and one concrete competent alternative
reading survives; D0 means rebutted or no violated obligation is established.
Neither W nor L determines D.

A `formal_oracle_rule` is a preregistered mapping from an exact formal
diagnostic code to a candidate quality norm. It proves only that the declared
formal fact occurred under the rule's stated applicability conditions; it does
not prove that the natural-language requirements make the condition defective.
Judge that normative applicability here. Never infer it from diagnostic message
wording, identifier spelling, or lexical overlap with the NL.

Use the supplied audit dossier fields only. `rationale` must name the supplied
NL clause, exact source/certificate fact, and the strongest alternative reading;
do not invent additional provenance fields or execution facts that are absent
from the dossier.

Return exactly one short decision per `finding_key`. Decide in this order:
grounding, violated obligation, strongest defeater, its disposition, then D.
`defeater_disposition` always describes whether the defeater itself remains
competent: `survives` means it still attacks the claim, `defeated` means supplied
evidence excludes or answers it, and `unresolved` means the dossier cannot decide
whether it survives. It never describes whether the original finding survives.
The required `rationale` is an audit basis, not a restatement: cite the supplied
NL clause, exact source/certificate fact, and why the strongest defeater is
defeated or survives. Keep it concise and do not introduce ledger knowledge or
an execution result that is absent from the dossier.
After deciding D, perform report-level semantic dedup inside this same whole-pair
call. Set `duplicate_of` only when the finding is the same technical defect as an
earlier supplied finding with a smaller ordinal: the same exact source elements
or transition set and the same violated property. Point to that earlier exact
`finding_key` and give one-sentence `duplicate_rationale`. Different
consequences or violated properties remain independent. Never group by wording,
token overlap, similar identifiers, or a ledger. Use null for both duplicate
fields when the issue is independent.

- D2: no competent defeater survives. Use D2-lit only when an exact NL quote
  explicitly and unambiguously states the same source, target, condition scope,
  or other violated obligation, or for a supplied binary language clause. Under
  this protocol D2-impl is closed to one of the supplied source-grounded
  non-final deadlock certificates: a sequential reachable deadlock, a complete
  orthogonal-region entry tuple whose concurrently active leaves and ancestors
  all lack continuation, or an exact missing-initial compiler bridge to a
  reachable fail-closed entry deadlock.
  Use D2-norm only for an explicit indispensable domain norm. A finding may
  carry typed `domain_obligations`; these are the only admissible structured
  domain-norm evidence. For a dead-end, `graph:deadlock_free` or
  `graph:escapable` with the exact dead-end target is a non-final operational
  obligation when the supplied NL/source context makes that obligation
  indispensable. A closed W2 deadlock certificate may therefore receive
  D2-norm when that typed obligation is the surviving basis. If no such typed
  domain obligation is supplied, do not manufacture one from `basis_kind`,
  `obligation`, diagnostic wording, state names, or absent outgoing edges.
  NL-required unreachability is D2-lit, never D2-impl.
- D1: use non-`none` grounding, `defeater_kind=undercutting`,
  `defeater_disposition=survives|unresolved`, and
  `d_subclass=not_applicable`. State the compatible second reading. Guard
  overlap is normally D1 when NL does not establish priority/exclusivity,
  but only when the dossier contains an exact formal guard-set/source
  certificate. A `guards_distinguishable` candidate whose selected labels are
  ordinary events, actions, display text, or otherwise lacks a parsed guard
  certificate has no grounded violated guard obligation; classify it D0 rather
  than publishing a lexical or label-level overlap hypothesis. The compiler's
  W1 fallback is evidence of missing executable support, not a defeater for
  this rule.
- D0: use `d_subclass=not_applicable`; use a rebutting defeater when facts show
  intended/non-defective behavior. Missing evidence without a grounded first
  reading is D0, not D1. A plausible quality recommendation or desired
  continuation that is not required by the NL, an applicable language rule, or
  an indispensable domain norm is also D0; uncertainty alone cannot manufacture
  the first violated reading required by D1. A D0 rebutting defeater must have
  `defeater_disposition=survives`, because it is the surviving rebuttal that makes
  the original claim false. Never mark that rebuttal `defeated`. Conversely, D2
  requires the strongest competent defeater to be `defeated`.

For a `contained_in` candidate with `goal.expected=false`, inspect the supplied
NL quote, obligation, basis, and exact source certificate together. If the
semantic basis establishes that two named operating configurations are
alternatives or mutually exclusive, and the certificate reports the forbidden
parent relation as a terminal source counterexample, this is a grounded first
reading even when the quote describes the configurations through a transition,
`or`, or a return route rather than using the word “sibling”. Do not rebut that
reading merely because the source can execute a transition between the states:
transition reachability and UML containment are different properties. Use D1
when a competent alternative interpretation of the names or scope remains, and
D2 only when the alternative-state obligation is explicit and no such reading
survives. If the supplied basis does not establish an alternative-state
obligation, or the source certificate is absent/inconclusive, classify the
candidate D0. Never create or reject this obligation from state-name similarity
or label wording.

For an `implicit_oracle` deadlock claim, a null or inconclusive source
certificate means the required source reachability/deadlock premise was not
grounded. Classify it D0, not D1; D1 is not a substitute for a missing formal
premise. This does not affect a separate NL-literal finding with an independently
grounded source certificate.

An executed missing-edge assertion proves only that the asserted exact edge is
absent. It does not prove that the LLM chose the normative target correctly. Use
the supplied shared exact source inventories and certificate anchors to test the
strongest alternative: when
the same source already has an edge that realizes the NL action under the stated
condition, a claim demanding another target is rebutted unless the NL explicitly
names that other target. Likewise, repeated use of one bare state concept does
not require a separate local copy inside every scope; a missing scope-local copy
is D0 unless the NL explicitly distinguishes per-scope instances.
If the NL does not establish the asserted target and the exact neighborhood
contains a competent alternative edge realizing the stated action, no grounded
first reading remains: classify the missing asserted edge as D0 with a rebutting
defeater, not D1.

For a transition-contract finding whose normative source is a composite state,
inspect the exact `observed_transition` and its structured source/parent fields.
When the selected authored edge starts in a descendant leaf of that composite
and reaches the required target with the same event, treat that descendant edge
as a competent realization of a scope-level “from/in the composite” statement.
Unless the supplied NL explicitly requires a direct composite-boundary edge or
an event consumed by the composite itself, a missing edge whose only difference
is the composite-versus-descendant source is D0 with a surviving rebutting
defeater. This is an AST parent/descendant fact, not a name or string heuristic;
do not apply it when no exact selected transition or structured parent relation
is present.

For a `source_transition_contract` whose certificate has
`relation_present=true` but `condition_present=false`, do not treat the
compiler's inconclusive condition binding as an automatic defect. First decide
what the NL condition means. If it is only the event/action that the exact
observed transition already carries (for example, NL says “when `evt_a` occurs”
and the selected edge has the exact event `evt_a`), the edge realizes the
obligation and the candidate is D0. If the NL adds a genuine qualifier (for
example, a value, state predicate, phase, or zero-time restriction) and the
source edge has no exact guard/formal qualifier for it, the qualified obligation
is still a grounded first reading; keep it D1 or D2 according to the surviving
alternative reading. `formal_condition_binding=false` is evidence about the
available formal binding, not by itself a semantic verdict. In particular, an
ordinary event label must not be required to repeat a natural-language paraphrase,
while a qualified guard must not be silently discharged by an unguarded event
label. The distinction is semantic and belongs to this LLM adjudication step;
the deterministic compiler must not infer it from punctuation or keywords.

An exact NL statement that a composite begins or starts in a child imposes a
default-entry obligation. An ordinary parent-to-child transition requiring an
event does not satisfy that obligation, because entering the composite does not
fire the event automatically. When the source certificate shows no initial
pseudostate edge to the required child, do not downgrade the violation merely
because a separate eventful edge reaches the same child.
Conversely, when NL says a child is entered first/default and an exact initial
pseudostate edge already enters that child, do not demand an additional ordinary
parent-to-child transition. That initial edge realizes the default-entry
obligation; an executed assertion for the absent ordinary edge is then D0.

An explicit containment statement is independent of transition reachability. A
normal edge into a state does not make that state a child of the source scope, so
it cannot defeat an exact parent/child obligation. However, ordinary NL
"within/contains" wording establishes transitive containment, not necessarily a
direct-parent relation. When a `source_containment_contract` reports
`within_expected_ancestor=true`, a direct-parent claim is D0 unless NL explicitly
requires a direct child, sibling set, same region, or one hierarchy level. When
the child lies outside the required ancestor entirely, the containment violation
survives. For stable termination, use
hierarchical execution semantics: while a leaf nested in a composite is active,
applicable outgoing transitions of its active ancestor can still continue the
machine. Therefore a leaf with no own outgoing edge is not a stable termination
target when the supplied source certificate proves an ancestor exit or cycle.
When NL explicitly states that reaching a named state ends, completes, or exits
the behavior, `explicit_final=false` is not a defeater; the missing formal final
marker may itself be part of the modeled violation. For
`source_unstable_termination_target`, decide from exact reachability,
`ancestor_chain`, and `continuing_transitions`: a reachable target with an
applicable active-ancestor exit or cycle is not stable termination even when the
leaf has no own outgoing transition. Reserve the exact `explicit_final` rule for
`reachable_deadlock`; do not transfer it to a literal termination obligation.

Treat the author-source transition action/effect slot as source semantics. When
an exact transition already has an action that semantically states the NL effect,
absence of a lower-level variable declaration or assignment is representation
debt, not an author-source defect, unless the NL or declared source language
explicitly requires that lower-level encoding. Also do not infer irreversible or
stable termination from a boundary phrase such as "before completion" alone. A
stable-termination obligation needs an explicit ends/exits/terminates statement,
an applicable language clause, or an indispensable domain norm.

An explicit statement that a named mode ends when a named state is reached is a
local stable-termination obligation for that mode; it does not need to say that
the whole state machine terminates. When a sound source certificate proves that
the named target is reachable and an inherited transition can continue, re-enter,
or leave the supposedly ended mode, the ending obligation is violated. Use the
exact NL ending statement as `grounding=lit`; do not rebut it merely because
system-wide termination was not required.

For D2 use a defeated/no surviving defeater and the subclass implied by
grounding (`lit|lang -> D2-lit`, `impl -> D2-impl`, `dom -> D2-norm`). Keep every
prose field to one sentence. Do not change a valid decision because another
finding is uncertain.

`source_attribution` is authoritative. If it is only `unattributed` or
`representation_debt` and `source_certificate` is null, an FCSTM result cannot
support D2-impl; D2 still requires an independently supplied literal, language,
or domain obligation plus source facts. A supplied `language_clause` may support
`grounding=lang` only when its antecedent and violation are established. Do not
invent language rules. For `reachable_deadlock`, use exact `explicit_final`;
never infer terminality from a state name or merely from absent outgoing edges.
For `concurrent_region_deadlock`, use the complete typed region-entry tuple and
do not treat the existence of orthogonal regions as a defeater when every active
region entry and ancestor is certified blocked. For `source_entry_deadlock`, use
the exact missing-initial compiler bridge rather than the generated state name.
Do not retain a concurrency defeater when exact source facts exclude concurrency.
When `protocol_d2_grounding` is non-null, it is the preregistered #189 subclass
for this typed formal certificate if and only if you decide D2; it does not tell
you whether the finding is D2, and it never overrides a surviving defeater.
The converse is strict: output `grounding=impl` only when that finding's dossier
sets `protocol_d2_grounding="impl"`. A formal source certificate without that
field may corroborate a literal obligation but cannot change its provenance;
when an exact quoted NL obligation is what survives the defeater, use
`grounding=lit` and D2-lit. This is a field-level contract, not a suggestion.

Synthetic calibration only: (1) NL requires `q0 -> q1` on `evt_a`, the source
edge is absent, and no alternate reading survives: D2-lit. (2) NL permits `q0`
to choose `q1` or `q2` under `c`, while a default-branch reading survives: D1
with an undercutting surviving defeater. (3) NL designates `q_stop` terminal and
the allegation is only that it lacks outgoing edges: D0. (4) NL says three modes
but not peer/parallel/sibling; a nested reading survives, so the peer-count claim
is not D2. (5) A finding claims an edge is absent, but its source certificate
lists an exact matching transition with the required endpoint and condition
slot: D0 even if FCSTM execution is inconclusive. (6) NL says `q0` reaches `q1`,
and if `c` it further reaches `q2`; if both `q0 -> q2 under c` and `q1 -> q2 under
c` remain competent readings, a guard-placement claim is D1, not D2-lit. (7) NL
only says execution proceeds to `q_choice`, while a source-grounded certificate
proves `q_choice` is reachable, non-final, and deadlocked in a certified
sequential fragment: D2-impl, not D2-lit. A complete orthogonal entry tuple with
all active non-final leaves blocked receives the same D2-impl treatment. (8) NL
requires reaching `q_exit` but says nothing about behavior after
`q_exit`; a claim that `q_exit` must continue to another termination state is D0,
not D1. (9) Two findings independently allege non-disjoint guards over the same
exact transitions `t1,t2`; the later finding is `duplicate_of` the earlier one,
whereas a separate claim that `t2` has the wrong target remains independent. (10)
One finding concerns an extraneous edge `t1` and another concerns a wrong-scope
route `t2`; even if both enter the same nested target, they use different exact
elements and distinct minimal corrections, so neither is a duplicate. (11) NL
literally says behavior ends when `q_end` is reached, while a source-localized
finding says `q_end` is not a genuine termination point but has no eligible W2
receipt; adjudicate the explicit obligation as D2-lit, not D2-impl, because D and
W are independent. (12) NL requires a component's initial state to operate, and
an exact source-graph certificate proves that component unreachable with
`no_concurrent_regions=true`; an imagined orthogonal-region interpretation does
not survive against the supplied source artifact, so use D2-lit rather than D1.
(13) NL says an operation decreases `count`, and the exact source transition has
the action `/ count decreased`; a claim that the author source omits the effect
merely because it lacks executable assignment syntax is D0. (14) NL says behavior
holds only "before completion" but never says completion ends the machine; a
claim that any restart after completion is forbidden is D0, not D1.
(15) NL says composite `P` first enters child `q`, and the source contains exact
initial edge `@initial:P -> q`; a claim that ordinary edge `P -> q` is missing is
D0. (16) A W2 deadlock finding and a later W1 prose hypothesis name the same exact
state and the same no-continuation property; the W1 restatement may be a duplicate
only when its `duplicate_eligible_earlier_keys` includes the earlier finding, but
it cannot use D2-impl without its own W2 receipt. Different exact blocked state
IDs remain independent even when they occur in one concurrent configuration.
(17) A finding calls `q` a reachable deadlock, but another exact source
certificate in the same dossier proves that a missing parent initial makes `q`
unreachable; the reachable-deadlock claim is rebutted and is D0. Do not convert
unreachability into deadlock merely because the converted artifact contains a
different generated fail-closed state.
(18) NL requires three unnamed regions but does not assign identities to them; a
count/coverage finding may be grounded, but separate claims that invented
placeholders `Region1`, `Region2`, and `Region3` are missing are D0. Cardinality
does not create named element-existence obligations.
(19) NL says mode `M` ends when target `q_end` is reached, and a sound source
certificate proves `q_end` reachable with an inherited continuation that can
continue, re-enter, or leave `M`; this is D2-lit for the local ending obligation
even when NL does not say the whole machine terminates. This differs from (14),
where "before completion" alone creates no stable-ending obligation.
(20) NL says substates `a,b,c` are "within P", while the source certificate says
`within_expected_ancestor=true` because each is nested under an intermediate
wrapper inside `P`; a claim that the wrapper itself violates containment is D0
unless NL explicitly requires direct children, siblings, or one hierarchy level.
(21) A W2 reachable non-final dead-end carries the typed obligation
`graph:escapable` for that exact target and the NL/source context makes
continuation indispensable; D2-norm is allowed. The same certificate without
that typed obligation uses D2-impl only when `protocol_d2_grounding="impl"`.
(22) NL literally says composite `P` begins in child `q`, while the source has
only an eventless ordinary edge `P -> q` and no initial-pseudostate edge in `P`.
The ordinary completion edge is evidence that the author attempted the relation,
but it does not establish default entry when `P` becomes active; classify the
missing initial-target relation as D2-lit when no other reading survives.
(23) NL requires `q0 -> q1` when event `evt_a` occurs, and the exact source edge
`q0 -> q1 : evt_a` is present while the condition binding is inconclusive: the
event-level contract is satisfied, so the missing-binding hypothesis is D0.
(24) NL requires `q0 -> q1` when `count=0`, and the exact source edge is
`q0 -> q1 : close` with no exact guard/formal qualifier: the endpoint edge does
not discharge the qualified obligation, so a grounded D1/D2 condition finding
may remain even though `relation_present=true`.
Do not propose repairs.
""".strip()


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _canonical_sha256(value: Any) -> str:
    return _sha256(
        json.dumps(
            _jsonable(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
    )


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "__dict__"):
        return {
            str(key): _jsonable(item)
            for key, item in vars(value).items()
            if not str(key).startswith("_")
        }
    return str(value)


def build_llm_binding_provenance(
    observations: list[dict[str, Any]],
    *,
    role: str,
    semantic_plan: BaseModel,
    grounded_contract_plan: BaseModel,
    grounded_evidence_plan: BaseModel,
    replayed: bool,
    llm_call_id: str | None = None,
) -> dict[str, Any] | None:
    """Bind an LLM semantic plan to its immutable call observation by hashes."""

    matching = [
        item
        for item in observations
        if isinstance(item, dict)
        and item.get("role") == role
        and item.get("status") == "completed"
        and (llm_call_id is None or item.get("llm_call_id") == llm_call_id)
    ]
    if not matching:
        return None
    semantic_plan_hash = _canonical_sha256(semantic_plan)
    matching = [
        item
        for item in matching
        if _canonical_sha256(item.get("parsed_output")) == semantic_plan_hash
    ]
    if not matching:
        return None
    observation = matching[-1]
    parsed_output = observation.get("parsed_output")
    observed_call_id = observation.get("llm_call_id")
    if not isinstance(observed_call_id, str) or not observed_call_id:
        return None
    payload = {
        "schema": "paper1.llm_semantic_provenance.v1",
        "stage_record_ref": f"llm_call:{observed_call_id}",
        "llm_call_id": observed_call_id,
        "role": role,
        "profile": observation.get("profile"),
        "provider": observation.get("provider"),
        "configured_model": observation.get("configured_model"),
        "observed_model": observation.get("observed_model"),
        "system_prompt_sha256": _canonical_sha256(observation.get("system_prompt")),
        "user_prompt_sha256": _canonical_sha256(observation.get("user_prompt")),
        "raw_response_sha256": _canonical_sha256(observation.get("raw_response")),
        "structured_schema_sha256": observation.get("structured_schema_sha256"),
        "schema_contract_repeated_in_prompt": observation.get(
            "schema_contract_repeated_in_prompt"
        ),
        "parsed_output_sha256": _canonical_sha256(parsed_output),
        "semantic_plan_sha256": semantic_plan_hash,
        "grounded_contract_plan_sha256": _canonical_sha256(grounded_contract_plan),
        "grounded_evidence_plan_sha256": _canonical_sha256(grounded_evidence_plan),
        "observation_sha256": _canonical_sha256(observation),
        "replayed": replayed,
    }
    payload["provenance_sha256"] = _canonical_sha256(payload)
    return payload


def _semantic_binding_receipt(
    authority: SemanticBindingAuthority,
    candidate: dict[str, Any],
    *,
    semantic_provenance: dict[str, Any] | None,
    compiler_input_plan_sha256: str,
    candidate_index: int | None,
    formal_binding_transforms: Any,
) -> dict[str, Any]:
    formal_only = authority in {"formal_source_ast", "formal_pyfcstm_diagnostic"}
    receipt = {
        "schema": "paper1.semantic_binding_receipt.v2",
        "authority": authority,
        "scope": "formal_fact_only" if formal_only else "nl_to_formal",
        "grounded_candidate_sha256": _canonical_sha256(candidate),
        "compiler_input_plan_sha256": compiler_input_plan_sha256,
        "candidate_index": candidate_index,
        "formal_reference_policy": "exact_id_or_declared_mapping_only",
        "formal_binding_transforms_sha256": _canonical_sha256(
            formal_binding_transforms
        ),
        "semantic_decision_claimed": not formal_only,
        "semantic_provenance": semantic_provenance if not formal_only else None,
    }
    receipt["receipt_sha256"] = _canonical_sha256(receipt)
    return receipt


def _attach_semantic_binding_receipt(
    outcome: dict[str, Any],
    authority: SemanticBindingAuthority,
    *,
    semantic_provenance: dict[str, Any] | None = None,
    compiler_input_plan_sha256: str,
) -> dict[str, Any]:
    candidate = outcome.get("candidate")
    candidate = candidate if isinstance(candidate, dict) else {}
    transforms = [
        group.get("compiler_route", {}).get("method_bindings", [])
        for group in outcome.get("probe_groups", [])
        if isinstance(group, dict) and isinstance(group.get("compiler_route"), dict)
    ]
    receipt = _semantic_binding_receipt(
        authority,
        candidate,
        semantic_provenance=semantic_provenance,
        compiler_input_plan_sha256=compiler_input_plan_sha256,
        candidate_index=outcome.get("candidate_index"),
        formal_binding_transforms=transforms,
    )
    outcome["semantic_binding_receipt"] = receipt
    for group in outcome.get("probe_groups", []):
        if not isinstance(group, dict):
            continue
        group["semantic_binding_receipt"] = receipt
        for certificate_field in (
            "execution_certificate",
            "source_causality_certificate",
        ):
            certificate = group.get(certificate_field)
            if isinstance(certificate, dict):
                certificate["semantic_binding_receipt"] = receipt
    return outcome


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise TypeError(f"expected JSON object: {path}")
    return value


def load_pair(case: str, report_root: Path = DEFAULT_REPORT_ROOT) -> dict[str, Any]:
    pair_dir = report_root / "pairs" / case
    pair_name = f"llms_emp_feedback_final_{case}"
    paths = {
        "nl": pair_dir / "nl.txt",
        "plantuml": pair_dir / "plantuml.puml",
        "fcstm": pair_dir / "fcstm.fcstm",
        "source_trace": report_root / "source_traces" / f"{pair_name}.json",
        "working_contract": report_root / "working_contracts" / f"{pair_name}.json",
        "canonical": report_root / "canonical" / f"{pair_name}.json",
    }
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing pair artifact(s): {missing}")
    return {
        "case": case,
        "pair_name": pair_name,
        "paths": {name: str(path) for name, path in paths.items()},
        "nl": paths["nl"].read_text(encoding="utf-8"),
        "plantuml": paths["plantuml"].read_text(encoding="utf-8"),
        "fcstm": paths["fcstm"].read_text(encoding="utf-8"),
        "source_trace": _load_json(paths["source_trace"]),
        "working_contract": _load_json(paths["working_contract"]),
        "canonical": _load_json(paths["canonical"]),
    }


def _source_label(ref: str) -> str:
    match = re.search(r":line:(\d+)$", ref)
    return f"PUML:L{match.group(1)}" if match else ref


def _fcstm_state_lines(fcstm: str) -> dict[str, int]:
    """Map exact FCSTM state paths to lines through the public DSL parser."""

    from pyfcstm.dsl import parse_with_grammar_entry

    ast = parse_with_grammar_entry(fcstm, "state_machine_dsl")
    lines: dict[str, int] = {}

    def visit(node: Any, parent: str | None) -> None:
        name = getattr(node, "name", None)
        span = getattr(node, "_span", None)
        line = getattr(span, "line", None)
        if not isinstance(name, str) or not isinstance(line, int):
            return
        path = f"{parent}.{name}" if parent else name
        lines[path] = line
        for child in getattr(node, "substates", []):
            visit(child, path)

    visit(ast.root_state, None)
    return lines


def annotate_fcstm(fcstm: str, contract: dict[str, Any]) -> str:
    """Render a display-only FCSTM view with source/compilation comments."""

    role_aliases = {
        "state": "identity",
        "source_initial_transition": "initial",
        "source_direct_transition": "direct",
        "composite_source_leaf_trigger": "leaf_route",
        "composite_source_sibling_continuation": "sibling_route",
        "protected_cross_scope_route_token": "route_token",
        "missing_source_initial_fail_closed": "missing_initial",
    }

    source_lines = fcstm.splitlines()
    exact_line_numbers: dict[str, list[int]] = {}
    for line_no, line in enumerate(source_lines, start=1):
        exact_line_numbers.setdefault(line.strip(), []).append(line_no)
    state_line_numbers = _fcstm_state_lines(fcstm)
    notes_by_line: dict[int, set[str]] = {}
    elements = contract.get("elements", [])
    if not isinstance(elements, list):
        elements = []
    for element in elements:
        if not isinstance(element, dict):
            continue
        metadata = element.get("metadata")
        metadata = metadata if isinstance(metadata, dict) else {}
        source_refs = element.get("source_refs")
        refs = (
            [str(item) for item in source_refs] if isinstance(source_refs, list) else []
        )
        origin = str(element.get("origin") or "unknown")
        role = (
            metadata.get("generated_role")
            or metadata.get("generated_reason")
            or element.get("kind")
        )
        role = role_aliases.get(str(role), str(role))
        ref_text = ",".join(_source_label(ref) for ref in refs) or "none"
        relation = (
            "identity"
            if origin == "source_owned"
            else f"lower:{role}"
            if refs
            else f"generated:{role}"
        )
        note = f"{ref_text} {relation}"
        line = metadata.get("line")
        if isinstance(line, str) and line.strip():
            matches = exact_line_numbers.get(line.strip(), [])
            if len(matches) == 1:
                notes_by_line.setdefault(matches[0], set()).add(note)
        fcstm_path = metadata.get("fcstm_path")
        if element.get("kind") == "state" and isinstance(fcstm_path, str) and refs:
            state_line = state_line_numbers.get(fcstm_path)
            if state_line is not None:
                notes_by_line.setdefault(state_line, set()).add(note)

    rendered: list[str] = []
    for line_no, line in enumerate(source_lines, start=1):
        notes = notes_by_line.get(line_no, set())
        mapping = f" @map {' | '.join(sorted(notes))}" if notes else ""
        rendered.append(f"{line}  // F{line_no}{mapping}")
    return "\n".join(rendered)


def inspect_fcstm(fcstm: str, path: str, *, smt_timeout_ms: int) -> dict[str, Any]:
    from pyfcstm.diagnostics import inspect_model
    from pyfcstm.dsl import parse_with_grammar_entry
    from pyfcstm.model import parse_dsl_node_to_state_machine

    ast = parse_with_grammar_entry(fcstm, "state_machine_dsl")
    model = parse_dsl_node_to_state_machine(ast, path=path)
    report = inspect_model(
        model,
        enable_verify=True,
        max_complexity_tier="smt_undecidable_heuristic",
        max_call_count_scaling="linear_in_transitions",
        smt_timeout_ms=smt_timeout_ms,
    ).to_json()
    if not isinstance(report, dict):
        raise TypeError("pyfcstm inspect did not return a JSON object")
    return report


def compact_inspect(report: dict[str, Any]) -> dict[str, Any]:
    diagnostics: list[dict[str, Any]] = []
    for item in report.get("diagnostics", []):
        if not isinstance(item, dict):
            continue
        refs = item.get("refs")
        compact_refs = {}
        if isinstance(refs, dict):
            compact_refs = {
                str(key): value for key, value in refs.items() if key != "suggested_fix"
            }
        diagnostics.append(
            {
                "code": item.get("code"),
                "severity": item.get("severity"),
                "message": item.get("message"),
                "span": item.get("span"),
                "refs": compact_refs,
            }
        )
    return {
        "schema": report.get("schema"),
        "status": report.get("status"),
        "metrics": report.get("metrics", {}),
        "diagnostics": diagnostics,
    }


def compact_capability_boundary(contract: dict[str, Any]) -> dict[str, Any]:
    eligibility = contract.get("capability_eligibility", {})
    eligibility = eligibility if isinstance(eligibility, dict) else {}
    simulation = eligibility.get("simulation", {})
    simulation = simulation if isinstance(simulation, dict) else {}
    return {
        "simulation_status": simulation.get("status"),
        "simulation_reason_codes": simulation.get("reason_codes", []),
        "simulation_claim_boundary": simulation.get("claim_boundary"),
    }


def _child_path(parent: str | None, child: str | None) -> str | None:
    if not child:
        return None
    if "." in child or not parent:
        return child
    return f"{parent}.{child}"


def derive_probe_seeds(report: dict[str, Any]) -> list[dict[str, Any]]:
    """Compile high-value inspect clues into exact, unexecuted probe bundles."""

    diagnostics = [
        item for item in report.get("diagnostics", []) if isinstance(item, dict)
    ]
    unreachable = {
        str(item.get("refs", {}).get("state_path"))
        for item in diagnostics
        if item.get("code") == "W_UNREACHABLE_STATE"
        and isinstance(item.get("refs"), dict)
        and item.get("refs", {}).get("state_path")
    }
    seeds: list[dict[str, Any]] = []
    signatures: set[str] = set()

    def add(
        code: str, hypothesis: str, locations: list[str], checks: list[dict[str, Any]]
    ) -> None:
        signature = json.dumps(checks, ensure_ascii=False, sort_keys=True)
        if not checks or signature in signatures or len(seeds) >= 16:
            return
        signatures.add(signature)
        seeds.append(
            {
                "seed_id": f"PS-{len(seeds) + 1:02d}",
                "diagnostic_code": code,
                "hypothesis": hypothesis,
                "locations": locations,
                "checks": checks,
            }
        )

    for item in diagnostics:
        code = str(item.get("code") or "")
        refs = item.get("refs")
        refs = refs if isinstance(refs, dict) else {}
        if code == "W_UNREACHABLE_STATE":
            state = refs.get("state_path")
            if isinstance(state, str) and state:
                add(
                    code,
                    "The required state may be unreachable from root entry.",
                    [state],
                    [
                        {
                            "role": "primary",
                            "kind": "reaches",
                            "source": "[*]",
                            "target": state,
                            "within_cycles": 6,
                            "expected": True,
                        }
                    ],
                )
        elif code in {"W_DEADLOCK_LEAF", "W_TOPOLOGICAL_NOEXIT"}:
            state = refs.get("state_path") or refs.get("representative_state_path")
            if isinstance(state, str) and state and state not in unreachable:
                add(
                    code,
                    "A reachable state or cycle may have no behavior to a root terminator.",
                    [state],
                    [
                        {
                            "role": "precondition",
                            "kind": "reaches",
                            "source": "[*]",
                            "target": state,
                            "within_cycles": 6,
                            "expected": True,
                        },
                        {
                            "role": "primary",
                            "kind": "terminates",
                            "source": state,
                            "expected": True,
                        },
                    ],
                )
        elif code == "W_TRANSITION_SHADOWED":
            transition = refs.get("transition")
            transition = transition if isinstance(transition, dict) else {}
            parent = transition.get("parent")
            source = _child_path(parent, transition.get("from_state"))
            target = _child_path(parent, transition.get("to_state"))
            trigger = transition.get("event")
            if all(
                isinstance(value, str) and value for value in (source, target, trigger)
            ):
                add(
                    code,
                    "A declared event branch may never be selectable at runtime.",
                    [source, trigger, target],
                    [
                        {
                            "role": "precondition",
                            "kind": "event_consumed",
                            "source": source,
                            "trigger": trigger,
                            "expected": True,
                        },
                        {
                            "role": "primary",
                            "kind": "occupancy_after",
                            "source": source,
                            "trigger": trigger,
                            "target": target,
                            "within_cycles": 2,
                            "expected": True,
                        },
                    ],
                )
    return seeds


def _numbered(text: str, prefix: str) -> str:
    return "\n".join(
        f"{prefix}{index}: {line}" for index, line in enumerate(text.splitlines(), 1)
    )


def _nl_anchor_valid(pair: dict[str, Any], candidate: Any) -> bool:
    """Validate only citation provenance; never infer NL meaning."""

    quote = getattr(candidate, "nl_quote", None)
    if isinstance(quote, str) and quote:
        return quote in pair["nl"]
    return getattr(candidate, "basis_kind", None) != "nl_literal"


def _contract_nl_quote(pair: dict[str, Any], contract: Any) -> str:
    """Return an LLM-selected exact span, with physical-line replay fallback."""

    quote = getattr(contract, "nl_quote", None)
    if isinstance(quote, str) and quote:
        return quote
    nl_line = int(contract.nl_line)
    nl_lines = pair["nl"].splitlines()
    return nl_lines[nl_line - 1] if nl_line <= len(nl_lines) else f"NL{nl_line}"


def build_context(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    seeds: list[dict[str, Any]] | None = None,
) -> str:
    contract_summary = pair["working_contract"].get("summary", {})
    seeds = derive_probe_seeds(inspect) if seeds is None else seeds
    return (
        "# Natural-language requirements\n\n"
        f"{_numbered(pair['nl'], 'NL')}\n\n"
        "# Author-source PlantUML\n\n"
        f"{_numbered(pair['plantuml'], 'PUML')}\n\n"
        "# Converted FCSTM with source/compiler mapping comments\n\n"
        "`@map PUML:L<n> identity|lower:*|generated:*`; `F<n>` is the FCSTM line.\n\n"
        "```fcstm\n"
        f"{annotate_fcstm(pair['fcstm'], pair['working_contract'])}\n"
        "```\n\n"
        "# Conversion contract summary\n\n"
        f"{json.dumps(contract_summary, ensure_ascii=False, sort_keys=True)}\n\n"
        "# Execution/source attribution boundary\n\n"
        f"{json.dumps(compact_capability_boundary(pair['working_contract']), ensure_ascii=False, sort_keys=True)}\n\n"
        "# Verify-enabled pyfcstm inspect cause summary\n\n"
        f"{json.dumps(compact_inspect_for_planner(pair, inspect, seeds), ensure_ascii=False, sort_keys=True)}\n"
    )


def build_broad_context(pair: dict[str, Any]) -> str:
    return (
        "# Natural-language requirements\n\n"
        f"{_numbered(pair['nl'], 'NL')}\n\n"
        "# Author-source PlantUML\n\n"
        f"{_numbered(pair['plantuml'], 'PUML')}\n"
    )


def build_contract_context(pair: dict[str, Any]) -> str:
    return (
        f"# Numbered natural-language requirements\n\n{_numbered(pair['nl'], 'NL')}\n"
    )


def _semantic_grounding_inventory(pair: dict[str, Any]) -> dict[str, Any]:
    source = _source_model(pair)
    states = []
    for item in source.get("states", []):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            continue
        raw_ref = item.get("raw_ref")
        row = {
            "id": item["id"],
            "kind": item.get("kind"),
            "parent": item.get("parent"),
            "ref": _source_label(raw_ref) if isinstance(raw_ref, str) else None,
        }
        label = item.get("label")
        if isinstance(label, str) and label != item["id"].rsplit(".", 1)[-1]:
            row["label"] = label
        states.append({key: value for key, value in row.items() if value is not None})
    transitions = []
    for item in source.get("transitions", []):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            continue
        raw_ref = item.get("raw_ref")
        row = {
            "id": item["id"],
            "source": item.get("source"),
            "target": item.get("target"),
            "event": item.get("event"),
            "guard": item.get("guard"),
            "action": item.get("action"),
            "ref": _source_label(raw_ref) if isinstance(raw_ref, str) else None,
        }
        transitions.append(
            {key: value for key, value in row.items() if value is not None}
        )
    return {
        "root_scope_id": _source_root_scope_id(pair),
        "states": states,
        "final_states": source.get("final_states", []),
        "final_pseudostates": sorted(_source_final_target_ids(pair)),
        "concurrent_regions": source.get("concurrent_regions", []),
        "transitions": transitions,
    }


def build_semantic_grounding_context(
    pair: dict[str, Any],
    contract_plan: ContractExtractionPlan,
    evidence_plan: IssueDiscoveryPlan,
) -> str:
    payload = {
        "raw_contract_plan": contract_plan.model_dump(mode="json"),
        "raw_evidence_plan": evidence_plan.model_dump(mode="json"),
        "author_source_inventory": _semantic_grounding_inventory(pair),
    }
    return (
        "# Numbered natural-language requirements\n\n"
        f"{_numbered(pair['nl'], 'NL')}\n\n"
        "# Author-source PlantUML\n\n"
        f"{_numbered(pair['plantuml'], 'PUML')}\n\n"
        "# Plans and exact formal inventory\n\n"
        f"{json.dumps(payload, ensure_ascii=False, sort_keys=True)}\n"
    )


def build_discovery_grounding_context(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    contract_plan: ContractExtractionPlan,
) -> str:
    """Build the single cross-view discovery and semantic-grounding context."""

    payload = {
        "raw_nl_contract_plan": contract_plan.model_dump(
            mode="json", exclude_none=True
        ),
        "author_source_inventory": _semantic_grounding_inventory(pair),
    }
    return (
        f"{build_goal_context(pair, inspect)}\n\n"
        "# Raw NL-only contract plan and exact source inventory\n\n"
        f"{json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':'))}\n"
    )


def build_evidence_context(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    seeds: list[dict[str, Any]],
    broad_plan: BroadDiscoveryPlan,
) -> str:
    broad = [item.model_dump(mode="json") for item in broad_plan.candidates]
    return (
        f"{build_context(pair, inspect, seeds)}\n\n"
        "# Broad source-side candidates to upgrade or refute\n\n"
        f"{json.dumps(broad, ensure_ascii=False, sort_keys=True)}\n"
    )


PROOF_TEMPLATE_CATALOG = [
    {
        "template": "T01_initial_contract",
        "relations": ["initial_target"],
        "requires": ["subject=composite", "target=initial child"],
        "purpose": "initial target exists, is local, unique, and unconditional",
    },
    {
        "template": "T02_inventory_effect",
        "relations": [
            "state_exists",
            "final_pseudostate_exists",
            "variable_exists",
            "event_exists",
            "action_exists",
            "effect_exists",
        ],
        "requires": ["subject", "relation-specific variable/phase when needed"],
        "purpose": "declared elements, state actions, and transition effects",
    },
    {
        "template": "T03_transition_contract",
        "relations": [
            "transition_contract",
            "transition_exists",
            "transition_absent",
            "event_consumed",
            "event_consumed_in_scope",
        ],
        "requires": [
            "source and target; optional condition/trigger, or observed transition"
        ],
        "purpose": "required direct edge and, when stated, its condition slot",
    },
    {
        "template": "T04_containment_contract",
        "relations": ["contained_in", "child_count"],
        "requires": ["source=parent and target=child, or subject and count"],
        "purpose": "containment, region cardinality, and name binding",
    },
    {
        "template": "T05_label_semantics",
        "relations": [
            "guard_present",
            "completion_transition_fireable",
            "action_exists",
            "effect_exists",
        ],
        "requires": [
            "source and target for guard_present; exact observed transition for completion semantics"
        ],
        "purpose": "trigger, guard, effect, and action label slots",
    },
    {
        "template": "T06_guard_determinism",
        "relations": ["guards_distinguishable"],
        "requires": ["source"],
        "purpose": "same-(source,event) branches are mutually exclusive or prioritized",
    },
    {
        "template": "T07_topology_entry",
        "relations": ["initial_target", "contained_in"],
        "requires": ["subject and target, or source and target"],
        "purpose": "local entry target, ancestor re-entry, and scope legality",
    },
    {
        "template": "T08_reachable_then_escapable",
        "relations": ["state_escapable"],
        "requires": ["subject=state"],
        "purpose": "a reachable non-final state has a continuation or termination",
    },
    {
        "template": "T09_reachability_certificate",
        "relations": ["target_reachable"],
        "requires": ["target"],
        "purpose": "required behavior is reachable or has an absence cut",
    },
    {
        "template": "T10_stable_termination",
        "relations": ["termination_target", "eventually_terminates"],
        "requires": ["subject=scope or state"],
        "purpose": "no reachable closed completion cycle or non-progress trap",
    },
    {
        "template": "T11_wrong_target_after_event",
        "relations": ["event_reaches_target", "event_avoids_scope"],
        "requires": [
            "source, trigger, target; or observed transition and forbidden scope"
        ],
        "purpose": "an event reaches the required target under the mapped runtime",
    },
    {
        "template": "T12_event_response",
        "relations": ["event_consumed", "eventually_responds"],
        "requires": ["source and trigger, or trigger and response"],
        "purpose": "an event is consumed and receives its required response",
    },
    {
        "template": "T13_transition_target_consistency",
        "relations": ["transition_target_consistency"],
        "requires": [
            "observed_transition_id, reference_transition_id, and normative target"
        ],
        "purpose": (
            "two LLM-judged same-role behaviors realize one target role in the "
            "author source and mapped FCSTM"
        ),
    },
]


def build_goal_context(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    seeds: list[dict[str, Any]] | None = None,
) -> str:
    """Build the one-call semantic planning context.

    Deterministic scouts are summarized as a frontier. The LLM can reason from
    their facts but cannot select their execution or suppress their execution.
    """

    del seeds
    progressive = derive_progressive_evidence_seeds(pair, inspect)
    frontier = [
        {
            "cause_key": item.get("cause_key"),
            "obligation": item.get("obligation"),
            "claim": item.get("claim"),
            "locations": item.get("locations", []),
            "source_cause": {
                key: certificate.get(key)
                for key in ("kind", "scope", "target", "component", "sound_for_claim")
                if certificate.get(key) is not None
            }
            if isinstance(certificate := item.get("source_causality_certificate"), dict)
            else None,
        }
        for item in progressive
    ]
    diagnostic_counts: dict[str, int] = {}
    for item in inspect.get("diagnostics", []):
        if not isinstance(item, dict):
            continue
        code = str(item.get("code") or "UNKNOWN")
        diagnostic_counts[code] = diagnostic_counts.get(code, 0) + 1
    inspect_summary = {
        "status": inspect.get("status"),
        "metrics": inspect.get("metrics", {}),
        "diagnostic_counts": diagnostic_counts,
        "deterministic_frontier": frontier,
    }
    return (
        "# Natural-language requirements\n\n"
        f"{_numbered(pair['nl'], 'NL')}\n\n"
        "# Author-source PlantUML\n\n"
        f"{_numbered(pair['plantuml'], 'PUML')}\n\n"
        "# Converted FCSTM with source/compiler mapping comments\n\n"
        "`@map PUML:L<n> identity|lower:*|generated:*`; `F<n>` is the FCSTM line.\n\n"
        "```fcstm\n"
        f"{annotate_fcstm(pair['fcstm'], pair['working_contract'])}\n"
        "```\n\n"
        "# Execution/source-attribution boundary\n\n"
        f"{json.dumps(compact_capability_boundary(pair['working_contract']), ensure_ascii=False, sort_keys=True, separators=(',', ':'))}\n\n"
        "# Verify-enabled pyfcstm inspect summary\n\n"
        f"{json.dumps(inspect_summary, ensure_ascii=False, sort_keys=True, separators=(',', ':'))}\n"
    )


def _quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


PREDICATE_SIGNATURES: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "state_declared": (("state", "kind"), ()),
    "variable_declared": (("variable",), ()),
    "event_declared": (("event",), ()),
    "containment": (("parent", "child"), ()),
    "initial_target": (("composite", "child"), ()),
    "edge_declared": (("source", "trigger", "target"), ()),
    "effect_declared": (("source", "trigger", "variable", "sign"), ()),
    "action_declared": (("state", "phase"), ("action",)),
    "guard_distinguishable": (("source", "trigger"), ()),
    "cardinality": (("scope", "count"), ()),
    "occupancy_after": (
        ("source", "trigger", "target"),
        ("within_cycles",),
    ),
    "event_consumed": (("source", "trigger"), ()),
    "stays_in": (("source", "trigger"), ()),
    "variable_delta_after": (("source", "trigger", "variable", "sign"), ()),
    "reaches": (("source", "target"), ("within_cycles",)),
    "terminates": (("scope",), ("trigger",)),
    "invariant": (("scope", "condition"), ("bound",)),
    "response_within": (("trigger", "response"), ("bound", "source")),
    "persists_until": (("state", "release"), ("bound",)),
}


TEMPLATE_BACKENDS: dict[str, str] = {
    "T01_initial_contract": "A_artifact_static",
    "T02_inventory_effect": "A_artifact_static",
    "T03_transition_contract": "A_artifact_static",
    "T04_containment_contract": "A_artifact_static",
    "T05_label_semantics": "A_artifact_static",
    "T06_guard_determinism": "Z_guard_solver",
    "T07_topology_entry": "A_artifact_static",
    "T08_reachable_then_escapable": "G_topology_proof",
    "T09_reachability_certificate": "G_topology_proof",
    "T10_stable_termination": "G_topology_proof",
    "T11_wrong_target_after_event": "T_fcstm_trace",
    "T12_event_response": "T_fcstm_trace_fbmcq",
    "T13_transition_target_consistency": "A_artifact_static",
}

TEMPLATE_BY_RELATION: dict[str, ProofTemplate] = {
    "initial_target": "T01_initial_contract",
    "state_exists": "T02_inventory_effect",
    "final_pseudostate_exists": "T02_inventory_effect",
    "variable_exists": "T02_inventory_effect",
    "event_exists": "T02_inventory_effect",
    "action_exists": "T02_inventory_effect",
    "effect_exists": "T02_inventory_effect",
    "transition_contract": "T03_transition_contract",
    "transition_exists": "T03_transition_contract",
    "transition_absent": "T03_transition_contract",
    "transition_target_consistency": "T13_transition_target_consistency",
    "completion_transition_fireable": "T05_label_semantics",
    "contained_in": "T04_containment_contract",
    "child_count": "T04_containment_contract",
    "guard_present": "T05_label_semantics",
    "guards_distinguishable": "T06_guard_determinism",
    "state_escapable": "T08_reachable_then_escapable",
    "target_reachable": "T09_reachability_certificate",
    "termination_target": "T10_stable_termination",
    "eventually_terminates": "T10_stable_termination",
    "event_reaches_target": "T11_wrong_target_after_event",
    "event_avoids_scope": "T11_wrong_target_after_event",
    "event_consumed": "T12_event_response",
    "event_consumed_in_scope": "T03_transition_contract",
    "eventually_responds": "T12_event_response",
}

ALLOWED_RELATIONS_BY_OBLIGATION: dict[str, frozenset[GoalRelation]] = {
    "element:exists:state": frozenset({"state_exists"}),
    "element:exists:final_pseudostate": frozenset({"final_pseudostate_exists"}),
    "element:exists:variable": frozenset({"variable_exists"}),
    "element:exists:event": frozenset({"event_exists"}),
    "element:exists:action": frozenset({"action_exists"}),
    "element:exists:effect": frozenset({"effect_exists"}),
    "element:exists:transition": frozenset({"transition_exists"}),
    "element:absent:transition": frozenset({"transition_absent"}),
    "element:cardinality:state": frozenset({"child_count"}),
    "attachment:containment": frozenset({"contained_in"}),
    "attachment:initial_target": frozenset({"initial_target"}),
    "attachment:transition_endpoints": frozenset(
        {"transition_contract", "transition_exists"}
    ),
    "attachment:transition_target_consistency": frozenset(
        {"transition_target_consistency"}
    ),
    "attachment:trigger": frozenset(
        {"transition_contract", "event_consumed", "event_consumed_in_scope"}
    ),
    "attachment:guard": frozenset(
        {"guard_present", "transition_contract", "completion_transition_fireable"}
    ),
    "attachment:effect": frozenset({"effect_exists", "transition_contract"}),
    "attachment:action_phase": frozenset({"action_exists"}),
    "guard_set:disjoint": frozenset({"guards_distinguishable"}),
    "graph:reachable": frozenset({"target_reachable"}),
    "graph:target_reachable": frozenset({"target_reachable"}),
    "graph:deadlock_free": frozenset({"state_escapable"}),
    "graph:escapable": frozenset({"state_escapable"}),
    "graph:stable_termination": frozenset({"termination_target"}),
    "graph:path_absent": frozenset({"transition_absent", "event_avoids_scope"}),
    "graph:event_target_reachable": frozenset({"event_reaches_target"}),
    "graph:event_consumer_reachable": frozenset(
        {"event_consumed", "event_consumed_in_scope"}
    ),
    "temporal:response": frozenset({"event_reaches_target", "eventually_responds"}),
    "temporal:absence": frozenset({"event_avoids_scope"}),
    "temporal:termination": frozenset({"termination_target", "eventually_terminates"}),
}


# This registry is deliberately independent from lowering compatibility.  A
# compatible relation is executable only after its exact operator has a
# preregistered soundness fragment; adding a relation to the lowering table must
# not silently raise its W ceiling.
EXECUTABLE_OBLIGATION_SIGNATURES = frozenset(
    {
        "element:exists:state",
        "element:exists:final_pseudostate",
        "element:exists:variable",
        "element:exists:event",
        "element:exists:action",
        "element:exists:effect",
        "element:exists:transition",
        "element:absent:transition",
        "element:cardinality:state",
        "attachment:containment",
        "attachment:initial_target",
        "attachment:transition_endpoints",
        "attachment:transition_target_consistency",
        "attachment:trigger",
        "attachment:guard",
        "attachment:effect",
        "attachment:action_phase",
        "guard_set:disjoint",
        "graph:reachable",
        "graph:target_reachable",
        "graph:deadlock_free",
        "graph:escapable",
        "graph:stable_termination",
        "graph:path_absent",
        "graph:event_target_reachable",
        "graph:event_consumer_reachable",
        "temporal:response",
        "temporal:absence",
        "temporal:termination",
    }
)


def _obligation_signature(obligation: DomainObligation) -> str:
    if isinstance(obligation, ElementObligation):
        return f"element:{obligation.operator}:{obligation.element_kind}"
    if isinstance(obligation, AttachmentObligation):
        return f"attachment:{obligation.attachment}"
    if isinstance(obligation, GuardSetObligation):
        return f"guard_set:{obligation.property}"
    if isinstance(obligation, GraphObligation):
        return f"graph:{obligation.property}"
    return f"temporal:{obligation.pattern}"


def obligation_surface_role(obligation: DomainObligation) -> ObligationSurfaceRole:
    """Return the provenance-backed role of an obligation operator."""

    signature = _obligation_signature(obligation)
    if signature in {
        "element:absent:state",
        "element:absent:final_pseudostate",
        "element:absent:event",
        "element:absent:variable",
        "element:absent:action",
        "element:absent:effect",
        "element:absent:transition",
        "graph:escapable",
        "graph:stable_termination",
        "graph:event_target_reachable",
        "temporal:termination",
        "temporal:persistence",
    }:
        return "derived_macro"
    if signature.startswith("element:kind_is:") or signature in {
        "guard_set:equivalent",
        "guard_set:implies",
        "graph:event_consumer_reachable",
    }:
        return "backend_comparison"
    if signature in {
        "element:cardinality:state",
        "attachment:containment",
    }:
        return "under_supported_extension"
    return "core"


def validate_domain_obligation_lowering(candidate: EvidenceCandidate) -> list[str]:
    """Check operator-level compiler compatibility, never free-text semantics."""

    obligation = candidate.domain_obligation
    if obligation is None:
        return []
    signature = _obligation_signature(obligation)
    allowed = ALLOWED_RELATIONS_BY_OBLIGATION.get(signature, frozenset())
    if candidate.goal.relation not in allowed:
        return [
            (
                f"domain obligation {signature!r} cannot lower to compiler relation "
                f"{candidate.goal.relation!r}; allowed relations are {sorted(allowed)}"
            )
        ]

    goal = candidate.goal
    errors: list[str] = []
    if (
        isinstance(obligation, TemporalObligation)
        and obligation.pattern == "termination"
    ):
        if obligation.state_ref is not None and goal.relation != "termination_target":
            errors.append(
                "typed temporal termination with a named state_ref must lower to "
                "termination_target, not a whole-machine termination relation"
            )
        if obligation.state_ref is None and goal.relation == "termination_target":
            errors.append(
                "termination_target requires a typed temporal termination state_ref"
            )
    bindings: list[tuple[str, Any, Any]] = []
    if isinstance(obligation, ElementObligation):
        goal_subject = (
            goal.observed_transition_id
            if obligation.element_kind == "transition"
            and obligation.operator == "absent"
            else goal.subject
        )
        bindings.extend(
            [
                ("subject_ref", obligation.subject_ref, goal_subject),
                ("expected_count", obligation.expected_count, goal.count),
            ]
        )
    elif isinstance(obligation, AttachmentObligation):
        if obligation.attachment == "containment":
            bindings.extend(
                [
                    ("subject_ref", obligation.subject_ref, goal.subject),
                    ("owner_ref", obligation.owner_ref, goal.target),
                ]
            )
        elif obligation.attachment == "initial_target":
            # Some live responses historically copied the two exact IDs into
            # the typed fields in owner/subject order. When both IDs are the
            # goal's exact endpoints, this is a schema-direction error rather
            # than a semantic ambiguity; accept it as a recorded field alias.
            initial_pairs = {
                (obligation.subject_ref, obligation.owner_ref),
                (obligation.owner_ref, obligation.subject_ref),
            }
            expected_pair = (goal.target, goal.subject)
            if expected_pair in initial_pairs or (
                obligation.owner_ref == goal.subject
                and obligation.subject_ref in {None, goal.subject}
            ):
                # The goal's exact child binding remains the executable source
                # of truth when the audit object omitted or duplicated it.
                pass
            else:
                bindings.extend(
                    [
                        ("subject_ref", obligation.subject_ref, goal.target),
                        ("owner_ref", obligation.owner_ref, goal.subject),
                    ]
                )
        elif obligation.attachment == "transition_target_consistency":
            bindings.extend(
                [
                    (
                        "subject_ref",
                        obligation.subject_ref,
                        goal.observed_transition_id,
                    ),
                    (
                        "reference_ref",
                        obligation.reference_ref,
                        goal.reference_transition_id,
                    ),
                    ("owner_ref", obligation.owner_ref, goal.target),
                ]
            )
        elif obligation.attachment in {"trigger", "guard", "effect"}:
            bindings.append(
                ("subject_ref", obligation.subject_ref, goal.observed_transition_id)
            )
        elif obligation.attachment == "action_phase":
            bindings.extend(
                [
                    ("subject_ref", obligation.subject_ref, goal.subject),
                    ("action_ref", obligation.action_ref, goal.action),
                    ("phase", obligation.phase, goal.phase),
                ]
            )
    elif isinstance(obligation, GuardSetObligation):
        bindings.append(("scope_ref", obligation.scope_ref, goal.source))
    elif isinstance(obligation, GraphObligation):
        if obligation.property == "stable_termination" and goal.relation == "termination_target":
            bindings.extend(
                [
                    ("target_ref", obligation.target_ref, goal.subject),
                    ("bound", obligation.bound, goal.within_cycles),
                ]
            )
        elif obligation.property in {"deadlock_free", "escapable"} and goal.relation == "state_escapable":
            bindings.extend(
                [
                    ("source_ref", obligation.source_ref, goal.subject),
                    ("bound", obligation.bound, goal.within_cycles),
                ]
            )
        else:
            bindings.extend(
                [
                    ("source_ref", obligation.source_ref, goal.source),
                    ("target_ref", obligation.target_ref, goal.target),
                    (
                        "forbidden_scope_ref",
                        obligation.forbidden_scope_ref,
                        goal.forbidden_scope,
                    ),
                    ("bound", obligation.bound, goal.within_cycles),
                ]
            )
    elif isinstance(obligation, TemporalObligation):
        bindings.extend(
            [
                ("trigger_ref", obligation.trigger_ref, goal.trigger),
                (
                    "response_ref",
                    obligation.response_ref,
                    goal.response or goal.target,
                ),
                ("state_ref", obligation.state_ref, goal.subject or goal.target),
                (
                    "scope_ref",
                    obligation.scope_ref,
                    goal.source or goal.forbidden_scope,
                ),
                ("bound", obligation.bound, goal.within_cycles),
            ]
        )
    errors.extend(
        f"typed binding {name}={typed!r} does not equal lowering binding {lowered!r}"
        for name, typed, lowered in bindings
        if typed is not None and typed != lowered
    )
    return errors


def validate_operator_executable_soundness(
    candidate: EvidenceCandidate,
) -> list[str]:
    """Fail closed when an operator fragment is not implemented soundly."""

    goal = candidate.goal
    obligation = candidate.domain_obligation
    if obligation is None:
        if goal.relation == "target_reachable" and goal.within_cycles is not None:
            return [
                (
                    "bounded target_reachable requires a bounded trace backend; "
                    "the topology backend is unbounded"
                )
            ]
        if goal.relation == "effect_exists" and goal.sign == "changed":
            return [
                (
                    "effect_exists sign='changed' has no registered sound runtime "
                    "operator; use a supported directional effect or retain W1"
                )
            ]
        return []

    signature = _obligation_signature(obligation)
    if signature not in EXECUTABLE_OBLIGATION_SIGNATURES:
        return [
            (
                f"domain obligation {signature!r} has no registered executable "
                "soundness fragment"
            )
        ]

    errors: list[str] = []
    if goal.relation == "effect_exists" and goal.sign == "changed":
        errors.append(
            "effect_exists sign='changed' has no registered sound runtime operator"
        )
    if isinstance(obligation, GuardSetObligation):
        exact_refs = list(dict.fromkeys(obligation.transition_refs))
        if obligation.scope_ref in {None, ""}:
            errors.append("guard_set:disjoint requires an exact typed scope_ref")
        if len(exact_refs) < 2:
            errors.append(
                "guard_set:disjoint requires at least two exact transition_refs"
            )
        if len(exact_refs) != len(obligation.transition_refs):
            errors.append("guard_set:disjoint transition_refs must be unique")
        binding_ids = [binding.transition_id for binding in obligation.guard_bindings]
        if len(binding_ids) != len(set(binding_ids)):
            errors.append("guard_set:disjoint guard_bindings must be unique")
        if set(binding_ids) != set(exact_refs):
            errors.append(
                "guard_set:disjoint requires one explicit guard_binding for every "
                "exact transition_ref"
            )
        if any(binding.semantic_role != "guard_condition" for binding in obligation.guard_bindings):
            errors.append("guard_set guard_bindings must declare semantic_role=guard_condition")
    if isinstance(obligation, GraphObligation):
        if obligation.property in {"deadlock_free", "escapable"}:
            if goal.relation != "state_escapable":
                errors.append("graph deadlock/escapable obligations require state_escapable")
            if obligation.source_ref in {None, ""}:
                errors.append("graph:deadlock_free requires a typed source_ref")
            if obligation.source_ref != goal.subject:
                errors.append("graph:deadlock_free source_ref must equal goal.subject")
            if obligation.expected != goal.expected:
                errors.append("graph:deadlock_free typed expected value must equal goal.expected")
            if obligation.bound is not None or goal.within_cycles is not None:
                errors.append("bounded graph:deadlock_free has no registered topology soundness fragment")
        elif obligation.property in {"reachable", "target_reachable"}:
            if obligation.target_ref in {None, ""}:
                errors.append("graph reachability requires a typed target_ref")
            if obligation.source_ref is None and goal.source is not None:
                errors.append(
                    "graph reachability goal.source requires a matching typed source_ref"
                )
            if obligation.expected != goal.expected:
                errors.append(
                    "graph reachability typed expected value must equal goal.expected"
                )
            if obligation.expected is not True:
                errors.append(
                    "graph reachability execution supports required "
                    "reachability only; forbidden paths require graph:path_absent"
                )
            if obligation.bound is not None or goal.within_cycles is not None:
                errors.append(
                    "bounded graph reachability requires a bounded trace backend; "
                    "the topology backend is unbounded"
                )
        elif obligation.property == "stable_termination":
            if obligation.target_ref in {None, ""}:
                errors.append("graph:stable_termination requires a typed target_ref")
            if obligation.source_ref is not None or goal.source is not None:
                errors.append(
                    "graph:stable_termination is defined from its target to root "
                    "termination and does not support a source_ref"
                )
            if obligation.bound is not None or goal.within_cycles is not None:
                errors.append(
                    "bounded graph:stable_termination has no registered topology "
                    "soundness fragment"
                )
        elif obligation.property == "event_consumer_reachable":
            if obligation.source_ref in {None, ""}:
                errors.append(
                    "graph:event_consumer_reachable requires an exact typed source_ref"
                )
            if goal.observed_transition_id in {None, ""}:
                errors.append(
                    "graph:event_consumer_reachable requires an exact observed "
                    "transition ID to bind event identity"
                )
            if obligation.expected != goal.expected or goal.expected is not True:
                errors.append(
                    "graph:event_consumer_reachable supports required event "
                    "consumption only and typed expected must equal goal.expected=True"
                )
            if obligation.target_ref is not None or obligation.bound is not None:
                errors.append(
                    "graph:event_consumer_reachable does not accept target_ref or bound"
                )
    return errors


def derive_support_disposition(
    candidate: EvidenceCandidate,
    lowering_errors: list[str],
) -> SupportDisposition:
    """Derive the W ceiling from formal support and localization only."""

    obligation = candidate.domain_obligation
    role: ObligationSurfaceRole | Literal["legacy_untyped"] = (
        obligation_surface_role(obligation)
        if obligation is not None
        else "legacy_untyped"
    )
    soundness_errors = validate_operator_executable_soundness(candidate)
    if not lowering_errors and not soundness_errors:
        return SupportDisposition(
            status="executable",
            w_ceiling="W2",
            surface_role=role,
            reason_code=(
                "sound_lowering_available"
                if obligation is not None
                else "legacy_replay"
            ),
            reason=(
                "A preregistered operator-level lowering is available."
                if obligation is not None
                else "Legacy replay remains executable under its frozen compiler relation."
            ),
        )
    if candidate.locations:
        return SupportDisposition(
            status="located_only",
            w_ceiling="W1",
            surface_role=role,
            reason_code="no_sound_lowering",
            reason="The obligation is localized but has no sound registered lowering.",
        )
    return SupportDisposition(
        status="prose_only",
        w_ceiling="W0",
        surface_role=role,
        reason_code="no_sound_lowering",
        reason="The obligation has neither a sound registered lowering nor localization.",
    )


def _goal_value(goal: EvidenceGoal, name: str) -> Any:
    return getattr(goal, name)


def _require_goal_fields(goal: EvidenceGoal, *names: str) -> list[str]:
    return [name for name in names if _goal_value(goal, name) in {None, ""}]


def compile_evidence_goal(goal: EvidenceGoal) -> dict[str, Any]:
    """Compile one semantic goal into a fixed method-owned route."""

    template = TEMPLATE_BY_RELATION[goal.relation]
    backend = TEMPLATE_BACKENDS[template]
    checks: list[ProbeCheck] = []
    missing: list[str] = []
    relation = goal.relation

    if relation == "initial_target":
        missing = _require_goal_fields(goal, "subject", "target")
        if not missing:
            checks = [
                ProbeCheck(
                    kind="initial_target",
                    bindings={"composite": goal.subject, "child": goal.target},
                    expected=goal.expected,
                )
            ]
    elif relation == "state_exists":
        missing = _require_goal_fields(goal, "subject")
        if not missing:
            checks = [
                ProbeCheck(
                    kind="state_declared",
                    bindings={"state": goal.subject, "kind": "any"},
                    expected=goal.expected,
                )
            ]
    elif relation == "final_pseudostate_exists":
        missing = _require_goal_fields(goal, "source")
    elif relation == "variable_exists":
        variable = goal.variable or goal.subject
        missing = ["variable"] if variable in {None, ""} else []
        if not missing:
            checks = [
                ProbeCheck(
                    kind="variable_declared",
                    bindings={"variable": variable},
                    expected=goal.expected,
                )
            ]
    elif relation == "event_exists":
        missing = _require_goal_fields(goal, "subject")
        if not missing:
            checks = [
                ProbeCheck(
                    kind="event_declared",
                    bindings={"event": goal.subject},
                    expected=goal.expected,
                )
            ]
    elif relation == "action_exists":
        missing = _require_goal_fields(goal, "subject", "action")
        if not missing:
            checks = [
                ProbeCheck(
                    kind="action_declared",
                    bindings={
                        "state": goal.subject,
                        **(
                            {"phase": goal.phase}
                            if goal.phase not in {None, ""}
                            else {}
                        ),
                        **(
                            {"action": goal.action}
                            if goal.action not in {None, ""}
                            else {}
                        ),
                    },
                    expected=goal.expected,
                )
            ]
    elif relation == "effect_exists":
        missing = _require_goal_fields(goal, "source", "trigger", "variable", "sign")
        if not missing:
            checks = [
                ProbeCheck(
                    kind="effect_declared",
                    bindings={
                        "source": goal.source,
                        "trigger": goal.trigger,
                        "variable": goal.variable,
                        "sign": goal.sign,
                    },
                    expected=goal.expected,
                )
            ]
    elif relation in {"transition_contract", "transition_exists"}:
        missing = _require_goal_fields(goal, "source", "target")
    elif relation in {"transition_absent", "completion_transition_fireable"}:
        missing = _require_goal_fields(goal, "observed_transition_id")
    elif relation == "transition_target_consistency":
        missing = _require_goal_fields(
            goal,
            "observed_transition_id",
            "reference_transition_id",
            "target",
        )
    elif relation == "contained_in":
        child = goal.subject or goal.source
        missing = [
            name
            for name, value in (("subject", child), ("target", goal.target))
            if value in {None, ""}
        ]
        if not missing:
            checks = [
                ProbeCheck(
                    kind="containment",
                    bindings={"parent": goal.target, "child": child},
                    expected=goal.expected,
                )
            ]
    elif relation == "child_count":
        missing = _require_goal_fields(goal, "subject", "count")
        if not missing:
            checks = [
                ProbeCheck(
                    kind="cardinality",
                    bindings={"scope": goal.subject, "count": goal.count},
                    expected=goal.expected,
                )
            ]
    elif relation == "guards_distinguishable":
        missing = _require_goal_fields(goal, "source")
    elif relation == "guard_present":
        missing = _require_goal_fields(goal, "source", "target")
    elif relation == "target_reachable":
        target = goal.target or goal.subject
        missing = ["target"] if target in {None, ""} else []
    elif relation == "state_escapable":
        missing = _require_goal_fields(goal, "subject")
    elif relation == "event_reaches_target":
        missing = _require_goal_fields(goal, "source", "trigger", "target")
        if not missing:
            checks = [
                ProbeCheck(
                    role="precondition",
                    kind="reaches",
                    source="[*]",
                    target=goal.source,
                    within_cycles=goal.within_cycles or 6,
                ),
                ProbeCheck(
                    role="primary",
                    kind="occupancy_after",
                    source=goal.source,
                    trigger=goal.trigger,
                    target=goal.target,
                    within_cycles=goal.within_cycles or 3,
                    expected=goal.expected,
                ),
            ]
    elif relation == "event_avoids_scope":
        missing = _require_goal_fields(
            goal, "source", "forbidden_scope", "observed_transition_id"
        )
    elif relation in {"event_consumed", "event_consumed_in_scope"}:
        missing = _require_goal_fields(goal, "source", "trigger")
        if relation == "event_consumed_in_scope" and not goal.observed_transition_id:
            missing.append("observed_transition_id")
        if not missing:
            checks = [
                ProbeCheck(
                    role="precondition",
                    kind="reaches",
                    source="[*]",
                    target=goal.source,
                    within_cycles=goal.within_cycles or 6,
                ),
                ProbeCheck(
                    role="primary",
                    kind="event_consumed",
                    source=goal.source,
                    trigger=goal.trigger,
                    expected=goal.expected,
                ),
            ]
    elif relation == "eventually_responds":
        missing = _require_goal_fields(goal, "trigger", "response")
        if not missing:
            bindings: dict[str, str | int] = {
                "trigger": goal.trigger,
                "response": goal.response,
                "bound": goal.within_cycles or 8,
            }
            if goal.source:
                bindings["source"] = goal.source
            checks = [
                ProbeCheck(
                    kind="response_within",
                    bindings=bindings,
                    expected=goal.expected,
                )
            ]
    elif relation in {"termination_target", "eventually_terminates"}:
        missing = _require_goal_fields(goal, "subject")

    errors = []
    if missing:
        errors.append(f"{relation} requires field(s): {', '.join(missing)}")
    return {
        "schema": "paper1.evidence_route.v1",
        "template": template,
        "ignored_template_hint": None,
        "relation": relation,
        "backend": backend,
        "operation": (
            "topology_certificate"
            if backend == "G_topology_proof"
            else "guard_solver"
            if backend == "Z_guard_solver"
            else "artifact_static"
            if backend == "A_artifact_static" and not checks
            else "predicate_bundle"
        ),
        "checks": checks,
        "errors": errors,
        "goal": goal.model_dump(mode="json"),
    }


def _source_transition_by_id(
    pair: dict[str, Any], transition_id: str
) -> dict[str, Any] | None:
    matches = [
        item
        for item in _source_model(pair).get("transitions", [])
        if isinstance(item, dict) and item.get("id") == transition_id
    ]
    return matches[0] if len(matches) == 1 else None


def _transition_binding_error(
    pair: dict[str, Any],
    transition_id: str,
    *,
    source: str | None = None,
    target: str | None = None,
) -> str | None:
    transition = _source_transition_by_id(pair, transition_id)
    if transition is None:
        return f"source transition ID does not exist exactly: {transition_id}"
    if source is not None and transition.get("source") != source:
        return (
            f"transition {transition_id} source is {transition.get('source')!r}, "
            f"not {source!r}"
        )
    if target is not None and transition.get("target") != target:
        return (
            f"transition {transition_id} target is {transition.get('target')!r}, "
            f"not {target!r}"
        )
    return None


def _validate_grounded_contract_plan(
    pair: dict[str, Any],
    plan: ContractExtractionPlan,
    concept_bindings: list[SemanticConceptBinding] | None = None,
) -> tuple[GroundedContractPlan, list[dict[str, str]]]:
    state_ids = _source_state_ids(pair)
    final_target_ids = _source_final_target_ids(pair)
    scope_ids = set(state_ids)
    root_scope_id = _source_root_scope_id(pair)
    if root_scope_id is not None:
        scope_ids.add(root_scope_id)
    diagnostics: list[dict[str, str]] = []
    concept_rows: dict[str, list[SemanticConceptBinding]] = {}
    for binding in concept_bindings or []:
        concept_rows.setdefault(binding.concept_id, []).append(binding)
    concept_map: dict[str, str] = {}
    for concept_id, rows in concept_rows.items():
        if len(rows) != 1:
            diagnostics.append(
                {
                    "stage": "semantic_grounding",
                    "class": "concept_binding_duplicate",
                    "message": f"concept {concept_id} must be bound exactly once",
                }
            )
            continue
        source_state_id = rows[0].source_state_id
        if source_state_id not in scope_ids | final_target_ids:
            diagnostics.append(
                {
                    "stage": "semantic_grounding",
                    "class": "formal_id_invalid",
                    "message": (
                        f"concept {concept_id} is not bound to an exact source "
                        f"state ID: {source_state_id}"
                    ),
                }
            )
            continue
        concept_map[concept_id] = source_state_id

    def concept_error(concept_id: str | None, formal_id: str, field: str) -> str | None:
        if concept_id is None:
            return None
        bound = concept_map.get(concept_id)
        if bound is None:
            return f"{field} uses unbound concept ID {concept_id}"
        if bound != formal_id:
            return (
                f"{field}={formal_id!r} disagrees with {concept_id} binding {bound!r}"
            )
        return None

    initial_contracts = []
    for index, contract in enumerate(plan.initial_contracts):
        missing = [
            field
            for field, value, inventory in (
                ("composite", contract.composite, scope_ids),
                ("target", contract.target, state_ids),
            )
            if value not in inventory
        ]
        concept_errors = [
            error
            for error in (
                concept_error(
                    contract.composite_concept_id,
                    contract.composite,
                    "composite",
                ),
                concept_error(contract.target_concept_id, contract.target, "target"),
            )
            if error
        ]
        if missing or concept_errors:
            diagnostics.append(
                {
                    "stage": "semantic_grounding",
                    "class": "formal_id_invalid",
                    "message": (
                        f"initial_contracts[{index}] lacks exact source state ID(s): "
                        f"{', '.join(missing)}"
                        + (f"; {'; '.join(concept_errors)}" if concept_errors else "")
                    ),
                }
            )
            continue
        initial_contracts.append(contract)

    containment_contracts = []
    for index, contract in enumerate(plan.containment_contracts):
        missing = [
            field
            for field, value, inventory in (
                ("parent", contract.parent, scope_ids),
                ("child", contract.child, state_ids),
            )
            if value not in inventory
        ]
        concept_errors = [
            error
            for error in (
                concept_error(contract.parent_concept_id, contract.parent, "parent"),
                concept_error(contract.child_concept_id, contract.child, "child"),
            )
            if error
        ]
        if missing or concept_errors:
            diagnostics.append(
                {
                    "stage": "semantic_grounding",
                    "class": "formal_id_invalid",
                    "message": (
                        f"containment_contracts[{index}] lacks exact source state "
                        f"ID(s): {', '.join(missing)}"
                        + (f"; {'; '.join(concept_errors)}" if concept_errors else "")
                    ),
                }
            )
            continue
        containment_contracts.append(contract)

    transition_groups = []
    for group_index, group in enumerate(plan.transition_groups):
        source_concept_error = concept_error(
            group.source_concept_id, group.source, "source"
        )
        if group.source not in state_ids or source_concept_error:
            diagnostics.append(
                {
                    "stage": "semantic_grounding",
                    "class": "formal_id_invalid",
                    "message": (
                        f"transition_groups[{group_index}].source is not an exact "
                        f"source state ID: {group.source}"
                        + (f"; {source_concept_error}" if source_concept_error else "")
                    ),
                }
            )
            continue
        targets = []
        for target_index, target in enumerate(group.targets):
            target_concept_error = concept_error(
                target.target_concept_id, target.target, "target"
            )
            if (
                target.target not in state_ids | final_target_ids
                or target_concept_error
            ):
                diagnostics.append(
                    {
                        "stage": "semantic_grounding",
                        "class": "formal_id_invalid",
                        "message": (
                            f"transition_groups[{group_index}].targets[{target_index}] "
                            f"is not an exact source state ID: {target.target}"
                            + (
                                f"; {target_concept_error}"
                                if target_concept_error
                                else ""
                            )
                        ),
                    }
                )
                continue
            if target.observed_transition_id:
                error = _transition_binding_error(pair, target.observed_transition_id)
                if error:
                    diagnostics.append(
                        {
                            "stage": "semantic_grounding",
                            "class": "formal_transition_inconsistent",
                            "message": (
                                f"transition_groups[{group_index}].targets"
                                f"[{target_index}]: {error}"
                            ),
                        }
                    )
                    continue
            if target.formal_condition is not None:
                observed = (
                    _source_transition_by_id(pair, target.observed_transition_id)
                    if target.observed_transition_id
                    else None
                )
                if not isinstance(observed, dict) or not (
                    _source_transition_guard_matches(observed, target.formal_condition)
                    if target.condition_role == "qualified_guard"
                    else _source_transition_condition_matches(
                        pair, observed, target.formal_condition
                    )
                ):
                    diagnostics.append(
                        {
                            "stage": "semantic_grounding",
                            "class": "formal_condition_inconsistent",
                            "message": (
                                f"transition_groups[{group_index}].targets"
                                f"[{target_index}] condition_binding is not the exact "
                                "event/raw label of observed_transition_id"
                            ),
                        }
                    )
                    target = target.model_copy(update={"formal_condition": None})
            targets.append(target)
        if targets:
            transition_groups.append(
                group.model_copy(deep=True, update={"targets": targets})
            )
    return (
        GroundedContractPlan(
            initial_contracts=initial_contracts,
            containment_contracts=containment_contracts,
            transition_groups=transition_groups,
            required_state_contracts=list(plan.required_state_contracts),
            required_event_scope_contracts=list(plan.required_event_scope_contracts),
            required_action_contracts=list(plan.required_action_contracts),
        ),
        diagnostics,
    )


def _validate_grounded_evidence_plan(
    pair: dict[str, Any],
    raw: IssueDiscoveryPlan,
    bindings: list[EvidenceGoalBinding],
) -> tuple[IssueDiscoveryPlan, list[dict[str, str]]]:
    diagnostics: list[dict[str, str]] = []
    lanes = {
        "surface_candidates": [
            item.model_copy(deep=True) for item in raw.surface_candidates
        ],
        "behavior_candidates": [
            item.model_copy(deep=True) for item in raw.behavior_candidates
        ],
    }
    seen: set[tuple[str, int]] = set()
    for binding in bindings:
        key = (binding.lane, binding.item_index)
        items = lanes[binding.lane]
        if key in seen:
            diagnostics.append(
                {
                    "stage": "semantic_grounding",
                    "class": "binding_patch_duplicate",
                    "message": f"duplicate evidence binding patch: {key}",
                }
            )
            continue
        seen.add(key)
        if binding.item_index >= len(items):
            diagnostics.append(
                {
                    "stage": "semantic_grounding",
                    "class": "binding_patch_out_of_range",
                    "message": f"evidence binding patch has no candidate: {key}",
                }
            )
            continue
        update = {
            field: value
            for field, value in binding.model_dump(mode="python").items()
            if field not in {"lane", "item_index"} and value is not None
        }
        goal = items[binding.item_index].goal.model_copy(update=update)
        if goal.observed_transition_id:
            error = _transition_binding_error(pair, goal.observed_transition_id)
            if error:
                diagnostics.append(
                    {
                        "stage": "semantic_grounding",
                        "class": "formal_transition_inconsistent",
                        "message": f"{binding.lane}[{binding.item_index}]: {error}",
                    }
                )
                goal = goal.model_copy(update={"observed_transition_id": None})
        if goal.reference_transition_id:
            error = _transition_binding_error(pair, goal.reference_transition_id)
            if error:
                diagnostics.append(
                    {
                        "stage": "semantic_grounding",
                        "class": "formal_transition_inconsistent",
                        "message": (
                            f"{binding.lane}[{binding.item_index}]: reference {error}"
                        ),
                    }
                )
                goal = goal.model_copy(update={"reference_transition_id": None})
        items[binding.item_index] = items[binding.item_index].model_copy(
            deep=True, update={"goal": goal}
        )
    for lane, items in lanes.items():
        for index in range(len(items)):
            if (lane, index) not in seen:
                diagnostics.append(
                    {
                        "stage": "semantic_grounding",
                        "class": "binding_patch_missing",
                        "message": f"no evidence binding patch for {lane}[{index}]",
                    }
                )
    evidence = IssueDiscoveryPlan(**lanes)
    return evidence, diagnostics


_GOAL_REQUIRED_STATE_FIELDS: dict[GoalRelation, tuple[str, ...]] = {
    "initial_target": ("subject", "target"),
    "state_exists": ("subject",),
    "final_pseudostate_exists": ("source",),
    "action_exists": ("subject",),
    "effect_exists": ("source",),
    "transition_contract": ("source", "target"),
    "transition_exists": ("source", "target"),
    "transition_target_consistency": ("target",),
    "completion_transition_fireable": ("source",),
    "contained_in": ("subject", "target"),
    "child_count": ("subject",),
    "guard_present": ("source", "target"),
    "guards_distinguishable": ("source",),
    "target_reachable": ("target",),
    "state_escapable": ("subject",),
    "event_reaches_target": ("source", "target"),
    "event_avoids_scope": ("source", "forbidden_scope"),
    "event_consumed": ("source",),
    "event_consumed_in_scope": ("source",),
    "termination_target": ("subject",),
    "eventually_terminates": ("subject",),
}


def _valid_expected_missing_state_reference(
    pair: dict[str, Any], goal: EvidenceGoal
) -> bool:
    """Validate only formal path grammar and exact parent anchoring."""

    if (
        goal.relation != "state_exists"
        or goal.expected is not True
        or not isinstance(goal.subject, str)
        or not isinstance(goal.source, str)
    ):
        return False
    root_scope = _source_root_scope_id(pair)
    state_ids = _source_state_ids(pair)
    if goal.source not in state_ids and goal.source != root_scope:
        return False
    expected = _strip_pair_root(goal.subject, pair["pair_name"])
    if expected in state_ids or not re.fullmatch(
        r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*", expected
    ):
        return False
    parent = expected.rpartition(".")[0] or None
    return parent is None if goal.source == root_scope else parent == goal.source


def _validate_direct_grounded_candidate(
    pair: dict[str, Any],
    candidate: BalancedEvidenceCandidate,
    *,
    lane: str,
    index: int,
) -> tuple[BalancedEvidenceCandidate, list[dict[str, str]]]:
    """Enforce exact formal references without interpreting any candidate text."""

    goal = candidate.goal.model_copy(deep=True)
    diagnostics: list[dict[str, str]] = []
    state_ids = _source_state_ids(pair)
    final_target_ids = _source_final_target_ids(pair)
    root_scope_id = _source_root_scope_id(pair)
    updates: dict[str, Any] = {}
    required_fields = _GOAL_REQUIRED_STATE_FIELDS.get(goal.relation, ())
    for field in required_fields:
        value = getattr(goal, field)
        if field == "subject" and goal.relation == "contained_in" and value is None:
            value = goal.source
            field = "source"
        if field == "target" and goal.relation == "target_reachable" and value is None:
            value = goal.subject
            field = "subject"
        if root_scope_id is not None and (
            (goal.relation == "initial_target" and field == "subject")
            or (goal.relation == "final_pseudostate_exists" and field == "source")
        ):
            allowed_ids = state_ids | {root_scope_id}
        elif (
            goal.relation == "event_consumed_in_scope"
            and field == "source"
        ):
            allowed_ids = state_ids | ({root_scope_id} if root_scope_id else set())
        elif (
            field == "target"
            and goal.relation
            in {
                "transition_contract",
                "transition_exists",
                "transition_target_consistency",
                "event_reaches_target",
            }
        ) or (field == "subject" and goal.relation == "termination_target"):
            allowed_ids = state_ids | final_target_ids
        else:
            allowed_ids = state_ids
        if value not in allowed_ids:
            if (
                goal.relation == "state_exists"
                and field == "subject"
                and _valid_expected_missing_state_reference(pair, goal)
            ):
                continue
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "formal_id_invalid",
                    "message": (
                        f"{lane}[{index}].goal.{field} is not an exact source "
                        f"state ID: {value!r}"
                    ),
                }
            )
            updates[field] = None
    if goal.relation == "event_consumed_in_scope" and goal.required_scope_ids:
        valid_scope_ids = state_ids | ({root_scope_id} if root_scope_id else set())
        normalized_scopes: list[str] = []
        for scope_id in goal.required_scope_ids:
            normalized = _strip_pair_root(str(scope_id), pair["pair_name"])
            if normalized not in valid_scope_ids:
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "class": "formal_id_invalid",
                        "message": (
                            f"{lane}[{index}].goal.required_scope_ids contains no "
                            f"exact source scope ID: {scope_id!r}"
                        ),
                    }
                )
                continue
            if normalized not in normalized_scopes:
                normalized_scopes.append(normalized)
        updates["required_scope_ids"] = normalized_scopes
    # A semantic grounding response may omit the observed transition when the
    # endpoint relation is unambiguous. Bind that case from the exact source
    # AST only when there is one and only one authored transition with the
    # normative endpoints. This is structural identity resolution, not a
    # textual condition/event match; multiple candidates remain unresolved so
    # the LLM must select the intended transition explicitly.
    if (
        goal.relation in {"transition_contract", "transition_exists"}
        and goal.observed_transition_id is None
        and isinstance(goal.source, str)
        and isinstance(goal.target, str)
    ):
        endpoint_rows = _source_transition_rows(
            pair, source=goal.source, target=goal.target
        )
        if len(endpoint_rows) == 1 and isinstance(endpoint_rows[0].get("id"), str):
            updates["observed_transition_id"] = endpoint_rows[0]["id"]
    if (
        goal.relation == "eventually_responds"
        and goal.source is not None
        and goal.source not in state_ids
    ):
        diagnostics.append(
            {
                "stage": "discovery_grounding",
                "class": "formal_id_invalid",
                "message": (
                    f"{lane}[{index}].goal.source is not an exact source "
                    f"state ID: {goal.source!r}"
                ),
            }
        )
        updates["source"] = None
    if goal.observed_transition_id:
        error = _transition_binding_error(pair, goal.observed_transition_id)
        if error:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "formal_transition_inconsistent",
                    "message": f"{lane}[{index}]: {error}",
                }
            )
            updates["observed_transition_id"] = None
    if goal.reference_transition_id:
        error = _transition_binding_error(pair, goal.reference_transition_id)
        if error:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "formal_transition_inconsistent",
                    "message": f"{lane}[{index}]: reference {error}",
                }
            )
            updates["reference_transition_id"] = None
    if updates:
        goal = goal.model_copy(update=updates)
    return candidate.model_copy(deep=True, update={"goal": goal}), diagnostics


def _assemble_grounded_contract_plan(
    pair: dict[str, Any],
    raw: ContractExtractionPlan,
    plan: DiscoveryGroundingPlan,
) -> tuple[GroundedContractPlan, list[dict[str, str]]]:
    """Apply LLM semantic bindings while keeping the NL contract write-protected."""

    diagnostics: list[dict[str, str]] = []

    def indexed(rows: list[Any], label: str) -> dict[int, Any]:
        result: dict[int, Any] = {}
        for row in rows:
            if row.item_index in result:
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "class": "binding_patch_duplicate",
                        "message": f"duplicate {label} binding index {row.item_index}",
                    }
                )
                continue
            result[row.item_index] = row
        return result

    concept_lines: dict[str, set[int]] = {}

    def note(concept_id: str | None, nl_line: int) -> None:
        if concept_id:
            concept_lines.setdefault(concept_id, set()).add(nl_line)

    for item in [*raw.initial_contracts, *plan.additional_contracts.initial_contracts]:
        note(item.composite_concept_id, item.nl_line)
        note(item.target_concept_id, item.nl_line)
    for item in [
        *raw.containment_contracts,
        *plan.additional_contracts.containment_contracts,
    ]:
        note(item.parent_concept_id, item.nl_line)
        note(item.child_concept_id, item.nl_line)
    for group in [*raw.transition_groups, *plan.additional_contracts.transition_groups]:
        note(group.source_concept_id, group.nl_line)
        for target in group.targets:
            note(target.target_concept_id, group.nl_line)
    required_concept_ids = {
        concept_id
        for item in raw.required_state_contracts
        for concept_id in (item.concept_id, item.scope_concept_id)
        if concept_id is not None
    }
    required_concept_ids.update(
        item.owner_concept_id
        for item in [
            *raw.required_action_contracts,
            *plan.additional_contracts.required_action_contracts,
        ]
    )
    concept_bindings = []
    for binding in plan.concept_bindings:
        lines = sorted(concept_lines.get(binding.concept_id, set()))
        if not lines and binding.concept_id not in required_concept_ids:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "concept_binding_unused",
                    "message": f"concept {binding.concept_id} has no raw NL occurrence",
                }
            )
            continue
        concept_bindings.append(
            SemanticConceptBinding(
                concept_id=binding.concept_id,
                source_state_id=binding.source_state_id,
                nl_lines=lines,
            )
        )
    concept_rows: dict[str, list[str]] = {}
    for binding in concept_bindings:
        concept_rows.setdefault(binding.concept_id, []).append(binding.source_state_id)
    concept_map = {
        concept_id: rows[0]
        for concept_id, rows in concept_rows.items()
        if len(rows) == 1
    }

    def authorize_indexed_binding(
        concept_id: str | None, source_state_id: str, nl_line: int
    ) -> None:
        """Treat the indexed LLM binding itself as semantic authorization."""

        if concept_id is None or concept_id in concept_map:
            return
        concept_map[concept_id] = source_state_id
        concept_bindings.append(
            SemanticConceptBinding(
                concept_id=concept_id,
                source_state_id=source_state_id,
                nl_lines=[nl_line],
            )
        )

    def mapped(concept_id: str | None, supplied: str) -> str:
        return concept_map.get(concept_id, supplied) if concept_id else supplied

    def sparse_mapped(
        concept_id: str | None,
        *,
        label: str,
    ) -> str | None:
        value = concept_map.get(concept_id) if concept_id else None
        if value is None:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "sparse_concept_binding_missing",
                    "message": f"{label} lacks one explicit concept binding",
                }
            )
        return value

    additional = ContractExtractionPlan(
        initial_contracts=[
            item.model_copy(
                deep=True,
                update={
                    "composite": mapped(item.composite_concept_id, item.composite),
                    "target": mapped(item.target_concept_id, item.target),
                },
            )
            for item in plan.additional_contracts.initial_contracts
        ],
        containment_contracts=[
            item.model_copy(
                deep=True,
                update={
                    "parent": mapped(item.parent_concept_id, item.parent),
                    "child": mapped(item.child_concept_id, item.child),
                },
            )
            for item in plan.additional_contracts.containment_contracts
        ],
        transition_groups=[
            group.model_copy(
                deep=True,
                update={
                    "source": mapped(group.source_concept_id, group.source),
                    "targets": [
                        target.model_copy(
                            deep=True,
                            update={
                                "target": mapped(
                                    target.target_concept_id, target.target
                                )
                            },
                        )
                        for target in group.targets
                    ],
                },
            )
            for group in plan.additional_contracts.transition_groups
        ],
        required_action_contracts=list(
            plan.additional_contracts.required_action_contracts
        ),
    )
    for item in additional.initial_contracts:
        authorize_indexed_binding(
            item.composite_concept_id, item.composite, item.nl_line
        )
        authorize_indexed_binding(item.target_concept_id, item.target, item.nl_line)
    for item in additional.containment_contracts:
        authorize_indexed_binding(item.parent_concept_id, item.parent, item.nl_line)
        authorize_indexed_binding(item.child_concept_id, item.child, item.nl_line)
    for group in additional.transition_groups:
        authorize_indexed_binding(group.source_concept_id, group.source, group.nl_line)
        for target in group.targets:
            authorize_indexed_binding(
                target.target_concept_id, target.target, group.nl_line
            )

    initial_bindings = indexed(plan.initial_contract_bindings, "initial_contract")
    initial_contracts = []
    for item_index, item in enumerate(raw.initial_contracts):
        binding = initial_bindings.get(item_index)
        if binding is None:
            composite = sparse_mapped(
                item.composite_concept_id,
                label=f"initial_contract[{item_index}].composite",
            )
            target = sparse_mapped(
                item.target_concept_id,
                label=f"initial_contract[{item_index}].target",
            )
            if composite is not None and target is not None:
                initial_contracts.append(
                    item.model_copy(
                        deep=True,
                        update={"composite": composite, "target": target},
                    )
                )
            continue
        if binding.status != "grounded":
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": f"binding_semantically_{binding.status}",
                    "message": (
                        f"initial_contract[{item_index}] {binding.status}: "
                        f"{binding.reason or 'no reason supplied'}"
                    ),
                }
            )
            continue
        if binding.composite is None or binding.target is None:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "binding_patch_incomplete",
                    "message": (
                        f"grounded initial_contract[{item_index}] lacks composite "
                        "or target"
                    ),
                }
            )
            continue
        initial_contracts.append(
            item.model_copy(
                deep=True,
                update={
                    "composite": binding.composite,
                    "target": binding.target,
                },
            )
        )
        authorize_indexed_binding(
            item.composite_concept_id, binding.composite, item.nl_line
        )
        authorize_indexed_binding(item.target_concept_id, binding.target, item.nl_line)

    containment_bindings = indexed(
        plan.containment_contract_bindings, "containment_contract"
    )
    containment_contracts = []
    for item_index, item in enumerate(raw.containment_contracts):
        binding = containment_bindings.get(item_index)
        if binding is None:
            parent = sparse_mapped(
                item.parent_concept_id,
                label=f"containment_contract[{item_index}].parent",
            )
            child = sparse_mapped(
                item.child_concept_id,
                label=f"containment_contract[{item_index}].child",
            )
            if parent is not None and child is not None:
                containment_contracts.append(
                    item.model_copy(
                        deep=True,
                        update={"parent": parent, "child": child},
                    )
                )
            continue
        if binding.status != "grounded":
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": f"binding_semantically_{binding.status}",
                    "message": (
                        f"containment_contract[{item_index}] {binding.status}: "
                        f"{binding.reason or 'no reason supplied'}"
                    ),
                }
            )
            continue
        if binding.parent is None or binding.child is None:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "binding_patch_incomplete",
                    "message": (
                        f"grounded containment_contract[{item_index}] lacks parent "
                        "or child"
                    ),
                }
            )
            continue
        containment_contracts.append(
            item.model_copy(
                deep=True,
                update={"parent": binding.parent, "child": binding.child},
            )
        )
        authorize_indexed_binding(item.parent_concept_id, binding.parent, item.nl_line)
        authorize_indexed_binding(item.child_concept_id, binding.child, item.nl_line)

    transition_bindings = indexed(plan.transition_group_bindings, "transition_group")
    transition_groups = []
    for item_index, group in enumerate(raw.transition_groups):
        binding = transition_bindings.get(item_index)
        if binding is None:
            source = sparse_mapped(
                group.source_concept_id,
                label=f"transition_group[{item_index}].source",
            )
            targets: list[ExpectedTransitionTarget] = []
            for target_index, target in enumerate(group.targets):
                target_id = sparse_mapped(
                    target.target_concept_id,
                    label=(f"transition_group[{item_index}].targets[{target_index}]"),
                )
                if target_id is not None:
                    targets.append(
                        target.model_copy(deep=True, update={"target": target_id})
                    )
            if source is not None and len(targets) == len(group.targets):
                transition_groups.append(
                    group.model_copy(
                        deep=True,
                        update={"source": source, "targets": targets},
                    )
                )
            continue
        if binding.status != "grounded":
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": f"binding_semantically_{binding.status}",
                    "message": (
                        f"transition_group[{item_index}] {binding.status}: "
                        f"{binding.reason or 'no reason supplied'}"
                    ),
                }
            )
            continue
        if binding.source is None or not binding.targets:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "binding_patch_incomplete",
                    "message": (
                        f"grounded transition_group[{item_index}] lacks source "
                        "or targets"
                    ),
                }
            )
            continue
        target_bindings: dict[int, TransitionTargetGrounding] = {}
        for target_binding in binding.targets:
            if target_binding.target_index in target_bindings:
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "class": "binding_patch_duplicate",
                        "message": (
                            f"duplicate transition_group[{item_index}] target binding "
                            f"{target_binding.target_index}"
                        ),
                    }
                )
                continue
            target_bindings[target_binding.target_index] = target_binding
        targets = []
        for target_index, target in enumerate(group.targets):
            target_binding = target_bindings.get(target_index)
            if target_binding is None:
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "class": "binding_patch_missing",
                        "message": (
                            f"no transition_group[{item_index}] target binding "
                            f"for index {target_index}"
                        ),
                    }
                )
                continue
            targets.append(
                target.model_copy(
                    deep=True,
                    update={
                        "target": target_binding.target,
                        "observed_transition_id": (
                            target_binding.observed_transition_id
                        ),
                        "formal_condition": target_binding.condition_binding,
                        "condition_role": target_binding.condition_role,
                    },
                )
            )
        if targets:
            transition_groups.append(
                group.model_copy(
                    deep=True,
                    update={"source": binding.source, "targets": targets},
                )
            )
            authorize_indexed_binding(
                group.source_concept_id, binding.source, group.nl_line
            )
            for target_index, target in enumerate(group.targets):
                target_binding = target_bindings.get(target_index)
                if target_binding is not None:
                    authorize_indexed_binding(
                        target.target_concept_id,
                        target_binding.target,
                        group.nl_line,
                    )

    assembled = GroundedContractPlan(
        initial_contracts=[
            *initial_contracts,
            *additional.initial_contracts,
        ],
        containment_contracts=[
            *containment_contracts,
            *additional.containment_contracts,
        ],
        transition_groups=[
            *transition_groups,
            *additional.transition_groups,
        ],
        required_state_contracts=list(raw.required_state_contracts),
        required_event_scope_contracts=list(raw.required_event_scope_contracts),
        required_action_contracts=[
            *raw.required_action_contracts,
            *additional.required_action_contracts,
        ],
    )
    validated, validation_diagnostics = _validate_grounded_contract_plan(
        pair, assembled, concept_bindings
    )
    return validated, [*diagnostics, *validation_diagnostics]


def _expand_required_state_bindings(
    pair: dict[str, Any],
    contracts: list[RequiredStateContract],
    bindings: list[RequiredStateGrounding],
    concept_bindings: list[CompactConceptBinding],
) -> tuple[list[BalancedEvidenceCandidate], list[dict[str, str]]]:
    """Compile sparse missing/unresolved resolutions and exact realized bindings."""

    diagnostics: list[dict[str, str]] = []
    by_index: dict[int, RequiredStateGrounding] = {}
    for binding in bindings:
        if binding.item_index in by_index:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "binding_patch_duplicate",
                    "message": (
                        f"duplicate required_state binding index {binding.item_index}"
                    ),
                }
            )
            continue
        if binding.item_index >= len(contracts):
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "binding_patch_out_of_range",
                    "message": (
                        f"required_state binding has no contract: {binding.item_index}"
                    ),
                }
            )
            continue
        by_index[binding.item_index] = binding

    state_ids = _source_state_ids(pair)
    final_target_ids = _source_final_target_ids(pair)
    realized_by_concept: dict[str, list[str]] = {}
    for binding in concept_bindings:
        realized_by_concept.setdefault(binding.concept_id, []).append(
            binding.source_state_id
        )
    candidates: list[BalancedEvidenceCandidate] = []

    def append_realized_role_candidate(
        contract: RequiredStateContract, realized_state_id: str
    ) -> None:
        if contract.role != "termination_state":
            return
        candidates.append(
            BalancedEvidenceCandidate(
                obligation=(
                    f"The NL-designated termination state {contract.concept!r} "
                    "must be a stable ending target for its declared behavior."
                ),
                claim=(
                    f"Required termination target {realized_state_id!r} admits "
                    "a source-level nonterminating continuation."
                ),
                basis=(
                    "The NL contract marks this exact grounded state as a "
                    "termination target, so its source continuation is a "
                    "directly testable stability obligation."
                ),
                basis_kind="nl_literal",
                nl_quote=contract.nl_quote,
                priority=contract.priority,
                locations=[realized_state_id],
                proposed_l="L2",
                observed_fact=(
                    "The contract LLM classified this concept as a termination "
                    "state and the grounding LLM bound it to this exact source ID; "
                    "the compiler evaluates local stable termination."
                ),
                domain_obligation=TemporalObligation(
                    pattern="termination",
                    state_ref=realized_state_id,
                    expected=True,
                ),
                goal=EvidenceGoal(
                    relation="termination_target",
                    subject=realized_state_id,
                    expected=True,
                ),
            )
        )

    for item_index, contract in enumerate(contracts):
        binding = by_index.get(item_index)
        if binding is None:
            realized_ids = realized_by_concept.get(contract.concept_id, [])
            if len(realized_ids) == 1 and realized_ids[0] in state_ids:
                append_realized_role_candidate(contract, realized_ids[0])
                continue
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "sparse_required_state_resolution_missing",
                    "message": (
                        f"required_state[{item_index}] has neither one exact "
                        "ordinary-state concept binding nor an explicit sparse "
                        "resolution"
                    ),
                }
            )
            continue
        if binding.status == "realized":
            allowed_ids = (
                final_target_ids
                if binding.formal_kind == "final_pseudostate"
                else state_ids
                if binding.formal_kind == "state"
                else set()
            )
            if binding.realized_state_id not in allowed_ids:
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "class": "formal_id_invalid",
                        "message": (
                            f"required_state[{item_index}] realized_state_id is not "
                            "an exact source ID of the declared formal kind: "
                            f"{binding.realized_state_id!r}"
                        ),
                    }
                )
            elif binding.formal_kind == "state" and isinstance(
                binding.realized_state_id, str
            ):
                append_realized_role_candidate(contract, binding.realized_state_id)
            continue
        if binding.status == "unresolved":
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "semantic_binding_unresolved",
                    "message": (
                        f"required_state[{item_index}]: "
                        f"{binding.reason or 'semantic realization unresolved'}"
                    ),
                }
            )
            continue

        if binding.formal_kind == "final_pseudostate":
            goal = EvidenceGoal(
                relation="final_pseudostate_exists",
                source=binding.parent_scope_id,
                expected=True,
            )
            valid_reference = binding.parent_scope_id in (
                state_ids | {_source_root_scope_id(pair)}
            )
        elif binding.formal_kind == "state":
            goal = EvidenceGoal(
                relation="state_exists",
                source=binding.parent_scope_id,
                subject=binding.normative_formal_path,
                expected=True,
            )
            valid_reference = _valid_expected_missing_state_reference(pair, goal)
        else:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "formal_kind_missing",
                    "message": (
                        f"required_state[{item_index}] requires an explicit formal_kind"
                    ),
                }
            )
            continue
        if not valid_reference:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "formal_missing_state_reference_invalid",
                    "message": (
                        f"required_state[{item_index}] missing resolution requires "
                        "an absent grammar-valid path anchored to one exact parent scope"
                    ),
                }
            )
        if binding.formal_kind == "final_pseudostate":
            obligation = (
                f"The exact source scope {binding.parent_scope_id!r} must declare "
                f"the final pseudostate denoted by {contract.concept!r}."
            )
            claim = (
                f"Exact source scope {binding.parent_scope_id!r} declares no "
                "final pseudostate."
            )
            observed_fact = (
                "The semantic-grounding LLM declared the required formal kind "
                "to be a final pseudostate; the compiler checks exact source and "
                "FCSTM scope-local final edges."
            )
        else:
            obligation = (
                f"The required state concept {contract.concept!r} must have a "
                "state realization in its declared scope."
            )
            claim = (
                f"No source state realizes required concept {contract.concept!r} "
                f"at {binding.normative_formal_path!r}."
            )
            observed_fact = (
                "The semantic-grounding LLM declared the required state absent; "
                "the formal compiler checks the declared path against the source "
                "AST and FCSTM artifact."
            )
        candidates.append(
            BalancedEvidenceCandidate(
                obligation=obligation,
                claim=claim,
                basis=(
                    "The required-state grounding records the NL concept and its "
                    "exact parent scope; the compiler checks that declared formal "
                    "path against the source AST and FCSTM inventory."
                ),
                basis_kind="nl_literal",
                nl_quote=contract.nl_quote,
                priority=contract.priority,
                locations=[],
                proposed_l="L0",
                observed_fact=observed_fact,
                goal=goal,
            )
        )
    return candidates, diagnostics


def _event_scope_ids(
    pair: dict[str, Any],
    anchors: list[str],
    applicability: Literal[
        "one_scope",
        "scope_and_descendants",
        "each_operating_mode",
    ],
) -> list[str]:
    """Return exact formal scope IDs covered by a typed event obligation.

    The only expansion performed here is over canonical ``parent`` links.  It
    deliberately does not inspect scope labels, event prose, or identifier
    spelling.  ``one_scope`` and ``each_operating_mode`` are already complete
    LLM-grounded sets; ``scope_and_descendants`` adds the formal descendant
    closure so a grouped obligation is not reduced to its anchor transition.
    """

    model = _source_model(pair)
    state_rows = [
        item
        for item in model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    state_ids = {str(item["id"]) for item in state_rows}
    root_scope = _source_root_scope_id(pair)
    valid_ids = state_ids | ({root_scope} if root_scope else set())
    normalized = [
        _strip_pair_root(str(anchor), pair["pair_name"])
        for anchor in anchors
        if isinstance(anchor, str) and anchor
    ]
    if not normalized or any(anchor not in valid_ids for anchor in normalized):
        return []
    normalized = list(dict.fromkeys(normalized))
    if applicability != "scope_and_descendants":
        return normalized

    parent_by_id = {
        str(item["id"]): item.get("parent")
        for item in state_rows
    }
    covered: list[str] = []
    for anchor in normalized:
        if anchor not in covered:
            covered.append(anchor)
        if anchor == root_scope:
            covered.extend(
                state_id for state_id in sorted(state_ids) if state_id not in covered
            )
            continue
        for state_id in sorted(state_ids):
            cursor: str | None = state_id
            while cursor is not None and cursor != anchor:
                parent = parent_by_id.get(cursor)
                cursor = str(parent) if isinstance(parent, str) and parent else None
            if cursor == anchor and state_id not in covered:
                covered.append(state_id)
    return covered


# Backward-compatible private name for callers/tests that need the typed
# expansion without constructing a candidate.
_expand_event_scope_ids = _event_scope_ids


def _expand_required_event_scope_bindings(
    pair: dict[str, Any],
    contracts: list[RequiredEventScopeContract],
    bindings: list[RequiredEventScopeGrounding],
) -> tuple[list[BalancedEvidenceCandidate], list[dict[str, str]]]:
    """Expand only LLM-declared exact event identities and normative scopes."""

    diagnostics: list[dict[str, str]] = []
    by_index: dict[int, RequiredEventScopeGrounding] = {}
    for binding in bindings:
        if binding.item_index in by_index:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "binding_patch_duplicate",
                    "message": (
                        "duplicate required_event_scope binding index "
                        f"{binding.item_index}"
                    ),
                }
            )
            continue
        if binding.item_index >= len(contracts):
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "binding_patch_out_of_range",
                    "message": (
                        "required_event_scope binding has no contract: "
                        f"{binding.item_index}"
                    ),
                }
            )
            continue
        by_index[binding.item_index] = binding

    state_ids = _source_state_ids(pair)
    root_scope = _source_root_scope_id(pair)
    valid_scope_ids = state_ids | ({root_scope} if root_scope else set())
    candidates: list[BalancedEvidenceCandidate] = []
    for item_index, contract in enumerate(contracts):
        binding = by_index.get(item_index)
        if binding is None:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "binding_patch_missing",
                    "message": f"no required_event_scope binding for index {item_index}",
                }
            )
            continue
        if binding.status == "unresolved":
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "semantic_binding_unresolved",
                    "message": (
                        f"required_event_scope[{item_index}]: "
                        f"{binding.reason or 'event identity or applicability unresolved'}"
                    ),
                }
            )
            continue
        if not binding.required_scope_ids:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "binding_patch_empty",
                    "message": (
                        f"required_event_scope[{item_index}] grounded resolution "
                        "requires at least one exact required scope"
                    ),
                }
            )
            continue
        transition_error = (
            _transition_binding_error(pair, binding.observed_transition_id)
            if binding.observed_transition_id
            else "observed_transition_id is required"
        )
        if transition_error:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "formal_transition_inconsistent",
                    "message": (
                        f"required_event_scope[{item_index}]: {transition_error}"
                    ),
                }
            )
            continue
        observed_transition = _source_transition_by_id(
            pair, str(binding.observed_transition_id)
        )
        if not isinstance((observed_transition or {}).get("event"), str) or not str(
            (observed_transition or {}).get("event")
        ):
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "formal_event_identity_missing",
                    "message": (
                        f"required_event_scope[{item_index}] observed transition "
                        "has no exact structured event identity"
                    ),
                }
            )
            continue
        # The LLM supplies the normative scope anchors.  Descendant expansion
        # is performed only over exact ``parent`` links in the canonical source
        # inventory; no state name or requirement prose is inspected here.
        coverage_scopes = _expand_event_scope_ids(
            pair,
            binding.required_scope_ids,
            contract.applicability,
        )
        if not coverage_scopes:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "formal_scope_expansion_empty",
                    "message": (
                        f"required_event_scope[{item_index}] has no exact formal "
                        "scope after applicability expansion"
                    ),
                }
            )
            continue
        # Each exact covered scope remains independently executable, while the
        # complete closure is retained on every candidate for contract-level
        # coverage auditing and consumer aggregation.
        candidate_scopes = coverage_scopes
        seen_scopes: set[str] = set()
        for scope in candidate_scopes:
            if scope in seen_scopes:
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "class": "binding_patch_duplicate",
                        "message": (
                            f"required_event_scope[{item_index}] repeats scope {scope!r}"
                        ),
                    }
                )
                continue
            seen_scopes.add(scope)
            if scope not in valid_scope_ids:
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "class": "formal_id_invalid",
                        "message": (
                            f"required_event_scope[{item_index}] scope is not an "
                            f"exact source state ID: {scope!r}"
                        ),
                    }
                )
                continue
            candidates.append(
                BalancedEvidenceCandidate(
                    obligation=(
                        f"Event concept {contract.event_concept!r} must be consumed "
                        f"while required scope {scope!r} is active."
                    ),
                    claim=(
                        f"Required scope {scope!r} has no reachable consumer for "
                        f"event concept {contract.event_concept!r}; authored consumers "
                        "may exist in an unreachable component."
                    ),
                    basis=(
                        "The grounding LLM supplied an exact event identity and "
                        "normative scope, allowing the compiler to test scope-local "
                        "event consumption without interpreting labels."
                    ),
                    basis_kind="nl_literal",
                    nl_quote=contract.nl_quote,
                    priority=contract.priority,
                    locations=[binding.observed_transition_id],
                    proposed_l="L0",
                    domain_obligation=GraphObligation(
                        property="event_consumer_reachable",
                        source_ref=scope,
                        expected=True,
                    ),
                    observed_fact=(
                        "The semantic-grounding LLM selected one exact transition "
                        "for event identity and declared this exact required scope."
                    ),
                    goal=EvidenceGoal(
                        relation="event_consumed_in_scope",
                        source=scope,
                        observed_transition_id=binding.observed_transition_id,
                        scope_applicability=contract.applicability,
                        required_scope_ids=coverage_scopes,
                        expected=True,
                    ),
                )
            )
    return candidates, diagnostics


def _expand_required_action_contracts(
    pair: dict[str, Any],
    contracts: list[RequiredActionContract],
    bindings: list[RequiredActionGrounding],
    concept_bindings: list[CompactConceptBinding],
) -> tuple[list[BalancedEvidenceCandidate], list[dict[str, str]]]:
    """Compile accepted NL action contracts from exact semantic owner bindings."""

    diagnostics: list[dict[str, str]] = []
    vetoes: dict[int, RequiredActionGrounding] = {}
    for binding in bindings:
        if binding.item_index in vetoes:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "binding_patch_duplicate",
                    "message": (
                        f"duplicate required_action binding index {binding.item_index}"
                    ),
                }
            )
            continue
        if binding.item_index >= len(contracts):
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "binding_patch_out_of_range",
                    "message": (
                        f"required_action binding has no contract: {binding.item_index}"
                    ),
                }
            )
            continue
        vetoes[binding.item_index] = binding

    concept_rows: dict[str, list[str]] = {}
    for binding in concept_bindings:
        concept_rows.setdefault(binding.concept_id, []).append(
            binding.source_state_id
        )
    exact_concepts = {
        concept_id: rows[0]
        for concept_id, rows in concept_rows.items()
        if len(set(rows)) == 1
    }
    state_ids = _source_state_ids(pair)
    candidates: list[BalancedEvidenceCandidate] = []
    for item_index, contract in enumerate(contracts):
        veto = vetoes.get(item_index)
        if veto is not None:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": f"binding_semantically_{veto.status}",
                    "message": (
                        f"required_action[{item_index}] {veto.status}: {veto.reason}"
                    ),
                }
            )
            continue
        owner = exact_concepts.get(contract.owner_concept_id)
        if owner not in state_ids:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "sparse_concept_binding_missing",
                    "message": (
                        f"required_action[{item_index}].owner lacks one exact "
                        "concept binding"
                    ),
                }
            )
            continue
        phase = None if contract.phase == "any" else contract.phase
        phase_text = "any lifecycle phase" if phase is None else f"the {phase} phase"
        candidates.append(
            BalancedEvidenceCandidate(
                obligation=(
                    f"State {owner!r} must own required {contract.action_kind} "
                    f"{contract.action_concept!r} in {phase_text}."
                ),
                claim=(
                    f"State {owner!r} lacks required {contract.action_kind} "
                    f"{contract.action_concept!r} in {phase_text}."
                ),
                basis=(
                    "The NL-only contract extractor classified one atomic named "
                    "state-owned action, and semantic grounding supplied the exact "
                    "owner state ID."
                ),
                basis_kind="nl_literal",
                nl_quote=contract.nl_quote,
                priority=contract.priority,
                locations=[owner],
                proposed_l="L0",
                observed_fact=(
                    "The compiler will compare this exact action identity against "
                    "the canonical lifecycle-action and mapped FCSTM inventories."
                ),
                domain_obligation=AttachmentObligation(
                    attachment="action_phase",
                    subject_ref=owner,
                    action_ref=contract.action_concept,
                    phase=phase,
                ),
                goal=EvidenceGoal(
                    relation="action_exists",
                    subject=owner,
                    phase=phase,
                    action=contract.action_concept,
                ),
            )
        )
    return candidates, diagnostics


def _expand_unauthorized_transition_bindings(
    pair: dict[str, Any],
    bindings: list[UnauthorizedTransitionGrounding],
) -> tuple[list[BalancedEvidenceCandidate], list[dict[str, str]]]:
    """Lower explicit LLM edge-authorization decisions into transition proofs."""

    diagnostics: list[dict[str, str]] = []
    candidates: list[BalancedEvidenceCandidate] = []
    seen: set[str] = set()
    nl_line_count = len(pair["nl"].splitlines())
    for binding in bindings:
        transition_id = binding.observed_transition_id
        if transition_id in seen:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "unauthorized_transition_duplicate",
                    "message": f"duplicate unauthorized transition {transition_id!r}",
                }
            )
            continue
        seen.add(transition_id)
        if any(line < 1 or line > nl_line_count for line in binding.nl_lines):
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "unauthorized_transition_nl_line_invalid",
                    "message": (
                        f"unauthorized transition {transition_id!r} cites an NL line "
                        f"outside 1..{nl_line_count}"
                    ),
                }
            )
        if binding.status == "unresolved":
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "unauthorized_transition_unresolved",
                    "message": (
                        f"semantic authorization for transition {transition_id!r} "
                        f"remains unresolved: {binding.rationale}"
                    ),
                }
            )
            continue
        transition = _source_transition_by_id(pair, transition_id)
        if transition is None:
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "formal_transition_inconsistent",
                    "message": (
                        f"unauthorized transition binding names no exact source "
                        f"transition: {transition_id!r}"
                    ),
                }
            )
            continue
        if not binding.nl_quote or not _nl_anchor_valid(pair, binding):
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "unauthorized_transition_nl_anchor_invalid",
                    "message": (
                        f"unauthorized transition {transition_id!r} requires one "
                        "verbatim NL span for source attribution"
                    ),
                }
            )
            continue
        locations = [transition_id]
        if isinstance(transition.get("ref"), str):
            locations.append(str(transition["ref"]))
        locations.extend(f"NL{line}" for line in binding.nl_lines)
        candidates.append(
            BalancedEvidenceCandidate(
                obligation=(
                    "Every authored transition must be semantically authorized by "
                    "the NL contract that governs its source and behavior role."
                ),
                claim=(
                    f"Authored transition {transition_id!r} is present but no "
                    "competent NL reading authorizes this exact edge."
                ),
                basis=binding.rationale,
                basis_kind="nl_literal",
                nl_quote=binding.nl_quote,
                priority=2,
                locations=locations,
                proposed_l="L0",
                observed_fact=(
                    "The semantic authorization audit selected this exact source "
                    "transition; the formal compiler will test its presence "
                    "against the declared absence obligation."
                ),
                domain_obligation=ElementObligation(
                    element_kind="transition",
                    operator="absent",
                    subject_ref=transition_id,
                ),
                goal=EvidenceGoal(
                    relation="transition_absent",
                    observed_transition_id=transition_id,
                    expected=False,
                ),
            )
        )
    return candidates, diagnostics


def validate_discovery_grounding(
    pair: dict[str, Any],
    raw_contract_plan: ContractExtractionPlan,
    plan: DiscoveryGroundingPlan,
) -> tuple[GroundedContractPlan, IssueDiscoveryPlan, list[dict[str, str]]]:
    """Validate only exact formal contracts after one LLM semantic decision."""

    contract, diagnostics = _assemble_grounded_contract_plan(
        pair, raw_contract_plan, plan
    )
    required_candidates, required_diagnostics = _expand_required_state_bindings(
        pair,
        raw_contract_plan.required_state_contracts,
        plan.required_state_bindings,
        plan.concept_bindings,
    )
    diagnostics.extend(required_diagnostics)
    event_scope_candidates, event_scope_diagnostics = (
        _expand_required_event_scope_bindings(
            pair,
            raw_contract_plan.required_event_scope_contracts,
            plan.required_event_scope_bindings,
        )
    )
    diagnostics.extend(event_scope_diagnostics)
    action_candidates, action_diagnostics = _expand_required_action_contracts(
        pair,
        raw_contract_plan.required_action_contracts,
        plan.required_action_bindings,
        plan.concept_bindings,
    )
    diagnostics.extend(action_diagnostics)
    additional_action_candidates, additional_action_diagnostics = (
        _expand_required_action_contracts(
            pair,
            plan.additional_contracts.required_action_contracts,
            [],
            plan.concept_bindings,
        )
    )
    action_candidates.extend(additional_action_candidates)
    diagnostics.extend(additional_action_diagnostics)
    unauthorized_candidates, unauthorized_diagnostics = (
        _expand_unauthorized_transition_bindings(
            pair, plan.unauthorized_transition_bindings
        )
    )
    diagnostics.extend(unauthorized_diagnostics)
    lanes: dict[str, list[BalancedEvidenceCandidate]] = {
        "surface_candidates": [],
        "behavior_candidates": [],
    }
    unresolved_candidate_indices = {
        "surface_candidates": {
            item.item_index
            for item in plan.unresolved
            if item.scope == "surface_candidate"
        },
        "behavior_candidates": {
            item.item_index
            for item in plan.unresolved
            if item.scope == "behavior_candidate"
        },
    }

    def veto_unresolved_candidate(
        candidate: BalancedEvidenceCandidate,
    ) -> BalancedEvidenceCandidate:
        goal = candidate.goal.model_copy(
            update={
                "observed_transition_id": None,
                "subject": None,
                "source": None,
                "trigger": None,
                "target": None,
                "forbidden_scope": None,
                "response": None,
                "variable": None,
                "action": None,
            }
        )
        return candidate.model_copy(deep=True, update={"goal": goal})

    planned_lanes = {
        "surface_candidates": list(plan.surface_candidates),
        "behavior_candidates": list(plan.behavior_candidates),
    }
    for lane, candidates in planned_lanes.items():
        for item_index in sorted(unresolved_candidate_indices[lane]):
            if item_index >= len(candidates):
                continue
            candidates[item_index] = veto_unresolved_candidate(candidates[item_index])
            diagnostics.append(
                {
                    "stage": "discovery_grounding",
                    "class": "semantic_binding_unresolved_veto",
                    "message": f"{lane}[{item_index}] was withheld from execution",
                }
            )
    raw_lanes = {
        "surface_candidates": [
            *planned_lanes["surface_candidates"],
            *required_candidates,
            *event_scope_candidates,
            *action_candidates,
            *unauthorized_candidates,
        ],
        "behavior_candidates": planned_lanes["behavior_candidates"],
    }
    for lane, validated_candidates in lanes.items():
        for index, candidate in enumerate(raw_lanes[lane]):
            validated, candidate_diagnostics = _validate_direct_grounded_candidate(
                pair, candidate, lane=lane, index=index
            )
            validated_candidates.append(validated)
            diagnostics.extend(candidate_diagnostics)
    diagnostics.extend(
        {
            "stage": "discovery_grounding",
            "class": "semantic_binding_unresolved",
            "message": f"{item.scope}[{item.item_index}].{item.field}: {item.reason}",
        }
        for item in plan.unresolved
    )
    return contract, IssueDiscoveryPlan(**lanes), diagnostics


def validate_semantic_grounding(
    pair: dict[str, Any],
    raw_evidence_plan: IssueDiscoveryPlan,
    grounding: SemanticGroundingPlan,
) -> tuple[GroundedContractPlan, IssueDiscoveryPlan, list[dict[str, str]]]:
    contract, contract_diagnostics = _validate_grounded_contract_plan(
        pair, grounding.contract_plan, grounding.concept_bindings
    )
    evidence, evidence_diagnostics = _validate_grounded_evidence_plan(
        pair, raw_evidence_plan, grounding.evidence_bindings
    )
    unresolved = [
        {
            "stage": "semantic_grounding",
            "class": "semantic_binding_unresolved",
            "message": (f"{item.scope}[{item.item_index}].{item.field}: {item.reason}"),
        }
        for item in grounding.unresolved
    ]
    return (
        contract,
        evidence,
        [
            *contract_diagnostics,
            *evidence_diagnostics,
            *unresolved,
        ],
    )


def expand_transition_groups(
    pair: dict[str, Any], groups: list[ExpectedTransitionGroup]
) -> list[EvidenceCandidate]:
    candidates: list[EvidenceCandidate] = []
    for group in groups:
        nl_quote = _contract_nl_quote(pair, group)
        locations = [f"NL{group.nl_line}"]
        for target in group.targets:
            condition_note = f" under {target.condition}" if target.condition else ""
            candidates.append(
                EvidenceCandidate(
                    obligation=(
                        f"{group.source} must transition directly to {target.target}"
                        f"{condition_note}."
                    ),
                    claim=(
                        f"The required {group.source} -> {target.target} transition"
                        f"{condition_note} is absent or loses its condition."
                    ),
                    basis_kind="nl_literal",
                    nl_quote=nl_quote,
                    priority=group.priority,
                    locations=locations,
                    proposed_l="L1" if target.condition else "L0",
                    goal=EvidenceGoal(
                        relation="transition_contract",
                        observed_transition_id=target.observed_transition_id,
                        source=group.source,
                        target=target.target,
                        condition=target.condition,
                        trigger=target.formal_condition,
                        condition_role=target.condition_role,
                    ),
                )
            )
        conditioned_targets = [item for item in group.targets if item.condition]
        if len(conditioned_targets) >= 2:
            transition_refs = [
                item.observed_transition_id
                for item in conditioned_targets
                if item.observed_transition_id is not None
            ]
            guard_bindings = []
            for transition_id in transition_refs:
                transition = _source_transition_by_id(pair, transition_id)
                raw_label = (
                    (transition.get("attributes") or {}).get("raw_label")
                    if isinstance(transition, dict)
                    else None
                )
                if isinstance(raw_label, str) and raw_label:
                    guard_bindings.append(
                        GuardConditionBinding(
                            transition_id=transition_id,
                            source_label=raw_label,
                            semantic_role="guard_condition",
                        )
                    )
            candidates.append(
                EvidenceCandidate(
                    obligation=(
                        f"The multi-way alternatives from {group.source} must have "
                        "a defined selection when their conditions coincide."
                    ),
                    claim=(
                        f"At least two of the {len(conditioned_targets)} conditioned "
                        f"branches from {group.source} overlap without priority."
                    ),
                    basis_kind="domain_norm",
                    nl_quote=nl_quote,
                    priority=group.priority,
                    locations=locations,
                    proposed_l="L1",
                    domain_obligation=GuardSetObligation(
                        property="disjoint",
                        scope_ref=group.source,
                        transition_refs=transition_refs,
                        guard_bindings=guard_bindings,
                    ),
                    goal=EvidenceGoal(
                        relation="guards_distinguishable",
                        source=group.source,
                    ),
                )
            )
    return candidates


def expand_initial_contracts(
    pair: dict[str, Any], contracts: list[ExpectedInitialContract]
) -> list[EvidenceCandidate]:
    candidates = []
    for contract in contracts:
        nl_quote = _contract_nl_quote(pair, contract)
        locations = [f"NL{contract.nl_line}"]
        candidates.append(
            EvidenceCandidate(
                obligation=(
                    f"{contract.composite} must initially enter {contract.target}."
                ),
                claim=(
                    f"The initial target of {contract.composite} is not "
                    f"{contract.target}."
                ),
                basis_kind="nl_literal",
                nl_quote=nl_quote,
                priority=contract.priority,
                locations=locations,
                requirement_group_id=contract.requirement_group_id,
                proposed_l="L0",
                goal=EvidenceGoal(
                    relation="initial_target",
                    subject=contract.composite,
                    target=contract.target,
                ),
            )
        )
    return candidates


def expand_containment_contracts(
    pair: dict[str, Any], contracts: list[ExpectedContainmentContract]
) -> list[EvidenceCandidate]:
    candidates = []
    for contract in contracts:
        nl_quote = _contract_nl_quote(pair, contract)
        candidates.append(
            EvidenceCandidate(
                obligation=(
                    f"{contract.child} must be directly contained in {contract.parent}."
                ),
                claim=(
                    f"{contract.child} is not directly contained in {contract.parent}."
                ),
                basis_kind="nl_literal",
                nl_quote=nl_quote,
                priority=contract.priority,
                locations=[f"NL{contract.nl_line}"],
                proposed_l="L1",
                goal=EvidenceGoal(
                    relation="contained_in",
                    subject=contract.child,
                    target=contract.parent,
                ),
            )
        )
    return candidates


def expand_contract_lens_plan(
    pair: dict[str, Any], plan: ContractLensPlan
) -> EvidencePlan:
    """Compatibility wrapper for the discarded one-call pilot."""

    candidates = expand_transition_groups(pair, plan.transition_groups)
    candidates.extend(plan.candidates)
    return EvidencePlan(candidates=candidates)


def _compiled_bindings(check: ProbeCheck) -> dict[str, str | int | float | bool]:
    bindings = dict(check.bindings)
    if check.source is not None:
        key = "scope" if check.kind == "terminates" else "source"
        bindings.setdefault(key, check.source)
    if check.trigger is not None:
        bindings.setdefault("trigger", check.trigger)
    if check.target is not None:
        bindings.setdefault("target", check.target)
    if check.within_cycles is not None:
        bindings.setdefault("within_cycles", check.within_cycles)
    return bindings


def compile_check(check: ProbeCheck) -> tuple[str | None, str | None]:
    if not check.kind:
        return None, "check requires kind"
    required, optional = PREDICATE_SIGNATURES[check.kind]
    bindings = _compiled_bindings(check)
    missing = [name for name in required if name not in bindings]
    if missing:
        return None, f"{check.kind} requires binding(s): {', '.join(missing)}"
    unexpected = sorted(set(bindings) - set(required) - set(optional))
    if unexpected:
        return None, f"{check.kind} does not accept binding(s): {', '.join(unexpected)}"
    ordered = [*required, *(name for name in optional if name in bindings)]
    rendered = ", ".join(
        f"{name}={json.dumps(bindings[name], ensure_ascii=False)}" for name in ordered
    )
    call = f"{check.kind}({rendered})"
    return f"{call} is {check.expected}", None


def build_assertion_artifact(
    executed_checks: list[dict[str, Any]],
) -> dict[str, Any] | None:
    compiled = [item for item in executed_checks if item.get("expression")]
    if not compiled:
        return None
    assignments = [
        f"_paper1_check_{index} = {item['expression']}"
        for index, item in enumerate(compiled, start=1)
    ]
    names = ", ".join(f"_paper1_check_{index}" for index in range(1, len(compiled) + 1))
    script = "\n".join(
        [
            "# Generated deterministically from paper1 AssertionIR.",
            *assignments,
            f"assert all([{names}]), {_quoted(EXECUTABLE_ASSERTION_MESSAGE)}",
        ]
    )
    parsed = parse_assertion_script(script)
    return {
        "schema": "paper1.compiled_assertion.v1",
        "assertion_ir": [
            {
                "role": item.get("normalized_probe", {}).get("role"),
                "predicate": item.get("normalized_probe", {}).get("kind"),
                "bindings": _compiled_bindings(
                    ProbeCheck.model_validate(item.get("normalized_probe", {}))
                ),
                "expected": item.get("normalized_probe", {}).get("expected"),
            }
            for item in compiled
        ],
        "compiled_assertion_code": script,
        "compiled_assertion_sha256": parsed.source_sha256,
        "terminal_expression": parsed.terminal_expression,
        "execution_model": "sealed_pyfcstm_predicate_environment",
    }


def build_execution_certificate(
    pair: dict[str, Any],
    artifact: dict[str, Any] | None,
    executed_checks: list[dict[str, Any]],
    *,
    terminal: bool,
    precondition_failed: bool,
    counterexample_found: bool,
) -> dict[str, Any] | None:
    if artifact is None:
        return None
    observations = []
    for item in executed_checks:
        execution = item.get("execution")
        execution = execution if isinstance(execution, dict) else {}
        observations.append(
            {
                "check_index": item.get("check_index"),
                "role": item.get("normalized_probe", {}).get("role"),
                "expression": item.get("expression"),
                "expression_sha256": execution.get("assert_sha256"),
                "terminal_result": execution.get("result", item.get("result")),
                "value": execution.get("value"),
                "function_call_trace": execution.get("function_call_trace", []),
            }
        )
    return {
        "schema": "paper1.execution_certificate.v1",
        "evaluated_artifact": pair["paths"]["fcstm"],
        "evaluated_artifact_sha256": _sha256(pair["fcstm"]),
        "compiled_assertion_sha256": artifact["compiled_assertion_sha256"],
        "engine": {
            "adapter": "paper_stm_feedback_loop.assertions",
            "formal_verification_enabled": True,
            "fbmcq_solver_timeout_ms": 5_000,
            "fbmcq_max_bound": 8,
        },
        "observations": observations,
        "terminal": terminal,
        "precondition_failed": precondition_failed,
        "counterexample_found": counterexample_found,
        "verdict": (
            "counterexample"
            if counterexample_found
            else "satisfied"
            if terminal and not precondition_failed
            else "inconclusive"
        ),
    }


def normalize_check(
    check: ProbeCheck, inspect: dict[str, Any], pair: dict[str, Any] | None = None
) -> tuple[ProbeCheck, list[dict[str, str]]]:
    """Apply only declared source-to-FCSTM namespace mappings."""

    updates: dict[str, Any] = {}
    normalizations: list[dict[str, str]] = []
    field_inventories = {
        "source": ("states", "path"),
        "target": ("states", "path"),
        "trigger": ("events", "qualified_name"),
    }

    declared_mappings: dict[str, dict[str, set[str]]] = {
        "states": {},
        "events": {},
        "variables": {},
    }
    if pair is not None:
        for element in pair["working_contract"].get("elements", []):
            if not isinstance(element, dict):
                continue
            fields = element.get("semantic_fields")
            fields = fields if isinstance(fields, dict) else {}
            metadata = element.get("metadata")
            metadata = metadata if isinstance(metadata, dict) else {}
            if element.get("kind") == "state":
                source_id = metadata.get("source_state_id")
                fcstm_id = metadata.get("fcstm_path") or fields.get("fcstm_identifier")
                table = "states"
            elif element.get("kind") == "opaque_event_projection":
                source_id = fields.get("raw_label")
                fcstm_id = fields.get("fcstm_identifier")
                table = "events"
            else:
                continue
            if isinstance(source_id, str) and isinstance(fcstm_id, str):
                declared_mappings[table].setdefault(source_id, set()).add(fcstm_id)

    def resolve(value: Any, table: str, key: str) -> str | None:
        if not isinstance(value, str) or not value or value == "[*]":
            return None
        inventory = {
            str(row[key])
            for row in inspect.get(table, [])
            if isinstance(row, dict) and isinstance(row.get(key), str)
        }
        if value in inventory:
            return value
        mapped = declared_mappings.get(table, {}).get(value, set())
        exact_mapped = sorted(item for item in mapped if item in inventory)
        return exact_mapped[0] if len(exact_mapped) == 1 else None

    for field, (table, key) in field_inventories.items():
        value = getattr(check, field)
        resolved = resolve(value, table, key)
        if resolved is None or resolved == value:
            continue
        updates[field] = resolved
        normalizations.append({"field": field, "from": value, "to": resolved})

    binding_inventories = {
        "state": ("states", "path"),
        "parent": ("states", "path"),
        "child": ("states", "path"),
        "composite": ("states", "path"),
        "source": ("states", "path"),
        "target": ("states", "path"),
        "scope": ("states", "path"),
        "trigger": ("events", "qualified_name"),
        "event": ("events", "qualified_name"),
        "variable": ("variables", "qualified_name"),
    }
    bindings = dict(check.bindings)
    for binding, (table, key) in binding_inventories.items():
        value = bindings.get(binding)
        resolved = resolve(value, table, key)
        if resolved is None or resolved == value:
            continue
        bindings[binding] = resolved
        normalizations.append(
            {"field": f"bindings.{binding}", "from": str(value), "to": resolved}
        )
    if bindings != check.bindings:
        updates["bindings"] = bindings

    return check.model_copy(update=updates), normalizations


def _compiler_exclusion_payload(reference: str) -> str | None:
    """Project only declared compiler-reference kinds to runtime formal IDs."""

    parts = reference.split(":", 2)
    if len(parts) != 3 or parts[0] != "compiler":
        return None
    if parts[1] not in {"state", "event_projection", "root", "route_control"}:
        return None
    return parts[2] or None


def _reference_matches_exclusion(reference: str, exclusions: list[str]) -> bool:
    formal_ref = reference.strip()
    if not formal_ref:
        return False
    for exclusion in exclusions:
        declared_ref = str(exclusion).strip()
        if formal_ref == declared_ref or formal_ref == _compiler_exclusion_payload(
            declared_ref
        ):
            return True
    return False


def classify_attribution(execution: dict[str, Any], exclusions: list[str]) -> str:
    refs = {
        str(ref)
        for call in execution.get("function_call_trace", [])
        if isinstance(call, dict)
        for ref in call.get("model_refs", [])
        if isinstance(ref, str) and ref
    }
    if "simulation:path_taint:ambiguous" in refs:
        return "unattributed"
    if any(_reference_matches_exclusion(ref, exclusions) for ref in refs):
        return "representation_debt"
    return "safe" if refs else "unattributed"


def _strip_pair_root(reference: str, pair_name: str) -> str:
    prefix = f"{pair_name}."
    return reference.removeprefix(prefix)


def _source_model(pair: dict[str, Any]) -> dict[str, Any]:
    model = pair["canonical"].get("model", {})
    return model if isinstance(model, dict) else {}


def _source_root_scope_id(pair: dict[str, Any]) -> str | None:
    name = _source_model(pair).get("name")
    return name if isinstance(name, str) and name else None


def _source_state_ids(pair: dict[str, Any]) -> set[str]:
    return {
        item["id"]
        for item in _source_model(pair).get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _source_final_target_ids(pair: dict[str, Any]) -> set[str]:
    return {
        item["target"]
        for item in _source_model(pair).get("transitions", [])
        if isinstance(item, dict)
        and isinstance(item.get("target"), str)
        and isinstance(item.get("attributes"), dict)
        and item["attributes"].get("transition_kind") == "final"
    }


def _source_has_concurrent_separator(pair: dict[str, Any]) -> bool:
    """Read concurrency only from the structured PlantUML canonical model."""

    return bool(_source_model(pair).get("concurrent_regions"))


def _resolve_source_state(
    pair: dict[str, Any], reference: str
) -> tuple[str | None, dict[str, Any] | None]:
    model = _source_model(pair)
    states = [item for item in model.get("states", []) if isinstance(item, dict)]
    normalized = _strip_pair_root(reference, pair["pair_name"])
    exact = [item for item in states if item.get("id") == normalized]
    if len(exact) == 1:
        return normalized, exact[0]
    return None, None


def _source_reachability(
    model: dict[str, Any], target: str
) -> tuple[bool, list[str], list[str]]:
    states = {
        str(item["id"])
        for item in model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    transitions = [
        item for item in model.get("transitions", []) if isinstance(item, dict)
    ]
    adjacency: dict[str, list[tuple[str, str]]] = {}
    starts: list[tuple[str, str]] = []
    for transition in transitions:
        source = transition.get("source")
        destination = transition.get("target")
        if not isinstance(source, str) or not isinstance(destination, str):
            continue
        if destination not in states:
            continue
        transition_id = str(transition.get("id") or transition.get("raw_ref") or "")
        kind = transition.get("attributes", {}).get("transition_kind")
        if kind == "initial" and source == "@initial:__root__":
            starts.append((destination, transition_id))
        elif kind == "initial":
            scope = transition.get("scope")
            if isinstance(scope, str) and scope in states:
                adjacency.setdefault(scope, []).append((destination, transition_id))
        elif source in states:
            adjacency.setdefault(source, []).append((destination, transition_id))

    queue: list[str] = []
    parents: dict[str, tuple[str | None, str]] = {}
    for state, transition_id in starts:
        if state not in parents:
            parents[state] = (None, transition_id)
            queue.append(state)
    while queue:
        state = queue.pop(0)
        if state == target:
            break
        for destination, transition_id in adjacency.get(state, []):
            if destination in parents:
                continue
            parents[destination] = (state, transition_id)
            queue.append(destination)
    if target not in parents:
        return False, [], []

    state_path: list[str] = []
    transition_path: list[str] = []
    cursor: str | None = target
    while cursor is not None:
        state_path.append(cursor)
        parent, transition_id = parents[cursor]
        transition_path.append(transition_id)
        cursor = parent
    state_path.reverse()
    transition_path.reverse()
    return True, state_path, transition_path


def _source_deadlock_certificate(
    pair: dict[str, Any], target_reference: str
) -> dict[str, Any] | None:
    model = _source_model(pair)
    target, target_state = _resolve_source_state(pair, target_reference)
    if not target or not target_state:
        return None

    states = {
        str(item["id"]): item
        for item in model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    scopes: list[str] = []
    cursor: str | None = target
    while cursor and cursor in states:
        scopes.append(cursor)
        parent = states[cursor].get("parent")
        cursor = str(parent) if isinstance(parent, str) and parent else None

    outgoing = [
        {
            "id": transition.get("id"),
            "source": transition.get("source"),
            "target": transition.get("target"),
            "raw_ref": transition.get("raw_ref"),
        }
        for transition in model.get("transitions", [])
        if isinstance(transition, dict)
        and transition.get("source") in scopes
        and transition.get("attributes", {}).get("transition_kind") != "initial"
    ]
    reachable, state_path, transition_path = _source_reachability(model, target)
    final_states = {str(item) for item in model.get("final_states", [])}
    explicit_final = target in final_states
    transition_by_id = {
        str(item.get("id")): item
        for item in model.get("transitions", [])
        if isinstance(item, dict) and item.get("id")
    }
    path_has_no_guards = all(
        not transition_by_id.get(transition_id, {}).get("guard")
        for transition_id in transition_path
    )
    assumptions = {
        "no_concurrent_regions": not bool(model.get("concurrent_regions"))
        and not _source_has_concurrent_separator(pair),
        "path_has_no_guards": path_has_no_guards,
        "target_is_root_level": target_state.get("parent") is None,
        "target_identity_resolved_exactly": True,
    }
    sound_for_claim = all(assumptions.values())
    counterexample = (
        sound_for_claim and reachable and not explicit_final and not outgoing
    )
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "reachable_deadlock",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": "reachable(target) and not explicit_final(target) and inherited_outgoing(target) == 0",
        "target": target,
        "reachable": reachable,
        "state_path": state_path,
        "transition_path": transition_path,
        "explicit_final": explicit_final,
        "active_scopes_checked": scopes,
        "outgoing": outgoing,
        "assumptions": assumptions,
        "sound_for_claim": sound_for_claim,
        "prototype_semantics": "existential_guard_free_sequential_fragment",
        "result": counterexample,
        "verdict": (
            "counterexample"
            if counterexample
            else "inconclusive"
            if not sound_for_claim
            else "not_established"
        ),
    }


def _source_concurrent_region_deadlock_certificate(
    pair: dict[str, Any], target_reference: str
) -> dict[str, Any] | None:
    """Certify one blocked state through the complete orthogonal entry tuple."""

    model = _source_model(pair)
    target, target_state = _resolve_source_state(pair, target_reference)
    if not target or not target_state:
        return None
    regions = [
        item for item in model.get("concurrent_regions", []) if isinstance(item, dict)
    ]
    target_regions = [
        item
        for item in regions
        if target
        in {
            str(state_id)
            for state_id in item.get("state_ids", [])
            if isinstance(state_id, str)
        }
    ]
    if len(target_regions) != 1:
        return None
    owner = target_regions[0].get("owner_scope")
    if not isinstance(owner, str) or not owner:
        return None
    owner_regions = [item for item in regions if item.get("owner_scope") == owner]
    if len(owner_regions) < 2:
        return None

    states = {
        str(item["id"]): item
        for item in model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    transitions = [
        item for item in model.get("transitions", []) if isinstance(item, dict)
    ]
    transition_by_id = {
        str(item.get("id")): item for item in transitions if item.get("id") is not None
    }
    active_targets: list[str] = []
    region_receipts: list[dict[str, Any]] = []
    initial_edges_complete = True
    initial_edges_unconditional = True
    for region in sorted(
        owner_regions, key=lambda item: int(item.get("region_index", 0))
    ):
        transition_ids = {
            str(item)
            for item in region.get("transition_ids", [])
            if isinstance(item, str)
        }
        initial_edges = [
            item
            for item in transitions
            if item.get("id") in transition_ids
            and item.get("attributes", {}).get("transition_kind") == "initial"
            and item.get("scope") == owner
        ]
        if len(initial_edges) != 1:
            initial_edges_complete = False
            initial_target = None
        else:
            initial_target = initial_edges[0].get("target")
            initial_edges_unconditional = initial_edges_unconditional and not bool(
                initial_edges[0].get("event") or initial_edges[0].get("guard")
            )
            if not isinstance(initial_target, str) or initial_target not in states:
                initial_edges_complete = False
                initial_target = None
            else:
                active_targets.append(initial_target)
        region_receipts.append(
            {
                "region_id": region.get("id"),
                "region_index": region.get("region_index"),
                "initial_transition_ids": [item.get("id") for item in initial_edges],
                "initial_target": initial_target,
            }
        )

    active_targets_are_leaves = bool(active_targets) and all(
        not any(state.get("parent") == active for state in states.values())
        for active in active_targets
    )
    final_states = {str(item) for item in model.get("final_states", [])}
    active_targets_nonfinal = bool(active_targets) and all(
        active not in final_states for active in active_targets
    )
    owner_reachable, owner_state_path, owner_transition_path = _source_reachability(
        model, owner
    )
    entry_path_has_no_guards = all(
        not transition_by_id.get(transition_id, {}).get("guard")
        for transition_id in owner_transition_path
    )

    active_scopes = set(active_targets)
    cursor: str | None = owner
    while cursor and cursor in states:
        active_scopes.add(cursor)
        parent = states[cursor].get("parent")
        cursor = str(parent) if isinstance(parent, str) and parent else None
    enabled_outgoing = [
        _compact_transition_for_d(item)
        for item in transitions
        if item.get("source") in active_scopes
        and item.get("attributes", {}).get("transition_kind") != "initial"
    ]
    assumptions = {
        "all_regions_have_one_initial": initial_edges_complete,
        "all_region_initials_unconditional": initial_edges_unconditional,
        "all_active_targets_leaf": active_targets_are_leaves,
        "all_active_targets_nonfinal": active_targets_nonfinal,
        "entry_path_has_no_guards": entry_path_has_no_guards,
        "no_enabled_outgoing": not enabled_outgoing,
        "owner_identity_resolved_exactly": owner in states,
        "target_is_active_region_entry": target in active_targets,
    }
    sound_for_claim = owner_reachable and all(assumptions.values())
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "concurrent_region_deadlock",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": (
            "reachable(owner) and all concurrent regions enter one non-final leaf "
            "and inherited_outgoing(active_configuration) == 0"
        ),
        "target": target,
        "owner_scope": owner,
        "reachable": owner_reachable,
        "state_path": owner_state_path,
        "transition_path": owner_transition_path,
        "explicit_final": target in final_states,
        "blocked_region_targets": active_targets,
        "region_entry_receipts": region_receipts,
        "active_scopes_checked": sorted(active_scopes),
        "outgoing": enabled_outgoing,
        "assumptions": assumptions,
        "sound_for_claim": sound_for_claim,
        "prototype_semantics": "exact_guard_free_concurrent_entry_configuration",
        "result": sound_for_claim,
        "verdict": "counterexample" if sound_for_claim else "inconclusive",
    }


def _source_entry_deadlock_certificate(
    pair: dict[str, Any], target_reference: str, parent_reference: str | None
) -> dict[str, Any] | None:
    """Bridge a compiler fail-closed entry leaf to its exact source composite."""

    if not isinstance(parent_reference, str) or not parent_reference:
        return None
    model = _source_model(pair)
    scope, scope_state = _resolve_source_state(pair, parent_reference)
    if not scope or not scope_state:
        return None
    exact_target = target_reference.removeprefix(f"{pair['pair_name']}.")
    formal_target = (
        target_reference
        if target_reference.startswith(f"{pair['pair_name']}.")
        else f"{pair['pair_name']}.{exact_target}"
    )
    generated_states: list[dict[str, Any]] = []
    generated_transitions: list[dict[str, Any]] = []
    expected_state_ref = f"state:{formal_target}"
    for element in pair["working_contract"].get("elements", []):
        if not isinstance(element, dict):
            continue
        metadata = element.get("metadata")
        metadata = metadata if isinstance(metadata, dict) else {}
        if metadata.get("generated_reason") != "missing_source_initial_fail_closed":
            continue
        model_refs = element.get("model_refs")
        model_refs = model_refs if isinstance(model_refs, list) else []
        if element.get("kind") == "synthetic_state" and model_refs == [
            expected_state_ref
        ]:
            generated_states.append(
                {
                    "element_id": element.get("element_id"),
                    "model_refs": model_refs,
                }
            )
        if (
            element.get("kind") == "synthetic_transition"
            and metadata.get("owner_state_id") == scope
            and metadata.get("scope") == scope
        ):
            element_id = str(element.get("element_id") or "")
            expected_model_ref = "fcstm-transition:" + element_id.removeprefix(
                "compiler:synthetic_transition:"
            )
            generated_transitions.append(
                {
                    "element_id": element_id,
                    "model_refs": model_refs,
                    "model_ref_exact": model_refs == [expected_model_ref],
                    "owner_state_id": metadata.get("owner_state_id"),
                    "scope": metadata.get("scope"),
                    "line": metadata.get("line"),
                    "scope_line_occurrence": metadata.get("scope_line_occurrence"),
                }
            )

    # Read the emitted target from the public grammar AST.  The working contract
    # only identifies the synthetic transition; it does not itself carry its
    # target, so counting synthetic elements cannot establish this bridge.
    fcstm_initial_targets: list[dict[str, Any]] = []
    try:
        from pyfcstm.dsl import parse_with_grammar_entry
        from pyfcstm.dsl.node import INIT_STATE

        ast = parse_with_grammar_entry(pair["fcstm"], "state_machine_dsl")
        selected_scope: Any | None = None
        selected_scope_path: str | None = None
        fcstm_state_paths: set[str] = set()

        def visit(node: Any, parent: str | None) -> None:
            nonlocal selected_scope, selected_scope_path
            name = getattr(node, "name", None)
            if not isinstance(name, str):
                return
            path = name if parent is None else f"{parent}.{name}"
            fcstm_state_paths.add(path)
            if _strip_pair_root(path, pair["pair_name"]) == scope:
                selected_scope = node
                selected_scope_path = path
            for child in getattr(node, "substates", []):
                visit(child, path)

        visit(ast.root_state, None)
        if selected_scope is not None and selected_scope_path is not None:
            source_lines = pair["fcstm"].splitlines()
            occurrences: dict[str, int] = {}
            for transition in getattr(selected_scope, "transitions", []):
                if getattr(transition, "from_state", None) is not INIT_STATE:
                    continue
                raw_target = getattr(transition, "to_state", None)
                if not isinstance(raw_target, str) or not raw_target:
                    continue
                span = getattr(transition, "_span", None)
                line_number = getattr(span, "line", None)
                line = (
                    source_lines[line_number - 1].strip()
                    if isinstance(line_number, int)
                    and 0 < line_number <= len(source_lines)
                    else None
                )
                if not isinstance(line, str) or not line:
                    continue
                occurrences[line] = occurrences.get(line, 0) + 1
                target = (
                    raw_target
                    if raw_target.startswith(f"{pair['pair_name']}.")
                    else f"{selected_scope_path}.{raw_target}"
                )
                fcstm_initial_targets.append(
                    {
                        "line": line,
                        "scope_line_occurrence": occurrences[line],
                        "line_number": line_number,
                        "target": target,
                        "target_declared": target in fcstm_state_paths,
                    }
                )
    except Exception:  # noqa: BLE001 - malformed FCSTM must fail the bridge closed
        fcstm_initial_targets = []

    bridge_receipts = []
    for transition in generated_transitions:
        line = transition.get("line")
        occurrence = transition.get("scope_line_occurrence")
        matches = [
            row
            for row in fcstm_initial_targets
            if row.get("line") == line
            and row.get("scope_line_occurrence") == occurrence
        ]
        target = matches[0].get("target") if len(matches) == 1 else None
        matches_synthetic_state = (
            len(matches) == 1
            and transition.get("model_ref_exact") is True
            and target == formal_target
            and matches[0].get("target_declared") is True
        )
        bridge_receipts.append(
            {
                "transition_element_id": transition.get("element_id"),
                "transition_model_refs": transition.get("model_refs", []),
                "fcstm_initial_transition": matches[0] if len(matches) == 1 else None,
                "fcstm_target": target,
                "matches_synthetic_state": matches_synthetic_state,
            }
        )
    compiler_bridge_transition_target_exact = (
        len(bridge_receipts) == 1
        and bridge_receipts[0]["matches_synthetic_state"] is True
    )

    states = {
        str(item["id"]): item
        for item in model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    transitions = [
        item for item in model.get("transitions", []) if isinstance(item, dict)
    ]
    initial_edges = [
        item
        for item in transitions
        if item.get("attributes", {}).get("transition_kind") == "initial"
        and item.get("scope") == scope
    ]
    direct_children = [
        {"id": item.get("id"), "raw_ref": item.get("raw_ref")}
        for item in states.values()
        if item.get("parent") == scope
    ]
    active_scopes: list[str] = []
    cursor: str | None = scope
    while cursor and cursor in states:
        active_scopes.append(cursor)
        parent = states[cursor].get("parent")
        cursor = str(parent) if isinstance(parent, str) and parent else None
    inherited_outgoing = [
        _compact_transition_for_d(item)
        for item in transitions
        if item.get("source") in active_scopes
        and item.get("attributes", {}).get("transition_kind") != "initial"
    ]
    reachable, state_path, transition_path = _source_reachability(model, scope)
    transition_by_id = {
        str(item.get("id")): item for item in transitions if item.get("id") is not None
    }
    path_has_no_guards = all(
        not transition_by_id.get(transition_id, {}).get("guard")
        for transition_id in transition_path
    )
    assumptions = {
        "source_scope_reachable": reachable,
        "entry_path_has_no_guards": path_has_no_guards,
        "missing_source_initial": not initial_edges,
        "source_has_direct_children": bool(direct_children),
        "no_inherited_outgoing": not inherited_outgoing,
        "compiler_bridge_exact": len(generated_states) == 1
        and len(generated_transitions) == 1
        and compiler_bridge_transition_target_exact,
        "compiler_bridge_transition_target_exact": compiler_bridge_transition_target_exact,
        "no_concurrent_regions": not _source_has_concurrent_separator(pair),
    }
    sound_for_claim = all(assumptions.values())
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "source_entry_deadlock",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": (
            "reachable(scope) and initial_edge_count(scope) == 0 and "
            "inherited_outgoing(scope) == 0 and compiler_fail_closed_leaf(target)"
        ),
        "target": formal_target,
        "scope": scope,
        "reachable": reachable,
        "state_path": state_path,
        "transition_path": transition_path,
        "explicit_final": False,
        "direct_children": direct_children,
        "initial_edges": [_compact_transition_for_d(item) for item in initial_edges],
        "active_scopes_checked": active_scopes,
        "outgoing": inherited_outgoing,
        "compiler_causal_bridge": {
            "states": generated_states,
            "transitions": generated_transitions,
            "initial_target_receipts": bridge_receipts,
        },
        "assumptions": assumptions,
        "sound_for_claim": sound_for_claim,
        "prototype_semantics": "exact_missing_initial_fail_closed_entry_fragment",
        "result": sound_for_claim,
        "verdict": "counterexample" if sound_for_claim else "inconclusive",
    }


def _source_stable_termination_certificate(
    pair: dict[str, Any], target_reference: str
) -> dict[str, Any] | None:
    """Refute a grounded terminal target with exact source-graph continuation."""

    model = _source_model(pair)
    target, target_state = _resolve_source_state(pair, target_reference)
    if not target or not target_state:
        return None
    states = {
        str(item["id"]): item
        for item in model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    ancestor_chain: list[str] = []
    cursor: str | None = target
    while cursor and cursor in states:
        ancestor_chain.append(cursor)
        parent = states[cursor].get("parent")
        cursor = str(parent) if isinstance(parent, str) and parent else None

    transitions = [
        item for item in model.get("transitions", []) if isinstance(item, dict)
    ]
    continuing = [
        {
            "id": item.get("id"),
            "source": item.get("source"),
            "target": item.get("target"),
            "event": item.get("event"),
            "guard": item.get("guard"),
            "raw_ref": item.get("raw_ref"),
        }
        for item in transitions
        if item.get("source") in ancestor_chain
        and item.get("attributes", {}).get("transition_kind")
        not in {"initial", "final"}
        and not item.get("guard")
    ]
    root_final_edges = [
        {
            "id": item.get("id"),
            "source": item.get("source"),
            "target": item.get("target"),
            "raw_ref": item.get("raw_ref"),
        }
        for item in transitions
        if item.get("attributes", {}).get("transition_kind") == "final"
        and item.get("target") == "@final:__root__"
    ]
    final_states = {str(item) for item in model.get("final_states", [])}
    explicit_final = target in final_states
    reachable, state_path, transition_path = _source_reachability(model, target)
    transition_by_id = {
        str(item.get("id")): item for item in transitions if item.get("id") is not None
    }
    path_has_no_guards = all(
        not transition_by_id.get(transition_id, {}).get("guard")
        for transition_id in transition_path
    )
    assumptions = {
        "no_concurrent_regions": not _source_has_concurrent_separator(pair),
        "target_identity_resolved_exactly": True,
        "entry_path_has_no_guards": path_has_no_guards,
        "open_event_environment": True,
    }
    sound_for_claim = all(assumptions.values())
    counterexample = bool(
        sound_for_claim and reachable and not explicit_final and continuing
    )
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "source_unstable_termination_target",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": (
            "reachable(target) and not explicit_final(target) and "
            "guard_free_inherited_continuation_count(target) > 0"
        ),
        "target": target,
        "reachable": reachable,
        "state_path": state_path,
        "transition_path": transition_path,
        "ancestor_chain": ancestor_chain,
        "explicit_final": explicit_final,
        "root_final_edges": root_final_edges,
        "root_final_edge_count": len(root_final_edges),
        "continuing_transitions": continuing,
        "assumptions": assumptions,
        "sound_for_claim": sound_for_claim,
        "prototype_semantics": "exact_source_open-event_stable-terminal_fragment",
        "result": counterexample,
        "verdict": (
            "counterexample"
            if counterexample
            else "inconclusive"
            if not sound_for_claim
            else "not_established"
        ),
    }


def _source_missing_initial_certificate(
    pair: dict[str, Any], target_reference: str
) -> dict[str, Any] | None:
    model = _source_model(pair)
    target, target_state = _resolve_source_state(pair, target_reference)
    if not target or not target_state:
        return None
    states = {
        str(item["id"]): item
        for item in model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    transitions = [
        item for item in model.get("transitions", []) if isinstance(item, dict)
    ]

    cursor = target_state.get("parent")
    missing_scope: str | None = None
    children: list[dict[str, Any]] = []
    while isinstance(cursor, str) and cursor in states:
        direct_children = [
            item for item in states.values() if item.get("parent") == cursor
        ]
        initial_edges = [
            item
            for item in transitions
            if item.get("attributes", {}).get("transition_kind") == "initial"
            and item.get("scope") == cursor
        ]
        if len(direct_children) >= 2 and not initial_edges:
            missing_scope = cursor
            children = direct_children
            break
        cursor = states[cursor].get("parent")
    if not missing_scope:
        return None

    generated = []
    for element in pair["working_contract"].get("elements", []):
        if not isinstance(element, dict):
            continue
        metadata = element.get("metadata")
        metadata = metadata if isinstance(metadata, dict) else {}
        element_id = str(element.get("element_id") or "")
        if (
            metadata.get("generated_reason") == "missing_source_initial_fail_closed"
            and missing_scope in element_id
        ):
            generated.append(
                {
                    "element_id": element_id,
                    "generated_reason": metadata.get("generated_reason"),
                }
            )
    source_assertion_result = bool(children)
    causal_bridge_result = bool(generated)
    counterexample = source_assertion_result and causal_bridge_result
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "missing_initial_with_compiler_consequence",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": "direct_child_count(scope) >= 2 and initial_edge_count(scope) == 0",
        "scope": missing_scope,
        "target_consequence": target,
        "direct_children": [
            {"id": item.get("id"), "raw_ref": item.get("raw_ref")} for item in children
        ],
        "initial_edge_count": 0,
        "compiler_causal_bridge": generated,
        "source_assertion_result": source_assertion_result,
        "causal_bridge_result": causal_bridge_result,
        "sound_for_claim": True,
        "prototype_semantics": "exact_static_initial-edge_fragment",
        "source_behavior_equivalence_claimed": False,
        "result": counterexample,
        "verdict": "counterexample" if counterexample else "not_established",
    }


def _source_unreachable_certificate(
    pair: dict[str, Any], target_reference: str
) -> dict[str, Any] | None:
    model = _source_model(pair)
    target, target_state = _resolve_source_state(pair, target_reference)
    if not target or not target_state:
        return None
    reachable, _, _ = _source_reachability(model, target)
    if reachable:
        return None
    states = {
        str(item["id"]): item
        for item in model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    component = target
    cursor = target_state
    while isinstance(cursor.get("parent"), str) and cursor["parent"] in states:
        component = str(cursor["parent"])
        cursor = states[component]
    transitions = [
        item for item in model.get("transitions", []) if isinstance(item, dict)
    ]
    incoming = [
        {
            "id": item.get("id"),
            "source": item.get("source"),
            "target": item.get("target"),
            "raw_ref": item.get("raw_ref"),
        }
        for item in transitions
        if isinstance(item.get("target"), str)
        and (
            item["target"] == component
            or str(item["target"]).startswith(f"{component}.")
        )
        and not (
            isinstance(item.get("source"), str)
            and (
                item["source"] == component
                or str(item["source"]).startswith(f"{component}.")
                or item["source"] == f"@initial:{component}"
            )
        )
    ]
    assumptions = {
        "no_concurrent_regions": not bool(model.get("concurrent_regions"))
        and not _source_has_concurrent_separator(pair),
        "target_identity_resolved_exactly": True,
        "guard_agnostic_absence_is_sound": True,
    }
    sound_for_claim = all(assumptions.values())
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "unreachable_source_component",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": "no source-graph path from root entry to target",
        "target": target,
        "component": component,
        "cross_component_incoming": incoming,
        "assumptions": assumptions,
        "sound_for_claim": sound_for_claim,
        "prototype_semantics": "exact_guard_agnostic_absence_fragment",
        "result": sound_for_claim,
        "verdict": "counterexample" if sound_for_claim else "inconclusive",
    }


def _source_root_target_reachability_certificate(
    pair: dict[str, Any], target_reference: str
) -> dict[str, Any] | None:
    """Certify a root-to-target reachability counterexample on the source AST.

    The topology backend can evaluate a root query on the converted FCSTM, but
    that result alone does not attribute the failure to the authored source.
    This companion certificate repeats the same exact root reachability query
    over the canonical source graph and is emitted only for the machine root.
    It deliberately fails closed for concurrent regions because this prototype
    does not claim a sequential source semantics for orthogonal regions.
    """

    model = _source_model(pair)
    target, target_state = _resolve_source_state(pair, target_reference)
    root_scope = _source_root_scope_id(pair)
    if not target or not target_state or not root_scope:
        return None
    reachable, state_path, transition_path = _source_reachability(model, target)
    root_initial_edges = [
        {
            "id": transition.get("id"),
            "target": transition.get("target"),
            "raw_ref": transition.get("raw_ref"),
        }
        for transition in model.get("transitions", [])
        if isinstance(transition, dict)
        and transition.get("attributes", {}).get("transition_kind") == "initial"
        and transition.get("source") == "@initial:__root__"
    ]
    concurrent = bool(model.get("concurrent_regions")) or _source_has_concurrent_separator(pair)
    assumptions = {
        "root_source_identity_exact": True,
        "target_identity_resolved_exactly": True,
        "no_concurrent_regions": not concurrent,
        "guard_agnostic_absence_is_sound": True,
    }
    sound_for_claim = all(assumptions.values())
    counterexample = sound_for_claim and not reachable
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "source_root_target_unreachable",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": "no source-graph path from the exact root entry to target",
        "source": root_scope,
        "target": target,
        "reachable": reachable,
        "state_path": state_path,
        "transition_path": transition_path,
        "root_initial_edges": root_initial_edges,
        "root_initial_edge_count": len(root_initial_edges),
        "assumptions": assumptions,
        "sound_for_claim": sound_for_claim,
        "prototype_semantics": "exact_source_root_reachability_fragment",
        "result": counterexample,
        "verdict": (
            "counterexample"
            if counterexample
            else "satisfied"
            if sound_for_claim
            else "inconclusive"
        ),
    }


def _source_initial_contract_certificate(
    pair: dict[str, Any], composite_reference: str
) -> dict[str, Any] | None:
    model = _source_model(pair)
    root_reference = pair["pair_name"]
    normalized = _strip_pair_root(composite_reference, pair["pair_name"])
    scope = (
        None if composite_reference == root_reference or not normalized else normalized
    )
    initial_edges = [
        item
        for item in model.get("transitions", [])
        if isinstance(item, dict)
        and item.get("attributes", {}).get("transition_kind") == "initial"
        and item.get("scope") == scope
    ]
    if not initial_edges:
        return None
    unconditional = [
        item
        for item in initial_edges
        if not item.get("event") and not item.get("guard")
    ]
    if unconditional:
        return None
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "initial_contract_violation",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": "initial_edge_count(scope) >= 1 and unconditional_initial_edge_count(scope) == 0",
        "scope": scope or "__root__",
        "initial_edges": [
            {
                "id": item.get("id"),
                "event": item.get("event"),
                "guard": item.get("guard"),
                "target": item.get("target"),
                "raw_ref": item.get("raw_ref"),
            }
            for item in initial_edges
        ],
        "unconditional_initial_edge_count": 0,
        "sound_for_claim": True,
        "prototype_semantics": "exact_static_initial-contract_fragment",
        "result": True,
        "verdict": "counterexample",
    }


def _source_initial_target_certificate(
    pair: dict[str, Any], composite_reference: str, child_reference: str
) -> dict[str, Any] | None:
    model = _source_model(pair)
    root_scope_id = _source_root_scope_id(pair)
    is_root_scope = composite_reference == root_scope_id
    if is_root_scope:
        composite = None
        composite_state = {"id": root_scope_id}
    else:
        composite, composite_state = _resolve_source_state(pair, composite_reference)
    child, child_state = _resolve_source_state(pair, child_reference)
    if (
        (not is_root_scope and (not composite or not composite_state))
        or not child
        or not child_state
    ):
        return None
    initial_edges = [
        item
        for item in model.get("transitions", [])
        if isinstance(item, dict)
        and item.get("attributes", {}).get("transition_kind") == "initial"
        and item.get("scope") == composite
    ]
    matching_edges = [item for item in initial_edges if item.get("target") == child]
    attempted_entry_edges = [
        item
        for item in model.get("transitions", [])
        if isinstance(item, dict)
        and item.get("source") == composite
        and item.get("target") == child
        and item.get("attributes", {}).get("transition_kind") == "normal"
        and not item.get("event")
        and not item.get("guard")
    ]
    direct_children = [
        str(item["id"])
        for item in model.get("states", [])
        if isinstance(item, dict)
        and isinstance(item.get("id"), str)
        and item.get("parent") == composite
    ]
    # An authored initial edge proves that the source treats this scope as a
    # composite even when all of its children are malformed or absent.  A leaf
    # with no children and no initial edge remains an inconclusive request.
    # An eventless authored edge from the named scope to the named target is
    # itself formal evidence that the author attempted to encode default entry
    # using an ordinary completion edge.  It is not an initial pseudostate edge,
    # so it still witnesses the contract violation even when the source parser
    # represents the named scope as a leaf.  An eventful edge (for example
    # ``AutonomousMode -> InitialState : initial``) is deliberately excluded:
    # it may be a normal sequential route and cannot establish default-entry
    # intent without an explicit initial construct.
    scope_supports_initial = (
        is_root_scope
        or bool(direct_children)
        or bool(initial_edges)
        or bool(attempted_entry_edges)
    )
    target_is_direct_child = child_state.get("parent") == composite
    actual = bool(matching_edges) and target_is_direct_child
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "source_initial_target_contract",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": "an initial edge targets a direct child in the same composite scope",
        "composite": root_scope_id if is_root_scope else composite,
        "child": child,
        "actual_parent": child_state.get("parent"),
        "initial_edges": [
            {
                "id": item.get("id"),
                "target": item.get("target"),
                "scope": item.get("scope"),
                "raw_ref": item.get("raw_ref"),
            }
            for item in initial_edges
        ],
        "attempted_entry_edges": [
            {
                "id": item.get("id"),
                "source": item.get("source"),
                "target": item.get("target"),
                "scope": item.get("scope"),
                "raw_ref": item.get("raw_ref"),
            }
            for item in attempted_entry_edges
        ],
        "attempted_entry_edge_count": len(attempted_entry_edges),
        "matching_edge_count": len(matching_edges),
        "direct_children": direct_children,
        "scope_supports_initial": scope_supports_initial,
        "target_is_direct_child": target_is_direct_child,
        "actual": actual,
        "expected": True,
        "sound_for_claim": scope_supports_initial,
        "result": scope_supports_initial and not actual,
        "verdict": (
            "counterexample"
            if scope_supports_initial and not actual
            else "satisfied"
            if scope_supports_initial
            else "inconclusive"
        ),
        "prototype_semantics": "exact_source_initial-target-scope_fragment",
    }


def _source_containment_certificate(
    pair: dict[str, Any],
    child_reference: str,
    expected_parent_reference: str,
    *,
    expected: bool = True,
) -> dict[str, Any] | None:
    model = _source_model(pair)
    child, child_state = _resolve_source_state(pair, child_reference)
    expected_parent, parent_state = _resolve_source_state(
        pair, expected_parent_reference
    )
    if not child or not child_state or not expected_parent or not parent_state:
        return None
    states = {
        str(item["id"]): item
        for item in model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    actual_parent = child_state.get("parent")
    actual_ancestor_chain: list[str] = []
    cursor = actual_parent
    while isinstance(cursor, str) and cursor in states:
        actual_ancestor_chain.append(cursor)
        cursor = states[cursor].get("parent")
    actual = actual_parent == expected_parent
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "source_containment_contract",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": (
            "the named child has the expected direct parent"
            if expected
            else "the named child does not have the forbidden direct parent"
        ),
        "child": child,
        "expected_parent": expected_parent,
        "actual_parent": actual_parent,
        "actual_ancestor_chain": actual_ancestor_chain,
        "within_expected_ancestor": expected_parent in actual_ancestor_chain,
        "child_raw_ref": child_state.get("raw_ref"),
        "expected_parent_raw_ref": parent_state.get("raw_ref"),
        "actual": actual,
        "expected": expected,
        "sound_for_claim": True,
        "result": actual != expected,
        "verdict": "counterexample" if actual != expected else "satisfied",
        "prototype_semantics": "exact_source_direct-containment_fragment",
    }


def _source_wrong_scope_certificate(
    pair: dict[str, Any], transition_id: str, forbidden_scope_reference: str
) -> dict[str, Any] | None:
    transition = _source_transition_by_id(pair, transition_id)
    forbidden_scope, forbidden_state = _resolve_source_state(
        pair, forbidden_scope_reference
    )
    if transition is None or forbidden_scope is None or forbidden_state is None:
        return None
    target = transition.get("target")
    if not isinstance(target, str):
        return None
    target_id, target_state = _resolve_source_state(pair, target)
    if target_id is None or target_state is None:
        return None
    states = {
        str(item["id"]): item
        for item in _source_model(pair).get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    target_ancestors: list[str] = []
    cursor: str | None = target_id
    while cursor and cursor in states:
        target_ancestors.append(cursor)
        parent = states[cursor].get("parent")
        cursor = str(parent) if isinstance(parent, str) and parent else None
    enters_forbidden_scope = forbidden_scope in target_ancestors
    source = transition.get("source")
    reachable = False
    state_path: list[str] = []
    transition_path: list[str] = []
    if isinstance(source, str):
        reachable, state_path, transition_path = _source_reachability(
            _source_model(pair), source
        )
    counterexample = reachable and enters_forbidden_scope
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "source_wrong_scope_route",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": "the selected event transition does not target the forbidden scope",
        "observed_transition_id": transition_id,
        "source": source,
        "target": target_id,
        "event": transition.get("event"),
        "forbidden_scope": forbidden_scope,
        "target_ancestor_chain": target_ancestors,
        "source_reachable": reachable,
        "state_path": state_path,
        "transition_path": transition_path,
        "enters_forbidden_scope": enters_forbidden_scope,
        "sound_for_claim": True,
        "prototype_semantics": "exact_source_transition_target_ancestry_fragment",
        "result": counterexample,
        "verdict": "counterexample" if counterexample else "satisfied",
    }


def _source_event_scope_certificate(
    pair: dict[str, Any], goal: EvidenceGoal
) -> dict[str, Any] | None:
    """Prove event-consumer availability from exact source topology.

    A scope obligation is not a lookup for a transition whose source is the
    scope itself.  A composite scope may be active while one of its descendants
    owns the consumer, and a leaf may inherit a transition declared on an
    ancestor.  The source certificate therefore records all structurally
    applicable consumers and evaluates reachability of each source state.  This
    keeps the two distinct failure modes visible: no consumer was authored, or
    consumers exist but every one is unreachable.
    """

    if not goal.observed_transition_id or not goal.source:
        return None
    observed = _source_transition_by_id(pair, goal.observed_transition_id)
    source, source_state = _resolve_source_state(pair, goal.source)
    root_scope = _source_root_scope_id(pair)
    if source is None and goal.source == root_scope:
        source, source_state = root_scope, {"id": root_scope}
    if observed is None or source is None or source_state is None:
        return None
    event = observed.get("event")
    if not isinstance(event, str):
        return None

    model = _source_model(pair)
    states = {
        str(item["id"]): item
        for item in model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    transitions = [
        item
        for item in model.get("transitions", [])
        if isinstance(item, dict)
        and item.get("event") == event
        and item.get("source") in states
    ]

    def ancestors(scope_id: str) -> list[str]:
        result: list[str] = []
        cursor: str | None = scope_id
        while cursor and cursor in states:
            result.append(cursor)
            parent = states[cursor].get("parent")
            cursor = str(parent) if isinstance(parent, str) and parent else None
        return result

    def descendants(scope_id: str) -> set[str]:
        if scope_id == root_scope:
            return set(states)
        result: set[str] = set()
        for state_id in states:
            if state_id == scope_id:
                result.add(state_id)
                continue
            cursor: str | None = state_id
            while cursor and cursor in states:
                parent = states[cursor].get("parent")
                cursor = str(parent) if isinstance(parent, str) and parent else None
                if cursor == scope_id:
                    result.add(state_id)
                    break
        return result

    def reachable_scope(scope_id: str) -> tuple[bool, list[str], list[str]]:
        targets = descendants(scope_id) or {scope_id}
        for target in sorted(targets):
            reachable, state_path, transition_path = _source_reachability(model, target)
            if reachable:
                return True, state_path, transition_path
        return False, [], []

    def consumer_row(transition: dict[str, Any]) -> dict[str, Any]:
        transition_source = str(transition["source"])
        reachable, state_path, transition_path = reachable_scope(transition_source)
        return {
            **_compact_transition_for_d(transition),
            "source_reachable": reachable,
            "state_path": state_path,
            "transition_path": transition_path,
        }

    def scope_result(scope_id: str) -> dict[str, Any]:
        normalized_scope = scope_id
        active_scopes = ancestors(normalized_scope)
        applicable_sources = descendants(normalized_scope) | set(active_scopes)
        rows = [
            consumer_row(transition)
            for transition in transitions
            if transition.get("source") in applicable_sources
        ]
        reachable_rows = [row for row in rows if row.get("source_reachable") is True]
        status = (
            "covered"
            if reachable_rows
            else "consumers_unreachable"
            if rows
            else "missing_consumer"
        )
        scope_reachable, state_path, transition_path = reachable_scope(normalized_scope)
        return {
            "scope": normalized_scope,
            "active_scopes_checked": active_scopes,
            "applicable_source_ids": sorted(applicable_sources),
            "consumers": rows,
            "reachable_consumers": reachable_rows,
            "scope_local_actual": any(
                row.get("source") in set(active_scopes) for row in rows
            ),
            "scope_reachable": scope_reachable,
            "state_path": state_path,
            "transition_path": transition_path,
            "status": status,
            "actual": status == "covered",
        }

    requested_scopes = list(
        dict.fromkeys(
            scope
            for scope in goal.required_scope_ids
            if isinstance(scope, str) and scope
        )
    )
    if source not in requested_scopes:
        requested_scopes.insert(0, source)
    scope_results = [scope_result(scope_id) for scope_id in requested_scopes]
    current_scope_result = next(
        (item for item in scope_results if item["scope"] == source),
        scope_result(source),
    )
    consumers = current_scope_result["consumers"]
    aggregate_consumers = list(
        {
            str(item.get("id")): item
            for result in scope_results
            for item in result["consumers"]
            if isinstance(item, dict) and item.get("id") is not None
        }.values()
    )

    def missing_initial_barriers(source_id: str) -> list[str]:
        barriers: list[str] = []
        for ancestor in ancestors(source_id):
            if ancestor == root_scope:
                # The model root is represented by the synthetic initial
                # vertex, not by a source state.  Keep the causal scope at the
                # nearest authored composite instead of collapsing every root
                # failure into the synthetic machine boundary.
                continue
            direct_children = {
                state_id for state_id, state in states.items()
                if state.get("parent") == ancestor
            }
            initial_edges = [
                transition
                for transition in model.get("transitions", [])
                if isinstance(transition, dict)
                and transition.get("scope") == ancestor
                and transition.get("attributes", {}).get("transition_kind")
                == "initial"
            ]
            if direct_children and not initial_edges:
                barriers.append(ancestor)
        return barriers

    unreachable_consumer_sources = [
        str(item.get("source"))
        for item in aggregate_consumers
        if isinstance(item, dict)
        and item.get("source_reachable") is False
        and isinstance(item.get("source"), str)
    ]
    barrier_sets = [
        set(missing_initial_barriers(source_id))
        for source_id in unreachable_consumer_sources
    ]
    common_barriers = set.intersection(*barrier_sets) if barrier_sets else set()
    blocking_scope = (
        max(common_barriers, key=lambda item: item.count("."))
        if common_barriers
        else None
    )
    missing_scope_ids = [
        str(item["scope"])
        for item in scope_results
        if item.get("scope_local_actual") is not True
    ]
    unreachable_scope_ids = [
        str(item["scope"])
        for item in scope_results
        if item["status"] == "consumers_unreachable"
    ]
    coverage_actual = not missing_scope_ids and not unreachable_scope_ids
    if unreachable_scope_ids:
        kind = (
            "source_event_consumers_unreachable"
            if not missing_scope_ids
            else "source_event_scope_unavailable"
        )
    else:
        kind = "source_event_missing_in_scope"
    source_reachable, state_path, transition_path = reachable_scope(source)
    counterexample = not coverage_actual
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": kind,
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": (
            "every required scope has at least one exact event consumer whose "
            "source scope is reachable in the canonical state graph"
        ),
        "observed_transition_id": goal.observed_transition_id,
        "observed_transition": _compact_transition_for_d(observed),
        "source": source,
        "event": event,
        "scope_applicability": goal.scope_applicability,
        "required_scope_ids": requested_scopes,
        "active_scopes_checked": current_scope_result["active_scopes_checked"],
        "consumers": consumers,
        "consumers_by_scope": scope_results,
        "aggregate_consumers": aggregate_consumers,
        "blocking_scope": blocking_scope,
        "missing_scope_ids": missing_scope_ids,
        "unreachable_scope_ids": unreachable_scope_ids,
        "coverage_actual": coverage_actual,
        "source_reachable": source_reachable,
        "state_path": state_path,
        "transition_path": transition_path,
        "actual": coverage_actual,
        "expected": True,
        "sound_for_claim": True,
        "result": counterexample,
        "verdict": "counterexample" if counterexample else "satisfied",
        "prototype_semantics": "exact_source_event_consumers_and_topology_reachability",
    }


def _source_child_count_certificate(
    pair: dict[str, Any], scope_reference: str, expected_count: int
) -> dict[str, Any] | None:
    scope, scope_state = _resolve_source_state(pair, scope_reference)
    if not scope or not scope_state:
        return None
    direct_children = sorted(
        str(item["id"])
        for item in _source_model(pair).get("states", [])
        if isinstance(item, dict)
        and isinstance(item.get("id"), str)
        and item.get("parent") == scope
    )
    actual_count = len(direct_children)
    actual = actual_count == expected_count
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "source_child_count_contract",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": "direct authored child count equals the grounded expected count",
        "scope": scope,
        "scope_raw_ref": scope_state.get("raw_ref"),
        "direct_children": direct_children,
        "actual_count": actual_count,
        "actual": actual_count,
        "expected": expected_count,
        "sound_for_claim": True,
        "result": not actual,
        "verdict": "counterexample" if not actual else "satisfied",
        "prototype_semantics": "exact_source_direct-child-cardinality_fragment",
    }


def _source_state_presence_certificate(
    pair: dict[str, Any], expected_reference: str
) -> dict[str, Any]:
    expected = _strip_pair_root(expected_reference, pair["pair_name"])
    states = {
        str(item["id"]): item
        for item in _source_model(pair).get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    actual = expected in states
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "source_required_state_presence",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": "the LLM-grounded normative formal state path exists",
        "expected_state": expected,
        "actual_state": states.get(expected),
        "actual": actual,
        "expected": True,
        "sound_for_claim": True,
        "result": not actual,
        "verdict": "counterexample" if not actual else "satisfied",
        "prototype_semantics": "exact_source_state_path_presence_fragment",
        "limitations": [
            "normative_path_identity_is_supplied_by_llm_semantic_grounding"
        ],
    }


def _source_final_pseudostate_presence_certificate(
    pair: dict[str, Any], scope_reference: str
) -> dict[str, Any]:
    scope = _strip_pair_root(scope_reference, pair["pair_name"])
    root_scope = _source_root_scope_id(pair)
    final_target = "@final:__root__" if scope == root_scope else f"@final:{scope}"
    final_edges = [
        _compact_transition_for_d(item)
        for item in _source_model(pair).get("transitions", [])
        if isinstance(item, dict) and item.get("target") == final_target
    ]
    actual = bool(final_edges)
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "source_required_final_pseudostate_presence",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": "the exact source scope declares an outgoing final edge",
        "scope": scope,
        "expected_final_target": final_target,
        "final_edges": final_edges,
        "actual": actual,
        "expected": True,
        "sound_for_claim": True,
        "result": not actual,
        "verdict": "counterexample" if not actual else "satisfied",
        "prototype_semantics": "exact_source_scope_final_pseudostate_fragment",
        "limitations": [
            "normative_final_pseudostate_kind_is_supplied_by_llm_semantic_grounding"
        ],
    }


def _source_certificate_for_seed(
    pair: dict[str, Any], seed: dict[str, Any]
) -> dict[str, Any] | None:
    locations = seed.get("locations")
    target = locations[0] if isinstance(locations, list) and locations else None
    if not isinstance(target, str):
        return None
    code = seed.get("diagnostic_code")
    if code in {"W_DEADLOCK_LEAF", "W_TOPOLOGICAL_NOEXIT"}:
        sequential = _source_deadlock_certificate(pair, target)
        if sequential is not None and sequential.get("verdict") == "counterexample":
            return sequential
        concurrent = _source_concurrent_region_deadlock_certificate(pair, target)
        if concurrent is not None and concurrent.get("verdict") == "counterexample":
            return concurrent
        diagnostic_refs = seed.get("diagnostic_refs")
        diagnostic_refs = diagnostic_refs if isinstance(diagnostic_refs, dict) else {}
        entry_deadlock = _source_entry_deadlock_certificate(
            pair, target, diagnostic_refs.get("parent_path")
        )
        if entry_deadlock is not None:
            return entry_deadlock
        return concurrent or sequential
    if code == "W_UNREACHABLE_STATE":
        return _source_missing_initial_certificate(
            pair, target
        ) or _source_unreachable_certificate(pair, target)
    if code in {
        "W_INITIAL_UNCONDITIONAL_MISSING",
        "W_COMPOSITE_INIT_INCOMPLETE",
    }:
        return _source_initial_contract_certificate(pair, target)
    return None


def _source_certificate_for_group(
    pair: dict[str, Any], group: dict[str, Any]
) -> dict[str, Any] | None:
    seed = group.get("seed")
    if isinstance(seed, dict):
        certificate = _source_certificate_for_seed(pair, seed)
        if certificate is not None:
            return certificate
    checks = group.get("checks", [])
    for check in checks:
        if not isinstance(check, ProbeCheck) or check.role != "primary":
            continue
        if check.kind == "reaches" and check.expected and check.target:
            certificate = _source_missing_initial_certificate(pair, check.target)
            if certificate is not None:
                return certificate
        if check.kind == "terminates" and check.expected and check.source:
            certificate = _source_deadlock_certificate(pair, check.source)
            if certificate is not None:
                return certificate
        if check.kind == "initial_target" and check.expected:
            composite = check.bindings.get("composite")
            child = check.bindings.get("child")
            if isinstance(composite, str) and isinstance(child, str):
                certificate = _source_initial_target_certificate(pair, composite, child)
                if certificate is not None:
                    return certificate
        if check.kind == "containment":
            parent = check.bindings.get("parent")
            child = check.bindings.get("child")
            if isinstance(parent, str) and isinstance(child, str):
                certificate = _source_containment_certificate(
                    pair, child, parent, expected=check.expected
                )
                if certificate is not None:
                    return certificate
        if check.kind == "cardinality" and check.expected:
            scope = check.bindings.get("scope")
            count = check.bindings.get("count")
            if isinstance(scope, str) and isinstance(count, int):
                certificate = _source_child_count_certificate(pair, scope, count)
                if certificate is not None:
                    return certificate
        if check.kind == "state_declared" and check.expected:
            state = check.bindings.get("state")
            if isinstance(state, str):
                return _source_state_presence_certificate(pair, state)
    return None


def _certificate_cause_key(certificate: dict[str, Any]) -> str | None:
    kind = certificate.get("kind")
    requirement_group_id = certificate.get("requirement_group_id")
    if (
        kind == "source_initial_target_contract"
        and isinstance(requirement_group_id, str)
        and requirement_group_id
    ):
        return f"source:initial_requirement_group:{requirement_group_id}"
    if kind == "reachable_deadlock":
        return f"source:reachable_deadlock:{certificate.get('target')}"
    if kind == "concurrent_region_deadlock":
        return f"source:concurrent_region_deadlock:{certificate.get('target')}"
    if kind == "source_entry_deadlock":
        return f"source:entry_deadlock:{certificate.get('scope')}"
    if kind == "missing_initial_with_compiler_consequence":
        return f"source:initial_contract:{certificate.get('scope')}"
    if kind == "unreachable_source_component":
        return f"source:unreachable_component:{certificate.get('component')}"
    if kind == "source_root_target_unreachable":
        # When the exact source root itself has no initial edge, all root-to-target
        # failures are merely consequences of that one structural cause. The
        # count comes from the canonical AST, not from an NL label or heuristic.
        if certificate.get("root_initial_edge_count") == 0:
            return f"source:initial_contract:{certificate.get('source')}"
        return f"source:root_target_unreachable:{certificate.get('target')}"
    if kind == "initial_contract_violation":
        return f"source:initial_contract:{certificate.get('scope')}"
    if kind == "source_initial_target_contract":
        if not certificate.get("initial_edges"):
            return f"source:initial_contract:{certificate.get('composite')}"
        return (
            "source:initial_target:"
            f"{certificate.get('actual_parent')}:{certificate.get('child')}"
        )
    if kind == "source_containment_contract":
        return f"source:containment:{certificate.get('expected_parent')}"
    if kind == "source_child_count_contract":
        return f"source:child_count:{certificate.get('scope')}"
    if kind == "source_required_state_presence":
        return f"source:required_state:{certificate.get('expected_state')}"
    if kind == "source_required_final_pseudostate_presence":
        return f"source:required_final_pseudostate:{certificate.get('scope')}"
    if kind == "source_guard_presence":
        return f"source:guard_presence:{certificate.get('source')}:{certificate.get('target')}"
    if kind == "source_guard_overlap":
        return f"source:guard_overlap:{certificate.get('source')}"
    if kind == "source_guarded_completion_unfireable":
        return (
            "source:guarded_completion_unfireable:"
            f"{certificate.get('observed_transition_id')}"
        )
    if kind == "source_transition_contract":
        return f"source:transition:{certificate.get('source')}:{certificate.get('trigger')}:{certificate.get('target')}"
    if kind == "source_transition_target_inconsistency":
        return (
            "source:transition_target_inconsistency:"
            f"{certificate.get('observed_transition_id')}"
        )
    if kind == "source_extraneous_transition":
        return (
            f"source:extraneous_transition:{certificate.get('observed_transition_id')}"
        )
    if kind == "source_wrong_scope_route":
        return f"source:wrong_scope_route:{certificate.get('observed_transition_id')}"
    if kind in {
        "source_event_consumers_unreachable",
        "source_event_scope_unavailable",
    }:
        consumers = certificate.get("aggregate_consumers")
        consumers = consumers if isinstance(consumers, list) else []
        blocking_scopes = sorted(
            {
                str(item.get("source"))
                for item in consumers
                if isinstance(item, dict) and item.get("source")
            }
        )
        # A shared unreachable source component is the causal identity; the
        # event itself is only a facet of that component.  This lets the six
        # event consumers in one unreachable region form one report issue.
        scope = certificate.get("blocking_scope")
        if not isinstance(scope, str) or not scope:
            scope = blocking_scopes[0] if len(blocking_scopes) == 1 else None
        if scope:
            return f"source:unreachable_event_consumers:{scope}"
        digest = _sha256(
            json.dumps(blocking_scopes, ensure_ascii=False, sort_keys=True)
        )[:12]
        return f"source:unreachable_event_consumers_group:{digest}"
    if kind == "source_event_missing_in_scope":
        required_scopes = certificate.get("required_scope_ids")
        if isinstance(required_scopes, list) and len(required_scopes) > 1:
            scope_digest = _sha256(
                json.dumps(required_scopes, ensure_ascii=False, sort_keys=True)
            )[:12]
            return (
                f"source:event_missing_scope_group:{scope_digest}:"
                f"{certificate.get('observed_transition_id')}"
            )
        return (
            f"source:event_missing_scope:{certificate.get('source')}:"
            f"{certificate.get('observed_transition_id')}"
        )
    if kind == "source_lifecycle_action":
        return (
            f"source:lifecycle_action:{certificate.get('state')}:"
            f"{certificate.get('phase')}:{certificate.get('action')}"
        )
    if kind == "source_unstable_termination_target":
        return f"source:stable_termination:{certificate.get('target')}"
    return None


def build_planner_cause_clusters(
    pair: dict[str, Any], inspect: dict[str, Any], seeds: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Compress repeated inspect consequences before the single LLM call."""

    clusters: dict[str, dict[str, Any]] = {}
    for seed in seeds:
        certificate = _source_certificate_for_seed(pair, seed)
        cause_key = (
            _certificate_cause_key(certificate)
            if isinstance(certificate, dict)
            else None
        )
        if not cause_key:
            locations = seed.get("locations", [])
            first_location = locations[0] if locations else "unknown"
            cause_key = f"inspect:{seed.get('diagnostic_code')}:{first_location}"
        cluster = clusters.setdefault(
            cause_key,
            {
                "cause_key": cause_key,
                "diagnostic_codes": [],
                "hypotheses": [],
                "affected_locations": [],
                "seed_options": [],
                "source_cause_clue": None,
            },
        )
        cluster["diagnostic_codes"].append(seed.get("diagnostic_code"))
        cluster["hypotheses"].append(seed.get("hypothesis"))
        cluster["affected_locations"].extend(seed.get("locations", []))
        cluster["seed_options"].append(
            {
                "seed_id": seed.get("seed_id"),
                "locations": seed.get("locations", []),
                "checks": seed.get("checks", []),
            }
        )
        if isinstance(certificate, dict):
            cluster["source_cause_clue"] = {
                key: certificate.get(key)
                for key in (
                    "kind",
                    "verdict",
                    "sound_for_claim",
                    "scope",
                    "target",
                    "direct_children",
                    "initial_edge_count",
                    "assumptions",
                )
                if certificate.get(key) is not None
            }

    for cluster in clusters.values():
        for field in ("diagnostic_codes", "hypotheses", "affected_locations"):
            cluster[field] = list(dict.fromkeys(cluster[field]))
    return list(clusters.values())


def compact_inspect_for_planner(
    pair: dict[str, Any], report: dict[str, Any], seeds: list[dict[str, Any]]
) -> dict[str, Any]:
    diagnostics = [
        item for item in report.get("diagnostics", []) if isinstance(item, dict)
    ]
    counts: dict[str, int] = {}
    for item in diagnostics:
        code = str(item.get("code") or "UNKNOWN")
        counts[code] = counts.get(code, 0) + 1
    return {
        "status": report.get("status"),
        "metrics": report.get("metrics", {}),
        "diagnostic_counts": counts,
        "cause_clusters": build_planner_cause_clusters(pair, report, seeds),
        "full_diagnostics_location": "run_record.inspect",
    }


_PROGRESSIVE_ORACLE_RULES = {
    "W_INITIAL_UNCONDITIONAL_MISSING": {
        "rule_id": "OR-PYFCSTM-INITIAL-UNCONDITIONAL-MISSING-v1",
        "candidate_norm": (
            "Every entered composite must provide a valid unconditional initial entry."
        ),
        "formal_fact": "pyfcstm reports no unconditional initial entry for the exact composite reference.",
        "applicability": "The referenced composite is behaviorally entered in the modeled system.",
    },
    "W_COMPOSITE_INIT_INCOMPLETE": {
        "rule_id": "OR-PYFCSTM-COMPOSITE-INIT-INCOMPLETE-v1",
        "candidate_norm": (
            "Composite entry must be defined for every admissible initialization."
        ),
        "formal_fact": "pyfcstm reports incomplete initialization for the exact composite reference.",
        "applicability": "The omitted initialization case is admissible under the requirements.",
    },
    "W_UNREACHABLE_STATE": {
        "rule_id": "OR-PYFCSTM-UNREACHABLE-STATE-v1",
        "candidate_norm": (
            "Behavior declared as part of the system must be reachable from root entry."
        ),
        "formal_fact": "pyfcstm reports the exact state reference unreachable from root entry.",
        "applicability": "The requirements intend the referenced state to be executable behavior.",
    },
    "W_DEADLOCK_LEAF": {
        "rule_id": "OR-PYFCSTM-DEADLOCK-LEAF-v1",
        "candidate_norm": (
            "A reachable non-final behavior must admit a continuation or valid termination."
        ),
        "formal_fact": "pyfcstm reports the exact reachable leaf reference as deadlocked.",
        "applicability": "The referenced state is not intended to be terminal behavior.",
    },
    "W_TOPOLOGICAL_NOEXIT": {
        "rule_id": "OR-PYFCSTM-TOPOLOGICAL-NOEXIT-v1",
        "candidate_norm": (
            "A reachable non-final behavior must admit a continuation or valid termination."
        ),
        "formal_fact": "pyfcstm reports no topological exit for the exact state reference.",
        "applicability": "The referenced state is reachable and is not intended to be terminal behavior.",
    },
    "W_TRANSITION_SHADOWED": {
        "rule_id": "OR-PYFCSTM-TRANSITION-SHADOWED-v1",
        "candidate_norm": (
            "Every declared event branch must be selectable under some admissible input."
        ),
        "formal_fact": "pyfcstm reports the exact transition reference as shadowed.",
        "applicability": "The requirements intend the referenced branch to be selectable.",
    },
}


def _diagnostic_location(item: dict[str, Any]) -> str | None:
    refs = item.get("refs")
    refs = refs if isinstance(refs, dict) else {}
    transition = refs.get("transition")
    transition = transition if isinstance(transition, dict) else {}
    return next(
        (
            str(value)
            for value in (
                refs.get("state_path"),
                refs.get("representative_state_path"),
                refs.get("composite_path"),
                refs.get("source_state_path"),
                transition.get("parent"),
            )
            if isinstance(value, str) and value
        ),
        None,
    )


def derive_progressive_evidence_seeds(
    pair: dict[str, Any],
    report: dict[str, Any],
    *,
    normative_quotes: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Mine strong zero-token evidence before any LLM chooses an executable API."""

    seeds: dict[str, dict[str, Any]] = {}
    for item in report.get("diagnostics", []):
        if not isinstance(item, dict):
            continue
        code = str(item.get("code") or "")
        oracle_rule = _PROGRESSIVE_ORACLE_RULES.get(code)
        location = _diagnostic_location(item)
        if not oracle_rule or not location:
            continue
        probe_seed = {
            "diagnostic_code": code,
            "locations": [location],
            "diagnostic_refs": item.get("refs", {}),
        }
        source_certificate = _source_certificate_for_seed(pair, probe_seed)
        cause_key = (
            _certificate_cause_key(source_certificate)
            if isinstance(source_certificate, dict)
            else None
        ) or f"inspect:{code}:{location}"
        seed = seeds.setdefault(
            cause_key,
            {
                "seed_id": f"PX-{len(seeds) + 1:02d}",
                "cause_key": cause_key,
                "origin": "progressive_deterministic_scout",
                "obligation": oracle_rule["candidate_norm"],
                "claim": f"Formal diagnostic {code} is present at exact reference {location}.",
                "basis_kind": "implicit_oracle",
                "formal_fact": oracle_rule["formal_fact"],
                "formal_oracle_rule": {
                    **oracle_rule,
                    "diagnostic_code": code,
                    "rule_source": "preregistered paper1 rule over exact pyfcstm diagnostic semantics",
                    "semantic_decision_claimed": False,
                },
                "locations": [],
                "diagnostics": [],
                "source_causality_certificate": source_certificate,
            },
        )
        seed["locations"].append(location)
        seed["diagnostics"].append(item)
        if (
            seed.get("source_causality_certificate") is None
            and source_certificate is not None
        ):
            seed["source_causality_certificate"] = source_certificate
    for seed in seeds.values():
        seed["locations"] = list(dict.fromkeys(seed["locations"]))
        if normative_quotes:
            certificate = seed.get("source_causality_certificate")
            references = []
            if isinstance(certificate, dict):
                for key in ("target", "target_consequence", "scope", "component"):
                    value = certificate.get(key)
                    if isinstance(value, str) and value:
                        references.append(value)
            quote = next(
                (
                    normative_quotes.get(_strip_pair_root(reference, pair["pair_name"]))
                    for reference in references
                    if _strip_pair_root(reference, pair["pair_name"]) in normative_quotes
                ),
                None,
            )
            if quote:
                # This is a typed concept-to-source binding supplied by the
                # contract/grounding stages, not a lexical search over NL.
                seed["nl_quote"] = quote
    return list(seeds.values())


def build_progressive_normative_quote_bindings(
    pair: dict[str, Any],
    contract_plan: ContractExtractionPlan,
    discovery_plans: list[DiscoveryGroundingPlan] | None = None,
) -> dict[str, str]:
    """Project LLM-selected normative spans onto exact source state IDs.

    Progressive pyfcstm diagnostics are discovered before the evidence planner
    chooses a goal, so they otherwise carry only an implicit oracle rule. This
    bridge preserves an exact NL span when the contract extractor and grounding
    stage already established the same concept-to-source identity. It never
    searches the NL text or guesses from a state name.
    """

    concept_to_source: dict[str, set[str]] = {}
    for plan in discovery_plans or []:
        for binding in plan.concept_bindings:
            concept_to_source.setdefault(binding.concept_id, set()).add(
                _strip_pair_root(binding.source_state_id, pair["pair_name"])
            )
    # Keep typed provenance while choosing the most specific requirement for a
    # source.  An initial-entry diagnostic must receive the initial-entry quote
    # when the same concept also has a generic "is a substate" quote; otherwise
    # D correctly sees a formal fact but no matching normative obligation and
    # drops the evidence to D0.  The priorities are over contract categories,
    # never over NL wording.
    quote_candidates: dict[str, tuple[int, str]] = {}

    def add_quote(concept_id: object, quote: object, priority: int) -> None:
        if not isinstance(concept_id, str) or not concept_id:
            return
        if not isinstance(quote, str) or not quote:
            return
        for source in concept_to_source.get(concept_id, set()):
            existing = quote_candidates.get(source)
            if existing is None or priority > existing[0]:
                quote_candidates[source] = (priority, quote)

    for contract in contract_plan.required_state_contracts:
        add_quote(getattr(contract, "concept_id", None), getattr(contract, "nl_quote", None), 10)
    for contract in contract_plan.required_event_scope_contracts:
        add_quote(getattr(contract, "scope_concept_id", None), getattr(contract, "nl_quote", None), 30)
    for contract in contract_plan.required_action_contracts:
        add_quote(getattr(contract, "owner_concept_id", None), getattr(contract, "nl_quote", None), 40)
    for contract in contract_plan.containment_contracts:
        add_quote(getattr(contract, "child_concept_id", None), getattr(contract, "nl_quote", None), 50)
        add_quote(getattr(contract, "parent_concept_id", None), getattr(contract, "nl_quote", None), 50)
    for contract in contract_plan.transition_groups:
        add_quote(getattr(contract, "source_concept_id", None), getattr(contract, "nl_quote", None), 70)
        for target in getattr(contract, "targets", []) or []:
            add_quote(getattr(target, "target_concept_id", None), getattr(contract, "nl_quote", None), 70)
    for contract in contract_plan.initial_contracts:
        add_quote(getattr(contract, "composite_concept_id", None), getattr(contract, "nl_quote", None), 100)
        add_quote(getattr(contract, "target_concept_id", None), getattr(contract, "nl_quote", None), 100)

    return {source: quote for source, (_, quote) in quote_candidates.items()}


def _compiled_inspect_assertion(seed: dict[str, Any]) -> dict[str, Any]:
    matchers = [
        {
            "code": item.get("code"),
            "refs": item.get("refs", {}),
        }
        for item in seed.get("diagnostics", [])
        if isinstance(item, dict)
    ]
    matcher_json = json.dumps(matchers, ensure_ascii=False, sort_keys=True)
    code = "\n".join(
        [
            "# `model` and `inspect_model` are supplied by the sealed pyfcstm runner.",
            "report = inspect_model(model, enable_verify=True).to_json()",
            f"expected_diagnostics = {matcher_json}",
            'observed = [{"code": d.get("code"), "refs": d.get("refs", {})} for d in report.get("diagnostics", [])]',
            f"assert not all(item in observed for item in expected_diagnostics), {_quoted(EXECUTABLE_ASSERTION_MESSAGE)}",
        ]
    )
    return {
        "schema": "paper1.compiled_evidence_program.v1",
        "backend": "pyfcstm.inspect",
        "assertion_ir": {
            "kind": "diagnostic_absence",
            "expected_diagnostics": matchers,
        },
        "compiled_assertion_code": code,
        "compiled_assertion_sha256": _sha256(code),
        "execution_model": "sealed_pyfcstm_inspect_environment",
    }


def execute_progressive_evidence_seeds(
    pair: dict[str, Any],
    report: dict[str, Any],
    *,
    normative_quotes: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    outcomes = []
    progressive_seeds = derive_progressive_evidence_seeds(
        pair, report, normative_quotes=normative_quotes
    )
    for index, seed in enumerate(progressive_seeds, start=1):
        artifact = _compiled_inspect_assertion(seed)
        source_certificate = seed.get("source_causality_certificate")
        certificate_counterexample = bool(
            isinstance(source_certificate, dict)
            and source_certificate.get("verdict") == "counterexample"
        )
        source_attribution = (
            "causal_dual_certificate" if certificate_counterexample else "unattributed"
        )
        execution_certificate = {
            "schema": "paper1.execution_certificate.v1",
            "evaluated_artifact": pair["paths"]["fcstm"],
            "evaluated_artifact_sha256": _sha256(pair["fcstm"]),
            "compiled_assertion_sha256": artifact["compiled_assertion_sha256"],
            "engine": {
                "adapter": "pyfcstm.inspect",
                "enable_verify": True,
                "max_complexity_tier": "smt_undecidable_heuristic",
            },
            "observations": seed["diagnostics"],
            "terminal": True,
            "precondition_failed": False,
            "counterexample_found": True,
            "verdict": "counterexample",
        }
        group = {
            "group_id": f"progressive:{seed['seed_id']}",
            "origin": seed["origin"],
            "claim": seed["claim"],
            "witness_level": "W2",
            "evaluated_artifact": pair["paths"]["fcstm"],
            "source_attribution": {"status": source_attribution},
            "precondition_failed": False,
            "counterexample_found": True,
            "source_candidate": certificate_counterexample,
            "source_causality_certificate": source_certificate,
            "compiled_assertion": artifact,
            "execution_certificate": execution_certificate,
            "checks": [],
        }
        candidate = {
            "obligation": seed["obligation"],
            "claim": seed["claim"],
            "basis_kind": seed["basis_kind"],
            "formal_fact": seed["formal_fact"],
            "formal_oracle_rule": seed["formal_oracle_rule"],
            "nl_quote": seed.get("nl_quote"),
            "priority": 5,
            "locations": seed["locations"],
            "probe_seed_ids": [],
            "checks": [],
        }
        outcomes.append(
            {
                "candidate_index": f"P{index}",
                "candidate": candidate,
                "planner_envelope_only": False,
                "nl_anchor_valid": True,
                "envelope_witness_level": "W2",
                "has_precondition_failed_group": False,
                "has_counterexample_group": True,
                "has_source_candidate_group": certificate_counterexample,
                "candidate_contract_warning": None,
                "probe_groups": [group],
                "checks": [],
            }
        )
    return [
        _attach_semantic_binding_receipt(
            outcome,
            "formal_pyfcstm_diagnostic",
            compiler_input_plan_sha256=_canonical_sha256(progressive_seeds),
        )
        for outcome in outcomes
    ]


def _source_guarded_completion_certificate(
    pair: dict[str, Any], transition: object
) -> dict[str, Any] | None:
    """Execute the sound guard-only/composite-no-final source fragment."""

    if not isinstance(transition, dict):
        return None
    transition_id = transition.get("id")
    source = transition.get("source")
    attributes = transition.get("attributes")
    attributes = attributes if isinstance(attributes, dict) else {}
    parsed_label = parse_guard_only_label(attributes.get("raw_label"))
    if (
        not isinstance(transition_id, str)
        or not isinstance(source, str)
        or attributes.get("transition_kind") != "normal"
        or parsed_label is None
    ):
        return None

    model = _source_model(pair)
    states = {
        str(item["id"]): item
        for item in model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    source_state = states.get(source)
    if not isinstance(source_state, dict) or source_state.get("kind") != "composite":
        return None
    direct_children = sorted(
        state_id for state_id, state in states.items() if state.get("parent") == source
    )
    if not direct_children:
        return None

    final_target = f"@final:{source}"
    final_edges = [
        _compact_transition_for_d(item)
        for item in model.get("transitions", [])
        if isinstance(item, dict) and item.get("target") == final_target
    ]
    fireable_in_sound_fragment = bool(final_edges)
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "source_guarded_completion_unfireable",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "engine": {
            "adapter": "paper1.uml251_transition_label_profile",
            "profile_id": UML_GUARD_ONLY_PROFILE_ID,
        },
        "assertion": (
            "guard_only_completion(source_transition) implies "
            "exists(final_transition_to(@final:source))"
        ),
        "assertion_executed": True,
        "observed_transition_id": transition_id,
        "source": source,
        "target": transition.get("target"),
        "raw_ref": transition.get("raw_ref"),
        "label_profile": {
            "profile_id": parsed_label.profile_id,
            "explicit_trigger_absent": parsed_label.explicit_trigger is None,
            "guard_present": True,
            "effect_absent": parsed_label.effect is None,
            "implicit_trigger": parsed_label.implicit_trigger,
        },
        "direct_children": direct_children,
        "expected_final_target": final_target,
        "final_edges": final_edges,
        "actual": fireable_in_sound_fragment,
        "expected": True,
        "result": not fireable_in_sound_fragment,
        "verdict": (
            "counterexample" if not fireable_in_sound_fragment else "satisfied"
        ),
        "sound_for_claim": True,
        "prototype_semantics": (
            "uml251_derived_guard_only_label_and_composite_without_final_edge"
        ),
        "limitations": [
            "guard_body_is_opaque_and_not_semantically_interpreted",
            "profile_is_declared_by_paper1_not_enforced_by_plantuml",
            "presence_of_a_final_edge_is_not_a_general_reachability_proof",
        ],
    }


def derive_source_static_evidence_plan(pair: dict[str, Any]) -> EvidencePlan:
    """Create candidates only for violations decidable on the formal source AST."""

    states = {
        str(item["id"]): item
        for item in _source_model(pair).get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    candidates = []
    for transition in _source_model(pair).get("transitions", []):
        if not isinstance(transition, dict):
            continue
        attributes = transition.get("attributes")
        attributes = attributes if isinstance(attributes, dict) else {}
        scope = transition.get("scope")
        target = transition.get("target")
        if (
            attributes.get("transition_kind") != "initial"
            or not isinstance(scope, str)
            or not isinstance(target, str)
        ):
            continue
        target_state = states.get(target)
        if target_state is not None and target_state.get("parent") == scope:
            continue
        raw_ref = transition.get("raw_ref")
        locations = [
            str(item)
            for item in (raw_ref, scope, target)
            if isinstance(item, str) and item
        ]
        candidates.append(
            EvidenceCandidate(
                obligation=(
                    "An initial pseudostate transition must target a vertex in "
                    "the same composite region."
                ),
                claim=(
                    f"Initial transition {transition.get('id')} in {scope} targets "
                    f"{target}, which is outside that region."
                ),
                basis_kind="domain_norm",
                priority=5,
                locations=locations[:3],
                proposed_l="L1",
                goal=EvidenceGoal(
                    relation="initial_target",
                    subject=scope,
                    target=target,
                ),
            )
        )
    for transition in _source_model(pair).get("transitions", []):
        certificate = _source_guarded_completion_certificate(pair, transition)
        if certificate is None or certificate.get("verdict") != "counterexample":
            continue
        transition_id = str(transition["id"])
        source = str(transition["source"])
        raw_ref = transition.get("raw_ref")
        candidates.append(
            EvidenceCandidate(
                obligation=(
                    "Under the declared UML-derived label profile, a guard-only "
                    "transition from a composite state is a completion transition "
                    "and requires a reachable composite completion."
                ),
                claim=(
                    f"Transition {transition_id} is a guarded completion transition "
                    f"from {source}, but that composite has no final-state exit."
                ),
                basis_kind="domain_norm",
                priority=5,
                locations=[
                    str(item)
                    for item in (raw_ref, transition_id, source)
                    if isinstance(item, str) and item
                ][:3],
                proposed_l="L0",
                goal=EvidenceGoal(
                    relation="completion_transition_fireable",
                    observed_transition_id=transition_id,
                    source=source,
                ),
            )
        )
    return EvidencePlan(candidates=candidates)


def execute_source_static_evidence_scouts(
    pair: dict[str, Any], inspect: dict[str, Any]
) -> list[dict[str, Any]]:
    """Execute formal source-AST violations against the exact FCSTM artifact."""

    return execute_evidence_plan(
        pair,
        inspect,
        derive_source_static_evidence_plan(pair),
        binding_authority="formal_source_ast",
    )


def retain_unupgraded_broad_candidates(
    pair: dict[str, Any], broad_plan: BroadDiscoveryPlan, evidence_plan: ProbePlan
) -> list[dict[str, Any]]:
    upgraded = {
        candidate_id
        for candidate in evidence_plan.candidates
        for candidate_id in candidate.broad_candidate_ids
    }
    outcomes = []
    for index, candidate in enumerate(broad_plan.candidates, start=1):
        if candidate.candidate_id in upgraded:
            continue
        witness_level = "W1" if candidate.locations else "W0"
        group = {
            "group_id": f"broad:{candidate.candidate_id}",
            "origin": "broad_source_discovery",
            "claim": candidate.claim,
            "witness_level": witness_level,
            "evaluated_artifact": None,
            "source_attribution": {"status": "source_localized"},
            "precondition_failed": False,
            "counterexample_found": False,
            "source_candidate": False,
            "source_causality_certificate": None,
            "compiled_assertion": None,
            "execution_certificate": None,
            "checks": [],
        }
        outcomes.append(
            {
                "candidate_index": f"B{index}",
                "candidate": candidate.model_dump(mode="json"),
                "planner_envelope_only": True,
                "nl_anchor_valid": _nl_anchor_valid(pair, candidate),
                "envelope_witness_level": witness_level,
                "has_precondition_failed_group": False,
                "has_counterexample_group": False,
                "has_source_candidate_group": False,
                "candidate_contract_warning": None,
                "probe_groups": [group],
                "checks": [],
            }
        )
    return outcomes


def _probe_groups(
    candidate: ProbeCandidate, seeds: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[str]]:
    seed_by_id = {str(seed.get("seed_id")): seed for seed in seeds}
    groups: list[dict[str, Any]] = []
    unknown: list[str] = []
    for seed_id in candidate.probe_seed_ids:
        seed = seed_by_id.get(seed_id)
        if not seed:
            unknown.append(seed_id)
            continue
        groups.append(
            {
                "group_id": f"seed:{seed_id}",
                "origin": "inspect_seed",
                "claim": str(seed.get("hypothesis") or candidate.claim),
                "seed": seed,
                "checks": [
                    ProbeCheck.model_validate(check) for check in seed.get("checks", [])
                ],
            }
        )
    if candidate.checks:
        groups.append(
            {
                "group_id": "custom",
                "origin": "planner_custom",
                "claim": candidate.claim,
                "seed": None,
                "checks": list(candidate.checks),
            }
        )
    return groups, unknown


def execute_plan(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    plan: ProbePlan,
    seeds: list[dict[str, Any]] | None = None,
    *,
    binding_authority: SemanticBindingAuthority = "formal_source_ast",
    semantic_provenance: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    seeds = derive_probe_seeds(inspect) if seeds is None else seeds
    exclusions = pair["source_trace"].get("attribution_exclusions", [])
    exclusions = (
        [str(item) for item in exclusions] if isinstance(exclusions, list) else []
    )
    environment = build_eval_environment(
        model_text=pair["fcstm"],
        model_path=pair["paths"]["fcstm"],
        inspect=inspect,
        source_mappings=pair["source_trace"].get("entries", []),
        source_exclusions=exclusions,
        formal_verification_enabled=True,
        fbmcq_solver_timeout_ms=5_000,
        fbmcq_max_bound=8,
        fbmcq_process_wall_seconds=30,
    )
    outcomes: list[dict[str, Any]] = []
    for candidate_index, candidate in enumerate(plan.candidates, start=1):
        groups, unknown_seed_ids = _probe_groups(candidate, seeds)
        group_outcomes: list[dict[str, Any]] = []
        if unknown_seed_ids:
            group_outcomes.append(
                {
                    "group_id": "unknown_seed",
                    "origin": "inspect_seed",
                    "claim": candidate.claim,
                    "witness_level": "W1",
                    "source_attribution": {"status": "unattributed"},
                    "precondition_failed": False,
                    "counterexample_found": False,
                    "source_candidate": False,
                    "source_causality_certificate": None,
                    "compiled_assertion": None,
                    "execution_certificate": None,
                    "checks": [
                        {
                            "check_index": 0,
                            "expression": None,
                            "result": "unsupported",
                            "error": f"unknown probe seed id(s): {unknown_seed_ids}",
                        }
                    ],
                }
            )
        for group in groups:
            checks: list[dict[str, Any]] = []
            terminal = True
            precondition_failed = False
            primary_contradicted = False
            attribution_statuses: list[str] = []
            primary_function_families: set[str] = set()
            expanded = group["checks"]
            for check_index, check in enumerate(expanded, start=1):
                normalized, normalizations = normalize_check(check, inspect, pair)
                expression, compile_error = compile_check(normalized)
                if compile_error:
                    terminal = False
                    checks.append(
                        {
                            "check_index": check_index,
                            "probe": check.model_dump(mode="json"),
                            "normalized_probe": normalized.model_dump(mode="json"),
                            "normalizations": normalizations,
                            "expression": None,
                            "result": "unsupported",
                            "error": compile_error,
                        }
                    )
                    continue
                result = environment.eval_assert(
                    expression, EXECUTABLE_ASSERTION_MESSAGE
                )
                result_payload = _jsonable(result)
                attribution_status = classify_attribution(result_payload, exclusions)
                attribution_statuses.append(attribution_status)
                if normalized.role == "primary":
                    primary_function_families.update(
                        str(family)
                        for family in result_payload.get("actual_function_families", [])
                        if isinstance(family, str)
                    )
                checks.append(
                    {
                        "check_index": check_index,
                        "probe": check.model_dump(mode="json"),
                        "normalized_probe": normalized.model_dump(mode="json"),
                        "normalizations": normalizations,
                        "expression": expression,
                        "execution": result_payload,
                        "attribution_status": attribution_status,
                    }
                )
                if result.result not in {"true", "false"}:
                    terminal = False
                if result.result == "false":
                    if normalized.role == "precondition":
                        precondition_failed = True
                    else:
                        primary_contradicted = True

            counterexample_found = (
                terminal and not precondition_failed and primary_contradicted
            )
            compiled_assertion = build_assertion_artifact(checks)
            execution_certificate = build_execution_certificate(
                pair,
                compiled_assertion,
                checks,
                terminal=terminal,
                precondition_failed=precondition_failed,
                counterexample_found=counterexample_found,
            )
            source_certificate = None
            if counterexample_found:
                source_certificate = _source_certificate_for_group(pair, group)
            certificate_counterexample = bool(
                source_certificate
                and source_certificate.get("verdict") == "counterexample"
            )
            if certificate_counterexample:
                source_attribution = "causal_dual_certificate"
            elif "representation_debt" in attribution_statuses:
                source_attribution = "representation_debt"
            elif (
                "unattributed" in attribution_statuses
                or not attribution_statuses
                or not primary_function_families.intersection({"simulation", "formal"})
            ):
                source_attribution = "unattributed"
            else:
                source_attribution = "safe_runtime_path"
            witness_level = (
                "W2" if terminal and expanded else "W1" if expanded else "W0"
            )
            source_candidate = (
                counterexample_found
                and witness_level == "W2"
                and certificate_counterexample
            ) or (
                counterexample_found
                and witness_level == "W2"
                and source_attribution == "safe_runtime_path"
            )
            group_outcomes.append(
                {
                    "group_id": group["group_id"],
                    "origin": group["origin"],
                    "claim": group["claim"],
                    "witness_level": witness_level,
                    "evaluated_artifact": pair["paths"]["fcstm"],
                    "source_attribution": {"status": source_attribution},
                    "precondition_failed": precondition_failed,
                    "counterexample_found": counterexample_found,
                    "source_candidate": source_candidate,
                    "source_causality_certificate": source_certificate,
                    "compiled_assertion": compiled_assertion,
                    "execution_certificate": execution_certificate,
                    "checks": checks,
                }
            )
        quote_valid = _nl_anchor_valid(pair, candidate)
        localized = bool(candidate.locations or groups or candidate.probe_seed_ids)
        envelope_witness_level = (
            "W2"
            if any(item["witness_level"] == "W2" for item in group_outcomes)
            else "W1"
            if localized
            else "W0"
        )
        outcomes.append(
            {
                "candidate_index": candidate_index,
                "candidate": candidate.model_dump(mode="json"),
                "planner_envelope_only": True,
                "nl_anchor_valid": quote_valid,
                "envelope_witness_level": envelope_witness_level,
                "has_precondition_failed_group": any(
                    item["precondition_failed"] for item in group_outcomes
                ),
                "has_counterexample_group": any(
                    item["counterexample_found"] for item in group_outcomes
                ),
                "has_source_candidate_group": quote_valid
                and any(item["source_candidate"] for item in group_outcomes),
                "candidate_contract_warning": (
                    "seed_and_custom_checks_were_executed_as_separate_groups"
                    if candidate.probe_seed_ids and candidate.checks
                    else None
                ),
                "probe_groups": group_outcomes,
                "checks": [
                    {**check, "group_id": group["group_id"]}
                    for group in group_outcomes
                    for check in group["checks"]
                ],
            }
        )
    plan_hash = _canonical_sha256(plan)
    return [
        _attach_semantic_binding_receipt(
            outcome,
            binding_authority,
            semantic_provenance=semantic_provenance,
            compiler_input_plan_sha256=plan_hash,
        )
        for outcome in outcomes
    ]


def _resolve_candidate_path(
    pair: dict[str, Any], reference: str, candidates: list[str]
) -> str | None:
    """Resolve an exact FCSTM ID or its declared source-ID namespace mapping."""

    if reference in candidates:
        return reference
    source_ids = {
        str(item["id"])
        for item in _source_model(pair).get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    mapped = f"{pair['pair_name']}.{reference}"
    return mapped if reference in source_ids and mapped in candidates else None


def _resolve_topology_reference(
    pair: dict[str, Any], reference: str, candidates: list[str]
) -> tuple[str | None, dict[str, Any]]:
    """Resolve a typed source reference to an exact topology node or closure.

    ``TopologyIndex`` is leaf-oriented, while NL contracts may intentionally
    name a composite scope. The canonical source AST is the only authority for
    expanding that scope: exact ``parent`` links select descendants and the
    FCSTM namespace prefix is applied only after the source ID has been
    resolved. No prose or identifier substring is interpreted here.
    """

    direct = _resolve_candidate_path(pair, reference, candidates)
    if direct is not None:
        return direct, {"reference": reference, "mode": "direct", "nodes": [direct]}

    source_model = _source_model(pair)
    source_states = [
        item
        for item in source_model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    normalized = _strip_pair_root(reference, pair["pair_name"])
    exact_source = next(
        (item for item in source_states if item.get("id") == normalized), None
    )
    if exact_source is None:
        return None, {"reference": reference, "mode": "unresolved", "nodes": []}

    source_id = str(exact_source["id"])
    source_to_full = {
        str(item.get("id")): f"{pair['pair_name']}.{item['id']}"
        for item in source_states
    }
    candidate_set = set(candidates)
    parent_by_id = {
        str(item["id"]): item.get("parent")
        for item in source_states
    }
    scope_cursor: str | None = source_id
    scope_ancestors: set[str] = set()
    while scope_cursor is not None and scope_cursor not in scope_ancestors:
        scope_ancestors.add(scope_cursor)
        scope_parent = parent_by_id.get(scope_cursor)
        scope_cursor = (
            str(scope_parent)
            if isinstance(scope_parent, str) and scope_parent
            else None
        )
    if scope_cursor is not None:
        return None, {
            "reference": reference,
            "mode": "parent_cycle",
            "source_id": source_id,
            "cyclic_descendants": sorted(scope_ancestors),
            "nodes": [],
        }
    descendants: list[str] = []
    cyclic_descendants: set[str] = set()
    for item in source_states:
        item_id = str(item["id"])
        cursor: str | None = item_id
        visited: set[str] = set()
        while cursor is not None and cursor not in visited:
            if cursor == source_id:
                descendants.append(item_id)
                break
            visited.add(cursor)
            parent = parent_by_id.get(cursor)
            cursor = str(parent) if isinstance(parent, str) and parent else None
        if cursor is not None and cursor in visited:
            cyclic_descendants.add(item_id)
    expanded = [
        source_to_full[item]
        for item in descendants
        if item not in cyclic_descendants and source_to_full.get(item) in candidate_set
    ]
    if not expanded:
        if cyclic_descendants:
            return None, {
                "reference": reference,
                "mode": "parent_cycle",
                "source_id": source_id,
                "cyclic_descendants": sorted(cyclic_descendants),
                "nodes": [],
            }
        return None, {
            "reference": reference,
            "mode": "composite_without_topology_descendant",
            "source_id": source_id,
            "nodes": [],
        }
    return expanded[0], {
        "reference": reference,
        "mode": "source_descendant_closure",
        "source_id": source_id,
        "nodes": expanded,
    }


def _source_transition_rows(
    pair: dict[str, Any], *, source: str, target: str | None = None
) -> list[dict[str, Any]]:
    normalized_source = _strip_pair_root(source, pair["pair_name"])
    normalized_target = (
        _strip_pair_root(target, pair["pair_name"]) if target is not None else None
    )
    rows = []
    for transition in _source_model(pair).get("transitions", []):
        if not isinstance(transition, dict):
            continue
        actual_source = transition.get("source")
        actual_target = transition.get("target")
        if not isinstance(actual_source, str) or actual_source != normalized_source:
            continue
        if normalized_target is not None and actual_target != normalized_target:
            continue
        rows.append(transition)
    return rows


def _source_transition_label(transition: dict[str, Any]) -> str | None:
    """Return the complete authored label used for semantic condition binding."""

    attributes = transition.get("attributes")
    if not isinstance(attributes, dict):
        attributes = {}
    raw_label = attributes.get("raw_label")
    if isinstance(raw_label, str) and raw_label.strip():
        return raw_label.strip()
    label = transition.get("label")
    return label.strip() if isinstance(label, str) and label.strip() else None


def _source_transition_condition_matches(
    pair: dict[str, Any], transition: dict[str, Any], binding: str | None
) -> bool:
    """Check an LLM-selected condition against exact source fields.

    This is deliberately an identity check over the canonical transition AST,
    not a lexical interpretation of a natural-language claim. A condition is
    accepted only when the binding is the authored event/label or its declared
    projected event identity.
    """

    if not isinstance(binding, str) or not binding.strip():
        return False
    candidate = binding.strip()
    event = transition.get("event")
    if isinstance(event, str) and candidate == event.strip():
        return True
    raw_label = _source_transition_label(transition)
    if raw_label is not None and candidate == raw_label:
        return True
    # A bracketed PlantUML guard is parsed by the formal label grammar.  The
    # comparison below is over the parser's guard field, not a substring or
    # keyword rule, so ordinary event/action labels cannot enter this branch.
    parsed_guard = parse_guard_only_label(raw_label)
    if parsed_guard is not None and parsed_guard.guard == candidate:
        return True
    if raw_label is not None:
        projected, _ = _projected_event(pair, raw_label)
        if isinstance(projected, str) and candidate == projected:
            return True
    return False


def _source_transition_guard_matches(
    transition: dict[str, Any], binding: str | None
) -> bool:
    """Match only an exact formal guard AST, never an event/raw label."""

    if not isinstance(binding, str) or not binding.strip():
        return False
    candidate = binding.strip()
    guard = transition.get("guard")
    if isinstance(guard, str) and guard.strip() == candidate:
        return True
    parsed_guard = parse_guard_only_label(_source_transition_label(transition))
    return parsed_guard is not None and parsed_guard.guard == candidate


def _canonical_formal_condition_binding(
    pair: dict[str, Any], binding: str | None
) -> bool:
    """Return whether a binding is an exact formal event/guard in the source AST.

    This is an AST inventory check, not a natural-language heuristic.  It lets
    the compiler execute a negative guard obligation when the requested formal
    guard is authored elsewhere but absent from the endpoint edge.  A prose
    condition that has no exact event, raw label, or parsed guard in the source
    model remains non-terminal and therefore cannot receive W2.
    """

    if not isinstance(binding, str) or not binding.strip():
        return False
    candidate = binding.strip()
    for transition in _source_model(pair).get("transitions", []):
        if not isinstance(transition, dict):
            continue
        for field in ("event", "guard"):
            value = transition.get(field)
            if isinstance(value, str) and value.strip() == candidate:
                return True
        raw_label = _source_transition_label(transition)
        if raw_label is not None and raw_label == candidate:
            return True
        parsed_guard = parse_guard_only_label(raw_label)
        if parsed_guard is not None and parsed_guard.guard == candidate:
            return True
    return False


def _apply_formal_transition_binding(
    pair: dict[str, Any], candidate: EvidenceCandidate
) -> tuple[EvidenceCandidate, list[dict[str, str]]]:
    goal = candidate.goal
    bindings: list[dict[str, str]] = []
    if not goal.observed_transition_id:
        return candidate, bindings
    transition = _source_transition_by_id(pair, goal.observed_transition_id)
    if transition is None:
        return candidate, bindings
    updates: dict[str, Any] = {}
    if goal.relation == "transition_target_consistency":
        reference = (
            _source_transition_by_id(pair, goal.reference_transition_id)
            if goal.reference_transition_id
            else None
        )
        for role, row in (("observed", transition), ("reference", reference)):
            if not isinstance(row, dict):
                continue
            for field in ("source", "target", "event", "guard"):
                value = row.get(field)
                if isinstance(value, str):
                    bindings.append(
                        {
                            "field": f"{role}_{field}",
                            "value": value,
                            "basis": ("llm_selected_transition_id_then_exact_ast_read"),
                        }
                    )
    elif goal.relation in {"transition_contract", "transition_exists"}:
        for field in ("source", "target", "event", "guard"):
            value = transition.get(field)
            if isinstance(value, str):
                bindings.append(
                    {
                        "field": f"observed_{field}",
                        "value": value,
                        "basis": "llm_selected_observed_transition_then_exact_ast_read",
                    }
                )
        # ``condition`` is an NL-facing normative rendering and may contain
        # Markdown or prose.  Once grounding has selected an exact authored
        # transition, the only sound executable condition identity is the
        # canonical event/raw label read from that transition.  This is a
        # structured AST lookup, never a textual normalization or semantic
        # guess, and it preserves the original ``condition`` for audit.
    elif goal.relation == "transition_absent":
        updates.update(
            {
                "source": transition.get("source"),
                "target": transition.get("target"),
                "trigger": transition.get("event"),
                "expected": False,
            }
        )
    elif goal.relation == "event_reaches_target":
        updates["source"] = transition.get("source")
        # The target is normative. An observed endpoint must never fill an
        # unresolved NL-to-formal target binding.
        updates["target"] = goal.target
        source_event = transition.get("event")
        updates["trigger"] = (
            _projected_event(pair, source_event)[0]
            if isinstance(source_event, str)
            else source_event
        )
    elif goal.relation == "event_avoids_scope":
        updates["source"] = transition.get("source")
        updates["target"] = transition.get("target")
        source_event = transition.get("event")
        updates["trigger"] = (
            _projected_event(pair, source_event)[0]
            if isinstance(source_event, str)
            else source_event
        )
        updates["expected"] = True
    elif goal.relation in {"event_consumed", "effect_exists"}:
        updates["source"] = transition.get("source")
        source_event = transition.get("event")
        updates["trigger"] = (
            _projected_event(pair, source_event)[0]
            if isinstance(source_event, str)
            else source_event
        )
    elif goal.relation == "event_consumed_in_scope":
        source_event = transition.get("event")
        updates["trigger"] = (
            _projected_event(pair, source_event)[0]
            if isinstance(source_event, str)
            else source_event
        )
    elif goal.relation == "guard_present":
        updates.update(
            {
                "source": transition.get("source"),
                "target": transition.get("target"),
            }
        )
    for field, value in updates.items():
        if isinstance(value, str) and getattr(goal, field) != value:
            bindings.append(
                {
                    "field": field,
                    "value": value,
                    "basis": (
                        "llm_selected_transition_id_then_declared_event_mapping"
                        if field == "trigger"
                        else "llm_selected_observed_transition_then_exact_ast_read"
                    ),
                }
            )
    goal = goal.model_copy(update=updates)
    return candidate.model_copy(update={"goal": goal}), bindings


def _source_static_certificate(
    pair: dict[str, Any], goal: EvidenceGoal, *, actual: bool, evidence: Any
) -> dict[str, Any]:
    return {
        "schema": "paper1.source_assertion.v1",
        "kind": (
            "source_guard_overlap"
            if goal.relation == "guards_distinguishable"
            else "source_guard_presence"
        ),
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": f"{goal.relation} == {goal.expected}",
        "source": goal.source,
        "target": goal.target,
        "evidence": evidence,
        "actual": actual,
        "expected": goal.expected,
        "sound_for_claim": True,
        "result": actual != goal.expected,
        "verdict": "counterexample" if actual != goal.expected else "satisfied",
        "prototype_semantics": (
            "quantifier_free_boolean_linear_real_fragment"
            if goal.relation == "guards_distinguishable"
            else "exact_guard_ast_or_declared_guard_only_label_profile"
        ),
    }


def _source_action_certificate(
    pair: dict[str, Any],
    goal: EvidenceGoal,
    *,
    actual: bool,
    evidence: Any,
    sound_for_claim: bool,
    projection_receipts: list[dict[str, Any]],
) -> dict[str, Any]:
    """Certify an exact lifecycle action from the canonical source inventory.

    The action identity is supplied by semantic grounding and compared as a
    structured field. This function never searches NL or interprets action prose.
    """

    return {
        "schema": "paper1.source_assertion.v1",
        "kind": "source_lifecycle_action",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": "exact_lifecycle_action(state, phase, action) == expected",
        "state": goal.subject,
        "phase": goal.phase,
        "action": goal.action,
        "evidence": evidence,
        "actual": actual,
        "expected": goal.expected,
        "fcstm_projection_audit": projection_receipts,
        "sound_for_claim": sound_for_claim,
        "result": sound_for_claim and actual != goal.expected,
        "verdict": (
            "counterexample"
            if sound_for_claim and actual != goal.expected
            else "satisfied"
            if sound_for_claim
            else "inconclusive"
        ),
        "prototype_semantics": "exact_canonical_lifecycle_action_inventory",
    }


def _working_contract_action_projection_receipts(
    pair: dict[str, Any], goal: EvidenceGoal
) -> list[dict[str, Any]]:
    """Resolve source action text through explicit working-contract macro links."""

    state = _strip_pair_root(str(goal.subject), pair["pair_name"])
    source_rows = []
    elements = [
        item
        for item in pair["working_contract"].get("elements", [])
        if isinstance(item, dict)
    ]
    for element in elements:
        metadata = element.get("metadata")
        metadata = metadata if isinstance(metadata, dict) else {}
        if not (
            element.get("kind") == "lifecycle_action"
            and metadata.get("state_id") == state
            and (
                goal.phase is None
                or metadata.get("lifecycle_kind") == goal.phase
            )
            and metadata.get("text") == goal.action
        ):
            continue
        source_rows.append(element)

    receipts = []
    for source_row in source_rows:
        macro_ids = {
            str(item)
            for item in source_row.get("macro_ids", [])
            if isinstance(item, str)
        }
        projection_rows = []
        projected_names: set[str] = set()
        for element in elements:
            element_macros = {
                str(item)
                for item in element.get("macro_ids", [])
                if isinstance(item, str)
            }
            if (
                element.get("kind") != "abstract_lifecycle_projection"
                or not macro_ids.intersection(element_macros)
            ):
                continue
            model_refs = [
                str(item)
                for item in element.get("model_refs", [])
                if isinstance(item, str)
            ]
            names = [
                item.removeprefix("action:")
                for item in model_refs
                if item.startswith("action:") and item.removeprefix("action:")
            ]
            projected_names.update(names)
            projection_rows.append(
                {
                    "element_id": element.get("element_id"),
                    "macro_ids": sorted(element_macros),
                    "model_refs": model_refs,
                    "projected_action_names": names,
                }
            )
        receipts.append(
            {
                "source_element_id": source_row.get("element_id"),
                "source_refs": source_row.get("source_refs", []),
                "macro_ids": sorted(macro_ids),
                "source_action": goal.action,
                "projection_rows": projection_rows,
                "projected_action_names": sorted(projected_names),
                "complete": bool(macro_ids)
                and len(projected_names) == 1
                and bool(projection_rows),
            }
        )
    return receipts


def _execute_action_effect_goal(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    candidate: EvidenceCandidate,
    route: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    """Execute exact action identity and delegate effects to the sealed predicate API."""

    goal = candidate.goal
    if goal.relation == "effect_exists":
        if goal.sign == "changed":
            return _single_group_outcome(
                pair,
                candidate,
                index=index,
                route=route,
                witness_level="W1",
                counterexample_found=False,
                source_attribution=(
                    "source_localized" if candidate.locations else "unattributed"
                ),
                compiled_assertion=None,
                execution_certificate=None,
                source_certificate=None,
                error=(
                    "effect_exists sign='changed' requires a registered runtime "
                    "operator; positive/negative delta evidence remains supported"
                ),
            )
        legacy_candidate = ProbeCandidate(
            obligation=candidate.obligation,
            claim=candidate.claim,
            basis_kind=candidate.basis_kind,
            nl_quote=candidate.nl_quote,
            priority=candidate.priority,
            locations=candidate.locations,
            checks=route["checks"],
        )
        outcome = execute_plan(
            pair,
            inspect,
            ProbePlan(candidates=[legacy_candidate]),
            [],
            binding_authority="formal_source_ast",
        )[0]
        outcome["candidate_index"] = index
        outcome["candidate"] = candidate.model_dump(mode="json")
        for group in outcome.get("probe_groups", []):
            group["compiler_route"] = _jsonable(route)
            group["evidence_goal"] = goal.model_dump(mode="json")
        return outcome

    state_paths = {
        str(row.get("path"))
        for row in inspect.get("states", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    state = _resolve_candidate_path(pair, str(goal.subject), sorted(state_paths))
    phase = {"entry": "enter", "exit": "exit", "during": "during"}.get(
        goal.phase or ""
    )
    projection_receipts = _working_contract_action_projection_receipts(pair, goal)
    complete_projected_names = {
        str(name)
        for receipt in projection_receipts
        if receipt.get("complete") is True
        for name in receipt.get("projected_action_names", [])
        if isinstance(name, str)
    }
    accepted_action_names = {
        str(goal.action),
        *complete_projected_names,
    }
    action_rows = [
        row
        for row in inspect.get("actions", [])
        if isinstance(row, dict)
        and row.get("state_path") == state
        and (phase is None or row.get("stage") == phase)
        and row.get("name") in accepted_action_names
    ]
    actual = bool(action_rows)
    source_state = _strip_pair_root(str(goal.subject), pair["pair_name"])
    source_rows = [
        row
        for row in _source_model(pair).get("states", [])
        if isinstance(row, dict) and row.get("id") == source_state
    ]
    source_actions: list[dict[str, Any]] = []
    source_phase = {"entry": "entry", "exit": "exit", "during": "during"}.get(
        goal.phase or ""
    )
    if len(source_rows) == 1:
        for row in source_rows[0].get("attributes", {}).get("lifecycle_actions", []):
            if not isinstance(row, dict) or (
                source_phase is not None and row.get("kind") != source_phase
            ):
                continue
            if goal.action in {None, ""} or row.get("text") == goal.action:
                source_actions.append(row)
    direct_artifact_identity = any(
        isinstance(row, dict)
        and row.get("state_path") == state
        and (phase is None or row.get("stage") == phase)
        and row.get("name") == goal.action
        for row in inspect.get("actions", [])
    )
    mapping_ambiguous = bool(source_actions) and not (
        direct_artifact_identity
        or (
            len(projection_receipts) == 1
            and projection_receipts[0].get("complete") is True
        )
    )
    terminal = bool(
        state is not None
        and goal.action not in {None, ""}
        and not mapping_ambiguous
    )
    source_sound = bool(len(source_rows) == 1 and goal.action not in {None, ""})
    source_certificate = _source_action_certificate(
        pair,
        goal,
        actual=bool(source_actions),
        evidence=source_actions,
        sound_for_claim=source_sound,
        projection_receipts=projection_receipts,
    )
    counterexample = terminal and actual != goal.expected
    code = (
        "assert exact_action_declared(state, optional_phase, action) is "
        f"{goal.expected}, {EXECUTABLE_ASSERTION_MESSAGE!r}"
    )
    program = {
        "schema": "paper1.compiled_evidence_program.v1",
        "backend": route["backend"],
        "assertion_ir": goal.model_dump(mode="json"),
        "compiled_assertion_code": code,
        "compiled_assertion_sha256": _sha256(code),
        "execution_model": "sealed_pyfcstm_inspect_action_inventory",
    }
    receipt = {
        "schema": "paper1.execution_certificate.v1",
        "evaluated_artifact": pair["paths"]["fcstm"],
        "evaluated_artifact_sha256": _sha256(pair["fcstm"]),
        "compiled_assertion_sha256": program["compiled_assertion_sha256"],
        "engine": {"adapter": "pyfcstm.inspect", "operation": "exact_action_declared"},
        "observations": {
            "resolved_state": state,
            "phase": phase,
            "action": goal.action,
            "accepted_action_names": sorted(accepted_action_names),
            "working_contract_projection_receipts": projection_receipts,
            "matching_action_rows": action_rows,
            "actual": actual,
            "expected": goal.expected,
            "mapping_ambiguous": mapping_ambiguous,
        },
        "terminal": terminal,
        "precondition_failed": not terminal,
        "counterexample_found": counterexample,
        "verdict": (
            "counterexample"
            if counterexample
            else "satisfied"
            if terminal
            else "inconclusive"
        ),
    }
    return _single_group_outcome(
        pair,
        candidate,
        index=index,
        route=route,
        witness_level="W2" if receipt["terminal"] else "W1",
        counterexample_found=counterexample,
        source_attribution=(
            "causal_dual_certificate"
            if counterexample and source_certificate["result"]
            else "unattributed"
        ),
        compiled_assertion=program,
        execution_certificate=receipt,
        source_certificate=source_certificate,
    )


def _single_group_outcome(
    pair: dict[str, Any],
    candidate: EvidenceCandidate,
    *,
    index: int,
    route: dict[str, Any],
    witness_level: str,
    counterexample_found: bool,
    source_attribution: str,
    compiled_assertion: dict[str, Any] | None,
    execution_certificate: dict[str, Any] | None,
    source_certificate: dict[str, Any] | None,
    error: str | None = None,
) -> dict[str, Any]:
    quote_valid = _nl_anchor_valid(pair, candidate)
    source_candidate = bool(
        quote_valid
        and counterexample_found
        and witness_level == "W2"
        and source_attribution
        in {"causal_dual_certificate", "source_direct_certificate"}
    )
    group = {
        "group_id": "compiled_goal",
        "origin": "method_owned_evidence_compiler",
        "claim": candidate.claim,
        "witness_level": witness_level,
        "evaluated_artifact": (
            execution_certificate.get("evaluated_artifact")
            if isinstance(execution_certificate, dict)
            else None
        ),
        "source_attribution": {"status": source_attribution},
        "precondition_failed": False,
        "counterexample_found": counterexample_found,
        "source_candidate": source_candidate,
        "source_causality_certificate": source_certificate,
        "compiled_assertion": compiled_assertion,
        "execution_certificate": execution_certificate,
        "compiler_route": route,
        "support_disposition": route.get("support_disposition"),
        "domain_obligation": (
            candidate.domain_obligation.model_dump(mode="json")
            if candidate.domain_obligation is not None
            else None
        ),
        "evidence_goal": candidate.goal.model_dump(mode="json"),
        "checks": [],
        "error": error,
    }
    return {
        "candidate_index": index,
        "candidate": candidate.model_dump(mode="json"),
        "planner_envelope_only": False,
        "nl_anchor_valid": quote_valid,
        "envelope_witness_level": witness_level,
        "has_precondition_failed_group": False,
        "has_counterexample_group": counterexample_found,
        "has_source_candidate_group": source_candidate,
        "candidate_contract_warning": error,
        "probe_groups": [group],
        "checks": [],
    }


def _fcstm_event_display_names(pair: dict[str, Any]) -> dict[str, str]:
    names: dict[str, str] = {}
    pattern = re.compile(
        r'^\s*event\s+([A-Za-z_][A-Za-z0-9_]*)\s+named\s+("(?:\\.|[^"\\])*")\s*;',
        re.MULTILINE,
    )
    for identifier, quoted in pattern.findall(pair["fcstm"]):
        display = json.loads(quoted)
        names[identifier] = display
        names[f"{pair['pair_name']}.{identifier}"] = display
    return names


def _guard_overlap_proof(conditions: list[str]) -> dict[str, Any]:
    if len(conditions) < 2:
        return {
            "conditions": conditions,
            "pairs": [],
            "overlap_found": False,
            "all_terminal": True,
        }
    return pairwise_overlaps(conditions)


def _execute_completion_transition_goal(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    candidate: EvidenceCandidate,
    route: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    """Run the source profile assertion and audit the exact FCSTM projection."""

    transition_id = candidate.goal.observed_transition_id
    transition = (
        _source_transition_by_id(pair, transition_id)
        if isinstance(transition_id, str)
        else None
    )
    certificate = _source_guarded_completion_certificate(pair, transition)
    if certificate is None:
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level="W1",
            counterexample_found=False,
            source_attribution="source_localized",
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error="transition is outside the declared guard-only source fragment",
        )

    attributes = transition.get("attributes") if isinstance(transition, dict) else {}
    attributes = attributes if isinstance(attributes, dict) else {}
    raw_label = attributes.get("raw_label")
    projected_event = None
    if isinstance(raw_label, str):
        projected_event, _ = _projected_event(pair, raw_label)
    event_rows = [
        row
        for row in inspect.get("events", [])
        if isinstance(row, dict)
        and isinstance(projected_event, str)
        and row.get("qualified_name") == projected_event
    ]
    projection_declared = any(row.get("is_declared") is True for row in event_rows)
    projection_used = any(
        row.get("is_used") is True and bool(row.get("used_by")) for row in event_rows
    )
    source = str(transition.get("source"))
    target = str(transition.get("target"))
    mapping_receipts = _mapped_transition_receipts(
        pair,
        source=source,
        target=target,
        observed_transition_id=str(transition_id),
    )
    representation_divergence = projection_declared and projection_used
    certificate["fcstm_projection_audit"] = {
        "evaluated_artifact": pair["paths"]["fcstm"],
        "evaluated_artifact_sha256": _sha256(pair["fcstm"]),
        "inspect_adapter": "pyfcstm.inspect",
        "projected_event": projected_event,
        "projection_declared": projection_declared,
        "projection_used": projection_used,
        "event_rows": event_rows,
        "mapping_receipts": mapping_receipts,
        "representation_divergence": representation_divergence,
    }
    program = {
        "schema": "paper1.compiled_evidence_program.v1",
        "backend": "source_ast_plus_fcstm_projection_audit",
        "assertion_ir": candidate.goal.model_dump(mode="json"),
        "compiled_assertion_code": (
            "profile = parse_guard_only_label(source_transition.raw_label)\n"
            "source_result = evaluate_composite_completion(source_ast, profile)\n"
            "projection = inspect_exact_event_projection(fcstm, source_transition.id)\n"
            f"assert source_result.fireable is True, {EXECUTABLE_ASSERTION_MESSAGE!r}"
        ),
        "execution_model": "sealed_source_profile_and_fcstm_inspect_environment",
    }
    program["compiled_assertion_sha256"] = _sha256(program["compiled_assertion_code"])
    certificate["compiled_assertion_sha256"] = program["compiled_assertion_sha256"]
    counterexample = certificate.get("verdict") == "counterexample"
    return _single_group_outcome(
        pair,
        candidate,
        index=index,
        route=route,
        witness_level="W1",
        counterexample_found=counterexample,
        source_attribution=(
            "representation_debt" if representation_divergence else "source_localized"
        ),
        compiled_assertion=program,
        execution_certificate=None,
        source_certificate=certificate,
    )


def _execute_source_guard_goal(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    candidate: EvidenceCandidate,
    route: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    goal = candidate.goal
    state_paths = [
        str(row.get("path"))
        for row in inspect.get("states", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    ]
    source = _resolve_candidate_path(pair, str(goal.source), state_paths)
    all_artifact_rows = [
        row
        for row in inspect.get("transitions", [])
        if isinstance(row, dict) and row.get("from_path") == source
    ]
    source_rows = _source_transition_rows(pair, source=str(goal.source))
    obligation = candidate.domain_obligation
    transition_refs = (
        set(obligation.transition_refs)
        if isinstance(obligation, GuardSetObligation)
        else set()
    )
    guard_bindings = (
        {
            binding.transition_id: binding
            for binding in obligation.guard_bindings
        }
        if isinstance(obligation, GuardSetObligation)
        else {}
    )
    profiled_source_rows: list[tuple[dict[str, Any], GuardOnlyLabel, str]] = []
    binding_errors: list[str] = []
    for row in source_rows:
        if transition_refs and row.get("id") not in transition_refs:
            continue
        attributes = row.get("attributes")
        attributes = attributes if isinstance(attributes, dict) else {}
        raw_label = attributes.get("raw_label")
        binding = guard_bindings.get(row.get("id"))
        if isinstance(obligation, GuardSetObligation):
            if binding is None:
                binding_errors.append(
                    f"missing semantic guard binding for exact transition {row.get('id')!r}"
                )
            elif not isinstance(raw_label, str) or binding.source_label != raw_label:
                binding_errors.append(
                    f"semantic guard binding does not equal authored raw label for "
                    f"transition {row.get('id')!r}"
                )
        profile = parse_guard_only_label(raw_label)
        # A semantic role declaration is not itself a formal guard. If the
        # source label is outside the registered guard-only grammar, there is
        # no sound condition AST to execute and this transition remains
        # unprofiled (the candidate degrades to W1).
        if profile is None or not isinstance(raw_label, str):
            continue
        projected_event, _ = _projected_event(pair, raw_label)
        profiled_source_rows.append((row, profile, projected_event))
    if binding_errors:
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level="W1",
            counterexample_found=False,
            source_attribution="source_localized",
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error="; ".join(binding_errors),
        )
    artifact_rows: list[dict[str, Any]] = []
    artifact_ambiguity = False
    for source_row, _, projected_event in profiled_source_rows:
        source_path = _resolve_candidate_path(
            pair,
            str(source_row.get("source")),
            [
                str(item.get("path"))
                for item in inspect.get("states", [])
                if isinstance(item, dict) and isinstance(item.get("path"), str)
            ],
        )
        target_path = _resolve_candidate_path(
            pair,
            str(source_row.get("target")),
            [
                str(item.get("path"))
                for item in inspect.get("states", [])
                if isinstance(item, dict) and isinstance(item.get("path"), str)
            ],
        )
        matches = [
            row
            for row in all_artifact_rows
            if row.get("from_path") == source_path
            and row.get("to_path") == target_path
            and row.get("event") == projected_event
        ]
        if len(matches) != 1:
            artifact_ambiguity = True
        artifact_rows.extend(matches)
    display_names = _fcstm_event_display_names(pair)
    artifact_conditions = [
        str(row.get("guard"))
        if row.get("guard")
        else display_names.get(str(row.get("event")), "true")
        for row in artifact_rows
    ]
    source_conditions = [profile.guard for _, profile, _ in profiled_source_rows]
    if isinstance(obligation, GuardSetObligation) and set(guard_bindings) != transition_refs:
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level="W1",
            counterexample_found=False,
            source_attribution="source_localized",
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error=(
                "guard overlap requires explicit semantic guard bindings for all "
                "selected exact transitions"
            ),
        )
    if artifact_ambiguity or len(source_conditions) < 2 or len(artifact_conditions) < 2:
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level="W1",
            counterexample_found=False,
            source_attribution="source_localized",
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error=(
                "guard-only transition mapping is ambiguous or fewer than two "
                "exact guard-only transitions share the declared implicit "
                "completion trigger"
            ),
        )
    try:
        proof = _guard_overlap_proof(artifact_conditions)
        source_proof = _guard_overlap_proof(source_conditions)
    except UnsupportedGuard as exc:
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level="W1",
            counterexample_found=False,
            source_attribution="source_localized",
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error=f"guard fragment unsupported: {exc}",
        )
    actual = not proof["overlap_found"]
    source_actual = not source_proof["overlap_found"]
    counterexample = proof["all_terminal"] and actual != goal.expected
    program = {
        "schema": "paper1.compiled_evidence_program.v1",
        "backend": route["backend"],
        "assertion_ir": goal.model_dump(mode="json"),
        "compiled_assertion_code": (
            "proof = pairwise_overlaps(source_conditions)\n"
            f"assert (not proof['overlap_found']) is {goal.expected}, "
            f"{EXECUTABLE_ASSERTION_MESSAGE!r}"
        ),
        "execution_model": "sealed_fcstm_event_label_smt_environment",
    }
    program["compiled_assertion_sha256"] = _sha256(program["compiled_assertion_code"])
    source_certificate = _source_static_certificate(
        pair, goal, actual=source_actual, evidence=source_proof
    )
    source_certificate["guard_binding_audit"] = (
        [
            {
                "transition_id": binding.transition_id,
                "source_label": binding.source_label,
                "semantic_role": binding.semantic_role,
            }
            for binding in obligation.guard_bindings
        ]
        if isinstance(obligation, GuardSetObligation)
        else []
    )
    source_certificate["sound_for_claim"] = bool(
        isinstance(obligation, GuardSetObligation)
        and set(guard_bindings) == transition_refs
    )
    receipt = {
        "schema": "paper1.execution_certificate.v1",
        "evaluated_artifact": pair["paths"]["fcstm"],
        "evaluated_artifact_sha256": _sha256(pair["fcstm"]),
        "compiled_assertion_sha256": program["compiled_assertion_sha256"],
        "engine": {"adapter": "paper1.fcstm_event_guard_solver", "timeout_ms": 3_000},
        "observations": {
            **proof,
            "source": source,
            "transition_rows": artifact_rows,
            "projected_conditions": artifact_conditions,
            "source_transition_ids": [
                row.get("id") for row, _, _ in profiled_source_rows
            ],
            "guard_binding_audit": source_certificate["guard_binding_audit"],
            "decision_group": {
                "source": goal.source,
                "trigger": "implicit_completion",
            },
        },
        "terminal": proof["all_terminal"],
        "precondition_failed": False,
        "counterexample_found": counterexample,
        "verdict": "counterexample" if counterexample else "satisfied",
    }
    return _single_group_outcome(
        pair,
        candidate,
        index=index,
        route=route,
        witness_level="W2" if proof["all_terminal"] else "W1",
        counterexample_found=counterexample,
        source_attribution=(
            "causal_dual_certificate"
            if (
                counterexample
                and source_certificate.get("sound_for_claim") is True
                and source_certificate.get("verdict") == "counterexample"
            )
            else "unattributed"
        ),
        compiled_assertion=program,
        execution_certificate=receipt,
        source_certificate=source_certificate,
    )


def _fcstm_scope_final_edges(
    pair: dict[str, Any], scope_reference: str
) -> list[dict[str, Any]] | None:
    """Read scope-local final edges from the public FCSTM grammar AST."""

    from pyfcstm.dsl import parse_with_grammar_entry
    from pyfcstm.dsl.node import EXIT_STATE

    ast = parse_with_grammar_entry(pair["fcstm"], "state_machine_dsl")
    root = ast.root_state
    scope = _strip_pair_root(scope_reference, pair["pair_name"])
    root_scope = _source_root_scope_id(pair)
    selected = root if scope == root_scope else None

    def visit(node: Any, parent: str | None) -> None:
        nonlocal selected
        name = getattr(node, "name", None)
        if not isinstance(name, str):
            return
        path = name if parent is None else f"{parent}.{name}"
        relative = _strip_pair_root(path, pair["pair_name"])
        if relative == scope:
            selected = node
        for child in getattr(node, "substates", []):
            visit(child, path)

    visit(root, None)
    if selected is None:
        return None
    rows = []
    for transition in getattr(selected, "transitions", []):
        if getattr(transition, "to_state", None) is not EXIT_STATE:
            continue
        span = getattr(transition, "_span", None)
        event_id = getattr(transition, "event_id", None)
        rows.append(
            {
                "from_state": str(getattr(transition, "from_state", "")),
                "to_state": "[*]",
                "event_id": str(event_id) if event_id is not None else None,
                "line": getattr(span, "line", None),
            }
        )
    return rows


def _execute_final_pseudostate_presence_goal(
    pair: dict[str, Any],
    candidate: EvidenceCandidate,
    route: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    """Execute the same scope-local final-edge assertion on source and FCSTM ASTs."""

    goal = candidate.goal
    scope = str(goal.source)
    artifact_edges = _fcstm_scope_final_edges(pair, scope)
    if artifact_edges is None:
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level="W1",
            counterexample_found=False,
            source_attribution="source_localized",
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error="formal FCSTM scope is unavailable",
        )
    artifact_actual = bool(artifact_edges)
    artifact_counterexample = artifact_actual != goal.expected
    source_certificate = _source_final_pseudostate_presence_certificate(pair, scope)
    source_counterexample = source_certificate["verdict"] == "counterexample"
    code = (
        "edges = final_edges_in_exact_scope(fcstm_ast, goal.source)\n"
        f"assert bool(edges) is {goal.expected}, {EXECUTABLE_ASSERTION_MESSAGE!r}"
    )
    program = {
        "schema": "paper1.compiled_evidence_program.v1",
        "backend": route["backend"],
        "assertion_ir": goal.model_dump(mode="json"),
        "compiled_assertion_code": code,
        "compiled_assertion_sha256": _sha256(code),
        "execution_model": "sealed_public_fcstm_grammar_ast_environment",
    }
    receipt = {
        "schema": "paper1.execution_certificate.v1",
        "evaluated_artifact": pair["paths"]["fcstm"],
        "evaluated_artifact_sha256": _sha256(pair["fcstm"]),
        "compiled_assertion_sha256": program["compiled_assertion_sha256"],
        "engine": {
            "adapter": "pyfcstm.dsl.parse_with_grammar_entry",
            "grammar_entry": "state_machine_dsl",
        },
        "observations": {
            "scope": scope,
            "scope_local_final_edges": artifact_edges,
            "actual": artifact_actual,
            "expected": goal.expected,
        },
        "terminal": True,
        "precondition_failed": False,
        "counterexample_found": artifact_counterexample,
        "verdict": "counterexample" if artifact_counterexample else "satisfied",
    }
    representation_divergence = source_counterexample != artifact_counterexample
    return _single_group_outcome(
        pair,
        candidate,
        index=index,
        route=route,
        witness_level=(
            "W2" if artifact_counterexample else "W1" if source_counterexample else "W2"
        ),
        counterexample_found=source_counterexample or artifact_counterexample,
        source_attribution=(
            "representation_debt"
            if representation_divergence
            else "causal_dual_certificate"
            if source_counterexample and artifact_counterexample
            else "unattributed"
        ),
        compiled_assertion=program,
        execution_certificate=receipt,
        source_certificate=source_certificate,
    )


def _projected_event(pair: dict[str, Any], trigger: str) -> tuple[str, str]:
    for element in pair["working_contract"].get("elements", []):
        if (
            not isinstance(element, dict)
            or element.get("kind") != "opaque_event_projection"
        ):
            continue
        fields = element.get("semantic_fields")
        fields = fields if isinstance(fields, dict) else {}
        raw_label = fields.get("raw_label")
        identifier = fields.get("fcstm_identifier")
        if trigger in {raw_label, identifier} and isinstance(identifier, str):
            return identifier, str(raw_label or trigger)
    return trigger, trigger


def _same_model_reference(pair: dict[str, Any], left: Any, right: Any) -> bool:
    if not isinstance(left, str) or not isinstance(right, str):
        return False
    left = _strip_pair_root(left, pair["pair_name"])
    right = _strip_pair_root(right, pair["pair_name"])
    return left == right


def _mapped_transition_receipts(
    pair: dict[str, Any],
    *,
    source: str,
    target: str,
    observed_transition_id: str | None = None,
) -> list[dict[str, Any]]:
    elements = [
        item
        for item in pair["working_contract"].get("elements", [])
        if isinstance(item, dict)
    ]
    fcstm_lines = {line.strip() for line in pair["fcstm"].splitlines()}
    receipts = []
    for root in elements:
        if root.get("kind") != "transition_macro_root":
            continue
        fields = root.get("semantic_fields")
        fields = fields if isinstance(fields, dict) else {}
        if not (
            _same_model_reference(pair, fields.get("source_endpoint"), source)
            and _same_model_reference(pair, fields.get("target_endpoint"), target)
        ):
            continue
        metadata = root.get("metadata")
        metadata = metadata if isinstance(metadata, dict) else {}
        transition_id = metadata.get("transition_id")
        if (
            observed_transition_id is not None
            and transition_id != observed_transition_id
        ):
            continue
        segments = []
        for item in elements:
            item_metadata = item.get("metadata")
            item_metadata = item_metadata if isinstance(item_metadata, dict) else {}
            if (
                item.get("kind") == "transition_segment"
                and item_metadata.get("source_transition_id") == transition_id
            ):
                line = item_metadata.get("line")
                segments.append(
                    {
                        "element_id": item.get("element_id"),
                        "role": item_metadata.get("generated_role"),
                        "line": line,
                        "present_in_fcstm": isinstance(line, str)
                        and line.strip() in fcstm_lines,
                    }
                )
        receipts.append(
            {
                "element_id": root.get("element_id"),
                "transition_id": transition_id,
                "mapping_reason": metadata.get("mapping_reason"),
                "raw_label": fields.get("raw_label"),
                "segments": segments,
                "complete": bool(segments)
                and all(item["present_in_fcstm"] for item in segments),
            }
        )
    return receipts


def _execute_transition_contract_goal(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    candidate: EvidenceCandidate,
    route: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    goal = candidate.goal
    state_paths = [
        str(row.get("path"))
        for row in inspect.get("states", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    ]
    source = _resolve_candidate_path(pair, str(goal.source), state_paths)
    target = _resolve_candidate_path(pair, str(goal.target), state_paths)
    artifact_rows = [
        row
        for row in inspect.get("transitions", [])
        if isinstance(row, dict)
        and row.get("from_path") == source
        and row.get("to_path") == target
    ]
    mapping_receipts = _mapped_transition_receipts(
        pair,
        source=str(goal.source),
        target=str(goal.target),
        observed_transition_id=goal.observed_transition_id,
    )
    mapped_relation_present = any(item["complete"] for item in mapping_receipts)
    direct_relation_present = bool(artifact_rows)
    artifact_relation_present = direct_relation_present or mapped_relation_present
    # Keep the normative NL qualifier separate from the exact formal identity
    # supplied by semantic grounding. A prose event description must not be
    # mistaken for a missing formal guard, while a qualified condition without
    # an exact binding must remain inconclusive rather than become a W2 defect.
    formal_condition = goal.trigger
    condition_role = goal.condition_role or (
        "event" if goal.condition is None and formal_condition else "unknown"
    )
    condition = (
        None
        if goal.relation == "transition_absent"
        else goal.condition if goal.condition is not None else formal_condition
    )
    bound_transition = (
        _source_transition_by_id(pair, goal.observed_transition_id)
        if goal.observed_transition_id
        else None
    )
    bound_event = (
        bound_transition.get("event") if isinstance(bound_transition, dict) else None
    )
    projected_event = (
        _projected_event(pair, bound_event)[0] if isinstance(bound_event, str) else None
    )
    # A prose condition is not a formal guard AST. It can support a terminal
    # missing-edge counterexample, but an existing edge is W2 only when the
    # semantic grounding also supplied an exact formal trigger binding. The
    # compiler never treats an arbitrary non-empty label as proof that the
    # requested condition is realized.
    source_condition_binding = isinstance(bound_transition, dict) and (
        _source_transition_guard_matches(bound_transition, formal_condition)
        if condition_role == "qualified_guard"
        else _source_transition_condition_matches(pair, bound_transition, formal_condition)
    )
    endpoint_source_rows = _source_transition_rows(
        pair, source=str(goal.source), target=str(goal.target)
    )
    direct_condition_present = bool(formal_condition) and source_condition_binding and any(
        (
            not goal.observed_transition_id
            or row.get("id") == goal.observed_transition_id
        )
        and isinstance(projected_event, str)
        and _same_model_reference(pair, row.get("event"), projected_event)
        and (
            condition_role != "qualified_guard"
            or _source_transition_guard_matches(bound_transition or {}, formal_condition)
        )
        for row in artifact_rows
    )
    mapped_condition_present = bool(formal_condition) and any(
        item["complete"]
        and any(
            (
                _source_transition_guard_matches(row, formal_condition)
                if condition_role == "qualified_guard"
                else _source_transition_condition_matches(pair, row, formal_condition)
            )
            for row in endpoint_source_rows
        )
        for item in mapping_receipts
        if (
            not goal.observed_transition_id
            or item.get("transition_id") == goal.observed_transition_id
        )
    )
    artifact_condition_present = direct_condition_present or mapped_condition_present
    source_rows = (
        [
            row
            for row in endpoint_source_rows
            if row.get("id") == goal.observed_transition_id
        ]
        if goal.observed_transition_id
        else endpoint_source_rows
    )
    source_relation_present = bool(source_rows)
    source_condition_present = bool(formal_condition) and any(
        (
            _source_transition_guard_matches(row, formal_condition)
            if condition_role == "qualified_guard"
            else _source_transition_condition_matches(pair, row, formal_condition)
        )
        for row in source_rows
    )
    formal_condition_binding = (
        any(
            _source_transition_guard_matches(row, formal_condition)
            for row in _source_model(pair).get("transitions", [])
            if isinstance(row, dict)
        )
        if condition_role == "qualified_guard"
        else _canonical_formal_condition_binding(pair, formal_condition)
    )
    actual = artifact_relation_present and (
        artifact_condition_present if condition else True
    )
    source_actual = source_relation_present and (
        source_condition_present if condition else True
    )
    condition_binding_terminal = (
        not condition
        or source_condition_present
        or formal_condition_binding
        or (not endpoint_source_rows and not artifact_relation_present)
    )
    terminal = source is not None and target is not None and condition_binding_terminal
    source_reference, _ = _resolve_source_state(pair, str(goal.source))
    target_reference, _ = _resolve_source_state(pair, str(goal.target))
    source_sound = (
        source_reference is not None
        and target_reference is not None
        and (
            not condition
            or source_condition_present
            or formal_condition_binding
            or not endpoint_source_rows
        )
    )
    counterexample = terminal and actual != goal.expected
    source_counterexample = source_sound and source_actual != goal.expected
    certificate_kind = (
        "source_extraneous_transition"
        if goal.relation == "transition_absent" or goal.expected is False
        else "source_transition_contract"
    )
    source_certificate = {
        "schema": "paper1.source_assertion.v1",
        "kind": certificate_kind,
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": (
            "the semantically forbidden authored transition is absent"
            if goal.relation == "transition_absent" or goal.expected is False
            else "source-target transition exists and has a condition slot"
            if condition
            else "source-target transition exists"
        ),
        "source": goal.source,
        "target": goal.target,
        "trigger": formal_condition or goal.condition,
        "normative_condition": goal.condition,
        "condition_role": condition_role,
        "observed_transition_id": goal.observed_transition_id,
        "observed_transition": bound_transition,
        "matching_transitions": source_rows,
        "relation_present": source_relation_present,
        "condition_present": source_condition_present,
        "formal_condition_binding": formal_condition_binding,
        "actual": source_actual,
        "expected": goal.expected,
        "sound_for_claim": source_sound,
        "result": source_counterexample,
        "verdict": (
            "counterexample"
            if source_counterexample
            else "satisfied"
            if source_sound
            else "inconclusive"
        ),
        "prototype_semantics": (
            "llm_selected_transition_id_then_exact_formal_mapping_execution"
        ),
        "semantic_binding_authority": "paper1_discovery_grounding_llm",
        "limitations": [
            (
                "Formal execution is conditional on the recorded LLM semantic "
                "binding; the compiler validates formal IDs but does not "
                "reinterpret NL."
            )
        ],
    }
    code = (
        "result = inspect_transition_contract(source, target, observed_transition_id)\n"
        f"assert result.relation_and_condition is {goal.expected}, "
        f"{EXECUTABLE_ASSERTION_MESSAGE!r}"
    )
    program = {
        "schema": "paper1.compiled_evidence_program.v1",
        "backend": route["backend"],
        "assertion_ir": {
            "normative": {
                key: value
                for key, value in goal.model_dump(mode="json").items()
                if key != "observed_transition_id"
            },
            "observed": {
                "transition_id": goal.observed_transition_id,
                "source": (
                    bound_transition.get("source")
                    if isinstance(bound_transition, dict)
                    else None
                ),
                "target": (
                    bound_transition.get("target")
                    if isinstance(bound_transition, dict)
                    else None
                ),
                "event": (
                    bound_transition.get("event")
                    if isinstance(bound_transition, dict)
                    else None
                ),
            },
        },
        "compiled_assertion_code": code,
        "compiled_assertion_sha256": _sha256(code),
        "execution_model": "sealed_pyfcstm_inspect_environment",
    }
    receipt = {
        "schema": "paper1.execution_certificate.v1",
        "evaluated_artifact": pair["paths"]["fcstm"],
        "evaluated_artifact_sha256": _sha256(pair["fcstm"]),
        "compiled_assertion_sha256": program["compiled_assertion_sha256"],
        "engine": {"adapter": "pyfcstm.inspect"},
        "observations": {
            "source": source,
            "target": target,
            "condition": condition,
            "formal_condition": formal_condition,
            "condition_role": condition_role,
            "observed_transition_id": goal.observed_transition_id,
            "observed_source": (
                bound_transition.get("source")
                if isinstance(bound_transition, dict)
                else None
            ),
            "observed_target": (
                bound_transition.get("target")
                if isinstance(bound_transition, dict)
                else None
            ),
            "projected_event": projected_event,
            "direct_transition_rows": artifact_rows,
            "mapping_macro_receipts": mapping_receipts,
            "relation_present": artifact_relation_present,
            "condition_present": artifact_condition_present,
            "condition_binding_terminal": condition_binding_terminal,
            "formal_condition_binding": formal_condition_binding,
        },
        "terminal": terminal,
        "precondition_failed": False,
        "counterexample_found": counterexample,
        "verdict": (
            "counterexample"
            if counterexample
            else "satisfied"
            if terminal
            else "inconclusive"
        ),
        "limitations": [
            (
                "Condition identity comes from the recorded LLM semantic binding, "
                "not from deterministic text matching."
            )
        ],
    }
    dual = terminal and counterexample and source_counterexample
    return _single_group_outcome(
        pair,
        candidate,
        index=index,
        route=route,
        witness_level="W2" if terminal else "W1",
        counterexample_found=counterexample,
        source_attribution=(
            "causal_dual_certificate"
            if dual
            else "source_localized"
            if source_reference is not None or target_reference is not None
            else "unattributed"
        ),
        compiled_assertion=program,
        execution_certificate=receipt,
        source_certificate=source_certificate,
    )


def _execute_transition_target_consistency_goal(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    candidate: EvidenceCandidate,
    route: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    """Execute an LLM-grounded same-role target comparison on exact IDs."""

    goal = candidate.goal
    observed = (
        _source_transition_by_id(pair, goal.observed_transition_id)
        if goal.observed_transition_id
        else None
    )
    reference = (
        _source_transition_by_id(pair, goal.reference_transition_id)
        if goal.reference_transition_id
        else None
    )
    state_paths = [
        str(row.get("path"))
        for row in inspect.get("states", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    ]

    def projection(
        transition: dict[str, Any] | None, target: str | None
    ) -> dict[str, Any]:
        if not isinstance(transition, dict) or not isinstance(target, str):
            return {"direct_rows": [], "mapping_receipts": [], "present": False}
        source = transition.get("source")
        if not isinstance(source, str):
            return {"direct_rows": [], "mapping_receipts": [], "present": False}
        source_path = _resolve_candidate_path(pair, source, state_paths)
        target_path = _resolve_candidate_path(pair, target, state_paths)
        direct_rows = [
            row
            for row in inspect.get("transitions", [])
            if isinstance(row, dict)
            and row.get("from_path") == source_path
            and row.get("to_path") == target_path
        ]
        receipts = _mapped_transition_receipts(
            pair,
            source=source,
            target=target,
            observed_transition_id=str(transition.get("id")),
        )
        return {
            "source_path": source_path,
            "target_path": target_path,
            "direct_rows": direct_rows,
            "mapping_receipts": receipts,
            "present": bool(direct_rows) or any(row["complete"] for row in receipts),
        }

    normative_target = goal.target
    observed_actual_target = (
        observed.get("target") if isinstance(observed, dict) else None
    )
    reference_actual_target = (
        reference.get("target") if isinstance(reference, dict) else None
    )
    observed_actual_projection = projection(observed, observed_actual_target)
    observed_normative_projection = projection(observed, normative_target)
    reference_normative_projection = projection(reference, normative_target)
    reference_supports_normative_target = bool(
        isinstance(reference, dict)
        and reference_actual_target == normative_target
        and reference_normative_projection["present"]
    )
    target_reference, _ = _resolve_source_state(pair, str(normative_target))
    terminal = bool(
        isinstance(observed, dict)
        and isinstance(reference, dict)
        and target_reference is not None
        and observed_actual_projection["present"]
        and reference_supports_normative_target
    )
    artifact_actual = bool(observed_normative_projection["present"])
    counterexample = bool(terminal and artifact_actual != goal.expected)
    source_sound = bool(
        isinstance(observed, dict)
        and isinstance(reference, dict)
        and target_reference is not None
        and reference_actual_target == normative_target
    )
    source_actual = bool(
        isinstance(observed, dict) and observed_actual_target == normative_target
    )
    source_counterexample = bool(source_sound and source_actual != goal.expected)
    source_certificate = {
        "schema": "paper1.source_assertion.v1",
        "kind": "source_transition_target_inconsistency",
        "evaluated_artifact": pair["paths"]["canonical"],
        "evaluated_artifact_sha256": _sha256(
            json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
        ),
        "assertion": (
            "given the recorded LLM same-role judgment, the observed and "
            "reference transitions realize the normative target"
        ),
        "observed_transition_id": goal.observed_transition_id,
        "reference_transition_id": goal.reference_transition_id,
        "observed_transition": observed,
        "reference_transition": reference,
        "normative_target": normative_target,
        "target": normative_target,
        "observed_target": observed_actual_target,
        "reference_target": reference_actual_target,
        "reference_supports_normative_target": reference_actual_target
        == normative_target,
        "actual": source_actual,
        "expected": goal.expected,
        "sound_for_claim": source_sound,
        "result": source_counterexample,
        "verdict": (
            "counterexample"
            if source_counterexample
            else "satisfied"
            if source_sound
            else "inconclusive"
        ),
        "prototype_semantics": (
            "llm_same_role_judgment_then_exact_transition_endpoint_comparison"
        ),
        "semantic_binding_authority": "paper1_discovery_grounding_llm",
        "limitations": [
            (
                "The LLM establishes same-role semantics; deterministic code "
                "does not compare transition labels, guards, or identifier text."
            )
        ],
    }
    code = (
        "reference = inspect_mapped_transition(reference_transition_id)\n"
        "observed = inspect_mapped_transition(observed_transition_id)\n"
        "assert reference.target == normative_target, 'reference precondition failed'\n"
        f"assert (observed.target == normative_target) is {goal.expected}, "
        f"{EXECUTABLE_ASSERTION_MESSAGE!r}"
    )
    program = {
        "schema": "paper1.compiled_evidence_program.v1",
        "backend": route["backend"],
        "assertion_ir": {
            "relation": goal.relation,
            "observed_transition_id": goal.observed_transition_id,
            "reference_transition_id": goal.reference_transition_id,
            "normative_target": normative_target,
            "expected": goal.expected,
        },
        "compiled_assertion_code": code,
        "compiled_assertion_sha256": _sha256(code),
        "execution_model": "sealed_pyfcstm_inspect_environment",
    }
    receipt = {
        "schema": "paper1.execution_certificate.v1",
        "evaluated_artifact": pair["paths"]["fcstm"],
        "evaluated_artifact_sha256": _sha256(pair["fcstm"]),
        "compiled_assertion_sha256": program["compiled_assertion_sha256"],
        "engine": {"adapter": "pyfcstm.inspect+declared_mapping"},
        "observations": {
            "observed_transition_id": goal.observed_transition_id,
            "reference_transition_id": goal.reference_transition_id,
            "normative_target": normative_target,
            "observed_actual_target": observed_actual_target,
            "reference_actual_target": reference_actual_target,
            "observed_actual_projection": observed_actual_projection,
            "observed_normative_projection": observed_normative_projection,
            "reference_normative_projection": reference_normative_projection,
            "reference_supports_normative_target": (
                reference_supports_normative_target
            ),
            "observed_supports_normative_target": artifact_actual,
        },
        "terminal": terminal,
        "precondition_failed": not reference_supports_normative_target,
        "counterexample_found": counterexample,
        "verdict": (
            "counterexample"
            if counterexample
            else "satisfied"
            if terminal
            else "inconclusive"
        ),
        "limitations": [
            (
                "Same-role semantics and the normative target are supplied by "
                "the recorded LLM binding; execution checks only exact formal IDs."
            )
        ],
    }
    dual = terminal and counterexample and source_counterexample
    return _single_group_outcome(
        pair,
        candidate,
        index=index,
        route=route,
        witness_level="W2" if terminal else "W1",
        counterexample_found=counterexample,
        source_attribution=("causal_dual_certificate" if dual else "source_localized"),
        compiled_assertion=program,
        execution_certificate=receipt,
        source_certificate=source_certificate,
    )


def _execute_guard_presence_goal(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    candidate: EvidenceCandidate,
    route: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    goal = candidate.goal
    state_paths = [
        str(row.get("path"))
        for row in inspect.get("states", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    ]
    source = _resolve_candidate_path(pair, str(goal.source), state_paths)
    target = _resolve_candidate_path(pair, str(goal.target), state_paths)
    rows = [
        row
        for row in inspect.get("transitions", [])
        if isinstance(row, dict)
        and row.get("from_path") == source
        and row.get("to_path") == target
    ]
    if source is None or target is None or not rows:
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level="W1",
            counterexample_found=False,
            source_attribution="source_localized",
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error="source/target transition could not be resolved exactly",
        )
    actual = any(row.get("guard") is not None for row in rows)
    counterexample = actual != goal.expected
    source_rows = _source_transition_rows(
        pair, source=str(goal.source), target=str(goal.target)
    )
    source_actual = any(
        row.get("guard") is not None
        or parse_guard_only_label(
            (row.get("attributes") or {}).get("raw_label")
            if isinstance(row.get("attributes"), dict)
            else None
        )
        is not None
        for row in source_rows
    )
    source_certificate = _source_static_certificate(
        pair, goal, actual=source_actual, evidence=source_rows
    )
    program_code = (
        "rows = inspect_transition(source, target)\n"
        f"assert any(row.guard is not None for row in rows) is {goal.expected}, "
        f"{EXECUTABLE_ASSERTION_MESSAGE!r}"
    )
    program = {
        "schema": "paper1.compiled_evidence_program.v1",
        "backend": route["backend"],
        "assertion_ir": goal.model_dump(mode="json"),
        "compiled_assertion_code": program_code,
        "compiled_assertion_sha256": _sha256(program_code),
        "execution_model": "sealed_pyfcstm_inspect_environment",
    }
    receipt = {
        "schema": "paper1.execution_certificate.v1",
        "evaluated_artifact": pair["paths"]["fcstm"],
        "evaluated_artifact_sha256": _sha256(pair["fcstm"]),
        "compiled_assertion_sha256": program["compiled_assertion_sha256"],
        "engine": {"adapter": "pyfcstm.inspect"},
        "observations": rows,
        "terminal": True,
        "precondition_failed": False,
        "counterexample_found": counterexample,
        "verdict": "counterexample" if counterexample else "satisfied",
    }
    dual = counterexample and source_certificate.get("verdict") == "counterexample"
    return _single_group_outcome(
        pair,
        candidate,
        index=index,
        route=route,
        witness_level="W2",
        counterexample_found=counterexample,
        source_attribution=("causal_dual_certificate" if dual else "unattributed"),
        compiled_assertion=program,
        execution_certificate=receipt,
        source_certificate=source_certificate,
    )


def _execute_unreachable_event_source_goal(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    candidate: EvidenceCandidate,
    route: dict[str, Any],
    index: int,
) -> dict[str, Any] | None:
    from paper_stm_feedback_loop.assertions.pyfcstm_adapter import (
        load_model_for_simulation,
    )
    from paper_stm_feedback_loop.assertions.topology import TopologyIndex

    goal = candidate.goal
    if not goal.source or not goal.target or not goal.trigger:
        return None
    machine = load_model_for_simulation(pair["fcstm"], pair["paths"]["fcstm"])
    topology = TopologyIndex(inspect, machine).topology()
    states = [str(item) for item in topology.get("states", [])]
    source = _resolve_candidate_path(pair, goal.source, states)
    target = _resolve_candidate_path(pair, goal.target, states)
    if source is None or target is None:
        return None
    initial_closure = set(topology.get("initial_closure", []))
    source_reachable = source in initial_closure or any(
        item.startswith(f"{source}.") for item in initial_closure
    )
    if source_reachable:
        return None

    actual = False
    counterexample = actual != goal.expected
    source_certificate = _source_missing_initial_certificate(
        pair, goal.source
    ) or _source_unreachable_certificate(pair, goal.source)
    code = (
        "source_reachable = topology_reachable(model, source)\n"
        "event_response = event_reaches_target(model, source, trigger, target) "
        "if source_reachable else False\n"
        f"assert (source_reachable and event_response) is {goal.expected}, "
        f"{EXECUTABLE_ASSERTION_MESSAGE!r}"
    )
    program = {
        "schema": "paper1.compiled_evidence_program.v1",
        "backend": route["backend"],
        "assertion_ir": {
            **goal.model_dump(mode="json"),
            "compiled_relation": "reachable_event_consumer_and_target_response",
        },
        "compiled_assertion_code": code,
        "compiled_assertion_sha256": _sha256(code),
        "execution_model": "sealed_pyfcstm_topology_then_trace_environment",
    }
    receipt = {
        "schema": "paper1.execution_certificate.v1",
        "evaluated_artifact": pair["paths"]["fcstm"],
        "evaluated_artifact_sha256": _sha256(pair["fcstm"]),
        "compiled_assertion_sha256": program["compiled_assertion_sha256"],
        "engine": {
            "adapter": "pyfcstm.verify.topology_then_trace",
            "guard_agnostic_reachability": True,
        },
        "observations": {
            "source": source,
            "target": target,
            "trigger": goal.trigger,
            "source_reachable": False,
            "initial_closure": sorted(initial_closure),
            "event_trace_executed": False,
            "short_circuit_reason": "unique event consumer is unreachable",
        },
        "terminal": True,
        "precondition_failed": False,
        "counterexample_found": counterexample,
        "verdict": "counterexample" if counterexample else "satisfied",
        "limitations": [
            "event trace is unnecessary after the unique consumer is proven unreachable"
        ],
    }
    source_counterexample = bool(
        isinstance(source_certificate, dict)
        and source_certificate.get("verdict") == "counterexample"
    )
    return _single_group_outcome(
        pair,
        candidate,
        index=index,
        route=route,
        witness_level="W2",
        counterexample_found=counterexample,
        source_attribution=(
            "causal_dual_certificate" if source_counterexample else "unattributed"
        ),
        compiled_assertion=program,
        execution_certificate=receipt,
        source_certificate=source_certificate,
    )


def _execute_event_scope_goal(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    candidate: EvidenceCandidate,
    route: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    goal = candidate.goal
    if not (
        goal.observed_transition_id
        and goal.source
        and goal.trigger
        and goal.target
        and goal.forbidden_scope
    ):
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level="W1",
            counterexample_found=False,
            source_attribution="source_localized",
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error="event_avoids_scope lacks a grounded observed transition route",
        )
    source_certificate = _source_wrong_scope_certificate(
        pair, goal.observed_transition_id, goal.forbidden_scope
    )
    enters_forbidden_scope = bool(
        isinstance(source_certificate, dict)
        and source_certificate.get("enters_forbidden_scope") is True
    )
    if not enters_forbidden_scope:
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level="W1",
            counterexample_found=False,
            source_attribution="source_localized",
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=source_certificate,
            error="the selected observed target is outside the grounded forbidden scope",
        )

    probe = ProbeCandidate(
        obligation=candidate.obligation,
        claim=candidate.claim,
        basis_kind=candidate.basis_kind,
        nl_quote=candidate.nl_quote,
        priority=candidate.priority,
        locations=candidate.locations,
        checks=[
            ProbeCheck(
                role="precondition",
                kind="reaches",
                source="[*]",
                target=goal.source,
                within_cycles=goal.within_cycles or 6,
            ),
            ProbeCheck(
                role="primary",
                kind="occupancy_after",
                source=goal.source,
                trigger=goal.trigger,
                target=goal.target,
                within_cycles=goal.within_cycles or 3,
                expected=False,
            ),
        ],
    )
    outcome = execute_plan(pair, inspect, ProbePlan(candidates=[probe]), [])[0]
    outcome["candidate_index"] = index
    outcome["candidate"] = candidate.model_dump(mode="json")
    for group in outcome.get("probe_groups", []):
        if not isinstance(group, dict):
            continue
        group["compiler_route"] = _jsonable(route)
        group["evidence_goal"] = candidate.goal.model_dump(mode="json")
        group["source_causality_certificate"] = source_certificate
        dual = bool(
            group.get("counterexample_found")
            and isinstance(source_certificate, dict)
            and source_certificate.get("verdict") == "counterexample"
        )
        if dual:
            group["source_attribution"] = {"status": "causal_dual_certificate"}
            group["source_candidate"] = bool(outcome.get("nl_anchor_valid"))
    outcome["has_source_candidate_group"] = any(
        isinstance(group, dict) and group.get("source_candidate") is True
        for group in outcome.get("probe_groups", [])
    )
    return outcome


def _execute_event_consumer_scope_goal(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    candidate: EvidenceCandidate,
    route: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    """Execute grouped exact event-consumer reachability on the FCSTM graph."""

    goal = candidate.goal
    source_certificate = _source_event_scope_certificate(pair, goal)
    if not isinstance(source_certificate, dict):
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level="W1",
            counterexample_found=False,
            source_attribution="source_localized",
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error="event consumer scope could not be resolved from exact source IDs",
        )

    from paper_stm_feedback_loop.assertions.pyfcstm_adapter import (
        load_model_for_simulation,
    )
    from paper_stm_feedback_loop.assertions.topology import TopologyIndex

    machine = load_model_for_simulation(pair["fcstm"], pair["paths"]["fcstm"])
    topology = TopologyIndex(inspect, machine).topology()
    initial_closure = {
        str(item) for item in topology.get("initial_closure", []) if isinstance(item, str)
    }

    def runtime_source_reachable(source_id: str) -> bool:
        formal_source = source_id
        if not formal_source.startswith(f"{pair['pair_name']}."):
            formal_source = f"{pair['pair_name']}.{formal_source}"
        return any(
            item == formal_source or item.startswith(f"{formal_source}.")
            for item in initial_closure
        )

    runtime_scope_results: list[dict[str, Any]] = []
    for scope_result in source_certificate.get("consumers_by_scope", []):
        if not isinstance(scope_result, dict):
            continue
        runtime_consumers: list[dict[str, Any]] = []
        for consumer in scope_result.get("consumers", []):
            if not isinstance(consumer, dict) or not isinstance(consumer.get("source"), str):
                continue
            row = dict(consumer)
            row["runtime_source_reachable"] = runtime_source_reachable(
                str(consumer["source"])
            )
            runtime_consumers.append(row)
        reachable_consumers = [
            row for row in runtime_consumers
            if row.get("runtime_source_reachable") is True
        ]
        runtime_scope_results.append(
            {
                "scope": scope_result.get("scope"),
                "consumers": runtime_consumers,
                "reachable_consumers": reachable_consumers,
                "actual": bool(reachable_consumers),
                "source_status": scope_result.get("status"),
            }
        )
    runtime_coverage = bool(runtime_scope_results) and all(
        item.get("actual") is True for item in runtime_scope_results
    )
    counterexample = not runtime_coverage
    code = (
        "for each required scope, collect exact source-AST transitions whose "
        "event identity equals observed_transition_id.event; assert every "
        "scope has one consumer source reachable in the FCSTM topology"
    )
    formal_scope = (
        goal.source
        if goal.source == pair["pair_name"]
        or goal.source.startswith(f"{pair['pair_name']}.")
        else f"{pair['pair_name']}.{goal.source}"
    )
    program = {
        "schema": "paper1.compiled_evidence_program.v1",
        "backend": "pyfcstm.topology",
        # Keep the historical two-step assertion view for audit consumers while
        # adding the typed grouped operator that actually decides the result.
        "assertion_ir": [
            {
                "predicate": "reachable",
                "bindings": {"source": f"{pair['pair_name']}.*"},
            },
            {
                "predicate": "event_consumed",
                "bindings": {
                    "source": formal_scope,
                    "trigger": source_certificate.get("event"),
                },
            },
            {
                "predicate": "grouped_event_consumer_reachable",
                "bindings": goal.model_dump(mode="json"),
            },
        ],
        "compiled_assertion_code": code,
        "compiled_assertion_sha256": _sha256(code),
        "execution_model": "sealed_pyfcstm_topology_environment",
    }
    receipt = {
        "schema": "paper1.execution_certificate.v1",
        "evaluated_artifact": pair["paths"]["fcstm"],
        "evaluated_artifact_sha256": _sha256(pair["fcstm"]),
        "compiled_assertion_sha256": program["compiled_assertion_sha256"],
        "engine": {
            "adapter": "pyfcstm.inspect.topology",
            "initial_closure_used": True,
        },
        "observations": {
            "event": source_certificate.get("event"),
            "observed_transition_id": goal.observed_transition_id,
            "initial_closure": sorted(initial_closure),
            "scopes": runtime_scope_results,
            "source_certificate_verdict": source_certificate.get("verdict"),
        },
        "terminal": True,
        "precondition_failed": False,
        "counterexample_found": counterexample,
        "verdict": "counterexample" if counterexample else "satisfied",
    }
    source_counterexample = source_certificate.get("verdict") == "counterexample"
    return _single_group_outcome(
        pair,
        candidate,
        index=index,
        route=route,
        witness_level="W2",
        counterexample_found=counterexample,
        source_attribution=(
            "causal_dual_certificate" if source_counterexample else "unattributed"
        ),
        compiled_assertion=program,
        execution_certificate=receipt,
        source_certificate=source_certificate,
    )


def _execute_topology_goal(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    candidate: EvidenceCandidate,
    route: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    from paper_stm_feedback_loop.assertions.pyfcstm_adapter import (
        load_model_for_simulation,
    )
    from paper_stm_feedback_loop.assertions.topology import (
        TopologyIndex,
        cyclic_components,
    )
    from pyfcstm.verify.topology import EXIT_ROOT_SINK, build_leaf_level_macro_graph

    goal = candidate.goal
    machine = load_model_for_simulation(pair["fcstm"], pair["paths"]["fcstm"])
    topology = TopologyIndex(inspect, machine).topology()
    reference = (
        goal.target or goal.subject
        if goal.relation == "target_reachable"
        else goal.subject
    )
    candidates = [str(item) for item in topology.get("states", [])]
    if reference and goal.relation != "eventually_terminates":
        target, target_resolution = _resolve_topology_reference(
            pair, str(reference), candidates
        )
    elif goal.relation == "eventually_terminates":
        target = pair["pair_name"]
        target_resolution = {
            "reference": pair["pair_name"],
            "mode": "whole_machine",
            "nodes": [pair["pair_name"]],
        }
    else:
        target = None
        target_resolution = {"reference": reference, "mode": "unresolved", "nodes": []}
    target_nodes = [
        str(item)
        for item in target_resolution.get("nodes", [])
        if isinstance(item, str)
    ]
    if goal.relation == "target_reachable" and goal.source:
        root_scope_ids = {
            pair["pair_name"],
            _source_root_scope_id(pair),
        }
        if str(goal.source) in root_scope_ids:
            # The topology backend represents the machine root by its initial
            # closure rather than by a leaf node.  Bind this exact canonical
            # root identity here; treating it as a regular state ID would
            # incorrectly report every root-to-target query as unresolved.
            source = pair["pair_name"]
            source_nodes = [
                str(node)
                for node in topology.get("initial_closure", [])
                if isinstance(node, str)
            ]
            source_resolution = {
                "reference": goal.source,
                "mode": "root_initial_closure",
                "nodes": source_nodes,
            }
        else:
            source, source_resolution = _resolve_topology_reference(
                pair, str(goal.source), candidates
            )
    else:
        source = None
        source_resolution = {
            "reference": goal.source,
            "mode": "not_applicable",
            "nodes": [],
        }
    if not (
        goal.relation == "target_reachable"
        and goal.source
        and str(goal.source)
        in {pair["pair_name"], _source_root_scope_id(pair)}
    ):
        source_nodes = [
            str(item)
            for item in source_resolution.get("nodes", [])
            if isinstance(item, str)
        ]
    if target is None:
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level="W1",
            counterexample_found=False,
            source_attribution="source_localized",
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error="topology subject could not be resolved exactly",
        )
    if goal.relation == "target_reachable" and goal.source and source is None:
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level="W1",
            counterexample_found=False,
            source_attribution="source_localized",
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error="topology source could not be resolved exactly",
        )

    source_certificate: dict[str, Any] | None = None
    if goal.relation == "target_reachable":
        if source is not None:
            graph = build_leaf_level_macro_graph(machine)
            queue = list(source_nodes)
            parents: dict[str, str | None] = {
                source_node: None for source_node in source_nodes
            }
            while queue:
                node = queue.pop(0)
                for successor in graph.edges.get(node, ()):
                    if successor in parents:
                        continue
                    parents[successor] = node
                    queue.append(successor)
            reached_targets = [node for node in target_nodes if node in parents]
            source_target_path: list[str] = []
            if reached_targets:
                cursor: str | None = reached_targets[0]
                while cursor is not None:
                    source_target_path.append(cursor)
                    cursor = parents[cursor]
                source_target_path.reverse()
            actual = bool(reached_targets)
            proof_slice = {
                "source": source,
                "source_resolution": source_resolution,
                "target": target,
                "target_resolution": target_resolution,
                "reached_targets": reached_targets,
                "source_target_path": source_target_path,
                "reachable_from_source": sorted(parents),
                "unreachable_leaves": topology.get("unreachable_leaves", []),
                "query_bound": None,
            }
            # A converted-topology counterexample is not source-attributed by
            # itself.  For the exact machine-root query, repeat the same
            # reachability fact on the canonical source AST so D can distinguish
            # an authored missing entry from representation debt.
            if not actual and source == pair["pair_name"]:
                source_certificate = _source_root_target_reachability_certificate(
                    pair, str(reference)
                )
        else:
            unreachable = set(topology.get("unreachable_leaves", []))
            reached_targets = [node for node in target_nodes if node not in unreachable]
            actual = bool(reached_targets)
            source_certificate = _source_missing_initial_certificate(
                pair, str(reference)
            ) or _source_unreachable_certificate(pair, str(reference))
            proof_slice = {
                "source": None,
                "source_resolution": source_resolution,
                "target": target,
                "target_resolution": target_resolution,
                "reached_targets": reached_targets,
                "unreachable_leaves": topology.get("unreachable_leaves", []),
                "initial_closure": topology.get("initial_closure", []),
                "absence_cut": [
                    edge
                    for edge in topology.get("transitions", [])
                    if edge.get("source") in set(topology.get("initial_closure", []))
                    and edge.get("target")
                    not in set(topology.get("initial_closure", []))
                ],
                "query_bound": None,
            }
        decisive = True
    elif goal.relation == "state_escapable":
        initial_closure = set(topology.get("initial_closure", []))
        dead_ends = set(topology.get("dead_ends", []))
        reachable_targets = [node for node in target_nodes if node in initial_closure]
        blocked_targets = [node for node in reachable_targets if node in dead_ends]
        initially_reachable = bool(reachable_targets)
        actual = initially_reachable and not blocked_targets
        source_certificate = _source_deadlock_certificate(pair, str(reference))
        decisive = initially_reachable
        proof_slice = {
            "target": target,
            "target_resolution": target_resolution,
            "initially_reachable": initially_reachable,
            "reachable_targets": reachable_targets,
            "blocked_targets": blocked_targets,
            "dead_ends": topology.get("dead_ends", []),
        }
    elif goal.relation == "termination_target":
        graph = build_leaf_level_macro_graph(machine)
        initial_closure = set(topology.get("initial_closure", []))
        target_reachable = target in initial_closure
        queue = [target]
        parents: dict[str, str | None] = {target: None}
        while queue:
            node = queue.pop(0)
            for successor in graph.edges.get(node, ()):
                if successor in parents:
                    continue
                parents[successor] = node
                queue.append(successor)
        sink_path: list[str] = []
        if EXIT_ROOT_SINK in parents:
            cursor: str | None = EXIT_ROOT_SINK
            while cursor is not None:
                sink_path.append(cursor)
                cursor = parents[cursor]
            sink_path.reverse()
        reachable_nodes = sorted(node for node in parents if node != EXIT_ROOT_SINK)
        reachable_node_set = set(reachable_nodes)
        scoped_edges = {
            node: tuple(
                successor
                for successor in graph.edges.get(node, ())
                if successor in reachable_node_set
            )
            for node in reachable_nodes
        }
        cycles = cyclic_components(reachable_nodes, scoped_edges)
        nonterminal_dead_ends = [
            node for node in reachable_nodes if not graph.edges.get(node, ())
        ]
        actual = bool(
            target_reachable and sink_path and not cycles and not nonterminal_dead_ends
        )
        decisive = target_reachable
        source_certificate = _source_stable_termination_certificate(
            pair, str(reference)
        )
        proof_slice = {
            "target": target,
            "target_initially_reachable": target_reachable,
            "target_successors": list(graph.edges.get(target, ())),
            "root_exit_sink": EXIT_ROOT_SINK,
            "root_exit_path": sink_path,
            "reachable_from_target": reachable_nodes,
            "reachable_cycles_avoiding_root_exit": cycles,
            "nonterminal_dead_ends": nonterminal_dead_ends,
        }
    else:
        finite = topology.get("topological_finite") or {}
        inevitable = topology.get("topological_inevitable_terminator") or {}
        actual = bool(finite.get("value") and inevitable.get("value"))
        decisive = (
            finite.get("value") is not None and inevitable.get("value") is not None
        )
        proof_slice = {
            "topological_finite": finite,
            "topological_inevitable_terminator": inevitable,
            "strongly_connected_components": topology.get(
                "strongly_connected_components", []
            ),
        }
    counterexample = decisive and actual != goal.expected
    operation = (
        "stable_termination_target"
        if goal.relation == "termination_target"
        else "source_target_reachability"
        if goal.relation == "target_reachable" and source is not None
        else "topology_certificate"
    )
    code = (
        f"proof = {operation}(model, goal)\n"
        f"assert proof.actual is {goal.expected}, {EXECUTABLE_ASSERTION_MESSAGE!r}"
    )
    program = {
        "schema": "paper1.compiled_evidence_program.v1",
        "backend": route["backend"],
        "assertion_ir": goal.model_dump(mode="json"),
        "compiled_assertion_code": code,
        "compiled_assertion_sha256": _sha256(code),
        "execution_model": "sealed_pyfcstm_topology_environment",
    }
    receipt = {
        "schema": "paper1.execution_certificate.v1",
        "evaluated_artifact": pair["paths"]["fcstm"],
        "evaluated_artifact_sha256": _sha256(pair["fcstm"]),
        "compiled_assertion_sha256": program["compiled_assertion_sha256"],
        "engine": {"adapter": "pyfcstm.verify.topology", "guard_agnostic": True},
        "observations": proof_slice,
        "terminal": decisive,
        "precondition_failed": False,
        "counterexample_found": counterexample,
        "verdict": (
            "counterexample"
            if counterexample
            else "satisfied"
            if decisive
            else "inconclusive"
        ),
        "limitations": topology.get("limitations", []),
    }
    source_counterexample = bool(
        isinstance(source_certificate, dict)
        and source_certificate.get("verdict") == "counterexample"
    )
    return _single_group_outcome(
        pair,
        candidate,
        index=index,
        route=route,
        witness_level="W2" if decisive else "W1",
        counterexample_found=counterexample,
        source_attribution=(
            "causal_dual_certificate" if source_counterexample else "unattributed"
        ),
        compiled_assertion=program,
        execution_certificate=receipt,
        source_certificate=source_certificate,
    )


def _execute_evidence_candidate(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    planned_candidate: EvidenceCandidate,
    *,
    index: int,
) -> dict[str, Any]:
    obligation = planned_candidate.domain_obligation
    lowering_errors = validate_domain_obligation_lowering(planned_candidate)
    soundness_errors = validate_operator_executable_soundness(planned_candidate)
    support = derive_support_disposition(planned_candidate, lowering_errors)
    if lowering_errors or soundness_errors:
        errors = lowering_errors or soundness_errors
        return _single_group_outcome(
            pair,
            planned_candidate,
            index=index,
            route={
                "schema": "paper1.evidence_route.v2",
                "template": None,
                "backend": None,
                "operation": (
                    "invalid_typed_lowering"
                    if lowering_errors
                    else "unsupported_executable_fragment"
                ),
                "checks": [],
                "errors": errors,
                "domain_obligation": (
                    obligation.model_dump(mode="json")
                    if obligation is not None
                    else None
                ),
                "typed_obligation_status": (
                    "invalid" if lowering_errors else "unsupported"
                ),
                "support_disposition": support.model_dump(mode="json"),
                "method_bindings": [],
            },
            witness_level=support.w_ceiling,
            counterexample_found=False,
            source_attribution=(
                "source_localized" if planned_candidate.locations else "unattributed"
            ),
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error="; ".join(errors),
        )
    candidate, method_bindings = _apply_formal_transition_binding(
        pair, planned_candidate
    )
    route = compile_evidence_goal(candidate.goal)
    route["schema"] = "paper1.evidence_route.v2"
    route["domain_obligation"] = (
        obligation.model_dump(mode="json") if obligation is not None else None
    )
    route["typed_obligation_status"] = (
        "validated" if obligation is not None else "legacy_untyped"
    )
    route["support_disposition"] = support.model_dump(mode="json")
    route["method_bindings"] = method_bindings
    if route["errors"]:
        support = derive_support_disposition(candidate, list(route["errors"]))
        route["support_disposition"] = support.model_dump(mode="json")
        return _single_group_outcome(
            pair,
            candidate,
            index=index,
            route=route,
            witness_level=support.w_ceiling,
            counterexample_found=False,
            source_attribution=(
                "source_localized" if candidate.locations else "unattributed"
            ),
            compiled_assertion=None,
            execution_certificate=None,
            source_certificate=None,
            error="; ".join(route["errors"]),
        )
    if candidate.goal.relation in {"action_exists", "effect_exists"}:
        return _execute_action_effect_goal(pair, inspect, candidate, route, index)
    if candidate.goal.relation == "event_consumed_in_scope":
        return _execute_event_consumer_scope_goal(
            pair, inspect, candidate, route, index
        )
    if route["operation"] == "topology_certificate":
        return _execute_topology_goal(pair, inspect, candidate, route, index)
    if route["operation"] == "guard_solver":
        return _execute_source_guard_goal(pair, inspect, candidate, route, index)
    if route["operation"] == "artifact_static":
        if candidate.goal.relation == "final_pseudostate_exists":
            return _execute_final_pseudostate_presence_goal(
                pair, candidate, route, index
            )
        if candidate.goal.relation == "completion_transition_fireable":
            return _execute_completion_transition_goal(
                pair, inspect, candidate, route, index
            )
        if candidate.goal.relation in {
            "transition_contract",
            "transition_exists",
            "transition_absent",
        }:
            return _execute_transition_contract_goal(
                pair, inspect, candidate, route, index
            )
        if candidate.goal.relation == "transition_target_consistency":
            return _execute_transition_target_consistency_goal(
                pair, inspect, candidate, route, index
            )
        return _execute_guard_presence_goal(pair, inspect, candidate, route, index)
    if candidate.goal.relation == "event_avoids_scope":
        return _execute_event_scope_goal(pair, inspect, candidate, route, index)
    if candidate.goal.relation == "event_reaches_target":
        unreachable_source = _execute_unreachable_event_source_goal(
            pair, inspect, candidate, route, index
        )
        if unreachable_source is not None:
            return unreachable_source

    legacy_candidate = ProbeCandidate(
        obligation=candidate.obligation,
        claim=candidate.claim,
        basis_kind=candidate.basis_kind,
        nl_quote=candidate.nl_quote,
        priority=candidate.priority,
        locations=candidate.locations,
        checks=route["checks"],
    )
    outcome = execute_plan(
        pair,
        inspect,
        ProbePlan(candidates=[legacy_candidate]),
        [],
        binding_authority="formal_source_ast",
    )[0]
    outcome["candidate_index"] = index
    outcome["candidate"] = candidate.model_dump(mode="json")
    for group in outcome.get("probe_groups", []):
        group["compiler_route"] = _jsonable(route)
        group["evidence_goal"] = candidate.goal.model_dump(mode="json")
        source_certificate = group.get("source_causality_certificate")
        if (
            candidate.goal.relation == "initial_target"
            and candidate.requirement_group_id is not None
            and isinstance(source_certificate, dict)
            and source_certificate.get("kind") == "source_initial_target_contract"
        ):
            source_certificate["requirement_group_id"] = (
                candidate.requirement_group_id
            )
        if candidate.goal.relation == "event_consumed_in_scope":
            source_certificate = _source_event_scope_certificate(pair, candidate.goal)
            group["source_causality_certificate"] = source_certificate
            dual = bool(
                group.get("counterexample_found")
                and isinstance(source_certificate, dict)
                and source_certificate.get("verdict") == "counterexample"
            )
            group["source_attribution"] = {
                "status": "causal_dual_certificate" if dual else "unattributed"
            }
            group["source_candidate"] = bool(
                dual and group.get("witness_level") == "W2"
            )
    return outcome


def execute_evidence_plan(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    plan: EvidencePlan | BalancedEvidencePlan | HybridEvidencePlan | IssueDiscoveryPlan,
    *,
    binding_authority: SemanticBindingAuthority = "formal_source_ast",
    semantic_provenance: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Execute semantic goals through the one fixed compiler policy."""

    outcomes: list[dict[str, Any]] = []
    for index, planned_candidate in enumerate(plan.candidates, start=1):
        try:
            outcomes.append(
                _execute_evidence_candidate(
                    pair, inspect, planned_candidate, index=index
                )
            )
        except Exception as exc:  # noqa: BLE001 - one candidate must not drop peers
            error = f"candidate execution degraded: {type(exc).__name__}: {exc}"
            outcomes.append(
                _single_group_outcome(
                    pair,
                    planned_candidate,
                    index=index,
                    route={
                        "template": None,
                        "backend": None,
                        "operation": None,
                        "checks": [],
                        "errors": [error],
                        "method_bindings": [],
                    },
                    witness_level="W1" if planned_candidate.locations else "W0",
                    counterexample_found=False,
                    source_attribution=(
                        "source_localized"
                        if planned_candidate.locations
                        else "unattributed"
                    ),
                    compiled_assertion=None,
                    execution_certificate=None,
                    source_certificate=None,
                    error=error,
                )
            )
    plan_hash = _canonical_sha256(plan)
    return [
        _attach_semantic_binding_receipt(
            outcome,
            binding_authority,
            semantic_provenance=semantic_provenance,
            compiler_input_plan_sha256=plan_hash,
        )
        for outcome in outcomes
    ]


def execute_contract_lens_plan(
    pair: dict[str, Any], inspect: dict[str, Any], plan: ContractLensPlan
) -> list[dict[str, Any]]:
    return execute_evidence_plan(pair, inspect, expand_contract_lens_plan(pair, plan))


def execute_contract_extraction_plan(
    pair: dict[str, Any],
    inspect: dict[str, Any],
    plan: ContractExtractionPlan,
    *,
    binding_authority: SemanticBindingAuthority = "formal_source_ast",
    semantic_provenance: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    candidates = [
        *expand_initial_contracts(pair, plan.initial_contracts),
        *expand_containment_contracts(pair, plan.containment_contracts),
        *expand_transition_groups(pair, plan.transition_groups),
    ]
    return execute_evidence_plan(
        pair,
        inspect,
        EvidencePlan(candidates=candidates),
        binding_authority=binding_authority,
        semantic_provenance=semantic_provenance,
    )


def select_finding_outcomes(outcomes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Quarantine diagnostic clues and prefer explicit facets for one cause."""

    explicit_causes = {
        cause_key
        for outcome in outcomes
        if any(
            isinstance(group, dict)
            and group.get("origin") != "progressive_deterministic_scout"
            and group.get("source_candidate") is True
            for group in outcome.get("probe_groups", [])
        )
        for group in outcome.get("probe_groups", [])
        if isinstance(group, dict)
        and isinstance(group.get("source_causality_certificate"), dict)
        and (cause_key := _certificate_cause_key(group["source_causality_certificate"]))
    }
    selected = []
    for outcome in outcomes:
        groups = []
        for group in outcome.get("probe_groups", []):
            if not isinstance(group, dict):
                continue
            if group.get("origin") == "progressive_deterministic_scout":
                if not group.get("source_candidate"):
                    continue
                certificate = group.get("source_causality_certificate")
                cause_key = (
                    _certificate_cause_key(certificate)
                    if isinstance(certificate, dict)
                    else None
                )
                if cause_key in explicit_causes:
                    continue
            groups.append(group)
        if groups:
            selected.append({**outcome, "probe_groups": groups})
    return selected


def build_issue_clusters(outcomes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate technical candidates by executable source cause."""

    clusters: dict[str, dict[str, Any]] = {}
    for outcome in outcomes:
        if not outcome.get("nl_anchor_valid"):
            continue
        candidate = outcome.get("candidate", {})
        candidate = candidate if isinstance(candidate, dict) else {}
        for group in outcome.get("probe_groups", []):
            if not isinstance(group, dict) or not group.get("source_candidate"):
                continue
            certificate = group.get("source_causality_certificate")
            certificate = certificate if isinstance(certificate, dict) else {}
            kind = certificate.get("kind")
            cause_key = _certificate_cause_key(certificate) or (
                f"source:safe:{outcome.get('candidate_index')}:{group.get('group_id')}"
            )
            cluster = clusters.setdefault(
                cause_key,
                {
                    "cause_key": cause_key,
                    "cause_kind": kind or "runtime_safe_path",
                    "witness_level": "W2",
                    "evaluated_artifact": group.get("evaluated_artifact"),
                    "source_attribution": group.get("source_attribution"),
                    "candidate_indices": [],
                    "probe_group_ids": [],
                    "claims": [],
                    "obligations": [],
                    "nl_quotes": [],
                    "artifact_consequences": [],
                    "source_causality_certificate": certificate or None,
                    "attempt_count": 0,
                    "needs_external_d_adjudication": True,
                },
            )
            cluster["candidate_indices"].append(outcome.get("candidate_index"))
            cluster["probe_group_ids"].append(group.get("group_id"))
            cluster["claims"].append(group.get("claim"))
            cluster["obligations"].append(candidate.get("obligation"))
            if candidate.get("nl_quote"):
                cluster["nl_quotes"].append(candidate["nl_quote"])
            if certificate.get("target_consequence"):
                cluster["artifact_consequences"].append(
                    certificate["target_consequence"]
                )
            elif certificate.get("target"):
                cluster["artifact_consequences"].append(certificate["target"])
            cluster["attempt_count"] += 1

    for cluster in clusters.values():
        for field in (
            "candidate_indices",
            "probe_group_ids",
            "claims",
            "obligations",
            "nl_quotes",
            "artifact_consequences",
        ):
            cluster[field] = list(dict.fromkeys(cluster[field]))
    return list(clusters.values())


def _finding_key(outcome: dict[str, Any], group: dict[str, Any] | None) -> str:
    certificate = (group or {}).get("source_causality_certificate")
    cause_key: str | None = None
    if isinstance(certificate, dict):
        cause_key = _certificate_cause_key(certificate)
    candidate = outcome.get("candidate", {})
    candidate = candidate if isinstance(candidate, dict) else {}
    if cause_key is None:
        cause_material = {
            "claim": (group or {}).get("claim", candidate.get("claim")),
            "locations": candidate.get("locations", []),
            "group_origin": (group or {}).get("origin", "planner_envelope"),
        }
        cause_digest = _sha256(
            json.dumps(cause_material, ensure_ascii=False, sort_keys=True)
        )[:16]
        cause_key = f"hypothesis:{cause_digest}"
    goal = candidate.get("goal")
    goal = goal if isinstance(goal, dict) else {}
    semantic_binding = {
        key: goal.get(key)
        for key in (
            "relation",
            "observed_transition_id",
            "reference_transition_id",
            "subject",
            "source",
            "trigger",
            "target",
            "forbidden_scope",
            "scope_applicability",
            "required_scope_ids",
            "response",
            "variable",
            "sign",
            "phase",
            "action",
            "count",
            "condition",
            "within_cycles",
            "expected",
        )
        if goal.get(key) is not None
        and not (
            key == "source"
            and goal.get("relation") == "event_consumed_in_scope"
        )
    }
    nl_locations = sorted(
        str(item)
        for item in candidate.get("locations", [])
        if re.fullmatch(r"NL:?\d+", str(item))
    )
    obligation_material = {
        "basis_kind": candidate.get("basis_kind"),
        "nl_anchor": nl_locations or candidate.get("nl_quote"),
        "semantic_binding": semantic_binding,
        "obligation": candidate.get("obligation")
        if not candidate.get("nl_quote")
        else None,
    }
    obligation_digest = _sha256(
        json.dumps(obligation_material, ensure_ascii=False, sort_keys=True)
    )[:12]
    return f"{cause_key}:facet:{obligation_digest}"


def _infer_l_level(candidate: dict[str, Any], group: dict[str, Any] | None) -> str:
    certificate = (group or {}).get("source_causality_certificate")
    certificate = certificate if isinstance(certificate, dict) else {}
    if certificate.get("kind") == "initial_contract_violation":
        return "L0"
    if certificate.get("kind") in {
        "source_transition_contract",
        "source_extraneous_transition",
        "source_guarded_completion_unfireable",
        "source_required_state_presence",
        "source_required_final_pseudostate_presence",
        "source_event_missing_in_scope",
    }:
        return "L0"
    if certificate.get("kind") == "source_initial_target_contract":
        direct_edge_fact = certificate.get("matching_edge_count") == 0 or (
            certificate.get("child") == certificate.get("composite")
        )
        return "L0" if direct_edge_fact else "L1"
    if certificate.get("kind") in {
        "source_containment_contract",
        "source_child_count_contract",
        "source_guard_presence",
        "source_guard_overlap",
        "source_transition_target_inconsistency",
    }:
        return "L1"
    if certificate.get("kind") in {
        "reachable_deadlock",
        "concurrent_region_deadlock",
        "source_entry_deadlock",
        "missing_initial_with_compiler_consequence",
        "unreachable_source_component",
        "source_root_target_unreachable",
        "source_wrong_scope_route",
        "source_unstable_termination_target",
        "source_event_consumers_unreachable",
        "source_event_scope_unavailable",
    }:
        return "L2"
    goal = candidate.get("goal")
    goal = goal if isinstance(goal, dict) else {}
    relation = goal.get("relation")
    if relation in {
        "initial_target",
        "state_exists",
        "final_pseudostate_exists",
        "variable_exists",
        "event_exists",
        "action_exists",
        "effect_exists",
        "transition_contract",
        "transition_exists",
        "transition_absent",
        "event_consumed_in_scope",
    }:
        return "L0"
    if relation in {
        "contained_in",
        "child_count",
        "guard_present",
        "guards_distinguishable",
        "transition_target_consistency",
    }:
        return "L1"
    if relation in {
        "target_reachable",
        "state_escapable",
        "event_reaches_target",
        "event_avoids_scope",
        "event_consumed",
        "eventually_responds",
        "eventually_terminates",
        "termination_target",
    }:
        return "L2"
    behavior = {
        "occupancy_after",
        "event_consumed",
        "stays_in",
        "variable_delta_after",
        "reaches",
        "terminates",
        "invariant",
        "response_within",
        "persists_until",
    }
    kinds = {
        check.get("normalized_probe", {}).get("kind")
        for check in (group or {}).get("checks", [])
        if isinstance(check, dict)
    }
    return "L2" if kinds.intersection(behavior) else "L1"


def _valid_semantic_binding_receipt(certificate: dict[str, Any]) -> bool:
    receipt = certificate.get("semantic_binding_receipt")
    if not isinstance(receipt, dict):
        return False
    stored_receipt_hash = receipt.get("receipt_sha256")
    receipt_payload = {
        key: value for key, value in receipt.items() if key != "receipt_sha256"
    }
    if not (
        receipt.get("schema") == "paper1.semantic_binding_receipt.v2"
        and stored_receipt_hash == _canonical_sha256(receipt_payload)
        and receipt.get("formal_reference_policy")
        == "exact_id_or_declared_mapping_only"
        and isinstance(receipt.get("grounded_candidate_sha256"), str)
        and isinstance(receipt.get("compiler_input_plan_sha256"), str)
        and isinstance(receipt.get("formal_binding_transforms_sha256"), str)
    ):
        return False
    authority = receipt.get("authority")
    if authority in {"formal_source_ast", "formal_pyfcstm_diagnostic"}:
        return bool(
            receipt.get("scope") == "formal_fact_only"
            and receipt.get("semantic_decision_claimed") is False
            and receipt.get("semantic_provenance") is None
        )
    if authority not in {
        "paper1_discovery_grounding_llm",
        "paper1_semantic_grounding_llm",
        "paper1_evidence_planning_llm",
    }:
        return False
    provenance = receipt.get("semantic_provenance")
    if not isinstance(provenance, dict):
        return False
    stored_provenance_hash = provenance.get("provenance_sha256")
    provenance_payload = {
        key: value for key, value in provenance.items() if key != "provenance_sha256"
    }
    expected_role = {
        "paper1_discovery_grounding_llm": "paper1_discovery_grounding",
        "paper1_semantic_grounding_llm": "paper1_semantic_grounding",
        "paper1_evidence_planning_llm": "paper1_evidence_planning",
    }[authority]
    return bool(
        receipt.get("scope") == "nl_to_formal"
        and receipt.get("semantic_decision_claimed") is True
        and provenance.get("role") == expected_role
        and isinstance(provenance.get("llm_call_id"), str)
        and provenance.get("stage_record_ref")
        == f"llm_call:{provenance.get('llm_call_id')}"
        and provenance.get("parsed_output_sha256")
        == provenance.get("semantic_plan_sha256")
        and isinstance(provenance.get("structured_schema_sha256"), str)
        and isinstance(provenance.get("schema_contract_repeated_in_prompt"), bool)
        and stored_provenance_hash == _canonical_sha256(provenance_payload)
    )


def validate_record_semantic_provenance(record: dict[str, Any]) -> list[str]:
    """Cross-check W2 receipt claims against the immutable run-level evidence."""

    errors: list[str] = []
    observations = {
        item.get("llm_call_id"): item
        for item in record.get("llm_observations", [])
        if isinstance(item, dict)
        and isinstance(item.get("llm_call_id"), str)
        and item.get("status") == "completed"
    }
    semantic_plans = record.get("discovery_grounding_plans")
    contract_plans = record.get("grounded_contract_plans")
    evidence_plans = record.get("grounded_evidence_plans")
    if not all(
        isinstance(items, list)
        for items in (semantic_plans, contract_plans, evidence_plans)
    ):
        semantic_plans = [record.get("discovery_grounding_plan")]
        contract_plans = [record.get("grounded_contract_plan")]
        evidence_plans = [record.get("grounded_evidence_plan")]
    expected_plan_hashes = [
        {
            "semantic_plan_sha256": _canonical_sha256(semantic_plan),
            "grounded_contract_plan_sha256": _canonical_sha256(contract_plan),
            "grounded_evidence_plan_sha256": _canonical_sha256(evidence_plan),
        }
        for semantic_plan, contract_plan, evidence_plan in zip(
            semantic_plans, contract_plans, evidence_plans, strict=True
        )
    ]
    for outcome_index, outcome in enumerate(record.get("outcomes", [])):
        if not isinstance(outcome, dict):
            continue
        candidate = outcome.get("candidate")
        candidate = candidate if isinstance(candidate, dict) else {}
        groups = [
            group
            for group in outcome.get("probe_groups", [])
            if isinstance(group, dict)
        ]
        transforms = [
            group.get("compiler_route", {}).get("method_bindings", [])
            for group in groups
            if isinstance(group.get("compiler_route"), dict)
        ]
        for group_index, group in enumerate(groups):
            certificate = group.get("execution_certificate")
            if not isinstance(certificate, dict):
                continue
            prefix = f"outcomes[{outcome_index}].probe_groups[{group_index}]"
            if not _valid_semantic_binding_receipt(certificate):
                errors.append(f"{prefix}: invalid semantic-binding receipt")
                continue
            receipt = certificate["semantic_binding_receipt"]
            if receipt.get("grounded_candidate_sha256") != _canonical_sha256(candidate):
                errors.append(
                    f"{prefix}: candidate hash does not match executed candidate"
                )
            if receipt.get("formal_binding_transforms_sha256") != _canonical_sha256(
                transforms
            ):
                errors.append(f"{prefix}: formal-binding transform hash mismatch")
            if receipt.get("scope") == "formal_fact_only":
                continue
            provenance = receipt["semantic_provenance"]
            call_id = provenance.get("llm_call_id")
            observation = observations.get(call_id)
            if not isinstance(observation, dict):
                errors.append(
                    f"{prefix}: referenced LLM call is absent from run record"
                )
                continue
            observation_hashes = {
                "system_prompt_sha256": _canonical_sha256(
                    observation.get("system_prompt")
                ),
                "user_prompt_sha256": _canonical_sha256(observation.get("user_prompt")),
                "raw_response_sha256": _canonical_sha256(
                    observation.get("raw_response")
                ),
                "parsed_output_sha256": _canonical_sha256(
                    observation.get("parsed_output")
                ),
                "observation_sha256": _canonical_sha256(observation),
            }
            if not any(
                all(
                    provenance.get(field) == expected for field, expected in row.items()
                )
                for row in expected_plan_hashes
            ):
                errors.append(
                    f"{prefix}: provenance does not match any discovery branch"
                )
            for field, expected in observation_hashes.items():
                if provenance.get(field) != expected:
                    errors.append(f"{prefix}: provenance field {field} does not match")
            for field in (
                "role",
                "profile",
                "provider",
                "configured_model",
                "observed_model",
                "structured_schema_sha256",
                "schema_contract_repeated_in_prompt",
            ):
                if provenance.get(field) != observation.get(field):
                    errors.append(f"{prefix}: provenance field {field} does not match")
            if bool(provenance.get("replayed")) != bool(
                record.get("replay_plans_from")
            ):
                errors.append(f"{prefix}: replay provenance does not match run mode")
    return errors


def _terminal_counterexample_certificates(
    group: dict[str, Any],
) -> list[dict[str, Any]]:
    certificate = group.get("execution_certificate")
    certificates = [certificate] if isinstance(certificate, dict) else []
    return [
        item
        for item in certificates
        if item.get("terminal") is True
        and item.get("verdict") == "counterexample"
        and item.get("counterexample_found") is True
        and isinstance(item.get("evaluated_artifact_sha256"), str)
        and isinstance(item.get("compiled_assertion_sha256"), str)
        and _valid_semantic_binding_receipt(item)
    ]


def _derive_witness_level(
    candidate: dict[str, Any], group: dict[str, Any]
) -> Literal["W2", "W1", "W0"]:
    """Derive W from evidence artifacts instead of accepting an LLM label."""

    if _terminal_counterexample_certificates(group):
        # A terminal FCSTM receipt alone is not enough to call a source-grounded
        # claim W2.  When a source certificate is present, the source side must
        # also be a closed counterexample; an inconclusive or explicitly unsound
        # bridge is a localized W1 result and must remain visible to D adjudication.
        source_certificate = group.get("source_causality_certificate")
        if isinstance(source_certificate, dict) and (
            source_certificate.get("sound_for_claim") is not True
            or source_certificate.get("verdict") != "counterexample"
        ):
            return "W1"
        return "W2"
    source_status = group.get("source_attribution")
    source_status = source_status if isinstance(source_status, dict) else {}
    localized = bool(
        candidate.get("locations")
        or group.get("compiled_assertion")
        or group.get("execution_certificate")
        or group.get("source_causality_certificate")
        or source_status.get("status") in {"source_localized", "representation_debt"}
    )
    return "W1" if localized else "W0"


def _group_is_issue_candidate(group: dict[str, Any]) -> bool:
    """Retain counterexamples and inconclusive hypotheses, but not passing checks."""

    if group.get("counterexample_found"):
        return True
    certificate = group.get("execution_certificate")
    if isinstance(certificate, dict) and certificate.get("verdict") == "satisfied":
        return False
    source_certificate = group.get("source_causality_certificate")
    if (
        isinstance(source_certificate, dict)
        and source_certificate.get("sound_for_claim") is True
        and source_certificate.get("verdict") == "satisfied"
    ):
        return False
    return group.get("witness_level") in {"W1", "W0"} or bool(group.get("error"))


def _canonical_source_fact(certificate: dict[str, Any]) -> str | None:
    """Render only typed source-certificate facts; never interpret model prose."""

    if certificate.get("verdict") != "counterexample":
        return None
    kind = certificate.get("kind")
    if kind == "source_initial_target_contract":
        return (
            f"Source composite {certificate.get('composite')!r} has no initial "
            f"transition to required child {certificate.get('child')!r}."
        )
    if kind == "source_containment_contract":
        if certificate.get("expected") is False:
            return (
                f"Source child {certificate.get('child')!r} has the forbidden "
                f"direct parent {certificate.get('expected_parent')!r}; the "
                "negative containment obligation is violated."
            )
        return (
            f"Source child {certificate.get('child')!r} has actual parent "
            f"{certificate.get('actual_parent')!r}, not required parent "
            f"{certificate.get('expected_parent')!r}."
        )
    if kind == "source_transition_contract":
        trigger = certificate.get("trigger")
        trigger_text = f" under {trigger!r}" if trigger is not None else ""
        return (
            f"Source has no matching transition from {certificate.get('source')!r} "
            f"to {certificate.get('target')!r}{trigger_text}."
        )
    if kind == "source_transition_target_inconsistency":
        return (
            f"Source transition {certificate.get('observed_transition_id')!r} targets "
            f"{certificate.get('observed_target')!r}, while reference transition "
            f"{certificate.get('reference_transition_id')!r} realizes required target "
            f"{certificate.get('normative_target')!r}."
        )
    if kind == "source_root_target_unreachable":
        return (
            f"No source-graph path reaches target {certificate.get('target')!r} "
            f"from the exact root entry {certificate.get('source')!r}."
        )
    if kind == "source_event_missing_in_scope":
        missing = certificate.get("missing_scope_ids")
        if not isinstance(missing, list):
            missing = [certificate.get("source")]
        return (
            f"Exact event {certificate.get('event')!r} has no consumer in required "
            f"scope(s) {missing!r}; observed event identity came from transition "
            f"{certificate.get('observed_transition_id')!r}."
        )
    if kind in {
        "source_event_consumers_unreachable",
        "source_event_scope_unavailable",
    }:
        unreachable = certificate.get("unreachable_scope_ids")
        unreachable = unreachable if isinstance(unreachable, list) else []
        consumers = certificate.get("aggregate_consumers")
        consumer_ids = [
            str(item.get("id"))
            for item in consumers
            if isinstance(item, dict) and item.get("id") is not None
        ] if isinstance(consumers, list) else []
        return (
            f"Exact event {certificate.get('event')!r} has authored consumers "
            f"{list(dict.fromkeys(consumer_ids))!r}, but none is reachable in "
            f"required scope(s) {unreachable!r}; the selected event identity came "
            f"from transition {certificate.get('observed_transition_id')!r}."
        )
    if kind == "source_wrong_scope_route":
        return (
            f"Source transition {certificate.get('observed_transition_id')!r} from "
            f"{certificate.get('source')!r} to {certificate.get('target')!r} enters "
            f"forbidden scope {certificate.get('forbidden_scope')!r}."
        )
    if kind == "unreachable_source_component":
        return (
            f"Source component {certificate.get('component')!r} is unreachable "
            "from the source root entry."
        )
    if kind == "source_guard_overlap":
        return (
            f"At least two exact outgoing guards from source state "
            f"{certificate.get('source')!r} overlap in the formal guard solver."
        )
    if kind == "source_extraneous_transition":
        transition = certificate.get("observed_transition")
        transition_id = (
            transition.get("id") if isinstance(transition, dict) else None
        ) or certificate.get("observed_transition_id")
        return f"Exact source transition {transition_id!r} is present but forbidden."
    if kind == "source_unstable_termination_target":
        return (
            f"Required termination target {certificate.get('target')!r} admits a "
            "source-level nonterminating continuation."
        )
    if kind == "reachable_deadlock":
        return (
            f"Source state {certificate.get('target')!r} is reachable, non-final, "
            "and has no enabled continuation in the certified fragment."
        )
    if kind == "concurrent_region_deadlock":
        return (
            f"Source state {certificate.get('target')!r} is one member of a "
            "reachable orthogonal entry configuration whose active non-final "
            "states and ancestors have no enabled continuation."
        )
    if kind == "source_entry_deadlock":
        return (
            f"Source composite {certificate.get('scope')!r} is reachable but has "
            "no default child entry or inherited continuation; its exact compiler "
            "fail-closed state is deadlocked."
        )
    return None


def build_finding_records(outcomes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build one independently adjudicated record per cause-obligation facet."""

    findings: dict[str, dict[str, Any]] = {}
    w_rank = {"W0": 0, "W1": 1, "W2": 2}
    for outcome in outcomes:
        candidate = outcome.get("candidate", {})
        candidate = candidate if isinstance(candidate, dict) else {}
        groups = [
            group
            for group in outcome.get("probe_groups", [])
            if isinstance(group, dict) and _group_is_issue_candidate(group)
        ]
        for group in groups:
            key = _finding_key(outcome, group)
            level = _derive_witness_level(candidate, group)
            record = findings.setdefault(
                key,
                {
                    "finding_key": key,
                    "witness_level": level,
                    "l_level": _infer_l_level(candidate, group),
                    "basis_kind": candidate.get("basis_kind"),
                    "bases": [],
                    "nl_anchor_valid": outcome.get("nl_anchor_valid"),
                    "claims": [],
                    "model_claims": [],
                    "obligations": [],
                    "nl_quotes": [],
                    "locations": [],
                    "source_attribution": [],
                    "evidence_status": "coverage_gap",
                    "coverage_gap_reasons": [],
                    "formal_oracle_rules": [],
                    "formal_goals": [],
                    "counterexample_found": False,
                    "compiled_assertions": [],
                    "execution_certificates": [],
                    "source_causality_certificate": None,
                    "domain_obligations": [],
                    "candidate_indices": [],
                    "probe_group_ids": [],
                    "d_decision": None,
                    "d_validation_errors": [],
                },
            )
            if w_rank.get(str(level), 0) > w_rank.get(str(record["witness_level"]), 0):
                record["witness_level"] = level
            model_claim = (group or {}).get("claim") or candidate.get("claim")
            record["model_claims"].append(model_claim)
            if candidate.get("basis"):
                record["bases"].append(candidate["basis"])
            certificate = (group or {}).get("source_causality_certificate")
            canonical_claim = (
                _canonical_source_fact(certificate)
                if isinstance(certificate, dict)
                else None
            )
            record["claims"].append(canonical_claim or model_claim)
            record["obligations"].append(candidate.get("obligation"))
            if candidate.get("nl_quote"):
                record["nl_quotes"].append(candidate["nl_quote"])
            if isinstance(candidate.get("formal_oracle_rule"), dict):
                rule = candidate["formal_oracle_rule"]
                if all(
                    existing.get("rule_id") != rule.get("rule_id")
                    for existing in record["formal_oracle_rules"]
                    if isinstance(existing, dict)
                ):
                    record["formal_oracle_rules"].append(rule)
            goal = candidate.get("goal")
            if isinstance(goal, dict) and all(
                _canonical_sha256(existing) != _canonical_sha256(goal)
                for existing in record["formal_goals"]
            ):
                record["formal_goals"].append(goal)
            domain_obligation = candidate.get("domain_obligation")
            if isinstance(domain_obligation, dict) and all(
                _canonical_sha256(existing) != _canonical_sha256(domain_obligation)
                for existing in record["domain_obligations"]
            ):
                record["domain_obligations"].append(domain_obligation)
            record["locations"].extend(candidate.get("locations", []))
            source_status = (group or {}).get("source_attribution", {}).get("status")
            if source_status:
                record["source_attribution"].append(source_status)
            record["counterexample_found"] = bool(
                record["counterexample_found"]
                or (group or {}).get("counterexample_found")
            )
            if group.get("counterexample_found"):
                record["evidence_status"] = "executed_counterexample"
            elif group.get("error"):
                record["coverage_gap_reasons"].append(str(group["error"]))
            elif isinstance(group.get("execution_certificate"), dict):
                verdict = group["execution_certificate"].get("verdict")
                if verdict == "inconclusive":
                    record["coverage_gap_reasons"].append(
                        "compiled execution returned inconclusive"
                    )
            else:
                record["coverage_gap_reasons"].append(
                    "no executable consequence was compiled"
                )
            if (group or {}).get("compiled_assertion"):
                record["compiled_assertions"].append(group["compiled_assertion"])
            if (group or {}).get("execution_certificate"):
                record["execution_certificates"].append(group["execution_certificate"])
            if isinstance(certificate, dict):
                record["source_causality_certificate"] = certificate
            record["candidate_indices"].append(outcome.get("candidate_index"))
            if (group or {}).get("group_id"):
                record["probe_group_ids"].append(group["group_id"])

    for finding in findings.values():
        for field in (
            "claims",
            "model_claims",
            "bases",
            "obligations",
            "nl_quotes",
            "locations",
            "source_attribution",
            "coverage_gap_reasons",
            "candidate_indices",
            "probe_group_ids",
        ):
            finding[field] = list(
                dict.fromkeys(item for item in finding[field] if item not in {None, ""})
            )
        finding["w_validation_errors"] = validate_witness_record(finding)
    return list(findings.values())


def validate_witness_record(finding: dict[str, Any]) -> list[str]:
    """Mechanically enforce that W2 means an assertion actually ran."""

    level = finding.get("witness_level")
    certificates = [
        item
        for item in finding.get("execution_certificates", [])
        if isinstance(item, dict)
    ]
    terminal_counterexamples = [
        item
        for item in certificates
        if item.get("terminal") is True
        and item.get("verdict") == "counterexample"
        and item.get("counterexample_found") is True
        and isinstance(item.get("evaluated_artifact_sha256"), str)
        and isinstance(item.get("compiled_assertion_sha256"), str)
        and _valid_semantic_binding_receipt(item)
    ]
    if level == "W2":
        return (
            []
            if terminal_counterexamples
            else [
                "W2 requires a terminal counterexample certificate with artifact/assertion hashes and an exact-policy semantic-binding receipt"
            ]
        )
    if terminal_counterexamples:
        return [f"{level} cannot retain a valid terminal counterexample certificate"]
    if level not in {"W1", "W0"}:
        return [f"unknown witness level: {level!r}"]
    return []


def _language_clause_for_finding(finding: dict[str, Any]) -> dict[str, Any] | None:
    certificate = finding.get("source_causality_certificate")
    certificate = certificate if isinstance(certificate, dict) else {}
    kind = certificate.get("kind")
    if kind == "initial_contract_violation":
        return {
            "clause_id": "UML_INITIAL_NO_TRIGGER_OR_GUARD",
            "text": "An outgoing transition from an initial pseudostate must not have a trigger or guard.",
            "antecedent_established": bool(certificate.get("initial_edges")),
            "violation_established": certificate.get("verdict") == "counterexample",
            "evidence_refs": ["source_certificate.initial_edges"],
        }
    if (
        kind == "source_initial_target_contract"
        and certificate.get("target_is_direct_child") is False
    ):
        return {
            "clause_id": "UML_INITIAL_TARGET_SAME_REGION",
            "text": "An outgoing transition from an initial pseudostate must target a vertex in the same region.",
            "antecedent_established": bool(certificate.get("initial_edges")),
            "violation_established": True,
            "evidence_refs": [
                "source_certificate.actual_parent",
                "source_certificate.target_is_direct_child",
            ],
        }
    if kind == "source_guarded_completion_unfireable":
        return {
            "clause_id": "UML251_DERIVED_GUARDED_COMPLETION",
            "text": (
                "Under the declared UML 2.5.1-derived profile, a transition with "
                "no explicit trigger and a guard has an implicit completion "
                "trigger; a composite state cannot generate that completion "
                "while its region has no final-state exit."
            ),
            "antecedent_established": certificate.get("assertion_executed") is True,
            "violation_established": certificate.get("verdict") == "counterexample",
            "evidence_refs": [
                "source_certificate.label_profile",
                "source_certificate.final_edges",
            ],
        }
    return None


def _compact_transition_for_d(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    return {
        key: value.get(key)
        for key in ("id", "source", "target", "event", "guard", "action", "raw_ref")
        if value.get(key) is not None
    }


def _compact_source_certificate_for_d(
    certificate: dict[str, Any],
) -> dict[str, Any] | None:
    keys = (
        "kind",
        "verdict",
        "sound_for_claim",
        "target",
        "scope",
        "owner_scope",
        "source",
        "state",
        "child",
        "composite",
        "expected_parent",
        "actual_parent",
        "actual_ancestor_chain",
        "within_expected_ancestor",
        "component",
        "observed_transition_id",
        "reference_transition_id",
        "normative_target",
        "observed_target",
        "reference_target",
        "reference_supports_normative_target",
        "forbidden_scope",
        "target_ancestor_chain",
        "state_path",
        "transition_path",
        "ancestor_chain",
        "continuing_transitions",
        "reachable",
        "source_reachable",
        "active_scopes_checked",
        "consumers",
        "consumers_by_scope",
        "aggregate_consumers",
        "reachable_consumers",
        "blocking_scope",
        "missing_scope_ids",
        "unreachable_scope_ids",
        "coverage_actual",
        "scope_applicability",
        "required_scope_ids",
        "explicit_final",
        "root_final_edge_count",
        "cross_component_incoming",
        "initial_edge_count",
        "matching_edge_count",
        "attempted_entry_edge_count",
        "attempted_entry_edges",
        "scope_supports_initial",
        "target_is_direct_child",
        "direct_children",
        "blocked_region_targets",
        "region_entry_receipts",
        "compiler_causal_bridge",
        "expected_state",
        "actual_state",
        "expected_final_target",
        "final_edges",
        "label_profile",
        "fcstm_projection_audit",
        "assertion_executed",
        "actual",
        "expected",
        "phase",
        "action",
        "evidence",
        "assumptions",
    )
    compact = {
        key: certificate.get(key) for key in keys if certificate.get(key) is not None
    }
    if certificate.get("observed_transition") is not None:
        compact["observed_transition"] = _compact_transition_for_d(
            certificate["observed_transition"]
        )
    if certificate.get("reference_transition") is not None:
        compact["reference_transition"] = _compact_transition_for_d(
            certificate["reference_transition"]
        )
    for key in (
        "outgoing",
        "continuing_transitions",
        "root_final_edges",
        "initial_edges",
        "matching_transitions",
    ):
        rows = certificate.get(key)
        if isinstance(rows, list):
            compact[key] = [_compact_transition_for_d(item) for item in rows[:8]]
    evidence = certificate.get("evidence")
    if isinstance(evidence, dict) and certificate.get("kind") == "source_guard_overlap":
        compact["guard_overlap_pairs"] = evidence.get("pairs", [])[:3]
    return compact or None


def _source_entry_semantics_for_d(pair: dict[str, Any]) -> dict[str, Any]:
    """Expose typed parent-entry facts without asking the judge to infer them."""

    model = _source_model(pair)
    states = [
        item
        for item in model.get("states", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    transitions = [
        item
        for item in model.get("transitions", [])
        if isinstance(item, dict)
        and item.get("attributes", {}).get("transition_kind") == "initial"
    ]
    state_ids = {str(item["id"]) for item in states}
    scopes: list[dict[str, Any]] = []
    for scope in sorted(states, key=lambda item: str(item["id"])):
        scope_id = str(scope["id"])
        direct_children = sorted(
            str(item["id"]) for item in states if item.get("parent") == scope_id
        )
        if not direct_children:
            continue
        scope_initials = sorted(
            str(item["id"]) for item in transitions if item.get("scope") == scope_id
        )
        child_initials = {
            child: sorted(
                str(item["id"]) for item in transitions if item.get("scope") == child
            )
            for child in direct_children
        }
        scopes.append(
            {
                "scope": scope_id,
                "scope_initial_transition_ids": scope_initials,
                "direct_children": direct_children,
                "child_scope_initial_transition_ids": child_initials,
            }
        )
    concurrent_regions = model.get("concurrent_regions")
    concurrent_regions = (
        concurrent_regions if isinstance(concurrent_regions, list) else []
    )
    return {
        "declared_concurrent_regions": concurrent_regions,
        "declared_concurrent_region_count": len(concurrent_regions),
        "state_ids_with_exact_parent": sorted(state_ids),
        "scope_entry_semantics": scopes,
    }


def d_finding_sort_key(finding: dict[str, Any]) -> tuple[int, int, str]:
    """Put reusable executed evidence before weaker semantic restatements."""

    w_rank = {"W2": 0, "W1": 1, "W0": 2}
    certificate = finding.get("source_causality_certificate")
    certified_rank = (
        0
        if isinstance(certificate, dict)
        and certificate.get("verdict") == "counterexample"
        else 1
    )
    return (
        w_rank.get(str(finding.get("witness_level")), 3),
        certified_rank,
        str(finding.get("finding_key") or ""),
    )


def _d_normative_basis(finding: dict[str, Any]) -> dict[str, Any]:
    """Project supplied normative provenance without interpreting its prose."""

    obligations = finding.get("obligations")
    obligations = obligations if isinstance(obligations, list) else []
    nl_quotes = finding.get("nl_quotes")
    nl_quotes = nl_quotes if isinstance(nl_quotes, list) else []
    return {
        "basis_kind": finding.get("basis_kind"),
        "obligation": next((item for item in obligations if item), None),
        "nl_quote": next((item for item in nl_quotes if item), None),
        "nl_anchor_valid": finding.get("nl_anchor_valid"),
        "domain_obligations": _domain_obligations_for_finding(finding),
        "language_clause": _language_clause_for_finding(finding),
    }


def _d_applicability_reason(finding: dict[str, Any]) -> dict[str, Any] | None:
    """Expose supplied applicability material, leaving its truth to the judge."""

    bases = finding.get("bases")
    bases = bases if isinstance(bases, list) else []
    oracle_rules = finding.get("formal_oracle_rules")
    oracle_rules = oracle_rules if isinstance(oracle_rules, list) else []
    conditions = [
        rule.get("applicability")
        for rule in oracle_rules
        if isinstance(rule, dict) and rule.get("applicability")
    ]
    candidate_basis = next((item for item in bases if item), None)
    if candidate_basis is None and not conditions:
        return None
    return {
        "candidate_basis": candidate_basis,
        "formal_oracle_applicability_conditions": conditions,
        "semantic_applicability_established": None,
    }


def _d_formal_fact(
    finding: dict[str, Any], source_certificate: dict[str, Any]
) -> dict[str, Any] | None:
    """Expose only facts carried by typed certificates or oracle receipts."""

    oracle_rules = finding.get("formal_oracle_rules")
    oracle_rules = oracle_rules if isinstance(oracle_rules, list) else []
    oracle_facts = [
        {
            "rule_id": rule.get("rule_id"),
            "diagnostic_code": rule.get("diagnostic_code"),
            "formal_fact": rule.get("formal_fact"),
        }
        for rule in oracle_rules
        if isinstance(rule, dict) and rule.get("formal_fact")
    ]
    source_fact = _canonical_source_fact(source_certificate)
    if source_fact is None and not oracle_facts:
        return None
    return {
        "canonical_source_fact": source_fact,
        "formal_oracle_facts": oracle_facts,
    }


def _mechanical_d_provenance_ceiling(finding: dict[str, Any]) -> dict[str, Any]:
    """Bound D2 provenance mechanically; never decide semantic applicability."""

    admissible_d2_groundings: list[str] = []
    nl_quotes = finding.get("nl_quotes")
    if finding.get("nl_anchor_valid") is True and isinstance(nl_quotes, list) and any(
        nl_quotes
    ):
        admissible_d2_groundings.append("lit")
    language_clause = _language_clause_for_finding(finding)
    if (
        isinstance(language_clause, dict)
        and language_clause.get("antecedent_established") is True
        and language_clause.get("violation_established") is True
    ):
        admissible_d2_groundings.append("lang")
    if _protocol_d2_grounding(finding) == "impl":
        admissible_d2_groundings.append("impl")
    if _has_typed_operational_domain_norm(finding):
        admissible_d2_groundings.append("dom")
    return {
        "level": "D2" if admissible_d2_groundings else "D1",
        "admissible_d2_groundings": admissible_d2_groundings,
        "semantic_d_decision_claimed": False,
    }


def build_d_context(pair: dict[str, Any], findings: list[dict[str, Any]]) -> str:
    compact = []
    ordered_findings = sorted(findings, key=d_finding_sort_key)
    for finding_ordinal, finding in enumerate(ordered_findings, start=1):
        source_certificate = finding.get("source_causality_certificate")
        source_certificate = (
            source_certificate if isinstance(source_certificate, dict) else {}
        )
        duplicate_eligible_earlier_keys = [
            str(earlier["finding_key"])
            for earlier in ordered_findings[: finding_ordinal - 1]
            if not validate_duplicate_reference(finding, earlier)
        ]
        compact.append(
            {
                "finding_ordinal": finding_ordinal,
                "finding_key": finding["finding_key"],
                "normative_basis": _d_normative_basis(finding),
                "applicability_reason": _d_applicability_reason(finding),
                "formal_fact": _d_formal_fact(finding, source_certificate),
                "source_certificate": _compact_source_certificate_for_d(
                    source_certificate
                ),
                "strongest_defeater": None,
                "defeater_disposition": None,
                "alternative_reading": None,
                "mechanical_d_provenance_ceiling": (
                    _mechanical_d_provenance_ceiling(finding)
                ),
                "basis_kind": finding.get("basis_kind"),
                "basis": next(iter(finding.get("bases", [])), None),
                "claim": next(iter(finding.get("claims", [])), None),
                "obligation": next(iter(finding.get("obligations", [])), None),
                "domain_obligations": _domain_obligations_for_finding(finding),
                "nl_quote": next(iter(finding.get("nl_quotes", [])), None),
                "evidence_status": finding.get("evidence_status"),
                "source_attribution": finding.get("source_attribution", []),
                "protocol_d2_grounding": _protocol_d2_grounding(finding),
                "language_clause": _language_clause_for_finding(finding),
                "formal_oracle_rules": finding.get("formal_oracle_rules", []),
                "formal_goals": finding.get("formal_goals", []),
                "duplicate_eligible_earlier_keys": duplicate_eligible_earlier_keys,
            }
        )
    source_state_inventory = [
        {
            "id": state.get("id"),
            "parent": state.get("parent"),
            "kind": state.get("kind"),
        }
        for state in _source_model(pair).get("states", [])
        if isinstance(state, dict)
    ]
    source_transition_inventory = [
        _compact_transition_for_d(transition)
        for transition in _source_model(pair).get("transitions", [])
        if isinstance(transition, dict)
    ]
    source_entry_semantics = _source_entry_semantics_for_d(pair)
    return (
        "# Natural-language requirements\n\n"
        f"{_numbered(pair['nl'], 'NL')}\n\n"
        "# Exact source state inventory\n\n"
        f"{json.dumps(source_state_inventory, ensure_ascii=False, sort_keys=True, separators=(',', ':'))}\n\n"
        "# Exact source transition inventory\n\n"
        f"{json.dumps(source_transition_inventory, ensure_ascii=False, sort_keys=True, separators=(',', ':'))}\n\n"
        "# Typed source entry semantics\n\n"
        "The following facts come from the canonical source AST. An initial transition is scoped to the exact composite named by its `scope`; an initial transition scoped to a child does not satisfy the parent scope's entry obligation. `declared_concurrent_regions` is the only authoritative concurrency inventory; an empty list means that no concurrent-region entry interpretation is available for this source artifact.\n\n"
        f"{json.dumps(source_entry_semantics, ensure_ascii=False, sort_keys=True, separators=(',', ':'))}\n\n"
        "# Findings to adjudicate\n\n"
        f"{json.dumps(compact, ensure_ascii=False, sort_keys=True, separators=(',', ':'))}\n"
    )


def _domain_obligations_for_finding(finding: dict[str, Any]) -> list[dict[str, Any]]:
    """Return only typed domain obligations carried by the finding dossier."""

    rows = finding.get("domain_obligations")
    if not isinstance(rows, list):
        rows = []
    singular = finding.get("domain_obligation")
    if isinstance(singular, dict):
        rows = [*rows, singular]
    return [row for row in rows if isinstance(row, dict)]


def _has_typed_operational_domain_norm(finding: dict[str, Any]) -> bool:
    """Recognize only the preregistered typed operational norm surface."""

    certificate = finding.get("source_causality_certificate")
    certificate = certificate if isinstance(certificate, dict) else {}
    certificate_target = certificate.get("target")
    for obligation in _domain_obligations_for_finding(finding):
        if (
            obligation.get("family") != "graph"
            or obligation.get("property") not in {"deadlock_free", "escapable"}
            or obligation.get("expected", True) is not True
        ):
            continue
        formal_refs = {
            str(obligation.get(field))
            for field in ("source_ref", "target_ref")
            if isinstance(obligation.get(field), str)
            and str(obligation.get(field)).strip()
        }
        if not formal_refs or (
            isinstance(certificate_target, str)
            and certificate_target not in formal_refs
        ):
            continue
        return True
    return False


def _has_closed_d2_impl_receipt(finding: dict[str, Any]) -> bool:
    certificate = finding.get("source_causality_certificate")
    certificate = certificate if isinstance(certificate, dict) else {}
    assumptions = certificate.get("assumptions")
    assumptions = assumptions if isinstance(assumptions, dict) else {}
    if not (
        finding.get("witness_level") == "W2"
        and certificate.get("verdict") == "counterexample"
        and certificate.get("explicit_final") is False
    ):
        return False
    kind = certificate.get("kind")
    if kind == "reachable_deadlock":
        return assumptions.get("no_concurrent_regions") is True
    if kind == "concurrent_region_deadlock":
        required = {
            "all_regions_have_one_initial",
            "all_region_initials_unconditional",
            "all_active_targets_leaf",
            "all_active_targets_nonfinal",
            "entry_path_has_no_guards",
            "no_enabled_outgoing",
            "owner_identity_resolved_exactly",
            "target_is_active_region_entry",
        }
        return all(assumptions.get(key) is True for key in required)
    if kind == "source_entry_deadlock":
        required = {
            "source_scope_reachable",
            "entry_path_has_no_guards",
            "missing_source_initial",
            "source_has_direct_children",
            "no_inherited_outgoing",
            "compiler_bridge_exact",
            "compiler_bridge_transition_target_exact",
            "no_concurrent_regions",
        }
        return all(assumptions.get(key) is True for key in required)
    return False


def validate_d_decision(finding: dict[str, Any], decision: DDecision) -> list[str]:
    errors: list[str] = []
    if decision.d_level == "D2" and decision.d_subclass == "not_applicable":
        errors.append("D2 requires a D2 subclass")
    if decision.d_level != "D2" and decision.d_subclass != "not_applicable":
        errors.append("D1/D0 require d_subclass=not_applicable")
    if decision.d_subclass == "D2-lit":
        if decision.grounding == "lit":
            quotes = finding.get("nl_quotes", [])
            if not finding.get("nl_anchor_valid") or not quotes:
                errors.append("literal D2-lit requires an exact NL quote")
        elif decision.grounding == "lang":
            clause = _language_clause_for_finding(finding)
            if not (
                isinstance(clause, dict)
                and clause.get("antecedent_established") is True
                and clause.get("violation_established") is True
            ):
                errors.append(
                    "language D2-lit requires an applicable violated language-clause receipt"
                )
        else:
            errors.append("D2-lit requires grounding=lit or grounding=lang")
    if decision.d_subclass == "D2-impl":
        if decision.grounding != "impl":
            errors.append("D2-impl requires grounding=impl")
        if not _has_closed_d2_impl_receipt(finding):
            errors.append(
                "grounding=impl is forbidden because protocol_d2_grounding is null; "
                "use the supplied literal/language/domain provenance or lower D"
            )
    if decision.d_subclass == "D2-norm":
        if decision.grounding != "dom":
            errors.append("D2-norm requires grounding=dom")
        elif not _has_typed_operational_domain_norm(finding):
            errors.append("D2-norm requires a typed operational domain obligation")
    if decision.d_level == "D2" and decision.defeater_disposition != "defeated":
        errors.append("D2 requires the strongest defeater to be defeated")
    if decision.d_level == "D1" and not (
        decision.defeater_kind == "undercutting"
        and decision.defeater_disposition in {"survives", "unresolved"}
    ):
        errors.append("D1 requires a surviving or unresolved undercutting defeater")
    if decision.d_level == "D1" and decision.grounding == "none":
        errors.append("D1 requires a grounded first reading")
    if decision.d_level == "D0" and decision.defeater_disposition not in {
        "survives",
        "unresolved",
    }:
        errors.append("D0 requires a surviving or unresolved defeater")
    if (
        decision.d_level == "D0"
        and decision.defeater_kind == "rebutting"
        and decision.defeater_disposition != "survives"
    ):
        errors.append("D0 rebutting defeater must survive")
    return errors


def _typed_source_certificate_cause_identity(
    finding: dict[str, Any],
) -> str | None:
    """Return a fail-closed identity for a deterministic source certificate."""

    certificate = finding.get("source_causality_certificate")
    if not isinstance(certificate, dict):
        return None
    cause_key = _certificate_cause_key(certificate)
    if cause_key is None:
        return None
    return _canonical_sha256(
        {
            "cause_key": cause_key,
            "certificate": certificate,
        }
    )


def _canonical_formal_property_signature(
    finding: dict[str, Any],
) -> tuple[str, ...] | None:
    """Return a complete executable-property signature or no duplicate proof."""

    formal_goals = finding.get("formal_goals")
    if not isinstance(formal_goals, list) or not formal_goals:
        return None
    signatures = set()
    for goal in formal_goals:
        if not isinstance(goal, dict):
            return None
        try:
            typed_goal = EvidenceGoal.model_validate(goal)
        except ValidationError:
            return None
        if compile_evidence_goal(typed_goal)["errors"]:
            return None
        signatures.add(
            _canonical_sha256(typed_goal.model_dump(mode="json", exclude_none=True))
        )
    return tuple(sorted(signatures)) or None


def validate_duplicate_reference(
    finding: dict[str, Any], earlier: dict[str, Any]
) -> list[str]:
    """Require matching typed cause and executable-property proof to deduplicate."""

    cause_identity = _typed_source_certificate_cause_identity(finding)
    earlier_cause_identity = _typed_source_certificate_cause_identity(earlier)
    if cause_identity is None or earlier_cause_identity is None:
        return [
            "duplicate_of requires positive typed source-certificate cause identity for both findings"
        ]
    if cause_identity != earlier_cause_identity:
        return [
            "duplicate_of conflicts with distinct exact source-certificate cause keys"
        ]
    property_signature = _canonical_formal_property_signature(finding)
    earlier_property_signature = _canonical_formal_property_signature(earlier)
    if property_signature is None or earlier_property_signature is None:
        return [
            "duplicate_of requires a canonical formal-property signature for both findings"
        ]
    if property_signature != earlier_property_signature:
        return ["duplicate_of conflicts with distinct exact formal property signatures"]

    return []


def _protocol_d2_grounding(finding: dict[str, Any]) -> str | None:
    """Return a closed #189 subclass only from typed formal evidence."""

    return "impl" if _has_closed_d2_impl_receipt(finding) else None


def normalize_d_decision(
    decision: DDecision, finding: dict[str, Any] | None = None
) -> DDecision:
    """Derive redundant D2 taxonomy fields without interpreting prose."""

    if decision.d_level != "D2":
        subclass: DSubclass = "not_applicable"
        grounding = decision.grounding
    else:
        typed_domain_norm = bool(
            isinstance(finding, dict) and _has_typed_operational_domain_norm(finding)
        )
        grounding = (
            decision.grounding
            if decision.grounding == "dom" and typed_domain_norm
            else (
                _protocol_d2_grounding(finding) if isinstance(finding, dict) else None
            )
            or decision.grounding
        )
        subclass = {
            "lit": "D2-lit",
            "lang": "D2-lit",
            "impl": "D2-impl",
            "dom": "D2-norm",
        }.get(grounding, "not_applicable")
    return decision.model_copy(update={"grounding": grounding, "d_subclass": subclass})


def apply_d_adjudication(
    findings: list[dict[str, Any]], plan: DAdjudicationPlan
) -> list[dict[str, Any]]:
    by_key: dict[str, DDecision] = {}
    duplicates: set[str] = set()
    for decision in plan.decisions:
        if decision.finding_key in by_key:
            duplicates.add(decision.finding_key)
        by_key[decision.finding_key] = decision
    expected = {finding["finding_key"] for finding in findings}
    supplied = set(by_key)
    if duplicates or expected != supplied:
        raise ValueError(
            "D adjudication must cover each finding exactly once; "
            f"missing={sorted(expected - supplied)} unexpected={sorted(supplied - expected)} "
            f"duplicates={sorted(duplicates)}"
        )
    findings_by_key = {str(finding["finding_key"]): finding for finding in findings}
    ordered_keys = [
        str(finding["finding_key"])
        for finding in sorted(findings, key=d_finding_sort_key)
    ]
    finding_positions = {
        finding_key: index for index, finding_key in enumerate(ordered_keys)
    }
    adjudicated = []
    for finding in findings:
        decision = normalize_d_decision(by_key[finding["finding_key"]], finding=finding)
        item = dict(finding)
        item["d_decision"] = decision.model_dump(mode="json")
        duplicate_errors: list[str] = []
        duplicate_of = decision.duplicate_of
        if duplicate_of is not None:
            if duplicate_of not in findings_by_key:
                duplicate_errors.append(
                    "duplicate_of must reference a supplied finding_key"
                )
            elif (
                finding_positions[duplicate_of]
                >= finding_positions[str(finding["finding_key"])]
            ):
                duplicate_errors.append(
                    "duplicate_of must reference an earlier stable finding_key"
                )
            else:
                duplicate_errors.extend(
                    validate_duplicate_reference(finding, findings_by_key[duplicate_of])
                )
            if not decision.duplicate_rationale:
                duplicate_errors.append("duplicate_of requires duplicate_rationale")
        elif decision.duplicate_rationale is not None:
            duplicate_errors.append("duplicate_rationale requires duplicate_of")
        item["d_validation_errors"] = [
            *validate_d_decision(finding, decision),
            *duplicate_errors,
        ]
        adjudicated.append(item)
    return adjudicated


def select_confirmed_issues(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    confirmed = []
    for finding in findings:
        decision = finding.get("d_decision")
        if not isinstance(decision, dict) or decision.get("d_level") != "D2":
            continue
        if finding.get("d_validation_errors"):
            continue
        if finding.get("w_validation_errors"):
            continue
        source_certificate = finding.get("source_causality_certificate")
        if (
            isinstance(source_certificate, dict)
            and source_certificate.get("sound_for_claim") is False
        ):
            continue
        if finding.get("witness_level") != "W2":
            continue
        source_statuses = set(finding.get("source_attribution", []))
        if not source_statuses.intersection(
            {
                "safe_runtime_path",
                "causal_dual_certificate",
                "source_direct_certificate",
            }
        ):
            continue
        item = dict(finding)
        item["release_status"] = "confirmed_issue"
        confirmed.append(item)
    return confirmed


def select_accepted_issues(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Release externally attributable D1 and D2 findings; retain D0 for audit."""

    accepted = []
    for finding in findings:
        decision = finding.get("d_decision")
        if not isinstance(decision, dict) or decision.get("d_level") not in {
            "D1",
            "D2",
        }:
            continue
        if finding.get("d_validation_errors") or finding.get("w_validation_errors"):
            continue
        source_certificate = finding.get("source_causality_certificate")
        if (
            isinstance(source_certificate, dict)
            and source_certificate.get("sound_for_claim") is False
        ):
            continue
        if finding.get("witness_level") == "W2" and not set(
            finding.get("source_attribution", [])
        ).intersection(
            {
                "safe_runtime_path",
                "causal_dual_certificate",
                "source_direct_certificate",
            }
        ):
            continue
        item = dict(finding)
        item["release_status"] = (
            "accepted_issue"
            if decision.get("d_level") == "D2" and finding.get("witness_level") == "W2"
            else "provisional_issue"
        )
        accepted.append(item)
    return accepted


_LEVEL_RANK = {
    "W0": 0,
    "W1": 1,
    "W2": 2,
    "D0": 0,
    "D1": 1,
    "D2": 2,
    "L0": 0,
    "L1": 1,
    "L2": 2,
}


def _cause_key_from_finding(finding: dict[str, Any]) -> str:
    key = str(finding.get("finding_key") or "")
    return key.rsplit(":facet:", 1)[0] if ":facet:" in key else key


def _facet_report_rank(finding: dict[str, Any]) -> tuple[int, int, int, int]:
    decision = finding.get("d_decision")
    decision = decision if isinstance(decision, dict) else {}
    valid = not finding.get("d_validation_errors") and not finding.get(
        "w_validation_errors"
    )
    source_safe = bool(
        set(finding.get("source_attribution", [])).intersection(
            {
                "causal_dual_certificate",
                "source_direct_certificate",
                "safe_runtime_path",
            }
        )
    )
    return (
        int(valid),
        _LEVEL_RANK.get(str(decision.get("d_level")), -1),
        _LEVEL_RANK.get(str(finding.get("witness_level")), -1),
        int(source_safe),
    )


def _strongest_level(values: list[str], prefix: str) -> str | None:
    candidates = [value for value in values if value.startswith(prefix)]
    return max(candidates, key=lambda item: _LEVEL_RANK.get(item, -1), default=None)


def build_report_issue_clusters(
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Collapse exact causes, then consume validated D duplicate relations."""

    findings_by_key = {str(finding.get("finding_key")): finding for finding in findings}
    cause_by_finding = {
        str(finding.get("finding_key")): _cause_key_from_finding(finding)
        for finding in findings
    }
    parent = {cause_key: cause_key for cause_key in cause_by_finding.values()}

    def root(cause_key: str) -> str:
        while parent[cause_key] != cause_key:
            parent[cause_key] = parent[parent[cause_key]]
            cause_key = parent[cause_key]
        return cause_key

    deduplicated_by_d: list[dict[str, str]] = []
    finding_positions = {
        str(finding.get("finding_key")): index
        for index, finding in enumerate(sorted(findings, key=d_finding_sort_key))
    }
    for finding in findings:
        finding_key = str(finding.get("finding_key"))
        decision = finding.get("d_decision")
        duplicate_of = (
            decision.get("duplicate_of") if isinstance(decision, dict) else None
        )
        if (
            finding.get("d_validation_errors")
            or not isinstance(duplicate_of, str)
            or duplicate_of not in cause_by_finding
            or findings_by_key[duplicate_of].get("d_validation_errors")
            or finding_positions[duplicate_of] >= finding_positions[finding_key]
            or validate_duplicate_reference(
                finding,
                findings_by_key[duplicate_of],
            )
        ):
            continue
        source_cause = root(cause_by_finding[finding_key])
        target_cause = root(cause_by_finding[duplicate_of])
        if source_cause == target_cause:
            continue
        parent[source_cause] = target_cause
        deduplicated_by_d.append(
            {
                "finding_key": finding_key,
                "duplicate_of": duplicate_of,
                "source_cause_key": source_cause,
                "target_cause_key": target_cause,
            }
        )

    grouped: dict[str, list[dict[str, Any]]] = {}
    for finding in findings:
        cause_key = root(cause_by_finding[str(finding.get("finding_key"))])
        grouped.setdefault(cause_key, []).append(finding)

    clusters = []
    for cause_key, facets in grouped.items():
        cause_keys = list(
            dict.fromkeys(_cause_key_from_finding(facet) for facet in facets)
        )
        duplicate_receipts = [
            item
            for item in deduplicated_by_d
            if root(item["target_cause_key"]) == cause_key
        ]
        representative = max(facets, key=_facet_report_rank)
        confirmed_facets = select_confirmed_issues(facets)
        accepted_facets = select_accepted_issues(facets)
        valid_d_levels = [
            str(facet.get("d_decision", {}).get("d_level"))
            for facet in facets
            if isinstance(facet.get("d_decision"), dict)
            and not facet.get("d_validation_errors")
        ]
        release_status = (
            "confirmed_report_issue"
            if confirmed_facets
            else "provisional_report_issue"
            if accepted_facets
            else "audit_only"
        )
        clusters.append(
            {
                "schema": "paper1.report_issue_cluster.v1",
                "report_issue_id": cause_key,
                "cause_key": cause_key,
                "cause_keys": cause_keys,
                "deduplicated_by_d": duplicate_receipts,
                "representative_finding_key": representative["finding_key"],
                "facet_keys": [facet["finding_key"] for facet in facets],
                "facet_count": len(facets),
                "confirmed_facet_keys": [
                    facet["finding_key"] for facet in confirmed_facets
                ],
                "accepted_facet_keys": [
                    facet["finding_key"] for facet in accepted_facets
                ],
                "claims": list(
                    dict.fromkeys(
                        claim for facet in facets for claim in facet.get("claims", [])
                    )
                ),
                "obligations": list(
                    dict.fromkeys(
                        obligation
                        for facet in facets
                        for obligation in facet.get("obligations", [])
                    )
                ),
                "nl_quotes": list(
                    dict.fromkeys(
                        quote
                        for facet in facets
                        for quote in facet.get("nl_quotes", [])
                    )
                ),
                "locations": list(
                    dict.fromkeys(
                        location
                        for facet in facets
                        for location in facet.get("locations", [])
                    )
                ),
                "witness_level": _strongest_level(
                    [str(facet.get("witness_level")) for facet in facets], "W"
                ),
                "d_level": _strongest_level(valid_d_levels, "D"),
                "l_level": _strongest_level(
                    [str(facet.get("l_level")) for facet in facets], "L"
                ),
                "source_attribution": list(
                    dict.fromkeys(
                        status
                        for facet in facets
                        for status in facet.get("source_attribution", [])
                    )
                ),
                "facet_d_levels": {
                    facet["finding_key"]: (
                        facet.get("d_decision", {}).get("d_level")
                        if isinstance(facet.get("d_decision"), dict)
                        else None
                    )
                    for facet in facets
                },
                "release_status": release_status,
            }
        )
    return clusters


def select_confirmed_report_issues(
    clusters: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        cluster
        for cluster in clusters
        if cluster.get("release_status") == "confirmed_report_issue"
    ]


def select_accepted_report_issues(
    clusters: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        cluster
        for cluster in clusters
        if cluster.get("release_status")
        in {"confirmed_report_issue", "provisional_report_issue"}
    ]


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    start_ns = time.perf_counter_ns()
    report_root = (
        Path(args.report_root).resolve() if args.report_root else DEFAULT_REPORT_ROOT
    )
    pair = load_pair(args.case, report_root)
    inspect = inspect_fcstm(
        pair["fcstm"],
        pair["paths"]["fcstm"],
        smt_timeout_ms=args.smt_timeout_ms,
    )
    seeds = derive_probe_seeds(inspect)
    context = build_context(pair, inspect, seeds)
    base_record: dict[str, Any] = {
        "schema": "paper1.witness_search_prototype.v3",
        "exploratory_only": True,
        "case": args.case,
        "pair_name": pair["pair_name"],
        "profile": args.profile,
        "inputs": {
            name: {
                "path": pair["paths"][name],
                "sha256": _sha256(pair[name]),
                "chars": len(pair[name]),
            }
            for name in ("nl", "plantuml", "fcstm")
        },
        "source_canonical": {
            "path": pair["paths"]["canonical"],
            "sha256": _sha256(
                json.dumps(pair["canonical"], ensure_ascii=False, sort_keys=True)
            ),
            "role": "deterministic_source_assertions_only_not_llm_context",
        },
        "inspect": compact_inspect(inspect),
        "capability_boundary": compact_capability_boundary(pair["working_contract"]),
        "probe_seeds": seeds,
        "system_prompt": SYSTEM_PROMPT,
        "context": context,
        "context_chars": len(context),
        "started_at": started.isoformat(),
    }
    if args.plan_file:
        saved = _load_json(Path(args.plan_file))
        plan_payload = saved.get("plan", saved)
        plan = ProbePlan.model_validate(plan_payload)
        base_record.update(
            {
                "status": "replay",
                "plan_source": str(Path(args.plan_file).resolve()),
                "plan": plan.model_dump(mode="json"),
                "outcomes": execute_plan(pair, inspect, plan, seeds),
                "llm": None,
            }
        )
    elif args.dry_run:
        base_record.update(
            {
                "status": "dry_run",
                "plan": None,
                "outcomes": [],
                "llm": None,
            }
        )
    else:
        responder = DirectStructuredResponder(
            args.profile,
            max_output_tokens=args.max_output_tokens,
            transport_retries=args.transport_retries,
            streaming=getattr(args, "streaming", None),
        )
        try:
            plan = responder.invoke_structured(
                role="witness_planner",
                schema=ProbePlan,
                system_prompt=SYSTEM_PROMPT,
                user_input=context,
            )
        # Provider adapters expose different exception types; every failed call
        # must still produce an auditable run record for this exploratory pair.
        except Exception as exc:  # noqa: BLE001
            observation = responder.take_last_observation()
            base_record.update(
                {
                    "status": "failed",
                    "failure_class": "provider_or_schema",
                    "failure": f"{type(exc).__name__}: {exc}",
                    "plan": None,
                    "outcomes": [],
                    "llm": _jsonable(observation),
                }
            )
        else:
            observation = responder.take_last_observation()
            base_record.update(
                {
                    "status": "completed",
                    "plan": plan.model_dump(mode="json"),
                    "outcomes": execute_plan(pair, inspect, plan, seeds),
                    "llm": _jsonable(observation),
                }
            )
    base_record["issue_clusters"] = build_issue_clusters(base_record["outcomes"])
    base_record["telemetry"] = {
        "planner_call_count": 0 if args.plan_file or args.dry_run else 1,
        "probe_group_attempt_count": sum(
            len(item.get("probe_groups", [])) for item in base_record["outcomes"]
        ),
        "raw_source_candidate_count": sum(
            bool(group.get("source_candidate"))
            for item in base_record["outcomes"]
            for group in item.get("probe_groups", [])
        ),
        "unique_issue_cluster_count": len(base_record["issue_clusters"]),
    }
    base_record["finished_at"] = datetime.now(timezone.utc).isoformat()
    base_record["elapsed_ms"] = (time.perf_counter_ns() - start_ns) / 1_000_000
    return base_record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True, help="four-digit pair id")
    parser.add_argument("--profile", default="gpt-5.5")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--report-root", default=None)
    parser.add_argument("--plan-file", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--smt-timeout-ms", type=int, default=3_000)
    parser.add_argument("--max-output-tokens", type=int, default=1_800)
    parser.add_argument(
        "--transport-retries", type=int, default=DEFAULT_TRANSPORT_RETRIES
    )
    stream_mode = parser.add_mutually_exclusive_group()
    stream_mode.add_argument(
        "--stream",
        dest="streaming",
        action="store_true",
        help="Use streaming responses (the default).",
    )
    stream_mode.add_argument(
        "--no-stream",
        dest="streaming",
        action="store_false",
        help="Use complete non-streaming responses.",
    )
    # Streaming is the default research transport; use ``--no-stream`` only
    # when a synchronous request is explicitly required for diagnostics.
    parser.set_defaults(streaming=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    record = run(args)
    output = Path(args.output_dir) / "record.json"
    _write_json(output, record)
    candidates = sum(
        bool(group.get("source_candidate"))
        for item in record["outcomes"]
        for group in item.get("probe_groups", [])
    )
    artifact_w2 = sum(
        group.get("witness_level") == "W2"
        for item in record["outcomes"]
        for group in item.get("probe_groups", [])
    )
    source_certificates = sum(
        group.get("source_causality_certificate") is not None
        for item in record["outcomes"]
        for group in item.get("probe_groups", [])
    )
    unique_clusters = len(record.get("issue_clusters", []))
    print(
        f"[{record['status']}] case={args.case} candidates={len(record['outcomes'])} "
        f"w2={artifact_w2} source_certificates={source_certificates} "
        f"source_candidates={candidates} unique_clusters={unique_clusters} "
        f"context_chars={record['context_chars']} -> {output}"
    )
    return 0 if record["status"] in {"completed", "dry_run", "replay"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
