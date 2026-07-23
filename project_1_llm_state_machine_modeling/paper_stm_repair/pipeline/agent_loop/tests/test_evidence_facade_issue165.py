from __future__ import annotations

from paper_stm_repair_loop.eval_env.runtime import EvalEnvironment
from paper_stm_repair_loop.eval_env.simulation import SimulationAPI
from paper_stm_repair_loop.eval_env.structure import StructureAPI
from paper_stm_repair_loop.pyfcstm_adapter import check_fcstm
from paper_stm_repair_loop.schemas.tools import ObserveTraceInput, QueryModelInput
from paper_stm_repair_loop.tools import observe_trace, query_model

MODEL = """def int count = 1;
def int flag = 0;
state Root {
    event go;
    event stop;
    state Idle;
    state Work {
        state A;
        state B;
        [*] -> A;
        A -> B : go effect { count = count + 1; }
    }
    [*] -> Idle;
    Idle -> Work : go;
}
"""

EVENT_CAUSALITY_MODEL = """state Root {
    event Brake;
    state Human;
    state Auto {
        state Final;
        [*] -> Final;
        Final -> [*];
    }
    [*] -> Auto;
    !Auto -> Human : Brake;
    Auto -> Human;
}
"""


def _inspect() -> dict:
    checked = check_fcstm(MODEL)
    assert checked["inspect_status"] == "ok"
    return checked["inspect"]


def test_tool_schemas_accept_strict_query_operation_and_hot_start_fields():
    query = QueryModelInput.model_validate(
        {
            "query_kind": "transitions",
            "operation": "path",
            "source": "Root.Idle",
            "target": "Root.Work.B",
            "max_hops": 3,
            "root_node_ids": ["ROOT-001"],
            "reason": "Resolve one path gap.",
        }
    )
    assert query.operation == "path"
    assert query.source == "Root.Idle"

    observe = ObserveTraceInput.model_validate(
        {
            "question": "Hot start from exact state.",
            "root_node_ids": ["ROOT-001"],
            "cycles": [["Root.Work.go"]],
            "initial_state": "Root.Work.A",
            "initial_vars": {"count": 1, "flag": 0},
            "reason": "Resolve one hot-start trace gap.",
        }
    )
    assert observe.initial_state == "Root.Work.A"
    assert observe.initial_vars == {"count": 1, "flag": 0}


def test_structure_filters_support_exact_path_and_within_without_suffix_ambiguity():
    api = StructureAPI(_inspect())

    assert [state.path for state in api.states(name="A", exact=True)] == ["Root.Work.A"]
    assert [state.path for state in api.states(path="Root.Work.A", exact=True)] == ["Root.Work.A"]
    assert [state.path for state in api.states(within="Root.Work")] == [
        "Root.Work",
        "Root.Work.A",
        "Root.Work.B",
    ]
    assert api.states(path="Work.A", exact=True) == ()
    assert api.transition_exists(source="Root.Work.A", event="Root.Work.go", target="Root.Work.B", exact=True)
    assert not api.transition_exists(source="Work.A", event="go", target="Work.B", exact=True)


def test_query_model_strict_entities_topology_and_path_operations():
    inspect_data = {"model_sha256": "m1", **_inspect()}

    entities = query_model.execute(
        inspect_data,
        query_kind="states",
        operation="entities",
        path="Root.Work.A",
        exact=True,
        reason="Find the exact Work.A state.",
    )
    assert entities["execution_status"] == "completed"
    assert [item["path"] for item in entities["matched_items"]] == ["Root.Work.A"]
    assert entities["requested_filters"]["path"] == "Root.Work.A"
    assert entities["effective_filters"]["exact"] is True

    topology = query_model.execute(
        inspect_data,
        query_kind="states",
        operation="topology",
        within="Root.Work",
        reason="Inspect deterministic topology within Work.",
    )
    assert topology["execution_status"] == "completed"
    assert topology["topology"]["states"] == ["Root.Work", "Root.Work.A", "Root.Work.B"]
    assert {edge["source"] for edge in topology["topology"]["transitions"]} == {"Root.Work", "Root.Work.A"}

    path = query_model.execute(
        inspect_data,
        query_kind="transitions",
        operation="path",
        source="Root.Idle",
        target="Root.Work.B",
        max_hops=3,
        reason="Find a bounded deterministic transition path.",
    )
    assert path["execution_status"] == "completed"
    assert path["paths"][0]["states"] == ["Root.Idle", "Root.Work", "Root.Work.A", "Root.Work.B"]
    assert path["paths"][0]["events"] == ["Root.go", None, "Root.Work.go"]


def test_query_model_machine_backed_topology_and_path_apply_filters():
    inspect_data = {"model_sha256": "m1", "model": {"content": MODEL}, **_inspect()}

    topology = query_model.execute(
        inspect_data,
        query_kind="states",
        operation="topology",
        within="Root.Work",
        reason="Machine-backed topology must be scoped to Work.",
    )
    assert topology["execution_status"] == "completed"
    assert "Root.Idle" not in topology["topology"]["states"]
    assert all(
        edge["source"].startswith("Root.Work") and edge["target"].startswith("Root.Work")
        for edge in topology["topology"]["transitions"]
    )

    stop_path = query_model.execute(
        inspect_data,
        query_kind="transitions",
        operation="path",
        source="Root.Idle",
        target="Root.Work.B",
        event="Root.stop",
        max_hops=3,
        reason="A stop-filtered path must not overclaim the go path.",
    )
    assert stop_path["execution_status"] == "completed"
    assert stop_path["total_matches"] == 0
    assert stop_path["paths"][0]["exists"] is False
    assert stop_path["paths"][0]["events"] == []

    scoped_path = query_model.execute(
        inspect_data,
        query_kind="transitions",
        operation="path",
        source="Root.Idle",
        target="Root.Work.B",
        within="Root.Work",
        max_hops=3,
        reason="Source outside Work scope must be absent rather than overclaimed.",
    )
    assert scoped_path["execution_status"] == "completed"
    assert scoped_path["total_matches"] == 0
    assert scoped_path["paths"][0]["exists"] is False
    assert "source_or_target_outside_query_scope" in scoped_path["paths"][0]["limitations"]

    avoided_path = query_model.execute(
        inspect_data,
        query_kind="transitions",
        operation="path",
        source="Root.Idle",
        target="Root.Work.B",
        event="Root.go",
        avoid=["Root.Work.A"],
        max_hops=3,
        reason="The event-filtered path must still honor avoid.",
    )
    assert avoided_path["execution_status"] == "completed"
    assert avoided_path["paths"][0]["exists"] is False

    suffix_path = query_model.execute(
        inspect_data,
        query_kind="transitions",
        operation="path",
        source="Idle",
        target="B",
        event="go",
        exact=False,
        max_hops=3,
        reason="Unique suffix references resolve to qualified paths.",
    )
    assert suffix_path["total_matches"] == 1
    assert suffix_path["paths"][0]["exists"] is True
    assert suffix_path["paths"][0]["nodes"] == [
        "Root.Idle",
        "Root.Work",
        "Root.Work.A",
        "Root.Work.B",
    ]

    eventless_only = query_model.execute(
        inspect_data,
        query_kind="transitions",
        operation="path",
        source="Root.Work",
        target="Root.Work.A",
        event="Root.stop",
        max_hops=1,
        reason="An event-filtered query must consume at least one matching event edge.",
    )
    assert eventless_only["total_matches"] == 0
    assert eventless_only["paths"][0]["exists"] is False
    assert eventless_only["paths"][0]["limitations"]

    unsupported = query_model.execute(
        inspect_data,
        query_kind="states",
        operation="topology",
        within="Root.Work",
        event="Root.go",
        reason="Unsupported topology filters must fail closed.",
    )
    assert unsupported["execution_status"] == "invalid_arguments"
    assert "unsupported_topology_filters" in unsupported["limitations"]
    assert "unsupported_filter:event" in unsupported["limitations"]


def test_query_model_filtered_entity_queries_do_not_complete_whole_category_gate():
    tool = query_model.build_tool({"model_sha256": "m1", **_inspect()})

    first = tool.invoke(
        {
            "query_kind": "states",
            "operation": "entities",
            "path": "Root.Work.A",
            "exact": True,
            "limit": 10,
            "reason": "Fetch filtered state A for one structural gap.",
        }
    )
    second = tool.invoke(
        {
            "query_kind": "states",
            "operation": "entities",
            "path": "Root.Work.B",
            "exact": True,
            "limit": 10,
            "reason": "Fetch filtered state B for a distinct structural gap.",
        }
    )

    assert first["execution_status"] == "completed"
    assert first["truncated"] is False
    assert [item["path"] for item in first["matched_items"]] == ["Root.Work.A"]
    assert second["execution_status"] == "completed"
    assert [item["path"] for item in second["matched_items"]] == ["Root.Work.B"]
    assert "category_already_returned_untruncated" not in second["limitations"]
    assert "duplicate_query_not_executed" not in second["limitations"]


def test_query_model_unfiltered_complete_entity_page_still_completes_category_gate():
    tool = query_model.build_tool({"model_sha256": "m1", **_inspect()})

    first = tool.invoke(
        {
            "query_kind": "states",
            "operation": "entities",
            "offset": 0,
            "limit": 500,
            "reason": "Fetch the complete unfiltered state category.",
        }
    )
    second = tool.invoke(
        {
            "query_kind": "states",
            "operation": "entities",
            "path": "Root.Work.B",
            "exact": True,
            "limit": 10,
            "reason": "Do not re-query a category already returned in full.",
        }
    )

    assert first["execution_status"] == "completed"
    assert first["truncated"] is False
    assert first["total_matches"] == len(first["matched_items"])
    assert second["execution_status"] == "invalid_arguments"
    assert "category_already_returned_untruncated" in second["limitations"]


def test_eval_assert_exposes_shared_public_topology_and_path_backend():
    environment = EvalEnvironment(model_text=MODEL, timeout_seconds=None)

    result = environment.eval_assert(
        "topology().guard_agnostic is True and path('Root.Idle', 'Root.Work.B').exists is True",
        "Use the shared public pyfcstm topology backend.",
        required_function_families=["structure"],
    )

    assert result.match_status == "matches"
    assert {item.function for item in result.function_call_trace} == {
        "topology",
        "path",
    }
    path_result = next(
        item.result for item in result.function_call_trace if item.function == "path"
    )
    assert path_result["data"]["nodes"] == [
        "Root.Idle",
        "Root.Work.A",
        "Root.Work.B",
    ]
    assert "positive_path_is_not_runtime_execution_evidence" in path_result[
        "data"
    ]["limitations"]


def test_simulate_preserves_cold_contract_and_records_initialization():
    sim = SimulationAPI(MODEL)

    observed = sim.simulate(cycles=[[], ["Root.go"], ["Root.Work.go"]])

    assert observed.requested_initialization.mode == "cold"
    assert observed.effective_initialization.mode == "cold"
    assert observed.effective_initialization.active_states == ("Root",)
    assert observed.final.is_active("Root.Work.B")


def test_simulate_supports_exact_hot_start_with_complete_variables():
    sim = SimulationAPI(MODEL)

    observed = sim.simulate(
        initial_state="Root.Work.A",
        initial_vars={"count": 4, "flag": 9},
        cycles=[["Root.Work.go"]],
    )

    assert observed.requested_initialization.mode == "hot"
    assert observed.requested_initialization.state == "Root.Work.A"
    assert observed.effective_initialization.active_states == ("Root", "Root.Work", "Root.Work.A")
    assert observed.cycles[0].variables["count"] == 5
    assert observed.final.is_active("Root.Work.B")


def test_simulate_supports_cold_partial_variable_overrides():
    sim = SimulationAPI(MODEL)

    observed = sim.simulate(
        initial_vars={"count": 4},
        cycles=[[], ["Root.go"]],
    )

    assert observed.requested_initialization.mode == "cold"
    assert observed.requested_initialization.state is None
    assert observed.requested_initialization.to_json()["data"]["variables"] == {
        "count": 4
    }
    assert observed.effective_initialization.to_json()["data"]["variables"] == {
        "count": 4,
        "flag": 0,
    }
    assert observed.final.is_active("Root.Work.A")


def test_hot_start_event_causality_is_not_replaced_by_leading_empty_cycle():
    sim = SimulationAPI(EVENT_CAUSALITY_MODEL)

    direct = sim.simulate(
        initial_state="Root.Auto.Final",
        initial_vars={},
        cycles=[["Root.Brake"]],
    )
    misleading = sim.simulate(
        initial_state="Root.Auto.Final",
        initial_vars={},
        cycles=[[], ["Root.Brake"]],
    )

    assert direct.effective_initialization.active_states == (
        "Root",
        "Root.Auto",
        "Root.Auto.Final",
    )
    assert direct.cycles[0].is_active("Root.Human")
    assert "Root.Brake" in direct.cycles[0].consumed_events
    assert direct.cycles[0].unconsumed_events == ()

    assert misleading.cycles[0].is_active("Root.Human")
    assert misleading.cycles[1].is_active("Root.Human")
    assert misleading.cycles[1].consumed_events == ()
    assert misleading.cycles[1].unconsumed_events == ("Root.Brake",)


def test_observe_trace_guides_recovery_from_unconsumed_event_causality():
    result = observe_trace.execute(
        EVENT_CAUSALITY_MODEL,
        question="Does Brake cause Auto.Final to enter Human?",
        root_node_ids=["ROOT-001"],
        cycles=[[], ["Root.Brake"]],
        reason="Expose the event-causality ordering gap.",
        initial_state="Root.Auto.Final",
        initial_vars={},
    )

    assert result["execution_status"] == "completed"
    assert result["cycles"][1]["consumed_events"] == []
    assert result["cycles"][1]["unconsumed_events"] == ["Root.Brake"]
    assert "were unconsumed" in result["recommended_action"]
    assert "Do not attribute the final state" in result["recommended_action"]
    assert "source state, consumed event, and resulting target state" in result[
        "pass_criteria"
    ]


def test_simulate_rejects_hot_start_without_complete_exact_variables():
    sim = SimulationAPI(MODEL)

    try:
        sim.simulate(initial_state="Root.Work.A", initial_vars={"count": 1}, cycles=[[]])
    except ValueError as exc:
        assert "complete exact initial_vars" in str(exc)
        assert "flag" in str(exc)
    else:
        raise AssertionError("missing hot-start variables must fail closed")

    try:
        sim.simulate(initial_state="Root.Work.A", initial_vars=None, cycles=[[]])
    except ValueError as exc:
        assert "exact initial_state with complete initial_vars" in str(exc)
    else:
        raise AssertionError("hot start without variables must fail closed")

    try:
        sim.simulate(initial_vars={"missing": 1}, cycles=[[]])
    except ValueError as exc:
        assert "only declared variables" in str(exc)
    else:
        raise AssertionError("unknown cold-start variable override must fail closed")


def test_observe_trace_accepts_cold_and_hot_initialization_records():
    cold = observe_trace.execute(
        MODEL,
        question="Cold trace remains compatible.",
        root_node_ids=["ROOT-001"],
        cycles=[[], ["Root.go"]],
        reason="Check cold initialization record.",
        initial_vars={"count": 7},
    )
    assert cold["execution_status"] == "completed"
    assert cold["requested_initialization"]["mode"] == "cold"
    assert cold["effective_initialization"]["mode"] == "cold"
    assert cold["requested_initialization"]["variables"] == {"count": 7}
    assert cold["effective_initialization"]["variables"] == {"count": 7, "flag": 0}

    hot = observe_trace.execute(
        MODEL,
        question="Hot trace starts exactly at Work.A.",
        root_node_ids=["ROOT-001"],
        cycles=[["Root.Work.go"]],
        reason="Check hot initialization record.",
        initial_state="Root.Work.A",
        initial_vars={"count": 2, "flag": 0},
    )
    assert hot["execution_status"] == "completed"
    assert hot["requested_initialization"]["state"] == "Root.Work.A"
    assert hot["effective_initialization"]["variables"] == {"count": 2, "flag": 0}
    assert hot["final"]["variables"]["count"] == 3


def test_observe_trace_invalid_hot_start_is_recoverable_inconclusive_evidence():
    result = observe_trace.execute(
        MODEL,
        question="Partial hot start must fail closed.",
        root_node_ids=["ROOT-001"],
        cycles=[["Root.Work.go"]],
        reason="Verify invalid hot-start failure semantics.",
        initial_state="Root.Work.A",
        initial_vars={"count": 1},
    )

    assert result["execution_status"] == "invalid_arguments"
    assert result["evidence_status"] == "inconclusive"
    assert result["error"]["status"] == "recoverable"
    assert "complete exact initial_vars" in result["error"]["message"]
    assert "inconclusive_evidence" in result["limitations"]
    assert "no_root_verdict" in result["limitations"]
    assert "root_verdict" not in result
    assert "Root verdict" in result["recommended_action"]


def test_observe_trace_tool_invalid_runtime_failure_does_not_consume_budget_or_verdict():
    snapshot = {
        "model": {"content": MODEL},
        "current_records": {"coverage_requirements": [{"clause_id": "001"}]},
    }
    tool = observe_trace.build_tool(
        snapshot, max_calls_per_root=1, registered_root_ids=lambda: {"ROOT-001"}
    )

    bad = tool.func(
        question="Unknown hot-start state should not become a verdict.",
        root_node_ids=["ROOT-001"],
        cycles=[["Root.Work.go"]],
        reason="Verify runtime setup failure semantics.",
        initial_state="Root.Work.Missing",
        initial_vars={"count": 1, "flag": 0},
    )
    assert bad["execution_status"] in {"invalid_arguments", "execution_error"}
    assert bad["evidence_status"] == "inconclusive"
    assert bad["error"]["status"] == "recoverable"
    assert "no_root_verdict" in bad["limitations"]
    assert "root_verdict" not in bad

    good = tool.func(
        question="Valid hot start still has budget after failed runtime setup.",
        root_node_ids=["ROOT-001"],
        cycles=[["Root.Work.go"]],
        reason="Verify recoverable failures do not consume observe budget.",
        initial_state="Root.Work.A",
        initial_vars={"count": 1, "flag": 0},
    )
    assert good["execution_status"] == "completed"
    assert good["final"]["variables"]["count"] == 2
