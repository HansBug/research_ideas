from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SRC = ROOT / "src"
REPORTS = ROOT / "reports"
CONVERSION_CANONICAL = REPO / "project_1_llm_state_machine_modeling/paper_stm_repair/conversion/reports/canonical"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_cli_regenerates_export_reports_in_tmp_path(tmp_path):
    out = tmp_path / "r45"
    cmd = [
        sys.executable,
        "-m",
        "paper_stm_repair_representation.cli",
        "export-selected",
        "--reports-dir",
        str(out),
    ]
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    completed = subprocess.run(cmd, cwd=REPO, env=env, text=True, capture_output=True, check=True)
    assert '"examples": 4' in completed.stdout
    report = load_json(out / "fcstm_export_report.json")
    by_id = {item["example_id"]: item for item in report["items"]}
    assert by_id["llms-emp-gpt4o-hldcs"]["status"] == "converted"
    assert by_id["llms-emp-gpt4o-hldcs"]["parse_status"] == "ok"
    assert by_id["sefm-ssc7-umple"]["status"] == "converted"
    assert by_id["sefm-ssc7-umple"]["parse_status"] == "ok"
    assert by_id["ttool-automatedbraking-xml"]["status"] == "blocked"
    assert by_id["ttool-automatedbraking-xml"]["fcstm_path"] is None
    assert by_id["unified-uml-synthetic-0000"]["status"] == "blocked"
    assert by_id["unified-uml-synthetic-0000"]["fcstm_path"] is None


def test_llms_hierarchy_and_composite_initials_are_preserved():
    parse_report = load_json(REPORTS / "fcstm_exports/llms-emp-gpt4o-hldcs/parse_inspect_report.json")
    assert parse_report["parse_status"] == "ok"
    assert parse_report["inspect_status"] == "ok"
    states = {state["path"]: state for state in parse_report["states"]}
    assert states["llms_emp_gpt4o_hldcs.start"]["is_pseudo"] is True
    assert states["llms_emp_gpt4o_hldcs.HumanDriving.startHumanDriving"]["is_pseudo"] is True
    assert states["llms_emp_gpt4o_hldcs.HumanDriving.Autonomous.startAutonomous"]["is_pseudo"] is True
    assert "llms_emp_gpt4o_hldcs.HumanDriving" in states
    assert "llms_emp_gpt4o_hldcs.HumanDriving.Autonomous" in states
    root_initial = states["llms_emp_gpt4o_hldcs"]["initial_targets"]
    human_initial = states["llms_emp_gpt4o_hldcs.HumanDriving"]["initial_targets"]
    auto_initial = states["llms_emp_gpt4o_hldcs.HumanDriving.Autonomous"]["initial_targets"]
    assert root_initial[0]["target"] == "llms_emp_gpt4o_hldcs.start"
    assert human_initial[0]["target"] == "llms_emp_gpt4o_hldcs.HumanDriving.startHumanDriving"
    assert auto_initial[0]["target"] == "llms_emp_gpt4o_hldcs.HumanDriving.Autonomous.startAutonomous"


def test_sefm_event_guard_transitions_use_pseudo_relay_not_event_flags():
    fcstm = (REPORTS / "fcstm_exports/sefm-ssc7-umple/model.fcstm").read_text(encoding="utf-8")
    assert "pseudo state ready_scan_barcode_is_valid_barcode_security_check_relay" in fcstm
    assert "Ready -> ready_scan_barcode_is_valid_barcode_security_check_relay : scanBarcode;" in fcstm
    assert "ready_scan_barcode_is_valid_barcode_security_check_relay -> SecurityCheck : if [isValidBarcode > 0];" in fcstm
    assert "ev_scanBarcode" not in fcstm
    assert "scanBarcode : if" not in fcstm
    parse_report = load_json(REPORTS / "fcstm_exports/sefm-ssc7-umple/parse_inspect_report.json")
    assert parse_report["metrics"]["n_states_pseudo"] >= 7


def test_name_mapping_covers_required_emitted_identifier_types():
    sefm = load_json(REPORTS / "fcstm_exports/sefm-ssc7-umple/name_mapping.json")
    llms = load_json(REPORTS / "fcstm_exports/llms-emp-gpt4o-hldcs/name_mapping.json")
    object_types = {item["object_type"] for item in sefm["items"] + llms["items"]}
    assert {"root_state", "state", "event", "pseudo_relay", "guard_variable", "action_flag", "abstract_action"} <= object_types
    assert any(item["raw_text"] == "Front Distance > 10" and item["emitted_identifier"] == "Front_Distance_10" for item in llms["items"])
    assert any(item["raw_text"] == "showError()" and item["object_type"] == "action_flag" for item in sefm["items"])


def test_lowering_inventory_counts_align_with_r3_canonical_for_converted_examples():
    for example_id in ["llms-emp-gpt4o-hldcs", "sefm-ssc7-umple"]:
        canonical = load_json(CONVERSION_CANONICAL / f"{example_id}.canonical_stm.json")
        inv = load_json(REPORTS / f"fcstm_exports/{example_id}/lowering_inventory.json")
        assert inv["counts"]["canonical_states"] == len(canonical["model"]["states"])
        assert inv["counts"]["canonical_transitions"] == len(canonical["model"]["transitions"])
        assert inv["counts"]["references"] == len(canonical["model"]["transitions"])
        assert inv["counts"]["hierarchy_items"] == len(canonical["model"]["states"])


def test_blocked_examples_do_not_emit_fake_fcstm_models():
    report = load_json(REPORTS / "fcstm_export_report.json")
    by_id = {item["example_id"]: item for item in report["items"]}
    for example_id in ["ttool-automatedbraking-xml", "unified-uml-synthetic-0000"]:
        assert by_id[example_id]["status"] == "blocked"
        assert by_id[example_id]["fcstm_path"] is None
        assert not (REPORTS / f"fcstm_exports/{example_id}/model.fcstm").exists()
        inv = load_json(REPORTS / f"fcstm_exports/{example_id}/lowering_inventory.json")
        assert inv["blocked_supplementary"]


def test_committed_reports_do_not_embed_local_absolute_paths():
    for path in sorted(REPORTS.glob("**/*")):
        if path.is_file() and path.suffix in {".json", ".jsonl", ".fcstm", ".md"}:
            text = path.read_text(encoding="utf-8")
            assert "/" + "home/" not in text
            assert "/" + "tmp/" not in text


def test_guard_variable_uses_fcstm_safe_identifier_for_special_token():
    from paper_stm_repair_representation.lowering import FCSTMExporter, inspect_fcstm

    canonical = {
        "schema_version": "r3.canonical_stm.v0",
        "example_id": "mini-e-guard",
        "seed_id": "mini",
        "source_format": "plantuml",
        "adapter": "plantuml",
        "status": "converted",
        "status_reason_code": "R3.STATUS.converted",
        "metadata": {"conversion_source": "official_scxml"},
        "diagnostics": [],
        "model": {
            "name": "Mini",
            "states": [
                {"id": "A", "label": "A", "kind": "state", "parent": None, "raw_ref": "raw:A", "attributes": {}},
                {"id": "B", "label": "B", "kind": "state", "parent": None, "raw_ref": "raw:B", "attributes": {}},
            ],
            "transitions": [
                {"id": "tr_0001", "source": "A", "target": "B", "event": "E", "guard": "E", "action": None, "label": "E [E]", "scope": None, "raw_ref": "raw:t1", "attributes": {}},
            ],
            "variables": [],
            "initial_states": ["A"],
            "final_states": [],
            "timing_level": "none",
            "hierarchy_level": "flat",
        },
    }
    result = FCSTMExporter(canonical).export()
    fcstm = result["fcstm"]
    assert "def int E_ = 0;" in fcstm
    assert "if [E_ > 0]" in fcstm
    assert "def int E = 0;" not in fcstm
    assert inspect_fcstm(fcstm, Path("mini.fcstm"))["parse_status"] == "ok"
