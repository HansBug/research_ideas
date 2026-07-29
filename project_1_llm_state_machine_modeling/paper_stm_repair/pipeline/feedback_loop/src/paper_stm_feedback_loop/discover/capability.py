"""Evidence-capability metadata for deterministic mandatory-evidence decisions.

Why this module exists
----------------------
``verification_kind`` (``structure``/``behavior``/``property``) is a *semantic*
label an LLM assigns to a natural-language requirement.  ``MANDATORY_PRIMARY_
EVIDENCE_FAMILIES`` turns that label into a *procedural* obligation ("a
``property`` requirement must carry an ``fbmcq`` primary").  Those two axes are
not related by a function: a universally quantified claim can still be closed
by one exact static query, and a bounded formal query cannot observe facts that
live in the transition relation's syntax rather than in its executions.

Pair 0029 is the worked counterexample.  "The two shared-condition transitions
out of ``enter_hwy`` must be distinguishable" is universally quantified over
variable valuations, so both GPT-5.5 and Claude froze it as ``property``.  The
frozen contract then demanded an ``fbmcq`` primary.  But FBMCQ observes state
activity, termination, events, cases, action calls and typed variables over
bounded traces -- it cannot observe guard expressions at all, and on 0029 the
query does not even compile at ``bound >= 2``.  Meanwhile ``conflicting_targets``
decides exactly that proposition in single-digit milliseconds.

So instead of asking "what kind of requirement is this", this module asks "what
can this evidence function actually decide, and over what domain".  That second
question has an objective answer that lives in code, not in a model's reading of
a sentence, so it is stable across models and across reruns.

Design rules
------------
1. The table is an **allowlist**.  A function waives a mandatory family only
   when it is listed here with an explicit justification.  Unknown functions
   never waive anything.
2. Only ``decisive`` procedures may waive, and only for the verification kinds
   named in ``waives_mandatory_for``.
3. ``behavior`` is never waived.  A static query does not witness a runtime
   response, and the 0000 cold-start regression this contract was built to stop
   is a *coverage* failure that must keep being caught.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Protocol

from paper_stm_feedback_loop.assertions.predicate_api import (
    PSEUDO_INITIAL,
    is_placeholder_name,
)

from .dependencies import dependency_closure
from .predicates import EXISTENCE_PREDICATES

__all__ = [
    "EvidenceCapability",
    "fbmcq_non_vacuity_findings",
    "vacuous_sibling_conjunction",
    "bare_reachability_probe",
    "unresolved_model_references",
    "unresolved_reference_findings",
    "initialization_anchored_findings",
    "placeholder_bindings",
    "redundant_proposal_findings",
    "termination_proposal_findings",
    "CLAIM_SUBJECT_BINDINGS",
    "SCOPE_LOCAL_WAIVER",
    "declared_path_bindings",
    "source_omitting_response_calls",
    "SOURCE_SENSITIVE_PHASES",
    "BOUND_PATH_KWARGS",
    "EVIDENCE_CAPABILITY",
    "DECISIVE_COMPLETENESS",
    "called_evidence_functions",
    "mandatory_waiver",
]

#: Completeness levels that are strong enough to close an obligation alone.
DECISIVE_COMPLETENESS = frozenset({"decisive"})


@dataclass(frozen=True)
class EvidenceCapability:
    """What one frozen evidence function can decide, and how completely.

    :param decides: short slug of the proposition class the function settles.
    :param completeness: ``decisive`` (settles the proposition outright),
        ``bounded_decisive`` (settles it only up to a declared bound),
        ``witness`` (can only exhibit one configuration) or ``locator``
        (only points at model elements, never settles anything).
    :param quantification: the domain the decision already ranges over.
    :param waives_mandatory_for: verification kinds whose mandatory primary
        family this function may replace when it is used as a primary.
    :param justification: why the waiver is sound; required for audit.
    """

    decides: str
    completeness: str
    quantification: str
    waives_mandatory_for: frozenset[str] = field(default_factory=frozenset)
    justification: str = ""


EVIDENCE_CAPABILITY: dict[str, EvidenceCapability] = {
    # --- universally quantified static decision procedures -------------------
    "guard_distinguishable": EvidenceCapability(
        decides="guard_indistinguishability",
        completeness="decisive",
        quantification="universal_static",
        waives_mandatory_for=frozenset({"property"}),
        justification=(
            "Returns True only when matching transitions have empty or identical "
            "guards, and raises UnsupportedEvidence rather than guessing for "
            "distinct non-empty guards. The True/False decision therefore already "
            "ranges over every variable valuation, which is exactly the "
            "quantification a distinguishability property asks for."
        ),
    ),
    "initial_target": EvidenceCapability(
        decides="initial_target",
        completeness="decisive",
        quantification="universal_static",
        waives_mandatory_for=frozenset({"property"}),
        justification=(
            "A composite has exactly one structured initial target or the query "
            "raises. The answer holds for every execution by construction, so a "
            "bounded trace query adds no quantification."
        ),
    ),
    # --- static queries that are decisive but only over their own domain -----
    "effect_declared": EvidenceCapability(
        decides="declared_effect",
        completeness="decisive",
        quantification="declared_effect_set",
        justification=(
            "Decides the declared effect set of matching transitions. It does not "
            "quantify over paths, so it never waives a property obligation."
        ),
    ),
    "state_declared": EvidenceCapability(
        decides="declared_state_set",
        completeness="decisive",
        quantification="declared_state_set",
    ),
    # --- weaker evidence ------------------------------------------------------
    "invariant": EvidenceCapability(
        decides="trace_property",
        completeness="bounded_decisive",
        quantification="all_traces_up_to_bound",
    ),
    "occupancy_after": EvidenceCapability(
        decides="run_outcome",
        completeness="witness",
        quantification="one_configuration",
    ),
    "edge_declared": EvidenceCapability(
        decides="edge_presence",
        completeness="locator",
        quantification="single_edge",
    ),
    "terminates": EvidenceCapability(
        decides="run_termination",
        completeness="witness",
        quantification="one_configuration",
    ),
    "containment": EvidenceCapability(
        decides="declared_containment",
        completeness="decisive",
        quantification="declared_state_set",
        waives_mandatory_for=frozenset({"property"}),
        justification=(
            "Direct substate membership is a closed declared set; the answer "
            "holds for every execution by construction."
        ),
    ),
    "action_declared": EvidenceCapability(
        decides="declared_action",
        completeness="decisive",
        quantification="declared_action_set",
    ),
    "cardinality": EvidenceCapability(
        decides="declared_state_count",
        completeness="decisive",
        quantification="declared_state_set",
        waives_mandatory_for=frozenset({"property"}),
        justification=(
            "Counting the declared non-pseudo substates of a scope ranges over "
            "the whole scope by construction, so a bounded trace adds nothing."
        ),
    ),
    "event_consumed": EvidenceCapability(
        decides="run_event_acceptance",
        completeness="witness",
        quantification="one_configuration",
    ),
    "stays_in": EvidenceCapability(
        decides="run_stability",
        completeness="witness",
        quantification="one_configuration",
    ),
    "variable_delta_after": EvidenceCapability(
        decides="run_variable_delta",
        completeness="witness",
        quantification="one_configuration",
    ),
    "reaches": EvidenceCapability(
        decides="bounded_reachability",
        completeness="witness",
        quantification="one_configuration",
    ),
    "response_within": EvidenceCapability(
        decides="bounded_response",
        completeness="bounded_decisive",
        quantification="all_traces_up_to_bound",
    ),
    "persists_until": EvidenceCapability(
        decides="bounded_persistence",
        completeness="bounded_decisive",
        quantification="all_traces_up_to_bound",
    ),
}


def called_evidence_functions(expression: str) -> frozenset[str]:
    """Return the evidence function names called by one assertion expression.

    Uses the same static-AST view the assertion audit already relies on, so this
    never executes model code and never needs a live environment.

    :param expression: the assertion's terminal Python expression.
    :return: the set of called plain-name functions, empty when unparseable.
    """

    # Assertions arrive as complete `assert ... , "..."` statements, not bare
    # expressions.  Parsing in "eval" mode alone raised on every one of them and
    # returned the empty set, so the procedure gate concluded that no predicate
    # had been called and rejected correct scripts until their budget ran out.
    tree = None
    for mode in ("eval", "exec"):
        try:
            tree = ast.parse(expression, mode=mode)
            break
        except SyntaxError:
            continue
    if tree is None:
        return frozenset()
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                names.add(func.id)
            elif isinstance(func, ast.Attribute):
                names.add(func.attr)
    return frozenset(names)


def mandatory_waiver(
    verification_kind: str, primary_expressions: tuple[str, ...]
) -> tuple[str, str] | None:
    """Decide whether decisive primary evidence waives the mandatory family.

    :param verification_kind: the requirement's frozen kind.
    :param primary_expressions: expressions of every ``primary`` assertion
        mapped to that requirement.
    :return: ``(function_name, justification)`` when the mandatory family is
        waived, otherwise ``None``.
    """

    for expression in primary_expressions:
        for name in sorted(called_evidence_functions(expression)):
            capability = EVIDENCE_CAPABILITY.get(name)
            if capability is None:
                continue
            if capability.completeness not in DECISIVE_COMPLETENESS:
                continue
            if verification_kind in capability.waives_mandatory_for:
                return name, capability.justification
    return None


# ---------------------------------------------------------------------------
# Deterministic non-vacuity gates for bounded formal queries
# ---------------------------------------------------------------------------
# Both rules below are already stated in prose in the converter and reviewer
# prompts.  Pair 0029 showed prose is not enough: across twelve GPT revisions
# and eight Claude revisions, ten of the eleven distinct FBMCQ queries violated
# one of them and every violation cost a full LLM round trip to discover.

_ACTIVE_CALL = re.compile(r'active\(\s*"([^"]+)"\s*\)')
_CONJUNCTION = re.compile(r'active\(\s*"([^"]+)"\s*\)\s*(?:&&|and)\s*active\(\s*"([^"]+)"\s*\)')


def vacuous_sibling_conjunction(query: str) -> tuple[str, str] | None:
    """Detect ``active(A) && active(B)`` over two siblings of one region.

    Two sibling states of a sequential region can never be active in the same
    configuration, so such a conjunction is unsatisfiable and its negation is a
    tautology -- the query's truth value cannot change when the defect is
    present.  Claude spent four revisions on exactly this shape.

    :param query: the FBMCQ query text.
    :return: the offending sibling pair, or ``None``.
    """

    for left, right in _CONJUNCTION.findall(query):
        if left == right:
            continue
        if left.rsplit(".", 1)[:-1] == right.rsplit(".", 1)[:-1] and "." in left:
            return left, right
    return None


def bare_reachability_probe(query: str) -> bool:
    """Detect a reachability query with no causal anchoring at all.

    ``check reach <= N: active("X");`` with no ``init``, no event assumption and
    no response trigger asks "is X reachable from anywhere", which is not
    evidence for any requirement that names a trigger.  The converter prompt
    already forbids it; this makes the rule enforceable instead of advisory.

    :param query: the FBMCQ query text.
    :return: ``True`` when the query is an unanchored reachability probe.
    """

    lowered = query.lower()
    if "check reach" not in lowered:
        return False
    if "init " in lowered or "assume" in lowered or "event(" in lowered:
        return False
    return True


def fbmcq_non_vacuity_findings(expression: str) -> tuple[str, ...]:
    """Return human-readable reasons one FBMCQ expression proves nothing.

    :param expression: the assertion's terminal Python expression.
    :return: zero or more finding strings; empty means the query is admissible.
    """

    findings: list[str] = []
    for query in re.findall(r"""fbmcq\(\s*(['"])(.*?)\1""", expression, re.S):
        text = query[1]
        siblings = vacuous_sibling_conjunction(text)
        if siblings is not None:
            findings.append(
                f"vacuous query: {siblings[0]} and {siblings[1]} are siblings of one "
                "sequential region and can never be active together, so this check "
                "is true regardless of the defect"
            )
        if bare_reachability_probe(text):
            findings.append(
                "unanchored query: a bare `check reach` with no init state, event "
                "assumption or response trigger is not causal evidence for a "
                "triggered requirement"
            )
    return tuple(findings)


# ---------------------------------------------------------------------------
# Model-reference binding for structural/relational evidence
# ---------------------------------------------------------------------------
# A relation query over elements the model does not contain matches nothing and
# therefore returns a *passing* answer.  On pair 0029 Claude wrote
# `event="/dist_to_front_25_extra_lane_true"` -- FCSTM transition syntax rather
# than the event path -- so `conflicting_targets` matched no transitions,
# returned False, and `not False` marked the guard-conflict requirement
# satisfied.  A typo silently turns a defect into a pass, so unresolvable
# references must be rejected before execution, exactly as bounded formal
# queries are rejected by structural binding.

#: Keyword arguments whose string value must name an existing model element.
# Predicate bindings that name a declared model element.  `trigger` is the
# predicate spelling of what the old relation API called `event`; missing it
# meant a fabricated event path -- pair 0029's `"/pick"` -- sailed through the
# unresolved-reference gate and made the check vacuously true.
BOUND_PATH_KWARGS = frozenset(
    {
        "source",
        "target",
        "event",
        "trigger",
        "state",
        "parent",
        "child",
        "composite",
        "scope",
        "variable",
        # `response_within(response=...)` names the state the response must
        # reach.  Left out, the reference gate never checked it, so a response
        # naming no declared state was looked up, not found, and answered
        # False -- a defect reported against a model that never had it.
        "response",
    }
)
def _path_bindings(expression: str) -> tuple[tuple[str, str], ...]:
    """Return every ``(kwarg, value)`` binding that is meant to name an element.

    One parse serves both reference policies below -- what is absent from the
    model, and what is not a name at all -- so they cannot disagree about which
    bindings they are talking about.

    :param expression: the assertion's terminal Python expression.
    :return: deduplicated ``(kwarg, value)`` pairs, in source order.
    """

    tree = None
    for mode in ("eval", "exec"):
        try:
            tree = ast.parse(expression, mode=mode)
            break
        except SyntaxError:
            continue
    if tree is None:
        return ()
    found: list[tuple[str, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for keyword in node.keywords:
            if keyword.arg not in BOUND_PATH_KWARGS:
                continue
            value = keyword.value
            if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
                continue
            found.append((str(keyword.arg), value.value))
    return tuple(dict.fromkeys(found))


def _absent_path_bindings(
    expression: str, known_paths: frozenset[str]
) -> tuple[tuple[str, str], ...]:
    """Return the bindings that name no element the frozen model declares."""

    if not known_paths:
        return ()
    return tuple(
        (arg, text)
        for arg, text in _path_bindings(expression)
        if text
        and text != PSEUDO_INITIAL
        and text not in known_paths
        # A placeholder is refused by `placeholder_bindings`, whose message
        # explains the precondition route; reporting it here too would pre-empt
        # that with the less useful "no such element".
        and not is_placeholder_name(text)
    )


def declared_path_bindings(
    expression: str, known_paths: frozenset[str]
) -> tuple[str, ...]:
    """Return the bindings that do name an element the frozen model declares.

    The symmetric read of `_absent_path_bindings`, and the one attribution needs.
    A `precondition` on a proposed name observes nothing at runtime that any
    frozen trace entry can cover, so on its own it is unattributable -- but the
    obligation it guards is about real elements, named statically in the
    assertions that depend on it.  Those are read from the expression rather than
    from an execution trace because a blocked dependent never produced one.

    :param expression: the assertion's terminal Python expression.
    :param known_paths: every state and event path the frozen model declares.
    :return: deduplicated declared names, in source order.
    """

    return tuple(
        dict.fromkeys(
            text
            for _, text in _path_bindings(expression)
            if text in known_paths
        )
    )


def placeholder_bindings(expression: str) -> tuple[str, ...]:
    """Return bindings whose value stands in for a name instead of being one.

    A producer writes one when the NL requires an element the model never
    declares.  That is a real observation, but it is not a check: nothing can be
    looked up, so the runtime refuses it.  Catching it here instead turns a
    wasted round trip into a specific instruction (issue #170 §11.2).

    :param expression: the assertion's terminal Python expression.
    :return: offending ``kwarg=value`` strings; empty when every value is a name.
    """

    return tuple(
        dict.fromkeys(
            f"{arg}={text!r}"
            for arg, text in _path_bindings(expression)
            if is_placeholder_name(text)
        )
    )


def unresolved_model_references(
    expression: str, known_paths: frozenset[str]
) -> tuple[str, ...]:
    """Return path-like arguments that no model element can satisfy.

    :param expression: the assertion's terminal Python expression.
    :param known_paths: every state and event path the frozen model declares.
    :return: offending ``kwarg=value`` strings; empty when all resolve.
    """

    return tuple(
        dict.fromkeys(
            f"{arg}={text!r}"
            for arg, text in _absent_path_bindings(expression, known_paths)
        )
    )


class _RequirementSpec(Protocol):
    """The fields of a ``Requirement`` the four-step gates read."""

    requirement_id: str
    predicate: str
    predicate_bindings: dict[str, str]
    limitations: tuple[str, ...]


#: Predicates whose False *is* the finding when the element is declared elsewhere,
#: so the waiver below does not apply to them.
#:
#: `containment(parent=M, child=<declared elsewhere>)` answers False precisely
#: because the state sits outside `M` -- which is the NL's "substate" obligation
#: being violated, stated directly.  Proposing `M.<name>` instead says the same
#: thing through an existence check plus a dependent, costs a conversion round to
#: add the precondition, and loses the declared path that anchored it.  Pair 0029's
#: expected structural defect is exactly this shape, and it is the one the reviewer
#: pushed toward a proposal.
_DECLARED_PATH_IS_THE_CLAIM = frozenset({"containment", "initial_target"})

#: The phrase a Requirement must contain in `limitations` to keep a proposed name
#: the step-2 comparison would otherwise refuse.
#:
#: Step 2 cannot tell a *shared* element from one the sentence wants *per scope*.
#: `FinishState` declared once and reached from both modes is the first; "each
#: region shall have its own Idle" on a model declaring only `RegionA.Idle` is the
#: second, and there the refusal has no legal answer -- bind the declared path and
#: the requirement now says something else, keep the proposal and the gate fires
#: again, five rounds and the run dies.  That is the shape that killed pair 0006
#: twice, so the gate carries an exit.
#:
#: An exit that costs nothing would be taken by default, so this one costs a
#: sentence the Requirement Reviewer then reads: the producer has to say the
#: sentence demands a scope-local instance, and the reviewer judges that claim
#: (step 3 versus step 4 is its job anyway).  Same bargain as `mandatory_waiver`
#: -- waivable, but only against an explicit justification that lands in the run
#: record.
SCOPE_LOCAL_WAIVER = "scope-local instance required"


#: Bindings that name the *subject* of a claim -- what the run must reach or hold.
#: A proposed name in one of these is what turns a pseudo-state concept into a
#: fabricated state; a proposed `source` or `scope` is a different mistake and is
#: caught by the reference gate instead.
CLAIM_SUBJECT_BINDINGS = frozenset({"target", "response", "state", "child"})


#: Which declaration namespace each binding draws its name from.  Bindings absent
#: from this map are not names -- `kind`, `sign`, `count`, and the FCSTM expressions
#: in `condition` / `release` -- and comparing them against declared paths is how a
#: `phase: "entry"` came within a case fold of matching a state called `Entry`.
_BINDING_NAMESPACE = {
    "source": "states",
    "target": "states",
    "state": "states",
    "parent": "states",
    "child": "states",
    "composite": "states",
    "scope": "states",
    "response": "states",
    "trigger": "events",
    "event": "events",
    "variable": "variables",
}


def redundant_proposal_findings(
    requirements: Iterable[_RequirementSpec],
    known_paths: frozenset[str],
    vocabulary: dict[str, tuple[str, ...]] | None = None,
) -> tuple[str, ...]:
    """Step 2 of the four-step procedure, decided rather than reviewed.

    A state two regions share is declared inside exactly one of them.  A sentence
    about the other region still means that one state, so the leaf name is already
    in the vocabulary under a different parent -- and proposing a new path for it
    reports a missing element that is present.  Pair 0029 proposed
    `<UrbanMode>.FinishState` while the vocabulary listed it under the sibling
    composite, and the resulting finding was published as a confirmed issue.

    Deterministic from the vocabulary alone, so it is a gate: leaving it to the
    Requirement Reviewer asks a judgement call of something a comparison settles,
    and a reviewer that misses it costs the item its repair budget.

    What the comparison cannot settle is *shared* versus *per scope*, so a
    Requirement whose `limitations` states `SCOPE_LOCAL_WAIVER` keeps its proposal
    and the reviewer judges it instead.  Measured over the corpus this is a rare
    need -- 7 of 60 models declare any leaf name twice, and in those the repeated
    name is the converter's own `UnspecifiedInitial` -- but the cost of being
    wrong without an exit is the whole run.
    """

    # Per namespace, because they are three flat lists that share leaf names.  A
    # state, an event and a variable can all be called `intersection`, and pair 0029
    # declares a state by that name while its NL line 7 writes `intersection=true`
    # -- a genuine missing-variable claim.  Compared against one merged index, that
    # claim was refused and told to bind `<root>.UrbanMode.intersection`, which
    # `variable_declared` then refuses outright ("variables take no path prefix").
    # No legal answer, five rounds, dead run.
    groups = vocabulary if vocabulary is not None else {"states": tuple(known_paths)}
    by_namespace: dict[str, dict[str, list[str]]] = {}
    for namespace, paths in groups.items():
        index: dict[str, list[str]] = {}
        for path in paths:
            index.setdefault(str(path).rsplit(".", 1)[-1], []).append(str(path))
        by_namespace[namespace] = index
    findings: list[str] = []
    for item in requirements:
        # The phrase has to *open* a limitation entry rather than appear anywhere in
        # one.  As a free substring, "no scope-local instance required, this is the
        # shared state" -- a limitation that explicitly denies the need -- switched
        # the gate off.  Unlikely in fresh prose, likely once a producer has read the
        # phrase in a refusal and is arguing with it.
        waived = item.predicate not in _DECLARED_PATH_IS_THE_CLAIM and any(
            str(entry).strip().lower().startswith(SCOPE_LOCAL_WAIVER)
            for entry in (getattr(item, "limitations", ()) or ())
        )
        if waived:
            continue
        for binding, value in (item.predicate_bindings or {}).items():
            namespace = _BINDING_NAMESPACE.get(binding)
            if namespace is None:
                continue
            text = str(value).strip()
            if not text or text == PSEUDO_INITIAL or text in known_paths:
                continue
            declared = sorted(
                by_namespace.get(namespace, {}).get(text.rsplit(".", 1)[-1], ())
            )
            if declared:
                findings.append(
                    f"{item.requirement_id} proposes {binding}={text!r} while the "
                    f"vocabulary already declares {declared}; bind the declared "
                    f"path"
                    + (
                        f", whose False is then the finding: {item.predicate} answers "
                        "False precisely because the element sits outside the scope "
                        "the sentence names, so there is nothing to propose (step 2)"
                        if item.predicate in _DECLARED_PATH_IS_THE_CLAIM
                        else f", or -- if the sentence really requires an instance "
                        f"inside this scope rather than the shared one -- open a "
                        f"limitations entry with {SCOPE_LOCAL_WAIVER!r} and the "
                        "Reviewer will judge that (step 2)"
                    )
                )
    return tuple(findings)


def initialization_anchored_findings(
    requirements: Iterable[_RequirementSpec],
) -> tuple[str, ...]:
    """Requirements that anchor a running-phase claim at the initial configuration.

    `[*]` as a source means "before the machine has entered anything", which is the
    right anchor for a power-on claim and the wrong one for every other phase.  Bound
    on an operation or termination requirement it makes the claim about
    initialization instead, and the two questions can have opposite answers on the
    same model.

    Pair 0000 is the case, and it is the pair's expected defect: the model declares
    `[*] -> FinalState : /Power_Off`, which is precisely the mistake -- power-off
    should terminate the *running* mode, not fire from the pseudo-initial.  A
    termination requirement bound to `source="[*]"` asks whether that very edge
    exists, so it is true *because* of the defect, and the pair's one expected issue
    goes unreported.  Verified: matrix-v13's 0000-claude wrote exactly that and
    published zero issues where matrix-v11 published the credited hit.

    Refused here rather than at conversion, because `predicate_bindings` are frozen
    once the requirement is accepted.  The converter cannot rebind a source, so a
    gate downstream of the freeze would leave the item no legal move -- which is how
    two earlier runs died.

    :param requirements: the accepted requirement set.
    :return: one finding per offending requirement; empty when every anchor fits its
        phase.
    """

    findings: list[str] = []
    for item in requirements:
        phase = str(
            (getattr(item, "source_context", None) or {}).get("behavior_phase", "")
        ).lower()
        # Allowed only where the phase says `initialization`, rather than refused
        # where it says operation or termination.  `behavior_phase` is optional, and
        # keyed the other way the gate reads a field the producer can simply leave
        # out: matrix-v15's 0000-claude emitted no phase on any requirement, so the
        # gate never fired and the vacuous termination claim went through exactly as
        # it had before the gate existed.  A permission has to be claimed; a
        # prohibition can be dodged by silence.
        if phase == "initialization":
            continue
        bindings = item.predicate_bindings or {}
        anchored = sorted(
            binding
            for binding in ("source", "scope")
            if str(bindings.get(binding, "")).strip() == PSEUDO_INITIAL
        )
        if anchored:
            findings.append(
                f"{item.requirement_id} binds {anchored} to {PSEUDO_INITIAL} with "
                f"source_context.behavior_phase={phase or 'unset'!r}. That anchors "
                "the claim before the machine has entered anything, so it asks about "
                "initialization -- and on a model whose defect is an edge leaving the "
                "pseudo-initial, the claim is then true because of the defect. Either "
                "name the running state the sentence is about (one requirement per "
                "state when the sentence does not pin one), or, if the sentence really "
                "is about power-on, set behavior_phase to \"initialization\"."
            )
    return tuple(findings)


def termination_proposal_findings(
    requirements: Iterable[_RequirementSpec],
    known_paths: frozenset[str],
    terminating: Iterable[dict[str, Any]],
) -> tuple[str, ...]:
    """Step 1 of the four-step procedure, decided rather than reviewed.

    Termination is written `[*]` and has no name, so a requirement that proposes
    one -- `FinalState`, `EndState`, whatever the sentence's wording suggests --
    asks about a state no correctly-terminating model declares.  Pair 0050 did it
    twice and both findings were published against a model whose termination is
    written correctly.

    Keyed on the model rather than on the sentence's wording: the gate fires only
    when the model actually ends the run from that source on that trigger, which is
    exactly when `terminates` can answer the claim.  Matching words like "final"
    would fire on requirements that have nothing to do with termination.

    The trigger is part of the key, always.  A source that ends the run on one
    event usually does other things on others: pair 0050's `HumanDrivingMode` ends
    the run on `Power_Off` and moves to `AutonomousMode` on a distance event.  A
    fallback that fired whenever the source ends the run on *anything* therefore
    refused every subject-proposing claim from it -- and `reaches` and `cardinality`
    have no trigger binding at all, so every "the NL needs a state this model lacks,
    reachable from X" claim died there, prescribing a `terminates` call that
    evaluates False.  44 source/pair combinations across 16 pairs.  Missing a
    trigger-less fabrication is the cheaper error: it reaches the Requirement
    Reviewer, which is where an undecidable case belongs.

    Reads `ends_run` and asks nothing else.  This gate used to reconstruct the
    lowering's two-edge termination itself, from ancestry -- an inner exit carrying
    the trigger plus any run-ending edge at or above its scope.  That is wrong
    whenever a composite exits on more than one event: pair 0050 leaves
    `SubState1` both on `Power_Off` (which ends the run) and on the mode-switch
    event (which does not), and ancestry cannot tell them apart, so the gate
    claimed the model terminates on a mode switch and told the producer to assert
    it -- a fabricated defect on 16 requirements across three pairs.  The route
    token decides it, and `_pseudo_state_facts` is where the token is visible.
    """

    rows = [row for row in terminating if isinstance(row, dict)]
    ends = {
        (str(row.get("source") or ""), str(row.get("trigger") or ""))
        for row in rows
        if row.get("ends_run")
    }

    findings: list[str] = []
    for item in requirements:
        if item.predicate == "terminates":
            continue
        bindings = item.predicate_bindings or {}
        proposed = sorted(
            binding
            for binding in CLAIM_SUBJECT_BINDINGS & set(bindings)
            if str(bindings[binding]).strip()
            and str(bindings[binding]).strip() != PSEUDO_INITIAL
            and str(bindings[binding]).strip() not in known_paths
        )
        if not proposed:
            continue
        source = str(bindings.get("source") or bindings.get("scope") or "").strip()
        trigger = str(bindings.get("trigger") or "").strip()
        if (source, trigger) in ends:
            findings.append(
                f"{item.requirement_id} proposes {proposed} as the claim's subject "
                f"while the model ends the run from {source!r}"
                + (f" on {trigger!r}" if trigger else "")
                + f"; use terminates(scope={source!r}"
                + (f", trigger={trigger!r}" if trigger else "")
                + ") -- termination has no state to bind (step 1)"
            )
    return tuple(findings)


def _existence_checked_names(
    expression: str, known_paths: frozenset[str]
) -> tuple[str, ...]:
    """Absent names this expression asks the *existence* of.

    Keyed on the predicate rather than on the assertion's `role`, because that is
    where the soundness actually comes from: `variable_declared` on an absent name
    returns False, which is the answer to the question asked, not a query that
    matched nothing and passed.  Reading `role == "precondition"` instead forced a
    requirement whose own predicate is an existence check into a precondition plus
    a byte-identical dependent -- and when a reviewer objected to that duplication
    and the producer removed one of them, the survivor lost its exemption and the
    run died with its repair budget spent (pair 0006, matrix-v10).
    """

    tree = None
    for mode in ("eval", "exec"):
        try:
            tree = ast.parse(expression, mode=mode)
            break
        except SyntaxError:
            continue
    if tree is None:
        return ()
    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if node.func.id not in EXISTENCE_PREDICATES:
            continue
        for keyword in node.keywords:
            if keyword.arg not in BOUND_PATH_KWARGS:
                continue
            value = keyword.value
            if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
                continue
            text = value.value
            if text and text != PSEUDO_INITIAL and text not in known_paths:
                found.append(text)
    return tuple(dict.fromkeys(found))


class _ScriptAssertion(Protocol):
    """The fields of an ``AssertionSpec`` the script-level reference gate reads."""

    assertion_id: str
    requirement_id: str
    role: str | None
    expression: str
    depends_on: tuple[str, ...]


def unresolved_reference_findings(
    assertions: Iterable[_ScriptAssertion], known_paths: frozenset[str]
) -> tuple[str, ...]:
    """Return findings for bindings naming an element the frozen model lacks.

    An absent name is legal in exactly one shape: a `precondition` proposes the
    name of an element the model should have declared, and every assertion that
    needs that element depends on it.  A missing element then makes the
    precondition false, its dependents are blocked rather than run, and blocked
    never counts as satisfied -- so nothing passes vacuously, and the repair
    stage receives a named target to add (issue #170 §11.2).

    Every other absent name is refused, because unlinked it still runs, still
    matches nothing, and still passes: the defect-hiding vacuous pass this gate
    exists to stop.

    The two halves have to be decided in one place.  Enforcing only the second
    deadlocked pair 0006 for six revisions -- the proposed name a precondition
    needs is absent by construction, so the gate rejected the one legal move and
    the run died with its repair budget spent.

    :param assertions: every assertion in the script.
    :param known_paths: every state and event path the frozen model declares.
    :return: one finding per offending binding; empty when all resolve.
    """

    items = tuple(assertions)
    closures = dependency_closure(items)
    proposed_by: dict[str, set[str]] = {}
    for item in items:
        checked = _existence_checked_names(item.expression, known_paths)
        for name in checked:
            proposed_by.setdefault(name, set()).add(item.assertion_id)
    findings: list[str] = []
    for item in items:
        allowed = {item.assertion_id} | closures[item.assertion_id]
        exempt = {
            name for name, owners in proposed_by.items() if owners & allowed
        }
        findings.extend(
            f"{item.requirement_id}/{item.assertion_id}: "
            f"unresolved model reference {arg}={text!r}"
            for arg, text in _absent_path_bindings(item.expression, known_paths)
            if text not in exempt
        )
    return tuple(findings)


#: Lifecycle phases where an event's *source placement* decides satisfaction.
SOURCE_SENSITIVE_PHASES = frozenset({"operation", "termination"})


def source_omitting_response_calls(expression: str) -> tuple[str, ...]:
    """Return `response_within` calls that leave `source` unbound.

    `source` is the one optional binding in the whole vocabulary, and leaving it
    out means "from the initial configuration".  For an operation or termination
    event that is initialization-only evidence: on pair 0000 the
    `[*] -> FinalState : /Power_Off` edge makes "Power_Off reaches FinalState"
    true from power-on while saying nothing about whether HumanDrivingMode can
    reach it at all -- which was the defect, and it was reported satisfied.

    This gate used to name `transition_exists` and `transitions`.  Neither is in
    the assertion environment any more, so it matched nothing and protected
    nothing while still reading as an active check.  The predicate era narrows
    the rule to the one call that can still express the mistake.

    :param expression: the assertion's terminal Python expression.
    :return: offending call names, empty when none.
    """

    tree = None
    for mode in ("eval", "exec"):
        try:
            tree = ast.parse(expression, mode=mode)
            break
        except SyntaxError:
            continue
    if tree is None:
        return ()
    bad = [
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "response_within"
        and "source" not in {keyword.arg for keyword in node.keywords}
    ]
    return tuple(dict.fromkeys(bad))
