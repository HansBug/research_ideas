from __future__ import annotations

import json
from types import SimpleNamespace

from paper_stm_repair_loop.agents import discover


class _Registry:
    def require(self, profile: str) -> object:
        assert profile == "gpt-5.5"
        return object()


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
