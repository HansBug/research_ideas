from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def repo_root() -> Path:
    for parent in [ROOT, *ROOT.parents]:
        if (parent / ".git").exists() and (parent / "project_1_llm_state_machine_modeling").exists():
            return parent
    raise RuntimeError("repository root not found")


REPO = repo_root()
SELECTED = (
    REPO
    / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/"
    "pipeline/conversion/fixtures/r3_selected_seed_examples"
)
REPORTS = ROOT / "reports"
SRC = ROOT / "src"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fake_toolchain_env(tmp_path: Path) -> dict[str, str]:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_plantuml = fake_bin / "plantuml.jar"
    fake_umple = fake_bin / "umple.jar"
    fake_plantuml.write_text(
        "#!/usr/bin/env python3\n"
        "import os, pathlib, sys\n"
        "args = sys.argv[1:]\n"
        "log = os.environ.get('PLANTUML_CALL_LOG')\n"
        "if log:\n"
        "    pathlib.Path(log).open('a').write(' '.join(args) + '\\n')\n"
        "if '-version' in args:\n"
        "    print('Fake PlantUML 0.0')\n"
        "    raise SystemExit(0)\n"
        "src = pathlib.Path(args[-1])\n"
        "text = src.read_text(encoding='utf-8')\n"
        "if any(line.strip().startswith('stm ') for line in text.splitlines()):\n"
        "    sys.stderr.write('Some diagram description contains errors\\n')\n"
        "    raise SystemExit(200 if '-checkonly' in args else 1)\n"
        "if '-checkonly' in args:\n"
        "    raise SystemExit(0)\n"
        "if '-tscxml' in args:\n"
        "    src.with_suffix('.scxml').write_text('<scxml version=\"1.0\" initial=\"S1\"><state id=\"S1\"><transition target=\"S2\" event=\"go\"/></state><state id=\"S2\"/></scxml>', encoding='utf-8')\n"
        "    raise SystemExit(0)\n"
        "raise SystemExit(0)\n",
        encoding="utf-8",
    )
    fake_umple.write_text(
        "#!/usr/bin/env python3\n"
        "import os, pathlib, sys\n"
        "args = sys.argv[1:]\n"
        "log = os.environ.get('UMPLE_CALL_LOG')\n"
        "if log:\n"
        "    pathlib.Path(log).open('a').write(' '.join(args) + '\\n')\n"
        "if '--version' in args:\n"
        "    print('Fake Umple 0.0')\n"
        "    raise SystemExit(0)\n"
        "if '-g' in args and 'Scxml' in args:\n"
        "    src = pathlib.Path(args[-1])\n"
        "    src.with_suffix('.scxml').write_text('<!-- official fake scxml --><scxml version=\"1.0\" initial=\"Ready\"><state id=\"Ready\"><transition target=\"Timeout\" event=\"timeout\"/></state><state id=\"Timeout\"><transition target=\"Ready\" event=\"timeoutTimeoutToReady\"/></state></scxml>', encoding='utf-8')\n"
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
    return {
        **os.environ,
        "PYTHONPATH": str(SRC),
        "PATH": f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
        "PLANTUML_JAR": str(fake_plantuml),
        "UMPLE_JAR": str(fake_umple),
    }


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
        "paper_stm_conversion.cli",
        "convert-selected",
        "--reports-dir",
        str(out),
        "--run-id",
        "pytest-r3-smoke",
    ]
    completed = subprocess.run(
        cmd,
        cwd=REPO,
        env=_fake_toolchain_env(tmp_path),
        text=True,
        capture_output=True,
        check=True,
    )
    assert '"examples": 4' in completed.stdout
    report = json.loads((out / "selected_seed_examples_conversion_report.json").read_text(encoding="utf-8"))
    by_id = {item["example_id"]: item for item in report["items"]}
    assert set(by_id) == {
        "llms-emp-deepseek-microwave",
        "llms-emp-gpt4o-hldcs",
        "llms-emp-kimi-autonomous-collision",
        "sefm-ssc7-umple",
    }
    assert by_id["llms-emp-gpt4o-hldcs"]["status"] == "converted"
    assert by_id["llms-emp-gpt4o-hldcs"]["conversion_source"] == "official_scxml"
    assert by_id["llms-emp-kimi-autonomous-collision"]["status"] == "converted"
    assert by_id["llms-emp-kimi-autonomous-collision"]["conversion_source"] == "official_scxml"
    assert by_id["sefm-ssc7-umple"]["status"] == "partial"
    assert by_id["sefm-ssc7-umple"]["conversion_source"] == "official_scxml"
    assert by_id["llms-emp-deepseek-microwave"]["status"] == "converted"
    assert by_id["llms-emp-deepseek-microwave"]["conversion_source"] == "official_scxml"
    assert by_id["llms-emp-deepseek-microwave"]["canonical_output_path"]
    microwave_codes = {d["code"] for d in by_id["llms-emp-deepseek-microwave"]["diagnostics"]}
    assert "R3.R31.NORMALIZED_SCXML_REPLAY_USED" in microwave_codes
    assert all("tool_preflight" in item for item in report["items"])
    for example_id, item in by_id.items():
        selected = (
            "project_1_llm_state_machine_modeling/paper_stm_issue_discover/"
            f"pipeline/conversion/fixtures/r3_selected_seed_examples/{example_id}"
        )
        assert item["source_nl_path"] == f"{selected}/nl.txt"
        assert item["source_stm0_path"].startswith(f"{selected}/stm0.")
        assert item["source_meta_path"] == f"{selected}/source_meta.json"
        assert item["canonical_output_path"]


def test_cli_fails_loudly_when_required_toolchains_missing(tmp_path):
    out = tmp_path / "reports"
    cmd = [
        sys.executable,
        "-m",
        "paper_stm_conversion.cli",
        "convert-selected",
        "--reports-dir",
        str(out),
        "--run-id",
        "pytest-r3-missing-tools",
    ]
    empty_path = tmp_path / "empty-path"
    empty_path.mkdir()
    env = {**os.environ, "PYTHONPATH": str(SRC), "PATH": str(empty_path)}
    for key in ("PLANTUML_JAR", "PLANTUML_PATH", "UMPLE_JAR", "UMPLE_PATH"):
        env.pop(key, None)
    completed = subprocess.run(cmd, cwd=REPO, env=env, text=True, capture_output=True, check=False)
    assert completed.returncode != 0
    err = completed.stderr + completed.stdout
    assert "R3 conversion toolchain setup failed" in err
    assert "PlantUML" in err
    assert "静默退回 regex/string/source-text parser" in err
    assert "不允许复用已提交 SCXML fixture" in err
    assert "PLANTUML_JAR" in err


def test_cli_fails_loudly_when_configured_plantuml_path_is_invalid(tmp_path):
    out = tmp_path / "reports"
    cmd = [
        sys.executable,
        "-m",
        "paper_stm_conversion.cli",
        "convert-selected",
        "--reports-dir",
        str(out),
        "--run-id",
        "pytest-r3-invalid-plantuml-path",
    ]
    env = {**_fake_toolchain_env(tmp_path)}
    env["PLANTUML_JAR"] = str(tmp_path / "missing-plantuml.jar")
    completed = subprocess.run(cmd, cwd=REPO, env=env, text=True, capture_output=True, check=False)
    assert completed.returncode != 0
    err = completed.stderr + completed.stdout
    assert "PlantUML 已通过环境变量配置，但路径无效" in err
    assert "PLANTUML_JAR" in err
    assert "missing-plantuml.jar" in err
    assert "下载官方 plantuml.jar" in err


def test_committed_report_keeps_r3_smoke_boundary_and_losses():
    report = json.loads((REPORTS / "selected_seed_examples_conversion_report.json").read_text(encoding="utf-8"))
    by_id = {item["example_id"]: item for item in report["items"]}
    assert set(by_id) == {
        "llms-emp-deepseek-microwave",
        "llms-emp-gpt4o-hldcs",
        "llms-emp-kimi-autonomous-collision",
        "sefm-ssc7-umple",
    }
    assert all(item["eligibility"] == "r3_smoke_fixture_only_not_main_experiment" for item in report["items"])
    for example_id, item in by_id.items():
        selected = (
            "project_1_llm_state_machine_modeling/paper_stm_issue_discover/"
            f"pipeline/conversion/fixtures/r3_selected_seed_examples/{example_id}"
        )
        assert item["source_nl_path"] == f"{selected}/nl.txt"
        assert item["source_stm0_path"].startswith(f"{selected}/stm0.")
        assert item["source_meta_path"] == f"{selected}/source_meta.json"
        assert (REPO / item["source_nl_path"]).exists()
        assert (REPO / item["source_stm0_path"]).exists()
        assert (REPO / item["source_meta_path"]).exists()
    assert by_id["llms-emp-gpt4o-hldcs"]["status"] == "converted"
    assert by_id["llms-emp-gpt4o-hldcs"]["hierarchy_level"] == "hierarchical"
    assert by_id["llms-emp-kimi-autonomous-collision"]["status"] == "converted"
    assert by_id["llms-emp-kimi-autonomous-collision"]["hierarchy_level"] == "hierarchical"
    assert by_id["sefm-ssc7-umple"]["timing_level"] == "qualitative"
    assert by_id["llms-emp-deepseek-microwave"]["status"] == "converted"
    assert by_id["llms-emp-deepseek-microwave"]["hierarchy_level"] == "hierarchical"
    assert by_id["llms-emp-deepseek-microwave"]["states_count"] == 17
    assert by_id["llms-emp-deepseek-microwave"]["transitions_count"] == 20
    assert by_id["llms-emp-deepseek-microwave"]["conversion_source"] == "official_scxml"
    assert by_id["llms-emp-deepseek-microwave"]["canonical_output_path"]
    losses = (REPORTS / "selected_seed_examples_loss_ledger.jsonl").read_text(encoding="utf-8")
    assert "sefm-ssc7-umple:umple:timing_after" in losses
    assert "llms-emp-deepseek-microwave:plantuml:official_preflight_failed" not in losses


def test_committed_reports_do_not_embed_local_absolute_paths():
    for path in [
        REPORTS / "selected_seed_examples_conversion_report.json",
        REPORTS / "selected_seed_examples_input_audit.json",
        REPORTS / "selected_seed_examples_loss_ledger.jsonl",
        REPORTS / "selected_seed_examples_summary.md",
        REPORTS / "unified_uml_plantuml_candidate_probe.json",
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

    kimi = json.loads((REPORTS / "canonical" / "llms-emp-kimi-autonomous-collision.canonical_stm.json").read_text(encoding="utf-8"))
    assert kimi["metadata"]["conversion_source"] == "official_scxml"
    assert kimi["metadata"]["fallback_used"] is False
    assert kimi["metadata"]["source_text_used_for_canonical"] is False
    assert all("stm0.scxml:" in s["raw_ref"] for s in kimi["model"]["states"])
    assert all("stm0.scxml:" in t["raw_ref"] for t in kimi["model"]["transitions"])
    assert any(d["code"] == "R3.STRUCTURED_EXPORT.CANONICAL_FROM_SCXML" for d in kimi["diagnostics"])

    umple = json.loads((REPORTS / "canonical" / "sefm-ssc7-umple.canonical_stm.json").read_text(encoding="utf-8"))
    assert umple["metadata"]["conversion_source"] == "official_scxml"
    assert umple["metadata"]["fallback_used"] is False
    assert umple["metadata"]["targeted_audit_used"] is True
    assert "raw Umple timing token audit" in umple["metadata"]["targeted_audit_scope"]
    assert all("stm0.scxml:" in s["raw_ref"] for s in umple["model"]["states"])
    assert all("stm0.scxml:" in t["raw_ref"] for t in umple["model"]["transitions"])
    assert any(d["code"] == "R3.UMPLE.TIMING_RAW_AUDIT" for d in umple["diagnostics"])
    assert any(t.get("event") == "timeoutTimeoutToReady" for t in umple["model"]["transitions"])


def test_microwave_uses_r31_normalized_scxml_replay_without_source_text_fallback():
    microwave_path = REPORTS / "canonical" / "llms-emp-deepseek-microwave.canonical_stm.json"
    assert microwave_path.exists()
    microwave = json.loads(microwave_path.read_text(encoding="utf-8"))
    assert microwave["status"] == "converted"
    assert microwave["metadata"]["conversion_source"] == "official_scxml"
    assert microwave["metadata"]["fallback_used"] is False
    assert microwave["metadata"]["r3_1_normalization_replay_used"] is True
    assert microwave["metadata"]["source_text_used_for_canonical"] is False
    assert "stm0.r3_1_normalized.scxml" in microwave["metadata"]["structured_export_path"]
    assert all("stm0.r3_1_normalized.scxml:" in s["raw_ref"] for s in microwave["model"]["states"])
    assert all("stm0.r3_1_normalized.scxml:" in t["raw_ref"] for t in microwave["model"]["transitions"])
    assert len(microwave["model"]["states"]) == 17
    assert len(microwave["model"]["transitions"]) == 20
    codes = {d["code"] for d in microwave["diagnostics"]}
    assert "R3.STRUCTURED_EXPORT.CANONICAL_FROM_SCXML" in codes
    assert "R3.R31.NORMALIZED_SCXML_REPLAY_USED" in codes


def test_canonical_outputs_never_use_text_fallback_conversion_source():
    canonical_dir = REPORTS / "canonical"
    names = {p.name for p in canonical_dir.glob("*.canonical_stm.json")}
    assert names == {
        "llms-emp-gpt4o-hldcs.canonical_stm.json",
        "llms-emp-kimi-autonomous-collision.canonical_stm.json",
        "sefm-ssc7-umple.canonical_stm.json",
        "llms-emp-deepseek-microwave.canonical_stm.json",
    }
    for path in canonical_dir.glob("*.canonical_stm.json"):
        doc = json.loads(path.read_text(encoding="utf-8"))
        assert doc["metadata"]["conversion_source"] == "official_scxml"
        assert doc["metadata"]["conversion_source"] != "fallback_text_probe"
        assert doc["metadata"].get("source_text_used_for_canonical") is False


def test_input_audit_records_source_pair_hashes_and_documented_divergence():
    audit = json.loads((REPORTS / "selected_seed_examples_input_audit.json").read_text(encoding="utf-8"))
    by_id = {row["example_id"]: row for row in audit["items"]}
    assert all(row["source_hash_divergence_documented"] for row in audit["items"])
    assert by_id["llms-emp-deepseek-microwave"]["source_nl_hash_match"] is False
    assert by_id["llms-emp-deepseek-microwave"]["source_nl_hash_divergence_documented"] is True
    assert by_id["llms-emp-kimi-autonomous-collision"]["source_nl_hash_match"] is False
    assert by_id["llms-emp-kimi-autonomous-collision"]["source_nl_hash_divergence_documented"] is True
    assert by_id["sefm-ssc7-umple"]["source_nl_hash_match"] is True
    assert by_id["sefm-ssc7-umple"]["source_stm0_hash_match"] is False
    assert by_id["sefm-ssc7-umple"]["source_stm0_hash_divergence_documented"] is True
    for example_id in ["llms-emp-deepseek-microwave", "llms-emp-kimi-autonomous-collision", "sefm-ssc7-umple"]:
        assert "whitespace normalization" in by_id[example_id]["hash_scope"]


def test_committed_report_contains_only_current_selected_examples():
    report = json.loads((REPORTS / "selected_seed_examples_conversion_report.json").read_text(encoding="utf-8"))
    by_id = {item["example_id"]: item for item in report["items"]}
    assert set(by_id) == {
        "llms-emp-deepseek-microwave",
        "llms-emp-gpt4o-hldcs",
        "llms-emp-kimi-autonomous-collision",
        "sefm-ssc7-umple",
    }


def test_committed_report_records_official_toolchain_preflight():
    report = json.loads((REPORTS / "selected_seed_examples_conversion_report.json").read_text(encoding="utf-8"))
    by_id = {item["example_id"]: item for item in report["items"]}

    llms = by_id["llms-emp-gpt4o-hldcs"]["tool_preflight"]
    assert llms["tool_name"] == "PlantUML CLI"
    assert llms["syntax_status"] == "ok"
    assert llms["structured_export_status"] == "scxml_export_ok"
    assert llms["structured_export_path"].endswith("toolchain_exports/llms-emp-gpt4o-hldcs/stm0.scxml")
    assert (REPO / llms["structured_export_path"]).exists()

    kimi = by_id["llms-emp-kimi-autonomous-collision"]["tool_preflight"]
    assert kimi["tool_name"] == "PlantUML CLI"
    assert kimi["syntax_status"] == "ok"
    assert kimi["structured_export_status"] == "scxml_export_ok"
    assert kimi["structured_export_path"].endswith("toolchain_exports/llms-emp-kimi-autonomous-collision/stm0.scxml")
    assert (REPO / kimi["structured_export_path"]).exists()

    microwave = by_id["llms-emp-deepseek-microwave"]["tool_preflight"]
    assert microwave["tool_name"] == "PlantUML CLI"
    assert microwave["syntax_status"] == "ok"
    assert microwave["structured_export_status"] == "scxml_export_ok"
    assert microwave["tool_invocation_status"] == "official_cli_syntax_and_scxml_ok_after_r3_1_normalization_replay"
    assert microwave["structured_export_path"].endswith("toolchain_exports/llms-emp-deepseek-microwave/stm0.r3_1_normalized.scxml")
    assert (REPO / microwave["structured_export_path"]).exists()
    assert microwave["evidence"]["r3_1_normalization_replay"] is True
    raw = microwave["evidence"]["r3_1_original_raw_preflight"]
    assert raw["syntax_status"] == "failed"
    assert raw["structured_export_status"] == "scxml_not_trusted_after_syntax_failure"
    assert "静默退回 regex/string/source-text parser" in raw["fallback_reason"]
    assert by_id["llms-emp-deepseek-microwave"]["status"] == "converted"

    sefm = by_id["sefm-ssc7-umple"]["tool_preflight"]
    assert sefm["tool_name"] == "Umple compiler CLI"
    assert sefm["syntax_status"] == "ok"
    assert sefm["structured_export_status"] == "scxml_export_ok"
    assert sefm["structured_export_path"].endswith("toolchain_exports/sefm-ssc7-umple/stm0.scxml")
    assert (REPO / sefm["structured_export_path"]).exists()
    assert by_id["sefm-ssc7-umple"]["conversion_source"] == "official_scxml"


def test_cli_invokes_configured_external_toolchains(tmp_path):
    out = tmp_path / "reports"
    cmd = [
        sys.executable,
        "-m",
        "paper_stm_conversion.cli",
        "convert-selected",
        "--reports-dir",
        str(out),
        "--run-id",
        "pytest-r3-toolchain",
    ]
    plant_log = tmp_path / "plantuml_calls.log"
    umple_log = tmp_path / "umple_calls.log"
    env = {
        **_fake_toolchain_env(tmp_path),
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


def test_unified_uml_candidate_probe_is_historical_not_current_smoke():
    probe_path = REPORTS / "unified_uml_plantuml_candidate_probe.json"
    probe = json.loads(probe_path.read_text(encoding="utf-8"))
    assert probe["report_version"] == "r3.unified_uml_plantuml_candidate_probe.v0"
    assert probe["probe_scope"].startswith("first 80 JSONL rows only")
    assert probe["summary"]["rows_checked"] == 80
    assert probe["summary"]["candidate_scxml_ok"] == 40
    first = probe["summary"]["earliest_candidates"][0]
    assert first["row"] == 3
    assert first["pair_id"] == "unified_uml_state_train_0003"
    assert first["scxml_bytes"] > 0
    assert "unified-uml-synthetic-0000" not in {item["example_id"] for item in json.loads((REPORTS / "selected_seed_examples_conversion_report.json").read_text(encoding="utf-8"))["items"]}
