from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from eval.extract.pyfcstm import extract_pyfcstm
from method.agents.scenariogen.generate import _extract_model_elements
from method.feedback.parse import check_parse
from method.feedback.semantic import check_semantic


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



def test_semantic_feedback_maps_missing_state_diagnostics() -> None:
    fb = check_semantic("state Root { state A; state B; [*] -> A; A -> B : /NoSuch.GhostEvt; }")

    assert not fb.ok
    assert fb.missing_states == ["Root.NoSuch"]
    assert fb.dangling_transitions[0]["tgt"] == "Root.NoSuch"
    assert fb.dangling_transitions[0]["reason"] == "event_path_not_found"
    assert fb.diagnostics[0]["code"] == "E_MISSING_STATE"

def test_extract_pyfcstm_uses_inspect_model_contract() -> None:
    components = extract_pyfcstm(HIER_ACTION_DSL)
    counts = components.counts()

    assert counts["states"] == 5
    assert counts["hierarchical_states"] == 2
    assert counts["transitions"] == 6
    assert counts["guards"] == 1
    assert counts["actions"] >= 3  # transition effect + enter inline + aspect abstract
    assert any(t["from_path"] == "Root.Outer.Idle" and t["to_path"] == "Root.Outer.Active" for t in components.transitions)
    assert any(a.get("kind") == "transition_effect" and a.get("code") == "x = x - 1;" for a in components.actions)
    assert any(a.get("state") == "Root.Outer.Idle" and a.get("kind") == "enter" for a in components.actions)


def test_scenariogen_elements_use_inspect_model_contract() -> None:
    elements = _extract_model_elements(SIMPLE_OK_DSL)

    assert elements["root"] == "Root"
    assert "Root.A" in elements["states"]
    assert "Root.B.Go" in elements["events"]
    assert elements["variables"][0]["name"] == "x"
    assert any(t["guard"] == "x > 0" and t["effect"] == "x = x - 1;" for t in elements["transitions"])
    assert elements["metrics"]["n_variables"] == 1


def test_path1_and_path2_core_datasets_remain_readable() -> None:
    """Smoke the core datasets named by PR #9/#10 when present locally."""
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
