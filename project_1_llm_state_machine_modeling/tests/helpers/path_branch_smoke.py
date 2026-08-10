"""Smoke exported Path 1 / Path 2 artifacts against pyfcstm migration.

CI exports representative artifacts into ``/tmp/pr13_artifacts`` before
running this script. The exported snapshots are fixed to the PR #9 / PR #10
core dataset commits used for PR #13 regression: Path 1
``b4ad12205bccf686a61671d1bdc7c28b1a22bab3`` and Path 2
``bdb25d93408f0a86f8dde8238e67c1f2bfdbbb59``. The smoke intentionally
exercises the same public functions used by Path 1/2 downstream code: parse
feedback, semantic feedback, eval component extraction, scenariogen element
extraction, and static verifier analysis.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "project_1_llm_state_machine_modeling"))

from archive.path1_evaluation.extract.pyfcstm import extract_pyfcstm
from archive.agent_loop_method.agents.scenariogen.generate import _extract_model_elements
from archive.agent_loop_method.feedback.parse import check_parse
from archive.agent_loop_method.feedback.semantic import check_semantic
from archive.path1_path2_guides.selection.ref_stms.verify_pyfcstm_static import analyze

ARTIFACT_ROOT = Path("/tmp/pr13_artifacts")
EXPECTED = {
    "path1": {
        "parquet": ARTIFACT_ROOT / "path1" / "sources_path1.parquet",
        "fcstm": ["cara.fcstm", "cubesat.fcstm"],
        "signed_refs": {
            "cara.fcstm": ARTIFACT_ROOT / "path1" / "cara_ref_components.json",
            "cubesat.fcstm": ARTIFACT_ROOT / "path1" / "cubesat_ref_components.json",
        },
    },
    "path2": {
        "parquet": ARTIFACT_ROOT / "path2" / "sources_path2.parquet",
        "fcstm": ["008.fcstm", "097.fcstm", "118.fcstm"],
    },
}


def smoke_parquet(path: Path) -> None:
    assert path.exists(), f"missing parquet artifact: {path}"
    df = pd.read_parquet(path)
    assert len(df) > 0, f"empty parquet artifact: {path}"
    assert "case_id" in df.columns, f"missing case_id in {path}: {df.columns.tolist()}"
    text_cols = [c for c in ("nl_text", "requirement", "requirements", "text") if c in df.columns]
    assert text_cols, f"missing NL text column in {path}: {df.columns.tolist()}"
    assert df[text_cols[0]].astype(str).str.len().gt(20).all(), f"short NL text in {path}"


def _component_counts(obj) -> dict[str, int]:
    if hasattr(obj, "counts"):
        return obj.counts()
    return {
        key: len(obj.get(key, []))
        for key in ["states", "transitions", "guards", "actions", "hierarchical_states"]
    }


def _normal_state(row: dict) -> dict:
    return {key: row.get(key, "") for key in ["id", "name", "parent", "text"]}


def _normal_transition(row: dict) -> dict:
    return {
        key: row.get(key, "")
        for key in ["src", "tgt", "event", "guard", "action", "is_forced", "text"]
    }


def _normal_guard(row: dict) -> dict:
    return {key: row.get(key, "") for key in ["transition_id", "expr", "text"]}


def _normal_action(row: dict) -> dict:
    return {
        "transition_id": row.get("transition_id", ""),
        "expr": row.get("expr", row.get("code", "")),
        "text": row.get("text", ""),
    }


def _normal_hierarchical(row: dict) -> dict:
    return {
        "name": row.get("name", ""),
        "children": row.get("children", []),
        "text": row.get("text", ""),
    }


def _assert_signed_ref_rowwise_compatible(path: Path, components, signed: dict) -> None:
    """Guard signed Path 1 IR compatibility beyond component counts.

    The public fields below are used by review packs and row-key style audit
    tooling.  Auxiliary fields such as ``*_path`` / ``scoped_text`` may differ
    or be newly added, but these signed fields must stay row-wise stable.
    """
    assert [_normal_state(s) for s in components.states] == [
        _normal_state(s) for s in signed.get("states", [])
    ], f"Path 1 signed state row drift for {path}"
    assert [_normal_transition(t) for t in components.transitions] == [
        _normal_transition(t) for t in signed.get("transitions", [])
    ], f"Path 1 signed transition row drift for {path}"
    assert [_normal_guard(g) for g in components.guards] == [
        _normal_guard(g) for g in signed.get("guards", [])
    ], f"Path 1 signed guard row drift for {path}"
    assert [_normal_action(a) for a in components.actions] == [
        _normal_action(a) for a in signed.get("actions", [])
    ], f"Path 1 signed action row drift for {path}"
    assert [_normal_hierarchical(h) for h in components.hierarchical_states] == [
        _normal_hierarchical(h) for h in signed.get("hierarchical_states", [])
    ], f"Path 1 signed hierarchical-state row drift for {path}"


def smoke_fcstm(path: Path, signed_ref_path: Path | None = None) -> None:
    assert path.exists(), f"missing fcstm artifact: {path}"
    src = path.read_text(encoding="utf-8")
    pf = check_parse(src)
    assert pf.ok, f"parse failed for {path}: {pf}"
    sf = check_semantic(src)
    assert sf.ok, f"semantic failed for {path}: {sf}"
    components = extract_pyfcstm(src)
    assert components.states, f"no states extracted for {path}"
    assert components.transitions, f"no transitions extracted for {path}"
    assert all("transition_id" in a and a.get("kind") == "transition_effect" for a in components.actions), (
        f"eval actions must remain transition effects only for {path}: {components.actions}"
    )
    if signed_ref_path is not None:
        assert signed_ref_path.exists(), f"missing signed Path 1 ref_components artifact: {signed_ref_path}"
        signed = json.loads(signed_ref_path.read_text(encoding="utf-8"))
        assert components.counts() == _component_counts(signed), (
            f"Path 1 signed component counts drift for {path}: "
            f"got {components.counts()} vs signed {_component_counts(signed)}"
        )
        _assert_signed_ref_rowwise_compatible(path, components, signed)
        signed_forced = sum(1 for t in signed.get("transitions", []) if t.get("is_forced"))
        got_forced = sum(1 for t in components.transitions if t.get("is_forced"))
        assert got_forced == signed_forced, (
            f"forced transition declaration count drift for {path}: got {got_forced}, signed {signed_forced}"
        )
    elements = _extract_model_elements(src)
    assert elements["states"] and elements["transitions"], f"empty scenariogen elements for {path}"
    scen_forced = [t for t in elements["transitions"] if t.get("is_forced")]
    eval_forced = [t for t in components.transitions if t.get("is_forced")]
    assert len(scen_forced) == len(eval_forced), (
        f"scenariogen forced transition count must use declaration-level view for {path}: "
        f"got {len(scen_forced)} vs eval {len(eval_forced)}"
    )
    static_diags = analyze(src)
    assert all(len(item) == 3 for item in static_diags), f"bad static diag tuple for {path}: {static_diags}"
    if signed_ref_path is not None:
        assert not [item for item in static_diags if item[0] == "error"], f"static verifier error for {path}: {static_diags}"


def main() -> None:
    for path_name, spec in EXPECTED.items():
        smoke_parquet(spec["parquet"])
        signed_refs = spec.get("signed_refs", {})
        for filename in spec["fcstm"]:
            smoke_fcstm(ARTIFACT_ROOT / path_name / filename, signed_refs.get(filename))
    print("path1/path2 pyfcstm feedback smoke passed")


if __name__ == "__main__":
    main()
