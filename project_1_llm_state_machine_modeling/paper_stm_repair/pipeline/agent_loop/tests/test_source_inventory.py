from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "src/paper_stm_repair_loop/source_inventory.py"


def load_inventory():
    spec = importlib.util.spec_from_file_location("paper1_source_inventory_under_test", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_source_inventory_enumerates_structured_kinds_without_semantic_role():
    inventory_mod = load_inventory()
    check_result = {
        "inspect": {
            "states": [{"path": "Root.Attack", "semantic_role": "attack"}],
            "events": [{"qualified_name": "Root.Attack_Complete"}],
            "variables": [{"qualified_name": "Root.uav_count"}],
            "transitions": [
                {
                    "transition_index": 4,
                    "source": "Root.Attack",
                    "event": "Root.Attack_Complete",
                    "target": "Root.Searching",
                    "guard": "uav_count > 0",
                    "effects": ["uav_count = uav_count - 1"],
                    "semantic_role": "return_to_search",
                }
            ],
            "initial_relations": [{"source": "[*]", "target": "Root.Searching"}],
            "hierarchy": [{"parent": "Root", "child": "Root.Attack"}],
            "regions": [{"owner": "Root.Searching", "region": "main"}],
            "diagnostics": [{"code": "W_DEMO", "severity": "warning"}],
        }
    }

    inventory = inventory_mod.build_source_inventory(
        check_result,
        source_trace_base={"entries": [{"source_elements": ["source:req"], "intermediate_elements": ["transition:4"]}]},
        relation_policy="exact_identity",
        identity_refs=[{"source_ref": "Root.Attack", "fcstm_ref": "Root.Attack"}],
        producer_version="0.6.0",
    )

    kinds = {fact["fact_kind"] for fact in inventory["facts"]}
    assert {
        "state",
        "event",
        "variable",
        "transition",
        "guard",
        "effect",
        "initial_relation",
        "hierarchy",
        "region",
        "diagnostic",
        "source_fcstm_mapping",
    }.issubset(kinds)

    for fact in inventory["facts"]:
        assert "semantic_role" not in fact
        assert "semantic_role" not in fact["payload"]
        assert fact["producer"]
        assert fact["provenance"]
        assert fact["behavior_relevant"] is (
            fact["fact_kind"]
            in {
                "state",
                "event",
                "variable",
                "transition",
                "forced_transition",
                "guard",
                "effect",
                "initial_relation",
                "hierarchy",
                "region",
            }
        )


def test_source_inventory_does_not_parse_exception_text_as_facts():
    inventory_mod = load_inventory()
    inventory = inventory_mod.build_source_inventory(
        {
            "execution_status": "completed",
            "parse_status": "failed",
            "error": {
                "type": "ValueError",
                "message": "state Root.Attack transition Root.Attack -> Root.Searching",
            },
        }
    )
    assert inventory["facts"] == []
