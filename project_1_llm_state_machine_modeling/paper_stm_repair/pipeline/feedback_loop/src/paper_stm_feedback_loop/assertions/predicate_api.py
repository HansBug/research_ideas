"""The 19 predicates of issue #170, as the only evidence calls an assertion may make.

Why this layer exists
---------------------
The evidence layer used to expose its raw building blocks -- ``states``,
``simulate``, ``fbmcq``, ``transition_exists`` and friends -- and every
assertion hand-assembled a check out of them.  Three problems followed.

First, the producer had to write bounded-model-checking query strings by hand.
On pair 0006 that produced ``init state("X"); check exists_always <= 1:
active("X")`` -- start in X, ask whether X holds for one step -- which is
near-tautological, passed, and reported a requirement as satisfied whose
obligation the model could not express at all.  A false negative wearing a pass.

Second, the requirement named a predicate but the assertion was free-form, so
the strongest available check was "did it call the right function".  That
cannot see whether the call *asks the right question*.

Third, every assertion re-derived the same shape.  ``occupancy_after`` appeared
511 times in one matrix, each time as a fresh lambda over ``simulate``.

Naming the predicate as a callable fixes all three: the query construction lives
here once and is reviewed once, the assertion becomes the claim itself rather
than an encoding of it, and an unsatisfiable obligation raises instead of
silently passing.

Contract
--------
Every predicate returns a strict ``bool``.  A predicate that cannot answer
raises :class:`UnsupportedEvidence`; the checker turns that into an unsupported
outcome rather than a truth value, which is what keeps an unanswerable claim out
of the satisfied set.

Bindings name model elements, and a name that is not shaped like one is refused
outright rather than answered.  A placeholder such as ``<undeclared>`` is not a
name, so no predicate can be handed one: the requirement it stands for needs a
proposed name and a `precondition`, which is a decision for the producer, not a
truth value this layer can invent.
"""

from __future__ import annotations

import re
from typing import Any

from .exceptions import UnsupportedEvidence

#: The pseudo-initial source, spelled exactly as FCSTM spells it.  A behaviour
#: claim about power-on or first entry has no named source state, and without a
#: sanctioned way to say so the producer invents one -- the smoke run produced
#: `source="<initial>"`, which the unresolved-reference gate correctly rejected
#: and then had to repair.  Accepting the real literal removes the guesswork.
PSEUDO_INITIAL = "[*]"

#: Cycle budget for the bounded simulations the B-family predicates run.  Kept
#: small on purpose: these are witnesses, not proofs, and a longer trace makes
#: the fired-transition derivation less likely to stay unambiguous.
DEFAULT_CYCLES = 1
DEFAULT_BOUND = 5
#: Cycles a termination probe drives before concluding the model cannot finish.
TERMINATION_CYCLES = 6

#: Hard ceiling on any caller-supplied cycle or step budget.  `reaches` builds
#: one plan entry per cycle, so `within_cycles=10**9` allocated a billion of them
#: and exhausted the machine's memory before any check ran.  A producer can write
#: that number by accident -- nothing in the prompt bounds it -- and an OOM kill
#: mid-run leaves a partial record indistinguishable from a model that produced
#: nothing.  Refuse instead: a budget this large is not a claim anyone can check.
MAX_BUDGET = 64


def _budget(value: Any, name: str, default: int) -> int:
    """Coerce a caller-supplied cycle or step budget, or refuse it.

    Refusing rather than clamping, because a clamped budget answers a *different*
    question than the one asked and returns a plain bool with no sign that it
    happened -- the failure mode this layer exists to avoid.
    """

    try:
        parsed = int(value)
    # `int(float("inf"))` raises OverflowError, which is neither of the other two:
    # it escaped as a bare exception, so the result was recorded as `exception`
    # rather than `unsupported` and the controller had no repair branch for it.
    except (TypeError, ValueError, OverflowError) as exc:
        raise UnsupportedEvidence(
            f"{name} must be an integer, got {value!r}"
        ) from exc
    if parsed < 1:
        raise UnsupportedEvidence(
            f"{name} must be at least 1, got {parsed}: a zero or negative budget "
            "checks nothing"
        )
    if parsed > MAX_BUDGET:
        raise UnsupportedEvidence(
            f"{name}={parsed} exceeds the {MAX_BUDGET}-step ceiling; a bounded "
            "check that large is not decidable here. State the obligation over a "
            "smaller horizon."
        )
    return parsed


#: The declaration table each binding's name must be shaped for.  A binding
#: absent from this map is not a name at all -- `condition` and `release` carry
#: FCSTM expressions -- so no identifier shape applies to it.
BINDING_DECLARATION_TABLE = {
    "variable": "variables",
    "trigger": "events",
    "event": "events",
    "state": "states",
    "source": "states",
    "target": "states",
    "parent": "states",
    "child": "states",
    "composite": "states",
    "scope": "states",
    "response": "states",
}



#: A single FCSTM identifier, and a dotted path of them.  Measured against the
#: whole corpus: 627 state paths, 387 event paths and 33 variable names, every one
#: matching, none deeper than six segments.  So a binding that does not match is
#: not an unusual model -- it is a malformed value, and answering `False` about it
#: would report "the model lacks this element" for a string that could never have
#: named one.
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_DOTTED_PATH = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*")

#: `<undeclared>` and anything else shaped like a placeholder.  It needs no
#: special case: `<` is not an identifier character, so the shape check already
#: refuses it.  What the shape gets it is a more specific diagnosis, because a
#: producer reaching for it is not making a typo -- it is expressing something real
#: and needs to be told where that belongs (issue #170 §11.2).
_PLACEHOLDER = re.compile(r"^<.*>$")


def is_placeholder_name(value: str) -> bool:
    """Whether a binding value is a placeholder rather than an element name.

    The static conversion gate needs the same test the runtime applies, so both
    live off this one predicate: two copies of the pattern would eventually
    disagree about what counts as a name, and the gate that was more permissive
    would pass work to the layer that refuses it.

    :param value: the raw bound value.
    :return: ``True`` when the value only stands in for a name.
    """

    return bool(_PLACEHOLDER.match(value.strip()))


def _require_identifier(
    value: Any, binding: str, *, dotted: bool, min_segments: int = 1
) -> str:
    """Return the value stripped, or refuse it rather than answering about it.

    ``dotted=False`` is for variable names: FCSTM declares variables outside the
    state tree, so they carry no path prefix.

    ``min_segments`` exists because the corpus is asymmetric.  All 387 declared
    events are addressed with exactly two segments, `<root>.<event>`, so a bare
    `go` cannot name one -- it would be looked up, not found, and reported as a
    missing event.  States are different: 60 of the 627 paths are single-segment,
    one per model, because each model's root is a state.  So the floor is a
    measured fact per binding kind, not a uniform rule.
    """

    text = _need(value, binding)
    stripped = text.strip()
    pattern = _DOTTED_PATH if dotted else _IDENTIFIER
    if pattern.fullmatch(stripped) and stripped.count(".") + 1 >= min_segments:
        return stripped
    if pattern.fullmatch(stripped):
        raise UnsupportedEvidence(
            f"predicate binding {binding!r} needs at least {min_segments} "
            f"path segments, got {text!r}. Events are addressed as "
            "`<root>.<event>`; copy the path as it appears under `events` in "
            "declared_model_vocabulary. A bare name matches nothing, and the "
            "`False` that would follow reads as a missing event."
        )
    if is_placeholder_name(stripped):
        raise UnsupportedEvidence(
            f"predicate binding {binding!r} is a placeholder, not a name: "
            f"{text!r}. An assertion cannot evaluate one. If the NL requires a "
            "term this model has no declaration for, give it a proposed name, "
            "assert that name's existence as a `precondition`, and make this "
            "assertion depend on it -- then the gap has something repair can add, "
            "and something a later run can verify."
        )
    shape = (
        "a dotted path of identifiers such as `Sys.Outer.Inner`"
        if dotted
        else "a bare identifier such as `units`"
    )
    raise UnsupportedEvidence(
        f"predicate binding {binding!r} is not a well-formed model name: "
        f"{text!r}. Expected {shape} -- letters, digits and underscores, not "
        "starting with a digit. A malformed name cannot denote a declared "
        "element, so this is refused rather than answered `False`."
    )


def _need(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise UnsupportedEvidence(f"predicate binding {name!r} must be a non-empty path")
    return value


class PredicateAPI:
    """Bind the predicate vocabulary to the frozen evidence facades.

    Parameters: the already-constructed structure / relation / effect /
    simulation / topology / formal facades, so predicates reuse exactly the
    evidence the controller froze and add no new capability of their own.
    """

    family = "predicate"

    def __init__(
        self,
        *,
        structure: Any,
        relations: Any,
        effects: Any,
        simulation: Any,
        topology: Any = None,
        formal: Any = None,
        source_exclusions: tuple[str, ...] = (),
    ) -> None:
        self.structure = structure
        self.relations = relations
        self.effects = effects
        self.simulation = simulation
        self.topology_api = topology
        self.formal = formal
        self.source_exclusions = tuple(source_exclusions)
        # Attribution needs to know which model elements a call rested on.  The
        # predicate is the only thing that knows: it chose the query.  Refs are
        # collected per call and consumed by the runtime's audit wrapper, so the
        # wrapper never has to re-derive them from a function name it no longer
        # recognises.
        self._refs: list[str] = []

    def begin_call(self) -> None:
        self._refs = []

    def consume_refs(self) -> tuple[str, ...]:
        refs, self._refs = self._refs, []
        return tuple(sorted(set(refs)))

    def _note(self, *refs: Any) -> None:
        for ref in refs:
            if isinstance(ref, str) and ref:
                self._refs.append(ref)

    #: The only bindings `[*]` can mean anything in: both name a configuration
    #: to start from, and "the initial one" is a configuration.  Everywhere else
    #: the literal names an element, and the entry marker is not one.
    #:
    #: Stated as one rule over bindings rather than a list per predicate, because
    #: the list was the bug: `edge_declared(trigger=...)`,
    #: `effect_declared(trigger=..., variable=...)`, `occupancy_after(target=...)`
    #: and `reaches(target=...)` were all absent from it, so each answered a
    #: silent False on every model -- a defect reported against all 60 pairs.
    _PSEUDO_INITIAL_BINDINGS = frozenset({"source", "scope"})

    #: Predicates that cannot take `[*]` even in those bindings.  `cardinality`
    #: would be counting the substates of an entry marker.
    #: `guard_distinguishable` reads the facade's `[*]` bucket, which holds the
    #: local entry edge of *every* composite: on pair 0002 that merged the
    #: entries of two concurrent regions and reported non-determinism between
    #: transitions in disjoint scopes.
    _NO_PSEUDO_INITIAL = {
        "cardinality": ("scope",),
        "guard_distinguishable": ("source",),
    }

    def _reject_pseudo_initial(self, predicate: str, **bindings: Any) -> None:
        """Refuse `[*]` where it cannot mean anything, instead of answering False.

        A producer learns from `occupancy_after(source="[*]")` that the literal is
        legal and carries it across.  Each of these then returned a silent False --
        "the model does not declare a state at [*]" -- which the pipeline reads as
        a defect the model does not have.  Answering a question nobody asked is
        worse than refusing to answer.
        """

        offenders = sorted(
            name
            for name in self._NO_PSEUDO_INITIAL.get(predicate, ())
            if bindings.get(name) == PSEUDO_INITIAL
        )
        if offenders:
            raise UnsupportedEvidence(
                f"{predicate} cannot take {PSEUDO_INITIAL} for {offenders} even "
                "though other predicates accept it there: this one reads the "
                "declaration under that name, and the pseudo-initial is an entry "
                "marker with no declaration of its own. Name the state or scope "
                "the claim is about."
            )

    def _require_well_formed_names(self, **bindings: Any) -> None:
        """Every model-name binding must be a name this model could have declared.

        One rule, replacing three.  Earlier designs judged `<undeclared>` per
        binding kind -- seal a false for `variable` and `trigger`, refuse for
        state-shaped ones, refuse for expressions -- which took three sets of
        judgement, three exemptions, a dedicated exception type and a dedicated
        seal path.  The third was measured to constrain nothing: 60 of 60 pairs
        have an empty author-owned variable table, so "the table is empty" carried
        no information and the seal fired for any pair at all.

        Shape subsumes it.  `<undeclared>` is refused because `<` is not an
        identifier character, not because it appears on a list -- and the same
        check catches embedded newlines, quotes, semicolons and injection
        attempts, each of which would otherwise be looked up, not found, and
        reported as a missing model element.

        Checking here rather than inside each predicate is what makes it uniform:
        `effect_declared` once passed an int straight to the effect facade, which
        concatenated it and raised `TypeError` -- an error class the controller has
        no repair branch for, so the producer got generic advice and spent its
        budget repeating the mistake.

        Variable names are checked without a dot, everything else with: FCSTM
        declares variables outside the state tree, and a producer generalising
        from state paths writes `Sys.units`, which names nothing.
        """

        for binding, value in bindings.items():
            table = BINDING_DECLARATION_TABLE.get(binding)
            if table is None:
                # `condition` / `release` are FCSTM expressions, so no identifier
                # shape applies -- but a placeholder is still a placeholder.  Left
                # to itself it reaches the solver and comes back "fbmcq query parse
                # failed", which is true and useless: the producer cannot tell from
                # it that the problem is the binding rather than the query builder.
                if isinstance(value, str) and is_placeholder_name(value):
                    _require_identifier(value, binding, dotted=True)
                continue
            # `None` is not skipped.  An optional binding that is absent is simply
            # not passed in (`terminates` and `response_within` do that), so a
            # `None` arriving here is a required binding left unset -- and letting
            # it through reached the effect facade as `unregistered item access:
            # None`, an exception class the controller cannot dispatch on.
            if value == PSEUDO_INITIAL:
                if binding in self._PSEUDO_INITIAL_BINDINGS:
                    continue  # the sanctioned literal for the initial configuration
                raise UnsupportedEvidence(
                    f"binding {binding!r} cannot be {PSEUDO_INITIAL}: the "
                    "pseudo-initial marks where a run begins, so it only means "
                    f"something for {sorted(self._PSEUDO_INITIAL_BINDINGS)}. "
                    f"A {table[:-1] if table.endswith('s') else table} is named, "
                    f"and this one is not; name the {binding} the claim is about."
                )
            _require_identifier(
                value,
                binding,
                dotted=table != "variables",
                # An event needs its root prefix; a state may be the root itself.
                min_segments=2 if table == "events" else 1,
            )

    # ---- helpers -----------------------------------------------------
    @staticmethod
    def _hot_startable(source: str | None) -> str | None:
        """Return the state to hot-start from, or None for the initial config."""

        if not source or source == PSEUDO_INITIAL:
            return None
        return source

    def _model_root(self) -> str | None:
        """The path every configuration is inside, or None if unreadable."""

        try:
            rows = self.structure.states()
        except Exception:
            return None
        for row in rows:
            if not getattr(row, "parent_path", None):
                path = getattr(row, "path", None)
                if isinstance(path, str) and path:
                    return path
        return None

    def _reject_undiscriminating_root(self, predicate: str, **bindings: Any) -> None:
        """Refuse a claim whose subject is active in every configuration.

        The root is entered before anything else and left only at termination, so
        `response_within(response=<root>)` holds however the model behaves, and
        `occupancy_after(target=<root>)` holds whenever the trigger is consumed at
        all.  A producer that binds the enclosing mode instead of the leaf gets a
        pass on a model whose transition goes to the wrong state -- which is the
        opposite of what these predicates are for.

        No static gate covers this one.  `condition_non_vacuity_findings` reads
        `invariant`/`persists_until` conditions, and a root binding is not a
        condition -- it is a path in `target`/`response`, valid on its face and
        vacuous only because of what the model's root happens to contain.  So the
        refusal has to happen here, at the call.
        """

        root = self._model_root()
        if not root:
            return
        offenders = sorted(name for name, value in bindings.items() if value == root)
        if offenders:
            raise UnsupportedEvidence(
                f"{predicate} cannot take the model root {root!r} for {offenders}: "
                "the root is active in every configuration, so the claim holds no "
                "matter what the model does. Name the state the requirement is "
                "actually about."
            )

    def _pins_a_composite(self, path: str) -> bool:
        """Whether pinning here starts the machine above a leaf configuration."""

        try:
            rows = self.structure.states(path=path, exact=True)
        except Exception:  # the pin itself is refused below, with a better message
            return False
        return len(rows) == 1 and bool(getattr(rows[0], "is_composite", False))

    def _simulate(self, *, source: str | None, trigger: str | None, cycles: int):
        """Run the smallest trace that can witness ``trigger`` fired from ``source``.

        A cold start plus the event is used when no source is given; otherwise a
        hot start pins the configuration so the observation is about that state
        and not about whatever the machine drifted into.

        A composite pin gets one empty settle cycle first, because committing the
        entry into its initial child *is* a cycle: offered in that same cycle the
        trigger is never consumed, so every B-family question about a mode rather
        than a leaf came back False.  Measured on pair 0000 -- pinned at
        `AutonomousMode`, plan `[[Condition_Met]]` consumes nothing while
        `[[], [Condition_Met]]` consumes it and reaches `AutoFinal`; the leaf pin
        answers the same either way, which is why only the composite case settles.
        704 bindings across 58 of the 60 pairs name a composite source, so this
        was a defect reported against models that handle the event correctly.

        The settle cycle does not have to commit an entry for the trigger to be
        consumed: pinned at pair 0000's root, that cycle reports "no stoppable
        successor was committed" and the next cycle still consumes `Power_Off`
        and fires the declared transition.  So an empty settle is not evidence
        that the configuration cannot receive events, and refusing on it would
        turn working root-pinned assertions into unsupported ones.
        """

        events = [[trigger]] if trigger else [[]]
        events += [[] for _ in range(max(0, cycles - 1))]
        pinned = self._hot_startable(source)
        if pinned:
            settle = 1 if self._pins_a_composite(pinned) else 0
            try:
                view = self.simulation.simulate(
                    initial_state=pinned,
                    initial_vars=self._all_vars(),
                    cycles=[[] for _ in range(settle)] + events,
                )
            except Exception as exc:
                # Falling back to a cold start here would answer about the
                # initial configuration while the caller asked about `pinned`,
                # and return a plain bool with no sign that it happened.  A
                # silently-different question is the worst failure this layer
                # can produce, so refuse instead.
                raise UnsupportedEvidence(
                    f"cannot start the model in {pinned!r} ({exc}); the claim is "
                    "about that configuration and cannot be answered from another"
                ) from exc
        else:
            view = self.simulation.simulate(cycles=[[]] + events)
        self._note_simulation(view)
        return view

    def _note_simulation(self, view: Any) -> None:
        """Record the path the trace actually took, not the states it observed.

        A state observation carries no path identity; the derived fired
        transitions do, which is what lets the exclusion table taint a simulated
        path exactly as it taints a static query.
        """

        ambiguous = False
        for cycle in getattr(view, "cycles", ()) or ():
            for ref in getattr(cycle, "path_refs", ()) or ():
                self._note(ref)
            if getattr(cycle, "path_taint", None) == "ambiguous":
                ambiguous = True
            # "Nothing happened" is often the defect itself, and it leaves no
            # path to attribute.  Anchor it to the transitions that declare the
            # ignored event, exactly as a failed structural query anchors to its
            # near miss -- otherwise a real finding lands as `unattributed`.
            fired = getattr(cycle, "fired_transitions", ()) or ()
            unconsumed = getattr(cycle, "unconsumed_events", ()) or ()
            if not fired and unconsumed:
                for event in unconsumed:
                    if isinstance(event, str) and event:
                        self._note(event)
                        self._note_transitions(event=event)
        if ambiguous:
            self._note("simulation:path_taint:ambiguous")

    def _all_vars(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for row in self.structure.variables():
            name = getattr(row, "name", None)
            init = getattr(row, "init_value", None)
            if isinstance(name, str):
                try:
                    out[name] = int(str(init))
                except Exception:
                    try:
                        out[name] = float(str(init))
                    except Exception:
                        out[name] = 0
        return out

    def _note_transitions(self, *, filtered_route_control: bool = False, **filters: Any) -> None:
        """Record the declared transitions a relational query matched.

        Three details carry over from the pre-predicate attribution path and must
        not be lost.  A route-control variable in a matched guard or effect is
        genuine evidence of converter lowering, so it keeps signalling debt.  A
        query that matches nothing still needs an anchor: without a near miss a
        negative structural answer has no model identity to attribute, which is
        how a real defect ends up merely `unattributed`.  And a near miss that
        differs only in the converter's event projection is itself the finding's
        cause, so the projection is reported under its qualified name.
        """

        clean = {k: v for k, v in filters.items() if isinstance(v, str) and v}
        try:
            rows = self.structure.transitions(**clean)
        except Exception:
            return
        used_near_miss = False
        if not rows:
            rows = self._near_miss(clean)
            used_near_miss = bool(rows)
        for row in rows:
            if used_near_miss:
                self._note_event_projection(row, requested=clean.get("event"))
            for key in ("from_path", "to_path", "event"):
                value = getattr(row, key, None)
                if isinstance(value, str) and value and value != "[*]":
                    self._note(value)
            index = getattr(row, "transition_index", None)
            if isinstance(index, int):
                self._note(f"transition:{index}")
            text = " ".join(
                str(getattr(row, k, "") or "") for k in ("guard", "effect")
            )
            for item in self.source_exclusions:
                prefix = "compiler:route_control:"
                if item.startswith(prefix):
                    variable = item.removeprefix(prefix)
                    if not variable or variable not in text:
                        continue
                    # EffectAPI already dropped this variable from the answer, so
                    # the result does not rest on it.  Reporting it as touched
                    # made attribution mark the finding `representation_debt`:
                    # on pair 0006 the only effect on the Attack_Complete
                    # transition is the compiler's own route token, so the query
                    # proving "no semantic decrement exists" was disqualified for
                    # having looked at the thing it filtered out.
                    self._note(
                        f"filtered_route_control:{variable}"
                        if filtered_route_control
                        else f"route_control:{variable}"
                    )

    def _note_event_projection(self, row: Any, *, requested: str | None) -> None:
        """Report a near miss that differs only by the converter's projection.

        When the converter folds a combined condition into a single event, an
        assertion that names the atomic event the NL used fails for a
        representation reason, not an authoring one.  The exclusion table names
        that event with its full ``compiler:event_projection:`` qualifier and the
        shared matcher in ``common.refs`` compares complete references, so the
        bare event path this method's caller already recorded does not intersect
        it.  Without the qualified form the finding is booked against the source
        author.
        """

        actual = getattr(row, "event", None)
        if not requested or not isinstance(actual, str) or not actual:
            return
        if actual == requested:
            return
        reference = f"compiler:event_projection:{actual}"
        if reference in self.source_exclusions:
            self._note(reference)

    def _near_miss(self, filters: dict[str, str]) -> tuple[Any, ...]:
        """Return the closest actual relation for a query that matched nothing."""

        for keys in (("source", "event"), ("source", "target"), ("event", "target")):
            if not all(k in filters for k in keys) or len(keys) >= len(filters):
                continue
            try:
                rows = self.structure.transitions(**{k: filters[k] for k in keys})
            except Exception:
                continue
            if rows:
                return rows
        if len(filters) <= 2:
            for key in ("source", "event", "target"):
                if key not in filters:
                    continue
                try:
                    rows = self.structure.transitions(**{key: filters[key]})
                except Exception:
                    continue
                if rows:
                    return rows
        return ()

    @staticmethod
    def _consumed(view: Any) -> set[str]:
        out: set[str] = set()
        for cycle in getattr(view, "cycles", ()) or ():
            for ev in getattr(cycle, "consumed_events", ()) or ():
                if isinstance(ev, str):
                    out.add(ev)
        return out

    @staticmethod
    def _initial_configuration(view: Any) -> set[str]:
        """The configuration the run held before any event was offered.

        A cold-start plan leads with an empty cycle for exactly this reason, so
        the first cycle's active ancestry is what `source="[*]"` names.
        """

        for cycle in getattr(view, "cycles", ()) or ():
            states = {
                str(state)
                for state in (getattr(cycle, "active_states", ()) or ())
                if str(state)
            }
            if states:
                return states
        return set()

    @staticmethod
    def _active(view: Any) -> tuple[str, ...]:
        final = getattr(view, "final", None)
        states = getattr(final, "active_states", ()) if final is not None else ()
        return tuple(str(s) for s in states or ())

    # ---- Family S: what the artifact declares ------------------------
    def state_declared(self, *, state: str, kind: str) -> bool:
        """The model declares a state at this path, of this kind."""

        self._reject_pseudo_initial("state_declared", state=state)
        self._require_well_formed_names(state=state)
        self._note(state)
        rows = self.structure.states(path=_need(state, "state"), exact=True)
        if len(rows) != 1:
            return False
        row = rows[0]
        want = str(kind).strip().lower()
        if want in {"leaf", "simple"}:
            return bool(row.is_leaf) and not bool(row.is_pseudo)
        if want in {"composite", "submachine", "compound"}:
            return bool(row.is_composite)
        if want in {"pseudo", "pseudostate"}:
            return bool(row.is_pseudo)
        if want in {"any", "declared", ""}:
            return True
        raise UnsupportedEvidence(
            f"unknown state kind {kind!r}; use leaf / composite / pseudo / any"
        )

    def variable_declared(self, *, variable: str) -> bool:
        """The model declares a variable of its own under this name.

        Existence in its own right, which the vocabulary previously had only for
        states: `variable` appeared solely inside `effect_declared` and
        `variable_delta_after`, always in a relational context.  That asymmetry is
        why "the NL requires a quantity this model has no variable for" had no
        checkable form and had to be smuggled through as `<undeclared>` -- see
        issue #170 §11.

        Route-control variables are not the author's.  The effect facade already
        drops them from every answer, so reporting one as declared here would
        promise evidence no other call can deliver.
        """

        self._reject_pseudo_initial("variable_declared", variable=variable)
        self._require_well_formed_names(variable=variable)
        wanted = _need(variable, "variable").strip()
        self._note(wanted)
        owned = {
            item.removeprefix("compiler:route_control:")
            for item in self.source_exclusions
            if item.startswith("compiler:route_control:")
        }
        for row in self.structure.variables():
            if str(getattr(row, "name", "") or "") != wanted:
                continue
            return wanted not in owned
        return False

    def event_declared(self, *, event: str) -> bool:
        """The model declares an event at this qualified path."""

        self._reject_pseudo_initial("event_declared", event=event)
        self._require_well_formed_names(event=event)
        wanted = _need(event, "event").strip()
        self._note(wanted)
        for row in self.structure.events():
            if str(getattr(row, "qualified_name", "") or "") == wanted:
                return bool(getattr(row, "is_declared", True))
        return False

    def containment(self, *, parent: str, child: str) -> bool:
        """This child is a direct substate of this parent."""

        self._reject_pseudo_initial("containment", parent=parent, child=child)
        self._require_well_formed_names(parent=parent, child=child)
        self._note(parent, child)
        rows = self.structure.states(
            parent=_need(parent, "parent"), recursive=False, exact=True
        )
        return _need(child, "child") in {str(r.path) for r in rows}

    def initial_target(self, *, composite: str, child: str) -> bool:
        """Entering this composite starts in this child."""

        self._reject_pseudo_initial("initial_target", composite=composite, child=child)
        self._require_well_formed_names(composite=composite, child=child)
        self._note(composite, child)
        return self._initial_child_of(_need(composite, "composite")) == _need(
            child, "child"
        )

    def _initial_child_of(self, composite: str) -> str | None:
        """The state entering ``composite`` lands in, by UML entry semantics.

        `structure.initial_child` demands exactly one declared initial edge and
        refuses otherwise.  That is right for a hand-written machine and wrong for
        a converted one: pair 0029's `HighwayMode` carries five, four of them
        guarded on the converter's own route token --

            [*] -> enter_hwy         if [R45RouteToken == 5]
            [*] -> FinishState       if [R45RouteToken == 25]
            [*] -> FinishState       if [R45RouteToken == 26]
            [*] -> FinishState       if [R45RouteToken == 27]
            [*] -> UnspecifiedInitial                            (unconditional)

        -- so the predicate refused, the producer was charged three repair rounds
        for an expression that could never execute, and a requirement the NL
        plainly states ("entering HighwayMode starts in enter_hwy") was filed as
        `no_progress`.  Two of pair 0029's requirements were lost that way in one
        cell, and the reason recorded made it look like the producer's fault.

        The guarded edges are re-entry points the converter generates for
        cross-hierarchy transitions, not entry declarations.  Entry with no
        history and no token set takes the unconditional edge, so that is the
        initial child, and answering from it turns an unanswerable claim into a
        decidable one.  The route-token names stay in the reference set, which is
        what lets attribution mark the resulting finding as representation debt
        rather than an authoring defect.
        """

        rows = self.structure.states(path=composite, exact=True)
        if len(rows) != 1:
            return None
        targets = getattr(rows[0], "initial_targets", None) or []
        # The rows come back as `FrozenView`, not dict -- the facade wraps nested
        # structures too.  An `isinstance(t, dict)` filter here silently matched
        # nothing and every call returned None, which reads as "the initial child
        # is not the one claimed" rather than "this code could not look".
        def field(item, name):
            if isinstance(item, dict):
                return item.get(name)
            return getattr(item, name, None)

        entries = [t for t in targets if field(t, "target")]
        if not entries:
            return None
        # A single declared entry *is* the entry, whatever labels it.  pyfcstm
        # counts an edge as unconditional only when it carries neither guard nor
        # event, so `[*] -> RunningState : /Activate_Pump` was "conditional" and
        # the predicate refused -- on 22 of the corpus's 169 composites -- with a
        # message about a guard the edge does not have.  Nothing is ambiguous
        # about one entry, so answer from it.
        if len(entries) == 1:
            return str(field(entries[0], "target"))
        unconditional = [t for t in entries if field(t, "is_unconditional")]
        if len(unconditional) == 1:
            for t in entries:
                if not field(t, "is_unconditional"):
                    # The guard names the converter's token; recording it is what
                    # lets attribution see the lowering behind this answer.
                    self._note(str(field(t, "guard") or ""))
            return str(field(unconditional[0], "target"))
        if len(unconditional) > 1:
            raise UnsupportedEvidence(
                f"{composite!r} declares {len(unconditional)} unconditional initial "
                "edges, so entry is genuinely ambiguous and no single initial child "
                "can be named"
            )
        raise UnsupportedEvidence(
            f"{composite!r} declares {len(entries)} initial edges and none of them "
            "is taken unconditionally -- each carries a guard or a trigger -- so "
            "which one entry takes depends on state this query cannot see. Ask "
            "about the edge you mean with edge_declared instead."
        )

    def edge_declared(self, *, source: str, trigger: str, target: str) -> bool:
        """The model declares an edge with this source, trigger and target."""

        self._require_well_formed_names(source=source, trigger=trigger, target=target)
        self._note(source, trigger, target)
        self._note_transitions(source=source, event=trigger, target=target)
        return bool(
            self.relations.transition_exists(
                source=source, event=trigger, target=target, exact=True
            )
        )

    def effect_declared(
        self, *, source: str, trigger: str, variable: str, sign: str
    ) -> bool:
        """This transition declares an effect on this variable, in this direction."""

        self._require_well_formed_names(source=source, trigger=trigger, variable=variable)
        # Deliberately not noting `variable`: a bare name matches the
        # `compiler:route_control:<name>` exclusion kind-agnostically, so noting
        # it booked every variable finding as compiler-owned debt -- the exact
        # pair-0006 regression `filtered_route_control:` was introduced to stop.
        self._note(source, trigger)
        self._note_transitions(
            source=source, event=trigger, filtered_route_control=True
        )
        want = str(sign).strip().lower()
        if want not in {"negative", "positive"}:
            raise UnsupportedEvidence(f"sign must be negative or positive, got {sign!r}")
        deltas = self.effects.effect_deltas(
            source=source, event=trigger, variable=variable
        )
        if not deltas:
            return False
        return any(d < 0 for _, d in deltas) if want == "negative" else any(
            d > 0 for _, d in deltas
        )

    def action_declared(self, *, state: str, phase: str) -> bool:
        """This state declares an entry, exit or during action."""

        self._reject_pseudo_initial("action_declared", state=state)
        self._require_well_formed_names(state=state)
        self._note(state)
        rows = self.structure.states(path=_need(state, "state"), exact=True)
        if len(rows) != 1:
            return False
        field = {
            "entry": "entry_actions",
            "enter": "entry_actions",
            "exit": "exit_actions",
            "during": "during_actions",
        }.get(str(phase).strip().lower())
        if field is None:
            raise UnsupportedEvidence(f"phase must be entry / exit / during, got {phase!r}")
        return bool(getattr(rows[0], field, ()) or ())

    def guard_distinguishable(self, *, source: str, trigger: str) -> bool:
        """A shared source and trigger cannot reach two targets indistinguishably."""

        self._reject_pseudo_initial("guard_distinguishable", source=source)
        self._require_well_formed_names(source=source, trigger=trigger)
        self._note(source, trigger)
        self._note_transitions(source=source, event=trigger)
        # No matching transition means the question is unanswerable, not
        # answered "distinguishable".  Returning True there reported a
        # mistyped or converter-projected trigger as satisfying the claim --
        # verbatim the pair-0029 defect.
        rows = self.structure.transitions(source=source, event=trigger, exact=True)
        if not rows:
            raise UnsupportedEvidence(
                f"no declared transition leaves {source!r} on {trigger!r}, so "
                "distinguishability cannot be decided; check the trigger spelling "
                "against declared_model_vocabulary"
            )
        branches = self._resolve_combo_branches(rows)
        if branches is not None:
            return not self._indistinguishable(branches)
        return not bool(self.relations.conflicting_targets(source=source, event=trigger))

    #: Marker the FCSTM lowering puts in the name of an intermediate state it
    #: creates for a `: /event + [guard]` combo transition.
    _COMBO_MARKER = "__combo"

    def _resolve_combo_branches(self, rows: Any) -> list[Any] | None:
        """Follow a combo intermediate state to the branches it really fans out to.

        `S -> A : /e + [g1];` and `S -> B : /e + [g2];` do not lower to two
        transitions out of `S`.  They lower to *one* transition into a generated
        intermediate state, whose unlabelled successors carry `g1` and `g2`.  So
        the direct query sees a single target, concludes there is nothing to
        distinguish, and answers True -- for any pair of guards, including two
        identical ones.  Since a guard attached to an event can only be written
        with the combo form, that made the True branch of this predicate
        unreachable for the case it exists to judge.

        Returns ``None`` when no combo is involved, so the ordinary facade path
        keeps handling the shape the corpus actually uses.
        """

        expanded: list[Any] = []
        saw_combo = False
        for row in rows:
            target = str(getattr(row, "to_path", "") or "")
            if self._COMBO_MARKER not in target:
                expanded.append(row)
                continue
            saw_combo = True
            expanded.extend(self.structure.transitions(source=target, exact=True))
        return expanded if saw_combo else None

    def _indistinguishable(self, rows: list[Any]) -> bool:
        """Do two of these branches reach different targets on overlapping guards?

        Mirrors `relations.conflicting_targets`, which cannot be reused directly
        because it re-queries by (source, event) and the combo branches share
        neither.
        """

        if len({str(getattr(r, "to_path", "")) for r in rows}) <= 1:
            return False
        undecidable = False
        for index, left in enumerate(rows):
            for right in rows[index + 1 :]:
                if str(left.to_path) == str(right.to_path):
                    continue
                try:
                    if self.relations.guards_overlap(
                        f"transition:{left.transition_index}",
                        f"transition:{right.transition_index}",
                    ):
                        return True
                except UnsupportedEvidence:
                    undecidable = True
        if undecidable:
            raise UnsupportedEvidence(
                "cannot decide whether the guarded alternatives overlap with the "
                "current structured public API"
            )
        return False

    def cardinality(self, *, scope: str, count: int) -> bool:
        """This scope declares exactly this many non-pseudo direct substates."""

        self._reject_pseudo_initial("cardinality", scope=scope)
        self._require_well_formed_names(scope=scope)
        self._note(scope)
        try:
            want = int(count)
        except Exception as exc:
            raise UnsupportedEvidence(f"count must be an integer, got {count!r}") from exc
        # An undeclared scope has no substates, so `count=0` used to come back
        # True -- "exactly zero, as claimed" -- passing a model that is missing the
        # whole enumerated set.  Nothing was counted, so nothing is decided.
        if not self.structure.states(path=_need(scope, "scope"), exact=True):
            raise UnsupportedEvidence(
                f"the model declares no state at {scope!r}, so it has no substates "
                "to count. A count over a scope that does not exist decides "
                "nothing; assert the scope's existence first"
            )
        rows = self.structure.states(parent=_need(scope, "scope"), recursive=False, exact=True)
        return len([r for r in rows if not bool(r.is_pseudo)]) == want

    # ---- Family B: what the model does at runtime --------------------
    def occupancy_after(
        self, *, source: str, trigger: str, target: str, within_cycles: int = DEFAULT_CYCLES
    ) -> bool:
        """After this trigger from this state, the system occupies this target.

        A declared edge is not enough: it may be unreachable, guard-blocked, or
        beaten by a competing transition.  This runs the trace and looks at where
        the machine actually ended up, accepting any leaf inside ``target`` since
        occupying a composite means occupying one of its leaves.
        """

        self._require_well_formed_names(source=source, trigger=trigger, target=target)
        self._reject_undiscriminating_root("occupancy_after", target=target)
        view = self._simulate(
            source=source,
            trigger=trigger,
            cycles=_budget(within_cycles, "within_cycles", DEFAULT_CYCLES),
        )
        # The claim is "this trigger takes the system there".  A completion
        # transition can reach the target on its own while the trigger is never
        # consumed; crediting the trigger for that is the false-positive shape
        # this predicate exists to prevent.
        if trigger not in self._consumed(view):
            return False
        active = self._active(view)
        return any(s == target or s.startswith(f"{target}.") for s in active)

    def event_consumed(self, *, source: str, trigger: str) -> bool:
        """In this configuration the event is actually consumed.

        There is no static substitute: an event being declared does not mean any
        configuration accepts it.
        """

        self._require_well_formed_names(source=source, trigger=trigger)
        view = self._simulate(source=source, trigger=trigger, cycles=1)
        for cycle in getattr(view, "cycles", ()) or ():
            if trigger in (getattr(cycle, "consumed_events", ()) or ()):
                return True
        return False

    def stays_in(self, *, source: str, trigger: str) -> bool:
        """After this trigger the system remains in the same state.

        `source="[*]"` asks it of the initial configuration.  That used to be a
        constant False: the literal was compared against real state paths, which
        it can never equal, so a power-on self-loop claim reported a missing
        self-loop on every model.  The configuration the cold start settles into
        is what the claim is about, so that is what gets compared.
        """

        self._require_well_formed_names(source=source, trigger=trigger)
        view = self._simulate(source=source, trigger=trigger, cycles=1)
        # Both halves matter.  Without the consumption check an ignored event
        # looks identical to a declared self-loop, so the missing-self-loop
        # defect this predicate advertises could never be observed.
        if trigger not in self._consumed(view):
            return False
        if source == PSEUDO_INITIAL:
            # The *deepest* state of the initial configuration, not its ancestry.
            # An observation reports the whole chain root..leaf, and the root is
            # active in every run, so comparing against the chain answers True
            # whatever the trigger does -- on the fixture model `Root.go` moves
            # `Inner` to `Done` and the chain still matched on `Root`.  Replacing
            # the old constant False with a near-constant True is no better.
            ancestry = self._initial_configuration(view)
            leaf = max(ancestry, key=lambda path: path.count("."), default="")
            # Only the root means nothing was committed: on pair 0000 no state is
            # entered until `Power_On` itself fires, so there is nothing to stay in.
            if len(ancestry) < 2 or not leaf:
                raise UnsupportedEvidence(
                    "the run enters no state before this trigger, so there is "
                    f"nothing for it to stay in. Name the state the claim is "
                    f"about instead of {PSEUDO_INITIAL}, or ask whether the "
                    "trigger is consumed there"
                )
            held = {leaf}
        else:
            # A composite subject cannot discriminate.  Every observation reports
            # the whole chain root..leaf, so a prefix match against an ancestor is
            # satisfied by its entire subtree: on the fixture pair where `go` moves
            # `Inner` to `Done`, binding `Root.Mode` -- or the root -- answered True
            # for the model that violates the obligation just as for the one that
            # satisfies it.  That is the same near-tautology the `[*]` branch above
            # was fixed for, reached instead by naming an ancestor, and it is why
            # the four sibling predicates refuse the root outright.
            #
            # Refused rather than reinterpreted: "stays inside this composite" and
            # "stays in this exact state" are different claims, and a composite
            # binding does not say which one the sentence meant.  Answering the
            # first would pass a model that moves between the composite's children,
            # answering the second would fail every model, since a composite is
            # never the deepest active state.
            if self._pins_a_composite(source):
                raise UnsupportedEvidence(
                    f"stays_in cannot take the composite {source!r}: every "
                    "observation reports the whole chain root..leaf, so a composite "
                    "subject is satisfied by any of its substates and the claim "
                    "holds however the model behaves. Name the leaf state the "
                    "requirement is about -- one requirement per state when the "
                    "sentence names none."
                )
            held = {source}
        active = self._active(view)
        # `held` holds one leaf, so equality is the whole comparison; a prefix test
        # here is what let an ancestor match its subtree.
        return any(state == name for name in held for state in active)

    def variable_delta_after(
        self, *, source: str, trigger: str, variable: str, sign: str
    ) -> bool:
        """Running this trigger changes this variable in this direction.

        Distinct from ``effect_declared``: an effect can be declared on an edge
        the executed path never reaches.
        """

        self._require_well_formed_names(source=source, trigger=trigger, variable=variable)
        self._note(source, trigger)
        want = str(sign).strip().lower()
        if want not in {"negative", "positive"}:
            raise UnsupportedEvidence(f"sign must be negative or positive, got {sign!r}")
        view = self._simulate(source=source, trigger=trigger, cycles=1)
        cycles = view.cycles
        before = getattr(getattr(view, "effective_initialization", None), "variables", None)
        start = _read_var(before, variable)
        end = _read_var(
            getattr(cycles[-1], "variables", None) if cycles else None, variable
        )
        if start is None or end is None:
            # Checked before consumption, deliberately.  A variable the model does
            # not declare makes this claim undecidable, and the earlier order
            # returned `False` for it whenever the trigger also happened not to
            # fire -- so a producer that named a variable the model lacks, or
            # forgot to depend on its existence precondition, got a verdict reading
            # "the quantity did not decrease" for a quantity that does not exist.
            raise UnsupportedEvidence(
                f"variable {variable!r} is not observable in the simulation state. "
                "If the NL requires a quantity this model has no variable for, "
                "assert that variable's existence as a `precondition` and make this "
                "assertion depend on it."
            )
        if trigger not in self._consumed(view):
            # A completion transition may have moved the variable; that is not
            # evidence that *this* trigger does.
            return False
        return (end - start) < 0 if want == "negative" else (end - start) > 0

    def reaches(self, *, source: str, target: str, within_cycles: int = 3) -> bool:
        """Within a bounded number of cycles this target is reachable from here."""

        self._require_well_formed_names(source=source, target=target)
        self._reject_undiscriminating_root("reaches", target=target)
        # Reachability without events only ever exercises completion
        # transitions, so every target one event away was reported unreachable
        # -- a fabricated defect on the most common shape in this corpus.  Offer
        # the whole declared alphabet each cycle and let the model take what it
        # can; that is the bounded over-approximation this predicate is for.
        return self._reaches_within(
            source=source,
            target=target,
            cycles=_budget(within_cycles, "within_cycles", 3),
        )

    def _reaches_within(self, *, source: str, target: str, cycles: int) -> bool:
        alphabet = [
            str(row.qualified_name)
            for row in self.structure.events()
            if getattr(row, "qualified_name", None)
        ]
        pinned = self._hot_startable(source)
        plan = [list(alphabet) for _ in range(max(1, cycles))]
        try:
            view = (
                self.simulation.simulate(
                    initial_state=pinned, initial_vars=self._all_vars(), cycles=plan
                )
                if pinned
                else self.simulation.simulate(cycles=[[]] + plan)
            )
        except Exception as exc:
            raise UnsupportedEvidence(
                f"cannot start the model in {source!r} ({exc})"
            ) from exc
        self._note_simulation(view)
        for cycle in getattr(view, "cycles", ()) or ():
            for item in getattr(cycle, "active_states", ()) or ():
                text = str(item)
                if text == target or text.startswith(f"{target}."):
                    return True
        return False

    def terminates(self, *, scope: str, trigger: str | None = None) -> bool:
        """The model actually finishes."""

        # `trigger=None` means "offer every declared event", so it is an absent
        # binding rather than a malformed one and must not be handed to the guard.
        optional = {"trigger": trigger} if trigger is not None else {}
        self._require_well_formed_names(scope=scope, **optional)
        # One cycle only ever saw the first step, so a final state two events
        # away was reported unreachable.  Drive the declared alphabet for a
        # bounded number of cycles instead: termination is a reachability
        # question, not a single-step one.
        alphabet = [
            str(row.qualified_name)
            for row in self.structure.events()
            if getattr(row, "qualified_name", None)
        ]
        offered = [trigger] if trigger else alphabet
        pinned = self._hot_startable(None if scope in {"", "root"} else scope)
        plan = [list(offered) for _ in range(TERMINATION_CYCLES)]
        try:
            view = (
                self.simulation.simulate(
                    initial_state=pinned, initial_vars=self._all_vars(), cycles=plan
                )
                if pinned
                else self.simulation.simulate(cycles=[[]] + plan)
            )
        except Exception as exc:
            raise UnsupportedEvidence(
                f"cannot start the model in {scope!r} ({exc})"
            ) from exc
        self._note_simulation(view)
        for cycle in getattr(view, "cycles", ()) or ():
            if bool(getattr(cycle, "is_ended", False)):
                return True
        return bool(getattr(getattr(view, "final", None), "is_ended", False))

    # ---- Family P: quantified properties -----------------------------
    def invariant(self, *, scope: str, condition: str, bound: int = DEFAULT_BOUND) -> bool:
        """Within the bound this condition always holds.

        The query is built here rather than by the producer, which is what stops
        a tautological hand-written formula from closing a real obligation.
        """

        self._require_well_formed_names(scope=scope, condition=condition)
        query = self._formal_query("invariant", scope, condition, bound)
        return self._formal_holds(query)

    def response_within(
        self,
        *,
        trigger: str,
        response: str,
        bound: int = DEFAULT_BOUND,
        source: str | None = None,
    ) -> bool:
        """Every occurrence of this trigger is answered within the bound.

        ``source`` pins the configuration the obligation is about.  Without one
        the solver places the trigger in the cold-initialization step, where
        nothing can consume it, and books that as a violation -- the predicate
        was a constant False.
        """

        # `source=None` means "no configuration was named"; only a value that is
        # present can be malformed.
        optional = {"source": source} if source is not None else {}
        self._require_well_formed_names(trigger=trigger, response=response, **optional)
        self._reject_undiscriminating_root("response_within", response=response)
        # Two things were wrong.  The response arm needs its own `within` or the
        # grammar rejects the query outright.  And with `within == bound` only
        # step 0 carries a complete obligation, so every later step lands in the
        # incomplete formula and the answer is a constant False.  Give the
        # response a window strictly inside the horizon.
        horizon = max(2, _budget(bound, "bound", DEFAULT_BOUND))
        window = max(1, horizon - 1)
        # `[*]` means the cold start, and the caller said so deliberately.
        # Falling through to `_default_init()` there would answer about whatever
        # leaf happens to come first in inspect order while the binding said
        # "before the machine starts" -- a silently different question, which is
        # the one failure this layer must never produce.  Only an *absent*
        # source gets the default, because then no configuration was named.
        if source == PSEUDO_INITIAL:
            pinned = None
        else:
            pinned = self._hot_startable(source) or self._default_init(trigger)
        head = f'init state("{pinned}"); ' if pinned else ""
        # `init state(...)` constrains step 0 only, while `check response`
        # quantifies the obligation over every step.  So the solver was free to
        # inject the trigger in some *later* configuration that cannot answer it
        # and book that as the violation -- which made the predicate True only
        # where the response state is a sink.  On the decisive pair, an identical
        # `Idle -/go-> Busy` edge answered True when `Busy` was a sink and False
        # once `Busy` could be left on an unrelated event, at every bound; over the
        # corpus, 67 edges pinned at their own source gave 6 True to 49 False.
        # Being able to leave the response state afterwards is not a violation of
        # "go is answered by Busy".
        #
        # So the trigger condition carries the configuration too, which is what
        # `source` was documented to mean.  The obligation is then "whenever the
        # trigger occurs *here*", and a model that routes it elsewhere still fails.
        occurrence = f'event("{trigger}", current)'
        if pinned:
            occurrence = f'({occurrence} && active("{pinned}"))'
        query = (
            f"{head}check response <= {horizon}: "
            f"trigger {occurrence} -> "
            f'within {window} active("{response}");'
        )
        return self._formal_holds(query)

    def persists_until(self, *, state: str, release: str, bound: int = DEFAULT_BOUND) -> bool:
        """This state holds continuously until the release condition."""

        self._reject_pseudo_initial("persists_until", state=state)
        self._require_well_formed_names(state=state, release=release)
        self._reject_undiscriminating_root("persists_until", state=state)
        # `exists_always` is a *witness* property: it asks whether some bounded
        # run keeps the condition, and with no events injected that run always
        # exists -- the truth value could not change when the defect was
        # present, which is the tautology this whole layer exists to remove.
        # The obligation is universal, so it belongs in invariant polarity:
        # until the release holds, the state must still hold.
        # `[*]` has to mean "do not pin" here too.  `_formal_query` learned
        # that; this query is hand-built and did not, so the literal went
        # straight into `init state("[*]")` and came back as an undiagnosable
        # solver failure.  One spelling, one meaning, in all five predicates
        # that accept it.
        pinned = self._hot_startable(state)
        head = f'init state("{pinned}"); ' if pinned and pinned != "root" else ""
        query = (
            f"{head}"
            f"check invariant <= {_budget(bound, 'bound', DEFAULT_BOUND)}: "
            f'({release}) || active("{state}");'
        )
        return self._formal_holds(query)

    # ---- formal plumbing ---------------------------------------------
    def _note_formal(self, result: Any) -> None:
        """Record what a bounded answer rests on.

        A refuted property exhibits a counterexample and the trace is the
        evidence.  An unrefuted one has no trace by definition, so only the
        elements the query named can be reported, marked so attribution does not
        read the absence of a counterexample as an exhibited defect.
        """

        getter = getattr(result, "get", None)
        witness = getter("witness", None) if callable(getter) else None
        refs = _witness_refs(witness) if witness is not None else []
        if refs:
            self._note(*refs)
            return
        self._note("formal:examined_only")

    def _default_init(self, trigger: str) -> str | None:
        """Pick the state a bounded response obligation should start from.

        The declared source of the trigger: that is the configuration where the
        obligation is meaningful, and pinning it keeps the solver from planting
        the event in the initialization step where nothing consumes it.

        It used to return the first leaf in inspect order, ignoring the trigger
        entirely -- so the same obligation answered True on a model whose first
        declared leaf happened to be the trigger's source and False on one that
        declares an unrelated state first.  Two models, one claim, opposite
        verdicts decided by declaration order.

        An ambiguous trigger is refused rather than resolved by picking one:
        `response_within` then reports about a source the caller did not choose,
        and the caller is the only one who knows which the requirement means.
        """

        try:
            rows = self.structure.transitions(event=trigger)
        except Exception:
            return None
        sources = sorted(
            {
                str(getattr(row, "from_path", "") or "")
                for row in rows
                if str(getattr(row, "from_path", "") or "")
                and str(getattr(row, "from_path", "")) != PSEUDO_INITIAL
            }
        )
        if len(sources) == 1:
            return sources[0]
        if not sources:
            return None
        raise UnsupportedEvidence(
            f"{trigger!r} is declared on {len(sources)} sources ({sources}); with "
            "`source` omitted the obligation would be answered about whichever "
            "one the model happens to declare first. Pin the source the "
            "requirement means, one assertion per source it ranges over."
        )

    def _formal_query(self, kind: str, scope: str, condition: str, bound: int) -> str:
        """Build the bounded query, treating `[*]` as "do not pin at all".

        `terminates` and `reaches` already read `[*]` as the cold start via
        `_hot_startable`; this path did not, and interpolated the literal
        straight into `init state("[*]")`, which the solver rejects.  The same
        spelling has to mean the same thing everywhere, or a producer that
        copies a legal binding from one predicate to another gets a failure it
        cannot diagnose.
        """

        pinned = self._hot_startable(scope)
        head = f'init state("{pinned}"); ' if pinned and pinned != "root" else ""
        return f"{head}check {kind} <= {_budget(bound, 'bound', DEFAULT_BOUND)}: {condition};"

    def _formal_holds(self, query: str) -> bool:
        if self.formal is None:
            raise UnsupportedEvidence("bounded model checking is not enabled for this run")
        try:
            result = self.formal.fbmcq(query)
        except TimeoutError as exc:
            # A solver timeout is "cannot answer", not "answered False", and no
            # rewrite of the assertion makes the model smaller.  Surfacing it as
            # a timeout sent it into the repair loop for five rounds at ~25s
            # each; as a refusal the controller quarantines it once.
            raise UnsupportedEvidence(
                f"bounded check exceeded its budget on this model ({exc}); the "
                "obligation is not decidable within the configured bound, so it "
                "must be recorded as a coverage gap rather than retried"
            ) from exc
        self._note_formal(result)
        status = getattr(result, "status", None)
        holds = getattr(result, "holds", None)
        if not isinstance(holds, bool):
            raise UnsupportedEvidence(
                f"bounded check returned no terminal verdict (status={status!r}); "
                "a non-terminal status is not a False"
            )
        return holds


def _witness_refs(witness: Any) -> list[str]:
    out: list[str] = []
    getter = getattr(witness, "get", None)
    if not callable(getter):
        return out
    for frame in getter("frames", None) or ():
        state = frame.get("state") if hasattr(frame, "get") else None
        if isinstance(state, str) and state:
            out.append(state)
    for step in getter("steps", None) or ():
        for ev in (step.get("consumed_events", None) if hasattr(step, "get") else None) or ():
            if isinstance(ev, str) and ev:
                out.append(ev)
    return out


def _read_var(container: Any, name: str) -> float | None:
    if container is None:
        return None
    getter = getattr(container, "get", None)
    value = getter(name, None) if callable(getter) else None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


#: predicate name -> (evidence family, method name).  The family is derived from
#: the predicate, never chosen by the producer.
PREDICATE_FAMILIES: dict[str, tuple[str, str]] = {
    "state_declared": ("structure", "state_declared"),
    "variable_declared": ("structure", "variable_declared"),
    "event_declared": ("structure", "event_declared"),
    "containment": ("structure", "containment"),
    "initial_target": ("structure", "initial_target"),
    "edge_declared": ("relation", "edge_declared"),
    "effect_declared": ("effect", "effect_declared"),
    "action_declared": ("structure", "action_declared"),
    "guard_distinguishable": ("relation", "guard_distinguishable"),
    "cardinality": ("structure", "cardinality"),
    "occupancy_after": ("simulation", "occupancy_after"),
    "event_consumed": ("simulation", "event_consumed"),
    "stays_in": ("simulation", "stays_in"),
    "variable_delta_after": ("simulation", "variable_delta_after"),
    "reaches": ("simulation", "reaches"),
    "terminates": ("simulation", "terminates"),
    "invariant": ("formal", "invariant"),
    "response_within": ("formal", "response_within"),
    "persists_until": ("formal", "persists_until"),
}

__all__ = [
    "DEFAULT_BOUND",
    "DEFAULT_CYCLES",
    "PREDICATE_FAMILIES",
    "PredicateAPI",
    "is_placeholder_name",
]
