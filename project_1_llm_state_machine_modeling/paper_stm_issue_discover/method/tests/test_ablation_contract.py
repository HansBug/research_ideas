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


@pytest.mark.parametrize("ablation", ["unknown", "no-predicate"])
def test_unimplemented_modes_fail_before_loading_or_provider(ablation, monkeypatch, tmp_path):
    def forbidden(*args, **kwargs):
        pytest.fail("unimplemented condition reached input/provider setup")

    monkeypatch.setattr(runner, "_source_provenance", forbidden)
    monkeypatch.setattr(runner, "PublicStructuredRuntime", forbidden)
    with pytest.raises(ValueError, match="ablation"):
        runner.run_experiment(report_root=REPORT, output_dir=tmp_path, ablation=ablation)
    assert not list(tmp_path.iterdir())


def test_condition_identity_worker_resume_and_legacy_reading(tmp_path, monkeypatch):
    if not REPORT.is_dir() and runner._release_source_provenance() is not None:
        pytest.skip("frozen repository pairs are not shipped in the verified release")
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


def test_independent_round_keeps_identity_and_resumes_without_earlier_rounds(tmp_path, monkeypatch):
    args = dict(report_root=REPORT, output_dir=tmp_path, profile="fixture", rounds=1,
                round_index=2, workers=1, pair_ids=["0004"], run_id="b" * 32)
    summary = runner.run_experiment(**args)
    root = Path(summary["artifact_root"])
    assert summary["round_index"] == 2
    cell_path = root / "method/0004/round-2.json"
    original = cell_path.read_bytes()
    assert json.loads(original)["round"] == 2
    assert not (root / "method/0004/round-1.json").exists()
    assert json.loads((root / "run_manifest.json").read_text())["round_index"] == 2

    def forbidden(**kwargs):
        pytest.fail("compatible completed round must not run again")

    monkeypatch.setattr(runner, "_method_cell", forbidden)
    resumed = runner.run_experiment(**args, resume=True)
    assert resumed["method_cell_count"] == 1
    assert cell_path.read_bytes() == original
    with pytest.raises(RuntimeError, match="resume contract mismatch"):
        runner.run_experiment(**{**args, "round_index": 3}, resume=True)
    with pytest.raises(ValueError, match="explicit round"):
        runner.run_experiment(**{**args, "rounds": 3})


def test_explicit_round_failure_terminalizes_exact_requested_round(tmp_path):
    identity = {
        "run_id": "b" * 32, "run_contract_hash": "sha256:" + "c" * 64,
        "ablation": "none", "round_index": 3,
        "source_provenance": {"source_commit": "0" * 40, "source_branch": "fixture",
                              "source_dirty": False, "reason": "Test identity.", "basis": "fixture"},
    }
    runner._terminalize_pair_failure(
        pair_id="0004", rounds=1, output_root=tmp_path, run_identity=identity,
        started_at="2026-09-07T00:00:00+00:00", error=RuntimeError("provider unavailable"),
    )
    files = list((tmp_path / "method/0004").glob("round-*.json"))
    assert [p.name for p in files] == ["round-3.json"]
    assert json.loads(files[0].read_text())["eligible"] is False


@pytest.mark.parametrize("pairs", [None, list(runner.FROZEN_PAIR_IDS)[:len(runner.REPRESENTATIVE_DIAGNOSTIC_PAIR_IDS) + 1]])
def test_non_luna_full_and_batched_live_require_review_gate(tmp_path, monkeypatch, pairs):
    args = dict(report_root=REPORT, output_dir=tmp_path, profile="claude-sonnet-5",
                rounds=1, round_index=2, pair_ids=pairs, allow_live=True)
    with pytest.raises(RuntimeError, match="allow_full_live"):
        runner.run_experiment(**args)

    def reached_provenance():
        raise LookupError("passed explicit live gates")

    monkeypatch.setattr(runner, "_source_provenance", reached_provenance)
    with pytest.raises(LookupError, match="passed explicit live gates"):
        runner.run_experiment(**args, allow_full_live=True)


def test_packaged_no_inspect_prompt_and_input_contract():
    from paper_stm_method.semantics.ablation import NoInspectInput, system_prompt_for
    from paper_stm_method.semantics.workflow import DISCOVERY_GROUNDING_SYSTEM_PROMPT

    assert "inspection" not in system_prompt_for(DISCOVERY_GROUNDING_SYSTEM_PROMPT, ablation="no-inspect").lower()
    assert system_prompt_for(DISCOVERY_GROUNDING_SYSTEM_PROMPT) is DISCOVERY_GROUNDING_SYSTEM_PROMPT
    for field in ("reference_inspection", "inspection_facts", "verify_facts", "smt_facts"):
        assert NoInspectInput.model_json_schema()["properties"][field]["type"] == "null"
