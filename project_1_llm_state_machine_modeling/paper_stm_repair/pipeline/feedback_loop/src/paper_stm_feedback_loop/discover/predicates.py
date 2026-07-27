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
    #: The evidence call that decides it.  Checked against what the converter
    #: actually wrote, so an easier query cannot close a harder claim.
    procedure: str
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
        "states(path=..., exact=True)",
    ),
    Predicate(
        "containment",
        FAMILY_STRUCTURE,
        "this child is (or is not) a substate of this parent",
        "misplaced substate; a region attached to the wrong parent",
        ("parent", "child"),
        "states(parent=..., recursive=False)",
    ),
    Predicate(
        "initial_target",
        FAMILY_STRUCTURE,
        "entering this composite starts in this child",
        "wrong or missing initial child; entry lands in the wrong mode",
        ("composite", "child"),
        "initial_child(...)",
    ),
    Predicate(
        "edge_declared",
        FAMILY_STRUCTURE,
        "the model declares an edge with this source, trigger and target",
        "a missing or wrongly-targeted declared transition",
        ("source", "trigger", "target"),
        "transition_exists(source=..., event=..., target=...)",
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
        "effect_deltas(source=..., event=...)",
        locators=("effects(...)",),
    ),
    Predicate(
        "action_declared",
        FAMILY_STRUCTURE,
        "this state declares an entry, exit or during action",
        "a missing declared action; an action attached to the wrong phase",
        ("state", "phase"),
        "states(path=..., exact=True)",
        caveat=(
            "Requires the action fields to be exposed by the structure API; see "
            "issue #170 C0."
        ),
    ),
    Predicate(
        "guard_distinguishable",
        FAMILY_STRUCTURE,
        "a shared source and trigger cannot reach two targets indistinguishably",
        "non-determinism: overlapping or absent discriminating guards",
        ("source", "trigger"),
        "conflicting_targets(source=..., event=...)",
        locators=("guards_overlap(...)",),
    ),
    Predicate(
        "cardinality",
        FAMILY_STRUCTURE,
        "this scope declares exactly this many non-pseudo states",
        "a missing or duplicated mode in an enumerated set",
        ("scope", "count"),
        "states(...)",
    ),
    # ---- Family B: runtime behaviour ------------------------------------
    Predicate(
        "occupancy_after",
        FAMILY_BEHAVIOR,
        "after this trigger from this state, the system is in this target",
        "wrong target; a local exit written as global completion; a declared "
        "edge that is guard-blocked or unreachable at runtime",
        ("source", "trigger", "target"),
        "simulate(...).final.is_active(...)",
        locators=("transition_exists(...)", "path(...)"),
    ),
    Predicate(
        "event_consumed",
        FAMILY_BEHAVIOR,
        "in this configuration the event is actually consumed",
        "a dangling event no transition consumes; an event silently ignored in "
        "the state where the NL requires a response",
        ("source", "trigger"),
        "simulate(...).cycles[...].consumed_events",
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
        "simulate(...) consumed_events and final.is_active(source)",
    ),
    Predicate(
        "variable_delta_after",
        FAMILY_BEHAVIOR,
        "running this trigger changes this variable in this direction",
        "an effect is declared but the executed path never reaches it: "
        "declaration and runtime disagree",
        ("source", "trigger", "variable", "sign"),
        "simulate(...).cycles[...].variables",
        locators=("effect_deltas(...)",),
    ),
    Predicate(
        "reaches",
        FAMILY_BEHAVIOR,
        "within a bounded number of cycles this target is reachable from here",
        "an unreachable target: a broken chain or dead branch",
        ("source", "target", "within_cycles"),
        "simulate(...) multi-cycle",
        locators=("path(...)",),
        caveat=(
            "path() is guard-blind and only accepts leaf targets, so it may "
            "locate but never close this claim; see issue #170 C4."
        ),
    ),
    Predicate(
        "terminates",
        FAMILY_BEHAVIOR,
        "the model actually finishes",
        "premature or impossible completion: the final state is unreachable, "
        "or the path to it is guard-blocked",
        ("scope",),
        "simulate(...).final.is_ended",
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
        "fbmcq('check invariant <= k: ...')",
        caveat=(
            "Writing !(active(A) && active(B)) for siblings of one sequential "
            "region is a tautology and proves nothing.  Only holds is False is "
            "a violation; a non-terminal status is invalid, never False."
        ),
    ),
    Predicate(
        "response_within",
        FAMILY_PROPERTY,
        "every occurrence of this trigger is answered within the bound",
        "a missing or conditional response to a mandatory trigger",
        ("trigger", "response", "bound"),
        "fbmcq('check response <= k: ...')",
    ),
    Predicate(
        "persists_until",
        FAMILY_PROPERTY,
        "this state holds continuously until this release condition",
        "premature exit from a state that must persist",
        ("state", "release", "bound"),
        "fbmcq('check exists_always <= k: ...')",
        caveat=(
            "Infeasible on the pairs where formula construction exceeds budget; "
            "expand into B-family claims when the domain is enumerable."
        ),
    ),
)

PREDICATE_BY_NAME = {item.name: item for item in PREDICATES}
PREDICATE_NAMES = frozenset(PREDICATE_BY_NAME)


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


def vocabulary_prompt() -> str:
    """Render the vocabulary for prompts, so text and gate cannot drift.

    The gate reads :data:`PREDICATES`; so does this.  Hand-writing the table in
    a prompt string would let the two diverge, and a prompt that advertises a
    predicate the gate rejects wastes a whole repair round.
    """

    lines = [
        "Predicate vocabulary. Every claim must name exactly one predicate from "
        "this closed list. The family, and therefore the mandatory evidence, is "
        "derived from the predicate -- you do not choose it.",
    ]
    for family, title in (
        (FAMILY_STRUCTURE, "Family S -- what the artifact declares (structural/relational evidence is correct here, not a compromise)"),
        (FAMILY_BEHAVIOR, "Family B -- what the model does at runtime (simulate() is mandatory; static queries may only locate)"),
        (FAMILY_PROPERTY, "Family P -- quantified over states, valuations or paths (bounded fbmcq() is mandatory)"),
    ):
        lines.append(f"\n{title}")
        for item in PREDICATES:
            if item.family != family:
                continue
            lines.append(
                f"- `{item.name}`({', '.join(item.bindings)}): {item.meaning}. "
                f"Exposes: {item.proves}. Decided by `{item.procedure}`."
            )
            if item.locators:
                lines.append(
                    f"    supporting locators only: {', '.join(f'`{x}`' for x in item.locators)}"
                )
            if item.caveat:
                lines.append(f"    caveat: {item.caveat}")
    return "\n".join(lines)


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
    "Predicate",
    "family_of",
    "verification_kind_of",
    "procedure_prompt",
    "vocabulary_prompt",
]
