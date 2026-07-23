from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


HELPER_PATH = Path(__file__).parent / "helpers" / "probe_discover_fbmcq.py"


def _load_helper():
    spec = importlib.util.spec_from_file_location("probe_discover_fbmcq", HELPER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_pairs(path: Path, pair_ids: list[str]) -> None:
    path.write_text(
        "".join(
            json.dumps({"pair_id": pair_id, "nl_text": f"Requirement {pair_id}"})
            + "\n"
            for pair_id in pair_ids
        ),
        encoding="utf-8",
    )


def _write_fcstm_dir(path: Path, stems: list[str]) -> None:
    path.mkdir(parents=True)
    for stem in stems:
        (path / f"{stem}.fcstm").write_text(
            "state Root {\n    state Idle;\n    [*] -> Idle;\n}\n",
            encoding="utf-8",
        )


def _write_report_manifest(fcstm_dir: Path) -> None:
    (fcstm_dir.parent / "manifest.json").write_text(
        json.dumps(
            {
                "research_commit": "abc123",
                "pairs_sha256": "pairs-sha",
                "artifact_set_sha256": "artifacts-sha",
                "implementation_tree_sha256": "impl-sha",
            }
        ),
        encoding="utf-8",
    )


def test_formal_probe_preflights_exact_60_assets_and_writes_report_provenance(
    tmp_path: Path, monkeypatch
):
    helper = _load_helper()
    pair_ids = [f"case_{idx:04d}" for idx in range(60)]
    pairs = tmp_path / "pairs.jsonl"
    report_dir = tmp_path / "report"
    fcstm_dir = report_dir / "fcstm"
    output = tmp_path / "probe.jsonl"
    _write_pairs(pairs, pair_ids)
    _write_fcstm_dir(fcstm_dir, pair_ids)
    _write_report_manifest(fcstm_dir)

    def fake_row(
        pair_id: str,
        fcstm_file: Path,
        bound: int,
        wall_seconds: float | None,
        input_provenance: dict[str, Any],
        probe_contract: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "pair_id": pair_id,
            "fcstm_path": str(fcstm_file),
            "bound": bound,
            "process_wall_seconds": wall_seconds,
            "input_provenance": input_provenance,
            "probe_contract": probe_contract,
            "status": "completed",
        }

    monkeypatch.setattr(helper, "_row", fake_row)

    rc = helper.main(
        [
            "--pairs",
            str(pairs),
            "--fcstm-dir",
            str(fcstm_dir),
            "--bounds",
            "7",
            "--output",
            str(output),
        ]
    )

    assert rc == 0
    rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 60
    assert {row["pair_id"] for row in rows} == set(pair_ids)
    assert rows[0]["input_provenance"] == {
        "report_manifest_path": str(report_dir / "manifest.json"),
        "research_commit": "abc123",
        "pairs_sha256": "pairs-sha",
        "artifact_set_sha256": "artifacts-sha",
        "implementation_tree_sha256": "impl-sha",
    }
    assert rows[0]["probe_contract"] == {
        "issue": "165",
        "formal_case_count": 60,
        "case_count_mode": "formal_60_case",
        "limit": None,
        "smoke_only": False,
    }


def test_formal_probe_fails_with_clear_preflight_reason_on_count_or_stem_mismatch(
    tmp_path: Path, capsys
):
    helper = _load_helper()
    pairs = tmp_path / "pairs.jsonl"
    fcstm_dir = tmp_path / "report" / "fcstm"
    output = tmp_path / "probe.jsonl"
    pair_ids = [f"case_{idx:04d}" for idx in range(60)]
    stems = pair_ids[:-1] + ["unexpected_extra_case"]
    _write_pairs(pairs, pair_ids)
    _write_fcstm_dir(fcstm_dir, stems)
    _write_report_manifest(fcstm_dir)

    rc = helper.main(
        [
            "--pairs",
            str(pairs),
            "--fcstm-dir",
            str(fcstm_dir),
            "--output",
            str(output),
        ]
    )

    captured = capsys.readouterr()
    assert rc == 2
    assert not output.exists()
    failure = json.loads(captured.err)
    assert failure["status"] == "input_asset_preflight_failed"
    assert failure["failure_reason"] == "input_asset_preflight_failed"
    assert any("pair_fcstm_id_mismatch" in reason for reason in failure["reasons"])
    assert any("case_0059" in reason for reason in failure["reasons"])
    assert any("unexpected_extra_case" in reason for reason in failure["reasons"])


def test_limit_is_explicit_smoke_and_does_not_require_60_cases(tmp_path: Path, monkeypatch):
    helper = _load_helper()
    pairs = tmp_path / "pairs.jsonl"
    fcstm_dir = tmp_path / "report" / "fcstm"
    output = tmp_path / "probe.jsonl"
    pair_ids = ["case_0000", "case_0001", "case_0002"]
    _write_pairs(pairs, pair_ids)
    _write_fcstm_dir(fcstm_dir, ["case_0000"])
    _write_report_manifest(fcstm_dir)

    def fake_row(
        pair_id: str,
        fcstm_file: Path,
        bound: int,
        wall_seconds: float | None,
        input_provenance: dict[str, Any],
        probe_contract: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "pair_id": pair_id,
            "fcstm_path": str(fcstm_file),
            "bound": bound,
            "process_wall_seconds": wall_seconds,
            "input_provenance": input_provenance,
            "probe_contract": probe_contract,
            "status": "completed",
        }

    monkeypatch.setattr(helper, "_row", fake_row)

    rc = helper.main(
        [
            "--pairs",
            str(pairs),
            "--fcstm-dir",
            str(fcstm_dir),
            "--limit",
            "1",
            "--bounds",
            "3",
            "--output",
            str(output),
        ]
    )

    assert rc == 0
    rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    assert rows[0]["pair_id"] == "case_0000"
    assert rows[0]["probe_contract"]["case_count_mode"] == "opt_in_smoke_limit"
    assert rows[0]["probe_contract"]["limit"] == 1
    assert rows[0]["probe_contract"]["smoke_only"] is True
