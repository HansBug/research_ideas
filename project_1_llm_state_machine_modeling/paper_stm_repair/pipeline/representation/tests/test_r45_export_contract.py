from __future__ import annotations

import json
import os
import hashlib
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
SRC = ROOT / "src"
REPORTS = ROOT / "reports"
CONVERSION_CANONICAL = REPO / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/reports/canonical"
SELECTED = REPO / "project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    assert report["summary"] == {"examples": 4, "converted": 4, "partial": 0, "blocked": 0}
    by_id = {item["example_id"]: item for item in report["items"]}
    assert set(by_id) == {
        "llms-emp-deepseek-microwave",
        "llms-emp-gpt4o-hldcs",
        "llms-emp-kimi-autonomous-collision",
        "sefm-ssc7-umple",
    }
    for example_id in by_id:
        assert by_id[example_id]["status"] == "converted"
        assert by_id[example_id]["parse_status"] == "ok"
        assert by_id[example_id]["fcstm_path"] is not None


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
    kimi = load_json(REPORTS / "fcstm_exports/llms-emp-kimi-autonomous-collision/name_mapping.json")
    microwave = load_json(REPORTS / "fcstm_exports/llms-emp-deepseek-microwave/name_mapping.json")
    object_types = {item["object_type"] for item in sefm["items"] + llms["items"] + kimi["items"] + microwave["items"]}
    assert {"root_state", "state", "event", "pseudo_relay", "guard_variable", "action_flag"} <= object_types
    assert "abstract_action" not in object_types
    assert any(item["raw_text"] == "Front Distance > 10" and item["emitted_identifier"] == "Front_Distance_10" for item in llms["items"])
    assert any(item["raw_text"] == "showError()" and item["object_type"] == "action_flag" for item in sefm["items"])
    assert any(item["raw_text"] == "AutonomousMode" and item["object_type"] == "state" for item in kimi["items"])
    assert any(item["raw_text"] == "DoorShutWithItem" and item["object_type"] == "state" for item in microwave["items"])
    assert any(item["raw_text"] == "Cooking Time Entered" and item["object_type"] == "event" for item in microwave["items"])


def test_lowering_inventory_counts_align_with_r3_canonical_for_converted_examples():
    for example_id in [
        "llms-emp-deepseek-microwave",
        "llms-emp-gpt4o-hldcs",
        "llms-emp-kimi-autonomous-collision",
        "sefm-ssc7-umple",
    ]:
        canonical = load_json(CONVERSION_CANONICAL / f"{example_id}.canonical_stm.json")
        inv = load_json(REPORTS / f"fcstm_exports/{example_id}/lowering_inventory.json")
        assert inv["counts"]["canonical_states"] == len(canonical["model"]["states"])
        assert inv["counts"]["canonical_transitions"] == len(canonical["model"]["transitions"])
        assert inv["counts"]["references"] == len(canonical["model"]["transitions"])
        assert inv["counts"]["hierarchy_items"] == len(canonical["model"]["states"])


def test_all_selected_examples_emit_parseable_fcstm_models_without_repair_credit():
    report = load_json(REPORTS / "fcstm_export_report.json")
    by_id = {item["example_id"]: item for item in report["items"]}
    assert report["summary"] == {"examples": 4, "converted": 4, "partial": 0, "blocked": 0}
    for example_id in by_id:
        assert by_id[example_id]["status"] == "converted"
        assert by_id[example_id]["parse_status"] == "ok"
        assert by_id[example_id]["repair_contribution_allowed"] is False
        assert (REPORTS / f"fcstm_exports/{example_id}/model.fcstm").exists()
        inv = load_json(REPORTS / f"fcstm_exports/{example_id}/lowering_inventory.json")
        assert inv["blocked_supplementary"] == []


def test_r45_report_keeps_upstream_nl_and_raw_stm_traceability():
    report = load_json(REPORTS / "fcstm_export_report.json")
    for item in report["items"]:
        assert item["upstream_source_nl_path"] == item["source_nl_path"]
        assert item["upstream_source_stm0_path"] == item["source_stm0_path"]
        assert item["upstream_source_meta_path"] == item["source_meta_path"]
        assert item["upstream_r3_status"] in {"converted", "partial"}
        assert item["upstream_source_format"] in {"plantuml", "umple"}
        assert (REPO / item["source_nl_path"]).is_file()
        assert (REPO / item["source_stm0_path"]).is_file()
        assert (REPO / item["source_meta_path"]).is_file()
        assert (REPO / item["canonical_output_path"]).is_file()
        inv = load_json(REPORTS / f"fcstm_exports/{item['example_id']}/lowering_inventory.json")
        trace = inv["source_traceability"]
        assert trace["source_nl_path"] == item["source_nl_path"]
        assert trace["source_stm0_path"] == item["source_stm0_path"]
        assert trace["source_meta_path"] == item["source_meta_path"]
        assert trace["canonical_output_path"] == item["canonical_output_path"]
        assert trace["upstream_r3_status"] == item["upstream_r3_status"]
        assert trace["repair_contribution_allowed"] is False


def test_kimi_condition_like_labels_are_loss_ledgered_as_events_not_guards():
    losses = [
        json.loads(line)
        for line in (REPORTS / "fcstm_export_loss_ledger.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    condition_losses = [
        row
        for row in losses
        if row["example_id"] == "llms-emp-kimi-autonomous-collision"
        and row["reason_code"] == "R45.LOSS.condition_like_label_lowered_as_event"
    ]
    assert len(condition_losses) >= 10
    assert any("dist_to_front<25" in row["extra"]["raw_event"] for row in condition_losses)
    assert all(row["extra"]["guard_field"] is None for row in condition_losses)
    assert all(row["repair_contribution_allowed"] is False for row in condition_losses)


def test_microwave_fcstm_is_from_r31_replay_canonical_and_not_repair_gain():
    canonical = load_json(CONVERSION_CANONICAL / "llms-emp-deepseek-microwave.canonical_stm.json")
    assert canonical["metadata"]["r3_1_normalization_replay_used"] is True
    assert canonical["metadata"]["source_text_used_for_canonical"] is False
    assert any(d["code"] == "R3.R31.NORMALIZED_SCXML_REPLAY_USED" for d in canonical["diagnostics"])
    parse_report = load_json(REPORTS / "fcstm_exports/llms-emp-deepseek-microwave/parse_inspect_report.json")
    assert parse_report["parse_status"] == "ok"
    states = {state["path"]: state for state in parse_report["states"]}
    assert "llms_emp_deepseek_microwave.DoorShut" in states
    assert "llms_emp_deepseek_microwave.DoorShut.DoorOpen.DoorOpenWithItem" in states
    assert "llms_emp_deepseek_microwave.DoorShut.DoorOpen.ReadytoCook.Cooking.CookingIdle" in states
    report = load_json(REPORTS / "fcstm_export_report.json")
    microwave = {item["example_id"]: item for item in report["items"]}["llms-emp-deepseek-microwave"]
    assert microwave["status"] == "converted"
    assert microwave["repair_contribution_allowed"] is False


def test_committed_reports_do_not_embed_local_absolute_paths():
    for path in sorted(REPORTS.glob("**/*")):
        if path.is_file() and path.suffix in {".json", ".jsonl", ".fcstm", ".md"}:
            text = path.read_text(encoding="utf-8")
            assert "/" + "home/" not in text
            assert "/" + "tmp/" not in text


def test_inspect_fcstm_diagnostics_preserve_nested_spans_as_json_safe_schema():
    from paper_stm_repair_representation.lowering import inspect_fcstm

    source = """def int counter = 0;
state Root {
    state Idle;
    state Done;
    [*] -> Idle;
}
"""
    report = inspect_fcstm(source, Path("mini-span.fcstm"))

    assert report["parse_status"] == "ok"
    assert report["inspect_status"] == "ok"
    json.dumps(report)
    diagnostics = report["diagnostics"]
    assert diagnostics
    unreachable = next(
        diagnostic
        for diagnostic in diagnostics
        if diagnostic["code"] == "W_UNREACHABLE_STATE"
    )
    assert set(unreachable) >= {"code", "severity", "message", "span", "refs"}
    assert unreachable["span"] == {
        "line": 4,
        "column": 5,
        "end_line": 4,
        "end_column": 16,
    }
    assert unreachable["refs"] == {"state_path": "Root.Done"}

    deadlock = next(
        diagnostic
        for diagnostic in diagnostics
        if diagnostic["code"] == "W_DEADLOCK_LEAF"
    )
    assert deadlock["span"]["line"] == 3
    assert deadlock["refs"]["suggested_fix"]["anchor"] == {
        "type": "ref",
        "ref": "refs.parent_path",
    }


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


def test_cli_syncs_selected_seed_example_fcstm_snapshots_in_tmp_path(tmp_path):
    reports_out = tmp_path / "reports"
    selected_out = tmp_path / "selected"
    cmd_export = [
        sys.executable,
        "-m",
        "paper_stm_repair_representation.cli",
        "export-selected",
        "--reports-dir",
        str(reports_out),
    ]
    cmd_sync = [
        sys.executable,
        "-m",
        "paper_stm_repair_representation.cli",
        "sync-selected-fcstm",
        "--reports-dir",
        str(reports_out),
        "--selected-dir",
        str(selected_out),
    ]
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    subprocess.run(cmd_export, cwd=REPO, env=env, text=True, capture_output=True, check=True)
    completed = subprocess.run(cmd_sync, cwd=REPO, env=env, text=True, capture_output=True, check=True)
    assert '"synced": 4' in completed.stdout
    for example_id in [
        "llms-emp-deepseek-microwave",
        "llms-emp-gpt4o-hldcs",
        "llms-emp-kimi-autonomous-collision",
        "sefm-ssc7-umple",
    ]:
        selected_fcstm = selected_out / example_id / "model.fcstm"
        meta = load_json(selected_out / example_id / "fcstm_meta.json")
        report_fcstm = reports_out / "fcstm_exports" / example_id / "model.fcstm"
        assert selected_fcstm.read_text(encoding="utf-8") == report_fcstm.read_text(encoding="utf-8")
        assert meta["selected_fcstm_sha256"] == sha256(selected_fcstm)
        assert meta["synchronized_from_fcstm_sha256"] == sha256(report_fcstm)
        assert meta["selected_fcstm_sha256"] == meta["synchronized_from_fcstm_sha256"]
        assert meta["parse_status"] == "ok"
        assert meta["inspect_status"] == "ok"
        assert meta["repair_contribution_allowed"] is False


def test_committed_selected_seed_examples_include_synced_fcstm_snapshots():
    report = load_json(REPORTS / "fcstm_export_report.json")
    by_id = {item["example_id"]: item for item in report["items"]}
    assert set(by_id) == {
        "llms-emp-deepseek-microwave",
        "llms-emp-gpt4o-hldcs",
        "llms-emp-kimi-autonomous-collision",
        "sefm-ssc7-umple",
    }
    for example_id, item in by_id.items():
        selected_dir = SELECTED / example_id
        selected_fcstm = selected_dir / "model.fcstm"
        selected_meta = selected_dir / "fcstm_meta.json"
        source_fcstm = REPO / item["fcstm_path"]
        meta = load_json(selected_meta)
        assert selected_fcstm.is_file()
        assert selected_meta.is_file()
        assert selected_fcstm.read_text(encoding="utf-8") == source_fcstm.read_text(encoding="utf-8")
        assert meta["schema_version"] == "selected_seed_examples.fcstm_snapshot.v0"
        assert meta["artifact_role"] == "r4_5_smoke_converted_fcstm_snapshot"
        assert meta["selected_fcstm_path"] == f"project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples/{example_id}/model.fcstm"
        assert meta["selected_fcstm_sha256"] == sha256(selected_fcstm)
        assert meta["synchronized_from_fcstm_path"] == item["fcstm_path"]
        assert meta["synchronized_from_fcstm_sha256"] == sha256(source_fcstm)
        assert meta["selected_fcstm_sha256"] == meta["synchronized_from_fcstm_sha256"]
        direct_item_keys = {
            "source_nl_path",
            "source_stm0_path",
            "source_meta_path",
            "canonical_output_path",
            "lowering_inventory_path",
            "name_mapping_path",
            "parse_inspect_report_path",
        }
        for key in direct_item_keys:
            assert meta[key] == item[key]
            assert (REPO / meta[key]).exists(), (example_id, key, meta[key])
        assert meta["parse_status"] == item["parse_status"] == "ok"
        assert meta["inspect_status"] == item["inspect_status"] == "ok"
        assert meta["repair_contribution_allowed"] is False
        assert meta["attribution"] == "representation_lowering_not_repair"
        from paper_stm_repair_representation.lowering import inspect_fcstm

        assert inspect_fcstm(selected_fcstm.read_text(encoding="utf-8"), selected_fcstm)["parse_status"] == "ok"



def test_r574_adjudication_baseline_bundles_are_cold_archived_not_active():
    active_index = REPORTS / "r5_7_4_adjudication_baseline_bundles/bundle_index.json"
    active_exports = REPORTS / "r5_7_4_adjudication_fcstm_exports"
    archive_root = REPO / "project_1_llm_state_machine_modeling/paper_stm_repair/archive/r5_7_better_stm_snapshot/pipeline/representation/reports"
    archived_index = archive_root / "r5_7_4_adjudication_baseline_bundles/bundle_index.json"
    archived_exports = archive_root / "r5_7_4_adjudication_fcstm_exports"

    assert not active_index.exists()
    assert not active_exports.exists()
    assert archived_index.is_file()
    assert archived_exports.is_dir()

    index = load_json(archived_index)
    assert index["schema_version"] == "r5_7_4.adjudication_baseline_bundle_index.v0"
    by_pair = {item["pair_id"]: item for item in index["items"]}
    assert set(by_pair) == {
        "llms_emp_stm_results_0000",
        "llms_emp_stm_results_0001",
        "llms_emp_stm_results_0018",
        "llms_emp_stm_results_0045",
    }
    for item in by_pair.values():
        assert item["repair_contribution_allowed"] is False

    # Historical symlink fan-in remains readable from archive. The R5.7.4-only
    # bundles live inside the archive; the R4.5 selected-smoke bundles remain
    # authoritative active representation artifacts and are referenced through
    # updated relative symlinks.
    for link in (archive_root / "r5_7_4_adjudication_baseline_bundles/bundles").iterdir():
        assert link.is_symlink(), link
        assert link.exists(), link
