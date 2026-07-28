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

__all__ = [
    "EvidenceCapability",
    "fbmcq_non_vacuity_findings",
    "vacuous_sibling_conjunction",
    "bare_reachability_probe",
    "unresolved_model_references",
    "source_omitting_relation_calls",
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

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
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
    }
)
#: The relation API exposes the pseudo-initial source under this exact literal.
PSEUDO_INITIAL = "[*]"
#: Sanctioned stand-in for a term the NL requires but the model never declares.
UNDECLARED = "<undeclared>"


def unresolved_model_references(
    expression: str, known_paths: frozenset[str]
) -> tuple[str, ...]:
    """Return path-like arguments that no model element can satisfy.

    :param expression: the assertion's terminal Python expression.
    :param known_paths: every state and event path the frozen model declares.
    :return: offending ``kwarg=value`` strings; empty when all resolve.
    """

    if not known_paths:
        return ()
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        return ()
    bad: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for keyword in node.keywords:
            if keyword.arg not in BOUND_PATH_KWARGS:
                continue
            value = keyword.value
            if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
                continue
            text = value.value
            # `<undeclared>` is the sanctioned way to say "the NL requires a
            # term this model never declares".  Rejecting it here left the
            # requirement with no legal move at all: the literal was refused,
            # any substitute is fabricated, and omitting the primary trips the
            # "at least one primary" rule -- a three-way deadlock that burned
            # the whole repair budget.  Let it through so precheck can turn it
            # into a coverage gap, which is the honest outcome.
            if (
                not text
                or text == PSEUDO_INITIAL
                or text == UNDECLARED
                or text in known_paths
            ):
                continue
            bad.append(f"{keyword.arg}={text!r}")
    return tuple(dict.fromkeys(bad))


#: Lifecycle phases where an event's *source placement* decides satisfaction.
SOURCE_SENSITIVE_PHASES = frozenset({"operation", "termination"})


def source_omitting_relation_calls(expression: str) -> tuple[str, ...]:
    """Return `transition_exists` calls that pin event/target but not source.

    The converter and reviewer prompts already state this twice: for an
    operation or termination event, a match attached only to the pseudo-initial
    `"[*]"` is initialization-only evidence, so `transition_exists(event=...,
    target=...)` with no `source` cannot decide the requirement.  It was still
    only prose.  On pair 0000 Claude used exactly that form for the Power-Off
    termination requirement; the `[*] -> FinalState : /Power_Off` edge made it
    True and EXP-0000-IT-001 was reported satisfied.

    :param expression: the assertion's terminal Python expression.
    :return: offending call names, empty when none.
    """

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        return ()
    bad: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = node.func.id if isinstance(node.func, ast.Name) else None
        if name not in {"transition_exists", "transitions"}:
            continue
        kwargs = {keyword.arg for keyword in node.keywords}
        if "source" in kwargs:
            continue
        if {"event", "target"} & kwargs:
            bad.append(name)
    return tuple(dict.fromkeys(bad))
