from __future__ import annotations

import inspect

from paper_stm_repair_loop.records import sha256_json
from paper_stm_repair_loop.tools.guide_access import GuideAccessState, guard_tool
from paper_stm_repair_loop.tools.inspect_model import build_tool, execute
from paper_stm_repair_loop.tools.read_task import build_tool as build_read_task


def _check_result() -> dict:
    inspect_payload = {
        "states": [{"path": "Root", "kind": "composite"}],
        "transitions": [{"transition_index": 0, "source": "Root", "target": "Root.Idle"}],
        "diagnostics": [{"code": "W_TEST", "severity": "warning", "message": "bounded"}],
        "metrics": {"state_count": 1, "transition_count": 1},
    }
    return {
        "record_id": "REC-000004",
        "execution_status": "completed",
        "parse_status": "ok",
        "semantic_status": "ok",
        "inspect_status": "ok",
        "executable": True,
        "diagnostics": inspect_payload["diagnostics"],
        "inspect": inspect_payload,
        "metrics": inspect_payload["metrics"],
        "model_sha256": "model-hash",
        "model_type": "StateMachine",
    }


def test_inspect_model_projects_only_frozen_check_result_llm_safe_view():
    check = _check_result()

    result = execute(check, "Inspect the frozen weak lead before querying model facts.")

    assert result["execution_status"] == "completed"
    assert result["parse_status"] == "ok"
    assert result["semantic_status"] == "ok"
    assert result["inspect_status"] == "ok"
    assert result["executable"] is True
    assert result["diagnostics"] == check["diagnostics"]
    assert result["inspect"] == check["inspect"]
    assert result["metrics"] == check["metrics"]
    assert result["model"] == {
        "model_id": "STM_0",
        "model_type": "StateMachine",
        "sha256": "model-hash",
        "model_sha256": "model-hash",
        "inspect_sha256": sha256_json(check["inspect"]),
    }
    assert result["check"]["check_result_sha256"] == sha256_json(check)
    assert result["record_id"] == "REC-000004"
    assert "controller_frozen_check_result_only" in result["limitations"]
    assert result["recommended_next_evidence"]
    assert not any("inspect_model" in item and "do not call" not in item for item in result["recommended_next_evidence"])
    assert "raw_source" not in result
    assert "content" not in result["model"]


def test_inspect_model_repeated_same_fingerprint_returns_no_new_fact():
    tool = build_tool(_check_result())

    first = tool.invoke({"reason": "Inspect frozen check result once."})
    second = tool.invoke({"reason": "Do not replay the same weak lead."})

    assert first["execution_status"] == "completed"
    assert second["execution_status"] == "no_new_fact"
    assert second["parse_status"] == first["parse_status"]
    assert second["semantic_status"] == first["semantic_status"]
    assert second["inspect_status"] == first["inspect_status"]
    assert second["executable"] is first["executable"]
    assert second["check"]["check_result_sha256"] == first["check"]["check_result_sha256"]
    assert second["model"]["model_sha256"] == first["model"]["model_sha256"]
    assert second["diagnostics"] == []
    assert second["inspect"] == {}
    assert second["metrics"] == {}
    assert "stop_repeating_inspect_model" in second["limitations"]
    assert any("Stop" in item or "do not call inspect_model again" in item for item in second["recommended_next_evidence"])
    assert any("query_model" in item for item in second["recommended_next_evidence"])
    assert any("register_coverage_plan" in item for item in second["recommended_next_evidence"])
    assert any("eval_assert" in item for item in second["recommended_next_evidence"])
    assert not any("call inspect_model" in item and "do not call" not in item for item in second["recommended_next_evidence"])



def test_guarded_inspect_model_duplicate_recovery_does_not_recommend_reinspect():
    state = GuideAccessState()
    state.mark_read("fcstm", {"resource_name": "fcstm", "sha256": "guide-hash"})
    tool = guard_tool(build_tool(_check_result()), state)

    first = tool.invoke({"reason": "Inspect frozen check result once."})
    second = tool.invoke({"reason": "Do not replay the same weak lead."})

    assert first["execution_status"] == "completed"
    assert second["execution_status"] == "no_new_fact"
    assert second["executable"] is True
    action = second["required_actions"][0]
    assert action["recommended_tools"] == [
        "query_model",
        "register_coverage_plan",
        "eval_assert",
    ]
    assert "Stop repeating inspect_model" in action["recommended_action"]
    assert "call inspect_model" not in action["recommended_action"]


def test_inspect_model_tool_docstring_is_model_visible_english_contract():
    tool = build_tool(_check_result())

    assert tool.name == "inspect_model"
    assert inspect.getdoc(tool.func) == tool.description
    assert "Purpose" in tool.description
    assert "reference/gold" in tool.description
    assert "Controller-frozen" in tool.description
    assert set(tool.args_schema.model_json_schema()["properties"]) == {"reason"}
    assert tool.args_schema.model_json_schema().get("additionalProperties") is False


def test_read_task_removes_duplicate_raw_inspect_but_preserves_worklist_sourcefacts_and_hashes():
    inspect_payload = _check_result()["inspect"]
    snapshot = {
        "stage": "B-discover",
        "loop_no": 0,
        "model": {
            "model_id": "STM_0",
            "content": "state Root {}",
            "model_sha256": "model-hash",
            "normalized_inspect": inspect_payload,
        },
        "targets": [],
        "current_records": {
            "coverage_requirements": {"requirements": [{"requirement_id": "REQ-1"}]},
            "source_inventory": {
                "inventory_sha256": "inventory-hash",
                "facts": [{"fact_id": "SF-1", "payload": {"state": "Root"}}],
            },
            "diagnostics": inspect_payload["diagnostics"],
            "inspect": inspect_payload,
        },
        "readable_history": [],
    }
    tool = build_read_task(snapshot)

    result = tool.invoke({"reason": "Read frozen task without duplicate raw inspect."})

    assert "normalized_inspect" not in result["model"]
    assert result["model"]["normalized_inspect_sha256"] == sha256_json(inspect_payload)
    assert "diagnostics" not in result["current_records"]
    assert "inspect" not in result["current_records"]
    assert result["current_records"]["diagnostics_sha256"] == sha256_json(inspect_payload["diagnostics"])
    assert result["current_records"]["inspect_sha256"] == sha256_json(inspect_payload)
    assert result["current_records"]["coverage_requirements"]["requirements"][0]["requirement_id"] == "REQ-1"
    assert result["current_records"]["source_inventory"]["facts"][0]["fact_id"] == "SF-1"

    duplicate = tool.invoke({"reason": "Do not replay the frozen task."})
    assert duplicate["execution_status"] == "no_new_task_fact"
    assert duplicate["snapshot_sha256"] == sha256_json(result)
