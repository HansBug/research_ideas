from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SELECTED = REPO / "project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples"
REPORTS = ROOT / "reports"
SRC = ROOT / "src"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_selected_examples_hashes_match_source_meta():
    for d in sorted(p for p in SELECTED.iterdir() if p.is_dir()):
        meta = json.loads((d / "source_meta.json").read_text(encoding="utf-8"))
        stms = list(d.glob("stm0.*"))
        assert len(stms) == 1
        assert sha256(d / "nl.txt") == meta["nl_sha256"]
        assert sha256(stms[0]) == meta["stm0_sha256"]
        source_pairs = (d / meta["source_pairs_jsonl"]).resolve()
        assert source_pairs.exists()
        assert any(json.loads(line).get("pair_id") == meta["pair_id"] for line in source_pairs.read_text(encoding="utf-8").splitlines())


def test_cli_regenerates_four_example_report(tmp_path):
    out = tmp_path / "reports"
    cmd = [
        sys.executable,
        "-m",
        "paper_stm_repair_conversion.cli",
        "convert-selected",
        "--reports-dir",
        str(out),
        "--run-id",
        "pytest-r3-smoke",
    ]
    completed = subprocess.run(
        cmd,
        cwd=REPO,
        env={**os.environ, "PYTHONPATH": str(SRC)},
        text=True,
        capture_output=True,
        check=True,
    )
    assert '"examples": 4' in completed.stdout
    report = json.loads((out / "selected_seed_examples_conversion_report.json").read_text(encoding="utf-8"))
    by_id = {item["example_id"]: item for item in report["items"]}
    assert by_id["llms-emp-gpt4o-hldcs"]["status"] == "converted"
    assert by_id["llms-emp-gpt4o-hldcs"]["conversion_source"] == "official_scxml"
    assert by_id["unified-uml-synthetic-0000"]["status"] == "partial"
    assert by_id["unified-uml-synthetic-0000"]["conversion_source"] == "no_canonical_conversion"
    assert by_id["unified-uml-synthetic-0000"]["canonical_output_path"] is None
    assert by_id["sefm-ssc7-umple"]["status"] == "partial"
    assert by_id["sefm-ssc7-umple"]["conversion_source"] == "official_scxml"
    assert by_id["ttool-automatedbraking-xml"]["status"] == "partial"
    assert by_id["ttool-automatedbraking-xml"]["conversion_source"] == "official_xml"
    assert all("tool_preflight" in item for item in report["items"])


def test_committed_report_keeps_r3_smoke_boundary_and_losses():
    report = json.loads((REPORTS / "selected_seed_examples_conversion_report.json").read_text(encoding="utf-8"))
    by_id = {item["example_id"]: item for item in report["items"]}
    assert all(item["eligibility"] == "r3_smoke_fixture_only_not_main_experiment" for item in report["items"])
    assert by_id["llms-emp-gpt4o-hldcs"]["status"] == "converted"
    assert by_id["llms-emp-gpt4o-hldcs"]["hierarchy_level"] == "hierarchical"
    assert by_id["unified-uml-synthetic-0000"]["status"] == "partial"
    assert by_id["unified-uml-synthetic-0000"]["hierarchy_level"] == "flat"
    assert by_id["unified-uml-synthetic-0000"]["states_count"] == 0
    assert by_id["unified-uml-synthetic-0000"]["transitions_count"] == 0
    assert by_id["unified-uml-synthetic-0000"]["conversion_source"] == "no_canonical_conversion"
    assert by_id["unified-uml-synthetic-0000"]["canonical_output_path"] is None
    assert by_id["sefm-ssc7-umple"]["timing_level"] == "qualitative"
    assert by_id["ttool-automatedbraking-xml"]["timing_level"] == "timed_constraints"
    losses = (REPORTS / "selected_seed_examples_loss_ledger.jsonl").read_text(encoding="utf-8")
    assert "sefm-ssc7-umple:umple:timing_after" in losses
    assert "ttool-automatedbraking-xml:ttool_xml:unresolved_connectors" in losses
    assert "unified-uml-synthetic-0000:plantuml:official_preflight_failed" in losses


def test_committed_reports_do_not_embed_local_absolute_paths():
    for path in [
        REPORTS / "selected_seed_examples_conversion_report.json",
        REPORTS / "selected_seed_examples_input_audit.json",
        REPORTS / "selected_seed_examples_loss_ledger.jsonl",
    ]:
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text



def test_committed_outputs_use_official_structured_sources_and_timing_audit_only():
    plant = json.loads((REPORTS / "canonical" / "llms-emp-gpt4o-hldcs.canonical_stm.json").read_text(encoding="utf-8"))
    assert plant["metadata"]["conversion_source"] == "official_scxml"
    assert plant["metadata"]["fallback_used"] is False
    assert all("stm0.scxml:" in s["raw_ref"] for s in plant["model"]["states"])
    assert all("stm0.scxml:" in t["raw_ref"] for t in plant["model"]["transitions"])
    assert any(d["code"] == "R3.STRUCTURED_EXPORT.CANONICAL_FROM_SCXML" for d in plant["diagnostics"])

    umple = json.loads((REPORTS / "canonical" / "sefm-ssc7-umple.canonical_stm.json").read_text(encoding="utf-8"))
    assert umple["metadata"]["conversion_source"] == "official_scxml"
    assert umple["metadata"]["fallback_used"] is True
    assert "targeted raw timing/loss audit" in umple["metadata"]["fallback_scope"]
    assert all("stm0.scxml:" in s["raw_ref"] for s in umple["model"]["states"])
    assert all("stm0.scxml:" in t["raw_ref"] for t in umple["model"]["transitions"])
    assert any(d["code"] == "R3.UMPLE.TIMING_RAW_AUDIT" for d in umple["diagnostics"])
    assert any(t.get("event") == "timeoutTimeoutToReady" for t in umple["model"]["transitions"])


def test_input_audit_records_source_pair_hashes_and_documented_divergence():
    audit = json.loads((REPORTS / "selected_seed_examples_input_audit.json").read_text(encoding="utf-8"))
    by_id = {row["example_id"]: row for row in audit["items"]}
    assert all(row["source_nl_hash_match"] for row in audit["items"])
    assert all(row["source_hash_divergence_documented"] for row in audit["items"])
    assert by_id["sefm-ssc7-umple"]["source_stm0_hash_match"] is False
    assert "whitespace normalization" in by_id["sefm-ssc7-umple"]["hash_scope"]


def test_ttool_partial_inventory_has_zero_resolved_counts():
    report = json.loads((REPORTS / "selected_seed_examples_conversion_report.json").read_text(encoding="utf-8"))
    ttool = next(item for item in report["items"] if item["example_id"] == "ttool-automatedbraking-xml")
    assert ttool["states_count"] > 0
    assert ttool["resolved_states_count"] == 0
    assert ttool["resolved_transitions_count"] == 0


def test_committed_report_records_official_toolchain_preflight():
    report = json.loads((REPORTS / "selected_seed_examples_conversion_report.json").read_text(encoding="utf-8"))
    by_id = {item["example_id"]: item for item in report["items"]}

    llms = by_id["llms-emp-gpt4o-hldcs"]["tool_preflight"]
    assert llms["tool_name"] == "PlantUML CLI"
    assert llms["syntax_status"] == "ok"
    assert llms["structured_export_status"] == "scxml_export_ok"
    assert llms["structured_export_path"].endswith("toolchain_exports/llms-emp-gpt4o-hldcs/stm0.scxml")
    assert (REPO / llms["structured_export_path"]).exists()

    unified = by_id["unified-uml-synthetic-0000"]["tool_preflight"]
    assert unified["tool_name"] == "PlantUML CLI"
    assert unified["syntax_status"] == "failed"
    assert unified["structured_export_status"] == "scxml_not_trusted_after_syntax_failure"
    assert by_id["unified-uml-synthetic-0000"]["status"] == "partial"

    sefm = by_id["sefm-ssc7-umple"]["tool_preflight"]
    assert sefm["tool_name"] == "Umple compiler CLI"
    assert sefm["syntax_status"] == "ok"
    assert sefm["structured_export_status"] == "scxml_export_ok"
    assert sefm["structured_export_path"].endswith("toolchain_exports/sefm-ssc7-umple/stm0.scxml")
    assert (REPO / sefm["structured_export_path"]).exists()
    assert by_id["sefm-ssc7-umple"]["conversion_source"] == "official_scxml"

    ttool = by_id["ttool-automatedbraking-xml"]["tool_preflight"]
    assert ttool["tool_name"] == "TTool / AVATAR XML artifact"
    assert ttool["syntax_status"] == "xml_wellformed_checked_by_python_etree"
    assert ttool["structured_export_status"] == "official_xml_available_no_scxml_json_ast_export_documented"


def test_cli_invokes_configured_external_toolchains(tmp_path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_plantuml = fake_bin / "plantuml.jar"
    fake_umple = fake_bin / "umple.jar"
    fake_plantuml.write_text(
        "#!/usr/bin/env python3\n"
        "import os, pathlib, sys\n"
        "args = sys.argv[1:]\n"
        "pathlib.Path(os.environ['PLANTUML_CALL_LOG']).open('a').write(' '.join(args) + '\\n')\n"
        "if '-version' in args:\n"
        "    print('Fake PlantUML 0.0')\n"
        "    raise SystemExit(0)\n"
        "if '-checkonly' in args:\n"
        "    raise SystemExit(0)\n"
        "if '-tscxml' in args:\n"
        "    src = pathlib.Path(args[-1])\n"
        "    src.with_suffix('.scxml').write_text('<scxml version=\\\"1.0\\\"/>', encoding='utf-8')\n"
        "    raise SystemExit(0)\n"
        "raise SystemExit(0)\n",
        encoding="utf-8",
    )
    fake_umple.write_text(
        "#!/usr/bin/env python3\n"
        "import os, pathlib, sys\n"
        "args = sys.argv[1:]\n"
        "pathlib.Path(os.environ['UMPLE_CALL_LOG']).open('a').write(' '.join(args) + '\\n')\n"
        "if '--version' in args:\n"
        "    print('Fake Umple 0.0')\n"
        "    raise SystemExit(0)\n"
        "if '-g' in args and 'Scxml' in args:\n"
        "    src = pathlib.Path(args[-1])\n"
        "    src.with_suffix('.scxml').write_text('<scxml version=\\\"1.0\\\"/>', encoding='utf-8')\n"
        "raise SystemExit(0)\n",
        encoding="utf-8",
    )
    fake_plantuml.chmod(0o755)
    fake_umple.chmod(0o755)

    fake_java = fake_bin / "java"
    fake_java.write_text(
        "#!/usr/bin/env python3\n"
        "import os, subprocess, sys\n"
        "args = sys.argv[1:]\n"
        "if args[:2] == ['-jar', os.environ['PLANTUML_JAR']]:\n"
        "    raise SystemExit(subprocess.call([os.environ['PLANTUML_JAR'], *args[2:]]))\n"
        "if args[:2] == ['-jar', os.environ['UMPLE_JAR']]:\n"
        "    raise SystemExit(subprocess.call([os.environ['UMPLE_JAR'], *args[2:]]))\n"
        "if args == ['-version']:\n"
        "    sys.stderr.write('fake java 1.8\\n')\n"
        "    raise SystemExit(0)\n"
        "raise SystemExit(2)\n",
        encoding="utf-8",
    )
    fake_java.chmod(0o755)

    out = tmp_path / "reports"
    cmd = [
        sys.executable,
        "-m",
        "paper_stm_repair_conversion.cli",
        "convert-selected",
        "--reports-dir",
        str(out),
        "--run-id",
        "pytest-r3-toolchain",
    ]
    plant_log = tmp_path / "plantuml_calls.log"
    umple_log = tmp_path / "umple_calls.log"
    env = {
        **os.environ,
        "PYTHONPATH": str(SRC),
        "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
        "PLANTUML_JAR": str(fake_plantuml),
        "UMPLE_JAR": str(fake_umple),
        "PLANTUML_CALL_LOG": str(plant_log),
        "UMPLE_CALL_LOG": str(umple_log),
    }
    subprocess.run(cmd, cwd=REPO, env=env, text=True, capture_output=True, check=True)

    plant_calls = plant_log.read_text(encoding="utf-8")
    umple_calls = umple_log.read_text(encoding="utf-8")
    try:
        assert "-checkonly" in plant_calls
        assert "-tscxml" in plant_calls
        assert "-g Nothing" in umple_calls
        assert "-g Scxml" in umple_calls
    finally:
        plant_log.unlink(missing_ok=True)
        umple_log.unlink(missing_ok=True)
