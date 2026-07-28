"""The 17 predicates of issue #170, as the only evidence calls an assertion may make.

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

``UNDECLARED`` is the binding value the splitter uses when the NL requires a term
the model does not declare.  Any predicate handed it raises immediately: the
absence is the finding, and no check can stand in for it.
"""

from __future__ import annotations

from typing import Any

from .exceptions import UnsupportedEvidence

#: Written by the splitter when the NL names something the model never declares.
UNDECLARED = "<undeclared>"

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


def _require_declared(**bindings: Any) -> None:
    """Refuse to answer a claim whose terms the model does not declare."""

    missing = sorted(k for k, v in bindings.items() if v == UNDECLARED)
    if missing:
        raise UnsupportedEvidence(
            f"binding(s) {missing} are {UNDECLARED}: the NL requires a term the "
            "model does not declare, so this obligation has no executable check. "
            "The absence is the finding; record it rather than testing around it."
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
            if isinstance(ref, str) and ref and ref != UNDECLARED:
                self._refs.append(ref)

    # ---- helpers -----------------------------------------------------
    @staticmethod
    def _hot_startable(source: str | None) -> str | None:
        """Return the state to hot-start from, or None for the initial config."""

        if not source or source == PSEUDO_INITIAL:
            return None
        return source

    def _simulate(self, *, source: str | None, trigger: str | None, cycles: int):
        """Run the smallest trace that can witness ``trigger`` fired from ``source``.

        A cold start plus the event is used when no source is given; otherwise a
        hot start pins the configuration so the observation is about that state
        and not about whatever the machine drifted into.
        """

        events = [[trigger]] if trigger else [[]]
        events += [[] for _ in range(max(0, cycles - 1))]
        source = self._hot_startable(source)
        view = None
        if source:
            try:
                view = self.simulation.simulate(
                    initial_state=source, initial_vars=self._all_vars(), cycles=events
                )
            except Exception:
                # A composite or otherwise non-hot-startable source falls back to a
                # cold start; the trace is weaker but still honest.
                view = None
        if view is None:
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
    def _active(view: Any) -> tuple[str, ...]:
        final = getattr(view, "final", None)
        states = getattr(final, "active_states", ()) if final is not None else ()
        return tuple(str(s) for s in states or ())

    # ---- Family S: what the artifact declares ------------------------
    def state_declared(self, *, state: str, kind: str) -> bool:
        """The model declares a state at this path, of this kind."""

        _require_declared(state=state)
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

    def containment(self, *, parent: str, child: str) -> bool:
        """This child is a direct substate of this parent."""

        _require_declared(parent=parent, child=child)
        self._note(parent, child)
        rows = self.structure.states(
            parent=_need(parent, "parent"), recursive=False, exact=True
        )
        return _need(child, "child") in {str(r.path) for r in rows}

    def initial_target(self, *, composite: str, child: str) -> bool:
        """Entering this composite starts in this child."""

        _require_declared(composite=composite, child=child)
        self._note(composite, child)
        return self.structure.initial_child(_need(composite, "composite")) == _need(
            child, "child"
        )

    def edge_declared(self, *, source: str, trigger: str, target: str) -> bool:
        """The model declares an edge with this source, trigger and target."""

        _require_declared(source=source, trigger=trigger, target=target)
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

        _require_declared(source=source, trigger=trigger, variable=variable)
        self._note(source, trigger, variable)
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

        _require_declared(state=state)
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

        _require_declared(source=source, trigger=trigger)
        self._note(source, trigger)
        self._note_transitions(source=source, event=trigger)
        return not bool(self.relations.conflicting_targets(source=source, event=trigger))

    def cardinality(self, *, scope: str, count: int) -> bool:
        """This scope declares exactly this many non-pseudo direct substates."""

        _require_declared(scope=scope)
        self._note(scope)
        try:
            want = int(count)
        except Exception as exc:
            raise UnsupportedEvidence(f"count must be an integer, got {count!r}") from exc
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

        _require_declared(source=source, trigger=trigger, target=target)
        view = self._simulate(source=source, trigger=trigger, cycles=int(within_cycles))
        active = self._active(view)
        return any(s == target or s.startswith(f"{target}.") for s in active)

    def event_consumed(self, *, source: str, trigger: str) -> bool:
        """In this configuration the event is actually consumed.

        There is no static substitute: an event being declared does not mean any
        configuration accepts it.
        """

        _require_declared(source=source, trigger=trigger)
        view = self._simulate(source=source, trigger=trigger, cycles=1)
        for cycle in getattr(view, "cycles", ()) or ():
            if trigger in (getattr(cycle, "consumed_events", ()) or ()):
                return True
        return False

    def stays_in(self, *, source: str, trigger: str) -> bool:
        """After this trigger the system remains in the same state."""

        _require_declared(source=source, trigger=trigger)
        view = self._simulate(source=source, trigger=trigger, cycles=1)
        active = self._active(view)
        return any(s == source or s.startswith(f"{source}.") for s in active)

    def variable_delta_after(
        self, *, source: str, trigger: str, variable: str, sign: str
    ) -> bool:
        """Running this trigger changes this variable in this direction.

        Distinct from ``effect_declared``: an effect can be declared on an edge
        the executed path never reaches.
        """

        _require_declared(source=source, trigger=trigger, variable=variable)
        want = str(sign).strip().lower()
        if want not in {"negative", "positive"}:
            raise UnsupportedEvidence(f"sign must be negative or positive, got {sign!r}")
        view = self._simulate(source=source, trigger=trigger, cycles=1)
        cycles = getattr(view, "cycles", ()) or ()
        if not cycles:
            return False
        before = getattr(getattr(view, "effective_initialization", None), "variables", None)
        start = _read_var(before, variable)
        end = _read_var(getattr(cycles[-1], "variables", None), variable)
        if start is None or end is None:
            raise UnsupportedEvidence(
                f"variable {variable!r} is not observable in the simulation state"
            )
        return (end - start) < 0 if want == "negative" else (end - start) > 0

    def reaches(self, *, source: str, target: str, within_cycles: int = 3) -> bool:
        """Within a bounded number of cycles this target is reachable from here."""

        _require_declared(source=source, target=target)
        view = self._simulate(source=source, trigger=None, cycles=int(within_cycles))
        for cycle in getattr(view, "cycles", ()) or ():
            for s in getattr(cycle, "active_states", ()) or ():
                if str(s) == target or str(s).startswith(f"{target}."):
                    return True
        return False

    def terminates(self, *, scope: str, trigger: str | None = None) -> bool:
        """The model actually finishes."""

        _require_declared(scope=scope)
        view = self._simulate(
            source=None if scope in {"", "root"} else scope,
            trigger=trigger,
            cycles=DEFAULT_CYCLES,
        )
        final = getattr(view, "final", None)
        return bool(getattr(final, "is_ended", False))

    # ---- Family P: quantified properties -----------------------------
    def invariant(self, *, scope: str, condition: str, bound: int = DEFAULT_BOUND) -> bool:
        """Within the bound this condition always holds.

        The query is built here rather than by the producer, which is what stops
        a tautological hand-written formula from closing a real obligation.
        """

        _require_declared(scope=scope, condition=condition)
        query = self._formal_query("invariant", scope, condition, bound)
        return self._formal_holds(query)

    def response_within(
        self, *, trigger: str, response: str, bound: int = DEFAULT_BOUND
    ) -> bool:
        """Every occurrence of this trigger is answered within the bound."""

        _require_declared(trigger=trigger, response=response)
        # The response arm needs its own `within`; without it the grammar rejects
        # the query and the predicate can only ever raise.  No test executed this
        # predicate, which is how a dead one shipped.
        query = (
            f"check response <= {int(bound)}: "
            f'trigger event("{trigger}", current) -> '
            f'within {int(bound)} active("{response}");'
        )
        return self._formal_holds(query)

    def persists_until(self, *, state: str, release: str, bound: int = DEFAULT_BOUND) -> bool:
        """This state holds continuously until the release condition."""

        _require_declared(state=state, release=release)
        query = (
            f'init state("{state}"); '
            f"check exists_always <= {int(bound)}: "
            f'active("{state}") && !({release});'
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

    def _formal_query(self, kind: str, scope: str, condition: str, bound: int) -> str:
        head = f'init state("{scope}"); ' if scope and scope not in {"root", ""} else ""
        return f"{head}check {kind} <= {int(bound)}: {condition};"

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

__all__ = ["DEFAULT_BOUND", "DEFAULT_CYCLES", "PREDICATE_FAMILIES", "PredicateAPI", "UNDECLARED"]
