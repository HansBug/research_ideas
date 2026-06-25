from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SRC = ROOT / "src"


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
    ]
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def _fake_plantuml_env(tmp_path: Path) -> dict[str, str]:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_plantuml = fake_bin / "plantuml.jar"
    fake_plantuml.write_text(
        "#!/usr/bin/env python3\n"
        "import pathlib, sys\n"
        "args = sys.argv[1:]\n"
        "if '-version' in args:\n"
        "    print('Fake PlantUML recovery 0.0')\n"
        "    raise SystemExit(0)\n"
        "src = pathlib.Path(args[-1])\n"
        "text = src.read_text(encoding='utf-8')\n"
        "bad = (('\"Menu Created\"' in text) and ('state \"Menu Created\" as' not in text)) or ('entry/Accelerate' in text) or ('fork fork1' in text)\n"
        "if '-checkonly' in args:\n"
        "    raise SystemExit(200 if bad else 0)\n"
        "if '-tscxml' in args:\n"
        "    if bad:\n"
        "        raise SystemExit(1)\n"
        "    src.with_suffix('.scxml').write_text('<scxml version=\"1.0\" initial=\"S1\"><state id=\"S1\"><transition target=\"S2\" event=\"go\"/></state><state id=\"S2\"/></scxml>', encoding='utf-8')\n"
        "    raise SystemExit(0)\n"
        "raise SystemExit(0)\n",
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
    cmd = [
        sys.executable,
        "-m",
        "paper_stm_repair_conversion.cli",
        "recover-plantuml",
        "--pair-source",
        str(pairs),
        "--reports-dir",
        str(reports),
        "--run-dir",
        str(run_dir),
        "--run-id",
        "pytest-r3.1-recovery",
        "--created-at",
        "2026-06-25T12:00:00+00:00",
    ]
    completed = subprocess.run(cmd, cwd=REPO, env=_fake_plantuml_env(tmp_path), text=True, capture_output=True, check=True)
    assert '"raw_total": 4' in completed.stdout
    report = json.loads((reports / "plantuml_recovery_report.json").read_text(encoding="utf-8"))
    ledger_rows = [json.loads(line) for line in (reports / "plantuml_normalization_ledger.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    jsonschema.Draft202012Validator(json.loads((ROOT / "schemas" / "recovery_report.schema.json").read_text(encoding="utf-8"))).validate(report)
    ledger_schema = json.loads((ROOT / "schemas" / "normalization_ledger.schema.json").read_text(encoding="utf-8"))
    for row in ledger_rows:
        jsonschema.Draft202012Validator(ledger_schema).validate(row)
        assert row["repair_contribution_allowed"] is False
    by_id = {item["pair_id"]: item for item in report["items"]}
    assert by_id["p_ok"]["raw_scxml_pass"] is True
    assert by_id["p_ok"]["recovery_bucket"] == "already_converted_before_normalization"
    assert by_id["p_low"]["technical_scxml_pass_all_rules"] is True
    assert by_id["p_low"]["low_risk_scxml_pass"] is True
    assert by_id["p_low"]["main_eligibility_included"] is True
    assert by_id["p_high"]["technical_scxml_pass_all_rules"] is False
    assert by_id["p_high"]["low_risk_scxml_pass"] is False
    assert by_id["p_high"]["main_eligibility_included"] is False
    assert by_id["p_fork"]["technical_scxml_pass_all_rules"] is True
    assert by_id["p_fork"]["concurrency_degraded"] is True
    assert by_id["p_fork"]["main_eligibility_included"] is False
    assert report["summary"]["technical_scxml_pass_all_rules"] == 2
    assert report["summary"]["low_risk_scxml_pass"] == 1
    assert report["summary"]["main_eligibility_included"] == 1
    assert report["summary"]["llms_emp_cross_llm_gate"]["passed"] is False
    assert set(report["summary"]["llms_emp_cross_llm_gate"]["eligible_after_by_llm"]) == {"Claude", "DeepSeek", "GPT-4", "GPT-4o", "Kimi", "Llama"}
    assert any(row["rule_id"] == "PUML.NORM.fork_join_decl_to_state" and row["concurrency_degraded"] for row in ledger_rows)
    assert all(row["raw_text_unchanged"] for row in report["raw_immutability"])
    assert "/home/" not in (reports / "plantuml_recovery_report.json").read_text(encoding="utf-8")
    assert "/tmp/" not in (reports / "plantuml_recovery_report.json").read_text(encoding="utf-8")
