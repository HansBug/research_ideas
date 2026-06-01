"""Smoke exported Path 1 / Path 2 artifacts against pyfcstm migration.

CI exports representative artifacts from ``dev/path1-hard-comparison`` and
``dev/path2-differentiation`` into ``/tmp/pr13_artifacts`` before running this
script. The smoke intentionally exercises the same public functions used by
Path 1/2 downstream code: parse feedback, semantic feedback, eval component
extraction, scenariogen element extraction, and static verifier analysis.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "project_1_llm_state_machine_modeling"))

from eval.extract.pyfcstm import extract_pyfcstm
from method.agents.scenariogen.generate import _extract_model_elements
from method.feedback.parse import check_parse
from method.feedback.semantic import check_semantic
from paper_v1.selection.ref_stms.verify_pyfcstm_static import analyze

ARTIFACT_ROOT = Path("/tmp/pr13_artifacts")
EXPECTED = {
    "path1": {
        "parquet": ARTIFACT_ROOT / "path1" / "sources_path1.parquet",
        "fcstm": ["cara.fcstm", "cubesat.fcstm"],
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


def smoke_fcstm(path: Path) -> None:
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
    elements = _extract_model_elements(src)
    assert elements["states"] and elements["transitions"], f"empty scenariogen elements for {path}"
    static_diags = analyze(src)
    assert all(len(item) == 3 for item in static_diags), f"bad static diag tuple for {path}: {static_diags}"


def main() -> None:
    for path_name, spec in EXPECTED.items():
        smoke_parquet(spec["parquet"])
        for filename in spec["fcstm"]:
            smoke_fcstm(ARTIFACT_ROOT / path_name / filename)
    print("path1/path2 pyfcstm feedback smoke passed")


if __name__ == "__main__":
    main()
