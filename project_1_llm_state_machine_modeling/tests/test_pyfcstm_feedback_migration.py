from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from eval.extract.pyfcstm import extract_pyfcstm
from method.agents.scenariogen.generate import _extract_model_elements
from method.feedback.parse import check_parse
from method.feedback.semantic import check_semantic
from paper_v1.selection.ref_stms.verify_pyfcstm_static import analyze


SIMPLE_OK_DSL = """
def int x = 2;
state Root {
    state A;
    state B;
    state C;
    [*] -> A;
    A -> B : if [x > 0] effect { x = x - 1; };
    B -> C :: Go;
    C -> [*];
}
"""

SEM_BAD_DSL = """
def int x = 0;
state Root {
    state A;
    state B;
    [*] -> A;
    A -> B : if [unknown > 0] effect { x = another + 1; };
}
"""

HIER_ACTION_DSL = """
def int x = 0;
state Root {
    state Outer {
        >> during after abstract CheckSafety;
        state Idle {
            enter { x = 1; }
        }
        state Active;
        [*] -> Idle;
        Idle -> Active : if [x > 0] effect { x = x - 1; };
        Active -> [*];
    }
    state Done;
    [*] -> Outer;
    Outer -> Done :: Finish;
    Done -> [*];
}
"""

FORCED_DECL_DSL = """
def int fault = 0;
def int x = 0;
state Root {
    state Outer {
        state A;
        state B;
        [*] -> A;
        A -> B :: Tick effect { x = x + 1; };
    }
    state Safe;
    [*] -> Outer;
    ! * -> Safe : if [fault == 1];
}
"""


REQUIRED_INSPECT_KEYS = {
    "root_state_path",
    "states",
    "transitions",
    "variables",
    "events",
    "actions",
    "forced_transitions",
    "metrics",
    "reachability_graph",
    "event_emission_map",
    "var_dataflow",
    "aspect_impact_map",
    "action_ref_graph",
    "diagnostics",
}


def test_parse_feedback_uses_structured_grammar_errors() -> None:
    fb = check_parse("def int x = 0\nstate Root { state A; }")

    assert not fb.ok
    assert fb.error_class == "GrammarParseError"
    assert fb.line == 2
    assert fb.col == 0
    assert fb.got == "state"
    assert "^" in (fb.snippet or "")
    assert fb.diagnostics
    assert fb.diagnostics[0]["code"] == "SyntaxFailError"
    assert fb.diagnostics[0]["line"] == 2


def test_semantic_feedback_dispatches_on_model_diagnostic_codes() -> None:
    fb = check_semantic(SEM_BAD_DSL)

    assert not fb.ok
    assert fb.error_class == "ModelValidationError"
    assert fb.undefined_vars == ["unknown", "another"]
    codes = [d["code"] for d in fb.diagnostics]
    assert codes == ["E_UNDEFINED_VAR", "E_UNDEFINED_VAR"]
    assert all("refs" in d for d in fb.diagnostics)
    assert {d["refs"]["referenced_in"] for d in fb.diagnostics} == {"guard", "effect"}


def test_semantic_feedback_collects_dangling_transition_refs() -> None:
    fb = check_semantic("state Root { state A; [*] -> A; A -> Missing; }")

    assert not fb.ok
    assert fb.dangling_transitions == [
        {
            "src": "A",
            "tgt": "Missing",
            "reason": "tgt_not_found",
            "span": {"line": 1, "column": 33, "end_line": 1, "end_column": 46},
            "message": "Unknown to state 'Missing' of transition:\nA -> Missing;",
        }
    ]
    assert fb.unresolved_event_refs == []


def test_semantic_feedback_routes_event_path_missing_out_of_dangling_transitions() -> None:
    fb = check_semantic("state Root { state A; state B; [*] -> A; A -> B : /NoSuch.GhostEvt; }")

    assert not fb.ok
    assert fb.missing_states == []
    assert fb.dangling_transitions == []
    assert fb.unresolved_event_refs == [
        {
            "code": "E_MISSING_STATE",
            "event_ref": None,
            "state_path": "Root.NoSuch",
            "referenced_from": "Root",
            "reason": "event_path_not_found",
            "span": {"line": 1, "column": 42, "end_line": 1, "end_column": 68},
            "message": "Cannot find state Root.NoSuch for transition:\nA -> B : /NoSuch.GhostEvt;",
            "refs": {
                "state_path": "Root.NoSuch",
                "referenced_from": "Root",
                "reason": "event_path_not_found",
            },
        }
    ]
    assert fb.diagnostics[0]["code"] == "E_MISSING_STATE"


def test_semantic_feedback_keeps_unhandled_error_codes_in_other_errors() -> None:
    fb = check_semantic("def int x = 0; def int x = 1; state Root { state A; [*] -> A; }")

    assert not fb.ok
    assert fb.other_errors
    assert fb.other_errors[0]["code"] == "E_DUPLICATE_VAR"
    assert fb.other_errors[0]["refs"]["var_name"] == "x"
    assert fb.other_errors[0]["refs"]["previous_span"] == {
        "line": 1,
        "column": 1,
        "end_line": 1,
        "end_column": 15,
    }


def test_inspect_model_to_json_schema_contract_for_downstream_extractors() -> None:
    from pyfcstm.dsl import parse_with_grammar_entry
    from pyfcstm.model import parse_dsl_node_to_state_machine
    from pyfcstm.diagnostics import inspect_model

    ast = parse_with_grammar_entry(HIER_ACTION_DSL, "state_machine_dsl")
    model = parse_dsl_node_to_state_machine(ast)
    data = inspect_model(model).to_json()

    assert REQUIRED_INSPECT_KEYS.issubset(data.keys())
    assert {"path", "name", "parent_path", "substates", "entry_actions", "during_actions", "exit_actions"}.issubset(data["states"][0])
    assert {"from_path", "to_path", "event", "event_scope", "guard", "effect", "is_forced", "forced_origin"}.issubset(data["transitions"][0])
    assert {"name", "type", "init_value", "read_in_guards", "written_in_effects"}.issubset(data["variables"][0])
    assert {"qualified_name", "scope", "used_by", "is_declared", "is_used"}.issubset(data["events"][0])
    assert {"signature", "state_path", "name", "stage", "aspect", "is_ref", "ref_target"}.issubset(data["actions"][0])


def test_extract_pyfcstm_uses_inspect_model_contract_without_lifecycle_eval_actions() -> None:
    components = extract_pyfcstm(HIER_ACTION_DSL)
    counts = components.counts()

    assert counts["states"] == 5
    assert counts["hierarchical_states"] == 2
    assert counts["transitions"] == 6
    assert counts["guards"] == 1
    assert counts["actions"] == 1  # eval protocol: only transition effect, no lifecycle actions
    assert any(t["from_path"] == "Root.Outer.Idle" and t["to_path"] == "Root.Outer.Active" for t in components.transitions)
    assert {s["name"]: s["parent"] for s in components.states}["Idle"] == "Outer"
    assert next(h for h in components.hierarchical_states if h["name"] == "Root")["children"] == ["Outer", "Done"]
    assert components.actions == [
        {
            "id": "a0",
            "transition_id": "t4",
            "kind": "transition_effect",
            "code": "x = x - 1;",
            "text": "Root.Outer.Idle -> Root.Outer.Active : if [x > 0] effect { x = x - 1; }",
        }
    ]
    assert all("transition_id" in a and a.get("kind") == "transition_effect" for a in components.actions)


def test_extract_pyfcstm_counts_forced_transitions_at_declaration_level() -> None:
    components = extract_pyfcstm(FORCED_DECL_DSL)

    assert components.counts()["transitions"] == 4
    forced = [t for t in components.transitions if t["is_forced"]]
    assert len(forced) == 1
    assert forced[0]["src"] == "*"
    assert forced[0]["tgt"] == "Safe"
    assert forced[0]["guard"] == "fault == 1"
    assert forced[0]["expansion_count"] == 2
    assert forced[0]["forced_origin"] == "! * -> Safe : if [fault == 1];"
    assert components.counts()["guards"] == 1
    assert components.guards[0]["transition_id"] == forced[0]["id"]
    assert components.counts()["actions"] == 1
    assert components.actions[0]["kind"] == "transition_effect"
    assert components.actions[0]["transition_id"] != forced[0]["id"]


def test_extract_pyfcstm_renders_event_scope_without_changing_machine_fields() -> None:
    src = """
state Root {
    state A;
    state B;
    [*] -> A;
    A -> B :: Tick;
    B -> A : Tick;
    A -> [*] : /Reset;
}
"""
    components = extract_pyfcstm(src)

    event_rows = [t for t in components.transitions if t["event"]]
    assert [(t["event"], t["event_scope"], t["event_path"]) for t in event_rows] == [
        ("Tick", "local", "Root.A.Tick"),
        ("Tick", "chain", "Root.Tick"),
        ("Reset", "absolute", "Root.Reset"),
    ]
    assert [t["text"] for t in event_rows] == [
        "Root.A -> Root.B :: Tick",
        "Root.B -> Root.A : Tick",
        "Root.A -> [*] : /Reset",
    ]


def test_scenariogen_elements_use_inspect_model_contract() -> None:
    elements = _extract_model_elements(SIMPLE_OK_DSL)

    assert elements["root"] == "Root"
    assert "Root.A" in elements["states"]
    assert "Root.B.Go" in elements["events"]
    assert elements["variables"][0]["name"] == "x"
    assert any(t["guard"] == "x > 0" and t["effect"] == "x = x - 1;" for t in elements["transitions"])
    assert elements["metrics"]["n_variables"] == 1


def test_static_verifier_suppresses_legacy_external_guard_vars() -> None:
    external_src = """
def int ext1 = 0; // @external [E1]
def int ext2 = 0; // @input
state Root {
    state A;
    state B;
    [*] -> A;
    A -> B : if [ext1 > 0 && ext2 > 0];
    B -> [*];
}
"""
    codes = [code for _sev, code, _msg in analyze(external_src)]
    assert "W_UNWRITTEN_READ_VAR" not in codes
    assert "W_GUARD_VARS_NEVER_CHANGE" not in codes

    mixed_src = external_src.replace("def int ext2 = 0; // @input", "def int ext2 = 0;")
    mixed_codes = [code for _sev, code, _msg in analyze(mixed_src)]
    assert "W_UNWRITTEN_READ_VAR" in mixed_codes
    assert "W_GUARD_VARS_NEVER_CHANGE" in mixed_codes


def test_locally_available_core_dataset_artifacts_remain_readable() -> None:
    """Smoke whichever core/path artifacts are available in this checkout."""
    candidates = [
        Path("project_1_llm_state_machine_modeling/eval/data/sources_path1.parquet"),
        Path("project_1_llm_state_machine_modeling/eval/data/sources_path2.parquet"),
        Path("project_1_llm_state_machine_modeling/reproduction/data/derived/structure_event_driven_cases.parquet"),
        Path("project_1_llm_state_machine_modeling/reproduction/data/derived/structure_event_driven_reference_solutions.parquet"),
    ]
    present = [p for p in candidates if p.exists()]
    assert present, "expected at least one path1/path2/core dataset artifact"

    for path in present:
        df = pd.read_parquet(path)
        assert len(df) > 0, path
        if "case_id" in df.columns:
            assert df["case_id"].notna().all(), path
        if path.name in {"sources_path1.parquet", "sources_path2.parquet"}:
            assert {"case_id", "nl_text"}.issubset(df.columns), path
            assert df["nl_text"].str.len().gt(20).all(), path


def test_existing_eval_demo_json_fixtures_are_unchanged() -> None:
    """Guard downstream manual-eval fixtures used as a tiny path smoke test."""
    root = Path("project_1_llm_state_machine_modeling/eval/data")
    for rel in [
        "refs/abs-fsm-brake-control/ref_components.json",
        "refs/automatic-elevator-controller/ref_components.json",
        "preds/abs-fsm-brake-control/pred_perfect.json",
        "preds/automatic-elevator-controller/pred_perfect.json",
    ]:
        data = json.loads((root / rel).read_text(encoding="utf-8"))
        assert len(data["states"]) >= 3
        assert len(data["transitions"]) >= 4
