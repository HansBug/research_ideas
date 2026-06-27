from __future__ import annotations

import json
import zipfile
from collections import Counter
from pathlib import Path

def repo_root() -> Path:
    cur = Path(__file__).resolve()
    for parent in [cur, *cur.parents]:
        if (parent / ".git").exists() and (parent / "project_1_llm_state_machine_modeling").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = repo_root()
SMOKE = ROOT / "project_1_llm_state_machine_modeling/paper_stm_repair/smoke"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_index_payloads():
    index = load(SMOKE / "seed_library_sweep/records_index.json")
    payloads = []
    for record in index["records"]:
        if record.get("path_on_disk"):
            payloads.append(load(ROOT / record["path_on_disk"]))
        else:
            with zipfile.ZipFile(ROOT / record["archive_path"]) as zf:
                payloads.append(json.loads(zf.read(record["path_in_zip"]).decode("utf-8")))
    return payloads


def test_selected_smoke_report_contract():
    report = load(SMOKE / "selected_examples/smoke_report.json")
    assert report["schema_version"] == "r5.selected_smoke_report.v0"
    assert report["repair_contribution_allowed"] is False
    assert report["generation_context"]["generator_cli_sha256"]
    assert report["generation_context"]["schema_sha256"]
    assert len(report["items"]) == 4
    counts = Counter(item["status"] for item in report["items"])
    assert report["summary"]["examples"] == 4
    assert report["summary"]["pass"] == counts.get("pass", 0)
    assert report["summary"]["partial"] == counts.get("partial", 0)
    assert report["summary"]["blocked"] == counts.get("blocked", 0)
    for item in report["items"]:
        assert item["status"] in {"pass", "partial", "blocked"}
        assert item["repair_contribution_allowed"] is False
        assert all(item["checks"].values()), item["example_id"]
        assert item["upstream_r45"]["direct_parse_report_status"] == item["upstream_r45"]["parse_status"]
        assert item["upstream_r45"]["direct_parse_report_inspect_status"] == item["upstream_r45"]["inspect_status"]
        record = SMOKE / "selected_examples/smoke_records" / f"{item['example_id']}.json"
        assert record.exists()


def test_seed_sweep_denominator_and_archive_contract():
    report = load(SMOKE / "seed_library_sweep/sweep_report.json")
    assert report["schema_version"] == "r5.seed_sweep_report.v0"
    assert report["meta"]["entry_dir_count"] == 36
    assert report["meta"]["registry_entry_count"] == 16
    assert report["meta"]["unregistered_entry_count"] == 20
    assert set(report["meta"]["excluded_non_entry_dirs"]) == {"schemas", "tools"}
    assert len(report["entries"]) == report["meta"]["entry_dir_count"]
    assert report["summary"]["entry_status_counts"] == dict(Counter(e["primary_entry_status"] for e in report["entries"]))
    assert report["summary"]["pair_records_total"] == 1078
    assert report["meta"]["generation_context"]["generator_cli_sha256"]
    assert report["meta"]["generation_context"]["schema_sha256"]
    manifest = load(SMOKE / "seed_library_sweep/archive_manifest.json")
    assert manifest["schema_version"] == "r5.archive_manifest.v0"
    assert len(manifest["archives"]) == 2
    for archive in manifest["archives"]:
        path = ROOT / archive["archive_path"]
        assert path.exists()
        with zipfile.ZipFile(path) as zf:
            assert len([n for n in zf.namelist() if n.endswith(".json")]) == archive["record_count"]


def test_records_index_recomputes_pair_and_asset_counts():
    report = load(SMOKE / "seed_library_sweep/sweep_report.json")
    index = load(SMOKE / "seed_library_sweep/records_index.json")
    assert len(index["records"]) == 1094
    index_type_counts = Counter(r["record_type"] for r in index["records"])
    assert index_type_counts == {"pair": 1078, "asset": 16}

    payloads = load_index_payloads()
    pair_payloads = [p for p in payloads if p["schema_version"] == "r5.seed_sweep_pair_record.v0"]
    asset_payloads = [p for p in payloads if p["schema_version"] == "r5.seed_sweep_asset_record.v0"]
    assert len(pair_payloads) == report["summary"]["pair_records_total"]
    assert len(asset_payloads) == report["summary"]["asset_records_total"]
    assert dict(Counter(p["status"] for p in pair_payloads)) == report["summary"]["pair_status_counts"]
    assert dict(Counter(p["status"] for p in asset_payloads)) == report["summary"]["asset_status_counts"]

    pair_by_entry = Counter(p["entry_id"] for p in pair_payloads)
    asset_by_entry = Counter(p["entry_id"] for p in asset_payloads)
    for entry in report["entries"]:
        assert pair_by_entry[entry["entry_id"]] == entry["pair_record_count"]
        assert asset_by_entry[entry["entry_id"]] == entry["asset_record_count"]


def test_handoff_files_are_pre_repair_only():
    for name in [
        "r5_to_r6_repair_inputs.json",
        "r5_to_r7_seed_eligibility.json",
        "r5_to_r8_negative_evidence.json",
    ]:
        doc = load(SMOKE / "handoff" / name)
        assert doc["schema_version"] == "r5.handoff.v0"
        assert doc["repair_contribution_allowed"] is False
        assert "STM_k" not in json.dumps(doc, ensure_ascii=False)


def test_handoff_counts_match_seed_sweep_records():
    payloads = load_index_payloads()
    pair_payloads = [p for p in payloads if p["schema_version"] == "r5.seed_sweep_pair_record.v0"]
    pair_counts = Counter(p["status"] for p in pair_payloads)

    r6 = load(SMOKE / "handoff/r5_to_r6_repair_inputs.json")
    assert r6["summary"]["converted"] == pair_counts["converted"]
    assert len(r6["items"]) == pair_counts["converted"]

    r7 = load(SMOKE / "handoff/r5_to_r7_seed_eligibility.json")
    assert r7["summary"]["converted"] == pair_counts["converted"]
    assert r7["summary"]["partial"] == pair_counts["partial"]

    r8 = load(SMOKE / "handoff/r5_to_r8_negative_evidence.json")
    expected_negative = dict(Counter(p["status"] for p in pair_payloads if p["status"] in {"blocked", "missing_asset", "not_applicable", "needs_generation"}))
    assert r8["summary"] == expected_negative
