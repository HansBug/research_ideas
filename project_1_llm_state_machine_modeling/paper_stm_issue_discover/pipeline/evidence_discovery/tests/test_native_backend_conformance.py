"""Native FCSTM conformance tests for every frozen predicate backend.

These fixtures are deliberately small FCSTM programs, not ModelIR graph
stand-ins.  They exercise the production dispatch with actual
``pyfcstm.model``, ``pyfcstm.verify.topology``, ``SimulationRuntime``, and
``fbmcq`` execution paths.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from typing import Any

import pytest

from pipeline.evidence_discovery.backends import run_backend
from pipeline.evidence_discovery.backends.fcstm_native import (
    all_events,
    all_transition_carriers,
    load_native_fcstm,
    state_path,
    transition_by_ref,
)
from pipeline.evidence_discovery.compiler.inputs import (
    UnsupportedPredicateInputs,
    validate_predicate_inputs,
)
from pipeline.evidence_discovery.compiler.lowering import PredicatePlan, SUPPORTED_PREDICATES
from pipeline.evidence_discovery.inputs import parse_fcstm


_STRUCTURAL_SOURCE = """
def int x = 0;
state Root {
    state A {
        enter abstract Start;
        during abstract Tick;
    }
    state B;
    state C;
    [*] -> A;
    A -> B : Go + [x >= 0] effect { x = 1; }
    A -> C : Go + [x < 0];
    B -> B : Go;
}
"""

_TOPOLOGY_SOURCE = """
state Root {
    state A;
    state B;
    state C;
    [*] -> A;
    A -> B;
    B -> [*];
}
"""

_CHOICE_SOURCE = """
def int x = 0;
state Root {
    state Disjoint;
    state Overlap;
    state Gap;
    state B;
    state C;
    [*] -> Disjoint;
    Disjoint -> B : Choice + [x < 0];
    Disjoint -> C : Choice + [x >= 0];
    Overlap -> B : OverlapEvent + [x >= 0];
    Overlap -> C : OverlapEvent + [x <= 0];
    Gap -> B : GapEvent + [x < 0];
    Gap -> C : GapEvent + [x > 0];
}
"""

_V5_SOURCE = """
state Root {
    state A;
    state B;
    [*] -> A;
}
"""


def _model(source: str):
    """Parse a complete FCSTM fixture through the production input facade."""

    return parse_fcstm(source)


def _transition_ref(model: Any, source: str, target: str) -> str:
    """Get one production grammar-span reference without inventing a carrier."""

    matches = [
        transition.ref
        for transition in model.transitions
        if transition.source == source and transition.target == target
    ]
    assert len(matches) == 1
    return matches[0]


def _event_path(model: Any, name: str) -> str:
    """Resolve one unique event through the native FCSTM model."""

    native = load_native_fcstm(model)
    matches = [event.path_name for event in all_events(native) if event.name == name]
    assert len(matches) == 1
    return matches[0]


def _guard_texts(model: Any, source: str) -> tuple[str, ...]:
    """Obtain exact guard AST renderings from the native choice group."""

    native = load_native_fcstm(model)
    return tuple(
        str(transition.guard.to_ast_node())
        for transition in all_transition_carriers(native)
        if transition.source in {source, f"Root.{source}"} and transition.guard is not None
    )


def _runtime_scenario(model: Any, *, selected: bool) -> dict[str, Any]:
    """Build a closed runtime input whose truth comes from SimulationRuntime."""

    go = _event_path(model, "Go")
    transition = _transition_ref(model, "A", "B")
    scenario: dict[str, Any] = {
        "schema": "evidence-discovery.fcstm-runtime-scenario.v2",
        "initialization": "cold",
        "root_state": state_path(load_native_fcstm(model).machine.root_state),
        "event_queue": [go],
        "schedule": [
            {"step": 0, "event_paths": []},
            {"step": 1, "event_paths": [go]},
            {"step": 2, "event_paths": []},
        ],
        "reason": "The fixture completes native cold entry before dispatching its only Go event, then observes one trailing macrostep.",
        "basis": "native FCSTM event path and grammar-span transition identity",
    }
    if selected:
        scenario.update(
            {
                "selected_step": 1,
                "selected_event_path": go,
                "selected_transition_ref": transition,
                "expected_active_before": "Root.A",
                "expected_active_after": "Root.B",
            }
        )
    return scenario


def _plan(predicate_id: str, values: dict[str, Any], *, executable: bool = True) -> PredicatePlan:
    """Create a production-shaped plan for one native backend fixture."""

    typed = validate_predicate_inputs(predicate_id, values)
    is_valid = not isinstance(typed, UnsupportedPredicateInputs)
    program = f"fixture ASSERT {predicate_id}"
    return PredicatePlan(
        plan_id=f"fixture:{predicate_id}:plan",
        predicate_id=predicate_id,
        registry_version="four-family-12-core.v1",
        inputs=typed,
        soundness_fragment="fixture closed FCSTM fragment",
        assumptions=("closed_fcstm_input",),
        formal_program=program if executable else None,
        formal_program_hash=("sha256:" + hashlib.sha256(program.encode("utf-8")).hexdigest()) if executable else None,
        predicate_registered=True,
        binding_precise=True,
        input_shape_valid=is_valid and executable,
        binding_complete=is_valid and executable,
        backend_available=True,
        soundness_fragment_satisfied=is_valid and executable,
        artifact_attribution_complete=is_valid and executable,
        supported=is_valid and executable,
        executable=is_valid and executable,
        reason="Native backend conformance fixture.",
        basis="Frozen predicate contract and native FCSTM fixture.",
        predicate_name=predicate_id,
        family="fixture",
        semantics="Fixture preserves the frozen predicate semantics.",
    )


def test_combo_transition_carrier_preserves_authored_native_semantics() -> None:
    """Generated combo relays retain their authored endpoint and payload binding."""

    model = _model(_STRUCTURAL_SOURCE)
    native = load_native_fcstm(model)
    carrier = transition_by_ref(native, _transition_ref(model, "A", "B"))

    assert carrier is not None
    assert carrier.combo_origin_id is not None
    assert len(carrier.native_transitions) > 1
    assert (carrier.source, carrier.target, carrier.owner_path) == ("A", "B", "Root")
    assert carrier.event is not None
    assert carrier.event.path_name == _event_path(model, "Go")
    assert str(carrier.guard.to_ast_node()) == "x >= 0"
    assert len(carrier.effects) == 1


def _fixture_cases() -> dict[str, dict[str, Any]]:
    """Return positive, negative, and out-of-fragment inputs for all 19 IDs."""

    structural = _model(_STRUCTURAL_SOURCE)
    topology = _model(_TOPOLOGY_SOURCE)
    choice = _model(_CHOICE_SOURCE)
    invariant = _model(_V5_SOURCE)
    ab = _transition_ref(structural, "A", "B")
    bb = _transition_ref(structural, "B", "B")
    go = _event_path(structural, "Go")
    choice_event = _event_path(choice, "Choice")
    overlap_event = _event_path(choice, "OverlapEvent")
    gap_event = _event_path(choice, "GapEvent")
    runtime = _runtime_scenario(structural, selected=True)
    unclosed_runtime = {**runtime, "root_state": "Not.Root"}
    finite_domain = {"x": {"values": [-1, 0, 1]}}
    return {
    "S1": {
            "model": structural,
            "positive": {"kind": "state", "element": "A", "scope": "closed_fcstm"},
            "negative": {"kind": "state", "element": "Missing", "scope": "closed_fcstm"},
            "out": {"kind": "state", "element": "A", "scope": "Not.Root"},
        },
    "S2": {
            "model": structural,
            "positive": {"source": "A", "target": "B", "scope": "Root", "transition": ab},
            "negative": {"source": "B", "target": "A", "scope": "Root"},
            "out": {"source": "A", "target": "B", "scope": "Not.Root"},
        },
    "S3": {
            "model": structural,
            "positive": {"transition": ab, "triggers": ["Go"]},
            "negative": {"transition": ab, "triggers": []},
            "out": {"transition": "transition:line:999", "triggers": ["Go"]},
        },
    "S4": {
            "model": structural,
            "positive": {"state": "A", "phase": "entry", "action": "Start"},
            "negative": {"state": "A", "phase": "entry", "action": "Missing"},
            "out": {"state": "Not.A", "phase": "entry", "action": "Start"},
        },
    "S5": {
            "model": structural,
            "positive": {"transition": ab, "guard": "x >= 0"},
            "negative": {"transition": ab, "guard": "x > 3"},
            "out": {"transition": ab, "guard": "x >"},
            "empty_positive": {"transition": bb, "guard": ""},
            "empty_negative": {"transition": ab, "guard": ""},
        },
    "G1": {
            "model": topology,
            "positive": {"source": "A", "target": "B"},
            "negative": {"source": "B", "target": "A"},
            "out": {"source": "Not.A", "target": "B"},
        },
    "G2": {
            "model": topology,
            "positive": {"source": "A", "target": "B"},
            "negative": {"source": "B", "target": "A"},
            "out": {"source": "Not.A", "target": "B"},
        },
    "G3": {
            "model": topology,
            "positive": {"roots": ["A"], "marked": ["B"]},
            "negative": {"roots": ["A"], "marked": ["C"]},
            "out": {"roots": ["Not.A"], "marked": ["B"]},
        },
    "R1": {
            "model": structural,
            "positive": {"scenario": runtime, "event": "Go", "step": 1},
            "negative": {"scenario": {**runtime, "expected_active_after": "Root.C"}, "event": "Go", "step": 1},
            "out": {"scenario": unclosed_runtime, "event": "Go", "step": 1},
        },
    "R2": {
            "model": structural,
            "positive": {"scenario": runtime, "stimulus": go, "state": "B", "window": [1, 2]},
            "negative": {"scenario": runtime, "stimulus": go, "state": "C", "window": [1, 2]},
            "out": {"scenario": unclosed_runtime, "stimulus": go, "state": "B", "window": [1, 2]},
        },
    "R3": {
            "model": structural,
            "positive": {"scenario": runtime, "state": "B", "interval": [1, 2]},
            "negative": {"scenario": runtime, "state": "A", "interval": [1, 2]},
            "out": {"scenario": unclosed_runtime, "state": "B", "interval": [1, 2]},
        },
    "V1": {
            "model": topology,
            "positive": {"initial_scope": "closed_fcstm"},
            "negative": {"initial_scope": "C"},
            "out": {"initial_scope": "Not.Root"},
        },
}


@pytest.fixture(scope="module")
def native_cases() -> dict[str, dict[str, Any]]:
    """Provide the complete frozen-ID conformance matrix once per test module."""

    return _fixture_cases()


def test_all_frozen_predicates_have_native_dispatch() -> None:
    """The public backend capability set must exactly match the frozen registry."""

    assert SUPPORTED_PREDICATES == {"S1", "S2", "S3", "S4", "S5", "G1", "G2", "G3", "R1", "R2", "R3", "V1"}


@pytest.mark.parametrize("predicate_id", sorted(SUPPORTED_PREDICATES))
def test_each_predicate_rejects_invalid_typed_shape(predicate_id: str) -> None:
    """Extra/untyped values never enter any frozen backend as executable input."""

    typed = validate_predicate_inputs(predicate_id, {"not_a_typed_input": "invalid"})
    assert isinstance(typed, UnsupportedPredicateInputs)
    plan = _plan(predicate_id, {"not_a_typed_input": "invalid"}, executable=False)
    receipt = run_backend(plan, _model(_STRUCTURAL_SOURCE), f"fixture:{predicate_id}:invalid")
    assert receipt.terminal_state == "unsupported"
    assert receipt.verdict == "unknown"
    assert receipt.run_metadata["failure_kind"] == "invalid_input"


@pytest.mark.parametrize("predicate_id", sorted(SUPPORTED_PREDICATES))
def test_each_predicate_uses_native_positive_and_negative_truth(
    predicate_id: str,
    native_cases: dict[str, dict[str, Any]],
) -> None:
    """Every predicate obtains both Boolean outcomes from its native FCSTM path."""

    case = native_cases[predicate_id]
    positive = run_backend(
        _plan(predicate_id, case["positive"]),
        case["model"],
        f"fixture:{predicate_id}:positive",
    )
    negative = run_backend(
        _plan(predicate_id, case["negative"]),
        case["model"],
        f"fixture:{predicate_id}:negative",
    )
    assert (positive.terminal_state, positive.verdict) == ("completed", "true")
    assert (negative.terminal_state, negative.verdict) == ("completed", "false")
    assert positive.run_metadata["execution_model"] == "pyfcstm.model.StateMachine"
    assert negative.run_metadata["execution_model"] == "pyfcstm.model.StateMachine"


def test_s5_compares_explicit_empty_guard_with_native_absence(
    native_cases: dict[str, dict[str, Any]],
) -> None:
    """Empty guard is a deliberate equality value, not an incomplete input."""

    case = native_cases["S5"]
    absent = run_backend(
        _plan("S5", case["empty_positive"]),
        case["model"],
        "fixture:S5:empty-guard-positive",
    )
    guarded = run_backend(
        _plan("S5", case["empty_negative"]),
        case["model"],
        "fixture:S5:empty-guard-negative",
    )

    assert (absent.terminal_state, absent.verdict) == ("completed", "true")
    assert (guarded.terminal_state, guarded.verdict) == ("completed", "false")


@pytest.mark.parametrize("predicate_id", sorted(SUPPORTED_PREDICATES))
def test_each_predicate_preserves_out_of_fragment_as_non_boolean(
    predicate_id: str,
    native_cases: dict[str, dict[str, Any]],
) -> None:
    """Input closure failures are never silently converted into false findings."""

    case = native_cases[predicate_id]
    receipt = run_backend(
        _plan(predicate_id, case["out"]),
        case["model"],
        f"fixture:{predicate_id}:out-of-fragment",
    )
    assert receipt.verdict == "unknown"
    assert receipt.terminal_state != "completed"


@pytest.mark.parametrize("predicate_id", sorted(SUPPORTED_PREDICATES))
def test_each_predicate_loader_error_is_a_terminal_failure(
    predicate_id: str,
    native_cases: dict[str, dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A native backend failure is auditable and cannot become a Boolean claim."""

    from pipeline.evidence_discovery.backends import bounded_verification, source_static, topology, trajectory

    module_by_family: dict[str, Any] = {
        "S": source_static,
        "G": topology,
        "R": trajectory,
        "V": bounded_verification,
    }

    def fail_loader(_model: Any) -> Any:
        raise RuntimeError("controlled native loader failure")

    monkeypatch.setattr(module_by_family[predicate_id[0]], "load_native_fcstm", fail_loader)
    case = native_cases[predicate_id]
    receipt = run_backend(
        _plan(predicate_id, case["positive"]),
        case["model"],
        f"fixture:{predicate_id}:loader-error",
    )
    assert receipt.terminal_state == "error"
    assert receipt.verdict == "unknown"
    assert receipt.run_metadata["failure_kind"] == "backend_error"
