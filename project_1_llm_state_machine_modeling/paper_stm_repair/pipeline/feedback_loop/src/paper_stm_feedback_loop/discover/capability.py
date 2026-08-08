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
from typing import Any, Iterable, Mapping, Protocol

from paper_stm_feedback_loop.assertions.predicate_api import (
    PSEUDO_INITIAL,
    is_placeholder_name,
)

from .dependencies import dependency_closure
from .predicates import (
    EXISTENCE_PREDICATES,
    PREDICATE_NAMES,
    PREDICATES,
    paired_presuppositions,
)

__all__ = [
    "EvidenceCapability",
    "missing_presupposition_findings",
    "unmatched_named_element_findings",
    "short_circuited_primary_findings",
    "condition_non_vacuity_findings",
    "CONDITION_BINDINGS",
    "vacuous_sibling_conjunction",
    "vacuous_containment_findings",
    "unresolved_model_references",
    "unresolved_reference_findings",
    "initialization_anchored_findings",
    "placeholder_bindings",
    "conceded_omission_findings",
    "projection_anchored_findings",
    "trigger_consuming_predicate_findings",
    "redundant_proposal_findings",
    "termination_proposal_findings",
    "CLAIM_SUBJECT_BINDINGS",
    "SCOPE_LOCAL_WAIVER",
    "declared_path_bindings",
    "source_omitting_response_calls",
    "anchors_at_initialization",
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
#: One `active("path")` operand, remembering whether it was negated. Matching the operand
#: rather than a whole two-term conjunction is what lets the pair-wise test below see every
#: combination in a longer chain, and what lets it drop a `!` it previously could not see.
_ACTIVE_OPERAND = re.compile(r'(!\s*)?active\(\s*"([^"]+)"\s*\)')

#: Disjunction splits a condition into independent claims, so operands from different sides
#: of a `||` are never jointly asserted and must not be paired.
_DISJUNCTION = re.compile(r"\|\||\bor\b")


def vacuous_sibling_conjunction(query: str) -> tuple[str, str] | None:
    """Detect ``active(A) && active(B)`` over two siblings of one region.

    Two sibling states of a sequential region can never be active in the same
    configuration, so such a conjunction is unsatisfiable and its negation is a
    tautology -- the query's truth value cannot change when the defect is
    present.  Claude spent four revisions on exactly this shape.

    :param query: the FBMCQ query text.
    :return: the offending sibling pair, or ``None``.
    """

    for disjunct in _DISJUNCTION.split(query):
        # Only operands the disjunct *asserts* can contradict each other. `!active(A) &&
        # active(B)` says "in B and not in A", which two siblings satisfy easily -- the old
        # detector matched the inner substring and never saw the `!`, so it refused a query
        # on the opposite of what was written.
        asserted = [
            path for negated, path in _ACTIVE_OPERAND.findall(disjunct) if not negated
        ]
        # Every pair, not just adjacent ones: `findall` over two-term shapes is
        # non-overlapping, so `active(M) && active(M.A) && active(N.B)` matched the nested
        # `(M, M.A)` and the vacuous `(M.A, N.B)` was never examined. Pair 0047 carries a real
        # three-term condition.
        for index, left in enumerate(asserted):
            for right in asserted[index + 1 :]:
                found = _incompatible(left, right)
                if found is not None:
                    return found
    return None


def _incompatible(left: str, right: str) -> tuple[str, str] | None:
    """The pair, when no configuration can hold both; otherwise nothing."""

    if left == right:
        return None
    if "." not in left or "." not in right:
        # A bare name carries no hierarchy, so nothing here can tell an unrelated state
        # from an unqualified reference to an ancestor: `M` against `Sys.M.A` may well be
        # `Sys.M`, which contains it and is co-active with it. The old rule required a
        # dot on the pair it compared; requiring one on *each side* keeps that
        # conservatism, which loosening it to "either side" would have quietly dropped.
        return None
    # Siblings were only the shortest case. paper1's object language is `M = (S, E, V,
    # Tr, A)` with orthogonal regions excluded, so exactly one leaf is active and the
    # active set is the chain from the root down to it -- two states are co-active if and
    # only if one contains the other. Cousins across two top-level modes are the same
    # impossibility with a longer prefix, and comparing immediate parents let every one
    # of them through: an unsatisfiable conjunction became a primary that could not fail,
    # so its requirement reported satisfied and its expected issue was lost.
    # The separator is load-bearing: `Sys.M10` starts with `Sys.M1` as a string but is
    # not inside it, and the corpus has exactly those shapes (`fork1`/`fork2`,
    # `Join1`/`Join2`).
    if not (left.startswith(f"{right}.") or right.startswith(f"{left}.")):
        return left, right
    return None


#: Bindings whose value is an FCSTM boolean expression rather than a model path.
#: These are where a vacuous condition can now hide; `fbmcq(...)` used to be the
#: only carrier and is no longer callable.
CONDITION_BINDINGS = ("condition", "release")


def _condition_arguments(expression: str) -> tuple[str, ...]:
    """Every `condition=`/`release=` string literal in the call, via the AST.

    Parsed rather than regexed because the value is itself full of quotes and
    operators -- `!(active("A") && active("B"))` -- and a regex over that is how
    the previous gate ended up matching a call shape instead of a value.
    """

    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except SyntaxError:
        return ()
    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for keyword in node.keywords:
            if keyword.arg in CONDITION_BINDINGS and isinstance(
                keyword.value, ast.Constant
            ) and isinstance(keyword.value.value, str):
                found.append(keyword.value.value)
    return tuple(found)


def condition_non_vacuity_findings(expression: str) -> tuple[str, ...]:
    """Return human-readable reasons one condition expression proves nothing.

    Reads the condition out of the predicate bindings that carry one.  The
    previous version regexed for `fbmcq('...')`, and `fbmcq` was removed from the
    assertion namespace when the vocabulary closed -- so it matched nothing on
    every real script while still being run as an active gate and described in
    the prompts as enforced.  The detection itself was fine; only the place it
    looked was gone.  What that costs is a mandatory primary that cannot fail:
    `invariant(scope="Sys.M", condition='!(active("Sys.M.A") && active("Sys.M.B"))')`
    over two siblings of one sequential region is true whatever the model does,
    so the requirement is reported satisfied and its expected issue is lost.

    The companion check for unanchored reachability probes is gone rather than
    ported: it looked for `check reach` with no `init`, which is FBMCQ DSL and not
    something a condition binding can contain, and the shape it guarded against is
    now unwritable -- `reaches` requires `source` and `target`, so there is no
    anchorless form of the query to reject.  The vocabulary enforces it by
    construction, which is the stronger place for it.

    :param expression: the assertion's terminal Python expression.
    :return: zero or more finding strings; empty means the query is admissible.
    """

    findings: list[str] = []
    for text in _condition_arguments(expression):
        pair = vacuous_sibling_conjunction(text)
        if pair is not None:
            left, right = pair
            # The wording has to hold for the general case now that the rule does. Calling a
            # cousin pair "siblings of one region" was a plain falsehood, and this string is
            # handed back to the producer as revision feedback -- a wrong reason invites an
            # argument with the gate rather than a fix.
            relation = (
                "siblings of one sequential region"
                if left.rsplit(".", 1)[0] == right.rsplit(".", 1)[0]
                else "in different branches of the hierarchy, neither containing the other"
            )
            findings.append(
                f"vacuous query: {left} and {right} are {relation}, so no configuration "
                "holds both and this check is true regardless of the defect"
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


def substituted_binding_findings(
    requirements: Iterable[_RequirementSpec],
    assertions: Iterable[Any],
    known_paths: frozenset[str],
) -> tuple[str, ...]:
    """Assertions naming an element nobody bound, declared, or proposed.

    Gate D checks that an assertion calls the predicate its Requirement named. It does not
    check *what the predicate is called on*, and that gap let pair 0050 publish a finding the
    ledger had explicitly withdrawn: the Requirement bound the composite event the model does
    declare, and the converter wrote both its assertions against `…human_steering_cmd` -- a
    prefix of that composite name, declared nowhere. The resulting precondition asked whether
    the model declares a separately-triggerable atom, which is the basis parent ruling
    withdrew on 2026-07-30 because the specification's comma list does not authorise reading
    the three conditions as independently triggerable.

    Three sources make an element legitimate, and the third is what keeps the proposed-name
    mechanism alive:

      the Requirement's own `predicate_bindings` -- what it asked about;
      the frozen model's declared paths -- reading the artefact, not inventing; and
      a name the Requirement wrote into `limitations` -- step 4, recorded and therefore
      reviewable.

    Anything else is the converter changing the question. Refused here rather than at
    execution, because a bound element cannot be rebound once the requirement is accepted --
    the same reason `initialization_anchored_findings` gates at split time.

    :param requirements: the accepted requirement set.
    :param assertions: the converted assertion specs.
    :param known_paths: every path the frozen model declares.
    :return: one finding per offending assertion.
    """
    if not known_paths:
        return ()
    by_id = {item.requirement_id: item for item in requirements}
    findings: list[str] = []
    for assertion in assertions:
        requirement = by_id.get(getattr(assertion, "requirement_id", None))
        # No predicate means a pre-vocabulary artefact; those keep the old behaviour so v1/v2
        # bundles still run.
        if requirement is None or not getattr(requirement, "predicate", None):
            continue
        # Every path-shaped token in every binding value, not just the values that *are*
        # paths. `persists_until` binds `release=active("<path>")`, so the element it names is
        # embedded in an expression -- reading only bare values refused a Requirement that had
        # bound the very element its assertion asserted, and the repeat killed the cell on the
        # no-progress gate.
        bound: set[str] = set()
        for value in (requirement.predicate_bindings or {}).values():
            text = str(value).strip()
            if not text:
                continue
            bound.add(text)
            bound.update(re.findall(r"[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)+", text))
        # Proposed names are recorded in prose, so the Requirement writes the *name* rather
        # than the qualified path it will be bound as. Compare last segments, which is the
        # same comparison `redundant_proposal_findings` performs.
        limitations_text = " ".join(
            str(entry) for entry in (getattr(requirement, "limitations", ()) or ())
        )
        for arg, text in _absent_path_bindings(
            getattr(assertion, "expression", ""), known_paths
        ):
            if text in bound or text in limitations_text:
                continue
            if text.rsplit(".", 1)[-1] in limitations_text:
                continue
            if any(text == candidate or text.rsplit(".", 1)[-1] == candidate.rsplit(".", 1)[-1]
                   for candidate in bound):
                continue
            findings.append(
                f"{assertion.assertion_id} binds {arg}={text!r}, which the model does not "
                f"declare, requirement {requirement.requirement_id} did not bind, and no "
                "`limitations` entry proposes. Assert what the requirement bound "
                f"({sorted(bound)}), or -- if the sentence needs an element the model lacks "
                "-- have the requirement propose it and record that in `limitations` first."
            )
    return tuple(findings)


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
    #: `RequirementDerivation | None` —— `derivation_contract_findings` 读它。
    #: 这里不写具体类型是为了不让 capability 依赖 schemas（其余门也都按 Protocol 松耦合）。
    derivation: object | None


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


def vacuous_containment_findings(
    requirements: Iterable[Any], known_paths: Iterable[str] = ()
) -> tuple[str, ...]:
    """Refuse a containment requirement whose parent was read off the child's own path.

    `containment(parent=P, child=P.X)` cannot come back False: a declared path's own prefix
    *is* its parent, so the answer follows from how the two strings were spelled. Measured
    over the corpus, 567 of 567 calls in that shape return True; over one generation's three
    rounds, the nested spelling was True 28 times and False never, while the cross-level
    spelling was False 25 times and True never.

    Refusing the shape inside the predicate was tried first and is wrong: a direct child's
    path is *always* its parent's plus one segment, so a call-site refusal leaves the
    predicate unable to return True at all, and four behaviour tests say so immediately. The
    shape is not the defect.

    The defect is where `parent` came from. Bound to what the sentence says, the check is
    ordinary -- True when the model agrees, False when it buries the element somewhere else,
    and that False is the finding. Bound to the declared path's own prefix, it asks "is this
    element where the model put it" and answers yes, while the hierarchy the sentence asked
    about is never examined. The two are identical at the call site and differ only in
    provenance, which is visible here and nowhere else.

    So the requirement has to say where the level came from. Where `nl_parent` agrees with
    the declared prefix there is no obligation to check -- the model already satisfies it by
    construction. Where it disagrees, that disagreement is the requirement, and the binding
    is not self-prefixed any more, so this gate never sees it.

    ⚠️ NOT WIRED as of v22. Landing it needs two things this function cannot supply: a prompt
    that teaches the producer to record `source_context.nl_parent`, and updated fixtures for
    the existing tests whose requirements use the nested spelling. Wiring it without those
    makes the refusal unanswerable -- the producer is told to supply a field nothing has
    described, exhausts its repair budget, and the cell is quarantined. Measured directly:
    wiring it alone turned fourteen green tests red, every one on "revised RequirementSet
    revision must increase". It lands with its tests now so the next iteration starts from a
    checked design instead of a description.
    """

    findings: list[str] = []
    declared = frozenset(str(p) for p in known_paths if p)
    for item in requirements:
        if getattr(item, "predicate", None) != "containment":
            continue
        bindings = getattr(item, "predicate_bindings", None) or {}
        parent = str(bindings.get("parent") or "").strip()
        child = str(bindings.get("child") or "").strip()
        if not parent or not child:
            # Absent or unresolved bindings have their own gate; reporting them here would
            # give the producer two different reasons for one problem.
            continue
        if not (child.startswith(f"{parent}.") and "." not in child[len(parent) + 1 :]):
            continue
        if declared and child not in declared:
            # `child` 是**提名路径**，模型没有声明它 —— 那么 `containment` 返回 False，而那个 False
            # 就是发现（元素缺失）。本门的整个前提是「已声明路径的自前缀必为其父，所以答案由拼写
            # 决定」；`child` 未声明时前提不成立，答案由模型决定。
            #
            # 没有别的门兜住这一类：`redundant_proposal_findings` 只在叶名在词表里另有声明时才拦，
            # 完全缺失的名字它不管。而 v23 恰好抬高了这个形状的出现概率：prompt 早就教「路径写成
            # `<句子所指的父>.<名字>`」，v23 又新教「parent 绑句子所指的层」，两条叠加，
            # `nl_parent + "." + name` 作 child 是自然产物。
            #
            # 历史激活 9/227 —— 首版注释写「0/105」，那是按**已封印断言**统计的（child 未声明者
            # 早在断言层被拒，永远进不了那个分母）。按**需求层**统计才是这道守卫的真实面：v21+v22
            # 共 227 条自前缀 containment 需求，其中 9 条 child 未声明，且这 9 条的叶名在词表里
            # 别处也没有 —— `redundant_proposal_findings` 兜不住。分母选错会把一条有真实激活面的
            # 守卫读成死代码，而那正是 V4/V5 整代次白跑的形状。
            # 所以这是前瞻性防护而非既存缺陷 —— 但代价不对称：漏放一次是白花一次 check，
            # 误拒一次是压掉一条真缺失。
            continue
        context = getattr(item, "source_context", None)
        nl_parent = getattr(context, "nl_parent", None)
        rid = getattr(item, "requirement_id", "?")
        if not nl_parent:
            findings.append(
                f"{rid} binds containment(parent={parent!r}, child={child!r}): the child is "
                "that parent's own prefix plus one segment, so the check cannot come back "
                "False and tests nothing. Record in `source_context.nl_parent` the level the "
                "sentence puts the element at, then bind that as `parent` and keep the "
                "declared path as `child`."
            )
        elif str(nl_parent).strip() == parent:
            # 放行，不拒。
            #
            # 这一支原本要求「删掉该需求」，理由是「模型按构造已满足，这次 check 白花」。那是**成本
            # 论证，不是正确性论证** —— 而它与另外两条指令构成无解闭环：splitter prompt 说
            # containment 语言必须产出 containment 需求，评审员规则说只用效果迁移表示它属 material
            # omission。生产者产出 → 本门要求删 → 评审员要求加回 → 本门再拒，两侧预算都有限，
            # 结果不是死循环而是**整格隔离**。仓库已两次记录过这个形态。
            #
            # 激活面证实这不是理论风险：v21+v22 的 480 条 containment 绑定里 **302 条（63%）是自前缀
            # 形状**，v22 的 68 格中 32 格至少命中一次，单个需求集最多 11 条，而修复预算只有 5 次
            # 且与其它契约错误共用。
            #
            # 门要拦的位移由另外两支覆盖：`nl_parent` 缺失（无从判断来源）与 `nl_parent` 指向别处
            # （明知句子说的是另一层却绑在模型的摆放上）。「句子本来就说这一层」是**正确的需求**，
            # 只是这一条恰好由构造成立 —— 让它照常执行并返回 True，代价是一次无信息的 check，
            # 而拒绝它的代价是整格数据。
            continue
        else:
            # `nl_parent` names a different level than the binding uses -- so the producer knows
            # the sentence puts the element somewhere else, and bound the check to the model's
            # placement anyway. That is the displacement this gate exists to catch, stated
            # outright in the requirement's own field. Left unrefused it would be the one shape
            # that survives by *filling the field correctly*.
            findings.append(
                f"{rid} records `nl_parent={str(nl_parent).strip()!r}` but binds "
                f"containment(parent={parent!r}, child={child!r}) -- the binding uses the "
                "model's placement, not the level the sentence names. Bind "
                f"parent={str(nl_parent).strip()!r} and keep the declared path as `child`; "
                "the False that produces is the finding."
            )
    return tuple(findings)


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
                        "the sentence names. A proposal instead needs a "
                        "state_declared precondition that is False for that same "
                        "reason, which blocks the dependent and reports the missing "
                        "proposed name rather than the declared element the sentence "
                        "is about (step 2)"
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
        # Keyed as a permission rather than a prohibition; see
        # `anchors_at_initialization` for why, and for the sibling gate that now
        # shares the judgement.
        # The permission is the requirement's own `behavior_phase`, so it has to be checked
        # against something the requirement cannot restate -- otherwise a claim marked
        # `initialization` exempts itself, which is how `v6run3/0000-claude` published nothing.
        if anchors_at_initialization(
            getattr(item, "source_context", None)
        ) and _trigger_can_fire_from_initial(item):
            continue
        phase = str(
            getattr(getattr(item, "source_context", None), "behavior_phase", None) or ""
        ).lower()
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
                "initialization, and if the model happens to be wrong in that configuration "
                "the answer comes back true for a reason the sentence never asked about. "
                "Either name the running state the sentence is about (one requirement per "
                "state when the sentence does not pin one), or, if the sentence really "
                "is about power-on, set behavior_phase to \"initialization\" -- but that "
                "permission only holds when the trigger is one the machine can see before "
                "entering anything, and a trigger the machine can only see while running is "
                "not one of them."
            )
    return tuple(findings)


#: Predicates whose subject is a *run* and which name it `source` or `scope`. Derived from
#: `verification_kind_of` rather than listed by hand so a new predicate joins the right side
#: automatically. `cardinality`, `edge_declared`, `effect_declared` and
#: `guard_distinguishable` also bind one of those names but ask about what the model
#: *declares*, so the root is a legitimate subject there -- as it is for `containment` and
#: `initial_target`, which name their subject differently and so never reach this gate.
_RUN_SCOPED_BINDINGS = ("source", "scope")


def _binds_a_run(predicate: str) -> bool:
    from .predicates import PREDICATE_BY_NAME, verification_kind_of

    if predicate not in PREDICATE_BY_NAME:
        return False
    if verification_kind_of(predicate) == "structure":
        return False
    bindings = getattr(PREDICATE_BY_NAME[predicate], "bindings", {}) or {}
    return any(name in bindings for name in _RUN_SCOPED_BINDINGS)


def root_anchored_findings(
    requirements: Iterable[_RequirementSpec],
    model_root: str,
) -> tuple[str, ...]:
    """Behavioural requirements that anchor their claim at the model root.

    The root is where a run begins, so binding a behavioural `source` or `scope` to it makes
    the claim about the initial configuration -- the same question `[*]` asks, which
    `initialization_anchored_findings` already refuses. Pair 0000 round 1 took this spelling
    instead: `occupancy_after(source=<root>, target=FinalState, trigger=Power_Off)` was True
    because `[*] -> FinalState : /Power_Off` fires on the first tick, so the claim was true
    *because of* the defect it was meant to catch and the cell published nothing. Rounds 2
    and 3 bound the running modes and found it.

    Decided rather than reviewed, for the reason the sibling gates give: prose fires at a
    rate, and three rounds measured the comparable prompt rule at two times in four. Treating
    run-to-run variance with an instrument that is itself a random variable does not reduce
    it.

    Scoped to run-subject predicates on purpose. Twelve ledger assertions bind the bare root
    under `cardinality`, `containment` and `initial_target` and are correct to -- those ask
    what the model declares about itself, and no configuration is being assumed. The prompt
    says the same thing two steps earlier ("Their False *is* the finding"); a gate that
    contradicted it would leave the splitter arguing with itself across revisions, which is
    the failure this whole change exists to remove.

    :param requirements: the accepted requirement set.
    :param model_root: the model's own name, i.e. the single-segment declared path. Empty
        disables the gate rather than refusing everything, because a pair whose root cannot
        be determined is a reason to say nothing, not to reject every binding.
    :return: one finding per offending requirement.
    """
    if not model_root:
        return ()
    findings: list[str] = []
    for item in requirements:
        predicate = str(getattr(item, "predicate", "") or "")
        if not _binds_a_run(predicate):
            continue
        bindings = item.predicate_bindings or {}
        anchored = sorted(
            binding
            for binding in _RUN_SCOPED_BINDINGS
            # `[*]` belongs to `initialization_anchored_findings`. Two findings for one
            # binding would hand the splitter two instructions in the same round.
            if str(bindings.get(binding, "")).strip() == model_root
        )
        if anchored:
            findings.append(
                f"{item.requirement_id} binds {anchored} to the model root "
                f"{model_root!r}. A run starts at the root, so the claim is answered by "
                "what happens at power-on rather than by the behaviour the sentence is "
                "about, and if the model happens to be wrong there the answer comes back "
                "true for a reason the sentence never asked about. Name the running state the sentence "
                "is about. "
                "This applies to behavioural claims only: cardinality, containment and "
                "initial_target may take the root as their subject."
            )
    return tuple(findings)


#: Wording a splitter uses when it concedes the model never declared something the NL named.
_CONCESSION = re.compile(
    r"(未声明|没有.{0,8}声明|not declared|does not declare|no such|undeclared)"
)

#: The shapes a conceded name takes in this corpus, most specific first. The last two exist
#: because the concession is sometimes a bare NL phrase with no delimiters at all --
#: 「auto final 是 NL 提及的名称」 -- and that is the exact round pair 0050 lost.
_CONCEDED_NAME_PATTERNS = (
    re.compile(r"\b([a-z_]+_final_\d+(?:\.[A-Za-z_][\w]*)+)"),
    re.compile(r"\b([A-Z][A-Za-z]+(?:\.[A-Za-z_][\w]*)+)"),
    re.compile("[「(（\"']\\s*([A-Za-z_][\\w ]{2,40}?)\\s*[」)）\"']"),
    re.compile(r"\b([a-z][a-z0-9_]{3,}(?:_[a-z0-9]+)+)\b"),
    re.compile(r"([A-Za-z][\w ]{2,30}?)\s*是\s*NL\s*(?:提及|提到|点名)"),
    re.compile("名为\\s*['\"「]?([A-Za-z_][\\w ]{2,30}?)['\"」]?\\s*的"),
)

#: Tokens a concession mentions that are never the missing element: the four-step procedure it
#: cites by number, and the compiler-owned names it explicitly rules out as substitutes. Without
#: this the gate reads `step 4` as the missing name and refuses a requirement that did propose.
_NOT_A_CONCEDED_NAME = re.compile(
    r"^(step\s*\d+|步骤\s*\d+|第\s*\d+\s*步|R45RouteToken.*|declared_model_vocabulary.*"
    r"|compiler.*|initial_target|.*编译器.*)$",
    re.IGNORECASE,
)


#: A model element is an identifier, not prose. The parenthesised pattern above exists to catch
#: `'auto final'` -- a two-word NL phrase -- but a parenthesis in these limitations far more often
#: holds a diagnosis. `(terminating_transitions 为空)` was read as a missing element name on two
#: live rounds; the gate then told the splitter to assert that an element called
#: "terminating_transitions 为空" exists, which it cannot, and refused the requirement three
#: revisions running until `v7run2/0000-claude` ran out of budget and the cell was lost. Any CJK
#: character means the token is prose, not a name the NL used.
_HAS_CJK = re.compile(r"[\u3400-\u9fff\u3000-\u303f\uff00-\uffef]")

#: Vocabulary of the report itself, not of the specification. A limitation explains its reasoning
#: with predicate names and with the fields of the frozen input it consulted, and the snake_case
#: pattern happily reads those as element names -- `terminating_transitions 为空` yielded
#: `terminating_transitions`, an input field, once the CJK filter removed the prose around it.
_REPORTING_VOCABULARY = frozenset(PREDICATE_NAMES) | {
    # The binding slots themselves. `within_cycles` was read as a missing element on
    # `v8run2/0050-claude`, one generation after the CJK and predicate-name filters went in --
    # the same mistake wearing a third costume. Derived from the predicate table rather than
    # listed by hand so a new slot joins automatically.
    slot
    for predicate in PREDICATES
    for slot in getattr(predicate, "bindings", ()) or ()
} | {
    "terminating_transitions",
    "declared_model_vocabulary",
    "compiler_owned_variables",
    "attribution_exclusions",
    "known_model_paths",
    "predicate_bindings",
    "source_context",
    "behavior_phase",
    "initial_target",
    "source_segment_ids",
}


def _tail(name: str) -> str:
    """Compare names on their last segment, ignoring case, underscores and spaces.

    `auto final` in prose has to match `…AutonomousMode.auto_final` in a binding.
    """
    return name.strip().rsplit(".", 1)[-1].lower().replace("_", "").replace(" ", "")


def _conceded_names(text: str, declared_tails: frozenset[str]) -> tuple[str, ...]:
    """The names a concession says are missing, minus anything the model did declare.

    A concession usually names the substitute in the same breath -- 「声明的是 FinalWaittr_0005」
    -- and the substitute is declared, so subtracting the declared set leaves the missing one.
    """
    for pattern in _CONCEDED_NAME_PATTERNS:
        found = tuple(
            token
            for token in (str(match).strip() for match in pattern.findall(text))
            if token
            and not _NOT_A_CONCEDED_NAME.match(token)
            and not _HAS_CJK.search(token)
            and token.lower() not in _REPORTING_VOCABULARY
            and _tail(token) not in declared_tails
        )
        if found:
            return found
    return ()


def _batch_proposals(
    requirements: tuple[_RequirementSpec, ...], declared_tails: frozenset[str]
) -> frozenset[str]:
    """Every undeclared name the batch binds anywhere -- these are its step-4 proposals.

    Reading only the `*_declared` predicates is not enough: pair 0006 proposes
    `MissionComplete` through `persists_until(release=active("<path>"))`, and a narrower reading
    called that requirement a bare concession on three separate rounds.
    """
    out: set[str] = set()
    for item in requirements:
        for value in (item.predicate_bindings or {}).values():
            for token in re.findall(r"[A-Za-z_][\w.]*", str(value)):
                if "." not in token and not token[:1].isupper() and "_" not in token:
                    continue
                if _tail(token) not in declared_tails:
                    out.add(_tail(token))
    return frozenset(out)


def conceded_omission_findings(
    requirements: Iterable[_RequirementSpec],
    known_paths: Iterable[str],
) -> tuple[str, ...]:
    """Requirements that concede an omission in prose without asserting it anywhere.

    A rule kept in prose fails two ways. The familiar one is that it does not fire. The other
    is worse to find, because the trace looks correct: on `v5run1` the splitter wrote

        「auto final 是 NL 提及的名称;模型未声明此名的子状态,声明的是 FinalWaittr_0005」

    into `limitations` -- exactly the right observation, step 4's own trigger condition -- and
    then bound the behavioural claim to three sibling substates that do exist. Every assertion
    came back True and the cell published nothing at all. A note in `limitations` cannot come
    back False, so the omission goes unreported no matter how accurately the note describes it.

    The check is therefore on the model's own internal consistency, not on the requirement's
    prose: concede that a name the NL used is undeclared, and something in this batch has to
    *claim* it, where a claim is a binding the model never declared and can therefore fail.
    Taking the trigger from the self-report rather than from the sentence is what keeps this
    narrow -- no noun-phrase extraction from NL, nothing to tune per pair.

    Silent when no name can be pulled out of the concession: 115 of the corpus's 246 concessions
    are like that, and refusing them all would repeat the `substituted_binding` accident, where
    a gate with no legal move killed a cell within two rounds. Missing is the cheaper error.

    :param requirements: the accepted requirement set for one batch.
    :param known_paths: the elements the model declares.
    :return: one finding per requirement that concedes an omission it never asserts.
    """
    declared_tails = frozenset(_tail(str(path)) for path in known_paths if str(path).strip())
    if not declared_tails:
        return ()
    batch = tuple(requirements)
    proposals = _batch_proposals(batch, declared_tails)
    findings: list[str] = []
    for item in batch:
        concessions = tuple(
            str(entry)
            for entry in (getattr(item, "limitations", ()) or ())
            if _CONCESSION.search(str(entry))
        )
        if not concessions:
            continue
        missing = tuple(
            name for text in concessions for name in _conceded_names(text, declared_tails)
        )
        if not missing or any(_tail(name) in proposals for name in missing):
            continue
        findings.append(
            f"{item.requirement_id} records in `limitations` that the model never declared "
            f"{sorted(set(missing))[:2]}, and then asserts nothing about it. A note in "
            "`limitations` cannot come back False, so the omission the sentence points at goes "
            "unreported however accurately the note describes it. Step 4 applies: propose the "
            "name the NL used and assert its existence, so the claim can fail. Keep the note as "
            "well -- it explains the proposal -- but the note is not the finding."
        )
    return tuple(findings)


def trigger_consuming_predicate_findings(
    requirements: Iterable[_RequirementSpec],
    known_paths: Iterable[str],
) -> tuple[str, ...]:
    """`reaches` where the sentence names a declared event, and `occupancy_after` was available.

    `reaches(source, target, within_cycles)` has no `trigger` slot, so it asks "can the machine
    get there at all", and on a projected model the only path that answers yes may run through
    `R45RouteToken`. The attribution layer then rules the evidence compiler-owned, marks the
    finding `representation_debt`, and it is never published. `occupancy_after(source, trigger,
    target)` asks the sentence's actual question -- what happens *on this event* -- and its
    evidence is the author's own edge.

    Pair 0000 has lost rounds to this twice, `v6run2` and `v10run3`, both times on the same
    sentence (power off shall reach the final state) and both times because the splitter reached
    for `reaches`. `v10run3` was the single sub-70% round in the first fixed-configuration sample
    of six.

    Narrow on purpose, and the width is what makes it usable. A first attempt refused every
    behavioural predicate lacking a `trigger` slot and matched 109 requirements, 62 of them in
    pair 0050 -- a cell that scores 1/1/1 every round -- because `terminates` legitimately has no
    such slot. Requiring the predicate to be `reaches` *and* the trigger to be an element the
    model declares brings it to 5 corpus matches, all in pair 0000, all `Power_Off`, all inside
    the three rounds already known to have lost or nearly lost the cell to this. Nothing else in
    nineteen rounds matches.

    :param requirements: the accepted requirement set.
    :param known_paths: the elements the model declares.
    :return: one finding per requirement that should have consumed its trigger.
    """
    declared = {str(path).strip() for path in known_paths if str(path).strip()}
    if not declared:
        return ()
    findings: list[str] = []
    for item in requirements:
        if str(getattr(item, "predicate", "")) != "reaches":
            continue
        bindings = item.predicate_bindings or {}
        trigger = str(bindings.get("trigger") or getattr(item, "trigger", "") or "").strip()
        if not trigger or trigger not in declared:
            continue
        findings.append(
            f"{item.requirement_id} asks `reaches` while naming {trigger!r}, an event the model "
            "declares. `reaches` has no trigger slot, so it asks whether the target is reachable "
            "at all -- and on a projected model that question can be answered by the compiler's "
            "routing rather than by the author's edge, which makes the finding "
            "`representation_debt` and stops it being published. Use "
            "`occupancy_after(source=..., trigger=..., target=...)`: it asks what the sentence "
            "actually asks, and it answers from the edge the author wrote."
        )
    return tuple(findings)


#: 每种许可派生所要求的：父 Requirement 的谓词，以及父子之间必须相等的那一对绑定键。
#:
#: 这张表是「派生」这个概念的全部内容。它是闭集，加项要过 review —— 否则 `derivation`
#: 就从「一小组具名蕴含」退化成「绕过 NL 审查的任意口子」。
_LICENSED_DERIVATIONS: dict[str, tuple[str, str, str]] = {
    # kind: (父谓词, 父侧绑定键, 子侧绑定键)
    "entry_follows_cardinality": ("cardinality", "scope", "composite"),
    "activation_residency": ("event_consumed", "source", "source"),
}


def derivation_contract_findings(
    requirements: Iterable[_RequirementSpec],
) -> tuple[str, ...]:
    """申报为机械派生的 Requirement，其申报是否站得住。

    ## 这道门存在的理由：消解 splitter 与 reviewer 的直接冲突

    splitter 侧写着入口义务的触发器「is mechanical: it does not depend on recognising a phrasing」，
    而 reviewer 侧的常设指令是「不得因 FCSTM 暴露了方便的元素就添加语义区分」，且 reviewer
    **看不到**那条触发器（实测：该文本只在 splitter prompt 里，reviewer / converter / adjudicator
    全为 0 命中）。于是 reviewer 判「无 NL 出处 → 删」，`0032` 删掉 3/4 格、`0047` 删掉 5/6 格。

    **reviewer 按自己的规则是对的** —— 它无从分辨「凭 FCSTM 方便就加的义务」与「从一条
    NL-grounded 义务蕴含出来的义务」。差别无法从产物推断，只能由 splitter 申报。

    所以这道门不是给派生义务的免检通道，而是把 reviewer 面对的问题从**不可判定**（有没有 NL 出处）
    换成**可判定**（申报是否满足四条）。任一条不满足 → 仍然删，但 finding 点明是哪一条。

    ## 四条判据里这道门负责哪两条

    - (b) `kind` 在许可清单内 —— 由 `RequirementDerivation.kind` 的 `Literal` 承担
    - (c) 形状正确 —— 由 `Requirement` 的 before-validator 承担（`child` 从必填改为禁填）
    - **(a) 父存在、且父自身有 NL 出处** ← 本门
    - **(d) 父子绑定一致** ← 本门

    (a) 里「父自身有 NL 出处」这条不能省：允许派生之上再派生，等于让整条链没有 NL 地板，
    那正是 reviewer 原本担心的那件事。

    :param requirements: 已接受的需求集。
    :return: 每条申报不成立的派生义务一条 finding。
    """

    items = list(requirements)
    by_id = {str(getattr(item, "requirement_id", "")): item for item in items}
    findings: list[str] = []
    for item in items:
        derivation = getattr(item, "derivation", None)
        if derivation is None:
            continue
        kind = str(getattr(derivation, "kind", "") or "")
        parent_id = str(getattr(derivation, "parent_requirement_id", "") or "")
        rid = str(getattr(item, "requirement_id", ""))
        licensed = _LICENSED_DERIVATIONS.get(kind)
        if licensed is None:
            findings.append(
                f"{rid} declares derivation kind {kind!r}, which is not a licensed entailment. "
                f"Licensed kinds are {sorted(_LICENSED_DERIVATIONS)}. Either drop the derivation "
                f"and ground the requirement in an NL segment, or remove the requirement."
            )
            continue
        parent_predicate, parent_key, child_key = licensed
        parent = by_id.get(parent_id)
        if parent is None:
            findings.append(
                f"{rid} declares it is derived from {parent_id!r}, which is not a requirement in "
                f"this set. A derivation names the obligation it is entailed by; without that "
                f"obligation present there is nothing anchoring it to the NL."
            )
            continue
        if getattr(parent, "derivation", None) is not None:
            findings.append(
                f"{rid} is derived from {parent_id!r}, which is itself derived. A derivation chain "
                f"has no NL floor -- the parent must be a requirement an NL segment states. Point "
                f"{rid} at that requirement, or drop it."
            )
            continue
        actual_parent_predicate = str(getattr(parent, "predicate", "") or "")
        if actual_parent_predicate != parent_predicate:
            findings.append(
                f"{rid} declares a {kind!r} derivation, which is only entailed by a "
                f"`{parent_predicate}` obligation, but {parent_id!r} names "
                f"`{actual_parent_predicate or 'no predicate'}`. The entailment does not follow "
                f"from that parent."
            )
            continue
        parent_value = str((getattr(parent, "predicate_bindings", None) or {}).get(parent_key) or "").strip()
        child_value = str((getattr(item, "predicate_bindings", None) or {}).get(child_key) or "").strip()
        if not parent_value or parent_value != child_value:
            findings.append(
                f"{rid} binds `{child_key}={child_value or '<empty>'}` while its parent "
                f"{parent_id!r} binds `{parent_key}={parent_value or '<empty>'}`. The entailment is "
                f"only about the parent's own scope, so the two must name the same element; a "
                f"derived obligation on a different scope is a new claim and needs its own NL "
                f"source."
            )
    return tuple(findings)


def orphaned_covered_segments(
    disposition: Mapping[str, str],
    requirements: Iterable[_RequirementSpec],
) -> tuple[str, ...]:
    """标为 `covered` 却没有任何需求承接的 NL 段。

    ## 这是一个不变量，它有两个被破坏的时点

    `segment_disposition` 的 description 逐字写着「`covered` asserts that some Requirement here
    carries that segment's obligation」，`source_segment_ids` 的 description 也写着「every segment
    you mark `covered` … must be listed by at least one requirement here」。契约是断言式的。

    它能在两个地方被破坏：

    1. **生产者自己标错** —— 发出的集合本身不一致。
    2. **门的局部隔离摘掉了唯一承接者** —— 集合原本一致，隔离后不再一致。

    v37 实测：61 份需求集快照里 14 份有孤立段，**全部**伴随隔离；「孤立且无隔离」为 **0**。
    也就是说第 1 类在 v37 一次都没发生，全部来自第 2 类 —— 而上一代次只修了第 1 类。

    后果两种，都实测过：

    - **沉默漏检。** v36 `run1/0000-claude` 把 `NL-M006`（power off → final state）标 `covered`
      却无承接，于是 `coverage_status` 报 `full`、裁决说「All released assertions evaluated True」、
      零 issue —— 读起来像一次干净的完整通过。该格在上一代次是命中的。
    - **修订锁死直至丢格。** 评审发现它时给出的 finding 说「缺了一条需求」，而那**归责不到任何
      requirement id**，于是预算耗尽后隔离机制无人可摘、整格致命。v37 `run1/0057-gpt` 六次尝试
      全撞这一处，耗尽 `MAXTRY=6` —— 本项目已知的第一次丢格，`EIS-0057-01` 因此只有 5 位。

    ## 为什么是一个谓词、两处调用

    上一代次我在两个时点各打了一个补丁，第三条路径随即复发（同一个格连续三代次同根因）。
    所以规则只有这一处定义；调用点是「已接受集合发生变化」的地方，那是可穷举的，
    而不是「我想到的地方」。处置按语境不同（契约拒绝 vs 并进修订反馈），但判据同一份。

    :param disposition: `segment_disposition`，段 id -> 四种取值之一。
    :param requirements: 已接受的需求集。
    :return: 孤立的段 id，升序。
    """

    listed: set[str] = set()
    for requirement in requirements:
        for segment in getattr(requirement, "source_segment_ids", None) or ():
            listed.add(str(segment))
    return tuple(
        sorted(
            segment
            for segment, verdict in (disposition or {}).items()
            if str(verdict) == "covered" and str(segment) not in listed
        )
    )


#: 投影插入元素的名族。`exclusion_roles` 是更准的来源，但断言层拿不到 working contract，
#: 而这三族名是投影自己生成的、拼写稳定；这里只用来判「析取里混进了作者没写的东西」。
_INSERTED_NAME_FAMILIES = ("UnspecifiedInitial", "InvalidInitial", "FinalWait")


def short_circuited_primary_findings(
    requirement: Any, assertions: Any
) -> tuple[str, ...]:
    """Primary assertions whose declared predicate sits behind a short circuit.

    Gate D parses the expression text and passes when the predicate's name appears in it.  A
    producer that writes ``P(...) is True if all([...]) else False`` therefore satisfies the gate
    while ``P`` is **never actually called** -- the conditional collapses to the ``else`` branch.
    This is not hypothetical: v37 has a worked instance whose own rationale states the motive
    ("the public check shows a bare ``guard_distinguishable`` is not executable here").

    A gate that can be satisfied without asking the question it exists to enforce is worse than
    no gate: it reports compliance.  The check is purely syntactic -- the predicate must occur in
    a position that is evaluated unconditionally.

    provenance: Python 语言参考 §6.12–6.13（条件表达式与布尔运算的短路求值语义）——
    出现在源文本中不蕴含被求值。

    :param requirement: the Requirement whose predicate must be discharged.
    :param assertions: its assertions.
    :return: one finding per offending primary; empty when none.
    """

    predicate = str(getattr(requirement, "predicate", "") or "")
    if not predicate:
        return ()
    findings: list[str] = []
    for spec in assertions or ():
        if (getattr(spec, "role", "primary") or "primary") != "primary":
            continue
        expression = str(getattr(spec, "expression", "") or "")
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError:
            continue
        unconditional = _unconditional_call_names(tree.body)
        if predicate in _all_call_names(tree.body) and predicate not in unconditional:
            findings.append(
                f"{spec.assertion_id} names {predicate} only behind a short circuit "
                "(a conditional branch or a lazy boolean operand), so the call may never run "
                "and the claim would go unasked while the gate reports it discharged. Put the "
                f"{predicate} call in a position that is always evaluated."
            )
    return tuple(findings)


def _all_call_names(node: ast.AST) -> set[str]:
    return {
        child.func.id
        for child in ast.walk(node)
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name)
    }


def _unconditional_call_names(node: ast.AST) -> set[str]:
    """Call names in positions Python always evaluates."""

    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        names = {node.func.id}
        for argument in [*node.args, *(kw.value for kw in node.keywords)]:
            names |= _unconditional_call_names(argument)
        return names
    if isinstance(node, ast.IfExp):
        # Only the test is guaranteed to run.
        return _unconditional_call_names(node.test)
    if isinstance(node, ast.BoolOp):
        # Only the first operand is guaranteed to run.
        return _unconditional_call_names(node.values[0]) if node.values else set()
    if isinstance(node, ast.Compare):
        names = _unconditional_call_names(node.left)
        for comparator in node.comparators:
            names |= _unconditional_call_names(comparator)
        return names
    if isinstance(node, (ast.UnaryOp,)):
        return _unconditional_call_names(node.operand)
    if isinstance(node, (ast.BinOp,)):
        return _unconditional_call_names(node.left) | _unconditional_call_names(node.right)
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        names: set[str] = set()
        for element in node.elts:
            names |= _unconditional_call_names(element)
        return names
    return set()


_KIND_TO_EXISTENCE = {
    "state": "state_declared",
    "event": "event_declared",
    "variable": "variable_declared",
}


def unmatched_named_element_findings(requirement_set: Any) -> tuple[str, ...]:
    """Elements the sentence names, the model does not declare, and nobody asserted.

    `named_elements` records the diff in a typed slot; this closes it.  Every entry whose
    `declared_match` is null is a missing element by the producer's own tabulation, and a
    missing element the specification names is a finding on its own -- so it owes an existence
    Requirement bound to the proposed name.

    Why the check and not just the field: v40 put the same rule in prose and measured the
    result -- `event_declared` went from 4/36 to 23/35 cells but its calls stayed at 110 True
    against 17 False, because the producer wrote the predicate on names the model already
    declares.  The field records which side of the diff each name is on; this finding makes the
    null side load-bearing.

    provenance: IEEE 29148-2018 §5.2（规范点名的要素构成独立义务）。

    :param requirement_set: the produced `RequirementSet`.
    :return: one finding per unmatched element with no existence Requirement.
    """

    named = tuple(getattr(requirement_set, "named_elements", ()) or ())
    if not named:
        return ()
    covered: set[tuple[str, str]] = set()
    for requirement in getattr(requirement_set, "requirements", ()) or ():
        predicate = str(getattr(requirement, "predicate", "") or "")
        if predicate not in set(_KIND_TO_EXISTENCE.values()):
            continue
        for value in (getattr(requirement, "predicate_bindings", {}) or {}).values():
            covered.add((predicate, str(value)))
    findings: list[str] = []
    for element in named:
        if getattr(element, "declared_match", None):
            continue
        predicate = _KIND_TO_EXISTENCE[str(element.kind)]
        if (predicate, str(element.proposed_path)) in covered:
            continue
        findings.append(
            f"named_elements records {element.name_in_sentence!r} as a {element.kind} the "
            f"sentence names with no declared counterpart, but no Requirement asserts it: add "
            f"{predicate}(...) bound to {element.proposed_path!r}. Its False IS the finding -- "
            "an element the specification names and the model lacks is a defect on its own, "
            "separately from whatever the sentence goes on to say about it."
        )
    return tuple(findings)


def missing_presupposition_findings(
    requirements: Any, assertions: Any
) -> tuple[str, ...]:
    """Requirements that bind an event or variable without asserting it exists.

    Every predicate presupposes the elements it binds (see `predicates.presupposes`).  States
    already have a forced pre-scan in the splitter prompt; events and variables had **nothing**,
    and the measured cost is the largest single block in the needs layer: of the 91 v37 positions
    where the ledger's predicate was never written at all, 23 are `event_declared` and the
    sentence had named the stimulus outright.

    The pairing is required as `supporting`, never as `precondition`.  A false precondition makes
    the controller skip the primary (`status="blocked"`), and v37 has 135 primaries that were
    never asked for exactly that reason -- the missing element became the reason the real
    question went unasked.  Supporting evidence carries the same information and blocks nothing.

    provenance: 形式语义中的预设（presupposition）；IEEE 29148-2018 §5.2 —— 规范点名的要素本身
    构成一条独立于其行为的义务。

    :param requirements: accepted `Requirement` objects.
    :param assertions: the `AssertionSpec` objects written for them.
    :return: one finding per unpaired (requirement, binding); empty when all are paired.
    """

    by_requirement: dict[str, list[Any]] = {}
    for spec in assertions or ():
        by_requirement.setdefault(str(getattr(spec, "requirement_id", "")), []).append(spec)
    findings: list[str] = []
    for requirement in requirements or ():
        pairs = paired_presuppositions(str(getattr(requirement, "predicate", "")))
        if not pairs:
            continue
        bindings = dict(getattr(requirement, "predicate_bindings", {}) or {})
        written = " ".join(
            str(getattr(spec, "expression", "") or "")
            for spec in by_requirement.get(str(requirement.requirement_id), ())
        )
        for binding, existence in pairs:
            value = str(bindings.get(binding) or "").strip()
            if not value or value == "[*]":
                continue
            if f"{existence}(" in written and value in written:
                continue
            findings.append(
                f"{requirement.requirement_id} binds {binding}={value!r} but no assertion "
                f"claims it exists. Add a `supporting` assertion "
                f"{existence}(...) on {value!r}: naming an element asserts it exists, and that "
                "claim is separately violable. Use role=\"supporting\", not "
                "\"precondition\" -- a false precondition would make the controller skip the "
                "primary, so the missing element would become the reason the real question is "
                "never asked."
            )
    return tuple(findings)


def entry_disjunction_findings(
    requirements: Iterable[_RequirementSpec],
    assertions: Iterable[Any],
) -> tuple[str, ...]:
    """`entry_follows_cardinality` 展开的析取里混进了投影插入的占位符。

    ## 为什么这必须是一道门

    converter prompt 已经写了这条，连后果都预言对了：「including the placeholder makes the
    disjunction true exactly when entry has nowhere the author declared to go」。把占位符放进析取，
    析取**恰好在「作者没写任何入口」时为真** —— 那正是义务要抓的情形，于是缺陷被自己的检查掩盖。

    v36 实测：17 条析取里 2 条违规（`run1/0043-claude` 的 `AST-REQ-003-1` 与 `AST-REQ-002B-1` 含
    `PumpControl.UnspecifiedInitial`），实测真值 `True`。

    ⚠️ **那一次没造成损失，但那是运气**：`0043` 的 NL 点名了入口子态（"The system first transitions
    to the PumpState substate"），所以旁边有一条合法的单绑定 `initial_target` 取 False，缺陷靠它
    发布了。风险在 NL **不**点名入口子态的 pair —— 那里派生析取是唯一通路，混入占位符即完全掩盖。
    而那正是入口义务最需要生效的地方。

    这与 `derivation_contract_findings` 同一个道理：规则写在 prompt 里两代次都没稳定生效，
    改成不可表达或可机械检出才生效。

    :param requirements: 已接受的需求集。
    :param assertions: 断言脚本里的断言，需有 `requirement_id` 与 `expression`。
    :return: 每条含占位符的析取一条 finding。
    """

    derived = {
        str(getattr(item, "requirement_id", "")): item
        for item in requirements
        if getattr(getattr(item, "derivation", None), "kind", None)
        == "entry_follows_cardinality"
    }
    if not derived:
        return ()
    findings: list[str] = []
    for assertion in assertions:
        requirement_id = str(getattr(assertion, "requirement_id", "") or "")
        if requirement_id not in derived:
            continue
        expression = str(getattr(assertion, "expression", "") or "")
        if "any(" not in expression:
            continue
        offenders = sorted(
            {
                child
                for child in re.findall(r'child\s*=\s*"([^"]+)"', expression)
                if any(family in child for family in _INSERTED_NAME_FAMILIES)
            }
        )
        if offenders:
            findings.append(
                f"{getattr(assertion, 'assertion_id', '?')} expands the entry disjunction over "
                f"{offenders}, which the projection inserted rather than the author writing them. "
                "Including a placeholder makes the disjunction true exactly when entry has nowhere "
                "the author declared to go -- the obligation then passes on the artefact it was "
                "written to catch. Cover only the composite's declared non-pseudo children."
            )
    return tuple(findings)


def projection_anchored_findings(
    requirements: Iterable[_RequirementSpec],
    exclusions: Iterable[str],
) -> tuple[str, ...]:
    """Behavioural requirements whose `source`/`scope` is a projection artefact.

    The R4.5 projection adds elements the author never wrote -- a completion hold for a nested
    final state, a routing token -- and lists them in `attribution_exclusions`. Anchoring a
    behavioural claim at one of them asks what a run *starting there* does, and that run is
    the compiler's, not the author's. On pair 0050 the splitter bound
    `reaches(source=…FinalWaittr_0005, …)` for a sentence about a substate the model lacks; the
    projection really does route that node onward, so the claim was True and the cell published
    nothing.

    The third gate of this shape, after `initialization_anchored_findings` (`[*]`) and
    `root_anchored_findings` (the model root). All three refuse the same mistake -- asking
    about a configuration the sentence is not about -- and all three are decided here rather
    than reviewed, because prose fires at a rate: the prompt already forbids this binding by
    name and it still happened on one round in three.

    Deliberately narrow in two directions. Only behavioural predicates: a *declarative* claim
    about a projection artefact is legitimate, and `bind_attribution` was taught one generation
    earlier to treat such an element as an omission's own evidence -- the two rules have to
    agree. And only `source`/`scope`: reaching *into* a projected node is an observable fact
    about the machine, so refusing that would block real work.

    :param requirements: the accepted requirement set.
    :param exclusions: the working contract's `attribution_exclusions`.
    :return: one finding per offending requirement.
    """
    # `compiler:root:<ns>` is on the exclusion list too, but the root is not a projection
    # artefact -- the author wrote it. Anchoring a behavioural claim there is a real mistake and
    # `root_anchored_findings` already refuses it, with the structural-predicate exemptions that
    # decision needs. Folding the root in here would refuse `terminates(scope=<root>)` for a
    # sentence that really is about the whole system, which is why the first published
    # feasibility table reported "0 误伤" off a corpus that happened to exclude those cells.
    artefacts = {
        str(ref).rsplit(":", 1)[-1].strip()
        for ref in exclusions
        if str(ref).strip() and not str(ref).startswith("compiler:root:")
    }
    artefacts = {name for name in artefacts if name}
    if not artefacts:
        return ()
    findings: list[str] = []
    for item in requirements:
        predicate = str(getattr(item, "predicate", "") or "")
        if not _binds_a_run(predicate):
            continue
        bindings = item.predicate_bindings or {}
        anchored = sorted(
            binding
            for binding in _RUN_SCOPED_BINDINGS
            if str(bindings.get(binding, "")).strip() in artefacts
        )
        if anchored:
            findings.append(
                f"{item.requirement_id} binds {anchored} to "
                f"{str(bindings.get(anchored[0]))!r}, which the projection injected and the "
                "working contract excludes from attribution. A run anchored there is the "
                "compiler's, not the author's, so the claim comes back about the projection "
                "rather than about the behaviour the sentence describes. Bind a state the "
                "author wrote; if the sentence names an element the model lacks, propose that "
                "name and assert its existence instead of substituting a projected sibling."
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


#: Triggers that can legitimately fire from the pseudo-initial state. Matched on the last
#: segment, underscore-insensitively, so `llms_emp_feedback_final_0000.Power_On` counts.
_POWER_ON_HINTS = ("poweron", "start", "boot", "init", "reset")


def _trigger_can_fire_from_initial(item: _RequirementSpec) -> bool:
    """Whether this requirement's trigger is one the machine can see before entering anything.

    `anchors_at_initialization` answers "does the requirement *claim* to be about power-on",
    and that answer is correct as far as it goes. What it cannot answer is whether the claim is
    credible, because `behavior_phase` is filled in by the same splitter the gate constrains.

    `v6run3/0000-claude` is what that costs. It bound
    `occupancy_after(source="[*]", trigger=Power_Off, target=FinalState)` and marked the phase
    `initialization`; the gate saw the claim and stepped aside. The assertion then came back
    True -- because the model's `Power_Off` edge really is misanchored at `[*]`, which is the
    one defect pair 0000 exists to find -- and the cell published nothing.

    A self-report can be trusted when making it costs the reporter something. This one is free.
    So the permission is checked against something the splitter cannot restate: a run that
    starts at `[*]` begins before the machine has entered anything, and only a power-on event
    can fire there. `Power_Off` from the pseudo-initial is not a claim about the specification.

    Corpus check over all 19 rounds: 123 pseudo-initial bindings carry a power-on trigger or
    none and stay permitted; 23 carry `Power_Off`. Twenty-one of those 23 spell the phase
    `termination` and are already refused today -- this changes the answer for the two that
    spelled it `initialization`, `v1 run3/0000-claude` and `v6run3/0000-claude`.

    ⚠️ That check measured the wrong thing, and the sentence it produced -- "误伤面 0" -- is
    withdrawn. It ran over bindings the pipeline had *already produced*, so it reports how many
    existing bindings this gate would newly refuse. It cannot report which correct bindings the
    gate makes unwritable, because a shape no round ever wrote does not appear in the corpus.

    The frozen ledger has such a shape. `EIS-0047-03` says pair 0047 activates its collision
    subsystem unconditionally at power-on where the sentence requires a detection first, and both
    of its encodings bind `source="[*]"` with trigger `Collision_Detected`. That tail is not in
    `_POWER_ON_HINTS`, so **every** `behavior_phase` spelling is refused -- measured, eight of
    eight combinations, against `Power_On` permitted. The record is unreachable, and the corpus
    check saw nothing because no round had written it yet.

    So the word list is not a neutral credibility test: it encodes "only a power-on event can
    fire from the pseudo-initial", which is true of *runs* and false of *declarations* --
    `edge_declared` asks what the model declares, and a model may declare an edge out of `[*]`
    on any trigger at all. That is exactly the defect 0047 has. Narrowing the gate to the
    behavioural predicates is the obvious repair and is deliberately **not** made here: it would
    be a rule change motivated by a ledger record, in the middle of preparing a run. It is
    pre-registered instead (see `V21_PREREGISTERED_CALIBRE.md` §9.1), so a miss on that record
    in v22 is attributable to this gate rather than read as a capability gap.

    The general lesson is §3.5 clause 3's: a backtest measures collateral damage, only a live
    run measures generality. This is the second time that has cost something here.

    :param item: the requirement whose initialization claim is being checked.
    :return: whether the trigger is consistent with starting from the pseudo-initial.
    """
    bindings = item.predicate_bindings or {}
    trigger = str(bindings.get("trigger") or getattr(item, "trigger", "") or "").strip()
    if not trigger:
        return True
    tail = trigger.rsplit(".", 1)[-1].lower().replace("_", "")
    return any(hint in tail for hint in _POWER_ON_HINTS)


def anchors_at_initialization(source_context: Any) -> bool:
    """Whether the requirement's claim is about the initial configuration.

    One owner for a question two gates ask, because they used to answer it in
    opposite directions.  `initialization_anchored_findings` allows `[*]` on
    `source`/`scope` only where the phase claims `initialization`; the gate on
    source-blind `response_within` used to fire only where the phase spelled
    `operation` or `termination`.  Both bear on the same thing -- an
    initialization claim is legitimately about the configuration before anything
    has been entered, so it may bind the pseudo-initial and may leave `source`
    unbound; every other claim is about a running machine and may do neither.

    Keyed as a permission, in the direction the sibling gate already learned:
    `behavior_phase` is optional, and the prompts also offer `structure`, so a
    prohibition keyed on two spellings is dodged by any third value and by
    silence.  matrix-v16's prompts offered `unspecified` for exactly the field
    that would have switched the gate off.
    """

    # 同时接受 `RequirementSourceContext` 与裸 dict。
    #
    # 字段已迁成数据模型，但这个函数是**判据入口**，被门、测试和外部审计脚本各自调用；
    # 只认模型会让任何仍持 dict 的调用者静默拿到 False —— 而 False 在这里意味着「不是
    # initialization」，即**放宽**判定。判据入口的静默放宽比报错危险得多。
    phase = str(
        (
            source_context.get("behavior_phase")
            if isinstance(source_context, dict)
            else getattr(source_context, "behavior_phase", None)
        )
        or ""
    ).lower()
    return phase == "initialization"


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
