"""The predicate vocabulary a requirement claim may use, as one source of truth.

Why a vocabulary at all
-----------------------
The splitter used to emit a free-form statement plus a three-way
``verification_kind`` (``structure`` / ``behavior`` / ``property``), and the
controller derived the mandatory evidence family from that label.  Two problems
followed.  First, the label was the *only* machine-readable thing about a
requirement, so nothing checked that the assertion written for it actually tested
the claim: an ``edge_declared``-shaped query could close an
``occupancy_after``-shaped obligation, which is how a false positive survives.
Second, two different models classified the same sentence differently, because
the ordered decision was prose and had to be re-derived per sentence.

Naming the predicate fixes both.  The family -- and therefore the mandatory
evidence -- becomes a table lookup rather than a judgement, and the procedure a
converter must call becomes checkable against the predicate the splitter chose.

Reading the family column
-------------------------
``S`` the claim is about what the artifact *declares*; a structural or relational
      query decides it outright and is the correct evidence, not a compromise.
``B`` the claim is about what the model *does* at runtime; ``simulate`` is
      mandatory because a declaration existing does not mean it is reachable,
      enabled, or the thing that fires.  Static queries may only locate.
``P`` the claim is quantified over states, valuations or paths such that neither
      one query nor one finite run settles it; bounded model checking is
      mandatory.  When the domain is finitely enumerable the controller may
      instead expand it into ``B`` claims.

See issue #170 for the derivation, per-predicate implementation notes and the
infrastructure caveats.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass

FAMILY_STRUCTURE = "S"
FAMILY_BEHAVIOR = "B"
FAMILY_PROPERTY = "P"

#: Kept for the existing mandatory-evidence machinery, which is keyed by the
#: legacy three-way label.  It is now derived, never judged.
FAMILY_TO_VERIFICATION_KIND = {
    FAMILY_STRUCTURE: "structure",
    FAMILY_BEHAVIOR: "behavior",
    FAMILY_PROPERTY: "property",
}


@dataclass(frozen=True)
class Predicate:
    """One nameable claim shape, with the procedure that may discharge it."""

    name: str
    family: str
    #: What the predicate asserts, in one line, for the prompt.
    meaning: str
    #: The defect class it can expose.  A predicate that cannot expose anything
    #: has no business in the vocabulary.
    proves: str
    #: Required binding names.  The splitter must supply all of them.
    bindings: tuple[str, ...]
    #: How strong the answer is.  This is what the producer needs to reason
    #: about; the mechanism that produces it is not.
    strength: str
    #: The evidence call that decides it.  Internal bookkeeping only -- never
    #: rendered into a prompt, because naming a mechanism the producer cannot
    #: call only invites it to try.
    procedure: str
    #: The bare function name inside ``procedure``.  The prose form is for the
    #: prompt; this is what the gate compares against the assertion's parsed
    #: call names, so an easier query cannot close a harder claim.
    procedure_function: str
    #: Optional weaker evidence, allowed only as ``supporting``.
    locators: tuple[str, ...] = ()
    #: Honest statement of what the current infrastructure cannot do.
    caveat: str = ""
    #: Per-binding format spec: (binding, what it must contain).  Prose about a
    #: field is not enough -- a producer that cannot see a field's domain guesses
    #: it, and a guessed literal fails at precheck.
    field_specs: tuple[tuple[str, str], ...] = ()
    #: At least three worked calls per predicate, covering the shapes that
    #: actually occur: the typical case, a literal or special-binding variant,
    #: and a case whose answer is False -- often a name the model does not
    #: declare, since that is the shape a precondition is written for.
    examples: tuple[str, ...] = ()


PREDICATES: tuple[Predicate, ...] = (
    # ---- Family S: artifact declarations -------------------------------
    Predicate(
        "state_declared",
        FAMILY_STRUCTURE,
        "the model declares a state at this path, of this kind",
        "missing or spurious state; a composite written as a leaf",
        ("state", "kind"),
        "decides the declaration outright",
        "states(path=..., exact=True)",
        "states",
        field_specs=(
            ('state', 'a declared state path, copied verbatim from declared_model_vocabulary'),
            ('kind', 'one of "leaf" (no substates), "composite" (has substates), "pseudo" (an initial/final marker), or "any" (declared at all)'),
        ),
        examples=(
            'state_declared(state="Sys.ModeA", kind="leaf")  # a simple operating mode',
            'state_declared(state="Sys.Outer", kind="composite")  # a mode with substates',
            'state_declared(state="Sys.Ghost", kind="any")  # only asks whether it exists at all',
        ),
    ),
    Predicate(
        "variable_declared",
        FAMILY_STRUCTURE,
        "the model declares a variable of the author's own under this name",
        "a quantity the NL requires that the model has no variable for",
        ("variable",),
        "decides the declaration outright",
        "variables(name=...)",
        "variables",
        caveat=(
            "Route-control variables the converter generated are not counted: the "
            "effect facade drops them from every answer, so reporting one as "
            "declared would promise evidence no other call can deliver."
        ),
        field_specs=(
            (
                "variable",
                'the BARE variable name, with no state-path prefix -- variables are '
                'declared outside the state tree. Either a name copied from the '
                '`variables` list in declared_model_vocabulary, or the name the '
                'Requirement proposes for a variable the model should have declared; '
                'a dotted name is refused, not answered',
            ),
        ),
        examples=(
            'variable_declared(variable="units")  # True when the author declared it',
            'variable_declared(variable="unit_count")  # False when the model declares no such variable',
            'variable_declared(variable="Sys.units")  # raises: variables take no path prefix',
        ),
    ),
    Predicate(
        "event_declared",
        FAMILY_STRUCTURE,
        "the model declares an event at this qualified path",
        "an event the NL names that the model never declares",
        ("event",),
        "decides the declaration outright",
        "events(path=...)",
        "events",
        field_specs=(
            (
                "event",
                'the FULLY QUALIFIED event path, as `<root>.<event>` -- either copied '
                'from the `events` list in declared_model_vocabulary, or the path the '
                'Requirement proposes for an event the model should have declared; a '
                'bare name with no dot is refused, not answered',
            ),
        ),
        examples=(
            'event_declared(event="Sys.evt")  # True when the author declared it',
            'event_declared(event="Sys.missing")  # False when the model declares no such event',
            'event_declared(event="evt")  # raises: events take the qualified path',
        ),
    ),
    Predicate(
        "containment",
        FAMILY_STRUCTURE,
        "this child is (or is not) a substate of this parent",
        "misplaced substate; a region attached to the wrong parent",
        ("parent", "child"),
        "decides the declaration outright",
        "states(parent=..., recursive=False)",
        "states",
        field_specs=(
            ('parent', 'the declared enclosing state'),
            ('child', 'the declared state that must be a DIRECT substate of parent; a grandchild answers False'),
        ),
        examples=(
            'containment(parent="Sys.Outer", child="Sys.Outer.Inner")  # direct child',
            'containment(parent="Sys.Outer", child="Sys.Outer.Inner.Deep")  # False: not direct',
            'containment(parent="Sys", child="Sys.Outer")  # top-level containment',
        ),
    ),
    Predicate(
        "initial_target",
        FAMILY_STRUCTURE,
        "entering this composite starts in this child",
        "wrong or missing initial child; entry lands in the wrong mode",
        ("composite", "child"),
        "decides the declaration outright",
        "initial_child(...)",
        "initial_child",
        field_specs=(
            ('composite', 'the declared composite whose entry is claimed'),
            ('child', 'the declared substate that entry must land on'),
        ),
        examples=(
            'initial_target(composite="Sys.Outer", child="Sys.Outer.Inner")',
            'initial_target(composite="Sys", child="Sys.ModeA")  # root entry',
            'initial_target(composite="Sys.Outer", child="Sys.Outer.Other")  # False when entry lands elsewhere',
        ),
    ),
    Predicate(
        "edge_declared",
        FAMILY_STRUCTURE,
        "the model declares an edge with this source, trigger and target",
        "a missing or wrongly-targeted declared transition",
        ("source", "trigger", "target"),
        "decides the declaration outright",
        "transition_exists(source=..., event=..., target=...)",
        "transition_exists",
        caveat=(
            "Use this only when the NL speaks about the model containing an "
            "edge.  'When X happens the system moves to Y' is a runtime claim: "
            "use occupancy_after, because a declared edge may be unreachable or "
            "guard-blocked."
        ),
        field_specs=(
            ('source', 'the declared source state, or "[*]" for the pseudo-initial'),
            ('trigger', 'the declared event path that labels the edge'),
            ('target', 'the declared target state'),
        ),
        examples=(
            'edge_declared(source="Sys.ModeA", trigger="Sys.evt", target="Sys.ModeB")',
            'edge_declared(source="[*]", trigger="Sys.on", target="Sys.ModeA")  # the initial edge',
            'edge_declared(source="Sys.ModeA", trigger="Sys.evt", target="Sys.Other")  # False when the edge points elsewhere',
        ),
    ),
    Predicate(
        "effect_declared",
        FAMILY_STRUCTURE,
        "this transition declares an effect on this variable, in this direction",
        "a missing or wrong-signed declared effect",
        ("source", "trigger", "variable", "sign"),
        "decides the declaration outright",
        "effect_deltas(source=..., event=...)",
        "effect_deltas",
        locators=("effects(...)",),
        field_specs=(
            ('source', 'the declared source state of the transition carrying the effect'),
            ('trigger', 'the declared event path'),
            ('variable', "the variable's BARE name, with no state-path prefix -- either copied from the `variables` list in declared_model_vocabulary, or the name the Requirement proposes for a variable the model should have declared"),
            ('sign', '"negative" for a decrease, "positive" for an increase'),
        ),
        examples=(
            'effect_declared(source="Sys.ModeA", trigger="Sys.done", variable="units", sign="negative")',
            'effect_declared(source="Sys.ModeA", trigger="Sys.add", variable="units", sign="positive")',
            'effect_declared(source="Sys.ModeA", trigger="Sys.done", variable="unit_count", sign="negative")  # False when the model declares no variable under that name',
        ),
    ),
    Predicate(
        "action_declared",
        FAMILY_STRUCTURE,
        "this state declares an entry, exit or during action",
        "a missing declared action; an action attached to the wrong phase",
        ("state", "phase"),
        "decides the declaration outright",
        "states(path=..., exact=True)",
        "states",
        caveat=(
            "Reports whether the phase declares any action at all, not what "
            "the action does."
        ),
        field_specs=(
            ('state', 'the declared state whose action is claimed'),
            ('phase', '"entry", "exit", or "during"'),
        ),
        examples=(
            'action_declared(state="Sys.ModeA", phase="entry")',
            'action_declared(state="Sys.ModeA", phase="exit")',
            'action_declared(state="Sys.ModeB", phase="during")  # False when no during action is declared',
        ),
    ),
    Predicate(
        "guard_distinguishable",
        FAMILY_STRUCTURE,
        "a shared source and trigger cannot reach two targets indistinguishably",
        "non-determinism: overlapping or absent discriminating guards",
        ("source", "trigger"),
        "decides it over every variable valuation",
        "conflicting_targets(source=..., event=...)",
        "conflicting_targets",
        locators=("guards_overlap(...)",),
        field_specs=(
            ('source', 'the declared source state the alternatives leave from'),
            ('trigger', 'the declared shared event path; raises when no transition leaves source on it'),
        ),
        examples=(
            'guard_distinguishable(source="Sys.Hub", trigger="Sys.pick")  # True when guards separate the targets',
            'guard_distinguishable(source="Sys.Hub", trigger="Sys.route")  # False when two targets share an empty guard',
            'guard_distinguishable(source="Sys.Leaf", trigger="Sys.pick")  # raises: no such transition, so undecidable',
        ),
    ),
    Predicate(
        "cardinality",
        FAMILY_STRUCTURE,
        "this scope declares exactly this many non-pseudo states",
        "a missing or duplicated mode in an enumerated set",
        ("scope", "count"),
        "decides the declaration outright",
        "states(...)",
        "states",
        field_specs=(
            ('scope', 'the declared enclosing state whose DIRECT substates are counted'),
            ('count', 'an integer; pseudo-states are not counted'),
        ),
        examples=(
            'cardinality(scope="Sys.Outer", count=3)  # exactly three direct modes',
            'cardinality(scope="Sys", count=2)  # top level',
            'cardinality(scope="Sys.Outer", count=4)  # False when only three are declared',
        ),
    ),
    # ---- Family B: runtime behaviour ------------------------------------
    Predicate(
        "occupancy_after",
        FAMILY_BEHAVIOR,
        "after this trigger from this state, the system is in this target",
        "wrong target; a local exit written as global completion; a declared "
        "edge that is guard-blocked or unreachable at runtime",
        ("source", "trigger", "target"),
        "one bounded witness: it shows what this configuration does, not what every run does",
        "simulate(...).final.is_active(...)",
        "simulate",
        locators=("transition_exists(...)", "path(...)"),
        field_specs=(
            ('source', 'the configuration the claim is about, or "[*]" for power-on / first entry'),
            ('trigger', 'the declared event path; the predicate also verifies this event was actually consumed'),
            ('target', 'the declared state; occupying any leaf inside a composite target counts'),
            ('within_cycles', 'how many cycles to run; default 1'),
        ),
        examples=(
            'occupancy_after(source="Sys.ModeA", trigger="Sys.evt", target="Sys.ModeB")',
            'occupancy_after(source="[*]", trigger="Sys.on", target="Sys.ModeA")  # power-on claim',
            'occupancy_after(source="Sys.ModeA", trigger="Sys.evt", target="Sys.Outer", within_cycles=2)  # composite target, two cycles',
        ),
    ),
    Predicate(
        "event_consumed",
        FAMILY_BEHAVIOR,
        "in this configuration the event is actually consumed",
        "a dangling event no transition consumes; an event silently ignored in "
        "the state where the NL requires a response",
        ("source", "trigger"),
        "one bounded witness",
        "simulate(...).cycles[...].consumed_events",
        "simulate",
        caveat=(
            "There is no static substitute: an event being declared does not "
            "mean any configuration accepts it."
        ),
        field_specs=(
            ('source', 'the configuration the event is offered in'),
            ('trigger', 'the declared event path'),
        ),
        examples=(
            'event_consumed(source="Sys.ModeA", trigger="Sys.evt")  # True when some transition accepts it here',
            'event_consumed(source="[*]", trigger="Sys.on")',
            'event_consumed(source="Sys.ModeB", trigger="Sys.evt")  # False when the event is silently ignored here',
        ),
    ),
    Predicate(
        "stays_in",
        FAMILY_BEHAVIOR,
        "after this trigger the system remains in the same state",
        "an event that should be ignored causes a transition; a required "
        "self-loop is missing",
        ("source", "trigger"),
        "one bounded witness",
        "simulate(...) consumed_events and final.is_active(source)",
        "simulate",
        field_specs=(
            ('source', 'the configuration that must not change'),
            ('trigger', 'the declared event path; the predicate requires it be consumed AND the state unchanged'),
        ),
        examples=(
            'stays_in(source="Sys.ModeA", trigger="Sys.noop")  # True only for a declared self-loop',
            'stays_in(source="Sys.ModeA", trigger="Sys.evt")  # False when the event moves the system',
            'stays_in(source="Sys.ModeA", trigger="Sys.other")  # False when this declared event is simply ignored here, so no self-loop exists',
        ),
    ),
    Predicate(
        "variable_delta_after",
        FAMILY_BEHAVIOR,
        "running this trigger changes this variable in this direction",
        "an effect is declared but the executed path never reaches it: "
        "declaration and runtime disagree",
        ("source", "trigger", "variable", "sign"),
        "one bounded witness",
        "simulate(...).cycles[...].variables",
        "simulate",
        locators=("effect_deltas(...)",),
        field_specs=(
            ('source', 'the configuration the run starts from'),
            ('trigger', 'the declared event path; the predicate verifies it was consumed'),
            ('variable', "the variable's BARE name -- declared, or proposed by the Requirement"),
            ('sign', '"negative" or "positive"'),
        ),
        examples=(
            'variable_delta_after(source="Sys.ModeA", trigger="Sys.done", variable="units", sign="negative")',
            'variable_delta_after(source="Sys.ModeA", trigger="Sys.add", variable="units", sign="positive")',
            'variable_delta_after(source="Sys.ModeA", trigger="Sys.done", variable="unit_count", sign="negative")  # False when the model declares no variable under that name',
        ),
    ),
    Predicate(
        "reaches",
        FAMILY_BEHAVIOR,
        "within a bounded number of cycles this target is reachable from here",
        "an unreachable target: a broken chain or dead branch",
        ("source", "target", "within_cycles"),
        "one bounded witness, and it ignores triggers",
        "simulate(...) multi-cycle",
        "simulate",
        locators=("path(...)",),
        caveat=(
            "Reachability here is a bounded witness, not a proof: it runs the "
            "model forward and reports whether the target was occupied within "
            "the cycle budget. It ignores triggers, so it cannot stand in for "
            "occupancy_after."
        ),
        field_specs=(
            ('source', 'the configuration to start from'),
            ('target', 'the declared state to reach'),
            ('within_cycles', 'cycle budget; default 3. Every declared event is offered each cycle, so this ignores which trigger caused it'),
        ),
        examples=(
            'reaches(source="Sys.ModeA", target="Sys.Final", within_cycles=3)',
            'reaches(source="[*]", target="Sys.ModeB", within_cycles=5)',
            'reaches(source="Sys.ModeA", target="Sys.Dead", within_cycles=3)  # False: unreachable within the budget',
        ),
    ),
    Predicate(
        "terminates",
        FAMILY_BEHAVIOR,
        "the model actually finishes",
        "premature or impossible completion: the final state is unreachable, "
        "or the path to it is guard-blocked",
        ("scope",),
        "one bounded witness",
        "simulate(...).final.is_ended",
        "simulate",
        locators=("topology(...)",),
        field_specs=(
            ('scope', 'the configuration to start from, or "[*]" for a cold start'),
            ('trigger', 'optional; when given only that event is offered, otherwise every declared event is'),
        ),
        examples=(
            'terminates(scope="Sys.ModeB", trigger="Sys.off")  # does this event finish the model',
            'terminates(scope="[*]")  # can the model finish at all from a cold start',
            'terminates(scope="Sys.ModeA")  # False when no run from here reaches a final state',
        ),
    ),
    # ---- Family P: quantified properties --------------------------------
    Predicate(
        "invariant",
        FAMILY_PROPERTY,
        "within the bound this condition always holds",
        "a violated mutual exclusion; a reachable unsafe state; a broken "
        "never/always constraint",
        ("scope", "condition", "bound"),
        "holds for every run up to the bound, and says nothing beyond it",
        "fbmcq('check invariant <= k: ...')",
        "fbmcq",
        caveat=(
            "Writing !(active(A) && active(B)) for siblings of one sequential "
            "region is a tautology and proves nothing.  Only holds is False is "
            "a violation; a non-terminal status is invalid, never False."
        ),
        field_specs=(
            ('scope', 'the declared state the run starts in'),
            ('condition', 'an FCSTM boolean expression such as !active("Sys.Fault"); NOT a bare state path'),
            ('bound', 'how many steps to check; default 5. Larger bounds cost exponentially more'),
        ),
        examples=(
            'invariant(scope=\'Sys.ModeA\', condition=\'!active("Sys.Fault")\', bound=4)',
            'invariant(scope=\'[*]\', condition=\'!active("Sys.Fault") && !active("Sys.Dead")\', bound=3)',
            'invariant(scope=\'Sys.ModeA\', condition=\'!active("Sys.ModeB")\', bound=2)  # False when ModeB is reachable in two steps',
        ),
    ),
    Predicate(
        "response_within",
        FAMILY_PROPERTY,
        "every occurrence of this trigger is answered within the bound; `response` is the state path that counts as the answer, not an expression",
        "a missing or conditional response to a mandatory trigger",
        ("trigger", "response", "bound"),
        "holds for every run up to the bound, and says nothing beyond it",
        "fbmcq('check response <= k: ...')",
        "fbmcq",
        field_specs=(
            ('trigger', 'the declared event path that creates the obligation'),
            ('response', 'the declared STATE PATH that counts as the answer; not an expression'),
            ('bound', 'step horizon; default 5'),
            ('source', 'the configuration the obligation is about; supply it, or the event is offered where nothing can consume it'),
        ),
        examples=(
            'response_within(trigger="Sys.evt", response="Sys.ModeB", bound=3, source="Sys.ModeA")',
            'response_within(trigger="Sys.on", response="Sys.ModeA", bound=2, source="[*]")',
            'response_within(trigger="Sys.evt", response="Sys.Never", bound=3, source="Sys.ModeA")  # False: no run answers in time',
        ),
    ),
    Predicate(
        "persists_until",
        FAMILY_PROPERTY,
        "this state holds continuously until this release condition",
        "premature exit from a state that must persist",
        ("state", "release", "bound"),
        "holds for every run up to the bound, and says nothing beyond it",
        "fbmcq('check exists_always <= k: ...')",
        "fbmcq",
        caveat=(
            "Infeasible on the pairs where formula construction exceeds budget; "
            "expand into B-family claims when the domain is enumerable."
        ),
        field_specs=(
            ('state', 'the declared state that must hold'),
            ('release', 'an FCSTM boolean expression that ends the obligation, such as active("Sys.Done")'),
            ('bound', 'step horizon; default 5'),
        ),
        examples=(
            'persists_until(state=\'Sys.Hold\', release=\'active("Sys.Done")\', bound=4)',
            'persists_until(state=\'Sys.Search\', release=\'active("Sys.Found")\', bound=3)',
            'persists_until(state=\'Sys.Hold\', release=\'active("Sys.Done")\', bound=2)  # False when the run can leave Hold early',
        ),
    ),
)

PREDICATE_BY_NAME = {item.name: item for item in PREDICATES}
_ALL_PROCEDURE_FUNCTIONS = frozenset(item.procedure_function for item in PREDICATES)
PREDICATE_NAMES = frozenset(PREDICATE_BY_NAME)
#: Declaration order, for building a stable Literal in the schema.
PREDICATE_ORDER: tuple[str, ...] = tuple(item.name for item in PREDICATES)


def family_of(predicate: str) -> str | None:
    """Return the family of a predicate name, or ``None`` when unknown."""

    entry = PREDICATE_BY_NAME.get(predicate)
    return entry.family if entry is not None else None


def verification_kind_of(predicate: str) -> str | None:
    """Derive the legacy three-way label from a predicate name.

    This replaces the prose ordered decision the splitter used to apply per
    sentence, which is why two models disagreed on the same requirement.
    """

    family = family_of(predicate)
    return FAMILY_TO_VERIFICATION_KIND.get(family) if family else None


#: Optional keyword arguments beyond the required bindings, with the runtime
#: default, so the signature shown to the producer is the real one.
PREDICATE_OPTIONS: dict[str, tuple[str, ...]] = {
    "occupancy_after": ("within_cycles: int = 1",),
    "reaches": ("within_cycles: int = 3",),
    "terminates": ("trigger: str | None = None",),
    "invariant": ("bound: int = 5",),
    "response_within": ("bound: int = 5", "source: str | None = None"),
    "persists_until": ("bound: int = 5",),
}

#: Binding names whose value is one of a fixed value list, not a model element.
FREE_FORM_BINDINGS = frozenset(
    {"kind", "sign", "phase", "count", "bound", "condition", "release"}
)

#: The literal value lists, rendered into the signature so the producer never
#: has to guess and the reviewer never has to reject a legal literal.
_LITERAL_ARGS = {
    "count": "count: int",
    "kind": 'kind: "leaf"|"composite"|"pseudo"|"any"',
    "sign": 'sign: "negative"|"positive"',
    "phase": 'phase: "entry"|"exit"|"during"',
    "condition": "condition: str",
    "release": "release: str",
    "bound": "bound: int",
    "within_cycles": "within_cycles: int",
}


def signature_of(name: str) -> str:
    """Render the exact callable signature of one predicate."""

    entry = PREDICATE_BY_NAME[name]
    args = [_LITERAL_ARGS.get(b, f"{b}: str") for b in entry.bindings]
    listed = set(entry.bindings)
    args.extend(
        opt
        for opt in PREDICATE_OPTIONS.get(name, ())
        if opt.split(":")[0].strip() not in listed
    )
    return f"{name}({', '.join(args)}) -> bool"


#: The predicates that ask whether the model declares an element at all.
#: A False from one of these is not a vacuous pass but the answer: nothing was
#: looked up and found empty, the question *was* "is it there".  So a name absent
#: from the frozen model is legitimate in exactly these calls, whatever role the
#: assertion carries -- which is what lets a requirement whose own predicate is an
#: existence check be discharged by one assertion instead of a precondition plus a
#: byte-identical dependent.
EXISTENCE_PREDICATES = frozenset(
    {"state_declared", "variable_declared", "event_declared"}
)


def accepted_bindings(name: str) -> frozenset[str]:
    """Every keyword one predicate accepts: required bindings plus its options."""

    entry = PREDICATE_BY_NAME[name]
    optional = {
        opt.split(":")[0].strip() for opt in PREDICATE_OPTIONS.get(name, ())
    }
    return frozenset(entry.bindings) | optional


def misspelled_binding_findings(expression: str) -> tuple[str, ...]:
    """Return predicate calls that pass a keyword the predicate does not accept.

    At runtime this is a `TypeError`, which the controller cannot dispatch on --
    but the static gates run first, and they mis-diagnose it.  `variable_declared`
    was briefly spelled with a `name=` keyword; a script written that way had its
    proposed name invisible to the reference gate, which then reported the
    *dependent* assertion as holding an unresolved reference.  The producer was
    told to fix a name that was correct, in an assertion that was correct, while
    the actual typo sat one line above.

    Naming the accepted keywords turns that into one round.

    :param expression: the assertion's terminal Python expression.
    :return: one finding per offending call; empty when every keyword is accepted.
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
    findings: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        called = node.func.id
        if called not in PREDICATE_BY_NAME:
            continue
        allowed = accepted_bindings(called)
        unknown = sorted(
            str(keyword.arg)
            for keyword in node.keywords
            if keyword.arg is not None and keyword.arg not in allowed
        )
        if unknown:
            findings.append(
                f"{called} does not accept {unknown}; its bindings are "
                f"{sorted(allowed)}"
            )
    return tuple(dict.fromkeys(findings))


def binding_examples(name: str) -> tuple[tuple[str, str], ...]:
    """Re-emit each worked call of ``name`` as the JSON binding dict.

    The requirement stages write `predicate_bindings`, the assertion stages
    write a call, and the two must agree on every value.  Deriving the dict form
    from the call form by parsing it makes that agreement structural rather than
    a thing two prompt authors have to keep in step by hand.  Values are
    stringified because that is what the schema stores.

    :param name: predicate name.
    :return: ``(json_object, note)`` per example; the note is the call's comment.
    """

    entry = PREDICATE_BY_NAME[name]
    rendered: list[tuple[str, str]] = []
    for example in entry.examples:
        call, _, note = example.partition("  # ")
        node = ast.parse(call.strip(), mode="eval").body
        assert isinstance(node, ast.Call)  # noqa: S101 - table is ours, checked in tests
        pairs = {
            kw.arg: str(ast.literal_eval(kw.value))
            for kw in node.keywords
            if kw.arg is not None
        }
        rendered.append((json.dumps(pairs, ensure_ascii=False), note.strip()))
    return tuple(rendered)


def vocabulary_prompt() -> str:
    """Render the vocabulary for the requirement stages.

    Says what each predicate decides, what defect it exposes, and how strong the
    answer is.  It deliberately does not say how any of them is computed: the
    requirement stages choose a claim shape, and the mechanism is not theirs to
    reason about.
    """

    lines = [
        "Predicate vocabulary. Every claim must name exactly one predicate from "
        "this closed list. The family, and therefore the evidence the controller "
        "requires, follows from the predicate -- you do not choose it.",
        "",
        "How the bindings look, one per family:",
        '  state_declared   -> {"state": "Sys.ModeA", "kind": "leaf"}',
        '  occupancy_after  -> {"source": "Sys.ModeA", "trigger": "Sys.evt", "target": "Sys.ModeB"}',
        '  invariant        -> {"scope": "Sys.ModeA", "condition": "!active(\\"Sys.Fault\\")", "bound": "4"}',
        "",
        "Every binding the predicate lists must be present, and every value that "
        "names a model element is a name: copied verbatim from "
        "`declared_model_vocabulary` when the model declares it, or -- when the "
        "sentence requires an element this model does not declare -- the name that "
        "element should have, taken from the sentence's own wording, together with "
        "a `limitations` entry recording that the model declares nothing under it. "
        'Do not substitute a different declared element that happens to fit the '
        'slot. "[*]" is the initial configuration, so a requirement binding it to '
        '`source` or `scope` -- including the signature examples below that do so -- '
        'is a claim anchored at power-on and must carry '
        '`source_context.behavior_phase = "initialization"`. That is true even when '
        'the claim is about the run ending: `terminates(scope="[*]")` asks whether a '
        'cold start can finish, and the anchor is still the initial configuration. '
        'Any other phase there is refused, because anchoring a running-system claim '
        'before the machine has entered anything asks a different question -- and on '
        'a model whose defect is an edge leaving the pseudo-initial, it asks one that '
        'is true because of the defect. The remaining bindings take one '
        "of the literal values shown in the signature.",
    ]
    for family, title in (
        (
            FAMILY_STRUCTURE,
            "Family S -- claims about what the model declares. Answered from the "
            "declarations, which is the correct evidence for them, not a shortcut.",
        ),
        (
            FAMILY_BEHAVIOR,
            "Family B -- claims about what the model does when it runs.",
        ),
        (
            FAMILY_PROPERTY,
            "Family P -- claims quantified over runs, checked up to a bound.",
        ),
    ):
        lines.append(f"\n{title}")
        for item in PREDICATES:
            if item.family != family:
                continue
            lines.append(f"- `{signature_of(item.name)}`")
            lines.append(f"    asserts: {item.meaning}")
            lines.append(f"    exposes: {item.proves}")
            lines.append(f"    strength: {item.strength}")
            if item.caveat:
                lines.append(f"    boundary: {item.caveat}")
            lines.append("    bindings, each required:")
            for binding, spec in item.field_specs:
                lines.append(f"      - {binding}: {spec}")
            lines.append("    predicate_bindings examples:")
            for payload, note in binding_examples(item.name):
                suffix = f"   # {note}" if note else ""
                lines.append(f"      {payload}{suffix}")
    return "\n".join(lines)


def callable_prompt() -> str:
    """Render the callable reference for the assertion stages.

    Signature, what it decides, how strong the answer is, where it stops, and a
    worked example.  Nothing about how it is implemented -- an assertion cannot
    reach the mechanism, so describing it only tempts the producer to try.
    """

    lines = [
        "Callable predicate reference. These are the ONLY evidence functions in "
        "the assertion environment. Each returns a strict bool and raises when it "
        "cannot answer, so you never guard a call.",
        "",
        "Arguments that name a model element take that element's name: copied "
        "verbatim from `declared_model_vocabulary` when the model declares it, or "
        "the name the Requirement proposes when it does not -- the existence "
        "predicates answer which of the two it is, so both are ordinary values "
        "here. `[*]` is also accepted wherever a source is expected, for the "
        "initial configuration: use it when the claim is about power-on or first "
        "entry and has no named source state. `condition` and `release` are FCSTM "
        "expressions rather than names. Arguments shown with a value list take one "
        "of those values.",
        "",
        "The `expression` field holds a bare boolean EXPRESSION. Do not write "
        "`assert`, do not append a message, do not end with a semicolon: the "
        "controller wraps what you give it as `assert (<your expression>), "
        "<your failure_message>`, so an `assert` inside the field produces "
        "`assert (assert ...), \"...\"` and the whole script fails to parse. The "
        "`[REQ-xxx][AST-xxx]` label belongs in the separate `failure_message` "
        "field, never in the expression.",
        "",
        "    right:  state_declared(state=\"Sys.ModeA\", kind=\"leaf\") is True",
        "    wrong:  assert state_declared(state=\"Sys.ModeA\", kind=\"leaf\") is True, \"[REQ-001] ...\"",
        "",
        "Worked expressions -- several per family, covering every argument shape.",
        "",
        "Family S (declarations). Note that `kind`, `phase`, `sign` and `count` "
        "take a listed literal, not a path:",
        '    state_declared(state="Sys.ModeA", kind="leaf") is True',
        '    containment(parent="Sys.Outer", child="Sys.Outer.Inner") is True',
        '    cardinality(scope="Sys.Outer", count=3) is True',
        '    action_declared(state="Sys.ModeA", phase="entry") is True',
        '    effect_declared(source="Sys.ModeA", trigger="Sys.done", variable="units", sign="negative") is True',
        "",
        "Family B (runtime). `source` is the configuration the claim is about; "
        'use "[*]" when the claim is about power-on or first entry:',
        '    occupancy_after(source="Sys.ModeA", trigger="Sys.evt", target="Sys.ModeB") is True',
        '    occupancy_after(source="[*]", trigger="Sys.on", target="Sys.ModeA") is True',
        '    event_consumed(source="Sys.ModeA", trigger="Sys.evt") is True',
        '    terminates(scope="Sys.ModeB", trigger="Sys.off") is True',
        "",
        "Family P (bounded over all runs). `condition` and `release` are FCSTM "
        "expressions, not paths:",
        '    invariant(scope="Sys.ModeA", condition=\'!active("Sys.Fault")\', bound=4) is True',
        '    response_within(trigger="Sys.evt", response="Sys.ModeB", bound=3, source="Sys.ModeA") is True',
        '    persists_until(state="Sys.Hold", release=\'active("Sys.Done")\', bound=4) is True',
        "",
        "A claim over several named elements folds with all(). An existence check "
        "is the one thing that never folds into the claim resting on it: a single "
        "verdict cannot distinguish an element that is missing from one that is "
        "present and behaves wrongly, and those take different repairs. Keep those "
        "two as separate assertions linked by depends_on:",
        '    all([occupancy_after(source="Sys.ModeA", trigger="Sys.off", target="Sys.Final"),',
        '         occupancy_after(source="Sys.ModeB", trigger="Sys.off", target="Sys.Final")]) is True',
        '    variable_declared(variable="unit_count") is True    # precondition',
        '    variable_delta_after(source="Sys.ModeA", trigger="Sys.done", variable="unit_count", sign="negative") is True    # depends_on it',
        "",
        "Besides these you may use only plain builtins: len, all, any, bool, int, "
        "str, sorted, sum, min, max, set, list, tuple, abs, round, float, iter. "
        "Anything else is not in the namespace.",
    ]
    for family, title in (
        (FAMILY_STRUCTURE, "Family S -- decided from the declarations"),
        (FAMILY_BEHAVIOR, "Family B -- decided by running the model"),
        (FAMILY_PROPERTY, "Family P -- decided up to a bound over all runs"),
    ):
        lines.append(f"\n{title}")
        for item in PREDICATES:
            if item.family != family:
                continue
            lines.append(f"  `{signature_of(item.name)}`")
            lines.append(f"      decides: {item.meaning}")
            lines.append(f"      strength: {item.strength}")
            if item.caveat:
                lines.append(f"      boundary: {item.caveat}")
            for binding, spec in item.field_specs:
                lines.append(f"      arg {binding}: {spec}")
            for example in item.examples:
                lines.append(f"      e.g. {example}")
    return "\n".join(lines)


def procedure_mismatch(
    predicate: str, called_functions: frozenset[str] | set[str]
) -> tuple[str, str] | None:
    """Return ``(required, note)`` when a primary assertion dodges the procedure.

    The gate exists because a locator answers a neighbouring, *easier* question.
    ``transition_exists`` says an edge is declared; ``occupancy_after`` asks
    whether the system actually gets there.  Closing the second with the first
    reports "satisfied" for a model whose declared edge is unreachable or
    guard-blocked, and reports a violation for a model that reaches the target
    through declared follow-up transitions.  Pair 0006's false positive was
    exactly this substitution.

    Returns ``None`` when the predicate is unknown or absent -- an unnamed claim
    keeps the pre-predicate behaviour rather than being rejected, so v1/v2
    artifacts and producers that have not adopted the vocabulary still run.

    :param predicate: the Requirement's declared predicate name.
    :param called_functions: evidence functions parsed from the assertion.
    :return: ``None`` when acceptable, else the required function and a note.
    """

    entry = PREDICATE_BY_NAME.get(predicate)
    if entry is None:
        return None
    # The predicate is itself the callable now, so the check is exact: the
    # primary assertion must call *this* predicate.  Checking only the underlying
    # primitive was the weaker form -- it could not tell whether the call asked
    # the right question, which is how a tautological bounded query passed.
    if predicate in called_functions:
        return None
    used = sorted(called_functions & PREDICATE_NAMES)
    if used:
        note = (
            f"predicate {predicate!r} must be discharged by calling "
            f"{signature_of(predicate)}; the primary assertion called "
            f"{used} instead. Another predicate answers a different question, so "
            "it cannot close this claim."
        )
    else:
        # No evidence call at all.  Pair 0006's converter reached this after the
        # Reviewer had rejected every substitute release condition: it wrote
        # `expression: "False"` with a rationale explaining why the model cannot
        # satisfy the claim.  That is a conclusion, not a check -- it asserts a
        # defect on no evidence -- so rejecting it is right.  But the producer had
        # nowhere left to go, and repeated the shape until the run died.  Naming
        # the exit turns a dead end into one more round.
        note = (
            f"predicate {predicate!r} must be discharged by calling "
            f"{signature_of(predicate)}; the primary assertion called no "
            "predicate at all. A literal such as `False` asserts a defect on no "
            "evidence and can never be accepted. If the claim needs a model "
            "element this model does not declare, name that element: assert its "
            "existence as a `precondition` under the name it should have, and "
            "have this primary list that precondition in depends_on."
        )
    return (predicate, note)


def unmodelled_claim_paths(
    *,
    statement: str,
    bindings: dict[str, str],
    expressions: tuple[str, ...],
    known_paths: frozenset[str],
) -> tuple[str, ...]:
    """Return declared model paths the statement names but nothing tests.

    Pair 0029 carried a requirement asserting two things at once -- that a state
    is contained in a parent *and* that entering the parent starts there -- and
    only the second half was asserted.  The requirement was then reported
    satisfied, because nothing noticed the first half had no evidence.

    Detecting that in general needs to read the sentence, which is not something
    to do deterministically.  What *is* deterministic is weaker and still useful:
    the statement names declared model paths that appear in neither the
    predicate's bindings nor any primary expression.  Each one is a candidate
    untested claim.

    This is reported, never enforced.  A statement legitimately names context
    paths, so a hard gate here would reject valid work; the point is to make the
    residue visible and measurable before deciding whether it needs a gate.

    :param statement: the requirement statement text.
    :param bindings: the requirement's ``predicate_bindings``.
    :param expressions: primary assertion expressions for that requirement.
    :param known_paths: declared state/event paths from the frozen inspect.
    :return: sorted paths named by the statement but covered nowhere.
    """

    covered = " ".join([*bindings.values(), *expressions])
    return tuple(
        sorted(
            path
            for path in known_paths
            if path and path in statement and path not in covered
        )
    )


__all__ = [
    "EXISTENCE_PREDICATES",
    "accepted_bindings",
    "misspelled_binding_findings",
    "FAMILY_BEHAVIOR",
    "FAMILY_PROPERTY",
    "FAMILY_STRUCTURE",
    "FAMILY_TO_VERIFICATION_KIND",
    "PREDICATES",
    "PREDICATE_BY_NAME",
    "PREDICATE_NAMES",
    "PREDICATE_ORDER",
    "Predicate",
    "family_of",
    "verification_kind_of",
    "FREE_FORM_BINDINGS",
    "PREDICATE_OPTIONS",
    "callable_prompt",
    "procedure_mismatch",
    "signature_of",
    "vocabulary_prompt",
]
