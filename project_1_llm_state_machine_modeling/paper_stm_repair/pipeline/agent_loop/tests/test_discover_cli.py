from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import paper_stm_repair_loop.inputs as input_module
from paper_stm_repair_loop.agents import discover
from paper_stm_repair_loop.inputs import load_custom


class _Registry:
    def require(self, profile: str) -> object:
        assert profile == "gpt-5.5"
        return object()


MANUAL_IDENTITY_DIR = Path(
    "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/agent_loop/"
    "fixtures/discover_integrated/0000_hldcs_manual_identity"
)
FORMAL_SELECTED_SEED_DIR = Path(
    "project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples/"
    "llms_emp_feedback_final_0000"
)
FORMAL_EVIDENCE_DIR = Path(
    "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/"
    "representation/reports/llms_emp_r45_java_60"
)
SELECTED_FEEDBACK_FINAL_STM_SHA256 = (
    "4fe07b05bdcfaac1c961d1176fb099d8240818160caa6edfb57928c6be2efc8a"
)
PHASE_I_GENERATION_STM_SHA256 = (
    "8fd2f71b338836488e2e29fe19c4e58c4992d4186367f43efc121fae6c36db7f"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_manual_identity_demo_uses_explicit_custom_fixture():
    case = load_custom(
        "llms_emp_stm_results_0000_manual_identity",
        MANUAL_IDENTITY_DIR / "nl.txt",
        MANUAL_IDENTITY_DIR / "STM_0.fcstm",
    )

    assert case.pair_id is None
    assert case.case_id == "llms_emp_stm_results_0000_manual_identity"
    assert case.input_mode == "custom"
    assert case.raw_source_format == "fcstm-identity"
    assert case.raw_source == case.fcstm
    assert case.source_trace["relation_policy"] == "exact_identity"


def test_pair_loader_rejects_duplicate_selected_directories(monkeypatch, tmp_path):
    for name in ("a", "b"):
        directory = tmp_path / name
        directory.mkdir()
        (directory / "source_meta.json").write_text(
            json.dumps({"pair_id": "llms_emp_feedback_final_0000"}),
            encoding="utf-8",
        )
    monkeypatch.setattr(input_module, "SELECTED_ROOT", tmp_path)

    with pytest.raises(ValueError, match="PAIR_SELECTED_DIRECTORY_AMBIGUOUS"):
        input_module.load_pair("llms_emp_feedback_final_0000")


def test_manual_identity_source_meta_uses_feedback_final_selected_seed_bytes():
    manual_meta = json.loads(
        (MANUAL_IDENTITY_DIR / "source_meta.json").read_text(encoding="utf-8")
    )
    formal_meta = json.loads(
        (FORMAL_SELECTED_SEED_DIR / "source_meta.json").read_text(encoding="utf-8")
    )

    assert manual_meta["discover_pair_id"] == "llms_emp_stm_results_0000_manual_identity"
    for field in (
        "pair_id",
        "source_pair_id",
        "source_locator_type",
        "source_locator",
        "source_locator_data",
        "selected_stage",
        "selected_stage_column",
        "selected_stage_cell",
        "stm0_sha256",
        "source_stm0_sha256",
    ):
        assert manual_meta[field] == formal_meta[field]

    assert _sha256(MANUAL_IDENTITY_DIR / "stm0.puml") == formal_meta["stm0_sha256"]
    assert _sha256(MANUAL_IDENTITY_DIR / "stm0.puml") == SELECTED_FEEDBACK_FINAL_STM_SHA256


def test_manual_identity_source_meta_binds_current_formal_manifest_and_seal():
    manual_meta = json.loads(
        (MANUAL_IDENTITY_DIR / "source_meta.json").read_text(encoding="utf-8")
    )

    assert manual_meta["conversion_manifest_sha256"] == _sha256(
        FORMAL_EVIDENCE_DIR / "manifest.json"
    )
    assert manual_meta["publication_seal_sha256"] == _sha256(
        FORMAL_EVIDENCE_DIR / "PUBLICATION_SEAL.json"
    )


def test_manual_identity_phase_i_generation_is_derivation_only_provenance():
    source_meta = json.loads(
        (MANUAL_IDENTITY_DIR / "source_meta.json").read_text(encoding="utf-8")
    )
    fcstm_meta = json.loads(
        (MANUAL_IDENTITY_DIR / "fcstm_meta.json").read_text(encoding="utf-8")
    )
    provenance_path = MANUAL_IDENTITY_DIR / "phase_i_generation_provenance.puml"

    assert _sha256(provenance_path) == PHASE_I_GENERATION_STM_SHA256
    assert (
        source_meta["manual_derivation_provenance"]["sha256"]
        == PHASE_I_GENERATION_STM_SHA256
    )
    assert (
        fcstm_meta["phase_i_generation_provenance_sha256"]
        == PHASE_I_GENERATION_STM_SHA256
    )
    assert source_meta["stm0_sha256"] != PHASE_I_GENERATION_STM_SHA256
    assert fcstm_meta["source_stm0_sha256"] != PHASE_I_GENERATION_STM_SHA256


def test_cli_custom_mode_emits_machine_readable_success(monkeypatch, tmp_path, capsys):
    nl = tmp_path / "nl.txt"
    model = tmp_path / "model.fcstm"
    out = tmp_path / "run"
    nl.write_text("Power_Off moves Active to Off.", encoding="utf-8")
    model.write_text("state Root {}", encoding="utf-8")
    case = object()
    monkeypatch.setattr(discover, "load_llm_registry", lambda _path: _Registry())
    monkeypatch.setattr(discover, "load_custom", lambda *args, **kwargs: case)
    monkeypatch.setattr(discover, "prepare_run_dir", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        discover,
        "run_discover",
        lambda run_dir, registry: SimpleNamespace(
            run_id="cli-test", completed_record_id="REC-000001"
        ),
    )

    code = discover.main(
        [
            "--case-id",
            "cli-test",
            "--nl-file",
            str(nl),
            "--fcstm-file",
            str(model),
            "--output-dir",
            str(out),
            "--max-model-calls",
            "7",
            "--max-tool-calls",
            "9",
            "--max-turns",
            "11",
            "--max-seconds",
            "120",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "outdir": str(out),
        "record_id": "REC-000001",
        "report": str(out / "loops/discover.md"),
        "run_id": "cli-test",
        "status": "discover_completed",
    }


def test_cli_defaults_leave_agent_and_reviewer_limits_unset(
    monkeypatch, tmp_path, capsys
):
    nl = tmp_path / "nl.txt"
    model = tmp_path / "model.fcstm"
    out = tmp_path / "run"
    nl.write_text("Power_Off moves Active to Off.", encoding="utf-8")
    model.write_text("state Root {}", encoding="utf-8")
    captured: dict[str, object] = {}
    monkeypatch.setattr(discover, "load_llm_registry", lambda _path: _Registry())
    monkeypatch.setattr(discover, "load_custom", lambda *args, **kwargs: object())

    def capture_prepare(*_args, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(discover, "prepare_run_dir", capture_prepare)
    monkeypatch.setattr(
        discover,
        "run_discover",
        lambda run_dir, registry: SimpleNamespace(
            run_id="unlimited-defaults", completed_record_id="REC-000001"
        ),
    )

    assert (
        discover.main(
            [
                "--case-id",
                "unlimited-defaults",
                "--nl-file",
                str(nl),
                "--fcstm-file",
                str(model),
                "--output-dir",
                str(out),
            ]
        )
        == 0
    )
    assert captured["agent_limits"] == {}
    assert captured["reviewer_limits"] == {}
    assert captured["profile"] == "gpt-5.5"
    assert "coverage_review_profile" not in captured
    assert "falsification_review_profile" not in captured
    capsys.readouterr()


def test_cli_exposes_only_one_profile_selector():
    parser = discover._parser()
    option_strings = {
        option
        for action in parser._actions
        for option in action.option_strings
    }

    assert "--profile" in option_strings
    assert "--coverage-review-profile" not in option_strings
    assert "--falsification-review-profile" not in option_strings


def test_cli_custom_mode_missing_files_returns_two(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(discover, "load_llm_registry", lambda _path: _Registry())
    code = discover.main(
        [
            "--case-id",
            "missing-inputs",
            "--output-dir",
            str(tmp_path / "run"),
        ]
    )
    assert code == 2
    assert "custom mode requires" in capsys.readouterr().err


def test_cli_pair_mode_rejects_custom_files(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(discover, "load_llm_registry", lambda _path: _Registry())
    code = discover.main(
        [
            "--pair-id",
            "pair-1",
            "--nl-file",
            str(tmp_path / "nl.txt"),
            "--output-dir",
            str(tmp_path / "run"),
        ]
    )
    assert code == 2
    assert "pair mode cannot use custom input arguments" in capsys.readouterr().err
