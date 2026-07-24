from __future__ import annotations

import hashlib
from .pyfcstm_adapter import load_model_for_simulation
from .scenario_setup import execute_cycles
from .exceptions import UnsupportedEvidence
from .views import FrozenView


def _is_active(view: FrozenView, state: str) -> bool:
    return state in view.active_states


FINAL_METHODS = {"is_active": _is_active}
INIT_FIELDS = frozenset({"mode", "state", "is_ended", "active_states", "variables"})
CYCLE_FIELDS = frozenset(
    {
        "index",
        "is_ended",
        "active_states",
        "variables",
        "input_events",
        "consumed_events",
        "unconsumed_events",
        "fired_transitions",
        "limitations",
    }
)
SIM_FIELDS = frozenset({"cycles", "final", "model_sha256", "requested_initialization", "effective_initialization"})
SIM_METHODS = frozenset({"is_active"})


class SimulationAPI:
    """Cycle-aware pyfcstm simulation facade for direct eval assertions.

    Parameters: ``model_text`` and ``model_path`` identify the controller-frozen
    FCSTM artifact.  The facade is bound before eval; Agents do not supply paths
    or alternate model text.

    Returns: ``simulate(cycles=[...])`` returns an immutable observation with
    ``cycles``, ``final``, ``model_sha256``, ``requested_initialization``, and
    ``effective_initialization``. Every cycle exposes its index,
    terminal-safe ``is_ended`` boolean, active-state ancestry, variables,
    input/consumed/unconsumed events, fired transition field, limitations, and
    ``is_active(state)`` method. A terminated cycle has ``is_ended=True`` and an
    empty ``active_states`` tuple; use ``is_ended`` instead of calling
    ``is_active`` to prove top-level completion.

    Execution: parses the frozen model through the existing pyfcstm adapter and
    uses ``SimulationRuntime.cycle`` exactly once for each requested cycle. It
    supports default cold starts and optional exact-state hot starts with complete
    persistent variable values. It inserts no hidden initialization/stabilization
    cycle. Cold initialization is represented explicitly by a leading ``[]``.
    With ``initial_state=None``, a partial ``initial_vars`` mapping overrides
    only those declared variables; omitted variables keep declaration
    initializers and appear in ``effective_initialization``. A complete hot start
    is already initialized and does not require ``[]``.
    ``cycle.variables`` is a mapping-like frozen view keyed by the complete
    variable path; access it with ``cycle.variables["Root.counter"]`` or the
    documented variable path, never with an integer index.  ``active_states``,
    ``consumed_events``, and ``unconsumed_events`` are tuples of strings.

    For a local event-causality check, put the event in the first hot-start
    caller cycle and inspect source-state initialization, consumed/unconsumed
    events, and the resulting active state. A leading empty cycle may fire a
    completion transition before the event and make a final-state-only check
    pass for the wrong reason. In hierarchical execution the same supplied
    event may appear more than once in one cycle's ``consumed_events`` while
    nested and ancestor-level forced transitions process it. Check membership
    in ``consumed_events`` and absence from ``unconsumed_events``; do not require
    a count of exactly one or treat duplicate labels alone as a model issue.

    Failure semantics: missing model text, malformed cycle specs, or incomplete
    hot-start variables raise ``UnsupportedEvidence`` or pyfcstm ``ValueError``.
    Runtime exceptions propagate to direct eval as
    exceptions; they are not parsed as domain facts.

    Evidence limitations: simulation is one bounded trace under pyfcstm cycle
    semantics. Hot-start traces are setup evidence and do not prove the hot state
    is reachable from cold initialization. It cannot prove global correctness,
    source closure, or semantic coverage outside the asserted trace.

    Permissions: read-only in-memory simulation; no arbitrary paths, shell,
    import, environment, time/random, network, mutation, or reference/gold data.

    Example: ``simulate(cycles=[[], ["Root.go"]]).final.is_active("Root.Done")``
    checks one cold-start path. ``simulate(initial_state="Root.Idle",
    initial_vars={}, cycles=[["Root.go"]])`` checks the event directly from a
    complete hot start; confirm ``Root.go`` appears in cycle 0
    ``consumed_events`` before attributing the target state to that event.
    ``simulate(cycles=[[], ["Root.stop"]]).final.is_ended is True`` checks an
    explicit top-level termination result without reading ``current_state``.
    """

    family = "simulation"

    def __init__(self, model_text: str | None, model_path: str = "<memory>") -> None:
        self.model_text = model_text
        self.model_path = model_path

    def simulate(
        self,
        *,
        cycles: list[list[str]],
        initial_state: str | None = None,
        initial_vars: dict[str, int | float] | None = None,
    ) -> FrozenView:
        if not isinstance(self.model_text, str) or not self.model_text.strip():
            raise UnsupportedEvidence("simulation requires frozen model_text")
        if (
            not isinstance(cycles, list)
            or not cycles
            or not all(
                isinstance(cycle, list)
                and all(isinstance(event, str) for event in cycle)
                for cycle in cycles
            )
        ):
            raise UnsupportedEvidence("cycles must be a non-empty list[list[str]]")
        model = load_model_for_simulation(self.model_text, self.model_path)
        _current_state, trace, requested_initialization, effective_initialization = execute_cycles(
            model, cycles, initial_state=initial_state, initial_vars=initial_vars
        )
        cycle_views = tuple(
            FrozenView(
                "simulation.cycle",
                item,
                allowed_fields=CYCLE_FIELDS,
                allowed_methods=SIM_METHODS,
                methods=FINAL_METHODS,
            )
            for item in trace
        )
        return FrozenView(
            "simulation",
            {
                "cycles": cycle_views,
                "final": cycle_views[-1],
                "model_sha256": hashlib.sha256(self.model_text.encode("utf-8")).hexdigest(),
                "requested_initialization": FrozenView(
                    "simulation.initialization",
                    requested_initialization,
                    allowed_fields=INIT_FIELDS,
                ),
                "effective_initialization": FrozenView(
                    "simulation.initialization",
                    effective_initialization,
                    allowed_fields=INIT_FIELDS,
                ),
            },
            allowed_fields=SIM_FIELDS,
            allowed_methods=frozenset(),
        )


__all__ = ["CYCLE_FIELDS", "INIT_FIELDS", "SIM_FIELDS", "SIM_METHODS", "SimulationAPI"]
