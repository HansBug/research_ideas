from __future__ import annotations

import json
import zipfile
from collections import Counter
from pathlib import Path

# R5 tests intentionally include snapshot counts for the current frozen seed_library
# census. If seed_library entries/assets/pairs change in later PRs, rerun
# `paper_stm_repair_smoke.cli run-seed-sweep` and update these numbers together
# with the committed sweep artifacts; do not silently relax the evidence contract.

def repo_root() -> Path:
    cur = Path(__file__).resolve()
    for parent in [cur, *cur.parents]:
        if (parent / ".git").exists() and (parent / "project_1_llm_state_machine_modeling").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = repo_root()
READINESS = ROOT / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_index_payloads():
    index = load(READINESS / "seed_sweep/records_index.json")
    payloads = []
    for record in index["records"]:
        if record.get("path_on_disk"):
            payloads.append(load(ROOT / record["path_on_disk"]))
        else:
            with zipfile.ZipFile(ROOT / record["archive_path"]) as zf:
                payloads.append(json.loads(zf.read(record["path_in_zip"]).decode("utf-8")))
    return payloads


def test_selected_smoke_report_contract():
    report = load(READINESS / "selected_examples/smoke_report.json")
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
        record = READINESS / "selected_examples/smoke_records" / f"{item['example_id']}.json"
        assert record.exists()


def test_seed_sweep_denominator_and_archive_contract():
    report = load(READINESS / "seed_sweep/sweep_report.json")
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
    manifest = load(READINESS / "artifact_archives/archive_manifest.json")
    assert manifest["schema_version"] == "r5.archive_manifest.v0"
    assert manifest["policy"]["archive_path_base"] == "repository_root"
    assert len(manifest["archives"]) == 2
    for archive in manifest["archives"]:
        path = ROOT / archive["archive_path"]
        assert path.exists()
        with zipfile.ZipFile(path) as zf:
            assert len([n for n in zf.namelist() if n.endswith(".json")]) == archive["record_count"]


def test_records_index_recomputes_pair_and_asset_counts():
    report = load(READINESS / "seed_sweep/sweep_report.json")
    index = load(READINESS / "seed_sweep/records_index.json")
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
        doc = load(READINESS / "handoff" / name)
        assert doc["schema_version"] == "r5.handoff.v0"
        assert doc["repair_contribution_allowed"] is False
        assert "STM_k" not in json.dumps(doc, ensure_ascii=False)


def test_validate_reports_no_llm_or_env_boundary():
    from paper_stm_repair_smoke.cli import load_index_payloads as cli_load_index_payloads
    from paper_stm_repair_smoke.cli import validate_no_llm_or_env_boundary

    index = load(READINESS / "seed_sweep/records_index.json")
    handoff_docs = {
        name: load(READINESS / "handoff" / name)
        for name in [
            "r5_to_r6_repair_inputs.json",
            "r5_to_r7_seed_eligibility.json",
            "r5_to_r8_negative_evidence.json",
        ]
    }
    errors: list[str] = []
    report = validate_no_llm_or_env_boundary(errors, cli_load_index_payloads(index), handoff_docs)
    assert errors == []
    assert report["status"] == "ok"
    assert "env_access" in report["forbidden_code_patterns"]
    assert "provider_usage" in report["forbidden_runtime_keys"]


def test_handoff_counts_match_seed_sweep_records():
    payloads = load_index_payloads()
    pair_payloads = [p for p in payloads if p["schema_version"] == "r5.seed_sweep_pair_record.v0"]
    pair_counts = Counter(p["status"] for p in pair_payloads)

    r6 = load(READINESS / "handoff/r5_to_r6_repair_inputs.json")
    assert r6["summary"]["converted"] == pair_counts["converted"]
    assert len(r6["items"]) == pair_counts["converted"]

    r7 = load(READINESS / "handoff/r5_to_r7_seed_eligibility.json")
    assert r7["summary"]["converted"] == pair_counts["converted"]
    assert r7["summary"]["partial"] == pair_counts["partial"]
    assert "partial_items" not in r7
    assert r7["sample_truncated"] == {"converted": True, "partial": True}
    assert len(r7["converted_sample"]) == r7["sample_counts"]["converted_sample"] == 50
    assert len(r7["partial_sample"]) == r7["sample_counts"]["partial_sample"] == 100
    assert r7["full_list_via"]["records_index"].endswith("records_index.json")

    r8 = load(READINESS / "handoff/r5_to_r8_negative_evidence.json")
    expected_negative = dict(Counter(p["status"] for p in pair_payloads if p["status"] in {"blocked", "missing_asset", "not_applicable", "needs_generation"}))
    assert r8["summary"] == expected_negative


def test_sampling_markdown_uses_pr_body_contract():
    text = (READINESS / "seed_sweep/sampling_analysis.md").read_text(encoding="utf-8")
    assert "Migration notice" in text
    assert "2026-06-28-04-03-18-seed-readiness-report.md" in text
    assert "sweep_report.json" in text
    assert "records_index.json" in text
    partial_cases = (READINESS / "seed_sweep/partial_cases.md").read_text(encoding="utf-8")
    assert "Migration notice" in partial_cases
    assert "2026-06-28-04-03-18-seed-readiness-report.md" in partial_cases


def load_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_r55_llms_emp_deep_profile_contract():
    base = READINESS / "llms_emp_profile"
    cases = load_jsonl(base / "llms_emp_case_matrix.jsonl")
    clusters = load_jsonl(base / "llms_emp_cluster_profiles.jsonl")
    matrix = load_jsonl(base / "llms_emp_cluster_llm_matrix.jsonl")
    partials = load_jsonl(base / "llms_emp_partial_attribution_ledger.jsonl")
    blocked = load_jsonl(base / "llms_emp_blocked_probe.jsonl")

    assert len(cases) == 60
    assert len(clusters) == 10
    assert len(matrix) == 60
    assert len(partials) == 44
    assert len(blocked) == 0
    assert Counter(row["conversion_status"] for row in cases) == {"converted": 16, "partial": 44}
    assert Counter(row["time_level"] for row in clusters) == {"T0": 8, "T0.5": 1, "T1": 1}
    assert Counter(row["r5_6_story_role"] for row in clusters) == {"main_candidate": 9, "supplementary_stress": 1}

    for cluster in clusters:
        features = cluster["behavior_feature_profile"]
        for key in [
            "has_guard_like_condition",
            "has_action_or_entry_exit",
            "has_variables_or_data_conditions",
            "has_hierarchy",
            "has_pseudostate",
            "has_explicit_time",
        ]:
            assert key in features, cluster["nl_cluster_id"]
    assert sum(1 for c in clusters if c["behavior_feature_profile"]["has_explicit_time"]) == 2
    assert sum(1 for c in clusters if c["behavior_feature_profile"]["has_guard_like_condition"]) == 10

    for cluster_id in {row["nl_cluster_id"] for row in clusters}:
        rows = [row for row in matrix if row["nl_cluster_id"] == cluster_id]
        assert len(rows) == 6
        assert {row["llm_family"] for row in rows} == {"gpt-4o", "gpt-4", "llama", "kimi", "deepseek", "claude"}

    for row in partials:
        assert row["conversion_status"] == "partial"
        assert row["observed_issue"]
        assert row["source_stage"]
        assert row["r5_loss_code"]
        assert row["evidence_anchor"]
        assert row["attribution_confidence"] in {"high", "medium", "low", "unknown"}
        assert row["r5_6_story_role"] in {"main_candidate", "supplementary_stress", "negative_evidence", "exclude_or_defer", "unknown"}

    recovered_from_blocked = {
        row["raw_pair_id"]: row
        for row in cases
        if row["raw_pair_id"] in {
            "llms_emp_stm_results_0018",
            "llms_emp_stm_results_0028",
            "llms_emp_stm_results_0037",
        }
    }
    assert set(recovered_from_blocked) == {
        "llms_emp_stm_results_0018",
        "llms_emp_stm_results_0028",
        "llms_emp_stm_results_0037",
    }
    for row in recovered_from_blocked.values():
        assert row["conversion_status"] == "partial"
        assert row["canonical_status"] == "converted"
        assert row["parse_status"] == "ok"
        assert row["inspect_status"] == "ok"
        assert "R5.LOSS.r3_1_normalization_replay_not_repair" in row["r5_loss_codes"]
        assert row["repair_contribution_allowed"] is False

    deep_text = (base / "llms_emp_deep_profile.md").read_text(encoding="utf-8")
    assert "Migration notice" in deep_text
    assert "2026-06-29-00-03-56-llms-emp-main-seed-profile.md" in deep_text
    for name in [
        "llms_emp_case_matrix.jsonl",
        "llms_emp_cluster_profiles.jsonl",
        "llms_emp_cluster_llm_matrix.jsonl",
        "llms_emp_partial_attribution_ledger.jsonl",
        "llms_emp_blocked_probe.jsonl",
    ]:
        assert name in deep_text
    handoff = (base / "llms_emp_r56_handoff.md").read_text(encoding="utf-8")
    assert "Migration notice" in handoff
    assert "2026-06-28-22-54-39-model-scope-handoff.md" in handoff
