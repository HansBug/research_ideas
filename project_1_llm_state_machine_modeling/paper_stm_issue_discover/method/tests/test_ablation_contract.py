"""Provider-free checks for the shared A1/A2 run identity."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from paper_stm_method import cli
from paper_stm_method.orchestration import contracts, runner


PAPER = Path(__file__).resolve().parents[2]
REPORT = PAPER / "pipeline/representation/reports/llms_emp_r45_java_60"


def test_cli_default_and_explicit_none(monkeypatch, tmp_path):
    calls = []

    def run(**kwargs):
        calls.append(kwargs)
        return {"artifact_root": str(tmp_path), "run_id": "0" * 32}

    monkeypatch.setattr(cli, "run_experiment", run)
    args = ["--report-root", str(REPORT), "--output-dir", str(tmp_path)]
    cli.main(args)
    cli.main([*args, "--ablation", "none"])
    assert calls[0] == calls[1]
    assert calls[0]["ablation"] == "none"


@pytest.mark.parametrize("ablation", ["unknown", "no-predicate", "no-predicates", "no-inspect"])
def test_unimplemented_modes_fail_before_loading_or_provider(ablation, monkeypatch, tmp_path):
    def forbidden(*args, **kwargs):
        pytest.fail("unimplemented condition reached input/provider setup")

    monkeypatch.setattr(runner, "_source_provenance", forbidden)
    monkeypatch.setattr(runner, "PublicStructuredRuntime", forbidden)
    with pytest.raises(ValueError, match="ablation"):
        runner.run_experiment(report_root=REPORT, output_dir=tmp_path, ablation=ablation)
    assert not list(tmp_path.iterdir())


def test_condition_identity_worker_resume_and_legacy_reading(tmp_path, monkeypatch):
    args = dict(report_root=REPORT, output_dir=tmp_path, profile="fixture", rounds=1,
                workers=2, pair_ids=["0004", "0023"], run_id="a" * 32)
    summary = runner.run_experiment(**args)
    run_root = Path(summary["artifact_root"])
    manifest = json.loads((run_root / "run_manifest.json").read_text())
    assert summary["ablation"] == manifest["ablation"] == "none"
    for pair_id in args["pair_ids"]:
        cell_path = run_root / "method" / pair_id / "round-1.json"
        cell = json.loads(cell_path.read_text())
        status = json.loads((run_root / "pairs" / pair_id / "status.json").read_text())
        assert cell["ablation"] == status["ablation"] == "none"
        assert cell["run_contract_hash"] == manifest["run_contract_hash"]
        legacy = {k: v for k, v in cell.items() if k != "ablation"}
        legacy["schema"] = "evidence-discovery.method_cell.v9"
        assert contracts.MethodCellReceipt.model_validate(legacy).ablation == "none"
        with pytest.raises(ValidationError, match="explicit ablation"):
            contracts.MethodCellReceipt.model_validate({k: v for k, v in cell.items() if k != "ablation"})
        with pytest.raises(ValidationError, match="legacy records"):
            contracts.MethodCellReceipt.model_validate({**legacy, "ablation": "no-inspect"})

    runner.run_experiment(**args, ablation="none", resume=True)
    before = (run_root / "method/0004/round-1.json").read_bytes()
    monkeypatch.setattr(contracts, "IMPLEMENTED_ABLATIONS", contracts.ABLATION_MODES)
    with pytest.raises(RuntimeError, match="resume contract mismatch"):
        runner.run_experiment(**args, ablation="no-inspect", resume=True)
    monkeypatch.setattr(runner, "_model_config_hash", lambda profile: "sha256:" + "c" * 64)
    with pytest.raises(RuntimeError, match="resume contract mismatch"):
        runner.run_experiment(**args, resume=True)
    assert (run_root / "method/0004/round-1.json").read_bytes() == before


def test_failure_receipt_keeps_disabled_condition(tmp_path):
    identity = {
        "run_id": "a" * 32, "run_contract_hash": "sha256:" + "b" * 64,
        "ablation": "no-inspect",
        "source_provenance": {"source_commit": "0" * 40, "source_branch": "fixture",
                              "source_dirty": False, "reason": "Test identity.", "basis": "fixture"},
    }
    cell = runner._failure_method_cell(pair_id="0004", round_index=1, output_root=tmp_path,
                                       error=RuntimeError("fixture"), run_identity=identity)
    assert cell["ablation"] == "no-inspect"
    assert not cell["eligible"]
