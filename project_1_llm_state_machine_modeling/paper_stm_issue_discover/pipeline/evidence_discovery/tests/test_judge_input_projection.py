from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.evidence_discovery.reporting.judge_input_projection import (
    JudgeInputProjectionAudit,
    JudgeInputProjectionCellAudit,
    ProjectedMethodRelease,
    build_judge_input_projection,
    main,
)
from pipeline.semantic_judge.artifacts import adapt_evidence_discovery_release


def _write_cell(
    root: Path,
    *,
    pair_id: str,
    round_no: int,
    status: str,
    eligible: bool,
    report_count: int,
) -> Path:
    path = root / "method" / pair_id / f"round-{round_no}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    reports = [
        {
            "issue_id": f"{pair_id}:r{round_no}:issue:{index}",
            "title": f"claim {index}",
            "locus_kind": "state",
            "locus_names": [f"State{index}"],
            "candidate_reason": f"reason {index}",
            "candidate_basis": f"basis {index}",
            "source_refs": [f"state:State{index}:line:1"],
        }
        for index in range(report_count)
    ]
    path.write_text(
        json.dumps(
            {
                "schema": "evidence-discovery.method_cell.v8",
                "status": status,
                "eligible": eligible,
                "pair_id": pair_id,
                "round": round_no,
                "report_issue_clusters": reports,
                "reason": "fixture reason",
                "basis": "fixture basis",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def test_projection_preserves_eligible_reports_and_empties_ineligible_surface(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    completed = _write_cell(
        source,
        pair_id="0001",
        round_no=1,
        status="completed",
        eligible=True,
        report_count=1,
    )
    diagnostic = _write_cell(
        source,
        pair_id="0002",
        round_no=1,
        status="completed_with_diagnostics",
        eligible=True,
        report_count=2,
    )
    failed = _write_cell(
        source,
        pair_id="0003",
        round_no=1,
        status="failed_with_receipt",
        eligible=False,
        report_count=3,
    )
    source_hashes = {path: path.read_bytes() for path in (completed, diagnostic, failed)}

    projection = tmp_path / "projection"
    audit = build_judge_input_projection(
        source,
        projection,
        projection_code_commit="a" * 40,
        expected_pair_ids=("0001", "0002", "0003"),
        expected_rounds=(1,),
    )

    assert audit.cell_count == 3
    assert audit.unchanged_hardlink_count == 1
    assert audit.eligible_diagnostic_projection_count == 1
    assert audit.empty_publication_projection_count == 1
    projected_completed = projection / "method/0001/round-1.json"
    assert completed.stat().st_ino == projected_completed.stat().st_ino
    assert projected_completed.read_bytes() == completed.read_bytes()

    diagnostic_record = json.loads(
        (projection / "method/0002/round-1.json").read_text(encoding="utf-8")
    )
    failed_record = json.loads(
        (projection / "method/0003/round-1.json").read_text(encoding="utf-8")
    )
    assert diagnostic_record["status"] == "completed"
    assert diagnostic_record["eligible"] is True
    assert diagnostic_record["report_issue_clusters"] == json.loads(
        diagnostic.read_text(encoding="utf-8")
    )["report_issue_clusters"]
    assert failed_record["status"] == "completed"
    assert failed_record["eligible"] is True
    assert failed_record["report_issue_clusters"] == []

    diagnostic_reports, _, _, _ = adapt_evidence_discovery_release(
        projection / "method/0002/round-1.json", ()
    )
    failed_reports, _, _, _ = adapt_evidence_discovery_release(
        projection / "method/0003/round-1.json", ()
    )
    assert len(diagnostic_reports) == 2
    assert failed_reports == ()
    assert all(path.read_bytes() == payload for path, payload in source_hashes.items())
    assert audit.cells[2].report_semantics_preserved is False
    assert audit.cells[2].original_report_count == 3
    assert audit.cells[2].projected_report_count == 0


def test_projection_rejects_unrecognized_terminal_contract(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _write_cell(
        source,
        pair_id="0001",
        round_no=1,
        status="completed_with_diagnostics",
        eligible=False,
        report_count=1,
    )
    with pytest.raises(ValueError, match="unsupported method terminal contract"):
        build_judge_input_projection(
            source,
            tmp_path / "projection",
            projection_code_commit="a" * 40,
        )


def test_projection_models_have_documented_fields() -> None:
    for model in (
        ProjectedMethodRelease,
        JudgeInputProjectionCellAudit,
        JudgeInputProjectionAudit,
    ):
        assert model.__doc__
        assert all(field.description for field in model.model_fields.values())


def test_cli_defaults_require_frozen_54_by_3_closure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source"
    _write_cell(
        source,
        pair_id="0001",
        round_no=1,
        status="completed",
        eligible=True,
        report_count=0,
    )
    monkeypatch.setattr(
        "pipeline.evidence_discovery.reporting.judge_input_projection._require_clean_commit",
        lambda _path: "a" * 40,
    )
    with pytest.raises(ValueError, match="method release closure mismatch"):
        main(
            (
                "--source-root",
                str(source),
                "--projection-root",
                str(tmp_path / "projection"),
            )
        )
