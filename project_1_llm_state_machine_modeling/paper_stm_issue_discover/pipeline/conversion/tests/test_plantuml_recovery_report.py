from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
def repo_root() -> Path:
    for parent in [ROOT, *ROOT.parents]:
        if (parent / ".git").exists() and (parent / "project_1_llm_state_machine_modeling").exists():
            return parent
    raise RuntimeError("repository root not found")


REPO = repo_root()
SRC = ROOT / "src"


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_pairs(path: Path) -> None:
    rows = [
        {
            "seed_id": "llms-emp-stm-subset",
            "pair_id": "p_ok",
            "nl_sha256": "0" * 64,
            "stm0_sha256": "1" * 64,
            "nl_text": "ok nl",
            "stm_format": "plantuml",
            "stm0_text": "@startuml\n[*] --> OK\nOK --> [*]\n@enduml\n",
            "llm": "GPT-4o",
            "generation_model_or_method": "fake",
            "source_locator": "fixture:ok",
        },
        {
            "seed_id": "llms-emp-stm-subset",
            "pair_id": "p_low",
            "nl_sha256": "2" * 64,
            "stm0_sha256": "3" * 64,
            "nl_text": "low-risk nl",
            "stm_format": "plantuml",
            "stm0_text": "@startuml\n[*] --> \"Menu Created\"\n\"Menu Created\" --> [*]\n@enduml\n",
            "llm": "GPT-4o",
            "generation_model_or_method": "fake",
            "source_locator": "fixture:low",
        },
        {
            "seed_id": "llms-emp-stm-subset",
            "pair_id": "p_empty_scxml",
            "nl_sha256": "8" * 64,
            "stm0_sha256": "9" * 64,
            "nl_text": "official scxml exists but canonical parse is blocked",
            "stm_format": "plantuml",
            "stm0_text": "@startuml\n[*] --> \"Empty SCXML\"\n\"Empty SCXML\" --> [*]\n@enduml\n",
            "llm": "Claude",
            "generation_model_or_method": "fake",
            "source_locator": "fixture:empty-scxml",
        },
        {
            "seed_id": "llms-emp-stm-subset",
            "pair_id": "p_high",
            "nl_sha256": "4" * 64,
            "stm0_sha256": "5" * 64,
            "nl_text": "high-risk nl",
            "stm_format": "plantuml",
            "stm0_text": "@startuml\nstate A {\n  entry/Accelerate\n}\nA --> [*]\n@enduml\n",
            "llm": "Llama",
            "generation_model_or_method": "fake",
            "source_locator": "fixture:high",
        },
        {
            "seed_id": "llms-emp-stm-subset",
            "pair_id": "p_fork",
            "nl_sha256": "6" * 64,
            "stm0_sha256": "7" * 64,
            "nl_text": "fork nl",
            "stm_format": "plantuml",
            "stm0_text": "@startuml\nfork fork1\nA --> fork1\n@enduml\n",
            "llm": "DeepSeek",
            "generation_model_or_method": "fake",
            "source_locator": "fixture:fork",
        },
        {
            "seed_id": "llms-emp-stm-subset",
            "pair_id": "p_when",
            "nl_sha256": "c" * 64,
            "stm0_sha256": "d" * 64,
            "nl_text": "when label nl",
            "stm_format": "plantuml",
            "stm0_text": "@startuml\nchoice2 --> Join1 when : sunny=true\n@enduml\n",
            "llm": "GPT-4",
            "generation_model_or_method": "fake",
            "source_locator": "fixture:when",
        },
        {
            "seed_id": "llms-emp-stm-subset",
            "pair_id": "p_empty_label",
            "nl_sha256": "e" * 64,
            "stm0_sha256": "f" * 64,
            "nl_text": "empty label nl",
            "stm_format": "plantuml",
            "stm0_text": "@startuml\nchoice1 --> choice3:\nFlash --> Terminate:\n@enduml\n",
            "llm": "Llama",
            "generation_model_or_method": "fake",
            "source_locator": "fixture:empty-label",
        },
        {
            "seed_id": "llms-emp-stm-subset",
            "pair_id": "p_bracket",
            "nl_sha256": "1" * 64,
            "stm0_sha256": "2" * 64,
            "nl_text": "bracket endpoint nl",
            "stm_format": "plantuml",
            "stm0_text": "@startuml\n[FrontendCollision] -down-> [BrakingControl] : Brake Signal Received\n[BrakingControl] --> [*] : Collision Avoided\n@enduml\n",
            "llm": "Kimi",
            "generation_model_or_method": "fake",
            "source_locator": "fixture:bracket",
        },
        {
            "seed_id": "unified-uml-multimodal-validation",
            "pair_id": "p_unified",
            "nl_sha256": "a" * 64,
            "stm0_sha256": "b" * 64,
            "nl_text": "synthetic unified nl",
            "stm_format": "plantuml",
            "stm0_text": "@startuml\n[*] --> \"Unified State\"\n\"Unified State\" --> [*]\n@enduml\n",
            "generation_model_or_method": "synthetic",
            "source_locator": "fixture:unified",
        },
    ]
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def _fake_plantuml_env(tmp_path: Path) -> dict[str, str]:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_plantuml = fake_bin / "plantuml.jar"
    fake_plantuml.write_text(
        textwrap.dedent(
            r'''
            #!/usr/bin/env python3
            import pathlib
            import sys

            args = sys.argv[1:]
            if "-version" in args:
                print("Fake PlantUML recovery 0.0")
                raise SystemExit(0)
            src = pathlib.Path(args[-1])
            text = src.read_text(encoding="utf-8")
            needs_alias = ('"Menu Created"' in text) or ('"Empty SCXML"' in text) or ('"Unified State"' in text)
            has_empty_label = any("-->" in line and line.strip().endswith(":") for line in text.splitlines())
            has_nonstar_bracket_endpoint = "[FrontendCollision]" in text or "[BrakingControl]" in text
            bad = (
                (needs_alias and ('state "' not in text))
                or ("entry/Accelerate" in text)
                or ("fork fork1" in text)
                or (" when :" in text)
                or has_empty_label
                or has_nonstar_bracket_endpoint
            )
            if "-checkonly" in args:
                raise SystemExit(200 if bad else 0)
            if "-tscxml" in args:
                if bad:
                    raise SystemExit(1)
                if "Empty SCXML" in text:
                    src.with_suffix(".scxml").write_text('<scxml version="1.0"><state id="S1"/></scxml>', encoding="utf-8")
                else:
                    src.with_suffix(".scxml").write_text('<scxml version="1.0" initial="S1"><state id="S1"><transition target="S2" event="go"/></state><state id="S2"/></scxml>', encoding="utf-8")
                raise SystemExit(0)
            raise SystemExit(0)
            '''
        ).lstrip(),
        encoding="utf-8",
    )
    fake_plantuml.chmod(0o755)
    fake_java = fake_bin / "java"
    fake_java.write_text(
        "#!/usr/bin/env python3\n"
        "import os, subprocess, sys\n"
        "args = sys.argv[1:]\n"
        "if args == ['-version']:\n"
        "    sys.stderr.write('fake java 1.8\\n')\n"
        "    raise SystemExit(0)\n"
        "if args[:2] == ['-jar', os.environ['PLANTUML_JAR']]:\n"
        "    raise SystemExit(subprocess.call([os.environ['PLANTUML_JAR'], *args[2:]]))\n"
        "raise SystemExit(2)\n",
        encoding="utf-8",
    )
    fake_java.chmod(0o755)
    return {
        **os.environ,
        "PYTHONPATH": str(SRC),
        "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
        "PLANTUML_JAR": str(fake_plantuml),
    }


def test_recover_plantuml_report_schema_and_eligibility_gates(tmp_path):
    pairs = tmp_path / "pairs.jsonl"
    reports = tmp_path / "reports"
    run_dir = tmp_path / "run"
    _write_pairs(pairs)
    pair_lines = pairs.read_text(encoding="utf-8").splitlines()
    cmd = [
        sys.executable,
        "-m",
        "paper_stm_conversion.cli",
        "recover-plantuml",
        "--pair-source",
        str(pairs),
        "--reports-dir",
        str(reports),
        "--run-dir",
        str(run_dir),
        "--archive-dir",
        str(tmp_path / "archive"),
        "--run-id",
        "pytest-r3.1-recovery",
        "--created-at",
        "2026-06-25T12:00:00+00:00",
    ]
    completed = subprocess.run(cmd, cwd=REPO, env=_fake_plantuml_env(tmp_path), text=True, capture_output=True, check=True)
    assert '"raw_total": 9' in completed.stdout
    assert (tmp_path / "archive" / "workdir.zip").exists()
    assert (tmp_path / "archive" / "workdir.zip.sha256").exists()
    assert (tmp_path / "archive" / "manifest.json").exists()
    assert not run_dir.exists(), "default CLI should archive then remove high-cardinality loose workdir"
    report = json.loads((reports / "plantuml_recovery_report.json").read_text(encoding="utf-8"))
    ledger_rows = [json.loads(line) for line in (reports / "plantuml_normalization_ledger.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    jsonschema.Draft202012Validator(json.loads((ROOT / "schemas" / "recovery_report.schema.json").read_text(encoding="utf-8"))).validate(report)
    assert report["repo_commit"] == report["generator_code_commit"]
    assert isinstance(report["generator_worktree_dirty"], bool)
    assert isinstance(report["generator_git_status_porcelain"], list)
    assert "recover-plantuml" in report["generation_command"]
    assert "artifact commit" in report["artifact_commit_note"]
    ledger_schema = json.loads((ROOT / "schemas" / "normalization_ledger.schema.json").read_text(encoding="utf-8"))
    for row in ledger_rows:
        jsonschema.Draft202012Validator(ledger_schema).validate(row)
        assert row["repair_contribution_allowed"] is False
    by_id = {item["pair_id"]: item for item in report["items"]}
    assert by_id["p_ok"]["raw_scxml_pass"] is True
    assert by_id["p_ok"]["raw_canonical_parse_pass"] is True
    assert by_id["p_ok"]["raw_conversion_pass"] is True
    assert by_id["p_ok"]["recovery_bucket"] == "already_converted_before_normalization"
    assert by_id["p_low"]["normalized_scxml_pass"] is True
    assert by_id["p_low"]["normalized_canonical_parse_pass"] is True
    assert by_id["p_low"]["normalized_conversion_pass"] is True
    assert by_id["p_low"]["technical_scxml_pass_all_rules"] is True
    assert by_id["p_low"]["low_risk_scxml_pass"] is True
    assert by_id["p_low"]["main_eligibility_included"] is True
    assert by_id["p_low"]["semantic_preservation_pass"] is True
    assert by_id["p_low"]["semantic_preservation_audit"]["status"] == "pass"
    assert by_id["p_empty_scxml"]["normalized_scxml_pass"] is True
    assert by_id["p_empty_scxml"]["normalized_canonical_parse_pass"] is False
    assert by_id["p_empty_scxml"]["normalized_conversion_pass"] is False
    assert by_id["p_empty_scxml"]["technical_scxml_pass_all_rules"] is False
    assert by_id["p_empty_scxml"]["low_risk_scxml_pass"] is False
    assert by_id["p_empty_scxml"]["main_eligibility_included"] is False
    assert by_id["p_high"]["technical_scxml_pass_all_rules"] is False
    assert by_id["p_high"]["low_risk_scxml_pass"] is False
    assert by_id["p_high"]["main_eligibility_included"] is False
    assert by_id["p_fork"]["technical_scxml_pass_all_rules"] is True
    assert by_id["p_fork"]["concurrency_degraded"] is True
    assert by_id["p_fork"]["main_eligibility_included"] is False
    assert by_id["p_unified"]["seed_class"] == "unified_synthetic"
    assert by_id["p_unified"]["main_eligibility_included"] is True
    assert by_id["p_when"]["normalized_scxml_pass"] is True
    assert by_id["p_when"]["main_eligibility_included"] is True
    assert by_id["p_when"]["semantic_preservation_pass"] is True
    assert "PUML.NORM.transition_when_label" in by_id["p_when"]["rule_ids"]
    assert by_id["p_empty_label"]["normalized_scxml_pass"] is True
    assert by_id["p_empty_label"]["main_eligibility_included"] is True
    assert by_id["p_empty_label"]["semantic_preservation_pass"] is True
    assert "PUML.NORM.remove_empty_transition_label" in by_id["p_empty_label"]["rule_ids"]
    assert by_id["p_bracket"]["normalized_scxml_pass"] is True
    assert by_id["p_bracket"]["main_eligibility_included"] is True
    assert by_id["p_bracket"]["semantic_preservation_pass"] is True
    assert "PUML.NORM.alias_bracket_endpoint" in by_id["p_bracket"]["rule_ids"]
    assert report["summary"]["technical_scxml_pass_all_rules"] == 6
    assert report["summary"]["low_risk_scxml_pass"] == 5
    assert report["summary"]["main_eligibility_included"] == 5
    assert report["semantic_preservation_audit_summary"]["audited_total"] == 8
    assert report["semantic_preservation_audit_summary"]["low_risk_fail_total"] == 0
    assert set(report["summary"]["by_seed_class"]) == {"llms_emp_cross_llm", "unified_synthetic"}
    assert report["summary"]["by_seed_class"]["unified_synthetic"]["main_eligibility_included"] == 1
    gate = report["summary"]["llms_emp_cross_llm_gate"]
    assert gate["passed"] is False
    assert set(gate["eligible_after_by_llm"]) == {"Claude", "DeepSeek", "GPT-4", "GPT-4o", "Kimi", "Llama"}
    assert gate["eligible_after_composition_by_llm"]["GPT-4o"]["raw_total"] == 2
    assert gate["eligible_after_composition_by_llm"]["GPT-4o"]["eligible_after"] == 2
    assert gate["eligible_after_composition_by_llm"]["GPT-4"]["raw_total"] == 1
    assert gate["eligible_after_composition_by_llm"]["GPT-4"]["eligible_after"] == 1
    assert gate["eligible_after_composition_by_llm"]["Llama"]["raw_total"] == 2
    assert gate["eligible_after_composition_by_llm"]["Llama"]["eligible_after"] == 1
    assert gate["eligible_after_composition_by_llm"]["Kimi"]["raw_total"] == 1
    assert gate["eligible_after_composition_by_llm"]["Kimi"]["eligible_after"] == 1
    assert gate["eligible_after_composition_by_llm"]["Claude"]["raw_total"] == 1
    assert gate["eligible_after_composition_by_llm"]["Claude"]["eligible_after"] == 0
    assert all(row["source_file_unchanged"] for row in report["source_file_immutability"])
    assert report["source_file_immutability"][0]["source_file_sha256_before"] == _sha256_file(pairs)
    assert report["source_file_immutability"][0]["source_file_sha256_after"] == _sha256_file(pairs)
    assert all(row["raw_text_unchanged"] for row in report["raw_immutability"])
    assert all(row["source_line_unchanged"] for row in report["raw_immutability"])
    assert all(row["source_file_unchanged"] for row in report["raw_immutability"])
    for item, immutability in zip(report["items"], report["raw_immutability"], strict=True):
        assert item["source_line_sha256"] == _sha256_text(pair_lines[item["row_index"]])
        assert item["source_file_sha256"] == _sha256_file(pairs)
        assert immutability["source_line_sha256_before"] == _sha256_text(pair_lines[item["row_index"]])
        assert immutability["source_line_sha256_after"] == _sha256_text(pair_lines[item["row_index"]])
        assert immutability["source_file_sha256_before"] == _sha256_file(pairs)
        assert immutability["source_file_sha256_after"] == _sha256_file(pairs)
    for row in ledger_rows:
        assert row["source_pairs_path"].endswith("pairs.jsonl")
        assert row["source_locator"].startswith("fixture:")
        assert row["source_line_sha256"] == _sha256_text(pair_lines[row["row_index"]])
        assert row["source_file_sha256"] == _sha256_file(pairs)
    assert any(row["rule_id"] == "PUML.NORM.transition_when_label" and row["pair_id"] == "p_when" for row in ledger_rows)
    assert any(row["rule_id"] == "PUML.NORM.remove_empty_transition_label" and row["pair_id"] == "p_empty_label" for row in ledger_rows)
    assert any(row["rule_id"] == "PUML.NORM.alias_bracket_endpoint" and row["pair_id"] == "p_bracket" for row in ledger_rows)
    assert any(row["rule_id"] == "PUML.NORM.fork_join_decl_to_state" and row["concurrency_degraded"] for row in ledger_rows)
    assert "/home/" not in (reports / "plantuml_recovery_report.json").read_text(encoding="utf-8")
    assert "/tmp/" not in (reports / "plantuml_recovery_report.json").read_text(encoding="utf-8")
