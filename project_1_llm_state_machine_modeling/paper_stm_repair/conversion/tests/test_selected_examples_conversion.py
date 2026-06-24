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
    statuses = {item["example_id"]: item["status"] for item in report["items"]}
    assert statuses["llms-emp-gpt4o-hldcs"] == "converted"
    assert statuses["unified-uml-synthetic-0000"] == "converted"
    assert statuses["sefm-ssc7-umple"] == "partial"
    assert statuses["ttool-automatedbraking-xml"] == "partial"


def test_committed_report_keeps_r3_smoke_boundary_and_losses():
    report = json.loads((REPORTS / "selected_seed_examples_conversion_report.json").read_text(encoding="utf-8"))
    by_id = {item["example_id"]: item for item in report["items"]}
    assert all(item["eligibility"] == "r3_smoke_fixture_only_not_main_experiment" for item in report["items"])
    assert by_id["llms-emp-gpt4o-hldcs"]["hierarchy_level"] == "hierarchical"
    assert by_id["unified-uml-synthetic-0000"]["hierarchy_level"] == "flat"
    assert by_id["sefm-ssc7-umple"]["timing_level"] == "qualitative"
    assert by_id["ttool-automatedbraking-xml"]["timing_level"] == "timed_constraints"
    losses = (REPORTS / "selected_seed_examples_loss_ledger.jsonl").read_text(encoding="utf-8")
    assert "sefm-ssc7-umple:umple:timing_after" in losses
    assert "ttool-automatedbraking-xml:ttool_xml:unresolved_connectors" in losses


def test_committed_reports_do_not_embed_local_absolute_paths():
    for path in [
        REPORTS / "selected_seed_examples_conversion_report.json",
        REPORTS / "selected_seed_examples_input_audit.json",
        REPORTS / "selected_seed_examples_loss_ledger.jsonl",
    ]:
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text



def test_plantuml_label_split_handles_guard_action_combo():
    from paper_stm_repair_conversion.adapters.plantuml import _split_label

    assert _split_label("evt [g] / doIt()") == ("evt", "g", "doIt()")
    assert _split_label("[g] / doIt()") == (None, "g", "doIt()")


def test_committed_outputs_link_state_body_and_timing_losses():
    plant = json.loads((REPORTS / "canonical" / "llms-emp-gpt4o-hldcs.canonical_stm.json").read_text(encoding="utf-8"))
    assert any(d["code"] == "R3.PUML.STATE_BODY_PRESERVED" for d in plant["diagnostics"])
    assert any(s["attributes"].get("plantuml_state_body_lines") for s in plant["model"]["states"])

    umple = json.loads((REPORTS / "canonical" / "sefm-ssc7-umple.canonical_stm.json").read_text(encoding="utf-8"))
    timing = [t for t in umple["model"]["transitions"] if t.get("event") == "after(60)"]
    assert timing and timing[0]["attributes"]["timing_loss_ref"] == "sefm-ssc7-umple:umple:timing_after"
    assert any(d["code"] == "R3.UMPLE.TIMING_TRANSITION_PARTIAL" for d in umple["diagnostics"])


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
