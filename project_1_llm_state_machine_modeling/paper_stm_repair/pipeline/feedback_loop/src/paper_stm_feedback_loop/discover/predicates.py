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
    "kind": 'kind: "leaf"|"composite"|"pseudo"',
    "sign": 'sign: "negative"|"positive"',
    "phase": 'phase: "entry"|"exit"|"during"',
    "condition": "condition: str",
    "release": "release: str",
    "bound": "bound: int",
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
        "Arguments that name a model element must be copied verbatim from "
        "`declared_model_vocabulary`. Three literals are also accepted wherever an "
        "element is expected: `[*]` for the initial configuration (use it when the "
        "claim is about power-on or first entry and has no named source state), and "
        "`<undeclared>` when the NL requires a term the model never declares -- that "
        "raises, and the controller records the absence, which is the honest "
        "outcome. Arguments shown with a value list take one of those values.",
        "",
        "Worked examples:",
        '    assert occupancy_after(source="Sys.ModeA", trigger="Sys.evt", target="Sys.ModeB") is True, "[REQ-001][AST-REQ-001-1] ..."',
        '    assert state_declared(state="Sys.ModeA", kind="leaf") is True, "[REQ-002][AST-REQ-002-1] ..."',
        '    assert all([',
        '        occupancy_after(source="Sys.ModeA", trigger="Sys.off", target="Sys.Final"),',
        '        occupancy_after(source="Sys.ModeB", trigger="Sys.off", target="Sys.Final"),',
        '    ]) is True, "[REQ-003][AST-REQ-003-1] ..."',
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
    return (
        predicate,
        (
            f"predicate {predicate!r} must be discharged by calling "
            f"{signature_of(predicate)}; the primary assertion called "
            f"{used or 'no predicate'} instead. Another predicate answers a "
            f"different question, so it cannot close this claim."
        ),
    )


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


def procedure_prompt() -> str:
    """Render only predicate -> procedure, for the assertion-writing stages.

    They do not need the full meaning text; they need to know which call is
    mandatory and which calls are merely locators.  Same source of truth.
    """

    lines = [
        "Predicate procedures. The `primary` assertion of a Requirement must "
        "call the procedure its predicate names. Locators may appear only as "
        "`supporting`.",
    ]
    for item in PREDICATES:
        row = f"- `{item.name}` -> primary MUST call `{item.procedure}`"
        if item.locators:
            row += f"; locators (supporting only): {', '.join(f'`{x}`' for x in item.locators)}"
        lines.append(row)
    return "\n".join(lines)


__all__ = [
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
    "procedure_prompt",
    "vocabulary_prompt",
]
