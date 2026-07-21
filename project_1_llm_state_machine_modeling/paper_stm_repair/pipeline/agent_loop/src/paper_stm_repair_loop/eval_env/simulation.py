from __future__ import annotations

import hashlib
from ..pyfcstm_adapter import load_model_for_simulation
from ..scenario_setup import execute_cycles
from .exceptions import UnsupportedEvidence
from .views import FrozenView


def _is_active(view: FrozenView, state: str) -> bool:
    return state in view.active_states


FINAL_METHODS = {"is_active": _is_active}
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
SIM_FIELDS = frozenset({"cycles", "final", "model_sha256"})
SIM_METHODS = frozenset({"is_active"})


class SimulationAPI:
    """Cycle-aware pyfcstm simulation facade for direct eval assertions.

    Parameters: ``model_text`` and ``model_path`` identify the controller-frozen
    FCSTM artifact.  The facade is bound before eval; Agents do not supply paths
    or alternate model text.

    Returns: ``simulate(cycles=[...])`` returns an immutable observation with
    ``cycles``, ``final``, and ``model_sha256``. Every cycle exposes its index,
    terminal-safe ``is_ended`` boolean, active-state ancestry, variables,
    input/consumed/unconsumed events, fired transition field, limitations, and
    ``is_active(state)`` method. A terminated cycle has ``is_ended=True`` and an
    empty ``active_states`` tuple; use ``is_ended`` instead of calling
    ``is_active`` to prove top-level completion.

    Execution: parses the frozen model through the existing pyfcstm adapter and
    uses ``SimulationRuntime.cycle`` exactly once for each requested cycle. It
    inserts no hidden initialization/stabilization cycle. Eventless
    initialization or stabilization is represented explicitly by ``[]`` in the
    caller-provided cycle list and preserved in the result.

    Failure semantics: missing model text or malformed cycle specs raise
    ``UnsupportedEvidence``.  Runtime exceptions propagate to direct eval as
    exceptions; they are not parsed as domain facts.

    Evidence limitations: simulation is one bounded trace under pyfcstm cycle
    semantics.  It cannot prove global correctness, source closure, or semantic
    coverage outside the asserted trace.

    Permissions: read-only in-memory simulation; no arbitrary paths, shell,
    import, environment, time/random, network, mutation, or reference/gold data.

    Example: ``simulate(cycles=[[], ["Root.go"]]).final.is_active("Root.Done")``
    checks the final active state after an explicit empty cycle and one event
    cycle. ``simulate(cycles=[[], ["Root.stop"]]).final.is_ended is True`` checks
    an explicit top-level termination result without reading ``current_state``.
    """

    family = "simulation"

    def __init__(self, model_text: str | None, model_path: str = "<memory>") -> None:
        self.model_text = model_text
        self.model_path = model_path

    def simulate(self, *, cycles: list[list[str]]) -> FrozenView:
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
        _current_state, trace = execute_cycles(model, cycles)
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
            },
            allowed_fields=SIM_FIELDS,
            allowed_methods=frozenset(),
        )


__all__ = ["CYCLE_FIELDS", "SIM_FIELDS", "SIM_METHODS", "SimulationAPI"]
